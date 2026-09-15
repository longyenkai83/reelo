import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path

import pytest

from integrations.content_intelligence.adapter import IntakeStore, dispatch
from integrations.content_intelligence.contract import ContentIntelligencePacket, packet_identity
from integrations.content_intelligence.host import correlated_result

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT/'integrations/content_intelligence/contracts'


@pytest.fixture
def packet():
    return json.loads((CONTRACTS/'fixtures/synthetic-content-intelligence-packet.json').read_text(encoding='utf-8'))


def test_canonical_contract_parity(packet):
    assert ContentIntelligencePacket.model_json_schema() == json.loads(
        (CONTRACTS/'content-intelligence-packet.schema.json').read_text(encoding='utf-8'))
    p = ContentIntelligencePacket.model_validate(packet)
    assert p.packet_id == packet['packet_id']
    assert p.model_dump(mode='json') == packet


@pytest.mark.parametrize('change', ['schema', 'time', 'source', 'quote', 'permission', 'type', 'missing', 'lineage', 'counter_quote'])
def test_invalid_never_authorizes_or_launches(packet, tmp_path, change):
    p = deepcopy(packet)
    if change == 'schema': p['schema_version'] = 'v3'
    if change == 'time': p['created_at'] = '2000-01-01T00:00:00Z'
    if change == 'source': p['customer_truth']['source_snapshots'][0]['text'] = 'Invented'
    if change == 'counter_quote': p['customer_truth']['verified_insight']['contradictions'][0]['counter_ref']['evidence_quote'] = 'Invented counter quote'
    if change == 'quote': p['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_quote'] = 'Invented'
    if change == 'permission': p['creative_execution']['constraints']['no_fake_statistics'] = False
    if change == 'type': p['content_strategy']['truth_type'] = 'OBSERVED'
    if change == 'missing': del p['selection']
    if change == 'lineage': p['lineage']['comment_ids'] = ['other']
    # Rehash most attacks to test semantics, not only the address checksum.
    if change != 'time': p['packet_id'] = packet_identity(p)
    calls = []
    with pytest.raises(ValueError):
        dispatch(IntakeStore(tmp_path/'state.db'), p, request_id='test',
                 authorize_current=lambda p: calls.append('auth'), launch=lambda *a: calls.append('launch'))
    assert calls == []


def test_current_recheck_blocks_before_launch(packet, tmp_path):
    calls = []
    def auth(p):
        calls.append('auth')
        if len(calls) == 2: raise ValueError('selection_revoked')
    with pytest.raises(ValueError, match='selection_revoked'):
        dispatch(IntakeStore(tmp_path/'state.db'), packet, request_id='r',
                 authorize_current=auth, launch=lambda *a: calls.append('launch'))
    assert calls == ['auth', 'auth']


def test_durable_idempotency_concurrent_reservation(packet, tmp_path):
    path = tmp_path/'state.db'
    store = IntakeStore(path)
    receipt = store.intake(packet)
    def reserve(_):
        s = IntakeStore(path)
        assert s.intake(packet) == receipt
        return s.reserve(receipt, 'same-request')
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(reserve, range(8)))
    assert sum(fresh for _, fresh in results) == 1
    assert len({r.generation_id for r, _ in results}) == 1
    assert IntakeStore(path).context(receipt)['packet'] == packet


def test_generation_lineage_and_unknown_no_retry(packet, tmp_path):
    store = IntakeStore(tmp_path/'state.db')
    calls = []
    def lost(*args):
        calls.append('launch')
        raise ValueError('lost')
    first = dispatch(store, packet, request_id='a', authorize_current=lambda p: None, launch=lost)
    assert first.status == 'UNKNOWN' and 'lost' in first.validation_issues
    result = dispatch(store, packet, request_id='a', authorize_current=lambda p: None, launch=lost)
    assert result.status == 'UNKNOWN' and calls == ['launch']
    with pytest.raises(ValueError, match='reconcile_previous'):
        store.reserve(result.receipt, 'b', result.generation_id)


def test_revision_chain_preserves_previous_and_blocks_old(packet, tmp_path):
    store = IntakeStore(tmp_path/'state.db')
    old = store.intake(packet)
    newer = deepcopy(packet)
    newer.update(packet_revision=2, supersedes_packet_id=packet['packet_id'], created_at='2026-09-16T00:00:00Z')
    newer['packet_id'] = packet_identity(newer)
    receipt = store.intake(newer)
    assert receipt.packet_id != old.packet_id
    assert store.context(old)['packet'] == packet
    with pytest.raises(ValueError, match='superseded'):
        store.reserve(old, 'old')
    fork = deepcopy(newer)
    fork['created_at'] = '2026-09-17T00:00:00Z'
    fork['packet_id'] = packet_identity(fork)
    with pytest.raises(ValueError, match='fork'):
        store.intake(fork)


def test_terminal_requires_bound_tool_and_task_artifact(tmp_path):
    script = tmp_path/'script.js'
    artifact = tmp_path/'returned.json'
    artifact.write_text('{"result":{"typed":"value"}}', encoding='utf-8')
    events = [
        {'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Workflow', 'id': 't',
         'input': {'scriptPath': script.as_posix()}}]}},
        {'type': 'system', 'subtype': 'task_started', 'task_id': 'w', 'tool_use_id': 't'},
        {'type': 'system', 'subtype': 'task_notification', 'task_id': 'w', 'tool_use_id': 't',
         'status': 'completed', 'output_file': str(artifact)},
    ]
    assert correlated_result(events, script, tmp_path)[0] == {'typed': 'value'}
    with pytest.raises(ValueError): correlated_result(events[:2], script, tmp_path)
    events[-1]['tool_use_id'] = 'unrelated'
    with pytest.raises(ValueError): correlated_result(events, script, tmp_path)


def test_v2_workflow_and_legacy_regression():
    subprocess.run(['node', str(ROOT/'tests/workflow-v2-test.cjs')], cwd=ROOT, check=True)


def test_notion_outbox_keeps_draft_and_human_approval_separate(packet, tmp_path):
    from integrations.content_intelligence import notion_handoff as n
    from integrations.content_intelligence.contract import value_hash
    store = IntakeStore(tmp_path/'state.db')
    receipt = store.intake(packet)
    result, _ = store.reserve(receipt, 'r')
    result.status = 'DRAFT_READY'
    result.critic_status = 'PASS'
    result.artifacts = [{'content': 'synthetic draft', 'content_hash': value_hash('synthetic draft'),
                         'writer': {'title': 'SYNTHETIC ONLY'}}]
    store.finish(result)
    kwargs = dict(destination='synthetic-test-destination', title_property='Title', status_property='Status',
                  draft_status='Draft', source_property='Source', authorize_current=lambda p: None)
    handoff, payload = n.prepare(store, result.generation_id, **kwargs)
    assert payload['pages'][0]['properties']['Status'] == 'Draft'
    assert n.prepare(store, result.generation_id, **kwargs)[0] == handoff
    assert n.claim(store, handoff, authorize_current=lambda p: None) == payload
    with pytest.raises(ValueError, match='already_claimed'):
        n.claim(store, handoff, authorize_current=lambda p: None)
    with pytest.raises(ValueError, match='verification_failed'):
        n.acknowledge(store, handoff, 'https://www.notion.so/test', verified_source_id=handoff,
                      verified_draft_status='Published', verified_destination='synthetic-test-destination')
    received = n.acknowledge(store, handoff, 'https://www.notion.so/test', verified_source_id=handoff,
                             verified_draft_status='Draft', verified_destination='synthetic-test-destination')
    assert received['human_approval'] == 'PENDING' and received['published'] is False
    assert received['status'] == 'DRAFT'
    assert store.status(result.generation_id).notion_status == 'DRAFT'
    assert store.status(result.generation_id).human_approval == 'PENDING'


@pytest.mark.parametrize('field,value', [('claude_code_version', '2.1.140'), ('tools', ['Read', 'Bash']),
                                      ('permissionMode', 'bypassPermissions'), ('mcp_servers', ['unexpected'])])
def test_runtime_profile_mismatch_is_not_accepted(tmp_path, field, value):
    from integrations.content_intelligence.host import HostConfig, verify_runtime_profile
    config = HostConfig(executable=tmp_path/'claude.exe', execution_workspace=tmp_path, state_directory=tmp_path)
    event = dict(type='system', subtype='init', claude_code_version='2.1.270', cwd=str(tmp_path),
                 tools=['Read', 'Workflow'], permissionMode='dontAsk', mcp_servers=[], plugins=[])
    verify_runtime_profile([event], config)
    event[field] = value
    with pytest.raises(ValueError, match='profile_mismatch'):
        verify_runtime_profile([event], config)


@pytest.mark.parametrize('effort', [None, 'medium', 'high'])
def test_effort_override_is_session_local_and_keeps_safety(packet, tmp_path, monkeypatch, effort):
    from integrations.content_intelligence.host import HostConfig, NativeHost
    home = tmp_path/'home'
    settings_file = home/'.claude/settings.json'
    settings_file.parent.mkdir(parents=True)
    settings_file.write_text('{"effortLevel":"xhigh","enabledPlugins":{"example":true}}')
    before = settings_file.read_bytes()
    monkeypatch.setattr(Path, 'home', classmethod(lambda cls: home))
    workspace = tmp_path/'workspace'
    script = workspace/'.claude/workflows/batch-content.js'
    script.parent.mkdir(parents=True)
    script.write_text('export const meta = {};\n/* V2_BOUND_CONTEXT */')
    monkeypatch.setattr(HostConfig, 'verify', lambda self: None)
    seen = []
    def stop_at_launch(argv, **kw):
        seen.extend(argv)
        raise RuntimeError('test launch boundary')
    monkeypatch.setattr(subprocess, 'Popen', stop_at_launch)
    store = IntakeStore(tmp_path/'store.db')
    receipt = store.intake(packet)
    execution, _ = store.reserve(receipt, 'test')
    config = HostConfig(executable=tmp_path/'claude.exe', execution_workspace=workspace,
                        state_directory=tmp_path/'runs', effort_level=effort)
    result = NativeHost(config)(execution, store.context(receipt))
    assert result.status == 'UNKNOWN'
    settings = json.loads(seen[seen.index('--settings')+1])
    assert settings.get('effortLevel') == effort
    assert settings['disableAllHooks'] is True
    assert settings['enabledPlugins'] == {'example': False}
    assert seen[seen.index('--tools')+1] == 'Workflow,Read'
    assert seen[seen.index('--permission-mode')+1] == 'dontAsk'
    assert seen[seen.index('--mcp-config')+1] == '{"mcpServers":{}}'
    assert settings_file.read_bytes() == before
    assert store.context(receipt)['packet'] == packet

@pytest.mark.parametrize('status,code', [('stopped', 'workflow_stopped_completion_unknown'), ('failed', 'workflow_failed')])
def test_native_stop_never_accepts_even_existing_partial_output(packet, tmp_path, status, code):
    script = tmp_path/'script.js'
    output = tmp_path/'partial.json'
    output.write_text('{"result":{"status":"DRAFT_READY"}}')
    events = [
        {'type':'assistant', 'message':{'content':[{'type':'tool_use','name':'Workflow','id':'t',
          'input':{'scriptPath':script.as_posix()}}]}},
        {'type':'system','subtype':'task_started','task_id':'w','tool_use_id':'t'},
        {'type':'system','subtype':'task_notification','task_id':'w','tool_use_id':'t',
         'status':status,'output_file':str(output)},
        {'type':'result','subtype':'success','is_error':False},
    ]
    store = IntakeStore(tmp_path/'state.db')
    calls = []
    def launch(*args):
        calls.append(1)
        return correlated_result(events, script, tmp_path)
    result = dispatch(store, packet, request_id='one', authorize_current=lambda p: None, launch=launch)
    assert result.status == 'UNKNOWN'
    assert code in result.validation_issues
    again = dispatch(store, packet, request_id='one', authorize_current=lambda p: None, launch=launch)
    assert again == result and calls == [1]

@pytest.mark.parametrize('case', [
    'exact', 'before', 'other_path', 'Write', 'PowerShell', 'Bash', 'mixed',
    'malformed', 'schema', 'context_hash', 'ingestion_id', 'packet_id', 'packet_revision',
    'packet_hash', 'receipt_context_hash', 'generation_id', 'missing_terminal',
    'missing_call', 'duplicate_call', 'unrelated_terminal', 'not_terminal',
])
def test_c53_permission_boundary_after_independent_validation(packet, tmp_path, monkeypatch, case):
    from integrations.content_intelligence.host import HostConfig, NativeHost
    workspace = tmp_path/'workspace'
    template = workspace/'.claude/workflows/batch-content.js'
    template.parent.mkdir(parents=True)
    template.write_text('export const meta = {};\n/* V2_BOUND_CONTEXT */')
    monkeypatch.setattr(HostConfig, 'verify', lambda self: None)
    monkeypatch.setattr(Path, 'home', classmethod(lambda cls: tmp_path/'home'))
    monkeypatch.setenv('TEMP', str(tmp_path))
    store = IntakeStore(tmp_path/'db.sqlite')
    receipt = store.intake(packet)
    execution, _ = store.reserve(receipt, 'c53')
    context = store.context(receipt)
    out = tmp_path/'claude'/'returned.json'
    out.parent.mkdir()
    from integrations.content_intelligence.stages import stage_identity
    stage = stage_identity(execution, 'WRITER', {})
    body = {'schema_version': 'reelo.host-stage.1', 'stage': dict(stage), 'output': {
        'status': 'DRAFT', 'content': 'SYNTHETIC ONLY', 'title': 'Synthetic', 'format': 'Reel',
        'issues': [], 'customer_evidence_ids': [packet['customer_truth']['verified_insight']['evidence_refs'][0]['evidence_id']],
        'external_dispositions': [dict(strategy_field=r['strategy_field'], disposition='omitted', explanation='Unsupported')
                                  for r in packet['external_evidence_requirements']]}}
    if case in ('context_hash', 'receipt_context_hash'): body['stage']['context_hash'] = 'bad'
    if case in ('ingestion_id', 'packet_id', 'packet_hash', 'generation_id'): body['stage'][case] = 'bad'
    if case == 'packet_revision': body['stage']['packet_revision'] += 1
    if case == 'schema': body['output']['published'] = True
    if case == 'not_terminal': body['output']['status'] = 'RUNNING'
    out.write_text('bad json' if case == 'malformed' else json.dumps({'result':body}), encoding='utf8')
    cfg = HostConfig(executable=tmp_path/'claude.exe',execution_workspace=workspace,state_directory=tmp_path/'runs')
    work = cfg.state_directory/execution.generation_id/'WRITER'
    work.mkdir(parents=True)
    script = work/'batch-content.js'
    events = [dict(type='system',subtype='init',claude_code_version='2.1.270',cwd=str(workspace),
                   tools=['Read','Workflow'],permissionMode='dontAsk',mcp_servers=[],plugins=[]),
        {'type':'assistant','message':{'content':[{'type':'tool_use','name':'Workflow','id':'workflow',
            'input':{'scriptPath':script.as_posix()}}]}},
        dict(type='system',subtype='task_started',task_id='task',tool_use_id='workflow')]
    notification = dict(type='system',subtype='task_notification',task_id='task',tool_use_id='workflow',
                        status='completed',output_file=str(out))
    name = case if case in ('Write','PowerShell','Bash') else 'Read'
    data = {'file_path': str(out if case != 'other_path' else tmp_path/'unrelated')}
    call = {'type':'assistant','message':{'content':[{'type':'tool_use','name':name,'id':'denied','input':data}]}}
    denial = dict(tool_name=name,tool_use_id='denied',tool_input=data)
    if case == 'before': events.append(call)
    if case == 'unrelated_terminal': notification['tool_use_id']='unrelated'
    if case != 'missing_terminal': events.append(notification)
    if case not in ('before','missing_call'): events.append(call)
    if case == 'duplicate_call': events.append(call)
    denials=[denial]
    if case == 'mixed':
        other={'file_path':str(tmp_path/'other')}
        events.append({'type':'assistant','message':{'content':[{'type':'tool_use','name':'Read','id':'other','input':other}]}})
        denials.append(dict(tool_name='Read',tool_use_id='other',tool_input=other))
    events.append(dict(type='result',subtype='success',permission_denials=denials))
    class Process:
        returncode=0
        def communicate(self, timeout): return '\n'.join(json.dumps(e) for e in events), ''
    captured=[]
    def launch(argv, **kwargs):
        captured.extend(argv)
        return Process()
    monkeypatch.setattr(subprocess,'Popen',launch)
    if case == 'exact':
        result, host = NativeHost(cfg).invoke_stage(execution, context, stage, {}, work, [])
        assert result == body and result['stage']['ingestion_id'] == receipt.ingestion_id
        assert len(host['permission_notes']) == 1
        assert host['permission_notes'][0]['code'] == 'redundant_post_terminal_output_read_denied'
        assert json.loads((work/'permission-review.json').read_text()) == host['permission_notes']
        allowed = captured[captured.index('--allowedTools')+1:captured.index('--permission-mode')]
        assert allowed == ['Workflow', 'Read('+script.as_posix()+')']
    else:
        with pytest.raises(ValueError): NativeHost(cfg).invoke_stage(execution, context, stage, {}, work, [])
        assert not (work/'validated-host-result.json').exists()
        assert not (work/'permission-review.json').exists()
    assert store.context(receipt) == context
