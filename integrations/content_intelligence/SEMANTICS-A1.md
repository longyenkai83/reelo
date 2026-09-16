# RP3.A — canonical semantics, Slice A1

Authority: owner-approved RP2 plus the bounded RP3.A implementation request.
The single semantic origin for **mode meaning, V2 title review and Critic
severity/repair** is [semantics-a1.json](semantics-a1.json). Its ordered title_checks
and named rules are the reviewable definition. This page explains maintenance,
not a second rubric. The rest of the historical quality library is out of scope.

## Ownership and representations

- Writing Knowledge taxonomy remains CORE / RECIPE / CREATOR_MEMORY / REFERENCE.
  Platform/workflow infrastructure is separate. No directory migration here.
- The six writing lenses are semantic language only; no six-boolean validator.
- The JSON is a maintenance contract, **not injected into runtime prompts**.
  Existing Python, JS and Claude-host representations remain in place and are
  checked against it. This preserves source/approval hashes and runtime behavior.
- V2 takes its eight meanings from the existing quality rubric with V2 boundary
  overrides, approved-plan placement of candidate tables and current code vetoes.
  The JSON now governs future maintenance of those V2 meanings. Legacy's rubric
  ownership statements still apply outside this narrow V2 scope.
- The canonical mode description clarifies purpose (including deeper written
  argument/narrative for LONG_ARTICLE); current runtime shorthand is preserved.
  Explicit mode is locked when present. Historical approval format fallback is
  unchanged; no forced migration or new required field is introduced.
- Legacy seven-item prompt/agent and eight-item library remain an **isolated
  compatibility discrepancy**, not a newly certified consistent legacy rubric.
  Existing V2 override supersedes seven-item instructions only in the V2 route.
- Existing owner-quality booleans are additional gates, not a ninth title box.
  All eight title results currently must pass in code; this patch relaxes none.
- Repair ownership is descriptive. It adds no dispatcher, retry, extra rewrite,
  model authority or permission to change a locked plan/angle/evidence/approval.

## Verification and safe maintenance

Run from Reelo root:

    python -m integrations.content_intelligence.semantic_parity
    python -m pytest tests -q

The first command checks scoped title meanings, mode clauses, V2 schema enums
and title cardinality, Python hard-category membership, V2 overrides, legacy
numeric guidance and required host clauses. Embedded JS still requires exact
sync. Missing files fail visibly. It reads repository text only.

The full suite also tests effective runtime behavior: each title failure blocks,
each canonical hard category defeats model advisory/PASS, UNKNOWN fails closed,
publication requirements do not authorize unsupported draft assertions, and
existing currentness, provenance, exact plan locks and bounded stages remain.
All creative outputs in tests are synthetic fixtures, never a live model call.

Clause checks normalize whitespace/Markdown emphasis and locate individual
rubric rows. They are conservative maintenance signatures, not proof of natural
language entailment. Rewording can require reviewed updates; contradictory extra
prose can still require human review. Behavioral regressions supplement signatures.
The checker is part of pytest, not a newly installed hosted CI service.

When changing an in-scope meaning, obtain the relevant owner/architect decision,
update the canonical definition first, then affected mirrors and regressions in
the same reviewed change. Do not merely update tests to bless unintended drift.
Do not retrofit old approvals, historical state or private source hashes.

## Frozen boundaries / next actor

Historic Reel ranges remain unresolved pending benchmark/product decision.
No numeric winner or universal word-count blocker is introduced. Story NONE
and exact approved Hook/Title wording remain protected. Publication approval
stays separate from Critic PASS.

C5 / Phase 9 creative acceptance remains FROZEN and NOT ACCEPTED. C5.15 UNKNOWN
and its psychology-library blocker are untouched. Creator-specific leakage and
migration belong to separately authorized RP3-B; no cleanup is done here.
No Planner/Writer/acceptance run, private source edit, Notion, publishing or merge.
After the A1 report, owner forwards it to Architect; no next slice is automatic.
