"""B1 structural/assembly tests, not a claim of model semantic accuracy."""
import subprocess
from pathlib import Path
import pytest
from integrations.content_intelligence.stages import validate_output
from test_stage_execution import packet, critic

ROOT = Path(__file__).resolve().parents[1]


def test_creator_context_assembly_without_model():
    subprocess.run(['node', 'tests/creator-context-test.cjs'], cwd=ROOT, check=True)


def test_reusable_active_paths_have_no_named_creator_or_global_rejected_title():
    paths = list((ROOT/'.claude/skills/viet-script').rglob('*.md'))
    paths += list((ROOT/'.agents/skills/viet-script').rglob('*.md'))
    paths += list((ROOT/'engine/cong-thuc-viral').glob('*.md'))
    paths += [ROOT/p for p in ('AGENTS.md', 'CLAUDE.md',
        '.claude/workflows/batch-content.js', 'integrations/content_intelligence/workflow-v2.js',
        'integrations/content_intelligence/creator-context.js')]
    for path in paths:
        text = path.read_text(encoding='utf-8-sig')
        for literal in ('Hiền', 'nhi-hien', 'Tiền thuê nặng, hay phần giữ lại đang mỏng?',
                        'kể/chia sẻ cho mình nha', 'bánh kem · Pilates · Đà Nẵng',
                        'gói 90', 'P3 Storytelling'):
            assert literal not in text, (path, literal)


def test_niche_story_and_cta_examples_are_not_active_defaults():
    active = (ROOT/'engine/cong-thuc-viral/khung-7-khuc-ke-chuyen.md').read_text(encoding='utf8')
    optional = (ROOT/'engine/cong-thuc-viral/reference-examples/legacy-story-examples.md').read_text(encoding='utf8')
    example = 'Chị làm nghề này 9 năm.'
    assert example not in active and example in optional
    assert all('### Khúc '+str(i) in active for i in range(1, 8))
    # Moving illustrations must not move the recipe's safety/integration rules.
    for clause in ('Vẫn qua GATE + Ban Giám Khảo', 'LUẬT THẤU',
                   'KHÔNG bịa case, số liệu, quote', 'Voice thắng kỹ thuật',
                   'Chiến lược trước, bài sau', '**1-2 chi tiết**'):
        assert clause in active
    assert 'tiếng nồi cơm điện nhảy nút' not in active
    assert 'tiếng nồi cơm điện nhảy nút' in optional
    pas = (ROOT/'.claude/skills/viet-script/references/cong-thuc-pas-promise.md').read_text(encoding='utf8')
    archived = (ROOT/'engine/cong-thuc-viral/reference-examples/legacy-pas-example.md').read_text(encoding='utf8')
    assert 'Problem → Agitate → Solution → Result + CTA' in pas
    assert 'Đừng quên theo dõi mình' not in pas
    assert 'Đừng quên theo dõi mình' in archived


@pytest.mark.parametrize('quality', ['title_meaning_clear','reader_centered_pov','non_prescriptive_tone'])
def test_rejected_case_lesson_is_quality_rule_not_global_literal(packet, quality):
    # Supplied semantic finding: validates the veto, not automatic natural-language detection.
    result = critic()
    result[quality] = False
    result['notes'] = ['Synthetic review: rejected meaningless contrast or imposing creator POV.']
    result['findings'] = [dict(category='creative_quality', severity='advisory',
        message='Owner quality requirement failed', evidence_refs=[],
        affected_text='Tiền thuê nặng, hay phần giữ lại đang mỏng?')]
    review = validate_output('CRITIC1', result, {'packet':packet})
    assert review['verdict'] == 'REVISE'
    assert quality+'_not_confirmed' in review['blocking_issues']
