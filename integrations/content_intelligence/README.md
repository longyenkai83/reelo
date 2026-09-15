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
Optional `effort_level` (`low`, `medium`, `high`) overrides reasoning effort for this
one host session through native settings. Omit it to keep the inherited user setting.
It never edits user/project settings, changes model, removes guards or grants tools.
The result records the requested effort (not a measured thinking-token guarantee).
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


C5.1 bounded quality patch (owner-authorized scope, not a new phase): V2 no longer
passes the first legacy TRUC_POOL entry as a preferred axis. Zone B determines the
selected direction; editorial history, psychology craft and story treatment must not
replace it. Unspecified presentation remains a compatible Zone C creative choice.
Legacy pool allocation and prompts are unchanged outside the V2 override.

For a controlled quality run, supply concrete read-only knowledge documents, not just
a WIKI index. Choose the relevant format/craft/voice/Story assets explicitly. V2 reads
needed sections without recursively restarting legacy source discovery; missing evidence
still blocks unsupported claims. Each independent Critic verifies its own sources.
The draft review header records asset paths/sections/roles and omissions without dumping
private passages. This is a prompt-level operational bound, not a hard read-count quota
or a guarantee of semantic correctness. Do not lower truth checks to meet a timeout.

Quality results and private drafts remain local; refer to the C5.1 owner review report.
No acceptance follows from offline tests alone. UNKNOWN remains UNKNOWN and must not be
blindly relaunched; a separately identified synthetic controlled test is not a recovery
or completion of the earlier execution. No merge, Source Router or Unified Web work.

The draft evidence-ID gate includes both verified_insight.evidence_refs and its validated
contradictions[].counter_ref. Counter-evidence must survive into the independent Critic;
unknown IDs and invented counter quotes still fail. This changes no source span/hash or
customer truth. The C5.1 live medium-effort draft exposed this false rejection before Critic.

## C5.2 — bounded lifecycle and Critic semantics

V2 Critic transport uses PASS / REVISE, blocking_issues and notes. Code retains the raw
review and computes a terminal verdict: PASS requires zero blockers, strict true checks,
eight true title criteria and a well-formed review. A reported PASS with findings becomes
REVISE without losing them. Informational notes alone do not trigger a rewrite. Legacy
issues, malformed fields or missing confirmation fail closed; at most one rewrite remains.
The existing execution critic_status PASS/FAIL/NOT_RUN and Phase 8 packet schema are unchanged.

Creator truth, context/scope and independent source verification have explicit V2 checks.
External knowledge does not establish first-person learning/experience; customer speech and
illustrations do not become creator history. Rent does not establish business premises,
and distinct source comments do not establish a shared situation. Translations must be
identified rather than passed off as exact quotes. These are fallible semantic checks,
not regex-based proof or permission to invent facts for better prose.

A correlated native stopped notification returns workflow_stopped_completion_unknown;
UNKNOWN reservation and no-retry behavior are retained even if a partial output file exists
or the main CLI says success. Completed task + valid structured correlated result remains
mandatory. Public stream lifecycle metadata and a native --debug-file are saved locally
for diagnosis, never used as an undocumented alternate completion API. Debug logs may contain
private material: keep outside Git and do not include raw logs in owner/architect reports.
Timeout/default effort/budget are not raised by this patch. No recovery loop is introduced.
