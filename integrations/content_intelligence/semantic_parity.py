"""Offline maintenance checks for RP3.A. Never imported by the creative runtime.

Canonical meaning lives in semantics-a1.json. Clause signatures deliberately require
review when wording changes; they are not an entailment engine. Runtime behavioral
tests complement these checks. No private assets, state stores or model calls.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = Path(__file__).with_name('semantics-a1.json')


def load_spec():
    return json.loads(SPEC_PATH.read_text(encoding='utf8'))


def normalized(text):
    return ' '.join(text.replace('**', '').split()).casefold()


def check_mirrors(root=ROOT, *, overrides=None):
    """Return actionable drift IDs. Overrides allow mutation tests without disk edits."""
    spec = load_spec()
    overrides = overrides or {}
    issues = []
    def read(path):
        if path in overrides:
            return overrides[path]
        try:
            return (root / path).read_text(encoding='utf-8-sig')
        except OSError:
            issues.append('missing_mirror:' + path)
            return ''
    def require(path, text, rule):
        if normalized(text) not in normalized(read(path)):
            issues.append(rule + ':' + path)

    workflow = 'integrations/content_intelligence/workflow-v2.js'
    for mode, rule in spec['modes'].items():
        require(workflow, rule['representation'], 'mode:' + mode)
    for mirror in spec['mirrors']:
        for index, clause in enumerate(mirror['required']):
            require(mirror['path'], clause, 'required_semantic:' + str(index))
    for mirror in spec['historical_word_counts']['mirrors']:
        require(mirror['path'], mirror['text'], 'legacy_word_range')

    rubric_path = 'engine/cong-thuc-viral/cong-kiem-chat-luong.md'
    rubric = read(rubric_path)
    section = re.search(r'^#### .*LỚP 3:.*?(?=^#### |\Z)', rubric, re.M | re.S)
    rubric = section.group(0) if section else ''
    # Match each criterion's own body, not a coincidental phrase elsewhere.
    rows = re.findall(r'^- \[ \] \*\*([①②③④⑤⑥⑦⑧]) (.*?)(?=^- \[ \]|\Z)',
                      rubric, flags=re.M | re.S)
    if [symbol for symbol, _ in rows] != list('①②③④⑤⑥⑦⑧'):
        issues.append('title_rubric_shape')
    by_symbol = dict(rows)
    for rule in spec['title_checks']:
        body = by_symbol.get(chr(0x2460 + rule['id'] - 1), '')
        for anchor in rule['anchors']:
            if normalized(anchor) not in normalized(body):
                issues.append('title_meaning:' + str(rule['id']) + ':' + anchor)

    js = read(workflow)
    bounds = re.search(r'title_criteria:\s*\{[^}]*minItems:\s*(\d+),\s*maxItems:\s*(\d+)', js)
    expected = str(len(spec['title_checks']))
    if not bounds or bounds.groups() != (expected, expected):
        issues.append('v2_title_schema_count')
    # Inspect the actual category/severity/verdict schema, not occurrences in prose.
    for field, expected_values in (
        ('category', set(spec['hard_categories']) | {'creative_quality', 'voice', 'format', 'other'}),
        ('severity', {'advisory', 'blocking'}),
        ('verdict', {'PASS', 'REVISE'}),
    ):
        match = re.search(field + r":\s*\{\s*type:\s*'string',\s*enum:\s*\[([^\]]+)\]", js)
        actual = set(re.findall(r"'([^']+)'", match.group(1))) if match else set()
        if actual != expected_values:
            issues.append('critic_schema:' + field)

    python = read('integrations/content_intelligence/stages.py')
    try:
        tree = ast.parse(python)
        hard = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'HARD_BLOCK_CATEGORIES'
                            for t in node.targets))
        actual = set(ast.literal_eval(hard.args[0]))
        if actual != set(spec['hard_categories']):
            issues.append('python_hard_categories')
    except (SyntaxError, StopIteration, AttributeError, ValueError, TypeError):
        issues.append('python_hard_categories')

    # Existing embedding requires exact equality; legitimate other representations
    # above use their own clauses/schema, never cross-host byte equality.
    if js not in read('.claude/workflows/batch-content.js'):
        issues.append('embedded_workflow_sync')
    return issues


if __name__ == '__main__':
    failures = check_mirrors()
    print(json.dumps(failures, ensure_ascii=True) if failures else 'A1 canonical mirror parity PASS')
    raise SystemExit(bool(failures))
