"""Synthetic campaign authority and native-boundary fixtures; never real owner approval."""
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path
import pytest

from integrations.journey.models import CampaignRequest, Source, JourneyPlan, STAGES, legacy_meaning
from integrations.journey.strategy import propose_flow, slot_context, verify_sources
from integrations.journey.store import CampaignStore
from integrations.journey.engine import JourneyEngine
from integrations.content_intelligence.contract import value_hash
from integrations.content_intelligence.purified_plan import validate
from integrations.content_intelligence.context_packs import assemble, ROOT
from tests.test_stage_execution import critic


def source(tmp, kind='CREATOR_STORY', sid='s1', creator='test-creator'):
    path = tmp/(sid+'.md')
    path.write_text('# selected\nSYNTHETIC source fact '+sid+'\n# unrelated\nDO NOT LOAD', encoding='utf8')
    return Source(source_id=sid, creator_id=creator, kind=kind, path=path.as_posix(),
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(), section='selected',
        summary='SYNTHETIC relevant source '+sid, topics=['test-topic'], provenance='SYNTHETIC fixture', truth_type='OBSERVED')


def request(**changes):
    return CampaignRequest.model_validate(dict(dict(campaign_id='test-campaign', creator_id='test-creator',
        campaign_goal='SYNTHETIC understand a practical approach', audience_scope='SYNTHETIC intended readers, not observed facts',
        starting_awareness_stage='UNAWARE', target_awareness_stage='SOLUTION_AWARE', content_count=3,
        autonomy_mode='AUTOPILOT', route='STORY_LED', topics=['test-topic'], timing='SYNTHETIC next week',
        allowed_cta_intents=['REFLECT','ENGAGE','LEARN_METHOD'], modes=['SHORT_ARTICLE'],
        boundaries=['No ungrounded claims. No publication.']), **changes))


def candidate(cid, text):
    return dict(candidate_id=cid, text=text, rationale='SYNTHETIC expression', evidence_refs=[],
                intent_preserved=True, factual_claims_supported=True, natural_and_meaningful=True)


def proposal(context):
    slot = context['slot']; packet = context['packet']
    proofs=[]
    mapping={'CREATOR_STORY':('CREATOR_STORY','creator_story'), 'CREATOR_KNOWLEDGE_POV':('CREATOR_KNOWLEDGE','creator_observation'),
             'EXTERNAL_KNOWLEDGE':('EXTERNAL_KNOWLEDGE','external_knowledge'),
             'OFFER_BUSINESS_CONTEXT':('BUSINESS_CONTEXT','business_context'), 'CLIENT_STORY':('CLIENT_STORY','client_story')}
    for s in context['sources']:
        kind, origin = mapping[s['kind']]
        proofs.append(dict(kind=kind, supports='SYNTHETIC selected fact', requires_factual_support=True,
            contribution='SYNTHETIC relevant contribution', source=dict(source_ref=s['path'],sha256=s['sha256'], section=s['section'],
            origin=origin, why_relevant='SYNTHETIC topic relevance', allowed_use='SYNTHETIC limited example',
            match_type='ADJACENT',support_quote='SYNTHETIC source fact '+s['source_id'])))
    if packet:
        proofs.append(dict(kind='CUSTOMER_EVIDENCE',supports='SYNTHETIC insight',requires_factual_support=True,
            evidence_ids=[packet['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_id']],contribution='SYNTHETIC insight'))
    return dict(schema_version='reelo.journey-creative-plan.1', campaign_id=context['campaign']['campaign_id'],
        slot_id=slot['slot_id'], context_hash=value_hash(context),
        packet_id=packet['packet_id'] if packet else None,
        verified_insight_id=packet['customer_truth']['verified_insight']['verified_insight_id'] if packet else None,
        angle_id=packet['content_strategy']['angle']['angle_id'] if packet else None,
        truth_type='PROPOSED',format=slot['mode'],one_idea=slot['one_idea'],content_job=slot['content_job'],recipe_id=slot['recipe_id'],
        reader_value=['SYNTHETIC useful meaning'],proof_plan=proofs,
        emotional_movement=dict(start_state='Question',tension_or_question='SYNTHETIC question',end_state='Clarity'),
        opening_plan=dict(recommended=candidate('h1','SYNTHETIC opening.')),
        title_plan=dict(recommended=candidate('t1','SYNTHETIC title')),
        outline=['SYNTHETIC exact source and useful reflection'],payoff='SYNTHETIC useful distinction',
        cta_direction=slot['cta_intent'],psychology='NONE',
        publication_requirements=[r['strategy_field'] for r in packet['external_evidence_requirements']] if packet else [],
        safety=dict.fromkeys(['truth_preserved','selected_intent_preserved','reader_centered_pov','non_prescriptive_tone','reader_value_clear','narrative_payoff_clear'],True),
        compatibility_titles=[dict(candidate=candidate('t2','SYNTHETIC second title'),frame='SELF_MADE'),
                              dict(candidate=candidate('t3','SYNTHETIC third title'),frame='SELF_MADE')])


class Provider:
    def __init__(self, rewrite=False, hard=False): self.calls=[]; self.rewrite=rewrite; self.hard=hard
    def __call__(self, execution, context, stage, inputs, work, assets):
        self.calls.append(deepcopy(dict(stage=stage,context=context,inputs=inputs)))
        # Exercise real D1 projection and independent asset loading too.
        pack, trace=assemble(stage['stage_type'],inputs,assets)
        assert not pack['missing_context']
        if stage['stage_type']=='CREATIVE_PLAN': out=proposal(context)
        elif stage['stage_type'] in ('WRITER','REWRITE'):
            p=inputs['approved_plan']; packet=context['packet']
            out=dict(status='DRAFT',title=p['selected_title']['text'],content=p['selected_hook']['text']+' SYNTHETIC body.',
                format=p['selected_mode'],issues=[],customer_evidence_ids=[packet['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_id']] if packet else [],
                external_dispositions=[dict(strategy_field=r['strategy_field'],disposition='omitted',explanation='Not asserted') for r in packet['external_evidence_requirements']] if packet else [],
                source_ids=context['source_ids'],source_notes=['SYNTHETIC metadata only'])
        else:
            out=critic()
            if (self.rewrite and stage['stage_type']=='CRITIC1') or self.hard:
                out['findings']=[dict(category='scope_broadening' if self.hard else 'creative_quality', severity='blocking',
                    message='SYNTHETIC repair',evidence_refs=[],affected_text='body',why='SYNTHETIC issue',repair_layer='PROSE')]
        return dict(schema_version='reelo.host-stage.1',stage=stage,output=out),dict(task_id='synthetic-task',tool_use_id='synthetic-tool')


def engine(tmp, plan, provider=None, current_insight=None):
    store=CampaignStore(tmp/'state.sqlite'); digest=store.save(plan)
    voice=tmp/'voice-profile.md';voice.write_text('SYNTHETIC selected creator voice',encoding='utf8')
    provider=provider or Provider()
    return JourneyEngine(store,tmp/'runs',provider,[voice],current_insight=current_insight),digest,provider


def authorize(e,d):
    e.store.decide(d,'AUTHORIZE_AUTOPILOT',reviewer='SYNTHETIC owner',human_attested=True,authority_ref='SYNTHETIC test authorization')


def test_five_stages_crosswalk_not_exact_and_hot_ambiguous():
    assert len(STAGES)==5
    for name in ('cold','warm','hot_pre_purchase','hot_sale_library','sell'):
        assert legacy_meaning(name)['exact'] is False
    with pytest.raises(ValueError,match='ambiguous_hot'):legacy_meaning('hot')


def test_ten_piece_flow_cta_prior_context_fuel_and_goal(tmp_path):
    sources=[source(tmp_path),source(tmp_path,'CREATOR_KNOWLEDGE_POV','k1'),source(tmp_path,'OFFER_BUSINESS_CONTEXT','offer')]
    r=request(content_count=10,route='AUTO_DISCOVERY',target_awareness_stage='MOST_AWARE',
        offer_context=dict(source_id='offer',intended_next_step='SYNTHETIC apply'),
        allowed_cta_intents=['REFLECT','ENGAGE','LEARN_METHOD','EXPLORE_OFFER','BOOK_BUY_APPLY'])
    p=propose_flow(r,sources)
    assert len(p.sequence)==10
    assert p.sequence[0].cta_intent=='REFLECT' and p.sequence[-1].cta_intent=='BOOK_BUY_APPLY'
    assert p.sequence[-1].dependencies==[s.slot_id for s in p.sequence[:-1]]
    assert 'slot-1' in p.sequence[1].journey_objective
    assert all(not s.supporting_sources for s in p.sequence if s.cta_intent not in ('EXPLORE_OFFER','BOOK_BUY_APPLY'))
    assert all(len(s.supporting_sources)<=2 for s in p.sequence)
    assert not p.audience_state_is_observed
    # No forced sales with the same count; start/target and source history change proposals.
    q=propose_flow(request(content_count=10,target_awareness_stage='UNAWARE'),[sources[0]])
    assert all(s.cta_intent=='REFLECT' and s.movement=='REINFORCE' for s in q.sequence)
    z=propose_flow(r,sources,history=[{'source_ids':['k1','offer']}])
    assert z.sequence[0].primary_source.source_id=='s1'


@pytest.mark.parametrize('route,kind',[('STORY_LED','CREATOR_STORY'),('KNOWLEDGE_POV_LED','CREATOR_KNOWLEDGE_POV'),('KNOWLEDGE_POV_LED','EXTERNAL_KNOWLEDGE'),('AUTO_DISCOVERY','CREATOR_STORY')])
def test_non_insight_routes_execute_shared_engine_without_fake_cip(tmp_path,route,kind):
    p=propose_flow(request(route=route,content_count=1),[source(tmp_path,kind)])
    e,d,provider=engine(tmp_path,p);authorize(e,d)
    result=e.execute_remaining(d)[0]
    assert result.status=='DRAFT_READY',result.validation_issues
    assert result.human_approval=='PENDING' and not result.published and result.notion_status=='NOT_SENT'
    assert [c['stage']['stage_type'] for c in provider.calls]==['CREATIVE_PLAN','WRITER','CRITIC1']
    assert all(c['context']['packet'] is None for c in provider.calls)
    assert result.artifacts[0]['writer']['customer_evidence_ids']==[]
    auth=result.host['approved_creative_plan']['authority_kind']
    assert auth['individual_human_creative_approval'] is False


@pytest.mark.parametrize('supports',[0,2])
def test_insight_expert_optional_story_and_knowledge(tmp_path,supports):
    fixture=ROOT/'integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json'
    packet=json.loads(fixture.read_text(encoding='utf8'))
    s=source(tmp_path)
    s=Source.model_validate(dict(s.model_dump(),kind='VERIFIED_INSIGHT',truth_type='DERIVED',path=fixture.as_posix(),sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),packet_id=packet['packet_id']))
    sources=[s,source(tmp_path,'CREATOR_STORY','story'),source(tmp_path,'CREATOR_KNOWLEDGE_POV','knowledge')]
    p=propose_flow(request(route='INSIGHT_LED',content_count=1),sources)
    raw=p.model_dump()
    if supports:raw['sequence'][0]['supporting_sources']=[dict(source_id=x.source_id,contribution='SYNTHETIC useful support') for x in sources[1:]]
    p=JourneyPlan.model_validate(raw);checks=[]
    e,d,provider=engine(tmp_path,p,current_insight=lambda body:checks.append(body['packet_id']));authorize(e,d)
    result=e.execute_remaining(d)[0]
    assert result.status=='DRAFT_READY',result.validation_issues
    assert len(checks)>2
    assert provider.calls[0]['context']['packet']==packet
    assert len(provider.calls[0]['context']['sources'])==supports


def test_guided_real_sample_then_remaining_campaign_only(tmp_path):
    p=propose_flow(request(autonomy_mode='GUIDED'),[source(tmp_path)])
    e,d,provider=engine(tmp_path,p)
    cp=e.prepare(d,'slot-1')
    with pytest.raises(ValueError,match='real_sample_creative_approval'):e.run(d,cp['creative_plan_id'])
    e.approve_sample_plan(d,cp['creative_plan_id'],reviewer='SYNTHETIC human',human_attested=True,authority_ref='SYNTHETIC')
    sample=e.run(d,cp['creative_plan_id']); assert sample.status=='DRAFT_READY'
    with pytest.raises(ValueError,match='explicit_campaign'): e.execute_remaining(d)
    e.store.decide(d,'APPROVE_SAMPLE',reviewer='SYNTHETIC',human_attested=True,authority_ref='SYNTHETIC',
        sample_hash=sample.artifacts[-1]['content_hash'],calibration={'tone':'SYNTHETIC quiet invitation'})
    e.store.decide(d,'EXECUTE_REMAINDER',reviewer='SYNTHETIC',human_attested=True,authority_ref='SYNTHETIC remaining two')
    results=e.execute_remaining(d)
    assert len(results)==2 and all(r.status=='DRAFT_READY' for r in results)
    assert len(provider.calls[-1]['context']['memory']['completed'])==2
    assert provider.calls[-1]['context']['memory']['calibration'][0]['scope']=='this_campaign_only'


@pytest.mark.parametrize('change,error',[('source','source_hash_changed'),('revoke','explicit_campaign'),('revision','campaign_plan_not_current')])
def test_currentness_guards_before_execution(tmp_path,change,error):
    s=source(tmp_path);p=propose_flow(request(content_count=1),[s]);e,d,_=engine(tmp_path,p);authorize(e,d);cp=e.prepare(d,'slot-1')
    if change=='source': Path(s.path).write_text('changed',encoding='utf8')
    elif change=='revoke': e.store.decide(d,'REVOKE',reviewer='SYNTHETIC',human_attested=True,authority_ref='SYNTHETIC')
    else:
        q=p.model_dump();q['request']['campaign_goal']='SYNTHETIC different';e.store.save(JourneyPlan.model_validate(q))
    with pytest.raises(ValueError,match=error):e.run(d,cp['creative_plan_id'])


def test_campaign_requires_explicit_authority_not_model_flag(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,provider=engine(tmp_path,p)
    with pytest.raises(ValueError,match='explicit_campaign'):e.execute_remaining(d)
    with pytest.raises(ValueError,match='explicit_human'):e.store.decide(d,'AUTHORIZE_AUTOPILOT',reviewer='model',human_attested=False,authority_ref='')
    assert provider.calls==[]


@pytest.mark.parametrize('n',[1,3])
def test_source_roles_no_duplicates_no_more_than_two_supports(tmp_path,n):
    p=propose_flow(request(content_count=1),[source(tmp_path)])
    raw=p.model_dump();raw['sequence'][0]['supporting_sources']=[dict(source_id='s1',contribution='irrelevant duplicate')]*n
    with pytest.raises(ValueError):JourneyPlan.model_validate(raw)


def test_creator_isolation_and_client_permission(tmp_path):
    with pytest.raises(ValueError,match='creator_scope'):propose_flow(request(),[source(tmp_path,creator='other')])
    s=source(tmp_path,'CLIENT_STORY');p=propose_flow(request(),[s])
    with pytest.raises(ValueError,match='client_story_permission'):verify_sources(p)


@pytest.mark.parametrize('rewrite,hard',[(True,False),(False,True)])
def test_same_bounded_rewrite_and_hard_findings(tmp_path,rewrite,hard):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,provider=engine(tmp_path,p,Provider(rewrite,hard));authorize(e,d)
    result=e.execute_remaining(d)[0]
    assert [c['stage']['stage_type'] for c in provider.calls]==['CREATIVE_PLAN','WRITER','CRITIC1','REWRITE','CRITIC2']
    assert result.status==('CRITIC_FAILED' if hard else 'DRAFT_READY')
    assert not result.published


def test_actual_js_shared_planner_prompt_and_title_voice_scope(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p)
    context=e.context(d,'slot-1');inputs=dict(plan_route='reelo.journey-creative-plan.1',plan_schema={})
    pack,_=assemble('CREATIVE_PLAN',inputs,e.assets(context))
    bound=dict(context=context,execution={'receipt':{}},assets=[],inputs=inputs,stage={'stage_type':'CREATIVE_PLAN'},context_pack=pack)
    code="""const fs=require('fs'),vm=require('vm');const b=JSON.parse(fs.readFileSync(0,'utf8'));
const s=fs.readFileSync('.claude/workflows/batch-content.js','utf8').replace('export const meta','const meta');
let calls=[];const e={args:[],V2_BOUND:b,log:()=>{},agent:async(p,o)=>{calls.push({p,o});return {synthetic:true}}};
(async()=>{await vm.runInNewContext('(async()=>{'+s+'})()',e);process.stdout.write(JSON.stringify(calls))})();"""
    calls=json.loads(subprocess.run(['node','-e',code],input=json.dumps(bound),text=True,encoding='utf8',capture_output=True,cwd=ROOT,check=True).stdout)
    assert len(calls)==1
    prompt=calls[0]['p']
    assert 'Voice owns CTA wording' in prompt and 'never observed customer motive' in prompt
    assert 'reelo.journey-creative-plan.1' in prompt and 'No publishing' in prompt
    assert 'SYNTHETIC source fact' in prompt and 'DO NOT LOAD' not in prompt


def test_early_sales_and_missing_resource_rejected(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)])
    raw=p.model_dump();raw['sequence'][0]['cta_intent']='BOOK_BUY_APPLY'
    with pytest.raises(ValueError,match='early_stage'):JourneyPlan.model_validate(raw)
    raw=p.model_dump();raw['request']['allowed_cta_intents']=['GET_RESOURCE'];raw['sequence'][0]['cta_intent']='GET_RESOURCE'
    with pytest.raises(ValueError,match='resource_cta'):JourneyPlan.model_validate(raw)


def test_invented_quote_role_and_source_identity_rejected(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p)
    context=e.context(d,'slot-1');raw=proposal(context)
    raw['proof_plan'][0]['source']['support_quote']='invented quote'
    with pytest.raises(ValueError,match='proof_support'):validate(raw,context,e.assets(context))
    raw=proposal(context);raw['proof_plan'][0]['source']['origin']='external_knowledge'
    with pytest.raises(ValueError,match='source_role'):validate(raw,context,e.assets(context))
    raw=proposal(context);raw['one_idea']='a different strategy'
    with pytest.raises(ValueError,match='slot_intent'):validate(raw,context,e.assets(context))


def test_client_permission_exact_scope_and_revocation(tmp_path):
    s=source(tmp_path,'CLIENT_STORY');permission=tmp_path/'permission.json'
    grant=dict(source_id=s.source_id,source_sha256=s.sha256,creator_id=s.creator_id,
               human_attested=True,reviewer='SYNTHETIC owner',scope='content_drafting',revoked=False)
    permission.write_text(json.dumps(grant),encoding='utf8')
    s=s.model_copy(update=dict(permission_ref=permission.as_posix(),permission_sha256=hashlib.sha256(permission.read_bytes()).hexdigest()))
    p=propose_flow(request(content_count=1),[s]);e,d,_=engine(tmp_path,p);authorize(e,d)
    cp=e.prepare(d,'slot-1')
    permission.write_text(json.dumps(dict(grant,revoked=True)),encoding='utf8')
    with pytest.raises(ValueError,match='permission_changed'):e.run(d,cp['creative_plan_id'])


def test_revocation_during_stages_stops_before_next_call(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);provider=Provider();e,d,_=engine(tmp_path,p,provider);authorize(e,d)
    cp=e.prepare(d,'slot-1');original=e.invoke
    def revoke(execution,context,stage,inputs,work,assets):
        body,host=original(execution,context,stage,inputs,work,assets)
        e.store.decide(d,'REVOKE',reviewer='SYNTHETIC',human_attested=True,authority_ref='SYNTHETIC')
        return body,host
    e.invoke=revoke;result=e.run(d,cp['creative_plan_id'])
    assert result.status=='UNKNOWN'
    assert [c['stage']['stage_type'] for c in provider.calls]==['CREATIVE_PLAN','WRITER']


def test_duplicate_execution_reservation_is_atomic_and_unknown_not_retried(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p);authorize(e,d)
    row=dict(slot_id='slot-1',generation_id='synthetic-started')
    e.store.append(d,'EXECUTION_STARTED',row)
    with pytest.raises(ValueError,match='already_reserved'):e.store.append(d,'EXECUTION_STARTED',row)
    e.store.append(d,'PLANNER_STARTED',row)
    with pytest.raises(ValueError,match='already_reserved'):e.prepare(d,'slot-1')
    with pytest.raises(ValueError,match='requires_reconciliation'):e.store.append(d,'PLANNER_STARTED',row)


def test_missing_current_ci_authority_fails_before_model(tmp_path):
    fixture=ROOT/'integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json'
    packet=json.loads(fixture.read_text(encoding='utf8'));s=source(tmp_path)
    s=Source.model_validate(dict(s.model_dump(),kind='VERIFIED_INSIGHT',truth_type='DERIVED',path=fixture.as_posix(),
        sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),packet_id=packet['packet_id']))
    p=propose_flow(request(route='INSIGHT_LED',content_count=1),[s]);e,d,provider=engine(tmp_path,p)
    with pytest.raises(ValueError,match='current_insight'):e.prepare(d,'slot-1')
    assert provider.calls==[]


def test_foreign_voice_and_future_as_observed_rejected(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p)
    foreign=tmp_path/'brand'/'another-creator'/'voice-profile.md';foreign.parent.mkdir(parents=True);foreign.write_text('OTHER')
    e.read_files=(foreign,)
    with pytest.raises(ValueError,match='creator_asset_scope'):e.prepare(d,'slot-1')
    with pytest.raises(ValueError,match='not_observed'):source(tmp_path,'FUTURE_POSSIBILITY','future')


def test_history_is_context_not_global_calibration_or_truth(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)],history=[dict(source_ids=['s1'],stage='SOLUTION_AWARE',status='historical draft')])
    e,d,_=engine(tmp_path,p);context=e.context(d,'slot-1')
    assert context['memory']['imported_editorial_history']==p.editorial_history
    assert context['campaign']['starting_awareness_stage']=='UNAWARE' and not context['audience_state_is_observed']
    assert context['memory']['calibration']==[]


def test_ten_piece_execution_toward_offer_is_sequential_and_never_publishes(tmp_path):
    sources=[source(tmp_path),source(tmp_path,'CREATOR_KNOWLEDGE_POV','knowledge'),source(tmp_path,'OFFER_BUSINESS_CONTEXT','offer')]
    p=propose_flow(request(content_count=10,route='AUTO_DISCOVERY',target_awareness_stage='MOST_AWARE',
        offer_context=dict(source_id='offer',intended_next_step='SYNTHETIC apply'),
        allowed_cta_intents=['REFLECT','ENGAGE','LEARN_METHOD','EXPLORE_OFFER','BOOK_BUY_APPLY']),sources)
    e,d,provider=engine(tmp_path,p);authorize(e,d);results=e.execute_remaining(d)
    assert len(results)==10 and all(r.status=='DRAFT_READY' for r in results)
    assert len(provider.calls)==30
    assert len(provider.calls[-1]['context']['memory']['completed'])==9
    assert provider.calls[-1]['context']['slot']['cta_intent']=='BOOK_BUY_APPLY'
    assert all(r.human_approval=='PENDING' and r.notion_status=='NOT_SENT' and not r.published for r in results)
    before=len(provider.calls);assert e.execute_remaining(d)==[];assert len(provider.calls)==before


def test_sql_events_are_append_only(tmp_path):
    import sqlite3
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p);authorize(e,d)
    with e.store.connect() as db:
        with pytest.raises(sqlite3.IntegrityError,match='append_only'):db.execute('DELETE FROM events')
        with pytest.raises(sqlite3.IntegrityError,match='immutable'):db.execute("UPDATE plans SET body='{}'")
        row=db.execute('SELECT * FROM events LIMIT 1').fetchone()
        with pytest.raises(sqlite3.IntegrityError,match='append_only'):db.execute('INSERT OR REPLACE INTO events VALUES (?,?,?)',row)


def test_unselected_client_source_does_not_force_permission_or_read(tmp_path):
    s=source(tmp_path);unused=source(tmp_path,'CLIENT_STORY','unused')
    p=propose_flow(request(content_count=1),[s,unused]);Path(unused.path).unlink()
    e,d,_=engine(tmp_path,p)
    assert e.context(d,'slot-1')['source_ids']==['s1']


def test_opt_in_cli_explores_and_inspects_without_execution(tmp_path):
    import sys
    r=tmp_path/'request.json';s=tmp_path/'sources.json';db=tmp_path/'cli.sqlite'
    r.write_text(json.dumps(request(content_count=2).model_dump()),encoding='utf8')
    s.write_text(json.dumps([source(tmp_path).model_dump()]),encoding='utf8')
    command=[sys.executable,'-m','integrations.journey','--store',str(db)]
    output=json.loads(subprocess.run(command+['explore','--request',str(r),'--sources',str(s)],cwd=ROOT,capture_output=True,text=True,encoding='utf8',check=True).stdout)
    assert output['execution_authorized'] is False
    inspected=json.loads(subprocess.run(command+['inspect','--plan-hash',output['plan_hash']],cwd=ROOT,capture_output=True,text=True,encoding='utf8',check=True).stdout)
    assert len(inspected['plan']['sequence'])==2 and inspected['memory']['completed']==[]


def test_rejected_terminal_revision_preserves_unknown_and_needs_real_gate(tmp_path):
    p=propose_flow(request(content_count=1,autonomy_mode='GUIDED'),[source(tmp_path)])
    e,d,provider=engine(tmp_path,p)
    original=e.invoke
    def changed(execution,context,stage,inputs,work,assets):
        body,host=original(execution,context,stage,inputs,work,assets)
        body['output']['one_idea']='SYNTHETIC paraphrase rejected by exact guard'
        return body,host
    e.invoke=changed
    with pytest.raises(ValueError,match='slot_intent_changed'):e.prepare(d,'slot-1')
    history=e.store.events(p.request.campaign_id);parent=history[-1]['data']['generation_id']
    raw=proposal(e.context(d,'slot-1'))
    derived=e.propose_terminal_revision(d,parent,raw,operator='SYNTHETIC operator',rationale='Restore locked strategy; pending human review')
    after=e.store.events(p.request.campaign_id)
    assert after[:len(history)]==history and derived['revision_audit']['original_unknown_preserved']
    assert not derived['revision_audit']['human_approval_inherited']
    with pytest.raises(ValueError,match='real_sample_creative_approval'):e.run(d,derived['creative_plan_id'])
    raw['proof_plan'][0]['source']['support_quote']='invented'
    with pytest.raises(ValueError,match='proof_support'):e.propose_terminal_revision(d,parent,raw,operator='SYNTHETIC',rationale='Must reject')


def test_commercial_offer_cannot_be_hidden_fourth_source(tmp_path):
    sources=[source(tmp_path),source(tmp_path,'CREATOR_KNOWLEDGE_POV','knowledge'),source(tmp_path,'OFFER_BUSINESS_CONTEXT','offer')]
    p=propose_flow(request(content_count=1,starting_awareness_stage='MOST_AWARE',target_awareness_stage='MOST_AWARE',
        offer_context=dict(source_id='offer',intended_next_step='SYNTHETIC apply'),allowed_cta_intents=['BOOK_BUY_APPLY']),sources)
    assert p.sequence[0].supporting_sources[0].source_id=='offer'
    raw=p.model_dump();raw['sequence'][0]['supporting_sources']=[]
    with pytest.raises(ValueError,match='offer_must_count'):JourneyPlan.model_validate(raw)


def test_journey_candidates_use_closed_source_ids_not_annotated_paths(tmp_path):
    p=propose_flow(request(content_count=1),[source(tmp_path)]);e,d,_=engine(tmp_path,p)
    context=e.context(d,'slot-1');raw=proposal(context)
    raw['opening_plan']['recommended']['evidence_refs']=['s1']
    assert validate(raw,context,e.assets(context))['packet_id'] is None
    raw['opening_plan']['recommended']['evidence_refs']=[p.sources[0].path+'#invented']
    with pytest.raises(ValueError,match='candidate_provenance'):validate(raw,context,e.assets(context))
