"""Phase 9 only: four bounded stages, no retry/resume or model-owned transitions."""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .adapter import encoded
from .contract import value_hash


class StageModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class Disposition(StageModel):
    strategy_field: str
    disposition: Literal['omitted', 'softened', 'blocked']
    explanation: str


class WriterOutput(StageModel):
    status: Literal['DRAFT', 'BLOCKED_PENDING_RESEARCH', 'FAILED']
    content: str
    title: str
    format: str
    issues: list[str]
    customer_evidence_ids: list[str]
    external_dispositions: list[Disposition]


FindingCategory = Literal[
    'unsupported_identity', 'scope_broadening', 'unsupported_causality', 'quote_integrity',
    'creator_truth_drift', 'external_fact_unsupported', 'market_validation_inflation',
    'purchase_validation_inflation', 'contradiction_loss', 'creative_quality', 'voice', 'format', 'other',
]
HARD_BLOCK_CATEGORIES = frozenset((
    'unsupported_identity', 'scope_broadening', 'unsupported_causality', 'quote_integrity',
    'creator_truth_drift', 'external_fact_unsupported', 'market_validation_inflation',
    'purchase_validation_inflation', 'contradiction_loss',
))


class CriticFinding(StageModel):
    category: FindingCategory
    severity: Literal['advisory', 'blocking']
    message: str
    evidence_refs: list[str]
    affected_text: str


class CriticOutput(StageModel):
    title_meaning_clear: bool
    reader_centered_pov: bool
    non_prescriptive_tone: bool
    findings: list[CriticFinding]
    verdict: Literal['PASS', 'REVISE']
    truth_preserved: bool
    selected_intent_preserved: bool
    limitations_preserved: bool
    external_claims_safe: bool
    creator_truth_preserved: bool
    context_scope_preserved: bool
    source_verification_complete: bool
    title_criteria: list[bool]
    blocking_issues: list[str]
    notes: list[str]


QUALITY_CHECKS = ('title_meaning_clear', 'reader_centered_pov', 'non_prescriptive_tone')

CHECKS = ('truth_preserved', 'selected_intent_preserved', 'limitations_preserved',
          'external_claims_safe', 'creator_truth_preserved', 'context_scope_preserved',
          'source_verification_complete')


def validate_output(stage_type, raw, context):
    if stage_type in ('WRITER', 'REWRITE'):
        draft = WriterOutput.model_validate(raw).model_dump()
        if draft['status'] == 'DRAFT':
            insight = context['packet']['customer_truth']['verified_insight']
            refs = insight['evidence_refs'] + [c['counter_ref'] for c in insight['contradictions']]
            allowed = {r['evidence_id'] for r in refs}
            expected = sorted(r['strategy_field'] for r in context['packet']['external_evidence_requirements'])
            if (not draft['content'].strip() or not draft['title'].strip() or not draft['format'].strip()
                    or not draft['customer_evidence_ids'] or not set(draft['customer_evidence_ids']) <= allowed
                    or sorted(r['strategy_field'] for r in draft['external_dispositions']) != expected
                    or any(r['disposition'] not in ('omitted', 'softened') or not r['explanation'].strip()
                           for r in draft['external_dispositions'])):
                raise ValueError('writer_output_or_provenance_invalid')
        return draft
    critic = CriticOutput.model_validate(raw).model_dump()
    if len(critic['title_criteria']) != 8 or any(not s.strip() for s in critic['notes'] + critic['blocking_issues']):
        raise ValueError('malformed_critic_result')
    blocking = list(critic['blocking_issues'])
    normalized_findings = []
    insight = context['packet']['customer_truth']['verified_insight']
    allowed_refs = {r['evidence_id'] for r in insight['evidence_refs']}
    allowed_refs.update(c['counter_ref']['evidence_id'] for c in insight['contradictions'])
    for finding in critic['findings']:
        if not finding['message'].strip() or not set(finding['evidence_refs']) <= allowed_refs:
            raise ValueError('invalid_critic_finding')
        must_block = finding['category'] in HARD_BLOCK_CATEGORIES or finding['severity'] == 'blocking'
        normalized_findings.append(dict(finding, reported_severity=finding['severity'],
                                        severity='blocking' if must_block else 'advisory'))
        if must_block:
            blocking.append(finding['category']+': '+finding['message'])
    blocking.extend(key+'_not_confirmed' for key in CHECKS if critic[key] is not True)
    blocking.extend(key+'_not_confirmed' for key in QUALITY_CHECKS if critic[key] is not True)
    if not all(critic['title_criteria']):
        blocking.append('title_criteria_not_passed')
    if critic['verdict'] == 'REVISE' and not blocking:
        blocking.append('revise_without_explanation')
    return dict(critic, findings=normalized_findings, reported_verdict=critic['verdict'],
                verdict='REVISE' if blocking else 'PASS', blocking_issues=list(dict.fromkeys(blocking)))


def stage_identity(execution, stage_type, inputs, parent=None):
    return dict(execution.receipt.model_dump(), generation_id=execution.generation_id,
                parent_generation_id=execution.parent_generation_id,
                stage_id=execution.generation_id+'-'+stage_type, stage_type=stage_type,
                parent_stage_id=parent['stage_id'] if parent else None,
                parent_artifact_hash=parent['artifact_hash'] if parent else None,
                input_hash=value_hash(inputs))


def validate_envelope(body, stage, context):
    if not isinstance(body, dict) or set(body) != {'schema_version', 'stage', 'output'}:
        raise ValueError('malformed_stage_envelope')
    if body['schema_version'] != 'reelo.host-stage.1' or encoded(body['stage']) != encoded(stage):
        raise ValueError('stage_identity_mismatch')
    if value_hash(context) != stage['context_hash']:
        raise ValueError('stage_context_mismatch')
    return validate_output(stage['stage_type'], body['output'], context)


def persist(path, body):
    """Atomic replacement with flushed bytes; completed stage files never overwritten."""
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('w', encoding='utf8') as stream:
        stream.write(encoded(body))
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def execute_stages(execution, context, work, assets, invoke):
    original_context = encoded(context)
    records = []
    execution.host = dict(profile='phase9-stage-wise', stages=records, assets=assets)
    def verify_completed():
        for previous in records:
            saved = json.loads((work/previous['stage_type']/'completed.json').read_text(encoding='utf8'))
            if (encoded(saved) != encoded(previous) or value_hash(saved['raw']) != saved['artifact_hash']
                    or value_hash(saved['normalized']) != saved['normalized_hash']):
                raise ValueError('persisted_stage_integrity_failure')

    stage_type, inputs = 'WRITER', {}
    while True:  # Only the explicit transitions below; at most four calls.
        stage = stage_identity(execution, stage_type, inputs, records[-1] if records else None)
        record = dict(stage, status=stage_type+'_RUNNING')
        stage_dir = work/stage_type
        stage_dir.mkdir(exist_ok=False)
        persist(stage_dir/'request.json', dict(stage=stage, inputs=inputs, context=context, assets=assets))
        start = time.monotonic()
        try:
            # Reload every predecessor before dispatch. Durable bytes, not model history.
            verify_completed()
            for asset in assets:
                import hashlib
                if hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest() != asset['sha256']:
                    raise ValueError('creative_asset_changed_during_execution')
            body, host = invoke(execution.model_copy(deep=True), json.loads(original_context),
                                stage, json.loads(encoded(inputs)), stage_dir, assets)
            normalized = validate_envelope(body, stage, context)
            if encoded(context) != original_context:
                raise ValueError('stage_context_mismatch')
            for asset in assets:
                import hashlib
                if hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest() != asset['sha256']:
                    raise ValueError('creative_asset_changed_during_execution')
            if not isinstance(host, dict) or not host.get('task_id') or not host.get('tool_use_id'):
                raise ValueError('stage_host_correlation_missing')
            record.update(status=stage_type+'_COMPLETED', raw=body['output'], normalized=normalized,
                          artifact_hash=value_hash(body['output']), normalized_hash=value_hash(normalized),
                          host=host, elapsed_seconds=round(time.monotonic()-start, 3))
            persist(stage_dir/'completed.json', record)
            records.append(record)
            if stage_type in ('WRITER', 'REWRITE'):
                version = len(execution.artifacts)+1
                artifact = dict(version=version, parent_version=version-1 if version > 1 else None,
                                stage_id=stage['stage_id'], content=normalized['content'], writer=normalized,
                                content_hash=value_hash(normalized['content']), path=str(stage_dir/'draft.md'))
                Path(artifact['path']).write_text(artifact['content'], encoding='utf8')
                execution.artifacts.append(artifact)
                if normalized['status'] != 'DRAFT':
                    execution.status = 'BLOCKED_PENDING_RESEARCH' if normalized['status'] == 'BLOCKED_PENDING_RESEARCH' else 'HOST_FAILED'
                    execution.validation_issues = normalized['issues'] or ['writer_reported_failure']
                    break
                inputs = {'draft': normalized}
                stage_type = 'CRITIC1' if stage_type == 'WRITER' else 'CRITIC2'
            else:
                execution.artifacts[-1].update(critic_raw=record['raw'], critic=normalized)
                if normalized['verdict'] == 'PASS' and not normalized['blocking_issues']:
                    verify_completed()
                    execution.status, execution.critic_status = 'DRAFT_READY', 'PASS'
                    break
                execution.critic_status = 'FAIL'
                if stage_type == 'CRITIC2':
                    execution.status = 'CRITIC_FAILED'
                    execution.validation_issues = normalized['blocking_issues']
                    break
                inputs = {'draft': execution.artifacts[-1]['writer'], 'critic': normalized}
                stage_type = 'REWRITE'
            persist(work/'progress.json', execution.model_dump(mode='json'))
        except Exception as exc:
            # No auto retry; verified predecessor records and drafts stay present.
            code = str(exc) if re.fullmatch(r'[a-z][a-z0-9_]+', str(exc)) else 'stage_validation_or_host_failure'
            record = dict(stage, status=stage['stage_type']+'_UNKNOWN', issue=code,
                          elapsed_seconds=round(time.monotonic()-start, 3))
            persist(stage_dir/'unknown.json', record)
            lifecycle = stage_dir/'lifecycle.json'
            if lifecycle.is_file():
                record['host_lifecycle'] = json.loads(lifecycle.read_text(encoding='utf8'))
                persist(stage_dir/'unknown.json', record)
            if records and records[-1]['stage_id'] == record['stage_id']:
                # Completed output remains on disk even if post-completion finalization failed.
                execution.host['finalization_issue'] = record
            else:
                records.append(record)
            execution.status = 'UNKNOWN'
            execution.validation_issues = ['execution_completion_unconfirmed', code]
            break
    persist(work/'result.json', execution.model_dump(mode='json'))
    return execution
