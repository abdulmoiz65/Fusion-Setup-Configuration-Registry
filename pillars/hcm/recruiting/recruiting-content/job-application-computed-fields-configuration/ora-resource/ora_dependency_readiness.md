# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | EFF context and segments | Obtain a fresh EFF task export through `hcm.recruiting.recruiting-common.manage-extensible-flexfields` and validate the fixed scope and authoritative segment file. |
| 2 | Fast Formula identity | Invoke `hcm.global-payroll.payroll-tools.fast-formulas` with the required all-details business request for every selected formula. If no Legislative Data Group filter is supplied, use `Global` for the current tenant. |
| 3 | Current computed-field mappings | Export this exact task through shared.setup-export.task-level-export. |
| 4 | Clean target | Confirm ORA_IRC_JA_COMPOUND_FIELD_DATA.csv contains zero mapping rows. |
| 5 | Immutable FSM archive | Preserve ASM_SETUP_CSV_METADATA.xml exactly and assemble the validated mapping CSV. |
| 6 | Task Hook preview | Run Core Data Loader task-hook validation against the exact immutable ZIP before requesting approval. |
| 7 | Approved import and verification | After exact approval, submit once through Core Data Loader, then verify with a fresh task export. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| JACF_EFF | Fresh EFF definition | Yes | Context, segment, or mapping work | Lookup | Delegated EFF skill export | resolve_computed_field_eff_scope | Establishes eligible context and segment identity | Select one context after reviewing the context summary | FlexContextCode and eligible FlexSegmentCode values |
| JACF_FORMULA | Fresh formula details | Yes | Formula listing or mapping work | Lookup | Delegated direct read through `hcm.global-payroll.payroll-tools.fast-formulas`; omitted Legislative Data Group defaults to `Global` | resolve_fast_formula_details | Establishes effective, compiled import identity from the taxonomy-supported offering and scopes discovery to the current tenant's global candidates | Correct any unavailable, ambiguous, ineffective, or uncompiled formula | BaseFormulaName, FormulaId, FormulaTypeId, effective and compile evidence |
| JACF_BASELINE | Fresh task export | Yes | Mapping creation, replacement, or import | Lookup | Task-level export | export_current_computed_field_mappings | Provides the immutable metadata member and current mapping state | Existing rows must be removed manually in the FSM task | Baseline ZIP, metadata member, mapping-row count |
| JACF_TASK_HOOK | Core Data Loader Task Hook | Yes | Final import preview | Verify | Exact immutable ZIP | validate_computed_field_import_artifact | Binds task validation and approval to exact bytes | Approve only after all task rules pass | Validation result, approval fingerprint, envelope readiness |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All fresh dependency evidence is complete and the target is clean | Yes; build and validate the immutable artifact |
| Manual cleanup required | Current mapping CSV contains one or more rows | No; stop until the user confirms manual deletion and a fresh export is clean |
| Blocked | Context, segment, formula, archive, task-hook, or environment evidence is missing or invalid | No |
