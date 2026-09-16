"""E1 deterministic contract/host fixtures only. No generated creative content."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import subprocess
import pytest

from integrations.content_intelligence.creative_plan import validate_proposal, plan_blockers
from integrations.content_intelligence.purified_plan import ROUTE, PurifiedPlan, title_table
from integrations.content_intelligence.context_packs import assemble, asset_id, ROOT
from integrations.content_intelligence.adapter import IntakeStore, dispatch
from integrations.content_intelligence.host import NativeHost, HostConfig
from tests.test_creative_plan import setup
from tests.purified_fixture import purified
from tests.test_stage_execution import draft, critic


@pytest.fixture
def e1(setup, tmp_path):
    packet, context, historical, assets, store = setup
    voice = tmp_path/'creator-b'/'voice-profile.md'; voice.parent.mkdir()
    voice.write_text('SYNTHETIC creator B voice', encoding='utf8')
    assets = deepcopy(assets) + [dict(path=voice.as_posix(),sha256=hashlib.sha256(voice.read_bytes()).hexdigest())]
    raw = purified(packet, Path(assets[0]['path']))
    plan = store.save(raw,context,assets,'SYNTHETIC-E1')
    approval = store.review(plan['creative_plan_id'],dict(decision='approved',reviewer='SYNTHETIC TEST E1',
        human_attested=True,approval_kind='synthetic_fixture',expected_plan_hash=plan['plan_hash']))
    return context, raw, assets, store, plan, approval


def test_none_psychology_valid_without_library_and_gate_small(e1):
    context, raw, assets, _, plan, approval = e1
    without_library = [a for a in assets if 'nguyen-ly-tam-ly' not in a['path']]
    assert validate_proposal(raw, context, without_library)['psychology'] == 'NONE'
    gate = plan['review_view']['integrated_plan']
    assert 'compatibility_titles' not in gate and 'candidates' not in plan['review_view']
    assert gate['opening_plan']['alternative'] is None and gate['title_plan']['alternative'] is None
    assert 'intent_preserved' not in gate['title_plan']['recommended']
    assert len(title_table(plan['proposal'])) == 3
    assert approval['psychology'] == 'NONE' and approval['selected_story_refs'] == []


@pytest.mark.parametrize('stage', ['CREATIVE_PLAN','WRITER','CRITIC1','REWRITE','CRITIC2'])
def test_none_never_loads_psychology_and_context_isolated(e1, stage):
    _, _, assets, _, _, approval = e1
    inputs = dict(plan_route=ROUTE) if stage == 'CREATIVE_PLAN' else dict(approved_plan=approval)
    pack, trace = assemble(stage, inputs, assets)
    assert pack['plan_route'] == ROUTE
    psy = [r for r in trace['receipts'] if r['role'] == 'PSYCHOLOGY']
    assert psy and all(r['states'] == ['ALLOWED','OMITTED'] for r in psy)
    assert 'Synthetic mechanism' not in json.dumps(pack)
    assert 'SYNTHETIC creator B voice' in json.dumps(pack)
    if stage in ('WRITER','REWRITE'):
        assert 'Synthetic third internal option' not in json.dumps(pack)
        assert pack['approved_plan']['psychology'] == 'NONE'
        assert pack['approved_plan']['plan']['proposal']['opening_plan']['alternative'] is None


def test_used_psychology_requires_stable_identity(e1):
    context, raw, assets, _, _, _ = e1
    psy = dict(primary_mechanism='Synthetic mechanism', optional_secondary_mechanism=None,
               rationale='Expression only', reference_id=asset_id(assets[0]['path']))
    raw['psychology'] = psy
    valid = validate_proposal(raw, context, assets)
    assert valid['psychology']['library_source'] == assets[0]['path']
    raw['psychology'].pop('reference_id')
    with pytest.raises(ValueError, match='psychology_reference_identity_required'):
        validate_proposal(raw,context,assets)


def test_proof_none_only_for_declared_nonfactual_reflection(e1):
    context, raw, assets, _, _, _ = e1
    raw['content_job']='REFLECT'; raw['recipe_id']='c1:REFLECT'
    raw['proof_plan']=[dict(kind='NONE',supports='A nonfactual question',requires_factual_support=False,
                            contribution='Quiet reflection')]
    assert not plan_blockers(validate_proposal(raw,context,assets))
    raw['proof_plan'][0]['requires_factual_support']=True
    with pytest.raises(ValueError,match='nonfactual_proof_cannot_support_factual_claim'):
        validate_proposal(raw,context,assets)


@pytest.mark.parametrize('kind,supported,same,blocked',[
    ('DIRECT',True,True,False),('DIRECT',False,True,True),
    ('ADJACENT',False,False,False),('ADJACENT',False,True,True)])
def test_creator_story_semantics_and_exact_support(e1,tmp_path,kind,supported,same,blocked):
    context,raw,assets,_,_,_=e1
    path=tmp_path/'creator-experience'/'story.md'; path.parent.mkdir(); path.write_text('# scene\nSYNTHETIC true quote')
    sha=hashlib.sha256(path.read_bytes()).hexdigest();assets.append(dict(path=path.as_posix(),sha256=sha))
    raw['proof_plan']=[dict(kind='CREATOR_STORY',supports='Creator event',requires_factual_support=True,
        contribution='Illustrates a distinction', source=dict(source_ref=path.as_posix(),sha256=sha,section='scene',
            origin='creator_story',why_relevant='SYNTHETIC relevance',allowed_use='Distinct experience only',
            match_type=kind,support_quote='SYNTHETIC true quote',same_situation_supported=supported,use_as_same_situation=same))]
    valid=validate_proposal(raw,context,assets)
    assert bool(plan_blockers(valid)) == blocked
    raw['proof_plan'][0]['source']['support_quote']='Invented quote'
    with pytest.raises(ValueError,match='proof_support_not_in_source'):
        validate_proposal(raw,context,assets)


@pytest.mark.parametrize('edit', ['recipe','mode','psychology','hook','outline'])
def test_consequential_revision_invalidates_without_inheriting_approval(e1,edit):
    context,raw,assets,store,plan,approval=e1
    if edit=='recipe': raw.update(content_job='REFLECT',recipe_id='c1:REFLECT')
    elif edit=='mode': raw['format']='REEL'
    elif edit=='psychology': raw['psychology']=dict(primary_mechanism='Synthetic mechanism', optional_secondary_mechanism=None,
        rationale='Expression',reference_id=asset_id(assets[0]['path']))
    elif edit=='hook': raw['opening_plan']['recommended']['text']='SYNTHETIC revised wording'
    else: raw['outline']=['SYNTHETIC revised outline']
    new=store.revise(plan['creative_plan_id'],raw,context,assets,reviewer='SYNTHETIC TEST owner',human_attested=True,
                     expected_plan_hash=plan['plan_hash'])
    assert new['plan_revision'] == plan['plan_revision']+1 and new['plan_hash'] != plan['plan_hash']
    assert new['revision_audit']['approval_inherited'] is False
    assert not new['review_view']['ready_to_write']
    with pytest.raises(ValueError,match='approval_not_current'): store.approved(approval['approval_id'],context,assets)


def test_no_model_gate_or_inline_meaning_edit(e1):
    context,raw,assets,store,plan,_=e1
    review=dict(decision='approved',reviewer='Model',human_attested=False,expected_plan_hash=plan['plan_hash'])
    with pytest.raises(ValueError): store.review(plan['creative_plan_id'],review)
    review.update(human_attested=True,reviewer='SYNTHETIC TEST',edited_hook='new')
    with pytest.raises(ValueError,match='purified_edit_requires_plan_revision'): store.review(plan['creative_plan_id'],review)
    raw['one_idea']='A different selected meaning'
    with pytest.raises(ValueError,match='upstream_owner_correction_required'):
        store.revise(plan['creative_plan_id'],raw,context,assets,reviewer='SYNTHETIC TEST',human_attested=True,
                     expected_plan_hash=plan['plan_hash'])


def test_title_eight_appendix_not_deleted_and_no_six_scores(e1):
    context,raw,assets,_,_,_=e1
    assert not {'CLEAR','RELEVANT','VALUABLE','TRUE','FELT','COMPLETE'} & set(PurifiedPlan.model_fields)
    raw['compatibility_titles']=raw['compatibility_titles'][:1]
    with pytest.raises(ValueError,match='title_eight_compatibility_table_required'):
        validate_proposal(raw,context,assets)


def test_canonical_title_overrides_are_explicit_and_narrow(e1):
    _,_,assets,_,_,approval=e1
    spec=json.loads((ROOT/'integrations/content_intelligence/semantics-a1.json').read_text(encoding='utf8'))
    assert set(spec['purified_e1_title_overrides'])=={'1','8'}
    pack,_=assemble('CRITIC1',{'approved_plan':approval},assets)
    rows=pack['knowledge']['title_compatibility']
    assert [r['id'] for r in rows]==list(range(1,9))
    for row in rows:
        assert set(row)=={'id','meaning'}
        assert row['meaning']==spec['purified_e1_title_overrides'].get(str(row['id']),spec['title_checks'][row['id']-1]['meaning'])


@pytest.mark.parametrize('decision',['rejected','deferred'])
def test_e1_reject_defer_revoke_current_approval(e1,decision):
    context,_,assets,store,plan,approval=e1
    store.review(plan['creative_plan_id'],dict(decision=decision,reviewer='SYNTHETIC TEST',
        human_attested=True,expected_plan_hash=plan['plan_hash']))
    with pytest.raises(ValueError,match='approval_not_current'):store.approved(approval['approval_id'],context,assets)


@pytest.mark.parametrize('defect',['PLAN','PROSE','title','hook','missing_repair'])
def test_terminal_repair_route_and_component_locks(e1,tmp_path,monkeypatch,defect):
    context,_,assets,_,_,approval=e1;packet=context['packet']
    monkeypatch.setattr(HostConfig,'verify',lambda _:None)
    host=NativeHost(HostConfig(tmp_path/'cli',tmp_path,tmp_path/'runs',tuple(Path(a['path']) for a in assets)),approval_id=approval['approval_id'])
    d=draft(packet);d['format']='SHORT_ARTICLE'
    if defect=='title': d['title']='Unapproved'
    if defect=='hook': d['content']='Unapproved opening'
    c=critic()
    if defect=='missing_repair': c['plan_fidelity']=False
    if defect in ('PLAN','PROSE'):
        c['findings']=[dict(category='creative_quality',severity='blocking',message='Story has no useful payoff',
            affected_text='SYNTHETIC passage',why='Does not contribute to the approved purpose',repair_layer=defect,evidence_refs=[])]
    queue=[d,c,deepcopy(d),critic()];calls=[]
    def invoke(execution,ctx,stage,inputs,work,refs):
        calls.append(stage['stage_type'])
        return dict(schema_version='reelo.host-stage.1',stage=stage,output=queue.pop(0)),dict(task_id='mock',tool_use_id='mock')
    monkeypatch.setattr(host,'invoke_stage',invoke)
    result=dispatch(IntakeStore(tmp_path/'intake'),packet,request_id='E1',authorize_current=lambda _:None,launch=host)
    if defect=='missing_repair':
        assert calls==['WRITER','CRITIC1'] and result.status=='UNKNOWN'
        assert 'purified_critic_actionable_findings_required' in result.validation_issues
    elif defect=='PLAN':
        assert calls==['WRITER','CRITIC1'] and result.status=='CRITIC_FAILED'
    elif defect=='PROSE':
        assert calls==['WRITER','CRITIC1','REWRITE','CRITIC2'] and result.status=='DRAFT_READY'
    else:
        assert len(calls)==4 and result.status=='CRITIC_FAILED'
        assert 'selected_'+defect+'_changed' in result.validation_issues
    assert result.human_approval=='PENDING'


@pytest.mark.parametrize('stage',['CREATIVE_PLAN','WRITER','CRITIC1','REWRITE'])
def test_e1_actual_agent_prompt_and_schema(e1,stage):
    context,_,assets,_,_,approval=e1
    inputs=dict(plan_route=ROUTE,plan_schema=PurifiedPlan.model_json_schema(),draft={'format':'SHORT_ARTICLE'},critic={'findings':[]})
    if stage!='CREATIVE_PLAN':inputs['approved_plan']=approval
    pack,_=assemble(stage,inputs,assets)
    bound=dict(context=context,execution={'receipt':{}},assets=[],inputs=inputs,stage={'stage_type':stage},context_pack=pack)
    code="""
const fs=require('fs'),vm=require('vm');const b=JSON.parse(fs.readFileSync(0,'utf8'));
const s=fs.readFileSync('.claude/workflows/batch-content.js','utf8').replace('export const meta','const meta');
const calls=[];const e={args:[],V2_BOUND:b,log:()=>{},agent:async(p,o)=>{calls.push({p,o});return {synthetic:true}}};
(async()=>{await vm.runInNewContext('(async()=>{'+s+'})()',e);process.stdout.write(JSON.stringify(calls))})();
"""
    calls=json.loads(subprocess.run(['node','-e',code],input=json.dumps(bound),text=True,encoding='utf8',capture_output=True,cwd=ROOT,check=True).stdout)
    assert len(calls)==1
    prompt=calls[0]['p']; assert 'psychology NONE is valid' in prompt
    assert 'Do not choose new psychology, job, recipe, Story' in prompt
    assert 'never six numeric scores' in prompt
    if stage=='CREATIVE_PLAN':assert 'Defaults: at least 8 hook' not in prompt
    if stage in ('WRITER','REWRITE'):assert 'Synthetic third internal option' not in prompt
    if stage=='CRITIC1':
        schema=calls[0]['o']['schema']
        assert schema['properties']['title_criteria']['minItems']==8
        assert 'repair_layer' in schema['properties']['findings']['items']['required']
