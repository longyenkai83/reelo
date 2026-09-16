# RP3.B — creator boundary, Slice B1

Reelo shared semantics do not identify a creator. Identity, voice, cadence, CTA,
life examples and lived Story come from the explicitly selected creator's private
context. Customer truth remains Zone A; creator context never expands it.

## Resolution

V2 reuses the existing operator read_files manifest, unchanged. creatorContext
adds an index of already-supplied about-me, voice-profile, writing-rules,
writing-rules-chi-tiet, kho-cta and kho-cau-chuyen assets. It does not read files,
discover folders, add tool permissions, replace paths, change hashes or remove
anything from the original manifest. The independent stages still read their
authorized sources. Nonstandard filenames remain in the full original manifest;
this small index does not infer their role.

Legacy may receive creator_assets as an explicit list of path/sha256 metadata on
each item. When absent, the existing selected private workspace and brand checks
remain authoritative. An unselected/missing workspace is reported as missing
context, never replaced with a named creator or another workspace. This is not
multi-tenant authentication or automatic brand discovery.

Existing creator preferences take precedence over illustrative shared defaults
within the approved plan and truth constraints. No generic voice is imposed to
replace a supplied private voice. Carousel's existing relaxed voice requirement
is preserved. No mode/recipe/psychology/hook mechanism has been redesigned.

## Dispositions

- MOVE_TO_CREATOR_MEMORY: named voice, preferred address, personal life anchors,
  CTA wording and cadence are delegated to existing configured private sources.
  No private file is rewritten or new private preference claimed as fact.
- MOVE_TO_REFERENCE: the historical niche story/question/scene examples and
  owner-liked PAS worked example now live in reference-examples. They are
  optional historical teaching illustrations, not creator/customer evidence.
  They are not in default active recipe text and are not automatically loaded.
- KEEP_SHARED: format distinctions, seven story stages, PAS mechanism, hook/title
  mechanics, generic Vietnamese craft and all protected truth/approval guards.
- REMOVE_LATER disposition from RP2 is now addressed for ownerQuality's named
  creator and rejected-title literal: keep general clarity/POV/tone principles;
  the rejected case lives only in regression fixtures.
- MOVE_TO_RECIPE: deferred. No recipe catalog migration or redesign in B1.

The root host instructions and affected .agents mirrors are neutralized as well;
otherwise removing a name from just the JS prompt would leave a second source.

## Preservation and limits

The existing creator workspace continues to supply its original read-only
sources. Tests use two explicitly synthetic workspaces with different name,
voice, CTA, writing preference and Story. They test context assembly/source
availability and guard behavior, not the quality of generated prose or whether
a model will always obey the sources. There is no live creative run.

Historical reports/logs, approvals, UNKNOWN and reconciliation records are not
rewritten. Shared library bytes changed in this slice, so a prior approval whose
manifest pins those shared files can become stale. Existing checks must reject
it; never update stored hashes or approvals to force a match. Any future creative
execution needs the existing currentness/approval process, outside this frozen
slice.

J: operational workspace is not deployed or modified by this implementation.
This branch is the implementation under review. Private source checks are
read-only. Historical creator examples are not evidence of new customer demand.

## Verification / state

Run python -m pytest tests -q and
python -m integrations.content_intelligence.semantic_parity from Reelo root.
The suite includes the Node fixture harness and embedded-module sync guards.
A1 canonical semantic definition, modes, eight title meanings, nine hard
categories, exact locks and maximum one rewrite remain unchanged.

C5 creative acceptance FROZEN; Phase 9 NOT ACCEPTED. No Writer, Planner,
Notion, publication, merge or next slice is authorized by B1 tests.
