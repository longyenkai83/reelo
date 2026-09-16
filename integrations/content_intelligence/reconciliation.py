"""Audited continuation of one proven Planner whitespace false negative.

Local operator authority, not a model API. No terminal execution is rewritten.
Every reservation replays evidence and current governance/approval/source checks.
"""
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .contract import value_hash
from .creative_plan import PlanStore, validate_proposal
from .host import HostConfig, correlated_result, verify_runtime_profile, review_permission_denials
from .stages import stage_identity, validate_envelope

REASON = 'psychology_whitespace_false_negative'
RESOLUTION = 'RECONCILED_SAFE_TO_CONTINUE'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError('reconciliation_'+code)


def assess(original, context, evidence, approval_id, authorize_current):
    require(callable(authorize_current), 'current_governance_required')
    require(original.status == 'UNKNOWN' and original.validation_issues == ['psychology_mechanism_not_in_library'],
            'different_failure_reason')
    authorize_current(context['packet'])
    stage_dir = Path(evidence['stage_directory'])
    request = read(stage_dir/'request.json')
    require(request['context'] == context, 'context_mismatch')
    expected = stage_identity(original, 'CREATIVE_PLAN', request['inputs'])
    require(request['stage'] == expected, 'identity_mismatch')
    unknown = read(stage_dir/'unknown.json')
    require(all(unknown.get(k) == v for k, v in expected.items()) and
            unknown.get('issue') == 'psychology_mechanism_not_in_library' and
            unknown.get('status') == 'CREATIVE_PLAN_UNKNOWN', 'different_failure_reason')
    require(read(stage_dir.parent/'result.json') == original.model_dump(mode='json'), 'original_result_changed')
    cfg = read(evidence['config_path'])
    config = HostConfig(executable=Path(cfg['executable']), execution_workspace=Path(cfg['execution_workspace']),
                        state_directory=Path(cfg['state_directory'])/'executions')
    events = [json.loads(line) for line in (stage_dir/'events.jsonl').read_text(encoding='utf8').splitlines() if line.strip()]
    results = [e for e in events if e.get('type') == 'result']
    require(bool(results) and all(e.get('is_error') is False and e.get('subtype') == 'success'
                                 and e.get('terminal_reason') == 'completed' for e in results), 'transport_not_completed')
    verify_runtime_profile(events, config)
    body, correlation = correlated_result(events, stage_dir/'batch-content.js', Path(os.environ['TEMP'])/'claude')
    validate_envelope(body, expected, context)
    require(body == read(stage_dir/'validated-host-result.json'), 'native_artifact_mismatch')
    permission_notes = review_permission_denials(events, correlation)
    require(permission_notes == read(stage_dir/'permission-review.json'), 'permission_mismatch')
    projection = read(evidence['projection_path'])
    provenance = read(evidence['provenance_path'])
    source = Path(provenance['source_proposal'])
    require(digest(source) == provenance['source_proposal_sha256'] and read(source) == body['output'], 'artifact_hash_mismatch')
    require(provenance['source_generation'] == original.generation_id and
            provenance['context_hash'] == value_hash(context) and
            projection['generation_id'] == 'DERIVED-C5.9-FROM-'+original.generation_id, 'projection_lineage_mismatch')
    assets = request['assets']
    require([Path(p).as_posix() for p in cfg['read_files']] == [a['path'] for a in assets], 'manifest_mismatch')
    require(all(Path(a['path']).is_file() for a in assets), 'source_unavailable')
    require(all(digest(a['path']) == a['sha256'] for a in assets), 'source_changed')
    plans = PlanStore(evidence['plan_store'])
    approved = plans.approved(approval_id, context, assets)
    require(approved['plan'] == projection and approved['approval_kind'] == 'human', 'plan_approval_mismatch')
    # Structural validation of the SAME raw artifact, not the later edited plan.
    validate_proposal(body['output'], context, assets)
    psychology = body['output']['psychology']
    library = Path(psychology['library_source']).read_text(encoding='utf8').casefold()
    mechanisms = [psychology['primary_mechanism'], psychology['optional_secondary_mechanism']]
    require(any(m and m.casefold() not in library and ' '.join(m.casefold().split()) in ' '.join(library.split())
                for m in mechanisms), 'not_whitespace_false_negative')
    paths = [stage_dir/name for name in ('request.json', 'unknown.json', 'events.jsonl',
             'validated-host-result.json', 'permission-review.json', 'batch-content.js')]
    paths += [stage_dir.parent/'result.json', Path(correlation['output_file']), source,
              Path(evidence['projection_path']), Path(evidence['provenance_path']), Path(evidence['config_path'])]
    return dict(generation_id=original.generation_id, original_status='UNKNOWN', resolution=RESOLUTION,
                reason_code=REASON, original_artifact_hash=value_hash(body['output']),
                original_artifact_file_sha256=digest(source), packet_id=original.receipt.packet_id,
                packet_revision=original.receipt.packet_revision, packet_hash=original.receipt.packet_hash,
                context_hash=original.receipt.context_hash, plan_id=projection['creative_plan_id'],
                plan_revision=projection['plan_revision'], plan_hash=projection['plan_hash'], approval_id=approval_id,
                approval_hash=value_hash(approved), assets=assets, evidence=evidence,
                evidence_hashes={str(p): digest(p) for p in paths}, correlation=correlation,
                checks=['terminal_completed', 'exact_correlated_artifact', 'packet_identity', 'context',
                        'reviewed_artifact_hash', 'unchanged_sources', 'only_known_false_negative',
                        'fixed_validator_accepts_same_artifact', 'transport_permission_lifecycle_clear',
                        'projection_lineage', 'current_approval', 'current_governance_selection'])


def append(store, generation_id, *, evidence, approval_id, authorize_current, actor, validator_commit):
    require(bool(actor.strip()) and bool(validator_commit.strip()), 'audit_actor_version_required')
    original = store.status(generation_id)
    checked = assess(original, store.context(original.receipt), evidence, approval_id, authorize_current)
    record = dict(checked, reconciliation_id='REC-'+uuid4().hex,
                  resolved_at=datetime.now(timezone.utc).isoformat(), resolver=actor,
                  validator_version='planner-whitespace-reconciliation.1', validator_commit=validator_commit,
                  validator_source_sha256=digest(__file__))
    record['record_hash'] = value_hash(record)
    with store.connect() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS execution_reconciliation
            (reconciliation_id TEXT PRIMARY KEY, generation_id TEXT NOT NULL, body TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS reconciliation_no_replace BEFORE INSERT ON execution_reconciliation
            WHEN EXISTS (SELECT 1 FROM execution_reconciliation WHERE reconciliation_id=NEW.reconciliation_id)
            BEGIN SELECT RAISE(ABORT, 'reconciliation_append_only'); END;
            CREATE TRIGGER IF NOT EXISTS reconciliation_no_update BEFORE UPDATE ON execution_reconciliation
            BEGIN SELECT RAISE(ABORT, 'reconciliation_append_only'); END;
            CREATE TRIGGER IF NOT EXISTS reconciliation_no_delete BEFORE DELETE ON execution_reconciliation
            BEGIN SELECT RAISE(ABORT, 'reconciliation_append_only'); END;''')
        db.execute('INSERT INTO execution_reconciliation VALUES(?,?,?)',
                   (record['reconciliation_id'], generation_id, json.dumps(record, ensure_ascii=False)))
    return record


def verify(store, reconciliation_id, original, context, approval_id, authorize_current):
    with store.connect() as db:
        try:
            row = db.execute('SELECT body FROM execution_reconciliation WHERE reconciliation_id=?', (reconciliation_id,)).fetchone()
        except sqlite3.OperationalError:
            row = None
    require(row is not None, 'missing_record')
    record = json.loads(row[0]); check = dict(record); check.pop('record_hash')
    require(value_hash(check) == record['record_hash'], 'record_integrity_failure')
    require(record['generation_id'] == original.generation_id and record['approval_id'] == approval_id,
            'generation_or_approval_mismatch')
    require(record['validator_source_sha256'] == digest(__file__), 'validator_changed')
    checked = assess(original, context, record['evidence'], approval_id, authorize_current)
    require(all(record.get(k) == v for k, v in checked.items()), 'evidence_or_state_changed')
    return record
