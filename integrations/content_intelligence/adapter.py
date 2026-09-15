"""Deterministic, local pre-host intake. No models, network, or producer imports."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone
from typing import Literal

from pydantic import Field
from .contract import ContentIntelligencePacket, StrictModel, value_hash, validate_revision


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class Receipt(StrictModel):
    ingestion_id: str
    packet_id: str
    packet_revision: int
    packet_hash: str
    context_hash: str


class ContentIntelligenceContext(StrictModel):
    schema_version: Literal['reelo.execution-context.1'] = 'reelo.execution-context.1'
    packet: ContentIntelligencePacket


class ExecutionResult(StrictModel):
    receipt: Receipt
    generation_id: str
    parent_generation_id: str | None
    status: Literal['RECEIVED', 'RUNNING', 'DRAFT_READY', 'CRITIC_FAILED',
                    'BLOCKED_PENDING_RESEARCH', 'HOST_FAILED', 'UNKNOWN', 'SUPERSEDED']
    critic_status: Literal['NOT_RUN', 'PASS', 'FAIL'] = 'NOT_RUN'
    human_approval: Literal['PENDING'] = 'PENDING'
    notion_status: Literal['NOT_SENT', 'DRAFT'] = 'NOT_SENT'
    notion_page_url: str | None = None
    published: Literal[False] = False
    validation_issues: list[str] = Field(default_factory=list)
    host: dict = Field(default_factory=dict)
    artifacts: list[dict] = Field(default_factory=list)


class IntakeStore:
    """Single-machine SQLite authority. Use a local disk, never a synced/remote DB.

    BEGIN IMMEDIATE serializes dispatch reservation. An interrupted RUNNING execution
    is never silently relaunched; reconcile or explicitly create a new generation.
    """
    def __init__(self, path: Path):
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS intake (
                    packet_id TEXT PRIMARY KEY, ingestion_id TEXT UNIQUE NOT NULL,
                    packet TEXT NOT NULL, context TEXT NOT NULL, receipt TEXT NOT NULL,
                    supersedes TEXT UNIQUE, created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS execution (
                    generation_id TEXT PRIMARY KEY, packet_id TEXT NOT NULL,
                    request_id TEXT NOT NULL, parent_id TEXT,
                    result TEXT NOT NULL, UNIQUE(packet_id, request_id));
            ''')

    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        return db

    def intake(self, raw: dict) -> Receipt:
        packet = ContentIntelligencePacket.model_validate(raw)
        data = packet.model_dump(mode='json')
        # No semantic reassembly: preserve the entire canonical A/B/C snapshot.
        context = ContentIntelligenceContext(packet=packet).model_dump(mode='json')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT * FROM intake WHERE packet_id=?', (packet.packet_id,)).fetchone()
            if old:
                if old['packet'] != encoded(data):
                    raise ValueError('packet_identity_collision')
                return Receipt.model_validate_json(old['receipt'])
            if packet.supersedes_packet_id:
                previous = db.execute('SELECT packet FROM intake WHERE packet_id=?',
                                      (packet.supersedes_packet_id,)).fetchone()
                if not previous:
                    raise ValueError('missing_previous_packet')
                validate_revision(packet, ContentIntelligencePacket.model_validate_json(previous['packet']))
                if db.execute('SELECT 1 FROM intake WHERE supersedes=?',
                              (packet.supersedes_packet_id,)).fetchone():
                    raise ValueError('packet_revision_fork')
            receipt = Receipt(ingestion_id='ING-'+uuid4().hex, packet_id=packet.packet_id,
                              packet_revision=packet.packet_revision,
                              packet_hash=packet.packet_id.removeprefix('CIP-'),
                              context_hash=value_hash(context))
            db.execute('INSERT INTO intake VALUES (?,?,?,?,?,?,?)',
                       (packet.packet_id, receipt.ingestion_id, encoded(data), encoded(context),
                        receipt.model_dump_json(), packet.supersedes_packet_id,
                        datetime.now(timezone.utc).isoformat()))
            return receipt

    def context(self, receipt: Receipt) -> dict:
        with self.connect() as db:
            row = db.execute('SELECT * FROM intake WHERE packet_id=?', (receipt.packet_id,)).fetchone()
        if not row or Receipt.model_validate_json(row['receipt']) != receipt:
            raise ValueError('unknown_receipt')
        context = json.loads(row['context'])
        if value_hash(context) != receipt.context_hash:
            raise ValueError('context_integrity_failure')
        packet = ContentIntelligenceContext.model_validate(context).packet
        if packet.packet_id != receipt.packet_id:
            raise ValueError('receipt_packet_mismatch')
        return context

    def reserve(self, receipt: Receipt, request_id: str, parent_id: str | None = None):
        if not request_id or len(request_id) > 120:
            raise ValueError('invalid_request_id')
        self.context(receipt)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT 1 FROM intake WHERE supersedes=?', (receipt.packet_id,)).fetchone():
                raise ValueError('superseded_packet')
            old = db.execute('SELECT result FROM execution WHERE packet_id=? AND request_id=?',
                             (receipt.packet_id, request_id)).fetchone()
            if old:
                result = ExecutionResult.model_validate_json(old['result'])
                if result.parent_generation_id != parent_id:
                    raise ValueError('request_id_reused_with_different_parent')
                return result, False
            previous = db.execute('SELECT * FROM execution WHERE packet_id=? ORDER BY rowid DESC LIMIT 1',
                                  (receipt.packet_id,)).fetchone()
            if previous:
                if parent_id != previous['generation_id']:
                    raise ValueError('explicit_parent_generation_required')
                if json.loads(previous['result'])['status'] in ('RUNNING', 'RECEIVED', 'UNKNOWN'):
                    raise ValueError('reconcile_previous_execution_first')
            elif parent_id:
                raise ValueError('unknown_parent_generation')
            result = ExecutionResult(receipt=receipt, generation_id='GEN-'+uuid4().hex,
                                     parent_generation_id=parent_id, status='RUNNING')
            db.execute('INSERT INTO execution VALUES (?,?,?,?,?)',
                       (result.generation_id, receipt.packet_id, request_id, parent_id, result.model_dump_json()))
            return result, True

    def finish(self, result: ExecutionResult):
        result = ExecutionResult.model_validate(result.model_dump())
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT result FROM execution WHERE generation_id=?',
                             (result.generation_id,)).fetchone()
            if not row:
                raise ValueError('unknown_generation')
            old = ExecutionResult.model_validate_json(row['result'])
            if old.receipt != result.receipt or old.parent_generation_id != result.parent_generation_id:
                raise ValueError('execution_lineage_mismatch')
            if old.status != 'RUNNING':
                if old != result:
                    raise ValueError('immutable_terminal_execution')
                return
            if result.status in ('RUNNING', 'RECEIVED'):
                raise ValueError('terminal_result_required')
            if result.status == 'DRAFT_READY' and (result.critic_status != 'PASS' or not result.artifacts):
                raise ValueError('draft_requires_critic_and_artifact')
            db.execute('UPDATE execution SET result=? WHERE generation_id=?',
                       (result.model_dump_json(), result.generation_id))

    def status(self, generation_id: str) -> ExecutionResult:
        """Project external draft receipt onto immutable generation history for the UI."""
        with self.connect() as db:
            row = db.execute('SELECT result FROM execution WHERE generation_id=?', (generation_id,)).fetchone()
            if not row:
                raise ValueError('unknown_generation')
            result = ExecutionResult.model_validate_json(row['result'])
            if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='notion_outbox'").fetchone():
                receipt = db.execute("SELECT page_url FROM notion_outbox WHERE generation_id=? AND status='DRAFT' ORDER BY rowid DESC LIMIT 1",
                                     (generation_id,)).fetchone()
                if receipt:
                    result.notion_status = 'DRAFT'
                    result.notion_page_url = receipt['page_url']
            return result


def dispatch(store: IntakeStore, raw: dict, *, request_id: str, authorize_current,
             launch, parent_id: str | None = None) -> ExecutionResult:
    """Application boundary. authorize_current must reload both current owner ledgers.

    It is a trusted application callback, never a packet flag/model declaration.
    No default authorizer and no offline-validation fallback are provided.
    """
    packet = ContentIntelligencePacket.model_validate(raw)
    authorize_current(packet.model_dump(mode='json'))
    receipt = store.intake(packet.model_dump(mode='json'))
    context = store.context(receipt)
    # Recheck after I/O, immediately before the atomic reservation and launch.
    authorize_current(context['packet'])
    result, fresh = store.reserve(receipt, request_id, parent_id)
    if not fresh:
        return store.status(result.generation_id)
    try:
        terminal = launch(result.model_copy(deep=True), context)
        if not isinstance(terminal, ExecutionResult):
            raise ValueError('typed_terminal_result_required')
        store.finish(terminal)
        return terminal
    except Exception as exc:
        # Launch may have succeeded before losing its response. Never auto-retry.
        import re
        result.status = 'UNKNOWN'
        result.validation_issues = ['execution_completion_unconfirmed']
        if re.fullmatch(r'[a-z][a-z0-9_]+', str(exc)):
            result.validation_issues.append(str(exc))
        store.finish(result)
        return result
