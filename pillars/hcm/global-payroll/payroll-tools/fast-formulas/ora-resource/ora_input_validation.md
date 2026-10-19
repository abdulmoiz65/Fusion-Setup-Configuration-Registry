# Fast Formulas Input Validation

## Functional and Data-Mapping Summary

Fast Formula provides reusable calculation, validation, defaulting, selection,
and control logic across payroll. Each formula type defines its own supported
contexts, inputs, and return values. Formula text must follow the Fast Formula
language rules and must be compiled before the formula is used.

For HDL, use the `FastFormula` business object and a `FastFormula.dat` file.
The developer-provided minimum file uses a `METADATA` row followed by a `MERGE`
row. The supplied attribute export confirms that `FormulaText` holds the name
of a separate formula-text file under `ClobFiles` in the same ZIP.

## HDL Operation Contract

| Operation | Supported | Identity | Attribute Behavior | Evidence |
|---|---|---|---|---|
| MERGE create | Yes | SourceSystemOwner plus SourceSystemId, or the documented user-key fields | FormulaCode and FormulaName are required for new records; FormulaCode becomes immutable after creation | FastFormula.dat and FastFormulasExport.xls |
| MERGE update | Yes | FormulaId, GUID, source key, or the user key FormulaCode plus FormulaTypeCode plus LegislativeDataGroupName, subject to target HDL key rules | FormulaId and GUID reference existing records; FormulaCode cannot be changed | FastFormulasExport.xls |
| DELETE | No supplied evidence | None | Do not prepare or execute DELETE | Neither supplied DAT file nor the attribute export documents DELETE |

## Minimum HDL Attributes

| Sequence | Attribute | Requirement |
|---|---|---|
| 1 | SourceSystemOwner | Included in the developer-provided minimum DAT as the source-key owner |
| 2 | SourceSystemId | Included in the developer-provided minimum DAT as the source-key identifier |
| 3 | EffectiveStartDate | Required by the attribute export |
| 4 | FormulaCode | Required for new records and immutable after creation |
| 5 | FormulaTypeCode | User-key and foreign-reference code used by the minimum DAT |
| 6 | FormulaName | Required for new records |
| 7 | FormulaText | Filename of the formula source under ClobFiles |
| 8 | LegislativeDataGroupId(SourceSystemId) | Optional LDG reference; blank in the supplied global-formula example |

## HDL Attribute Metadata

| Attribute | Label | Length | Key Type | Integration Keys Supported | Integration Object | User Key or Reference | Required | Description |
|---|---|---:|---|---|---|---|---|---|
| FormulaId | Fast Formula ID | 18 | Surrogate ID | Yes | Formula | FormulaCode, FormulaTypeCode, LegislativeDataGroupName | Yes | Existing-record surrogate ID; available only when updating |
| FormulaTypeCode | Fast Formula Type Code | 80 | User Key | | | | No | Code of the fast formula type |
| FormulaCode | Formula Code | 80 | User Key | | | | For new records | Unique formula code; cannot be updated after creation |
| LegislativeDataGroupName | Legislative Data Group Name | 240 | User Key | | | | No | Legislative data group name |
| EffectiveEndDate | Effective End Date | | | | | | No | End date of date-effective changes; blank defaults to end of time |
| EffectiveStartDate | Effective Start Date | | | | | | Yes | Start date of the record or date-effective changes |
| Description | Description | 240 | | | | | No | Optional fast formula description |
| FormulaName | Fast Formula Name | 120 | | | | | For new records | Fast formula name |
| FormulaText | Fast Formula Text | | | | | | No | Filename containing formula text under the ZIP's ClobFiles subfolder |
| FormulaTypeId | Fast Formula Type ID | 18 | Foreign Object Reference | No | | FormulaTypeCode | For new records | Surrogate ID of the fast formula type |
| LegislativeDataGroupId | Legislative Data Group ID | 18 | Foreign Object Reference | Yes | LegislativeDataGroups | LegislativeDataGroupName | No | Unique LDG reference |
| SourceSystemId | Source System ID | 100 | Source Key | | | | No | Unique identifier within the source-system owner and component |
| SourceSystemOwner | Source System Owner | 30 | Source Key | | | | No | Source system that generated SourceSystemId |
| GUID | Globally Unique ID | 32 | Globally Unique ID | | | | No | Existing-record reference only; cannot be supplied for new records |
| SourceRefTableName | Reference Context | 200 | | | | | No | METADATA-line context for user-defined staging references; don't supply as a data value |
| SourceRef001 | Reference 1 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef002 | Reference 2 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef003 | Reference 3 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef004 | Reference 4 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef005 | Reference 5 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef006 | Reference 6 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef007 | Reference 7 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef008 | Reference 8 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef009 | Reference 9 | 200 | | | | | No | User-defined staging reference; not saved in the application |
| SourceRef010 | Reference 10 | 200 | | | | | No | User-defined staging reference; not saved in the application |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Validate, Prepare HDL, or Guidance | Stop and request one supported operation | Classify the request before preparing task output | Always | |
| HDL business object | FastFormula | Reject a different object for this task | Use the task manifest businessObject value | Prepare HDL | |
| Formula identity | SourceSystemOwner, SourceSystemId, FormulaCode, FormulaName | Stop and identify each missing value | Supply stable source keys, a formula code, and a meaningful formula name | Prepare HDL | |
| Formula classification | FormulaTypeCode or FormulaTypeId using the exported foreign-reference contract | Stop before DAT preparation | Supply an exact formula-type reference supported by the selected formula design | Prepare HDL | |
| Effective start | EffectiveStartDate | Stop before DAT preparation | Supply a date on or before the start date of every object that refers to the formula | Prepare HDL | |
| Formula text file | One UTF-8 text filename and matching file under ClobFiles | Stop before ZIP preparation | Put the formula source in the named text file and package it under ClobFiles | Prepare HDL | |
| Legislative scope | LegislativeDataGroupName, LegislativeDataGroupId, LegislativeDataGroupId(SourceSystemId), or an intentionally blank value for a global formula | Stop if the intended scope is unclear | Identify whether the formula is LDG-specific or global and use one exported LDG reference form | Prepare HDL | |
| Formula-type contract | Formula-type-specific contexts, inputs, outputs, and return data types | Stop before presenting the formula as usable | Reconcile the selected type with its current Oracle product documentation and target metadata | Validate or Prepare HDL | |
| Compilation readiness | Formula text with valid statement order, initialized variables, compatible data types, supported contexts, functions, and operators | Return all detected issues and stop before loader handoff | Correct the formula and require compilation after load | Validate or Prepare HDL | |
| DAT user-key reference fields | FormulaTypeCode and LegislativeDataGroupName | Stop before DAT or ZIP preparation and identify both missing fields | Populate both fields in every generated FastFormula DAT record using the resolved formula type and legislative data group values | Prepare HDL | |
| Persisted formula action target | FormulaName or FormulaId resolving to one primary-endpoint record with FormulaId and EffectiveStartDate | Stop before a formula-content or compilation action | Resolve the persisted record through the primary Fast Formula endpoint and map FormulaId to formulaId and EffectiveStartDate to effectiveDate | Get formula content or compile formula | resolve_fast_formula_action_target |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Prepare HDL is requested | Valid only when the object is FastFormula, operation is MERGE, the applicable identity and effective-date fields are present, and the FormulaText filename exists under ClobFiles | Prepare an immutable HDL archive preview and hand it to core.data-loader | |
| A formula is LDG-specific | Valid only when the supplied LDG reference resolves through an authorized target-environment workflow | Preserve the exact supported source-system reference form in the HDL record | |
| A formula is global | Valid only when the selected formula type permits global scope and the blank LDG reference is deliberate | Keep the LDG reference blank and record the scope decision | |
| Another object refers to the formula | Valid only when EffectiveStartDate is on or before the referring object's start date | Correct the formula effective date before load | |
| Formula text uses a database item | Valid only when the item is available to the formula type, required contexts are supported, the item is treated as read-only, and a required default is declared | Correct the item, context, or DEFAULT statement before load | |
| Formula text uses a flexfield database item | Valid only after the flexfield is deployed, its database items are generated, and dependent formulas are compiled or recompiled | Complete the flexfield database-item process before formula use | |
| A formula calls another formula | Valid only when the called formula exists, inputs and outputs use compatible types, recursion is absent, and the supported call-depth limit isn't exceeded | Correct the call contract before load | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Data file is FastFormula.dat and business object is FastFormula | Reject another file or business object | Prepare HDL | |
| Record action is MERGE | Reject an undocumented action | Prepare HDL | |
| METADATA and MERGE rows have the same ordered columns and delimiter count | Reject a malformed DAT file | Prepare HDL | |
| The developer-provided minimum create fields SourceSystemOwner, SourceSystemId, FormulaCode, FormulaTypeCode, FormulaName, and FormulaText are nonblank | Return the missing fields and stop | Prepare HDL create using the minimum contract | |
| EffectiveStartDate is present and no later than each referring object's start date | Reject an absent or incompatible effective date | Prepare HDL | |
| Formula text isn't embedded directly in FastFormula.dat | Reject direct formula source in the DAT row | Prepare HDL | |
| Formula text filename identifies one existing UTF-8 file under ClobFiles | Reject a missing, duplicate, absolute, traversing, or out-of-folder path | Prepare HDL | |
| FormulaText contains only a filename and the referenced file exists under ClobFiles | Reject direct formula text, a missing file, or a file outside ClobFiles | Prepare HDL | |
| FormulaId or GUID is supplied only for an existing record | Reject either identifier for a new record | Prepare HDL create | |
| FormulaCode is unchanged during update | Reject an attempted FormulaCode change | Prepare HDL update | |
| FormulaCode and FormulaTypeCode don't exceed 80 characters, FormulaName doesn't exceed 120, SourceSystemOwner doesn't exceed 30, SourceSystemId doesn't exceed 100, and Description doesn't exceed 240 | Return every overlength attribute | Prepare HDL | |
| SourceRefTableName is declared as METADATA context and isn't supplied as a row value | Reject a row value for SourceRefTableName | Prepare HDL with staging references | |
| SourceRef001 through SourceRef010 are used only as named staging references | Reject presenting source-reference values as application-persisted attributes | Prepare HDL with staging references | |
| ALIAS, DEFAULT, DEFAULT_DATA_VALUE, and INPUTS statements appear in a valid statement order | Return a compilation-readiness error | Validate or Prepare HDL | |
| Assignments don't write to database items and context assignment occurs only within CHANGE_CONTEXTS | Return a compilation-readiness error | Validate or Prepare HDL | |
| Variables are initialized and used with one compatible data type | Return a compilation-readiness error | Validate or Prepare HDL | |
| Numeric division can't use zero as the divisor and text results remain within documented limits | Return an execution-risk error | Validate or Prepare HDL | |
| Array access tests index existence and loop termination is reachable | Return an execution-risk error | Validate or Prepare HDL | |
| Formula-type-specific required inputs and returns are present and type-compatible | Return the missing or incompatible contract items | Validate or Prepare HDL | |
| FormulaName is nonblank | Return a validation error identifying FormulaName as required and stop before HDL preparation | Create, update, or import | |
| FormulaTypeCode, FormulaTypeId, or a Formula Type name or display value is nonblank | Return a validation error identifying Formula Type as required and stop before HDL preparation | Create, update, or import | resolve_fast_formula_type_reference |
| FormulaName matches the existing formula's FormulaName | Reject an attempted FormulaName change | Update | resolve_existing_fast_formula_for_update |
| The resolved FormulaTypeCode or FormulaTypeId matches the existing formula's formula-type identity | Reject an attempted Formula Type change | Update | resolve_existing_fast_formula_for_update |
| The developer-provided DAT generation contract applies instead of the earlier sample-derived minimum source-key contract | Require FormulaName as input; don't request FormulaCode, SourceSystemOwner, or SourceSystemId, and don't stop because those three values weren't supplied | Prepare HDL from provided input data | |
| FormulaCode exactly equals FormulaName for every generated record | Copy FormulaName exactly into FormulaCode without deriving, abbreviating, normalizing, or otherwise transforming it; reject a supplied FormulaCode that differs from FormulaName | Prepare HDL | |
| FormulaName doesn't exceed the 80-character FormulaCode limit when FormulaCode is copied from FormulaName | Return a validation error instead of truncating or transforming FormulaName | Prepare HDL | |
| SourceSystemOwner and SourceSystemId aren't populated | Omit both columns from the generated METADATA and MERGE rows, or leave both unpopulated when the selected DAT shape retains them | Prepare HDL | |
| Every populated DAT value is present in the source data or produced by an explicit documented transformation | Reject fabricated values and preserve supplied source values exactly except for the explicit FormulaName-to-FormulaCode copy | Prepare HDL | |
| Final DAT integrity verification confirms each FormulaCode equals its corresponding FormulaName and both source-system fields are absent or unpopulated | Stop and return every affected record before producing the final DAT file if any check fails | Prepare HDL | |
| Every generated FastFormula DAT record has nonblank FormulaTypeCode and LegislativeDataGroupName values | Reject the record before preview when either column is absent or blank; always populate both columns in the METADATA and MERGE rows | Prepare HDL | |
| Formula content and compilation custom actions use Content-Type application/vnd.oracle.adf.action+json | Stop before the action when the required content type is absent or different | Get formula content, submit compilation, or retrieve compile messages | |
| A formula custom-action body contains only the resolved formulaId and effectiveDate fields required by the supplied contract | Reject missing, blank, guessed, stale, or additional undocumented action fields | Get formula content, submit compilation, or retrieve compile messages | resolve_fast_formula_action_target |
| A submitCompileJob response contains result.formulaId, result.essJobId, result.essJobState, and result.effectiveDate | Classify an incomplete or malformed response as process failed and don't begin status polling | Compile formula | |

## Reference and LOV Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| A formula-type name or display value is supplied for the FormulaTypeId reference | Resolve exactly one matching FormulaTypeCode or FormulaTypeId before DAT preparation | Create, update, or import | resolve_fast_formula_type_reference |
| A Legislative Data Group name or display value is supplied for the LegislativeDataGroupId reference | Resolve exactly one matching LegislativeDataGroupId or supported reference form before DAT preparation | Create, update, or import for an LDG-scoped formula | resolve_legislative_data_group_reference |
| A reference code or ID is already supplied and valid | Use the supplied value directly without another lookup | Create, update, or import | |
| A reference name or display value returns no match | Return a validation error identifying the field and invalid supplied value | Any reference resolution | |
| A reference name or display value returns multiple matches | Return an ambiguity error and don't select automatically | Any reference resolution | |
| A name remains unresolved for a code-or-ID field | Reject the import field before preview | Create, update, or import | |
| A reference value repeats within the same operation | Reuse the operation-local resolved value and don't perform a duplicate lookup | Create, update, or import | |
| A predefined Yes/No LOV field receives a name or display value | Resolve exactly one YES_NO Meaning and use its LookupCode in the import field | Create, update, or import when target metadata defines the field as YES_NO | resolve_yes_no_lookup_code |
| A formula status field receives a name or display value | Resolve exactly one ORA_FORMULA_STATUS_VB Meaning and use its LookupCode in the import field | Create, update, or import when target metadata defines the field as formula status | resolve_formula_status_lookup_code |
| A lookup requires Fusion access and no session is active | Establish or refresh the configured authorized session before the read-only lookup | Any reference or LOV resolution | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.VALIDATE_INPUT | decision | 1 | validate_input | valid->FF.RESOLVE_DEPENDENCIES;invalid->FF.HANDLE_ERROR | none | stop | Always |

## Sources

- Developer-provided /scratch/share/FastFormulaAll.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormula.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Developer-provided standard reference and LOV instructions, received 2026-08-17.
- Developer-provided Fast Formula reference endpoint and session instructions, received 2026-08-17.
- Developer-provided Fast Formula field-level input validation instructions, received 2026-08-17.
- Developer-provided Fast Formula DAT name-to-code, source-system omission, and data-integrity instructions, received 2026-08-17.
- Developer-confirmed primary Fast Formula endpoint as the update comparison resolver, received 2026-08-18.
- Developer-provided mandatory FastFormula DAT population instruction for LegislativeDataGroupName and FormulaTypeCode, received 2026-08-18.
- Developer-provided persisted formula-content and formula-compilation custom-action contracts, received 2026-08-18.
- Oracle Fusion Cloud HCM, Example of Loading Fast Formula: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-fast-formula.html
- Oracle Fusion Cloud HCM, Overview of Using Formulas: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-using-formulas.html
- Oracle Fusion Cloud HCM, Overview of Writing Formulas: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-writing-formulas.html
- Oracle Fusion Cloud HCM, Overview of Using Fast Formula Components: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/overview-of-using-fast-formula-components.html
- Oracle Fusion Cloud HCM, Formula Statements: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-statements.html
- Oracle Fusion Cloud HCM, Formula Compilation Errors: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-compilation-errors.html
- Oracle Fusion Cloud HCM, Formula Execution Errors: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-execution-errors.html
- Oracle Fusion Cloud HCM, Formula Compilation: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-compilation.html
