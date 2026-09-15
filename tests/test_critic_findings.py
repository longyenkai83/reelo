from copy import deepcopy

import pytest
from pydantic import ValidationError

from integrations.content_intelligence.stages import HARD_BLOCK_CATEGORIES, validate_output
from test_stage_execution import packet, draft, critic, run


def finding(category, severity='advisory', message='Unresolved scope defect', evidence_refs=None, affected_text=''):
    return dict(category=category, severity=severity, message=message,
                evidence_refs=evidence_refs or [], affected_text=affected_text)


@pytest.mark.parametrize('category', sorted(HARD_BLOCK_CATEGORIES))
@pytest.mark.parametrize('severity', ['advisory', 'blocking'])
def test_all_hard_categories_override_reported_pass_and_severity(packet, category, severity):
    raw = critic()
    raw['findings'] = [finding(category, severity)]
    original = deepcopy(raw)
    normalized = validate_output('CRITIC1', raw, {'packet': packet})
    assert raw == original
    assert normalized['reported_verdict'] == 'PASS'
    assert normalized['verdict'] == 'REVISE' and normalized['blocking_issues']
    assert normalized['findings'][0]['severity'] == 'blocking'
    assert normalized['findings'][0]['reported_severity'] == severity


@pytest.mark.parametrize('category', ['creative_quality', 'voice', 'format', 'other'])
@pytest.mark.parametrize('severity', ['advisory', 'blocking'])
def test_non_hard_categories_follow_declared_rubric_severity(packet, category, severity):
    raw = critic(); raw['findings'] = [finding(category, severity, 'Expression could be smoother')]
    result = validate_output('CRITIC1', raw, {'packet':packet})
    assert result['verdict'] == ('PASS' if severity == 'advisory' else 'REVISE')


@pytest.mark.parametrize('category,copy,message', [
    ('unsupported_identity', 'Two people describe rent differently.',
     'Two anonymous source comments do not establish two distinct people.'),
    ('unsupported_causality', 'Their different remaining income explains why these sources disagree.',
     'Separate source comments provide no evidence explaining why their experiences differ.'),
])
def test_exact_c54_findings_drive_one_rewrite_with_raw_audit(packet, tmp_path, monkeypatch, category, copy, message):
    # Synthetic controlled Critic output: this tests deterministic handling, not model detection.
    assert len(packet['customer_truth']['source_snapshots']) == 2
    assert all(s['author'] is None for s in packet['customer_truth']['source_snapshots'])
    insight = packet['customer_truth']['verified_insight']
    refs = [insight['evidence_refs'][0]['evidence_id'], insight['contradictions'][0]['counter_ref']['evidence_id']]
    bad = draft(packet); bad['content'] = copy
    first = critic()
    # The detailed defect is in notes; typed finding still makes it blocking despite PASS/advisory.
    first['notes'] = [message]
    first['findings'] = [finding(category, message='See affected text and review note.', evidence_refs=refs, affected_text=copy)]
    original = deepcopy(first)
    corrected = draft(packet); corrected['content'] = 'Two source comments contain contrasting rental statements. Their authors and circumstances are unknown.'
    result, calls, work = run(packet, tmp_path, monkeypatch, [bad, first, corrected, critic()])
    assert [s['stage_type'] for s in calls] == ['WRITER', 'CRITIC1', 'REWRITE', 'CRITIC2']
    assert result.status == 'DRAFT_READY'
    assert result.artifacts[0]['critic_raw'] == original
    assert result.artifacts[0]['critic']['verdict'] == 'REVISE'
    assert result.artifacts[0]['critic']['findings'][0]['severity'] == 'blocking'
    assert result.artifacts[-1]['critic']['findings'] == []
    assert result.artifacts[0]['content'] == copy


def test_hard_finding_at_final_critic_blocks_draft_ready(packet, tmp_path, monkeypatch):
    hard = critic(); hard['findings'] = [finding('unsupported_identity')]
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet), hard, draft(packet), hard])
    assert result.status == 'CRITIC_FAILED' and result.critic_status == 'FAIL'
    assert len(calls) == 4
    assert result.validation_issues == ['unsupported_identity: Unresolved scope defect']


def test_clean_review_and_harmless_notes_pass_without_keyword_heuristics(packet):
    raw = critic()
    raw['notes'] = ['Voice is conversational.', 'No unsupported_identity or unsupported_causality defect detected.']
    result = validate_output('CRITIC1', raw, {'packet':packet})
    assert result['verdict'] == 'PASS' and result['blocking_issues'] == []
    assert result['notes'] == raw['notes']


@pytest.mark.parametrize('mutation', ['missing_findings', 'unknown_category', 'unknown_severity', 'missing_message',
                                      'empty_message', 'invented_ref', 'extra_field', 'missing_affected_text'])
def test_malformed_findings_fail_closed(packet, mutation):
    raw = critic(); raw['findings'] = [finding('unsupported_identity')]
    if mutation == 'missing_findings': del raw['findings']
    if mutation == 'unknown_category': raw['findings'][0]['category'] = 'minor_truth_issue'
    if mutation == 'unknown_severity': raw['findings'][0]['severity'] = 'ignore'
    if mutation == 'missing_message': del raw['findings'][0]['message']
    if mutation == 'empty_message': raw['findings'][0]['message'] = ' '
    if mutation == 'invented_ref': raw['findings'][0]['evidence_refs'] = ['invented']
    if mutation == 'extra_field': raw['findings'][0]['safe_to_ignore'] = True
    if mutation == 'missing_affected_text': del raw['findings'][0]['affected_text']
    with pytest.raises((ValueError, ValidationError)):
        validate_output('CRITIC1', raw, {'packet':packet})
