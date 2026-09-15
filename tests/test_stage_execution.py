import json
from copy import deepcopy
from pathlib import Path

import pytest

from integrations.content_intelligence.adapter import IntakeStore, dispatch
from integrations.content_intelligence.contract import value_hash
from integrations.content_intelligence.host import NativeHost, HostConfig
from integrations.content_intelligence.stages import CHECKS, validate_output


@pytest.fixture
def packet():
    return json.loads((Path(__file__).resolve().parents[1]/'integrations/content_intelligence/contracts/fixtures/synthetic-content-intelligence-packet.json').read_text(encoding='utf8'))


def draft(packet):
    return dict(status='DRAFT', content='SYNTHETIC draft', title='Synthetic', format='Reel', issues=[],
                customer_evidence_ids=[packet['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_id']],
                external_dispositions=[dict(strategy_field=r['strategy_field'], disposition='omitted', explanation='Not supported')
                                       for r in packet['external_evidence_requirements']])


def critic(revise=False):
    return dict(findings=[], verdict='REVISE' if revise else 'PASS', **dict.fromkeys(CHECKS, True),
                title_criteria=[True]*8, blocking_issues=['Fix scope'] if revise else [], notes=['Owner review pending'])


def run(packet, tmp_path, monkeypatch, queue, change=None):
    monkeypatch.setattr(HostConfig, 'verify', lambda self: None)
    store = IntakeStore(tmp_path/'store.db')
    config = HostConfig(executable=tmp_path/'claude.exe', execution_workspace=tmp_path,
                        state_directory=tmp_path/'stages')
    host = NativeHost(config)
    calls = []
    def invoke(execution, context, stage, inputs, work, assets):
        # A completed predecessor must already be durable before the next launch.
        if calls:
            previous = work.parent/calls[-1]['stage_type']/'completed.json'
            assert previous.is_file()
            assert json.loads(previous.read_text(encoding='utf8'))['stage_id'] == stage['parent_stage_id']
        assert context['packet'] == packet
        assert stage['input_hash'] == value_hash(inputs)
        assert stage['generation_id'] == execution.generation_id
        assert stage['context_hash'] == execution.receipt.context_hash
        calls.append(deepcopy(stage))
        output = queue.pop(0)
        if isinstance(output, Exception): raise output
        body = dict(schema_version='reelo.host-stage.1', stage=deepcopy(stage), output=output)
        if change: change(body, work)
        return body, dict(task_id='task-'+stage['stage_type'], tool_use_id='tool-'+stage['stage_type'])
    monkeypatch.setattr(host, 'invoke_stage', invoke)
    kwargs = dict(request_id='one', authorize_current=lambda p: None, launch=host)
    result = dispatch(store, packet, **kwargs)
    assert dispatch(store, packet, **kwargs) == result  # Never re-execute same reservation.
    assert store.context(result.receipt)['packet'] == packet
    return result, calls, config.state_directory/result.generation_id


@pytest.mark.parametrize('rewrite', [False, True])
def test_completed_paths_and_lineage(packet, tmp_path, monkeypatch, rewrite):
    queue = [draft(packet), critic()]
    if rewrite: queue = [draft(packet), critic(True), draft(packet), critic()]
    result, calls, work = run(packet, tmp_path, monkeypatch, queue)
    assert result.status == 'DRAFT_READY' and result.critic_status == 'PASS'
    assert result.human_approval == 'PENDING' and result.published is False and result.notion_status == 'NOT_SENT'
    assert [s['stage_type'] for s in calls] == (['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2'] if rewrite else ['WRITER', 'CRITIC1'])
    stages = result.host['stages']
    for i, stage in enumerate(stages):
        assert stage['status'] == stage['stage_type']+'_COMPLETED'
        assert stage['parent_stage_id'] == (stages[i-1]['stage_id'] if i else None)
        assert stage['parent_artifact_hash'] == (stages[i-1]['artifact_hash'] if i else None)
        assert stage['artifact_hash'] == value_hash(stage['raw'])
        assert stage['normalized_hash'] == value_hash(stage['normalized'])
        assert json.loads((work/stage['stage_type']/'completed.json').read_text()) == stage
    assert stages[-1]['raw']['notes'] and stages[-1]['normalized']['verdict'] == 'PASS'


@pytest.mark.parametrize('index', range(4))
@pytest.mark.parametrize('reason', ['workflow_stopped_completion_unknown', 'host_timeout_completion_unknown'])
def test_stop_retains_every_completed_stage_no_retry(packet, tmp_path, monkeypatch, index, reason):
    queue = [draft(packet), critic(True), draft(packet), critic()]
    queue[index] = ValueError(reason)
    result, calls, work = run(packet, tmp_path, monkeypatch, queue)
    assert result.status == 'UNKNOWN' and reason in result.validation_issues
    assert len(calls) == index+1
    assert len(result.host['stages']) == index+1
    assert result.host['stages'][-1]['status'] == calls[-1]['stage_type']+'_UNKNOWN'
    for call in calls[:-1]: assert (work/call['stage_type']/'completed.json').is_file()
    assert len(result.artifacts) == (0 if index == 0 else 1 if index <= 2 else 2)


@pytest.mark.parametrize('field', ['packet_id', 'packet_revision', 'packet_hash', 'context_hash', 'ingestion_id',
                                  'generation_id', 'parent_generation_id', 'stage_id', 'stage_type',
                                  'parent_stage_id', 'parent_artifact_hash', 'input_hash'])
def test_identity_mismatch_blocks_without_retry(packet, tmp_path, monkeypatch, field):
    def corrupt(body, work): body['stage'][field] = 'bad'
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet)], corrupt)
    assert result.status == 'UNKNOWN' and 'stage_identity_mismatch' in result.validation_issues
    assert len(calls) == 1


@pytest.mark.parametrize('malformed', [None, {}, {'verdict':'PASS'}, 'text'])
def test_malformed_critic_stops_not_rewrite(packet, tmp_path, monkeypatch, malformed):
    result, calls, work = run(packet, tmp_path, monkeypatch, [draft(packet), malformed])
    assert result.status == 'UNKNOWN' and len(calls) == 2
    assert (work/'WRITER/completed.json').is_file()


def test_single_rewrite_maximum(packet, tmp_path, monkeypatch):
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet), critic(True), draft(packet), critic(True)])
    assert len(calls) == 4 and result.status == 'CRITIC_FAILED'
    assert result.validation_issues == ['Fix scope']


def test_persisted_artifact_tamper_stops_before_next_call(packet, tmp_path, monkeypatch):
    from integrations.content_intelligence import stages
    real = stages.persist
    def corrupt(path, body):
        real(path, body)
        if path.name == 'progress.json':
            p = path.parent/'WRITER/completed.json'
            data = json.loads(p.read_text()); data['raw']['content'] = 'tampered'
            real(p, data)
    monkeypatch.setattr(stages, 'persist', corrupt)
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet)])
    assert result.status == 'UNKNOWN' and len(calls) == 1
    assert 'persisted_stage_integrity_failure' in result.validation_issues


@pytest.mark.parametrize('field', CHECKS)
def test_strict_critic_vetoes_are_retained(packet, field):
    raw = critic(); raw[field] = False
    normalized = validate_output('CRITIC1', raw, {'packet':packet})
    assert normalized['reported_verdict'] == 'PASS' and normalized['verdict'] == 'REVISE'
    assert field+'_not_confirmed' in normalized['blocking_issues']


def test_revise_without_explanation_and_reported_pass_with_blockers(packet):
    raw = critic(); raw['verdict'] = 'REVISE'
    assert validate_output('CRITIC1', raw, {'packet':packet})['blocking_issues'] == ['revise_without_explanation']
    raw = critic(); raw['blocking_issues'] = ['scope']
    assert validate_output('CRITIC1', raw, {'packet':packet})['verdict'] == 'REVISE'

@pytest.mark.parametrize('kind', ['invented_id', 'missing_disposition', 'duplicate_disposition', 'blocked_disposition', 'blank_content'])
def test_writer_provenance_rejection_is_terminal(packet, tmp_path, monkeypatch, kind):
    output = draft(packet)
    if kind == 'invented_id': output['customer_evidence_ids'] = ['invented']
    if kind == 'missing_disposition': output['external_dispositions'].pop()
    if kind == 'duplicate_disposition': output['external_dispositions'].append(output['external_dispositions'][0])
    if kind == 'blocked_disposition': output['external_dispositions'][0]['disposition'] = 'blocked'
    if kind == 'blank_content': output['content'] = ' '
    result, calls, _ = run(packet, tmp_path, monkeypatch, [output])
    assert result.status == 'UNKNOWN' and len(calls) == 1
    assert 'writer_output_or_provenance_invalid' in result.validation_issues


def test_counter_evidence_remains_valid(packet, tmp_path, monkeypatch):
    output = draft(packet)
    output['customer_evidence_ids'].append(packet['customer_truth']['verified_insight']['contradictions'][0]['counter_ref']['evidence_id'])
    result, calls, _ = run(packet, tmp_path, monkeypatch, [output, critic()])
    assert result.status == 'DRAFT_READY' and len(calls) == 2


@pytest.mark.parametrize('status,expected', [('BLOCKED_PENDING_RESEARCH', 'BLOCKED_PENDING_RESEARCH'), ('FAILED', 'HOST_FAILED')])
def test_writer_reports_no_draft_without_critic(packet, tmp_path, monkeypatch, status, expected):
    output = draft(packet); output.update(status=status, content='', issues=['missing_external_evidence'])
    result, calls, work = run(packet, tmp_path, monkeypatch, [output])
    assert result.status == expected and len(calls) == 1
    assert (work/'WRITER/completed.json').is_file()
