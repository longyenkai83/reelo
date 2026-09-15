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


@pytest.mark.parametrize('change', ['schema', 'time', 'source', 'quote', 'permission', 'type', 'missing', 'lineage'])
def test_invalid_never_authorizes_or_launches(packet, tmp_path, change):
    p = deepcopy(packet)
    if change == 'schema': p['schema_version'] = 'v3'
    if change == 'time': p['created_at'] = '2000-01-01T00:00:00Z'
    if change == 'source': p['customer_truth']['source_snapshots'][0]['text'] = 'Invented'
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
