"""Offline semantic regressions. No real Planner/Writer, private assets or APIs."""
from copy import deepcopy
from typing import get_args
import pytest

from integrations.content_intelligence.semantic_parity import ROOT, load_spec, check_mirrors
from integrations.content_intelligence.stages import (
    HARD_BLOCK_CATEGORIES, CriticOutput, CriticFinding, validate_output,
)
from integrations.content_intelligence.creative_plan import review_readiness
from test_stage_execution import packet, critic, draft
from test_creative_plan import setup

SPEC = load_spec()
WORKFLOW = 'integrations/content_intelligence/workflow-v2.js'
RUBRIC = 'engine/cong-thuc-viral/cong-kiem-chat-luong.md'


def text(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


def test_all_current_mirrors_match_canonical_semantics():
    assert [r['id'] for r in SPEC['title_checks']] == list(range(1, 9))
    assert len(SPEC['hard_categories']) == 9
    assert check_mirrors() == []


def test_python_category_loss_is_detected_even_if_js_is_unchanged():
    path = 'integrations/content_intelligence/stages.py'
    altered = text(path).replace("'unsupported_identity',", '')
    assert 'python_hard_categories' in check_mirrors(overrides={path: altered})


@pytest.mark.parametrize('mode', list(SPEC['modes']))
def test_spoken_written_mode_drift_is_detected(mode):
    old = SPEC['modes'][mode]['representation']
    altered = text(WORKFLOW).replace(old, mode + ' means any platform format')
    assert 'mode:' + mode + ':' + WORKFLOW in check_mirrors(overrides={WORKFLOW: altered})


@pytest.mark.parametrize('rule', SPEC['title_checks'], ids=lambda r: str(r['id']))
def test_each_title_meaning_missing_is_detected(rule):
    anchor = rule['anchors'][0]
    altered = text(RUBRIC).replace(anchor, 'REMOVED SEMANTIC')
    assert any(i.startswith('title_meaning:' + str(rule['id']) + ':')
               for i in check_mirrors(overrides={RUBRIC: altered}))


@pytest.mark.parametrize('count', [7, 9])
def test_js_title_count_drift_is_detected(count):
    altered = text(WORKFLOW).replace('minItems: 8, maxItems: 8',
                                    f'minItems: {count}, maxItems: {count}')
    assert 'v2_title_schema_count' in check_mirrors(overrides={WORKFLOW: altered})


@pytest.mark.parametrize('mirror', SPEC['mirrors'], ids=lambda m: m['path'])
def test_missing_required_host_semantics_is_detected(mirror):
    assert check_mirrors(overrides={mirror['path']: ''})


@pytest.mark.parametrize('rule', SPEC['historical_word_counts']['mirrors'], ids=lambda m: m['path'])
def test_numeric_guidance_cannot_silently_choose_a_winner(rule):
    changed = text(rule['path']).replace(rule['text'], 'NEW UNIVERSAL RANGE')
    assert 'legacy_word_range:' + rule['path'] in check_mirrors(overrides={rule['path']: changed})


@pytest.mark.parametrize('category', SPEC['hard_categories'])
def test_canonical_nine_cannot_be_lost_or_downgraded(packet, category):
    assert HARD_BLOCK_CATEGORIES == frozenset(SPEC['hard_categories'])
    value = critic()
    value['findings'] = [dict(category=category, severity='advisory',
        message='Synthetic unsupported claim', evidence_refs=[], affected_text='Synthetic')]
    value['notes'] = ['Publication requirement: verify later']
    result = validate_output('CRITIC1', value, {'packet': packet})
    assert result['verdict'] == 'REVISE'
    assert result['findings'][0]['severity'] == 'blocking'
    changed = text(WORKFLOW).replace("'" + category + "'", "'other'")
    assert 'critic_schema:category' in check_mirrors(overrides={WORKFLOW: changed})


@pytest.mark.parametrize('index', range(8))
def test_every_existing_title_check_blocks_pass(packet, index):
    value = critic()
    value['title_criteria'][index] = False
    assert validate_output('CRITIC1', value, {'packet': packet})['verdict'] == 'REVISE'


@pytest.mark.parametrize('count', [7, 9])
def test_python_title_shape_not_seven_or_nine(packet, count):
    value = critic()
    value['title_criteria'] = [True] * count
    with pytest.raises(ValueError, match='malformed_critic_result'):
        validate_output('CRITIC1', value, {'packet': packet})


def test_unknown_never_a_quality_verdict_or_severity(packet):
    assert set(get_args(CriticOutput.model_fields['verdict'].annotation)) == {'PASS', 'REVISE'}
    assert set(get_args(CriticFinding.model_fields['severity'].annotation)) == {'blocking', 'advisory'}
    value = critic()
    value['verdict'] = 'UNKNOWN'
    with pytest.raises(ValueError):
        validate_output('CRITIC1', value, {'packet': packet})
    changed = text(WORKFLOW).replace("enum: ['PASS', 'REVISE']", "enum: ['PASS', 'REVISE', 'UNKNOWN']")
    assert 'critic_schema:verdict' in check_mirrors(overrides={WORKFLOW: changed})


def test_publication_requirements_do_not_allow_unsupported_draft(setup):
    packet, context, approved, _, _ = setup
    proposal = deepcopy(approved['plan']['proposal'])
    proposal['publication_requirements'] = ['Verify external claim before publication']
    view = review_readiness(proposal, context, human_approved=True)
    assert view['ready_to_write'] and not view['ready_to_publish']
    value = draft(packet)
    value['external_dispositions'][0]['disposition'] = 'blocked'
    with pytest.raises(ValueError, match='writer_output_or_provenance_invalid'):
        validate_output('WRITER', value, context)


def test_repair_map_is_non_executable_and_grants_no_authority():
    assert SPEC['repair_layers'] == {
        'prose': 'Writer/Rewrite', 'plan_expression': 'Planner/Human Creative Gate',
        'angle_meaning': 'upstream Owner correction',
        'customer_evidence_truth': 'Customer Intelligence', 'state_source_approval': 'Platform',
    }
    # The maintenance layer cannot silently become a creative dispatcher/router.
    for path in (ROOT / 'integrations/content_intelligence').glob('*.py'):
        if path.name in ('semantic_parity.py', 'context_packs.py'):
            continue
        assert 'semantic_parity' not in path.read_text(encoding='utf-8-sig')
        assert 'semantics-a1.json' not in path.read_text(encoding='utf-8-sig')
