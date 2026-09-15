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


class Candidate(Model):
    candidate_id: str
    text: str
    rationale: str
    evidence_refs: list[str]
    intent_preserved: bool
    factual_claims_supported: bool
    natural_and_meaningful: bool


class Psychology(Model):
    primary_mechanism: str
    optional_secondary_mechanism: str | None
    library_source: str
    rationale: str


class Illustration(Model):
    description: str
    origin: Literal['illustrative_ai']
    disclosure: str


class PlanProposal(Model):
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
    cta_direction: str
    creative_constraints: list[str]
    truth_preserved: bool
    selected_intent_preserved: bool
    reader_centered_pov: bool
    non_prescriptive_tone: bool
    issues: list[str]


class Review(Model):
    decision: Literal['approved', 'rejected', 'deferred']
    reviewer: str = Field(min_length=1)
    human_attested: Literal[True]
    approval_kind: Literal['human', 'synthetic_fixture'] = 'human'
    expected_plan_hash: str
    hook_id: str | None = None
    title_id: str | None = None
    edited_hook: str | None = None
    edited_title: str | None = None
    edited_outline: list[str] | None = None


def source_role(path):
    p = Path(path).as_posix().lower()
    if 'kho-cau-chuyen' in p or '/creator-experience/' in p:
        return 'creator'
    if '/wiki/' in p or '/raw/' in p:
        return 'knowledge'
    return 'reference'


def validate_proposal(raw, context, assets):
    p = PlanProposal.model_validate(raw).model_dump()
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
    return p


def plan_blockers(p):
    failures = list(p['issues'])
    failures += [k for k in ('truth_preserved', 'selected_intent_preserved', 'reader_centered_pov', 'non_prescriptive_tone') if not p[k]]
    for c in p['hook_candidates'] + p['title_candidates']:
        failures += [c['candidate_id']+':'+k for k in ('intent_preserved', 'factual_claims_supported', 'natural_and_meaningful') if not c[k]]
    return failures


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

    def save(self, proposal, context, assets, generation_id):
        proposal = validate_proposal(proposal, context, assets)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rev = db.execute('SELECT COALESCE(MAX(revision),0)+1 FROM plans WHERE packet_id=?', (proposal['packet_id'],)).fetchone()[0]
            plan = dict(creative_plan_id='CP-'+uuid4().hex, plan_revision=rev, context_hash=value_hash(context),
                        proposal=proposal, assets=assets, generation_id=generation_id,
                        created_at=datetime.now(timezone.utc).isoformat(), blockers=plan_blockers(proposal))
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
        plan = self.get(plan_id); p = plan['proposal']
        if review['expected_plan_hash'] != plan['plan_hash']: raise ValueError('stale_plan_review')
        if review['decision'] == 'approved' and plan['blockers']: raise ValueError('blocked_plan_cannot_be_approved')
        if review['approval_kind'] == 'synthetic_fixture' and not review['reviewer'].startswith('SYNTHETIC TEST'):
            raise ValueError('synthetic_reviewer_label_required')
        def choose(group, key, default, edited):
            cid = review[key] or p[default]
            found = next((c for c in p[group] if c['candidate_id'] == cid), None)
            if not found: raise ValueError('unknown_candidate_id')
            text = review[edited] if review[edited] is not None else found['text']
            if not text.strip(): raise ValueError('empty_creative_selection')
            return dict(candidate_id=cid, text=text)
        outline = review['edited_outline'] if review['edited_outline'] is not None else p['outline']
        if not outline or not all(s.strip() for s in outline): raise ValueError('empty_approved_outline')
        result = dict(approval_id='CPA-'+uuid4().hex, plan=plan, **review,
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
        if a['approval_kind'] == 'synthetic_fixture' and 'synthetic_fixture' not in context['packet']['project']['source_route_context']:
            raise ValueError('synthetic_approval_requires_synthetic_packet')
        return a
