# V2 Content Intelligence consumer

RP3.C knowledge authority: [Writing Core, jobs and mechanisms](../../engine/writing-knowledge/CORE.md)
and [asset dispositions](../../engine/writing-knowledge/ASSET-MAP.md).
Knowledge model only: existing runtime psychology/title guards and read_files
remain unchanged. Do not treat optional reference as permission to bypass them.

RP3.B creator isolation: [creator boundary and configuration](CREATOR-BOUNDARY-B1.md).

RP3.A maintenance authority: [canonical semantics and parity](SEMANTICS-A1.md).
Read before changing mode, V2 title or Critic severity/repair meanings. This does
not reopen C5 or authorize creative execution.

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

## C5.3 — redundant terminal-output Read denial

The main/model must not read task output; Python is the authoritative artifact reader.
The host allowlist and permission review remain unchanged. A denial becomes a non-blocking
permission_notes audit entry ONLY after a correlated completed notification, independent
Python artifact read/structured validation, exact receipt/context/generation/parent identity,
terminal execution status and unchanged creative assets have passed.

Each denial must be Read of the exact output_file string returned by that terminal event.
Its tool_use_id must identify one actual Read invocation in the stream after completion,
with matching input, before the denial report. A final aggregate permission_denials list
alone cannot prove timing. Any unexpected denial, missing/duplicate tool call, earlier Read,
other target/tool, missing terminal, invalid artifact or identity mismatch still blocks.
No path aliases, broader temporary-directory read grant, ignored arbitrary denials or retry.
The original native events remain intact; permission-review.json and host.permission_notes
record the bounded classification. Main prose/Read never authorizes completion.
## C5.4 — bounded stage-wise execution (owner-authorized architecture decision)

Phase 9 orchestration now lives in `stages.py`: WRITER -> CRITIC1 -> optional REWRITE ->
CRITIC2. Each host invocation executes exactly one creative agent with the existing Writer,
Critic and rewrite craft. Native print mode no longer owns the full multi-stage chain.
No generic orchestrator, queue or resume mechanism is introduced. Legacy workflow unchanged.

Every call receives identical canonical A/B/C and execution identity, the same read-only asset
manifest, and only its required previous draft/review. No accumulated host logs or stage history
are placed in the creative context. The model returns stage output, not execution status.
Python verifies terminal correlation, stage identity/input hash and strict output schema before
C5.3 permission-denial classification. It then persists raw output, normalized output, artifact
hashes, packet/revision/ingestion/generation lineage, parent stage and host task/session metadata.
`completed.json` is atomically written/flushed before the next stage. Predecessor bytes/hashes
are rechecked before each next call and before final PASS; raw Critic output remains separate.

States: WRITER_COMPLETED, CRITIC1_COMPLETED, REWRITE_COMPLETED, CRITIC2_COMPLETED. A stopped,
timed-out, malformed or mismatched stage stops the generation with UNKNOWN and a stage-specific
*_UNKNOWN record. Verified predecessors remain authoritative in their files and final result.
Abrupt process loss can leave RUNNING/progress files; it never grants automatic retry/resume.
No previous UNKNOWN generation is relabeled by a new controlled acceptance.

PASS still requires strict truth/intent/scope/source checks, all eight title checks and zero
blockers. Valid reported PASS with blockers becomes REVISE; notes alone do not trigger rewrite.
Malformed transport now stops immediately rather than launching another model to repair it.
There is at most one rewrite. Final REVISE is CRITIC_FAILED. DRAFT_READY requires all completed
stage identity/hash checks and final applicable Critic PASS. Approval stays PENDING, no publish.
Notion is not invoked by this state machine.

Host timeout/budget configuration now bounds EACH stage independently: existing defaults 600s
and USD5, at most four stages (up to USD20 configured aggregate ceiling). This is a bound, not
measured billing. The controlled C5.4 run retains the prior explicit 900s/medium/USD5 settings
per invocation. No global settings or tool grants change; no retry after the native wait ceiling.
Private drafts/logs remain machine-local, outside Git. Technical PASS does not accept C5.

## C5.5 — typed Critic findings (V2 only)

Critic now requires `findings`: category, severity (`advisory`/`blocking`), message,
`evidence_refs` (packet evidence IDs; [] when not applicable) and `affected_text` (draft
passage when practical, otherwise empty). Categories are the nine hard boundaries below,
plus creative_quality, voice, format and other. Unknown/malformed categories, missing
findings, blank messages and unknown evidence references fail closed.

Python always turns unsupported_identity, scope_broadening, unsupported_causality,
quote_integrity, creator_truth_drift, external_fact_unsupported, market_validation_inflation,
purchase_validation_inflation and contradiction_loss into blocking findings and REVISE.
This holds even if raw severity is advisory, reported verdict is PASS, all booleans are true
and blocking_issues is empty. Raw output remains untouched for audit. Normalized findings
retain reported_severity and effective severity; normalized blocking_issues drive the
existing state machine. Other categories follow declared severity/current rubric.

Notes are advisory only. Critic must put each detected unresolved hard-boundary defect into
a typed finding rather than hiding it in notes or a style category. In particular anonymous
comment counts do not establish people; separate sources do not establish shared context or
why experiences differ; hedging does not supply causal evidence. Creative expression stays
allowed. No second Critic, semantic regex, extra LLM layer or generic quality framework.

Deterministic tests prove handling of supplied typed findings; they do not prove automatic
semantic detection. If the model omits/mislabels a defect while emitting a structurally valid
empty findings list, code cannot discover that from free-form notes without semantic analysis.
Human quality review remains necessary. C5.4 host lifecycle/permission/identity/Q1 remain closed;
at most one rewrite and the same final truth/title checks remain. No legacy critic change.

## C5.6 — owner-confirmed V2 voice / title / tone

Owner quality review of C5.5 FAILED despite its technical PASS. For V2, keep the reader
("ban/bạn") central; useful real creator stories/observations may appear, then return focus
to the reader. An explicitly selected personal-story-first format may legitimately foreground
the creator. This is semantic judgment, never pronoun counts or a mechanical ratio.

Titles need immediate semantic meaning, direct selected-angle relevance, natural Vietnamese,
reader usefulness and meaningful curiosity. No awkward poetic opposition or cleverness for
its own sake. The owner-rejected C5.5 title must not be reused or merely paraphrased. The
existing title system/eight checks remain; no broad legacy title change.

Invite reflection through questions, suggestions and tentative frames. Do not lecture, diagnose
reader motives/problems without evidence or present a proposed framework as universally true.
Creator experience is one lens, not imposed authority. Reader address/questions never waive truth.

Three required V2 Critic booleans: title_meaning_clear, reader_centered_pov,
non_prescriptive_tone. A false value deterministically blocks/REVISE; missing/non-boolean values
fail closed. Critic must describe failures as blocking creative_quality/voice findings; truth
violations retain their existing hard category. Raw review, one Critic, maximum one rewrite,
host lifecycle, permission, Q1, packet/provenance and all C5.5 hard categories are unchanged.
Semantic detection remains fallible; technical PASS is not owner quality acceptance.


## Integrated Creative Planner — one explicit human gate (owner scope after C5.7)

Sending a packet without `--approval-id` now runs only CREATIVE_PLAN and returns
PLAN_PENDING_APPROVAL (or PLAN_BLOCKED/UNKNOWN). It never writes an article.
The internal PROPOSED plan does not modify the Phase8 packet or select another angle.
Story/Knowledge matches use the explicit read-only manifest; unmatched necessary assets
must be reported. Candidate counts use existing craft defaults, not fixed product constants.

Minimal operator surface in the Insight CLI (same current input-ledger flags as before):

```text
python -m tiktok_insight_miner send-content-packet packet.json [current input flags] --reelo-config config.json --request-id plan-1
python -m tiktok_insight_miner review-reelo-plan --reelo-config config.json --plan-id CP-... > plan-review.json
python -m tiktok_insight_miner review-reelo-plan --reelo-config config.json --plan-id CP-... --review-file human-decision.json
python -m tiktok_insight_miner send-content-packet packet.json [current input flags] --reelo-config config.json --request-id write-1 --parent-generation-id GEN-... --approval-id CPA-...
```

The operator sees the angle reference, source matches, psychology, format/treatment,
hook/title candidates, recommended choices and outline in one local JSON artifact.
Submit ONE decision, not separate approvals for each field:

```json
{"decision":"approved","reviewer":"actual operator name","human_attested":true,
 "expected_plan_hash":"hash from inspected plan","hook_id":"candidate ID",
 "title_id":"candidate ID","edited_hook":null,"edited_title":null,"edited_outline":null}
```

`rejected`/`deferred` also supported. Omitted choice fields select the recommendations.
Edits are persisted in the approved artifact; they remain subject to truth/semantic Critic.
A later review supersedes earlier approval; a new plan revision or changed manifest/source
invalidates stale approval. Re-read current upstream ledgers at Writer dispatch as before.
Approval is local operator attestation, not authenticated multiuser authorization; hashes
bind versions, not identity. Do not let model output invoke the review API.

Synthetic technical tests must label reviewer `SYNTHETIC TEST ...` and set
`approval_kind: synthetic_fixture`; consumer only accepts that kind for synthetic packets.
This never changes final `human_approval=PENDING`, Notion state or publication state.

Writer/Critic/Rewrite receive the identical approved plan. Writer executes selected title,
hook, outline, psychology, treatment and sources, while retaining prose/voice craft.
Critic checks plan fidelity and existing truth/quality gates; no second Critic added.
Missing/false plan-fidelity confirmation blocks; selected title/format mismatch also blocks
in code. Other semantic judgments are fallible model review, not regex truth proof.


## C5.9 ? findings semantics and owner review

Canonical C5.8 names the integrated Planner implementation whose local source report
was named REPORT-C5.6.md. C5.9 does not redesign it.

Internal plans separate blocking_issues, limitations, advisories and publication_requirements.
Historical issues remain fail-closed until explicitly reviewed into a NEW derived projection.
Outline truth drift is blocking (outline_blocking_issues); hiding/contradicting a limitation
is a truth defect, not an advisory. Packet external requirements are copied into review_view
by code, cannot be cleared by model omission, and never become publication permission.
ready_for_owner_review is distinct from ready_to_write (requires actual current human approval).
ready_to_publish remains false: this internal plan API cannot authorize publication, including
when all plan blockers are zero. No new publisher or research workflow has been introduced.

Each candidate has computed eligibility (selectable/blocked with reasons). Semantic source
review may add blocking_reasons even when all model booleans are true. Blocked alternatives
do not block a safe recommendation; blocked recommendations/no safe alternatives block the plan.
The human review endpoint rejects selection of a blocked candidate, including text-edit bypass.
A rejected/deferred decision remains possible. Human edits to otherwise safe options remain
explicit, immutable and subject to the existing downstream truth Critic; they are not machine
proof of truth. No model approval or automatic human decision is permitted.

Story match_type DIRECT requires source-supported same experience; ADJACENT requires precise
allowed_use and cannot use_as_same_situation. Exact local support_quote must exist in the source.
No story match is valid (NONE); an illustrative_ai scene is ILLUSTRATIVE_AI with required disclosure.
Support span/hash checks prove source wording/origin, not semantic entailment: the Planner,
source-reviewing operator and downstream Critic must assess meaning. No pronoun/keyword regex
can prove identity, causality or relevance. Shared reports redact private support passages.

Writer/Critic receive the same approved snapshot including every limitation, advisory and
publication requirement. C5.9 itself runs only offline validation and tests: no Planner rerun,
Writer, Critic, rewrite, Notion or publication. Owner reviews ONE gate artifact before any drafting.

## C5.10 — owner edit approval and output modes

Explicit EDIT_AND_APPROVE is stored as owner_decision alongside normalized decision=approved
for existing orchestration. selected_mode (REEL/SHORT_ARTICLE/LONG_ARTICLE), optional knowledge
policy, limitations and publication requirements travel with the immutable approval snapshot.
Original plan/revision/hash remain. human kind records actual owner authorization even for a
synthetic packet; this is neither model approval nor final article approval.

REEL means spoken Vietnamese with breath and conversational rhythm, never a short article read
aloud. SHORT_ARTICLE/LONG_ARTICLE are written content. Writer/Critic retain the approved mode.
Title/opening must be immediately clear; no deliberate obscurity or cleverness before meaning.
Exact owner edits override candidate wording. Optional knowledge may be omitted when unhelpful.

Creative approval does not clear UNKNOWN execution history. The unchanged reserve guard raises
reconcile_previous_execution_first. C5.10 does not reconcile, rewrite history or use a new intake
database to bypass the guard. Host lifecycle/permissions and truth categories remain unchanged.

## C5.11 - append-only audited UNKNOWN reconciliation

reconciliation.append is a trusted local operator API, never a model approval or generic
ignore-UNKNOWN switch. Only the Planner psychology whitespace false negative is eligible:
replay exact correlated native terminal output, strict identity/context/artifact checks,
original single failure reason, current fixed validator, manifest and current approval of its
explicit C5.9 derived projection. Governance/selection are reloaded by the application authorizer.
Missing assets fail closed; no fallback copies or alternate sources.

Original execution/result/events stay UNKNOWN and unchanged. Separate execution_reconciliation
SQLite records bind resolver/time/version/commit, evidence paths/hashes and plan/approval/packet.
SQL triggers reject UPDATE/DELETE. Hashes bind contents, not multiuser authentication; local
operator/store remains trusted. Reserve/dispatch require explicit reconciliation_id + approval_id.
UNKNOWN without reconciliation blocks. A matching record must pass every evidence/current-state
check again at reservation. RUNNING/RECEIVED never unlock. No auto-retry, terminal overwrite,
new intake database or Planner rerun. Existing Writer/Critic/max-one-rewrite orchestration,
host permissions, truth guards and legacy behavior remain unchanged.

## C5.15 ? reader value and narrative payoff

New internal PlanProposal requires reader_value aligned one-to-one with outline,
narrative_payoffs for selected Story source/section, reader_value_clear and
narrative_payoff_clear. Empty/missing section values fail validation. A used Story
without one explicit job/setup/turn/meaning/reader payoff blocks plan approval. NONE
uses an empty payoff list and may pass. Semantic booleans false block; these checks
do not prove usefulness/entailment or fabricate a source realization. Owner review
is still required. No private creator-specific rule is encoded in core.

Historical plan bodies/approvals remain stored unchanged; they are not automatically
upgraded to satisfy the expanded internal quality contract. A corrected upstream
packet has a different context/angle and cannot reuse their approval. Portable
Phase8 schema, truth categories, stage lifecycle and permissions are unchanged.
