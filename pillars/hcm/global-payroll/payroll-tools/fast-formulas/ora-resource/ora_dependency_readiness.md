# Fast Formulas Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Operation and route | Route Fast Formula setup-data preparation and mutation only through core.data-loader using HCM Data Loader. |
| 2 | Formula type | Confirm the exact FormulaTypeCode and its supported contexts, inputs, and return values for the target release. |
| 3 | Legislative scope | Establish whether the formula is global or LDG-specific and resolve an LDG reference when required. |
| 4 | Effective dating | Ensure the formula starts on or before every object that refers to it. |
| 5 | Dynamic database items | Deploy required flexfields and generate their database items before compiling formulas that use them. |
| 6 | Called formulas | Ensure called formulas exist and have compatible input/output contracts without recursion. |
| 7 | HDL metadata | Apply the supplied FastFormula attribute export: MERGE, supported keys, requiredness, lengths, FormulaText CLOB filename, and immutable/update-only rules. |
| 8 | Compilation | Compile the loaded formula before it is used and resolve every compilation error. |
| 9 | Preview and approval | Require an immutable archive preview and explicit approval in the authorized data-loader workflow before upload or submission. |
| 10 | Fast Formula Type reference | Resolve a supplied formula-type name or display value to exactly one supported FormulaTypeCode or FormulaTypeId; reuse an already valid code or ID. |
| 11 | Legislative Data Group reference | Resolve a supplied LDG name or display value to exactly one supported LegislativeDataGroupId or reference form; reuse an already valid ID. |
| 12 | Predefined Yes/No LOV | When target metadata defines a Fast Formula field as YES_NO, resolve a supplied Meaning to exactly one LookupCode. |
| 13 | Formula status LOV | When target metadata defines a status field as ORA_FORMULA_STATUS_VB, resolve a supplied Meaning to exactly one LookupCode. |
| 14 | Persisted formula action target | Resolve FormulaId and EffectiveStartDate from the primary Fast Formula endpoint for the supplied FormulaName or FormulaId before a formula-content or compilation action. |
| 15 | Persisted formula content | Use the resolved formulaId and effectiveDate to retrieve the stored formula text through getFormulaContent. |
| 16 | Compilation submission | After the formula is persisted, submit it once through submitCompileJob using the resolved formulaId and effectiveDate and the required action content type. |
| 17 | Compilation monitoring | Requery the primary endpoint every 5 seconds while Compiled is N; don't submit another compilation job while the first outcome is pending or uncertain. |
| 18 | Compilation messages | When Compiled is Y and CompileStatus is I or E, retrieve and display the existing compiler message through getFormulaCompileMsg. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| hdl_route | HCM Data Loader route | Yes | Prepare HDL or live load | Satisfied | User instruction and generated task manifest | | The developer explicitly requires all setup-data mutations to use the data-loader route | Use core.data-loader with business object FastFormula | dataloader_import_mode=HDL; businessObject=FastFormula |
| formula_type_contract | Selected formula type | Yes | Validate or Prepare HDL | Blocked | Supplied FastFormulasExport.xls plus the selected formula-type documentation | | FormulaTypeCode is supported metadata, but inputs, contexts, and outputs vary by selected type | Supply the intended FormulaTypeCode and its type-specific contract | FormulaTypeCode; supported contexts; inputs; outputs |
| legislative_scope | Global or LDG-specific formula scope | Yes | Prepare HDL | Blocked | Supplied FastFormulasExport.xls plus explicit design choice | | The export supports LDG name and ID references, while the supplied minimum example demonstrates a blank global scope | State global or LDG-specific and provide one supported LDG reference when scoped | LegislativeDataGroupName or LegislativeDataGroupId reference; scope decision |
| effective_start_order | Formula effective date precedes dependent objects | Yes | Another object refers to the formula | Satisfied | Formula EffectiveStartDate and referring-object start date supplied to the runbook | | Oracle requires the formula to be effective before dependent objects start | Provide both dates and correct the formula date if required | EffectiveStartDate readiness result |
| flexfield_database_items | Generated flexfield database items | Conditional | Formula source uses a flexfield database item | Blocked | Deployed flexfield and Generate Flexfield Database Items process evidence | | Flexfield database items don't exist until the process generates them | Deploy the flexfield, generate its database items, then compile dependent formulas | Generated database-item names and process result |
| called_formula_contract | Called formula compatibility | Conditional | Formula source calls another formula | Blocked | Calling and called formula contracts | | Missing formulas, recursion, type mismatch, and excessive call depth cause execution errors | Supply both contracts and correct every mismatch before compile | Called formula identity; input/output types; call-depth result |
| fastformula_hdl_metadata | FastFormula HDL contract | Yes | Prepare HDL | Satisfied | Supplied FastFormulaAll.dat, FastFormula.dat, and FastFormulasExport.xls | | The supplied sources establish MERGE, the supported attribute set, key types, requiredness, lengths, FormulaText CLOB handling, and update-only fields | Use only the captured contract; don't infer DELETE or other actions | MERGE; key strategy; FormulaText; attributes; lengths; requiredness |
| authorized_hdl_handoff | Authorized HDL execution workflow | Conditional | Live upload, import, or load is requested | Blocked | Approved environment, authorized Data Exchange access, exact preview, and explicit approval | | Resource authoring doesn't authorize Fusion mutation | Complete core.data-loader validation, preview, approval, submission, and monitoring gates | Environment; archive fingerprint; approval evidence; request ID |
| compilation_result | Successful Fast Formula compilation | Yes | Formula will be used | Blocked | Fast Formulas compile action or Compile Formula flow result | | All formulas must compile before use | Compile after load and correct every reported line/type error | Compilation status and sanitized errors |
| formula_type_reference | Fast Formula Type foreign reference | Conditional | A formula-type name or display value is supplied, or a supplied FormulaTypeCode or FormulaTypeId isn't already validated | Lookup | Supplied formula-type name, display value, code, or ID | resolve_fast_formula_type_reference | FormulaTypeId is an exported foreign object reference whose user-key alternative is FormulaTypeCode | Provide an exact formula-type value and don't use an unresolved display name in the HDL record | FormulaTypeId; FormulaTypeCode |
| legislative_data_group_reference | Legislative Data Group foreign reference | Conditional | The formula is LDG-scoped and an LDG name or display value is supplied, or a supplied ID isn't already validated | Lookup | Supplied LegislativeDataGroupName, display value, LegislativeDataGroupId, or supported source-system reference | resolve_legislative_data_group_reference | LegislativeDataGroupId is an exported foreign object reference to LegislativeDataGroups with LegislativeDataGroupName as its user key | Provide one exact LDG value and don't use an unresolved display name in a code-or-ID field | LegislativeDataGroupId or supported reference; LegislativeDataGroupName |
| predefined_yes_no_lov | Predefined Yes/No lookup | Conditional | Target metadata defines an in-scope Fast Formula field as YES_NO and a Meaning is supplied instead of a valid LookupCode | Lookup | Supplied Meaning or already-valid LookupCode | resolve_yes_no_lookup_code | Import fields that require a code must not receive unresolved display text | Provide the exact Yes/No display value or a valid LookupCode | Target field: LookupCode; display evidence: Meaning |
| formula_status_lov | Fast Formula status lookup | Conditional | Target metadata defines an in-scope status field as ORA_FORMULA_STATUS_VB and a Meaning is supplied instead of a valid LookupCode | Lookup | Supplied Meaning or already-valid LookupCode | resolve_formula_status_lookup_code | Formula status imports must use the resolved status code rather than unresolved display text | Provide the exact status display value or a valid LookupCode | Status field: LookupCode; display evidence: Meaning |
| formula_action_target | Persisted Fast Formula action target | Conditional | Formula content or compilation is requested | Lookup | Primary Fast Formula endpoint record matched by supplied FormulaName or FormulaId | resolve_fast_formula_action_target | The supplied custom actions require the persisted FormulaId and effective date rather than guessed values | Provide FormulaName or FormulaId and require one effective persisted match | formulaId: FormulaId; effectiveDate: EffectiveStartDate; Compiled; CompileStatus |
| formula_content | Persisted Fast Formula content | Conditional | Formula text is requested for a persisted formula | Lookup | getFormulaContent result for the resolved action target | get_fast_formula_content | Stored content must be returned from Fusion rather than a local or stale copy | Resolve the target and return the custom-action result | FormulaText: result |
| formula_compile_submission | Fast Formula compile job submission | Conditional | A persisted formula is submitted for compilation | Blocked | Developer-provided submitCompileJob contract plus current target resolution and task-specific mutation approval | | Compilation starts a server-side ESS job and must not run before persistence, exact target resolution, and approval | Resolve the persisted target, obtain current approval, then use an authorized executor to submit once | formulaId; effectiveDate; essJobId; essJobState |
| formula_compile_monitoring | Fast Formula compilation state | Conditional | submitCompileJob returned a job response and Compiled remains N | Lookup | Primary Fast Formula endpoint queried with FormulaName or FormulaId every 5 seconds | resolve_fast_formula_action_target | The persisted formula record is the supplied source for Compiled and CompileStatus | Poll until Compiled is Y or the workflow timeout is reached; don't resubmit the compile job | Compiled; CompileStatus; FormulaId; EffectiveStartDate |
| formula_compile_message | Existing Fast Formula compiler message | Conditional | Compiled is Y and CompileStatus is I or E | Lookup | getFormulaCompileMsg result for the resolved action target | get_fast_formula_compile_message | The supplied action returns the existing compiler status, warnings, and errors | Retrieve once and display the returned message | FormulaCompileMessage: result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Supplied source or runbook evidence establishes the dependency | Continue without inventing a lookup. |
| Blocked | Target metadata, design scope, compilation evidence, access, preview, or approval is missing | No; resolve the blocker first. |
| Unsupported | Source material doesn't establish the requested route, action, formula type, or field | No; stop and obtain current target evidence. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->FF.RESOLVE_REFERENCES;blocked->FF.HANDLE_ERROR;unsupported->FF.HANDLE_ERROR | FF.VALIDATE_INPUT | stop | Validated Fast Formula request with an explicit formula type and legislative scope |

## Sources

- Developer-provided /scratch/share/FastFormulaAll.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormula.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Developer-provided standard reference and LOV instructions, received 2026-08-17.
- Developer-provided Fast Formula reference endpoint and session instructions, received 2026-08-17.
- Oracle Fusion Cloud HCM, Example of Loading Fast Formula: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-fast-formula.html
- Oracle Fusion Cloud HCM, Database Items: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/database-items.html
- Oracle Fusion Cloud HCM, Overview of Generating Flexfield Database Items: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-generating-flexfield-database-items.html
- Oracle Fusion Cloud HCM, Example of Generating Flexfield Database Items: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/example-of-generating-flexfield-database-items.html
- Oracle Fusion Cloud HCM, Formula Contexts: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-contexts.html
- Oracle Fusion Cloud HCM, Overview of Calling a Formula from a Formula: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-calling-a-formula-from-a-formula.html
- Oracle Fusion Cloud HCM, Examples of Calling a Formula from a Formula: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/examples-of-calling-a-formula-from-a-formula.html
- Developer-provided persisted formula-content and formula-compilation custom-action contracts, received 2026-08-18.
