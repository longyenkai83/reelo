"""Local immutable campaign revisions and append-only human authority/execution memory.

Trusted operator API; never expose decision methods to model tools. Hashes are integrity,
not authentication. Campaign execution permission is NOT human creative/truth approval.
"""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from integrations.content_intelligence.adapter import encoded
from integrations.content_intelligence.contract import value_hash
from .models import JourneyPlan


class CampaignStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS plans (id TEXT PRIMARY KEY, campaign TEXT NOT NULL, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, campaign TEXT NOT NULL, body TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS plans_no_update BEFORE UPDATE ON plans BEGIN SELECT RAISE(ABORT,'immutable'); END;
            CREATE TRIGGER IF NOT EXISTS plans_no_delete BEFORE DELETE ON plans BEGIN SELECT RAISE(ABORT,'immutable'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append_only'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'append_only'); END;
            CREATE TRIGGER IF NOT EXISTS plans_no_replace BEFORE INSERT ON plans
              WHEN EXISTS(SELECT 1 FROM plans WHERE id=NEW.id) BEGIN SELECT RAISE(ABORT,'immutable'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_replace BEFORE INSERT ON events
              WHEN EXISTS(SELECT 1 FROM events WHERE id=NEW.id) BEGIN SELECT RAISE(ABORT,'append_only'); END;
            ''')

    def connect(self):
        return sqlite3.connect(self.path, timeout=30)

    def save(self, plan):
        plan = JourneyPlan.model_validate(plan.model_dump())
        digest = value_hash(plan.model_dump())
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            prior = db.execute('SELECT body FROM plans WHERE id=?', (digest,)).fetchone()
            if prior:
                if prior[0] != encoded(plan.model_dump()): raise ValueError('campaign_identity_collision')
            else:
                db.execute('INSERT INTO plans VALUES (?,?,?)', (digest, plan.request.campaign_id, encoded(plan.model_dump())))
        return digest

    def load(self, digest):
        with self.connect() as db:
            row = db.execute('SELECT body FROM plans WHERE id=?', (digest,)).fetchone()
            latest = db.execute('SELECT id FROM plans WHERE campaign=(SELECT campaign FROM plans WHERE id=?) ORDER BY rowid DESC LIMIT 1', (digest,)).fetchone()
        if not row or latest[0] != digest: raise ValueError('campaign_plan_not_current')
        body = json.loads(row[0])
        if value_hash(body) != digest: raise ValueError('campaign_integrity_failure')
        return JourneyPlan.model_validate(body)

    def events(self, campaign):
        with self.connect() as db:
            rows = db.execute('SELECT id,body FROM events WHERE campaign=? ORDER BY rowid', (campaign,)).fetchall()
        result = []
        previous = None
        for event_id, raw in rows:
            body = json.loads(raw)
            if body['previous'] != previous or value_hash(body) != event_id: raise ValueError('campaign_event_integrity_failure')
            result.append(dict(body, event_id=event_id)); previous = event_id
        return result

    def append(self, digest, kind, data):
        plan = self.load(digest)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT id FROM plans WHERE campaign=? ORDER BY rowid DESC LIMIT 1', (plan.request.campaign_id,)).fetchone()[0] != digest:
                raise ValueError('campaign_plan_not_current')
            last = db.execute('SELECT id FROM events WHERE campaign=? ORDER BY rowid DESC LIMIT 1', (plan.request.campaign_id,)).fetchone()
            existing = [json.loads(row[0]) for row in db.execute('SELECT body FROM events WHERE campaign=? ORDER BY rowid', (plan.request.campaign_id,))]
            if kind == 'EXECUTION_STARTED' and any(e['plan_hash'] == digest and e['kind'] == kind and
                    e['data']['slot_id'] == data['slot_id'] for e in existing):
                raise ValueError('slot_already_reserved_no_automatic_retry')
            if kind == 'PLANNER_STARTED':
                starts = [e for e in existing if e['plan_hash'] == digest and e['kind'] == kind and e['data']['slot_id'] == data['slot_id']]
                if starts and not any(e['kind'] == 'CREATIVE_PLAN' and e['data']['generation_id'] == starts[-1]['data']['generation_id'] for e in existing):
                    raise ValueError('planner_completion_requires_reconciliation')
            body = dict(plan_hash=digest, kind=kind, data=data, previous=last[0] if last else None,
                        time=datetime.now(timezone.utc).isoformat(), nonce=uuid4().hex)
            event_id = value_hash(body)
            db.execute('INSERT INTO events VALUES (?,?,?)', (event_id, plan.request.campaign_id, encoded(body)))
        return event_id

    def decide(self, digest, action, *, reviewer, human_attested, authority_ref, sample_hash=None, calibration=None):
        if human_attested is not True or not reviewer.strip() or not authority_ref.strip():
            raise ValueError('explicit_human_instruction_required')
        plan = self.load(digest)
        events = self.events(plan.request.campaign_id)
        if action not in ('AUTHORIZE_AUTOPILOT', 'APPROVE_SAMPLE', 'EXECUTE_REMAINDER', 'REVOKE'):
            raise ValueError('invalid_campaign_decision')
        if action == 'AUTHORIZE_AUTOPILOT' and plan.request.autonomy_mode != 'AUTOPILOT':
            raise ValueError('autonomy_mode_mismatch')
        if action == 'APPROVE_SAMPLE':
            if plan.request.autonomy_mode != 'GUIDED' or not sample_hash or not calibration:
                raise ValueError('guided_sample_and_calibration_required')
            if not any(e['plan_hash'] == digest and e['kind'] == 'RESULT' and
                       e['data'].get('draft_hash') == sample_hash and e['data'].get('status') == 'DRAFT_READY' for e in events):
                raise ValueError('actual_successful_sample_required')
        if action == 'EXECUTE_REMAINDER' and not any(e['plan_hash'] == digest and e['kind'] == 'APPROVE_SAMPLE' for e in events):
            raise ValueError('sample_approval_required')
        return self.append(digest, action, dict(reviewer=reviewer, actor_kind='human', human_attested=True,
            authority_ref=authority_ref, sample_hash=sample_hash, calibration=calibration,
            scope='this_campaign_only', publish_authorized=False))

    def authority(self, digest, *, sample=False):
        plan = self.load(digest)
        events = [e for e in self.events(plan.request.campaign_id) if e['plan_hash'] == digest]
        decisions = [e for e in events if e['kind'] in ('AUTHORIZE_AUTOPILOT', 'EXECUTE_REMAINDER', 'REVOKE')]
        if decisions and decisions[-1]['kind'] != 'REVOKE': return decisions[-1]
        # GUIDED sample still needs its genuine Creative Plan approval at the caller gate.
        if sample and plan.request.autonomy_mode == 'GUIDED' and not decisions:
            return None
        raise ValueError('explicit_campaign_execution_authority_required')

    def memory(self, digest):
        plan = self.load(digest)
        events = [e for e in self.events(plan.request.campaign_id) if e['plan_hash'] == digest]
        return dict(completed=[e['data'] for e in events if e['kind'] == 'RESULT' and e['data']['status'] == 'DRAFT_READY'],
                    failed_attempts=[e['data'] for e in events if e['kind'] == 'RESULT' and e['data']['status'] != 'DRAFT_READY'],
                    calibration=[e['data'] for e in events if e['kind'] == 'APPROVE_SAMPLE'],
                    audience_progress='UNKNOWN; assigned/completed stages are not measured audience change')
