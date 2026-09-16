"""Synthetic native history; no live tools or private assets."""
import json
import sqlite3
from pathlib import Path
from copy import deepcopy
import pytest

from integrations.content_intelligence.adapter import IntakeStore
from integrations.content_intelligence.creative_plan import PlanStore
from integrations.content_intelligence.contract import value_hash
from integrations.content_intelligence.stages import stage_identity
from integrations.content_intelligence import reconciliation as rec
from tests.creative_fixture import proposal


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf8')


@pytest.fixture(params=['whitespace', 'redundant_titles'])
def case(tmp_path, monkeypatch, request):
    title_repair = request.param == 'redundant_titles'
    monkeypatch.setenv('TEMP', str(tmp_path))
    packet=json.loads((Path(__file__).parents[1]/'integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json').read_text(encoding='utf8'))
    intake=IntakeStore(tmp_path/'intake.sqlite')
    receipt=intake.intake(packet); context=intake.context(receipt)
    original,_=intake.reserve(receipt,'planner')
    failure = 'invalid_candidate_selection' if title_repair else 'psychology_mechanism_not_in_library'
    original.status='UNKNOWN'; original.validation_issues=[failure]
    intake.finish(original)
    stage_dir=tmp_path/original.generation_id/'CREATIVE_PLAN';stage_dir.mkdir(parents=True)
    library=tmp_path/'nguyen-ly-tam-ly.md';library.write_text('Synthetic  mechanism',encoding='utf8')
    assets=[dict(path=library.as_posix(),sha256=rec.digest(library))]
    raw=proposal(packet,library);inputs={'synthetic_test': True}
    if title_repair:
        from tests.purified_fixture import purified
        from integrations.content_intelligence.context_packs import manifest, ROOT
        raw=purified(packet,library)
        raw['compatibility_titles'].insert(0,dict(candidate=deepcopy(raw['title_plan']['recommended']),frame='SELF_MADE'))
        assets=manifest([library],ROOT)
    stage=stage_identity(original,'CREATIVE_PLAN',inputs)
    body=dict(schema_version='reelo.host-stage.1',stage=stage,output=raw)
    put(stage_dir/'request.json',dict(context=context,assets=assets,inputs=inputs,stage=stage))
    put(stage_dir/'unknown.json',dict(stage,issue=failure,status='CREATIVE_PLAN_UNKNOWN'))
    put(stage_dir.parent/'result.json',original.model_dump(mode='json'))
    script=stage_dir/'batch-content.js';script.write_text('synthetic script',encoding='utf8')
    native=tmp_path/'claude/task.output';put(native,{'result':body})
    events=[dict(type='system',subtype='init',claude_code_version='2.1.270',cwd=str(tmp_path),permissionMode='dontAsk',tools=['Read','Workflow'],mcp_servers=[],plugins=[]),
        dict(type='assistant',message={'content':[dict(type='tool_use',id='tool-test',name='Workflow',input={'scriptPath':script.as_posix(),'args':{}})]}),
        dict(type='system',subtype='task_started',task_id='task-test',tool_use_id='tool-test'),
        dict(type='system',subtype='task_notification',task_id='task-test',tool_use_id='tool-test',status='completed',output_file=str(native)),
        dict(type='result',subtype='success',is_error=False,terminal_reason='completed')]
    (stage_dir/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in events),encoding='utf8')
    put(stage_dir/'validated-host-result.json',body);put(stage_dir/'permission-review.json',[])
    source=tmp_path/'source.json';put(source,raw)
    cfg=tmp_path/'config.json';put(cfg,dict(executable=str(tmp_path/'native.exe'),execution_workspace=str(tmp_path),state_directory=str(tmp_path),read_files=[library.as_posix()]))
    plans=PlanStore(tmp_path/'plans.sqlite')
    plan=plans.save(rec.remove_redundant_titles(raw) if title_repair else raw,context,assets,
                    ('DERIVED-RP4-FROM-' if title_repair else 'DERIVED-C5.9-FROM-')+original.generation_id)
    approval=plans.review(plan['creative_plan_id'],dict(decision='approved',reviewer='Synthetic test human input',human_attested=True,expected_plan_hash=plan['plan_hash']))
    projection=tmp_path/'projection.json';put(projection,plan)
    provenance=tmp_path/'provenance.json';put(provenance,dict(source_proposal=str(source),source_proposal_sha256=rec.digest(source),source_generation=original.generation_id,context_hash=value_hash(context)))
    evidence=dict(stage_directory=str(stage_dir),config_path=str(cfg),projection_path=str(projection),provenance_path=str(provenance),plan_store=str(plans.path))
    if title_repair:evidence['resolution_kind']=rec.TITLE_REASON
    return dict(intake=intake,original=original,context=context,assets=assets,plans=plans,
                approval=approval,evidence=evidence,source=source,native=native,library=library,events=events)


def audit(c):
    return rec.append(c['intake'],c['original'].generation_id,evidence=c['evidence'],
        approval_id=c['approval']['approval_id'],authorize_current=lambda raw: None,
        actor='Synthetic test resolver',validator_commit='synthetic-test-commit')


def reserve(c, record):
    return c['intake'].reserve(c['original'].receipt,'writer',c['original'].generation_id,
        reconciliation_id=record['reconciliation_id'],approval_id=c['approval']['approval_id'],authorize_current=lambda raw: None)


def test_exact_false_negative_continues_and_preserves_unknown(case):
    with pytest.raises(ValueError,match='reconcile_previous'):
        case['intake'].reserve(case['original'].receipt,'writer',case['original'].generation_id)
    record=audit(case);child,fresh=reserve(case,record)
    assert fresh and child.parent_generation_id==case['original'].generation_id
    assert record['resolution']=='RECONCILED_SAFE_TO_CONTINUE'
    assert case['intake'].status(case['original'].generation_id)==case['original']


@pytest.mark.parametrize('defect', ['artifact','packet_id','packet_hash','revision','context','manifest',
                                   'source','missing_source','reason','another_generation','stale_approval',
                                   'permission','transport','native_identity','projection'])
def test_changed_evidence_or_current_state_blocks(case,defect):
    c=case;record=audit(c);directory=Path(c['evidence']['stage_directory'])
    if defect=='artifact':
        raw=rec.read(c['source']);raw['format']='changed';put(c['source'],raw)
    elif defect in ('packet_id','packet_hash','revision','context'):
        q=rec.read(directory/'request.json');key={'revision':'packet_revision','context':'context_hash'}.get(defect,defect)
        q['stage'][key]=99 if defect=='revision' else 'wrong';put(directory/'request.json',q)
    elif defect=='manifest':
        q=rec.read(c['evidence']['config_path']);q['read_files']=[];put(Path(c['evidence']['config_path']),q)
    elif defect=='source':c['library'].write_text('Changed',encoding='utf8')
    elif defect=='missing_source':c['library'].rename(c['library'].with_suffix('.unavailable'))
    elif defect=='reason':
        q=rec.read(directory/'unknown.json');q['issue']='host_timeout_completion_unknown';put(directory/'unknown.json',q)
    elif defect=='another_generation':
        with pytest.raises(ValueError,match='generation_or_approval'):
            rec.verify(c['intake'],record['reconciliation_id'],c['original'].model_copy(update={'generation_id':'another'}),c['context'],c['approval']['approval_id'],lambda p:None)
        return
    elif defect=='stale_approval':
        p=c['approval']['plan'];c['plans'].review(p['creative_plan_id'],dict(decision='deferred',reviewer='Test human',human_attested=True,expected_plan_hash=p['plan_hash']))
    elif defect in ('permission','transport'):
        ev=deepcopy(c['events'])
        if defect=='permission':ev[-1]['permission_denials']=[dict(tool_name='Bash',tool_use_id='bad',tool_input={})]
        else:ev[-1]['is_error']=True
        (directory/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in ev),encoding='utf8')
    elif defect=='native_identity':
        q=rec.read(c['native']);q['result']['stage']['generation_id']='wrong';put(c['native'],q)
    elif defect=='projection':
        q=rec.read(c['evidence']['projection_path']);q['plan_hash']='wrong';put(Path(c['evidence']['projection_path']),q)
    with pytest.raises(ValueError):reserve(c,record)
    assert c['intake'].status(c['original'].generation_id).status=='UNKNOWN'


def test_audit_is_append_only(case):
    record=audit(case)
    with case['intake'].connect() as db:
        for sql in ('UPDATE execution_reconciliation SET body=body','DELETE FROM execution_reconciliation'):
            with pytest.raises(sqlite3.IntegrityError,match='append_only'):db.execute(sql)
        with pytest.raises(sqlite3.IntegrityError,match='append_only'):
            db.execute('INSERT OR REPLACE INTO execution_reconciliation VALUES(?,?,?)',
                       (record['reconciliation_id'],record['generation_id'],'{}'))
    assert rec.verify(case['intake'],record['reconciliation_id'],case['original'],case['context'],case['approval']['approval_id'],lambda raw:None)==record


def test_governance_rechecked_before_continuation(case):
    record=audit(case)
    def revoked(raw):raise ValueError('selection_revoked')
    with pytest.raises(ValueError,match='selection_revoked'):
        case['intake'].reserve(case['original'].receipt,'writer',case['original'].generation_id,
            reconciliation_id=record['reconciliation_id'],approval_id=case['approval']['approval_id'],authorize_current=revoked)


def test_no_reconciliation_for_non_whitespace_failure(case):
    # A source where the old exact comparator already succeeds cannot justify this resolution.
    case['library'].write_text('Synthetic mechanism',encoding='utf8')
    with pytest.raises(ValueError):audit(case)


@pytest.mark.parametrize('defect',['text','evidence','safety','primary_id','frame'])
def test_conflicting_appendix_cannot_be_removed(case,defect):
    if case['evidence'].get('resolution_kind') != rec.TITLE_REASON:pytest.skip('E1 only')
    raw=rec.read(case['source']);row=raw['compatibility_titles'][0];c=row['candidate']
    if defect=='text':c['text']='A different claim'
    elif defect=='evidence':c['evidence_refs']=['invented']
    elif defect=='safety':c['factual_claims_supported']=False
    elif defect=='primary_id':raw['title_plan']['alternative']=deepcopy(raw['title_plan']['recommended'])
    else:row['frame']='different frame'
    with pytest.raises(ValueError):rec.remove_redundant_titles(raw)


def test_approved_but_semantically_edited_projection_cannot_reconcile(case):
    if case['evidence'].get('resolution_kind') != rec.TITLE_REASON:pytest.skip('E1 only')
    p=deepcopy(case['approval']['plan']['proposal']);p['one_idea']='Different meaning'
    plan=case['plans'].save(p,case['context'],case['assets'],'DERIVED-RP4-FROM-'+case['original'].generation_id)
    case['approval']=case['plans'].review(plan['creative_plan_id'],dict(decision='approved',reviewer='Synthetic human',human_attested=True,expected_plan_hash=plan['plan_hash']))
    put(Path(case['evidence']['projection_path']),plan)
    with pytest.raises(ValueError,match='repair_changed_plan_content'):audit(case)
