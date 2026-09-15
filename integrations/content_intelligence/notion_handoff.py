"""Main-owned Notion draft outbox. Writer/Workflow never gets a Notion connector.

The connector owner supplies schema-verified property names and an owner-authorized
destination. Claim once, create once, fetch to verify, then acknowledge the URL.
Lost connector response stays DISPATCHING until reconciliation; never auto-duplicate.
"""
import json
from urllib.parse import urlparse

from .adapter import ExecutionResult, encoded
from .contract import value_hash


def prepare(store, generation_id, *, destination, title_property, status_property,
            draft_status, source_property, authorize_current):
    if not all(isinstance(x, str) and x.strip() for x in
               (destination, title_property, status_property, draft_status, source_property)):
        raise ValueError('verified_notion_destination_schema_required')
    if len({title_property, status_property, source_property}) != 3:
        raise ValueError('distinct_notion_properties_required')
    with store.connect() as db:
        row = db.execute('SELECT result FROM execution WHERE generation_id=?', (generation_id,)).fetchone()
    if not row:
        raise ValueError('unknown_generation')
    result = ExecutionResult.model_validate_json(row['result'])
    if result.status != 'DRAFT_READY' or result.critic_status != 'PASS':
        raise ValueError('critic_pass_draft_required')
    context = store.context(result.receipt)
    authorize_current(context['packet'])
    artifact = result.artifacts[-1]
    if value_hash(artifact['content']) != artifact.get('content_hash'):
        raise ValueError('draft_hash_mismatch')
    handoff_id = 'NH-'+value_hash([generation_id, destination])
    # Existing database columns only; no new schema, publication flag, or fake approval.
    payload = {'parent': {'data_source_id': destination}, 'pages': [{
        'properties': {title_property: artifact['writer']['title'], status_property: draft_status,
                       source_property: handoff_id},
        'content': 'DRAFT — HUMAN APPROVAL PENDING — NOT PUBLISHED\n\n'+artifact['content']+
                   '\n\nPacket: '+result.receipt.packet_id+'\n\nGeneration: '+generation_id+
                   '\n\nHandoff: '+handoff_id,
    }]}
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM intake WHERE supersedes=?', (result.receipt.packet_id,)).fetchone():
            raise ValueError('superseded_packet')
        latest = db.execute('SELECT generation_id FROM execution WHERE packet_id=? ORDER BY rowid DESC LIMIT 1',
                            (result.receipt.packet_id,)).fetchone()
        if latest['generation_id'] != generation_id:
            raise ValueError('superseded_generation')
        db.execute('CREATE TABLE IF NOT EXISTS notion_outbox '
                   '(handoff_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL, page_url TEXT, draft_status TEXT NOT NULL, generation_id TEXT NOT NULL)')
        old = db.execute('SELECT * FROM notion_outbox WHERE handoff_id=?', (handoff_id,)).fetchone()
        if old and old['payload'] != encoded(payload):
            raise ValueError('immutable_notion_handoff_conflict')
        if not old:
            db.execute('INSERT INTO notion_outbox VALUES (?,?,?,NULL,?,?)', (handoff_id, encoded(payload), 'PREPARED', draft_status, generation_id))
    return handoff_id, payload


def claim(store, handoff_id, *, authorize_current):
    with store.connect() as db:
        row = db.execute('SELECT e.result FROM execution e JOIN notion_outbox n ON e.generation_id=n.generation_id WHERE n.handoff_id=?',
                         (handoff_id,)).fetchone()
    if not row:
        raise ValueError('unknown_handoff')
    result = ExecutionResult.model_validate_json(row['result'])
    authorize_current(store.context(result.receipt)['packet'])
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM intake WHERE supersedes=?', (result.receipt.packet_id,)).fetchone():
            raise ValueError('superseded_packet')
        latest = db.execute('SELECT generation_id FROM execution WHERE packet_id=? ORDER BY rowid DESC LIMIT 1',
                            (result.receipt.packet_id,)).fetchone()
        if latest['generation_id'] != result.generation_id:
            raise ValueError('superseded_generation')
        row = db.execute('SELECT * FROM notion_outbox WHERE handoff_id=?', (handoff_id,)).fetchone()
        if not row or row['status'] != 'PREPARED':
            raise ValueError('handoff_already_claimed_or_unknown_reconcile_do_not_resend')
        db.execute('UPDATE notion_outbox SET status=? WHERE handoff_id=?', ('DISPATCHING', handoff_id))
        return json.loads(row['payload'])


def acknowledge(store, handoff_id, page_url, *, verified_source_id, verified_draft_status, verified_destination):
    """Call only after the Main connector fetched the created page and checked properties."""
    url = urlparse(page_url)
    if url.scheme != 'https' or url.hostname not in ('www.notion.so', 'notion.so', 'app.notion.com', 'www.notion.com'):
        raise ValueError('notion_page_url_required')
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row = db.execute('SELECT * FROM notion_outbox WHERE handoff_id=?', (handoff_id,)).fetchone()
        if not row or row['status'] not in ('DISPATCHING', 'DRAFT'):
            raise ValueError('handoff_not_dispatched')
        payload = json.loads(row['payload'])
        if (verified_source_id != handoff_id or verified_draft_status != row['draft_status']
                or verified_destination != payload['parent']['data_source_id']):
            raise ValueError('notion_draft_verification_failed')
        if row['status'] == 'DRAFT' and row['page_url'] != page_url:
            raise ValueError('notion_receipt_conflict')
        db.execute('UPDATE notion_outbox SET status=?,page_url=? WHERE handoff_id=?', ('DRAFT', page_url, handoff_id))
    return {'handoff_id': handoff_id, 'status': 'DRAFT', 'page_url': page_url,
            'human_approval': 'PENDING', 'published': False}
