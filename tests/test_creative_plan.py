import json
from copy import deepcopy
from pathlib import Path
import hashlib
import pytest
from integrations.content_intelligence.creative_plan import PlanStore, validate_proposal, plan_blockers
from integrations.content_intelligence.adapter import IntakeStore, dispatch
from integrations.content_intelligence.host import HostConfig, NativeHost
from tests.creative_fixture import approved_fixture, proposal
from tests.test_stage_execution import draft, critic


@pytest.fixture
def setup(tmp_path):
    packet=json.loads((Path(__file__).parents[1]/'integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json').read_text(encoding='utf8'))
    approved,assets,store=approved_fixture(packet,tmp_path)
    context=dict(schema_version='reelo.execution-context.1',packet=packet)
    return packet,context,approved,assets,store


@pytest.mark.parametrize('field',['angle_id','packet_id','verified_insight_id'])
def test_cannot_replace_upstream_identity(setup,field):
    _,c,a,assets,_=setup
    raw=deepcopy(a['plan']['proposal']);raw[field]='invented'
    with pytest.raises(ValueError,match='identity'):validate_proposal(raw,c,assets)


def test_no_customer_truth_field_allowed(setup):
    _,c,a,assets,_=setup
    raw=deepcopy(a['plan']['proposal']);raw['new_customer_pain']='invented'
    with pytest.raises(ValueError):validate_proposal(raw,c,assets)


@pytest.mark.parametrize('group',['story_matches','knowledge_matches'])
def test_nonexistent_source_rejected(setup,group):
    _,c,a,assets,_=setup;raw=deepcopy(a['plan']['proposal'])
    raw[group]=[dict(source_ref='/missing',sha256='x',section='one',origin='external_knowledge',why_relevant='x',allowed_use='x')]
    with pytest.raises(ValueError,match='source_origin'):validate_proposal(raw,c,assets)


def test_external_cannot_become_creator(setup,tmp_path):
    _,c,a,assets,_=setup;raw=deepcopy(a['plan']['proposal'])
    wiki=tmp_path/'wiki/source.md';wiki.parent.mkdir();wiki.write_text('External source')
    h=hashlib.sha256(wiki.read_bytes()).hexdigest();assets.append(dict(path=wiki.as_posix(),sha256=h))
    raw['story_matches']=[dict(source_ref=wiki.as_posix(),sha256=h,section='one',origin='creator_story',why_relevant='x',allowed_use='x')]
    with pytest.raises(ValueError,match='source_origin'):validate_proposal(raw,c,assets)


def test_illustration_requires_origin_and_visible_disclosure(setup):
    _,c,a,assets,_=setup;raw=deepcopy(a['plan']['proposal'])
    raw['illustrations']=[dict(description='Hypothetical scene',origin='illustrative_ai',disclosure='')]
    with pytest.raises(ValueError,match='disclosure'):validate_proposal(raw,c,assets)
    raw['illustrations'][0]['disclosure']='SYNTHETIC illustration, not a real experience'
    assert validate_proposal(raw,c,assets)['illustrations']


@pytest.mark.parametrize('group,check',[('hook_candidates','intent_preserved'),('title_candidates','intent_preserved'),
 ('title_candidates','natural_and_meaningful'),('title_candidates','factual_claims_supported')])
def test_flagged_semantic_candidate_blocks_approval(setup,group,check):
    _,c,a,assets,store=setup;raw=deepcopy(a['plan']['proposal']);raw[group][0][check]=False
    p=store.save(raw,c,assets,'SYNTHETIC-new')
    assert p['blockers']
    with pytest.raises(ValueError,match='blocked_plan'):
        store.review(p['creative_plan_id'],dict(decision='approved',reviewer='Tester',human_attested=True,expected_plan_hash=p['plan_hash']))


@pytest.mark.parametrize('check',['truth_preserved','selected_intent_preserved','reader_centered_pov','non_prescriptive_tone'])
def test_flagged_plan_semantics_cannot_pass(setup,check):
    p=deepcopy(setup[2]['plan']['proposal']);p[check]=False
    assert check in plan_blockers(p)


def test_library_required_not_invented_psychology(setup):
    _,c,a,assets,_=setup;raw=deepcopy(a['plan']['proposal']);raw['psychology']['library_source']='/new-library'
    with pytest.raises(ValueError,match='psychology'):validate_proposal(raw,c,assets)


def test_library_label_whitespace_is_not_semantic_change(setup):
    _,c,a,assets,_=setup;raw=deepcopy(a['plan']['proposal'])
    raw['psychology']['primary_mechanism']='Synthetic   mechanism'
    assert validate_proposal(raw,c,assets)['psychology']['primary_mechanism']=='Synthetic   mechanism'
    raw['psychology']['primary_mechanism']='Invented mechanism'
    with pytest.raises(ValueError,match='not_in_library'):validate_proposal(raw,c,assets)


def test_changed_plan_invalidates_approval(setup):
    _,c,a,assets,store=setup
    p=deepcopy(a['plan']['proposal']);p['outline']=['Changed expression']
    store.save(p,c,assets,'new-generation')
    with pytest.raises(ValueError,match='current'):store.approved(a['approval_id'],c,assets)


def test_one_gate_select_edit_and_persist(setup):
    _,c,a,assets,store=setup;p=a['plan']
    review=store.review(p['creative_plan_id'],dict(decision='approved',reviewer='SYNTHETIC TEST editor',
        approval_kind='synthetic_fixture',human_attested=True,expected_plan_hash=p['plan_hash'],hook_id='h2',title_id='t2',
        edited_hook='Edited synthetic hook',edited_title='Edited synthetic title',edited_outline=['Edited synthetic outline']))
    persisted=store.approved(review['approval_id'],c,assets)
    assert persisted['selected_hook']['text']=='Edited synthetic hook'
    assert persisted['selected_title']['text']=='Edited synthetic title'
    assert persisted['approved_outline']==['Edited synthetic outline']
    with pytest.raises(ValueError):store.approved(a['approval_id'],c,assets)


@pytest.mark.parametrize('decision',['rejected','deferred'])
def test_reject_defer_revokes_previous_approval(setup,decision):
    _,c,a,assets,store=setup;p=a['plan']
    r=store.review(p['creative_plan_id'],dict(decision=decision,reviewer='Test human',human_attested=True,expected_plan_hash=p['plan_hash']))
    for ident in [a['approval_id'],r['approval_id']]:
        with pytest.raises(ValueError):store.approved(ident,c,assets)


def test_source_change_invalidates(setup):
    _,c,a,assets,store=setup;Path(assets[0]['path']).write_text('Changed')
    with pytest.raises(ValueError,match='source_changed'):store.approved(a['approval_id'],c,assets)


def test_one_planner_call_stops_before_writer(setup,tmp_path,monkeypatch):
    packet,c,a,assets,_=setup
    monkeypatch.setattr(HostConfig,'verify',lambda s:None)
    host=NativeHost(HostConfig(tmp_path/'cli',tmp_path,tmp_path/'runs',tuple(Path(x['path']) for x in assets)))
    calls=[]
    def invoke(execution,context,stage,inputs,work,refs):
        assert context==c and stage['stage_type']=='CREATIVE_PLAN'
        assert 'plan_schema' in inputs
        calls.append(stage)
        return dict(schema_version='reelo.host-stage.1',stage=stage,output=a['plan']['proposal']),dict(task_id='p',tool_use_id='p')
    monkeypatch.setattr(host,'invoke_stage',invoke)
    result=dispatch(IntakeStore(tmp_path/'intake'),packet,request_id='plan',authorize_current=lambda p:None,launch=host)
    assert result.status=='PLAN_PENDING_APPROVAL' and len(calls)==1 and not result.artifacts
    assert result.human_approval=='PENDING'


def test_unknown_approval_never_invokes_writer(setup,tmp_path,monkeypatch):
    packet,c,a,assets,_=setup
    monkeypatch.setattr(HostConfig,'verify',lambda s:None)
    host=NativeHost(HostConfig(tmp_path/'cli',tmp_path,tmp_path/'runs',tuple(Path(x['path']) for x in assets)),approval_id='missing')
    monkeypatch.setattr(host,'invoke_stage',lambda *a:pytest.fail('must not launch'))
    result=dispatch(IntakeStore(tmp_path/'intake'),packet,request_id='write',authorize_current=lambda p:None,launch=host)
    assert result.status=='UNKNOWN' and 'human_creative_approval_required' in result.validation_issues


def test_same_approved_plan_to_every_stage(setup,tmp_path,monkeypatch):
    packet,c,a,assets,_=setup
    monkeypatch.setattr(HostConfig,'verify',lambda s:None)
    host=NativeHost(HostConfig(tmp_path/'cli',tmp_path,tmp_path/'runs',tuple(Path(x['path']) for x in assets)),approval_id=a['approval_id'])
    queue=[draft(packet),critic(True),draft(packet),critic()]; seen=[]
    def invoke(execution,context,stage,inputs,work,refs):
        assert inputs['approved_plan']==a and context==c;seen.append(stage['stage_type'])
        return dict(schema_version='reelo.host-stage.1',stage=stage,output=queue.pop(0)),dict(task_id='s',tool_use_id='s')
    monkeypatch.setattr(host,'invoke_stage',invoke)
    result=dispatch(IntakeStore(tmp_path/'intake'),packet,request_id='write',authorize_current=lambda p:None,launch=host)
    assert result.status=='DRAFT_READY' and seen==['WRITER','CRITIC1','REWRITE','CRITIC2']
    assert result.human_approval=='PENDING'


@pytest.mark.parametrize('defect',['fidelity_false','fidelity_missing','title_changed','format_changed'])
def test_plan_drift_blocks_even_reported_pass(setup,tmp_path,monkeypatch,defect):
    from tests.test_stage_execution import run
    packet=setup[0];d=draft(packet);c=critic()
    if defect=='fidelity_false':c['plan_fidelity']=False
    if defect=='fidelity_missing':c.pop('plan_fidelity')
    if defect=='title_changed':d['title']='Unapproved title'
    if defect=='format_changed':d['format']='Unapproved format'
    result,calls,_=run(packet,tmp_path,monkeypatch,[deepcopy(d),deepcopy(c),deepcopy(d),deepcopy(c)])
    assert result.status=='CRITIC_FAILED' and len(calls)==4


def test_explicit_human_attestation_required(setup):
    a,store=setup[2],setup[4];p=a['plan']
    with pytest.raises(ValueError):
        store.review(p['creative_plan_id'],dict(decision='approved',reviewer='No attestation',expected_plan_hash=p['plan_hash']))

# C5.9 findings semantics: deterministic enforcement of source-reviewed findings.
from integrations.content_intelligence.creative_plan import candidate_eligibility, review_readiness


@pytest.mark.parametrize('field', ['limitations', 'advisories', 'publication_requirements'])
def test_visible_non_blocking_findings_allow_human_gate(setup, field):
    _, context, approved, assets, store = setup
    raw = deepcopy(approved['plan']['proposal'])
    raw[field] = ['Visible unresolved finding']
    plan = store.save(raw, context, assets, 'SYNTHETIC-C5.9')
    assert not plan['blockers']
    assert not plan['review_view']['ready_to_write']
    review = store.review(plan['creative_plan_id'], dict(decision='approved', reviewer='SYNTHETIC TEST reviewer',
        human_attested=True, approval_kind='synthetic_fixture', expected_plan_hash=plan['plan_hash']))
    assert store.approved(review['approval_id'], context, assets)
    ready = review_readiness(raw, context, human_approved=True)
    assert ready['ready_to_write'] and not ready['ready_to_publish']
    assert ready['publication_blocked_by_requirements']
    assert ready[field]  # Findings remain visible, including packet publication requirements.


@pytest.mark.parametrize('field', ['issues', 'blocking_issues', 'outline_blocking_issues'])
def test_unresolved_truth_and_legacy_findings_remain_blocking(setup, field):
    _, context, approved, assets, store = setup
    raw = deepcopy(approved['plan']['proposal']); raw[field] = ['Unsupported creator/customer inference']
    plan = store.save(raw, context, assets, 'SYNTHETIC-C5.9')
    with pytest.raises(ValueError, match='blocked_plan'):
        store.review(plan['creative_plan_id'], dict(decision='approved', reviewer='Tester',
            human_attested=True, expected_plan_hash=plan['plan_hash']))


@pytest.mark.parametrize('group,key', [('hook_candidates','hook_id'), ('title_candidates','title_id')])
def test_unsafe_alternative_not_whole_plan_blocked_and_cannot_select(setup, group, key):
    _, context, approved, assets, store = setup
    raw = deepcopy(approved['plan']['proposal'])
    bad = raw[group][1]
    # Model booleans all true; an independent finding must still block selection.
    bad['blocking_reasons'] = ['Unsupported causal/creator inference after source review']
    bad['semantic_review'] = 'Source does not support this assertion'
    assert candidate_eligibility(bad)['state'] == 'blocked'
    assert candidate_eligibility(raw[group][0])['state'] == 'selectable'
    plan = store.save(raw, context, assets, 'SYNTHETIC-C5.9')
    assert not plan['blockers']
    decision = dict(decision='approved', reviewer='Tester', human_attested=True, expected_plan_hash=plan['plan_hash'])
    with pytest.raises(ValueError, match='blocked_candidate'):
        store.review(plan['creative_plan_id'], dict(**decision, **{key: bad['candidate_id']}))
    # Editing a known-blocked option cannot bypass the eligibility check.
    with pytest.raises(ValueError, match='blocked_candidate'):
        store.review(plan['creative_plan_id'], dict(**decision, **{key: bad['candidate_id'],
            'edited_hook' if key == 'hook_id' else 'edited_title': 'Replacement'}))
    assert store.review(plan['creative_plan_id'], decision)['decision'] == 'approved'


def test_none_story_and_packet_requirements_not_erased(setup):
    _, context, approved, _, _ = setup
    before = deepcopy(context)
    raw = deepcopy(approved['plan']['proposal'])
    raw['publication_requirements'] = []
    view = review_readiness(raw, context)
    assert view['story_types'] == ['NONE'] and view['ready_for_owner_review']
    assert view['publication_requirements'] and not view['ready_to_publish']
    assert context == before


@pytest.mark.parametrize('kind,supported,same,blocked', [
    ('DIRECT', False, True, True), ('DIRECT', True, True, False),
    ('ADJACENT', False, True, True), ('ADJACENT', False, False, False)])
def test_story_semantic_contract(setup, tmp_path, kind, supported, same, blocked):
    _, context, approved, assets, _ = setup
    raw = deepcopy(approved['plan']['proposal'])
    story = tmp_path/'creator-experience/story.md'; story.parent.mkdir()
    story.write_text('SYNTHETIC creator experienced event X.', encoding='utf8')
    digest = hashlib.sha256(story.read_bytes()).hexdigest()
    assets = assets + [dict(path=story.as_posix(), sha256=digest)]
    raw['story_matches'] = [dict(source_ref=story.as_posix(), sha256=digest,
        section='Synthetic event', origin='creator_story', why_relevant='Supported event X; not event Y',
        allowed_use='Only the source-supported event X, no customer situation Y', match_type=kind,
        support_quote='SYNTHETIC creator experienced event X.',
        same_situation_supported=supported, use_as_same_situation=same)]
    valid = validate_proposal(raw, context, assets)
    assert bool(plan_blockers(valid)) is blocked
    raw['story_matches'][0]['support_quote'] = 'Invented creator event Y'
    with pytest.raises(ValueError, match='story_support_not_in_source'):
        validate_proposal(raw, context, assets)


def test_approved_snapshot_cannot_mutate_stored_plan(setup):
    _, context, approved, assets, store = setup
    approved['plan']['proposal']['limitations'].append('In-memory tamper')
    with pytest.raises(ValueError, match='integrity'):
        # Direct database tampering is detected by the bound plan hash.
        with store.connect() as db:
            db.execute('UPDATE plans SET body=? WHERE plan_id=?',
                (json.dumps(approved['plan']), approved['creative_plan_id']))
        store.approved(approved['approval_id'], context, assets)


def test_real_edit_approval_keeps_mode_policy_and_plan_snapshot(setup):
    _, context, original, assets, store = setup
    plan = original['plan']
    approved = store.review(plan['creative_plan_id'], dict(decision='EDIT_AND_APPROVE',
        reviewer='Product Owner', human_attested=True, approval_kind='human',
        expected_plan_hash=plan['plan_hash'], hook_id='h1', title_id='t1',
        edited_hook='Owner exact hook', edited_title='Owner exact title',
        selected_mode='SHORT_ARTICLE', knowledge_choice_policy='Optional only when useful'))
    assert approved['decision'] == 'approved' and approved['owner_decision'] == 'EDIT_AND_APPROVE'
    assert approved['approval_kind'] == 'human'
    assert approved['selected_mode'] == 'SHORT_ARTICLE'
    assert approved['selected_hook']['text'] == 'Owner exact hook'
    assert approved['selected_title']['text'] == 'Owner exact title'
    assert approved['approved_outline'] == plan['proposal']['outline']
    assert approved['plan'] == plan and approved['publication_requirements']
    assert store.approved(approved['approval_id'], context, assets) == approved
    approved['selected_mode'] = 'REEL'
    assert store.approved(approved['approval_id'], context, assets)['selected_mode'] == 'SHORT_ARTICLE'


def test_unknown_history_still_blocks_owner_approved_new_execution(setup, tmp_path):
    packet, context, original, assets, plans = setup
    intake = IntakeStore(tmp_path/'guard.sqlite')
    receipt = intake.intake(packet)
    previous, _ = intake.reserve(receipt, 'previous-planner')
    previous.status = 'UNKNOWN'; intake.finish(previous)
    with pytest.raises(ValueError, match='reconcile_previous_execution_first'):
        intake.reserve(receipt, 'owner-approved-writer', previous.generation_id)
    assert intake.status(previous.generation_id).status == 'UNKNOWN'
