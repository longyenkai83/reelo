# Journey restoration — owner-authorized product correction, 2026-09-16

Reelo is a personal-brand content journey system. Campaign goal → awareness/journey →
sequence → selected fuel → one idea → job/recipe → mode → purified Creative Plan → shared
Writer/Critic/at most one prose repair. Journey owns the communication job, not prose.
Customer Intelligence is one source, not a mandatory root. This supersedes the GLOBAL
reading of Insight DEC-007; the Insight-led pipeline and its actual human truth/angle
gates remain unchanged. No portable CIP schema change, operational J: deployment, Notion,
publish, main merge or Phase 9 acceptance is implied.

## Recovered legacy capability

| Evidence family | What it actually supplied | Authority / runtime distinction |
|---|---|---|
| `engine/cong-thuc-viral/chien-luoc-content.md` | Five awareness stages; stage-to-content suggestions; cycle continuation | Doctrine. Earlier fixed ratios explicitly disabled; do not revive them |
| `.claude/skills/chien-luoc-gia` and `.agents` mirror | Goal/time, campaign first, allocation, proposed calendar, owner approval | Agent instructions, not an executable durable journey object |
| `viet-script/references/tuyen-lanh/am/nong/ban.md` | Different jobs, content treatments and CTA restraint | Reference doctrine; recipes are not awareness stages |
| `review-chu-ky` | Review actual performance, bottlenecks, next-cycle allocation | Dynamic Ratio is contextual planning guidance, not inferred customer truth |
| Creator campaign plans / journey map / CTA / offer bank | Campaign-specific objective, sequence, wording, offer transitions | Private creator configuration/historical decisions; not new authorization |
| Editorial index / archived index | Source/topic/treatment/CTA usage and draft status | History, not proof of market validation or current approval |
| `viet-bai` / `viet-script` | Format router and sequential agent procedure | Markdown orchestration; conflicting older microgates remain legacy-only |
| Operational `batch-content.js` | Parallel independent article workers, rotating treatment, Critic, one repair | Actual JS behavior. No cross-piece journey state; source lookup delegated to workers |

Operational J: differs from this branch by V2 boundary banners, creator neutralization,
and the V2 workflow module. Several reference files have equal normalized text but
different newline bytes. The local audit manifest records both locations; no private
creator sources or historical files were changed. Root journals/indices and campaign
examples do not prove all named campaigns or offers are currently active.

## Semantic crosswalk and CTA

| Legacy meaning | Five-stage range | Useful legacy restriction |
|---|---|---|
| Cold | UNAWARE / PROBLEM_AWARE | Recognition/reach, no accidental sale |
| Warm | PROBLEM_AWARE / SOLUTION_AWARE | Trust/education; real resource or conversation when relevant |
| Hot in `tuyen-nong` | SOLUTION_AWARE / PRODUCT_AWARE | Pre-purchase/category/proof; no direct pitch |
| Hot-sale in creator CTA bank | PRODUCT_AWARE / MOST_AWARE | Historical grouped commercial wording; needs explicit commercial scope |
| Sell | MOST_AWARE | Clear real offer and one direct CTA when authorized |

These are semantic ranges, **not exact equivalence**. Unqualified `hot` is ambiguous.
Seven lifecycle stages and creator's six journey phases also include post-purchase
support/loyalty/advocacy, outside the five awareness labels. Do not normalize creator data
in place. A strategy stage is PROPOSED intended audience context, not observed identity,
belief, motive, purchase readiness, demand or actual movement after publication.

CTA STRATEGY is the slot intent. CTA VOICE is expression from selected creator context.
Small intent set: reflect, engage, save/follow, resource, method, DM, explore offer,
book/buy/apply. No fixed exhaustive stage-template matrix. Enforced ceilings: no commercial
CTA in the first two stages; explore-offer needs product/most-aware; direct sale needs
most-aware AND real offer context AND human campaign execution authority. Resource CTA
needs an actual resource source. Other choices depend on goal/job/context. Critic checks
semantic CTA fidelity; deterministic enums cannot prove prose has no disguised pitch.

## Typed local scope and sources

`models.py`: JourneyPlan binds CampaignRequest, full source catalog, ordered slots and
imported editorial context. Request binds creator, goal/audience, start/target, count,
route, timing, allowed modes/CTAs, boundaries, optional offer/resource. Each slot binds
stage/objective/movement/next stage, one idea, job/recipe, exactly one primary, zero-to-two
useful supports, reader value, CTA, mode and all prior slots. Recipes reuse C1 unchanged.
No universal ten-step sequence. `explore` accepts one bounded proposal provider with all
prior assignments/history. `propose_flow` is a deterministic starting proposal using
explicit topics, start/target and optional stage sequence; it is not semantic discovery
or a claim of strategic effectiveness. A source is not automatically evidence merely
because its summary matches a topic. Human/semantic quality review still matters.

Four entry routes feed one engine: STORY_LED, INSIGHT_LED, KNOWLEDGE_POV_LED,
AUTO_DISCOVERY. Source kinds stay internal. The catalog may include customer speech,
verified insight, creator/client story, creator knowledge/experience, market observation,
future possibility and offer facts. No forced Story/Insight/Knowledge. Automatic matching
is currently exact catalog-topic matching plus source-use history, not whole-vault search.
Catalog construction/relevance is explicit operator input; no hidden private-source crawl.

Every source binds creator/path/hash/exact unique section/provenance/truth type. Source
summaries are index proposals, not claim evidence. Source bytes are read-only and rechecked
before/after each stage. Attributed EXTERNAL_KNOWLEDGE stays distinct from creator POV.
Offer/resource fuel counts within the same primary-plus-two bound; no hidden fourth source.
Candidate refs may cite exact selected source IDs or real CIP evidence IDs, not annotated paths.
Selected source bytes are checked
before/after each stage. Client Story needs a separate current permission JSON bound to
source ID/hash, creator, reviewer/human attestation, `scope=content_drafting`, `revoked=false`;
grant file itself is hash-pinned. This is local operator attestation, not legal/RBAC proof.
Future possibilities remain HYPOTHESIS/PROPOSED. Unsupported or changed data fail closed.

Insight use additionally requires an actual canonical CIP plus a producer-owned CURRENT
ledger callback. No callback means no model call. Its A/B are copied intact, and the slot
one idea is the selected core argument; journey cannot silently replace that angle.
Non-Insight context uses null packet/insight/angle IDs, never invented Verified Insights.
`reelo.journey-creative-plan.1` extends E1's same expression fields with campaign/slot/hash;
it does not alter the existing `reelo.creative-plan.e1` or portable CIP schema.

## Authority, calibration, memory and execution

CampaignStore keeps immutable plan revisions and hash-linked append-only events on local
SQLite. No synced operational vault DB. Changing the plan invalidates old authority;
revoke is checked during execution. Local file access is trusted, hashes not authentication.
Concurrent execution reservation is serialized; same slot does not launch again. UNKNOWN
does not auto-retry; an unresolved Planner launch requires reconciliation. Earlier RP4
UNKNOWN/approvals/results are untouched and are not imported into this new campaign store.

A terminal proposal rejected by validation may be the parent of an explicit trusted-operator
`propose_terminal_revision`: exact durable request/envelope/current sources are rechecked,
all original UNKNOWN/raw fields remain unchanged, and the new proposal records its origin,
parent hash/operator/rationale. This does not declare the native candidate accepted or
grant continuation/approval. Guided execution still requires a new actual human Creative Gate.
The API is not exposed as a model tool or automatic quote/claim repair.

GUIDED: explore → proposed Creative Plan → actual human sample-plan approval → sample
Writer/Critic → actual human sample approval/calibration → explicit EXECUTE_REMAINDER.
Calibration is campaign-local, never automatically written to global voice. AUTOPILOT:
explicit human authorization of the exact campaign revision → plan/write remaining slots
within that scope without per-piece approval. Per-piece plans record campaign-execution
authority, **not** fabricated human creative approval. Models receive no decision tools.
Final human content approval remains PENDING and publishing authority is separate.

`JourneyEngine` uses `NativeHost.invoke_stage`, D1 context packs, E1 semantic fields/checks,
the same `execute_stages`, same nine hard finding categories and one-rewrite maximum.
Writer content excludes internal source headers; typed metadata records sources separately.
Critic receives fresh checked source excerpts. Non-prose defects stop at their proper layer.
Later slots receive completed source/topic/idea/job/stage/CTA/hook/title history,
campaign calibration and next intended movement. Completed stages do not establish an
audience state change. Imported history cannot override goal, truth or scope.

## Opt-in use

Run from the Reelo repository with existing requirements installed:

```text
python -m integrations.journey --store LOCAL_PATH/campaign.sqlite explore --request request.json --sources sources.json [--history history.json]
python -m integrations.journey --store LOCAL_PATH/campaign.sqlite inspect --plan-hash HASH
python -m integrations.journey --store LOCAL_PATH/campaign.sqlite prepare --plan-hash HASH --slot slot-1 --config host.json
python -m integrations.journey --store LOCAL_PATH/campaign.sqlite approve-sample-plan --plan-hash HASH --creative-plan-id JCP-ID --config host.json --reviewer OWNER --confirm-human --authority-ref ACTUAL_INSTRUCTION
python -m integrations.journey --store LOCAL_PATH/campaign.sqlite run --plan-hash HASH --creative-plan-id JCP-ID --config host.json
```

`decide` records actual AUTHORIZE_AUTOPILOT / APPROVE_SAMPLE / EXECUTE_REMAINDER / REVOKE.
Never execute those commands from model recommendations. `batch` executes the remaining
authorized scope. `host.json` pins executable, execution_workspace, state_directory,
read_files and bounded timeout/budget/effort. Existing native host verification remains.
CI campaigns use the Python API with the actual producer current-ledger validator; the
standalone CLI fails closed rather than guess authority paths. No publication command.

Legacy Markdown skills and JS entry remain compatible; they are not silently migrated
or certified as obeying Journey. Opt in through this module/API. No deployment to J: in
this change. Historical campaign ratios, personal preferences and indices stay read-only.

## Verification / benchmark boundary

`python -m pytest tests -q -p no:cacheprovider` includes the 22 owner requirements mapped
to tests/test_journey.py; fixtures explicitly synthetic. Node prompt tests exercise the
shared embedded workflow. Existing canonical semantics/legacy regressions remain enabled.
Deterministic stage completion is not evidence of native creative quality.

Resume diversified quality benchmark after integration: Story-led, Insight expert without
Story, Insight + Story, Knowledge/POV, and a multi-piece offer journey. Real sources and
current human truth selections must qualify first. The archived RP4 article remains paused.
Offer availability/campaign business scope needs an actual current owner decision; old
campaign files are insufficient. One final local REPORT-JOURNEY-RESTORATION.md is the
owner handoff; no claim of Phase9 acceptance or validated audience conversion.
