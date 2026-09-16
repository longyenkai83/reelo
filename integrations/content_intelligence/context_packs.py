"""D1 deterministic projections. Local payload is private; trace contains metadata only.

READ_SUCCEEDED means this assembler read verified bytes, not model comprehension.
No discovery outside the configured manifest, no model or network calls.
"""
import hashlib
import json
from pathlib import Path

from .contract import value_hash

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_PATHS = ('engine/writing-knowledge/CORE.md',
                   'engine/writing-knowledge/recipes.json',
                   'integrations/content_intelligence/semantics-a1.json')


def asset_id(path):
    return 'asset-' + hashlib.sha256(Path(path).as_posix().encode()).hexdigest()[:24]


def catalog():
    return {r['job']: r for r in json.loads((ROOT / KNOWLEDGE_PATHS[1]).read_text(encoding='utf8'))}


def recipe_id(job):
    return 'c1:' + job


def validate_recipe(job, recipe):
    if job not in catalog() or recipe != recipe_id(job):
        raise ValueError('invalid_canonical_job_recipe')


def role(path):
    p = Path(path)
    if p.name in ('voice-profile.md', 'writing-rules.md', 'writing-rules-chi-tiet.md'):
        return 'VOICE'
    if p.name == 'about-me.md': return 'IDENTITY'
    if p.name == 'kho-cau-chuyen.md' or '/creator-experience/' in p.as_posix(): return 'STORY'
    if '/wiki/' in p.as_posix() or '/raw/' in p.as_posix(): return 'KNOWLEDGE'
    if p.name == '_INDEX.md': return 'EDITORIAL_HISTORY'
    if p.name in ('kho-cta.md', 'kho-san-pham-offer.md'): return 'OFFER_CTA'
    if 'nguyen-ly-tam-ly' in p.name: return 'PSYCHOLOGY'
    return 'REFERENCE'


def manifest(read_files, workspace):
    paths = list(read_files) + [workspace / p for p in KNOWLEDGE_PATHS]
    unique = dict.fromkeys(p.as_posix() for p in paths)
    return [dict(path=p, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p in unique]


def registry(assets):
    return [dict(a, asset_id=asset_id(a['path']), role=role(a['path'])) for a in assets]


def selected_section(text, section):
    """Only an exact unique Markdown heading; no fuzzy fallback to whole vault."""
    lines = text.splitlines()
    indexes = [i for i, line in enumerate(lines)
               if line.startswith('#') and line.lstrip('#').strip() == section.strip().lstrip('#').strip()]
    if len(indexes) != 1: raise ValueError('selected_source_section_not_unique')
    start = indexes[0]
    level = len(lines[start]) - len(lines[start].lstrip('#'))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith('#') and len(lines[i]) - len(lines[i].lstrip('#')) <= level), len(lines))
    return '\n'.join(lines[start:end])


def project_approval(approved, critic=False):
    """No unselected candidate text or full source manifest in Writer/Rewrite prompt."""
    selected = {k: v for k, v in approved.items() if k not in ('plan',)}
    proposal = approved['plan']['proposal']
    keep = ('content_job', 'recipe_id', 'format', 'treatment_or_truc', 'reader_value',
            'narrative_payoffs', 'cta_direction', 'creative_constraints', 'illustrations',
            'limitations', 'advisories', 'publication_requirements')
    selected['plan'] = {k: approved['plan'][k] for k in
                        ('creative_plan_id', 'plan_revision', 'plan_hash', 'context_hash')}
    selected['plan']['proposal'] = {k: proposal[k] for k in keep if k in proposal}
    if critic:
        for key in ('hook_candidates', 'title_candidates'):
            selected['plan']['proposal'][key] = proposal[key]
    return selected


def assemble(stage, inputs, assets, policy=None):
    """Policy is explicit operator selection by ID, never path annotations.

    Optional records: {asset_id, stages, display_note, section?}. Policy is pinned
    by the host manifest and plan approval, not an unreviewed Writer argument.
    """
    policy = policy or []
    stage = 'CRITIC' if stage.startswith('CRITIC') else stage
    if stage not in ('CREATIVE_PLAN', 'WRITER', 'CRITIC', 'REWRITE'):
        raise ValueError('invalid_context_stage')
    records = registry(assets)
    by_id = {a['asset_id']: a for a in records}
    by_path = {a['path']: a for a in records}
    selected = {}
    canonical_paths = {(ROOT / p).as_posix() for p in KNOWLEDGE_PATHS}
    for selection in policy:
        if set(selection) - {'asset_id', 'stages', 'display_note', 'section'}:
            raise ValueError('invalid_reference_selection')
        if selection['asset_id'] not in by_id: raise ValueError('unknown_reference_identity')
        if (not isinstance(selection.get('stages'), list) or not selection['stages'] or
                any(s not in ('CREATIVE_PLAN', 'WRITER', 'CRITIC', 'REWRITE') for s in selection['stages'])):
            raise ValueError('invalid_reference_stages')
        if stage in selection['stages']:
            a = by_id[selection['asset_id']]
            if a['asset_id'] in selected: raise ValueError('duplicate_reference_selection')
            if stage != 'CREATIVE_PLAN' and a['role'] in ('STORY', 'KNOWLEDGE', 'PSYCHOLOGY'):
                raise ValueError('post_approval_source_selection_requires_plan')
            if stage != 'CREATIVE_PLAN' and Path(a['path']).name in (
                    'hook-system.md', 'kho-hook.md', 'bo-tieu-de.md', 'psychology-gate.md'):
                raise ValueError('candidate_library_not_execution_context')
            selected[a['asset_id']] = ('explicit_task_reference', selection.get('section'))
    approved = inputs.get('approved_plan')
    proposal = approved['plan']['proposal'] if approved else None
    if proposal:
        validate_recipe(proposal.get('content_job'), proposal.get('recipe_id'))
    mode = (approved.get('selected_mode') or proposal['format']) if approved else inputs.get('selected_mode')
    aliases = {'Reel': 'REEL', 'Short article': 'SHORT_ARTICLE', 'Long article': 'LONG_ARTICLE'}
    mode = aliases.get(mode, mode)
    if approved and mode not in ('REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE'):
        raise ValueError('explicit_context_mode_required')
    matches = {}
    for a in records:
        if a['role'] == 'VOICE' or (stage == 'CREATIVE_PLAN' and a['role'] == 'IDENTITY'):
            selected.setdefault(a['asset_id'], ('configured_creator_' + a['role'].lower(), None))
        if stage == 'CREATIVE_PLAN' and a['role'] == 'EDITORIAL_HISTORY':
            selected.setdefault(a['asset_id'], ('editorial_recent_entries', None))
        if stage == 'CREATIVE_PLAN' and a['role'] == 'PSYCHOLOGY':
            selected.setdefault(a['asset_id'], ('runtime_psychology_compatibility', None))
        if stage == 'CRITIC' and Path(a['path']).name == 'bo-tieu-de.md':
            selected.setdefault(a['asset_id'], ('title_eight_library_verification', None))
    if approved:
        for match in approved['selected_story_refs'] + approved['selected_knowledge_refs']:
            path = Path(match['source_ref']).as_posix()
            if path not in by_path or by_path[path]['sha256'] != match['sha256']:
                raise ValueError('selected_support_not_in_manifest')
            a = by_path[path]
            matches.setdefault(a['asset_id'], []).append(match)
            selected[a['asset_id']] = ('approved_source_support', None)
        if stage == 'CRITIC':
            path = Path(approved['psychology']['library_source']).as_posix()
            if path not in by_path: raise ValueError('approved_psychology_library_required')
            selected[by_path[path]['asset_id']] = ('independent_psychology_verification', None)
    trace = dict(stage=stage, authority_inputs=['immutable CIP Zone A/B', 'stage input hash',
                 'human approval/currentness' if approved else 'PROPOSED plan only'],
                 writing_knowledge=[], creator_assets=[], reference_assets=[], source_support=[],
                 omitted_optional_families=[], receipts=[],
                 delivery='ASSEMBLED_ONLY; host delivery and model comprehension UNKNOWN',
                 auto_injection=dict(status='UNKNOWN', sources=['host project instructions',
                     'agent definition', 'embedded workflow text'],
                     note='Not explicit asset Read receipts; host may inject additional instructions.'))
    payload = dict(stage=stage, mode=mode, creator_assets=[], references=[], source_support=[],
                   available_for_matching=[], knowledge={},
                   approved_plan=project_approval(approved, stage == 'CRITIC') if approved else None)
    for a in records:
        if a['path'] in canonical_paths:
            continue
        receipt = dict(stage=stage, asset_id=a['asset_id'], path=a['path'], sha256=a['sha256'],
                       role=a['role'], states=['ALLOWED'], hash_verification='not a model read',
                       model_read='UNKNOWN')
        if a['asset_id'] not in selected:
            receipt['states'].append('OMITTED')
            receipt['reason'] = 'not_required_for_stage'
            trace['omitted_optional_families'].append(a['role'])
            if stage == 'CREATIVE_PLAN' and a['role'] in ('STORY', 'KNOWLEDGE', 'REFERENCE'):
                payload['available_for_matching'].append(a)
            trace['receipts'].append(receipt)
            continue
        reason, section = selected[a['asset_id']]
        receipt.update(reason=reason, states=['ALLOWED', 'SELECTED', 'READ_ATTEMPTED'])
        trace['receipts'].append(receipt)
        try:
            raw = Path(a['path']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != a['sha256']: raise ValueError('context_source_hash_changed')
            text = raw.decode('utf-8-sig')
            if a['asset_id'] in matches:
                text = '\n\n'.join(selected_section(text, m['section']) for m in matches[a['asset_id']])
                for m in matches[a['asset_id']]:
                    if m.get('support_quote') and m['support_quote'] not in text:
                        raise ValueError('selected_quote_not_in_section')
            elif section:
                text = selected_section(text, section)
            elif a['role'] == 'EDITORIAL_HISTORY':
                # Markdown table rows: last two entries plus header, no whole campaign history.
                rows = [line for line in text.splitlines() if line.startswith('|')]
                text = '\n'.join(rows[:2] + rows[-2:])
                if not rows: raise ValueError('editorial_selection_section_required')
            elif a['role'] in ('STORY', 'KNOWLEDGE'):
                raise ValueError('planner_source_section_required')
            receipt['states'].append('READ_SUCCEEDED')
            receipt['projection_sha256'] = hashlib.sha256(text.encode()).hexdigest()
            receipt['loaded_characters'] = len(text)
        except (OSError, UnicodeError, ValueError) as exc:
            receipt['states'].append('READ_FAILED')
            error = ValueError('context_asset_load_failed')
            error.trace = trace
            raise error from exc
        family = 'source_support' if a['role'] in ('STORY', 'KNOWLEDGE') else (
            'creator_assets' if a['role'] in ('VOICE', 'IDENTITY', 'EDITORIAL_HISTORY', 'OFFER_CTA') else 'references')
        payload[family].append(dict(a, text=text))
        trace['reference_assets' if family == 'references' else family].append(a['asset_id'])
    # Canonical projections: narrow sections, not the whole maintenance document.
    canonical = {}
    for name in KNOWLEDGE_PATHS:
        path = (ROOT / name).as_posix()
        raw = Path(path).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if path in by_path and by_path[path]['sha256'] != digest:
            raise ValueError('canonical_knowledge_changed')
        canonical[name] = raw.decode('utf8')
        trace['writing_knowledge'].append(dict(path=name, sha256=digest, outcome='ADAPTER_PROJECTION_LOADED'))
        trace['receipts'].append(dict(stage=stage, asset_id=asset_id(path), path=name, sha256=digest,
            role='CANONICAL', reason='canonical_stage_projection',
            states=['ALLOWED', 'SELECTED', 'READ_ATTEMPTED', 'READ_SUCCEEDED'],
            hash_verification='not a model read', model_read='UNKNOWN'))
    core = canonical[KNOWLEDGE_PATHS[0]]
    lenses = selected_section(core, 'Sáu lăng kính ngữ nghĩa')
    hook = selected_section(core, 'Hook').split('REEL thêm')[0]
    if mode == 'REEL':
        hook += ' REEL: SPOKEN + TEXT + VISUAL + optional AUDIO align around the same idea.'
    title = selected_section(core, 'Title')
    payload['knowledge'] = dict(core=lenses, hook=hook, title=title,
        mode={'REEL': 'Spoken Vietnamese; breath and conversational rhythm.',
              'SHORT_ARTICLE': 'Short written content, not a spoken script.',
              'LONG_ARTICLE': 'Deeper written explanation or narrative as selected.'}.get(mode, 'Mode not selected; resolve in integrated plan.'),
        recipe=next(r for r in json.loads(canonical[KNOWLEDGE_PATHS[1]]) if r['job'] == proposal['content_job'])
               if proposal else json.loads(canonical[KNOWLEDGE_PATHS[1]]))
    if stage == 'CREATIVE_PLAN':
        payload['knowledge']['prewriting'] = selected_section(core, 'Trước khi viết: một Creative Plan tích hợp')
    if matches or any(a['role'] == 'STORY' for a in payload['source_support']):
        payload['knowledge']['story'] = selected_section(core, 'Story: có công việc rõ ràng hoặc NONE')
    payload['missing_context'] = [] if any(a['role'] == 'VOICE' for a in payload['creator_assets']) else ['configured_creator_voice']
    spec = json.loads(canonical[KNOWLEDGE_PATHS[2]])
    if stage in ('CREATIVE_PLAN', 'CRITIC'):
        payload['knowledge']['title_compatibility'] = spec['title_checks']
    if stage in ('CRITIC', 'REWRITE'):
        payload['knowledge']['repair_layers'] = spec['repair_layers']
    if stage == 'REWRITE':
        payload['repair_constraint'] = 'Prose repair only; report plan/angle/truth/state defects to their layer. Do not re-plan.'
    trace['omitted_optional_families'] = sorted(set(trace['omitted_optional_families']))
    trace['payload_hash'] = value_hash(payload)
    trace['load_summary'] = {state: sum(state in r['states'] for r in trace['receipts'])
                             for state in ('ALLOWED', 'SELECTED', 'READ_ATTEMPTED', 'READ_SUCCEEDED', 'OMITTED')}
    return payload, trace
