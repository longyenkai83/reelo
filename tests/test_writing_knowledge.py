"""C1 catalog/maintenance checks, not semantic evaluation of generated prose.

No model, retrieval, private source or workflow execution is added here.
Existing runtime regressions exercise the retained source and approval guards.
"""
import json
from copy import deepcopy
from pathlib import Path

import pytest

from integrations.content_intelligence.creative_plan import validate_proposal
from tests.test_creative_plan import setup

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / 'engine/writing-knowledge'
RECIPES = json.loads((KNOWLEDGE / 'recipes.json').read_text(encoding='utf8'))
BY_JOB = {r['job']: r for r in RECIPES}
CORE = ' '.join((KNOWLEDGE / 'CORE.md').read_text(encoding='utf8').split())


def test_catalog_is_small_and_jobs_are_purposes():
    assert len(RECIPES) == len(BY_JOB) == 9
    assert set(BY_JOB) == {'TEACH', 'DIAGNOSE', 'BELIEF_SHIFT', 'STORY',
        'MISTAKE_LESSON', 'CASE_STUDY', 'REFRAME', 'PERSUADE', 'REFLECT'}


@pytest.mark.parametrize('recipe', RECIPES, ids=lambda r: r['job'])
def test_minimal_recipe_has_no_micro_approvals_or_mandatory_reference(recipe):
    assert set(recipe) == {'job', 'when_to_use', 'required_inputs', 'optional_inputs',
        'core_sequence', 'reader_value', 'truth_limits', 'completion_condition'}
    for key, value in recipe.items():
        assert isinstance(value, list if key.endswith('_inputs') or key == 'core_sequence' else str)
        assert value
        if isinstance(value, list):
            assert all(isinstance(item, str) and item.strip() for item in value)
            assert len(value) == len(set(value))
    assert not set(recipe['required_inputs']) & set(recipe['optional_inputs'])
    assert {'psychology_reference', 'contrast_technique'} <= set(recipe['optional_inputs'])
    if recipe['job'] != 'STORY':
        assert 'story_selection_DIRECT_ADJACENT_NONE' in recipe['optional_inputs']
        assert 'sourced_story_with_relevant_job' not in recipe['required_inputs']
        assert 'TENSION / CONFLICT' not in recipe['core_sequence']


def test_teach_and_reflect_have_different_payoffs():
    teach = BY_JOB['TEACH']
    assert 'USEFUL DISTINCTION' in teach['core_sequence']
    assert 'CURRENT FRAME' not in teach['core_sequence']
    assert 'supported_or_hypothetical_current_frame' not in teach['required_inputs']
    reflect = BY_JOB['REFLECT']
    assert reflect['core_sequence'][-1] == 'OPEN OR COMPLETE PAYOFF'
    assert 'APPLICATION / TAKEAWAY' not in reflect['core_sequence']
    assert 'INVITATION' not in reflect['core_sequence']
    assert 'Proof NONE' in reflect['truth_limits']


def test_story_recipe_requires_source_not_fabricated_completion():
    story = BY_JOB['STORY']
    assert 'sourced_story_with_relevant_job' in story['required_inputs']
    assert 'Không fabricate realization/emotion/result/quote/climax' in story['truth_limits']
    assert story['core_sequence'][-2:] == ['MEANING', 'READER PAYOFF']


def test_reference_optionality_does_not_remove_current_runtime_guard(setup):
    _, context, approved, assets, _ = setup
    raw = deepcopy(approved['plan']['proposal'])
    raw['psychology'] = None
    with pytest.raises(ValueError):
        validate_proposal(raw, context, assets)
    # Optional C1 reference is a knowledge capability, not an approval migration.
    assert 'chưa phải khả năng nhận null của runtime V2' in CORE


def test_hook_title_and_mode_boundaries_are_documented_without_scoring_schema():
    # Conservative maintenance signatures, not a language-quality test.
    for clause in (
        'RAPID CONTEXT + RELEVANCE + CURIOSITY / TENSION + TRUTH + CLARITY',
        'SPOKEN + TEXT + VISUAL + optional AUDIO cùng một ý',
        'SHORT_ARTICLE và LONG_ARTICLE là văn viết; không bắt Reel hook package',
        'Title đã được Owner duyệt vẫn khóa nguyên văn',
        'CLEAR, RELEVANT, FAITHFUL TO ONE IDEA, USEFUL PROMISE, NO DECODING REQUIRED',
        'không phải sáu boolean',
    ):
        assert clause in CORE


def test_all_seventeen_formats_have_explicit_dispositions():
    mapping = (KNOWLEDGE / 'ASSET-MAP.md').read_text(encoding='utf8')
    formats = sorted((ROOT / '.claude/skills/viet-script/formats').glob('*.md'))
    assert len(formats) == 17
    for path in formats:
        rows = [line for line in mapping.splitlines() if line.startswith('| ' + path.name + ' |')]
        assert len(rows) == 1
        assert any(disposition in rows[0] for disposition in (
            'KEEP AS RECIPE', 'MERGE INTO RECIPE', 'MOVE TO REFERENCE', 'LEGACY ONLY'))


def test_knowledge_model_runtime_entry_is_explicit_d1_projection():
    source = (ROOT / 'integrations/content_intelligence/host.py').read_text(encoding='utf8')
    assert 'from .context_packs import assemble' in source
    assert "'context_pack': pack" in source
