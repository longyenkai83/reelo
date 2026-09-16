"""Internal proposed creative plans and one local, explicit operator review gate.

The local operator/store is trusted, like the existing intake store. Hashes bind
versions, not user authentication. No model can emit an approval through this API.
"""
from __future__ import annotations
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field
from .contract import value_hash


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class SourceMatch(Model):
    source_ref: str
    sha256: str
    section: str
    origin: Literal['creator_story', 'creator_observation', 'external_knowledge']
    why_relevant: str
    allowed_use: str
    match_type: Literal['DIRECT', 'ADJACENT'] | None = None
    support_quote: str = ''  # Local source evidence; never export private passages.
    same_situation_supported: bool = False
    use_as_same_situation: bool = False


class Candidate(Model):
    candidate_id: str
    text: str
    rationale: str
    evidence_refs: list[str]
    intent_preserved: bool
    factual_claims_supported: bool
    natural_and_meaningful: bool
    blocking_reasons: list[str] = Field(default_factory=list)
    semantic_review: str = ''


class Psychology(Model):
    primary_mechanism: str
    optional_secondary_mechanism: str | None
    library_source: str = ''  # D1 resolves an ID to the pinned exact path.
    rationale: str
    reference_id: str | None = None


class Illustration(Model):
    description: str
    origin: Literal['illustrative_ai']
    disclosure: str


class NarrativePayoff(Model):
    source_ref: str
    section: str
    story_job: str
    setup: str
    tension_or_turn: str
    meaning: str
    reader_payoff: str


class PlanProposal(Model):
    content_job: str | None = None  # Historical plans retain absent fields.
    recipe_id: str | None = None
    packet_id: str
    verified_insight_id: str
    angle_id: str
    truth_type: Literal['PROPOSED']
    story_matches: list[SourceMatch]
    knowledge_matches: list[SourceMatch]
    illustrations: list[Illustration]
    psychology: Psychology
    format: str
    treatment_or_truc: str
    hook_candidates: list[Candidate] = Field(min_length=2)
    title_candidates: list[Candidate] = Field(min_length=2)
    recommended_hook_id: str
    recommended_title_id: str
    outline: list[str] = Field(min_length=1)
    reader_value: list[str] = Field(min_length=1)
    narrative_payoffs: list[NarrativePayoff]
    reader_value_clear: bool
    narrative_payoff_clear: bool
    cta_direction: str
    creative_constraints: list[str]
    truth_preserved: bool
    selected_intent_preserved: bool
    reader_centered_pov: bool
    non_prescriptive_tone: bool
    issues: list[str] = Field(default_factory=list)  # Historical, unclassified: fail closed.
    blocking_issues: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    advisories: list[str] = Field(default_factory=list)
    publication_requirements: list[str] = Field(default_factory=list)
    outline_blocking_issues: list[str] = Field(default_factory=list)


class Review(Model):
    decision: Literal['approved', 'EDIT_AND_APPROVE', 'rejected', 'deferred']
    reviewer: str = Field(min_length=1)
    human_attested: Literal[True]
    approval_kind: Literal['human', 'synthetic_fixture'] = 'human'
    expected_plan_hash: str
    hook_id: str | None = None
    title_id: str | None = None
    edited_hook: str | None = None
    edited_title: str | None = None
    edited_outline: list[str] | None = None
    selected_mode: Literal['REEL', 'SHORT_ARTICLE', 'LONG_ARTICLE'] | None = None
    knowledge_choice_policy: str | None = None


def source_role(path):
    p = Path(path).as_posix().lower()
    if 'kho-cau-chuyen' in p or '/creator-experience/' in p:
        return 'creator'
    if '/wiki/' in p or '/raw/' in p:
        return 'knowledge'
    return 'reference'


def validate_proposal(raw, context, assets):
    from .purified_plan import is_purified, validate
    if is_purified(raw): return validate(raw, context, assets)
    p = PlanProposal.model_validate(raw).model_dump()
    from .context_packs import validate_recipe, asset_id
    if p['content_job'] is not None or p['recipe_id'] is not None:
        validate_recipe(p['content_job'], p['recipe_id'])
    for key in ('content_job', 'recipe_id'):
        if key not in raw: p.pop(key)
    reference = p['psychology'].get('reference_id')
    if reference:
        found = [a for a in assets if asset_id(a['path']) == reference]
        if len(found) != 1 or (p['psychology']['library_source'] and
                             Path(p['psychology']['library_source']).as_posix() != found[0]['path']):
            raise ValueError('psychology_reference_identity_mismatch')
        p['psychology']['library_source'] = found[0]['path']
    if 'reference_id' not in raw['psychology']: p['psychology'].pop('reference_id')
    packet = context['packet']
    vi = packet['customer_truth']['verified_insight']
    if (p['packet_id'] != packet['packet_id'] or p['angle_id'] != packet['content_strategy']['angle']['angle_id']
            or p['verified_insight_id'] != vi['verified_insight_id']):
        raise ValueError('plan_upstream_identity_mismatch')
    allow = {Path(a['path']).as_posix(): a['sha256'] for a in assets}
    for group, role in [('story_matches', 'creator'), ('knowledge_matches', 'knowledge')]:
        for m in p[group]:
            path = Path(m['source_ref']).as_posix()
            if (path not in allow or m['sha256'] != allow[path] or source_role(path) != role
                    or (role == 'creator' and m['origin'] == 'external_knowledge')
                    or (role == 'knowledge' and m['origin'] != 'external_knowledge')):
                raise ValueError('plan_source_origin_invalid')
            if not all(m[k].strip() for k in ('section', 'why_relevant', 'allowed_use')):
                raise ValueError('plan_source_use_missing')
            if role == 'creator' and m['support_quote']:
                if m['support_quote'] not in Path(path).read_text(encoding='utf8'):
                    raise ValueError('story_support_not_in_source')
    lib = Path(p['psychology']['library_source']).as_posix()
    if lib not in allow or 'nguyen-ly-tam-ly' not in lib:
        raise ValueError('approved_psychology_library_required')
    library_text = ' '.join(Path(lib).read_text(encoding='utf8').casefold().split())
    for mechanism in (p['psychology']['primary_mechanism'], p['psychology']['optional_secondary_mechanism']):
        if mechanism is not None and (not mechanism.strip() or ' '.join(mechanism.casefold().split()) not in library_text):
            raise ValueError('psychology_mechanism_not_in_library')
    refs = {r['evidence_id'] for r in vi['evidence_refs']}
    refs.update(c['counter_ref']['evidence_id'] for c in vi['contradictions'])
    for group, recommendation in [('hook_candidates', 'recommended_hook_id'), ('title_candidates', 'recommended_title_id')]:
        ids = [c['candidate_id'] for c in p[group]]
        if len(ids) != len(set(ids)) or p[recommendation] not in ids:
            raise ValueError('invalid_candidate_selection')
        for c in p[group]:
            if not c['text'].strip() or not c['rationale'].strip() or not set(c['evidence_refs']) <= refs:
                raise ValueError('invalid_candidate_provenance')
    if not all(x.strip() for x in p['outline']) or not p['format'].strip() or not p['treatment_or_truc'].strip():
        raise ValueError('incomplete_creative_plan')
    if any(not i['disclosure'].strip() for i in p['illustrations']):
        raise ValueError('illustration_disclosure_required')
    if len(p['reader_value']) != len(p['outline']) or any(not v.strip() for v in p['reader_value']):
        raise ValueError('reader_value_required_for_every_section')
    return p


def candidate_eligibility(c):
    reasons = list(c.get('blocking_reasons', []))
    reasons += [k for k in ('intent_preserved', 'factual_claims_supported', 'natural_and_meaningful') if not c[k]]
    return dict(state='blocked' if reasons else 'selectable', reasons=reasons)


def plan_blockers(p):
    from .purified_plan import execution_view
    p = execution_view(p)
    failures = list(p.get('issues', [])) + list(p.get('blocking_issues', [])) + list(p.get('outline_blocking_issues', []))
    failures += [k for k in ('truth_preserved', 'selected_intent_preserved', 'reader_centered_pov', 'non_prescriptive_tone') if not p[k]]
    failures += [k for k in ('reader_value_clear', 'narrative_payoff_clear') if not p.get(k)]
    payoffs = p.get('narrative_payoffs', [])
    for m in p['story_matches']:
        found = [x for x in payoffs if (x['source_ref'], x['section']) == (m['source_ref'], m['section'])]
        if len(found) != 1 or any(not found[0][k].strip() for k in
                ('story_job', 'setup', 'tension_or_turn', 'meaning', 'reader_payoff')):
            failures.append('story_job_and_payoff_required')
    if any(not any((x['source_ref'], x['section']) == (m['source_ref'], m['section'])
                   for m in p['story_matches']) for x in payoffs):
        failures.append('payoff_requires_selected_story')
    for m in p['story_matches']:
        if not m.get('match_type') or not m.get('support_quote', '').strip():
            failures.append('story_classification_and_source_support_required')
        if m.get('match_type') == 'DIRECT' and not m.get('same_situation_supported'):
            failures.append('direct_story_experience_not_supported')
        if m.get('match_type') == 'ADJACENT' and m.get('use_as_same_situation'):
            failures.append('adjacent_story_cannot_be_same_experience')
    for group, recommendation in [('hook_candidates', 'recommended_hook_id'), ('title_candidates', 'recommended_title_id')]:
        safe = [c['candidate_id'] for c in p[group] if candidate_eligibility(c)['state'] == 'selectable']
        if not safe:
            failures.append(group+':no_safe_alternative')
        if p[recommendation] not in safe:
            failures.append(recommendation+':blocked_recommendation')
    return failures


def review_readiness(p, context, *, human_approved=False):
    """Conservative review projection, never a publication authorization.

    Packet requirements cannot be cleared by model omission/softening or plan approval.
    Semantic judgments require source review; deterministic checks do not prove meaning.
    """
    from .purified_plan import is_purified, execution_view, gate
    if is_purified(p):
        result = review_readiness(execution_view(p), context, human_approved=human_approved)
        result.pop('candidates')
        result['integrated_plan'] = gate(p)
        result['integrated_plan']['publication_requirements'] = result['publication_requirements']
        return result
    requirements = list(p.get('publication_requirements', []))
    requirements += [json.dumps(r, ensure_ascii=False, sort_keys=True)
                     for r in context['packet'].get('external_evidence_requirements', [])]
    blockers = plan_blockers(p)
    return dict(blocking_issues=blockers, limitations=p.get('limitations', []),
                advisories=p.get('advisories', []), publication_requirements=requirements,
                ready_for_owner_review=not blockers, ready_to_write=human_approved and not blockers,
                ready_to_publish=False, publication_blocked_by_requirements=bool(requirements),
                story_types=[m.get('match_type') for m in p['story_matches']] or
                            (['ILLUSTRATIVE_AI'] if p['illustrations'] else ['NONE']),
                candidates={group: [dict(**c, eligibility=candidate_eligibility(c)) for c in p[group]]
                            for group in ('hook_candidates', 'title_candidates')})


class PlanStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS plans
                (plan_id TEXT PRIMARY KEY, packet_id TEXT, revision INTEGER, body TEXT);
                CREATE TABLE IF NOT EXISTS reviews
                (approval_id TEXT PRIMARY KEY, plan_id TEXT, body TEXT);''')

    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        return db

    def save(self, proposal, context, assets, generation_id, *, revision_audit=None):
        proposal = validate_proposal(proposal, context, assets)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if revision_audit is not None:
                current = db.execute('SELECT plan_id FROM plans WHERE packet_id=? ORDER BY revision DESC LIMIT 1',
                                     (proposal['packet_id'],)).fetchone()
                if not current or current[0] != revision_audit['parent_plan_id']:
                    raise ValueError('superseded_creative_plan')
            rev = db.execute('SELECT COALESCE(MAX(revision),0)+1 FROM plans WHERE packet_id=?', (proposal['packet_id'],)).fetchone()[0]
            plan = dict(creative_plan_id='CP-'+uuid4().hex, plan_revision=rev, context_hash=value_hash(context),
                        proposal=proposal, assets=assets, generation_id=generation_id,
                        created_at=datetime.now(timezone.utc).isoformat(), blockers=plan_blockers(proposal),
                        review_view=review_readiness(proposal, context))
            if revision_audit is not None: plan['revision_audit'] = revision_audit
            plan['plan_hash'] = value_hash(plan)
            db.execute('INSERT INTO plans VALUES(?,?,?,?)', (plan['creative_plan_id'], proposal['packet_id'], rev, json.dumps(plan)))
        return plan

    def get(self, plan_id):
        with self.connect() as db:
            row = db.execute('SELECT body FROM plans WHERE plan_id=?', (plan_id,)).fetchone()
        if not row: raise ValueError('unknown_creative_plan')
        p = json.loads(row[0]); check = dict(p); check.pop('plan_hash')
        if value_hash(check) != p['plan_hash']: raise ValueError('plan_integrity_failure')
        return p

    def review(self, plan_id, raw):
        review = Review.model_validate(raw).model_dump()
        owner_decision = review['decision']
        if owner_decision == 'EDIT_AND_APPROVE':
            review['decision'] = 'approved'
        plan = self.get(plan_id); p = plan['proposal']
        from .purified_plan import is_purified, execution_view
        if is_purified(p):
            if any(review[k] is not None for k in ('edited_hook', 'edited_title', 'edited_outline')):
                raise ValueError('purified_edit_requires_plan_revision')
            if review['selected_mode'] is not None and review['selected_mode'] != p['format']:
                raise ValueError('mode_edit_requires_plan_revision')
            review['selected_mode'] = p['format']
            # Internal compatibility titles are not additional human choices.
            allowed_titles = [p['title_plan']['recommended']['candidate_id']]
            if p['title_plan']['alternative']: allowed_titles.append(p['title_plan']['alternative']['candidate_id'])
            if review['title_id'] is not None and review['title_id'] not in allowed_titles:
                raise ValueError('internal_title_requires_new_plan_revision')
            p = execution_view(p)
        if review['expected_plan_hash'] != plan['plan_hash']: raise ValueError('stale_plan_review')
        if review['decision'] == 'approved' and (plan['blockers'] or plan_blockers(p)):
            raise ValueError('blocked_plan_cannot_be_approved')
        if review['approval_kind'] == 'synthetic_fixture' and not review['reviewer'].startswith('SYNTHETIC TEST'):
            raise ValueError('synthetic_reviewer_label_required')
        def choose(group, key, default, edited):
            cid = review[key] or p[default]
            found = next((c for c in p[group] if c['candidate_id'] == cid), None)
            if not found: raise ValueError('unknown_candidate_id')
            if review['decision'] == 'approved' and candidate_eligibility(found)['state'] == 'blocked':
                raise ValueError('blocked_candidate_cannot_be_selected')
            text = review[edited] if review[edited] is not None else found['text']
            if not text.strip(): raise ValueError('empty_creative_selection')
            return dict(candidate_id=cid, text=text)
        outline = review['edited_outline'] if review['edited_outline'] is not None else p['outline']
        if not outline or not all(s.strip() for s in outline): raise ValueError('empty_approved_outline')
        if review['decision'] == 'approved' and len(outline) != len(p.get('reader_value', [])):
            raise ValueError('outline_edit_requires_new_reader_value_plan')
        result = dict(approval_id='CPA-'+uuid4().hex, plan=plan, **review,
                      owner_decision=owner_decision,
                      limitations=p.get('limitations', []),
                      publication_requirements=plan.get('review_view', {}).get('publication_requirements', []),
                      approved_at=datetime.now(timezone.utc).isoformat() if review['decision'] == 'approved' else None,
                      creative_plan_id=plan_id, plan_revision=plan['plan_revision'],
                      packet_id=p['packet_id'], angle_id=p['angle_id'],
                      selected_story_refs=p['story_matches'], selected_knowledge_refs=p['knowledge_matches'],
                      psychology=p['psychology'], format=p['format'], treatment=p['treatment_or_truc'],
                      selected_hook=choose('hook_candidates', 'hook_id', 'recommended_hook_id', 'edited_hook'),
                      selected_title=choose('title_candidates', 'title_id', 'recommended_title_id', 'edited_title'),
                      approved_outline=outline)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            latest = db.execute('SELECT plan_id FROM plans WHERE packet_id=? ORDER BY revision DESC LIMIT 1', (p['packet_id'],)).fetchone()[0]
            if latest != plan_id: raise ValueError('superseded_creative_plan')
            db.execute('INSERT INTO reviews VALUES(?,?,?)', (result['approval_id'], plan_id, json.dumps(result)))
        return result

    def revise(self, plan_id, proposal, context, assets, *, reviewer, human_attested, expected_plan_hash):
        """Append a pending revision. Never carries approval across a consequential edit."""
        from .purified_plan import is_purified
        old = self.get(plan_id)
        if human_attested is not True or not isinstance(reviewer, str) or not reviewer.strip():
            raise ValueError('human_plan_revision_required')
        if old['plan_hash'] != expected_plan_hash: raise ValueError('stale_plan_review')
        if not is_purified(old['proposal']) or not is_purified(proposal):
            raise ValueError('explicit_purified_revision_required')
        if old['context_hash'] != value_hash(context): raise ValueError('plan_upstream_identity_mismatch')
        if any(proposal[k] != old['proposal'][k] for k in ('packet_id', 'angle_id', 'verified_insight_id', 'one_idea')):
            raise ValueError('upstream_owner_correction_required')
        with self.connect() as db:
            latest = db.execute('SELECT plan_id FROM plans WHERE packet_id=? ORDER BY revision DESC LIMIT 1',
                                (old['proposal']['packet_id'],)).fetchone()[0]
        if latest != plan_id: raise ValueError('superseded_creative_plan')
        return self.save(proposal, context, assets, 'OWNER-REVISION', revision_audit=dict(
            parent_plan_id=plan_id, parent_plan_hash=expected_plan_hash, reviewer=reviewer,
            human_attested=True, approval_inherited=False))

    def approved(self, approval_id, context, assets):
        with self.connect() as db:
            row = db.execute('SELECT body,plan_id FROM reviews WHERE approval_id=?', (approval_id,)).fetchone()
            if not row: raise ValueError('human_creative_approval_required')
            a = json.loads(row['body']); plan = self.get(row['plan_id'])
            latest = db.execute('SELECT plan_id FROM plans WHERE packet_id=? ORDER BY revision DESC LIMIT 1', (plan['proposal']['packet_id'],)).fetchone()[0]
            last_review = db.execute('SELECT approval_id FROM reviews WHERE plan_id=? ORDER BY rowid DESC LIMIT 1', (row['plan_id'],)).fetchone()[0]
        if a['decision'] != 'approved' or latest != row['plan_id'] or last_review != approval_id:
            raise ValueError('approval_not_current')
        if a['plan'] != plan or plan['context_hash'] != value_hash(context) or plan['assets'] != assets:
            raise ValueError('approval_plan_or_assets_changed')
        for asset in assets:
            if hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest() != asset['sha256']:
                raise ValueError('approved_source_changed')
        validate_proposal(plan['proposal'], context, assets)
        if plan_blockers(plan['proposal']):
            raise ValueError('blocked_plan_cannot_be_executed')
        if a['approval_kind'] == 'synthetic_fixture' and 'synthetic_fixture' not in context['packet']['project']['source_route_context']:
            raise ValueError('synthetic_approval_requires_synthetic_packet')
        return a
