# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate mapping identities | Validate one selected context, eligible segments, and exact eligible formulas from fresh delegated evidence. |
| 2 | Enforce one-to-one mapping | Reject duplicate segments or formulas across the complete proposal. |
| 3 | Prove clean target | Require a fresh task export with zero mapping rows. |
| 4 | Assemble immutable archive | Preserve metadata exactly and write only the exact six-column mapping CSV. |
| 5 | Run Task Hook | Validate the exact ZIP before showing approval. |
| 6 | Submit and verify | After approval, submit once through Core Data Loader and verify with a fresh export. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Mapping validation | Blocker | resolve_computed_field_eff_scope | Context or segment is outside the fixed EFF scope or segment eligibility | Select an eligible context and segment from fresh authoritative data | No |
| Mapping validation | Blocker | resolve_fast_formula_details | Formula identity, type, effective state, or compilation evidence is invalid | Correct the formula and re-run delegated direct reads | No |
| Complete mapping set | Blocker | | A segment or formula is duplicated | Provide a one-to-one mapping set | Yes |
| Import preparation | Blocker | export_current_computed_field_mappings | Baseline members are missing or current mapping rows are nonzero | Perform manual cleanup and re-export | No |
| Archive construction | Blocker | | Metadata changes, header differs, Formula Text appears, or technical identity is not exact | Rebuild from the fresh clean baseline | Yes |
| Final preview | Blocker | validate_computed_field_import_artifact | Task Hook is incomplete, artifact identity changed, or preview lacks required evidence | Re-run Task Hook against exact final bytes | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_computed_field_eff_scope | Context, segment, or mapping work | Eligible context and segment identity | ora_reference_lookups.md |
| resolve_fast_formula_details | Formula list or mapping work | Eligible formula and exact import identity | ora_reference_lookups.md |
| export_current_computed_field_mappings | Mapping creation, import, or verification | Fresh baseline, mapping rows, or post-import comparison | ora_reference_lookups.md |
| validate_computed_field_import_artifact | Final import preview | Exact archive validation and approval fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JACF.VALIDATE_MAPPING | step | 5 | design_enforcement | valid->JACF.EXPORT_BASELINE;issues->JACF.MAPPING_ISSUES | JACF.RESOLVE_FORMULAS | stop | A complete mapping proposal is available |
| JACF.BUILD_ARTIFACT | step | 7 | design_enforcement | built->JACF.TASK_HOOK_PREVIEW;issues->JACF.ARTIFACT_ISSUES | JACF.EXPORT_BASELINE | stop | Fresh baseline contains zero mapping rows |
