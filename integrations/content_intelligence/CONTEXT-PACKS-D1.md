# D1 — Stage context packs / knowledge projection

Runtime knowledge integration after C1. Phase 8 CIP, Zone A/B, nine hard
categories, source/currentness/approval guards and one-rewrite lifecycle remain.
No creative acceptance is implied. C5 FROZEN; Phase 9 NOT ACCEPTED.

## Assembly and authority

`context_packs.py` builds a fresh pack inside `NativeHost.invoke_stage` before
each native launch. NativeHost pins canonical CORE, recipes and A1 semantics in
the plan asset manifest alongside configured `read_files`. Existing before/after
hash checks remain. A historical approval lacking these assets is stale, never
silently upgraded. The host requires a D1-enabled workflow; no deployment to an
older J: workspace is performed automatically.

Original stage inputs, immutable CIP and full approval are retained locally as
execution authority. The creative agent receives a projection. Writer/Rewrite
do not get unselected hook/title candidates or the full approval asset manifest.
Critic gets candidate tables because the existing eight title checks require
them. Projection never changes the stored plan, selected wording or input hash.
The exact payload hash and workflow script hash are recorded in host evidence.

| Stage | Knowledge | Creator/source support | References |
|---|---|---|---|
| CREATIVE_PLAN | Six semantic lenses, prewriting, nine recipes, hook/title mechanism, title-eight compatibility | Configured identity/voice, recent editorial table entries; Story/Knowledge metadata by default; exact candidate sections only when explicitly selected | Current psychology library required for compatibility; others selected by task policy |
| WRITER | Core, selected recipe/job, selected mode, hook/title mechanism | Voice, approved Story/Knowledge sections, approved outline/hook/title/CTA, limitations | No candidate-generation library by default; explicit craft reference only |
| CRITIC1/2 | Core, selected recipe/job/mode, title-eight and repair-layer contract | Fresh independent loads of selected support/voice plus current draft/approved plan | Psychology and configured title-frame library for required membership checks; other defect references explicit |
| REWRITE | Core, approved recipe/mode, repair-layer contract | Current draft, typed findings, approved sources/voice | No alternative recipe/angle/psychology or Planner candidates; prose repair only |

Customer assertion support is the immutable packet, including contradictions;
creative-source files never replace it. Writer self-report cannot satisfy Critic
source verification. Each Critic assembly reads and hash-checks source bytes anew.
It must then independently evaluate those excerpts. Hash checks cannot evaluate
semantic truth, voice quality or the adequacy of a chosen excerpt.

## Job / recipe identity

New Planner results must contain `content_job` and `recipe_id`. Jobs come from
C1 `recipes.json`; deterministic ID is `c1:<JOB>`, e.g. `c1:TEACH`. Invalid pairs
fail validation. They are in the proposal and therefore the plan hash. New
revision/job/recipe invalidates old approval through existing currentness.
Historical proposals may omit both fields and remain readable/valid history.
D1 execution refuses to invent a recipe for them. A new reviewed plan is needed;
no SQL/data migration or automatic reapproval is introduced.

## Stable asset identity and operator selection

`asset_id` is `asset-` plus the first 24 hex characters of SHA256 of the exact
normalized manifest path. Content version is the separate full SHA256. Display
notes never participate in path lookup or identity. Names are not creator roles:
known basenames/folder conventions classify VOICE, IDENTITY, STORY, KNOWLEDGE,
EDITORIAL_HISTORY, OFFER_CTA and REFERENCE. Unrecognized files stay REFERENCE;
there is no named-creator fallback. This is not a new authentication boundary.

Optional operator policy is a **configured read_files entry** named exactly
`context-selection.json`. It is itself hashed/pinned in approval; changing it
cannot change an approved execution silently. It contains a JSON list:

```json
[
  {
    "asset_id": "asset-<ID obtained from registry>",
    "stages": ["CREATIVE_PLAN"],
    "display_note": "candidate Story relevant to this task",
    "section": "Exact unique Markdown heading"
  }
]
```

`registry(assets)` provides identities without loading source bodies. Stage
names are CREATIVE_PLAN / WRITER / CRITIC / REWRITE (both Critic passes use CRITIC).
Only manifest assets can be selected. A policy is curated task selection, not a
search/router, inferred recommendation or token/file cap. Nonstandard creator
filenames require a separately reviewed role/config extension; do not guess.

Planner Story/Knowledge selections require an exact unique heading; missing or
ambiguous section fails, never falls back to the entire vault. Execution uses
the approved match section and verifies support_quote within it when present.
Multiple approved sections of the same file are included; unused sections are
not. Story NONE gives no Story body. Missing required voice is explicitly marked
in the pack; NativeHost stops before launch with `creator_voice_context_required`.
Editorial default is table header plus last two rows, not a full-history audit;
non-table history requires explicit section selection. Its limited coverage
must not be represented as complete anti-repeat verification.

Psychology is **still required by runtime**. `psychology.reference_id` may select
the exact configured library; code resolves `library_source`. A supplied path
must match exactly. Annotated paths are rejected, never stripped or guessed.
Old exact-path proposals remain valid history. Policy optionality from C1 does
not remove library validation, title-eight or the C5.15 UNKNOWN/blocker history.

## Read/load evidence and privacy

Local `context-trace.json` records stage, authority inputs, knowledge hashes,
selected creator/reference/source IDs, omitted families and receipt counts.
Receipts distinguish ALLOWED → SELECTED → READ_ATTEMPTED → READ_SUCCEEDED,
or ALLOWED → OMITTED; failed loads record READ_FAILED where an asset read began.
Path/hash/reason/section projection hash and character count are metadata only.
No private raw excerpts or display-note text are written into the trace.

READ_SUCCEEDED means **the deterministic adapter loaded verified bytes** into
the stage payload. The payload is embedded into the trusted script, then passed
to the creative agent prompt. This is distinct from a native Read tool event,
model attention/comprehension, and a file being merely hashed/allowed. Each
receipt marks `model_read=UNKNOWN`. Do not call this proof of model understanding.
Source-file Read grants are removed for D1; required selected excerpts are inline.
Only the workflow script remains readable by the outer host. Existing local
intake/script/event artifacts can contain private data and remain private; the
metadata trace is not permission to publish those raw artifacts.

## Auto-injection visibility

Known: adapter-built stage prompt, canonical projection, selected creator and
reference excerpts; stored payload hash and workflow script hash. Embedded
workflow also contains legacy text and the outer host can read that script.
Critic uses the independent agent type; D1 replaces explicit legacy Critic prompt
in the V2 stage with the canonical contract. It does not rewrite agent files.

UNKNOWN: extra effective host/project/agent instructions and whether the model
attended to them. Trace labels these separately as host/agent auto-injection;
they are not explicit asset-read receipts. No claim of full host observability
or of eliminating all automatic legacy influence. This remains a review risk.

## Modes, tests and next boundary

REEL projection includes spoken rhythm and spoken/text/visual/optional-audio
alignment. SHORT/LONG Writer projections omit that package and use written
rules. Historical word ranges are untouched. There is no token-saving claim.

Run `python -m pytest tests -q -p no:cacheprovider` and
`python -m integrations.content_intelligence.semantic_parity`.
Fixtures test stage payloads and actual JS agent prompt assembly without model
generation, role isolation, section exclusion, fresh Critic reads, stable IDs,
old-plan history/new-plan invalidation and unchanged hard/title/mode guards.

Remaining policy migrations: optional psychology, title-eight modernization,
better editorial selection, nonstandard roles/sections and host auto-injection
visibility. These are not silently resolved in D1. No C5 rerun, RP3.E, Writer
model run, Notion, publish or merge is authorized by green tests.
