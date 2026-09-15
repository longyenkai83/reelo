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
