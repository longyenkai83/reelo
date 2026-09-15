from copy import deepcopy

import pytest
from integrations.content_intelligence.stages import QUALITY_CHECKS, validate_output
from test_stage_execution import packet, draft, critic, run


@pytest.mark.parametrize('field', QUALITY_CHECKS)
def test_owner_quality_veto_cannot_be_downgraded_to_note(packet, field):
    raw = critic(); raw[field] = False
    raw['notes'] = ['Owner quality requirement not met']
    original = deepcopy(raw)
    result = validate_output('CRITIC1', raw, {'packet':packet})
    assert raw == original and result['reported_verdict'] == 'PASS'
    assert result['verdict'] == 'REVISE'
    assert field+'_not_confirmed' in result['blocking_issues']


@pytest.mark.parametrize('field', QUALITY_CHECKS)
@pytest.mark.parametrize('value', [None, 'true', 1])
def test_quality_checks_are_required_strict_booleans(packet, field, value):
    raw = critic()
    if value is None: del raw[field]
    else: raw[field] = value
    with pytest.raises(ValueError): validate_output('CRITIC1', raw, {'packet':packet})


@pytest.mark.parametrize('field', QUALITY_CHECKS)
def test_quality_failure_uses_existing_single_rewrite_cycle(packet, tmp_path, monkeypatch, field):
    fail = critic(); fail[field] = False
    fail['findings'] = [dict(category='voice' if field != 'title_meaning_clear' else 'creative_quality',
        severity='blocking', message='Owner requirement not met', affected_text='Synthetic failing copy', evidence_refs=[])]
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet), fail, draft(packet), critic()])
    assert result.status == 'DRAFT_READY' and len(calls) == 4
    assert result.artifacts[0]['critic_raw'][field] is False
    assert result.artifacts[-1]['critic'][field] is True


def test_good_quality_does_not_override_hard_truth_finding(packet):
    raw = critic()
    raw['findings'] = [dict(category='unsupported_identity', severity='advisory',
        message='An attractive title invents reader identity', affected_text='', evidence_refs=[])]
    assert validate_output('CRITIC1', raw, {'packet':packet})['verdict'] == 'REVISE'


def test_personal_story_exception_is_semantic_not_pronoun_counter(packet, tmp_path, monkeypatch):
    # Controlled semantic PASS may contain many creator pronouns; code never counts words.
    story = draft(packet); story['content'] = 'I / mình / tôi / Hiền: synthetic personal-story-first fixture.'
    result, calls, _ = run(packet, tmp_path, monkeypatch, [story, critic()])
    assert result.status == 'DRAFT_READY' and len(calls) == 2

@pytest.mark.parametrize('field', QUALITY_CHECKS)
def test_unresolved_owner_quality_after_rewrite_is_not_ready(packet, tmp_path, monkeypatch, field):
    fail = critic(); fail[field] = False
    result, calls, _ = run(packet, tmp_path, monkeypatch, [draft(packet), fail, draft(packet), fail])
    assert result.status == 'CRITIC_FAILED' and len(calls) == 4
    assert field+'_not_confirmed' in result.validation_issues
