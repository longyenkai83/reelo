# V2 Content Intelligence consumer

Read [V2-BOUNDARY.md](V2-BOUNDARY.md). Phase 9 is pending architect review. This is an
opt-in consumer in the existing Reelo creative engine; legacy batch input remains supported.

Requirements: Python 3.11+, `pydantic==2.13.3`, configured native Claude Code 2.1.270.
Do not use a PATH executable with a different version. No additional API key is introduced.

The Insight operator owns a local JSON config with four required keys:

```json
{
  "execution_workspace": "C:/work/reelo-implementation",
  "executable": "C:/exact/native-binary/claude.exe",
  "state_directory": "C:/Users/OWNER/AppData/Local/Reelo-V2",
  "read_files": ["C:/work/reelo-implementation/engine/cong-thuc-viral/cong-kiem-chat-luong.md"]
}
```

Optional operator limits: `timeout_seconds` (default 600, maximum 3600) and `max_budget_usd` (default 5).
These are execution limits, not quality thresholds. A timeout remains UNKNOWN, never auto-retried.

Replace examples with actual verified paths. `read_files` must include the creative rules,
format reference, hook/title sources and selected brand voice/Story/RAW/WIKI/index files
needed for the requested content. Paths are exact files, not broad read/write grants. Missing
references must not be invented. Keep private config and state outside Git. Operational
assets can remain on the owner's Drive while implementation and SQLite stay separate.

From Insight:

```text
python -m tiktok_insight_miner send-content-packet PACKET.json
  --verified-insights VERIFIED.json --content-tree TREE.json
  --selection SELECTED.json --reviews REVIEWS.json --selection-ledger LEDGER.json
  --reelo-config LOCAL-CONFIG.json --request-id stable-request-id
```

Use one command line in the shell. Reuse request-id for a transport retry. To request a new
creative generation, supply a new request-id plus `--parent-generation-id GEN-...`.
Do not rerun an UNKNOWN execution; reconcile its recorded host events/task first.
The existing packet-preview UI enables Send to Reelo when the operator sets `REELO_CONFIG`.
It does not expose a filesystem/executable selector to web users.

`adapter.py`: validation, immutable intake, atomic dispatch reservation and execution status.
`contract.py`: bounded port from Insight ca09ae4d; `contract-provenance.json` pins source hashes.
`host.py`: explicit executable/profile, existing Workflow, task/artifact correlation.
`workflow-v2.js`: V2 section included verbatim in `.claude/workflows/batch-content.js`.
`notion_handoff.py`: Main-only outbox, prepare → current recheck/claim → connector create →
connector fetch → acknowledge. Fetch database schema first; use its data source ID and actual
title/status/source property names. Draft permission does not imply human content approval.
Query `IntakeStore.status(generation_id)` for the Notion receipt projection; historical
generation output is not overwritten by external status updates.

Tests: `python -m pytest tests -q` (Node required for the offline Workflow harness).
Live synthetic host test lives in the Insight repo and is opt-in, never an ordinary pytest call.
It substitutes creative responses in an isolated copy only; production has no synthetic bypass.

Unsigned content hashes protect integrity, not producer authentication. The consumer is called
by the trusted local producer service, which supplies current-ledger authorization. Exposing
this API to untrusted remote callers would require a reviewed authentication design.
