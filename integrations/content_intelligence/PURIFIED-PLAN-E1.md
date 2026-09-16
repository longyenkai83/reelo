# E1 — simplified integrated Creative Plan

Route identity: `reelo.creative-plan.e1`. New Planner runs produce this contract;
historical V2 plans and the legacy batch route retain their own validation.
C5 FROZEN; Phase 9 NOT ACCEPTED. No creative/model acceptance in this slice.

## One semantic plan, one human gate

Primary fields are one_idea, reader_value, content_job/recipe_id, proof_plan,
emotional_movement, opening_plan, title_plan, outline/payoff, cta_direction,
limitations, advisories, publication_requirements. Packet/insight/angle identity,
PROPOSED truth type and output format remain explicit platform fields. Existing
safety attestations are internal guards, not scores for the six writing lenses.

`PurifiedPlan` is stored once. `execution_view` derives a compatibility view for
existing source/Story/candidate checks and approval machinery; it is not a second
stored semantic authority. Full E1 meaning is retained in Writer/Critic packs.
The gate projection omits internal compatibility rows and technical candidate
checks, exposing one recommended Hook/Title and at most one alternative each.
It includes proof use, movement, reader value, outline/payoff and limitations.
Packet publication requirements are added by code and cannot be cleared by omission.

## Psychology and proof

`psychology = "NONE"` is valid in E1. No psychology library is required or loaded
into an approved NONE plan's packs. Planner does not select that library by
default; an explicit task reference selection may support exploration before
a plan exists. If used, psychology requires stable reference_id, exact configured
source/hash and supported mechanism name. Optional path must match the resolved
ID. Psychology may support expression only, never infer motives or replace B.

Proof kinds: CUSTOMER_EVIDENCE, CREATOR_STORY, CREATOR_KNOWLEDGE,
EXTERNAL_KNOWLEDGE, ILLUSTRATIVE_AI, NONE. Each says what it supports and how it
contributes. Customer evidence references must exist in the immutable packet.
Source-backed proof checks manifest identity/hash, allowed source role, exact
unique section and exact support_quote. Creator knowledge uses attributed
creator_observation from creator sources, not external facts promoted to lived
experience. ILLUSTRATIVE_AI requires disclosure and cannot serve factual proof.
NONE cannot accompany `requires_factual_support=true`, a source or evidence IDs.

This last check validates a declared contract, not semantic detection of every
factual sentence. Human/independent Critic must catch a false declaration; the
nine hard truth guards and source-scope constraints still apply. Story is optional;
DIRECT needs supported same experience, ADJACENT cannot be used as that experience.
No selected Story is NONE. Source emotion, realization and results may not be
fabricated to complete a recipe. Creator/knowledge path conventions remain those
of the existing source-role boundary; this is not a private data migration.

## Movement, opening, title

Movement is the planned reader transition: start → question/tension → optional
change → end. Confusion-to-clarity and quiet reflection are valid. It is not a
statement about emotions in source material.

Opening uses rapid context/relevance/curiosity/truth/clarity; no mandatory hook
taxonomy. REEL may have aligned spoken/text/visual/optional audio. Article plans
reject a Reel package. Output mode is explicit and bound into the plan hash.

Title uses meaning/relevance/faithfulness/useful promise, preserving exact approved
wording. Internal compatibility remains **three to five real title options** total:
title_plan choices plus compatibility_titles. Extra rows are not presented as
Owner choices and cannot be selected through the human review API without first
becoming a primary/alternative component in a new plan revision.

No invented or copied padding rows: candidates have distinct IDs and must be
genuine distinct options. This retains some internal exploration cost; E1 does
not claim candidate-table complexity has disappeared from runtime entirely.

## Single canonical title-eight compatibility

`semantics-a1.json` remains the title meaning authority. Its explicit
`purified_e1_title_overrides` specializes only checks 1 and 8 for this route:

- Check 1 retains separate psychology/frame/treatment columns; psychology NONE
  needs no library. A used mechanism must verify its stable reference. SELF_MADE
  frame is allowed; sourced frames require exact source identity/section.
- Check 8 keeps the real internal 3–5-row table; it is not duplicated into the
  article or exposed as 3–5 mandatory choices in the human gate.

`title_table` derives these columns from the single stored plan. Other six
meanings remain shared. All eight booleans must still pass; false/malformed
results keep existing vetoes. No second independent title rubric or auto-PASS.
Historical route keeps the original meanings; no stored results are rewritten.

## Human edit and repair API

`PlanStore.review` retains approve/EDIT_AND_APPROVE/reject/defer and human_attested.
Selecting an already-present meaningful alternative makes a new approval and
invalidates the old current approval through the existing latest-review check.
It does not rewrite the plan's component text.

E1 inline edited_hook/edited_title/edited_outline or changed selected_mode are
rejected with a revision-required error. Use:

```python
pending = store.revise(plan_id, revised_proposal, context, assets,
    reviewer="Owner", human_attested=True, expected_plan_hash=old_hash)
# Present pending['review_view']['integrated_plan']; obtain a NEW human review.
# Then use store.review with this revision's ID/hash. Never inherit approval.
```

Revision is append-only, binds parent ID/hash/reviewer, starts pending, and checks
the latest revision again inside the write transaction. Job, recipe, Story,
movement, outline or mode changes invalidate the old approval. One Idea wording
changes are conservatively routed upstream as well: the code does not pretend
to prove semantic equivalence. Different angle/One Idea meaning requires Owner
correction upstream; the plan revision API cannot change those authority fields.
Local operator trust/authentication assumptions are unchanged. Model tools never
receive a review/approval capability; human_attested is not a new identity system.

## Writer and independent Critic

Writer receives the approved recommended/selected components, not alternatives
or internal title rows. It may shape prose/rhythm/transitions, not recipe, Story,
proof, psychology, mode, angle or selected component direction. NONE remains NONE.
Code retains exact title/mode checks and adds exact opening-prefix verification
for E1. Semantic fidelity beyond exact words still needs Critic/human review.

Critic uses six lenses semantically, never six numeric scores. Findings include
WHAT (message), WHERE (affected_text), WHY and typed repair_layer:
PROSE / PLAN / UPSTREAM_OWNER / CUSTOMER_INTELLIGENCE / PLATFORM.
Missing actionable findings for reported blocking/fidelity failure is an integrity
error, not implicit permission to rewrite. A blocking non-PROSE finding stops at
CRITIC_FAILED for review; no Writer strategy repair or new automatic loop. Prose
repair remains maximum one rewrite, followed by Critic2.

The layer is a semantic judgment supplied by Critic, not inferred via regex.
Example: faithful Story with no useful payoff → PLAN, not “add emotion”.
The nine hard categories still force blocking regardless of reported severity;
adding a repair layer never downgrades them. Final owner content approval remains
PENDING even after machine PASS.

## Context and history

D1 receipts/projections stay in place. NONE psychology is omitted with an explicit
trace reason; manifest hashing/currentness still checks allowed assets and is not
a model/context read. Writer/Rewrite receive selected proof/voice, not exploration.
Critic alone gets the internal title table and sourced frame library if needed.
Full historical plans/approvals/UNKNOWN are not mutated or reconciled. No C5.15 run.
Host/agent auto-injection remains UNKNOWN as documented in D1; no new observability
claim, no token-saving claim and no private source contents in shared reports.

Tests: `python -m pytest tests -q -p no:cacheprovider` plus A1 semantic parity.
No live model, Notion, publish, merge or next phase is authorized by green tests.
