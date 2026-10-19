# Payroll Time Definition Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parent create identity | TimeDefinitionCode, DefinitionName, DefinitionType, LegislativeDataGroupName | Stop before DAT construction | Supply all four nonblank values; never identify a record by DefinitionName alone | Parent create | resolve_legislative_data_group |
| Parent delete identity | TimeDefinitionCode or DefinitionName, plus LegislativeDataGroupName | Stop before DELETE construction | Resolve exactly one parent by supplied code or name plus LDG, derive the DAT code from exported ShortName, and never require TimeDefinitionId | Parent delete | resolve_payroll_time_definition |
| Usage assignment identity | Parent TimeDefinitionCode or DefinitionName, LegislativeDataGroupName, and UsageType | Stop before child MERGE construction | Resolve exactly one parent and derive child TimeDefinitionCode from exported ShortName; internal IDs are not user inputs | Assign usage | resolve_payroll_time_definition |
| Usage removal identity | Parent TimeDefinitionCode or DefinitionName, LegislativeDataGroupName, and UsageType | Stop before child DELETE construction | Resolve exactly one parent and derive child TimeDefinitionCode from exported ShortName; internal IDs are not user inputs | Remove usage | resolve_payroll_time_definition |
| Local task context | Active initialized project, exact Time Definitions catalog values, and nested task skill path | Stop only when an existing context is unsafe or conflicts | Resolve the existing row or bootstrap and schema-validate the missing local task-context.json without separate approval or an Oracle Run Book | Every task-routed HDL request | bootstrap_task_context |
| Static inputs | StartDate, positive NumberOfYears, and exactly one of PeriodType or PeriodTimeDefinitionCode | Stop before DAT construction | Supply the documented type-dependent fields in HDL date and number formats | DefinitionType unambiguously matches Static time definition | resolve_payroll_time_definition |
| User-defined date inputs | BaseTimeDefinitionCode and adjustment fields required by the selected rule | Stop before DAT construction | Resolve the base definition in the same LDG and reject self-reference | DefinitionType unambiguously matches User-defined date | resolve_payroll_time_definition |
| Time span inputs | Exactly one of PeriodType or PeriodTimeDefinitionCode and normally PeriodUnit | Stop before DAT construction | Supply the documented period basis and signed whole-number period count | DefinitionType unambiguously matches Time span | resolve_payroll_time_definition |
| Retrieval Date inputs | DatabaseItemCode | Stop before DAT construction | Supply a nonblank value and preserve it exactly for Fusion Data Loader validation | DefinitionType unambiguously matches Retrieval Date |  |
| Source-system identity | SourceSystemOwner and SourceSystemId together | Stop before DAT construction | Supply both fields or omit both | A source-system key is used |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Scalar normalization | Trim surrounding whitespace, then preserve supplied parent business values and UsageType without translating them to export encodings, lookup codes, or existing-row values | Every operation |  |
| DAT content safety | Reject any supplied value containing a pipe, carriage return, or line feed unless the live template supplies and validates an explicit escaping contract; name the offending field | Every DAT row |  |
| Parent create natural key | Apply the verified two-file task-export algorithm and require zero distinct parent GroupingKey candidates | Parent create | resolve_payroll_time_definition |
| Parent delete natural key | Apply the verified two-file task-export algorithm and require exactly one distinct parent GroupingKey candidate for supplied TimeDefinitionCode or DefinitionName plus LDG; emit the resolved parent ShortName as TimeDefinitionCode in the DAT | Parent delete | resolve_payroll_time_definition |
| Usage parent identity | Require exactly one parent candidate for supplied TimeDefinitionCode or DefinitionName plus LDG, then use exported ShortName as the child TimeDefinitionCode | Assign or remove usage | resolve_payroll_time_definition |
| Usage child identity | Join through parent-qualified ShortName and LDG, then match exact UsageType meaning; use the joined parent ShortName in HDL. An unqualified child export value equal to that parent's DefinitionName is a nonblocking display-name projection; assignment requires zero child candidates and removal requires exactly one | Assign or remove usage | resolve_payroll_time_definition |
| Recent successful HDL fallback | When a usable fresh export has zero parent or child candidates immediately after a create, require exact immutable parent-and-usage DAT plus successful terminal ProcessId evidence or authenticated exact read-back from the same target, task, and LDG. Reject preview-only, initiated-only, failed, unknown-status, cross-target, or conflicting evidence. On success retain the DAT TimeDefinitionCode and disclose task export visibility lag. | Assign or remove usage | resolve_recent_successful_payroll_time_definition |
| Natural-key DAT boundary | Parent DELETE uses TimeDefinitionCode and LegislativeDataGroupName only; child MERGE or DELETE uses TimeDefinitionCode, LegislativeDataGroupName, and UsageType only | Parent delete or usage child |  |
| Internal-ID privacy | Internal IDs may support resolution and impact checks but must not be required, substituted, or exposed in DAT, approval display, or routine output when a verified natural key is sufficient | Parent delete or usage child |  |
| Duplicate input keys | Reject duplicate parent keys and duplicate child keys within the same request | Bulk operation |  |
| LDG scope | Resolve exactly one LDG and require every supplied representation and reference to agree in that LDG | Every row | resolve_legislative_data_group |
| Type guidance | Apply documented type-dependent missing-field, blank-field, and XOR checks only when DefinitionType unambiguously matches a documented type; unfamiliar supplied values are preserved | Parent create |  |
| Period basis | PeriodType and PeriodTimeDefinitionCode are mutually exclusive; documented Static and Time span shapes require exactly one; documented Retrieval Date requires both blank | Recognized documented type | resolve_payroll_time_definition |
| Dates and numbers | Validate supplied StartDate as YYYY/MM/DD; validate NumberOfYears as a positive whole number and PeriodUnit and DayAdjustment as signed whole numbers when used | A corresponding value is supplied |  |
| References and cycles | Resolve BaseTimeDefinitionCode and PeriodTimeDefinitionCode in the same LDG against exported DefinitionName; reject missing, ambiguous, cross-LDG, self, and direct in-request cyclic references and never rewrite the supplied reference to ShortName | BaseTimeDefinitionCode or PeriodTimeDefinitionCode is supplied | resolve_payroll_time_definition |
| Create identifiers | Omit TimeDefinitionId and GUID for a new parent | Parent create |  |
| Parent updateability | Reject a requested rename or change to parent type, date, period, base, database-item, or other registered parent business attributes; never emulate through delete and recreate | Parent business-field update |  |
| Usage meaning | Require a nonblank DAT-safe value, preserve its trimmed meaning exactly, and do not require a local allowlist or substitute UsageTypeCode | Assign or remove usage |  |
| Bulk mapping and order | Map every input column to a registered attribute, normalize parent and child keys separately, place parent MERGE before child MERGE, emit child DELETE only when retaining its parent, emit only one parent DELETE for complete parent deletion, topologically order referenced parents, and renew approval if scope changes | Bulk import | resolve_payroll_time_definition |
| Immutable approval | Recompute the preview and obtain fresh approval whenever any normalized row, DAT byte, environment, operation, or batch scope changes | A preview already exists |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Local task context is absent and exact project and task metadata are known | Bootstrap-ready local state | Create, persist, and schema-validate the minimal task-context.json, then continue in the same run without separate approval or a Fusion call | bootstrap_task_context |
| Existing local task context conflicts with project, catalog, or nested skill metadata | Unsafe project context | Stop and identify the conflicting field; never overwrite silently | bootstrap_task_context |
| LDG does not resolve uniquely | Missing legislative context | Stop and request one exact LDG identity | resolve_legislative_data_group |
| Fresh export is usable and returns zero parent candidates | Parent create identity is available | Continue through DAT construction, live schema validation, immutable preview, and one approval request in the same run | resolve_payroll_time_definition |
| Fresh export returns exactly one parent and zero exact usage children | Usage assignment is available | Continue with natural-key child MERGE and all remaining preflights | resolve_payroll_time_definition |
| Fresh export returns exactly one parent and one exact usage child | Usage removal is available | Continue with natural-key child DELETE and all remaining preflights | resolve_payroll_time_definition |
| Joined usage unqualified TimeDefinitionCode equals the same parent DefinitionName | Usage export display-name projection | Disclose the nonblocking warning, retain joined parent ShortName as the HDL key, and continue with normal child validation, preview, and approval | resolve_payroll_time_definition |
| Fresh export has zero parent or child candidates immediately after a create and qualified successful HDL evidence is exact | Export visibility lag | Retain parent and child natural-key mapping from the successful DAT, disclose the warning, and continue with the child DAT, live schema validation, immutable preview, and one approval request | resolve_recent_successful_payroll_time_definition |
| Fresh export has zero parent or child candidates but successful terminal evidence or authenticated exact read-back is absent, failed, unknown, cross-target, or conflicting | Unverified child identity | Stop; do not treat the zero export as proof of absence and do not construct a child DAT | resolve_recent_successful_payroll_time_definition |
| Fresh export returns exactly one parent and zero parent rows referencing it through BaseTimeDefinitionCode or PeriodTimeDefinitionCode | Parent deletion is available | Continue regardless of usage count with one natural-key parent DELETE, live schema validation, immutable preview including exact cascade usage meanings, disclosed nonblocking limitations, and one approval request | assess_payroll_time_definition_delete_impact |
| Parent delete target has exported usage rows | Cascade-delete impact | Record every exact UsageType meaning in the destructive preview and continue; do not construct separate child DELETE rows for complete parent deletion | assess_payroll_time_definition_delete_impact |
| Parent delete target has exported base or period dependents | Verified delete dependency | Stop and list each dependent natural key and reference field | assess_payroll_time_definition_delete_impact |
| Parent delete ownership or unrelated cross-consumer resolver is unavailable | Nonblocking delete limitation | Record the unresolved limitation, disclose it in the preview, and let Fusion Data Loader enforce referential integrity after approval | assess_payroll_time_definition_delete_impact |
| Requested usage is already assigned | No-op duplicate | Report it and do not upload a redundant child MERGE | resolve_payroll_time_definition |
| Requested usage removal target is absent | No-op missing target | Report it and do not upload child DELETE | resolve_payroll_time_definition |
| Export is COMPLETED_WARNINGS or optional warning details are unavailable without a relevant failure | Nonblocking evidence warning | Disclose the warning and continue when required files, columns, joins, and cardinality are usable | resolve_payroll_time_definition |
| Export is failed, truncated, structurally unusable, inconsistent, or explicitly warns about the requested key or LDG | Unreliable identity evidence | Block; do not fall back to public LOV, SQL, fuzzy matching, or first-row selection | resolve_payroll_time_definition |
| Direct business value or UsageType is absent from examples, exports, or lookup evidence | Fusion-authoritative value | Preserve the trimmed value in the DAT and let Fusion validate it after approval |  |
| Parent business-field update is requested | Unsupported update | Explain that registered parent fields are not updatable and do not delete and recreate |  |

## DAT Construction Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent create instruction | Emit UTF-8 METADATA and MERGE rows using component PayrollTimeDefinition and normalized supplied values | Parent create |  |
| Parent delete instruction | Emit METADATA with TimeDefinitionCode and LegislativeDataGroupName followed by one DELETE with those natural-key values; usage rows are cascade-deleted and must not produce child DELETE rows for complete parent deletion | Parent delete | resolve_payroll_time_definition |
| Usage assignment instruction | Emit METADATA with TimeDefinitionCode, LegislativeDataGroupName, and UsageType followed by MERGE for TimeDefinitionUsage | Assign usage | resolve_payroll_time_definition |
| Usage removal instruction | Emit the same child natural-key METADATA followed by DELETE for TimeDefinitionUsage | Remove usage | resolve_payroll_time_definition |
| Registered object | Validate the exact immutable PayrollTimeDefinition.dat through core.data-loader against PayrollTimeDefinition and its applicable parent or child component | Parent create, parent delete, usage assignment, or usage removal | validate_payroll_time_definition_dat |
| Approval continuity | DAT construction is intermediate; continue through live BO/template validation, task-rule preview, fingerprinting, and the approval request | Every supported mutation |  |

Parent create header:

```text
METADATA|PayrollTimeDefinition|TimeDefinitionCode|DefinitionName|StartDate|DayAdjustment|DefinitionType|NumberOfYears|PeriodType|PeriodUnit|BaseTimeDefinitionCode|DatabaseItemCode|PeriodTimeDefinitionCode|AdjustmentType|LegislativeDataGroupName
```

Parent delete shape:

```text
METADATA|PayrollTimeDefinition|TimeDefinitionCode|LegislativeDataGroupName
DELETE|PayrollTimeDefinition|<TimeDefinitionCode>|<LegislativeDataGroupName>
```

Usage child shapes:

```text
METADATA|TimeDefinitionUsage|TimeDefinitionCode|LegislativeDataGroupName|UsageType
MERGE|TimeDefinitionUsage|<TimeDefinitionCode>|<LegislativeDataGroupName>|<UsageType meaning>
DELETE|TimeDefinitionUsage|<TimeDefinitionCode>|<LegislativeDataGroupName>|<UsageType meaning>
```

## Unresolved Contracts

Existing-environment cycle traversal, field maximum lengths, target-specific character patterns, complete business-value lists, localization, and downstream parent-delete dependency sources beyond the verified task export remain **TBD**. Unavailable parent-delete ownership and unrelated cross-consumer sources are nonblocking preview limitations under the supplied source; other unresolved contracts block only operations that require them. Parent business-field update is unsupported; usage-child discriminator, template, operations, natural key, and pass-through meaning are verified and are not TBD.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TD.VALIDATE_INPUT | step | 10 | validate_input | valid->TD.BOOTSTRAP_CONTEXT;invalid->TD.ERROR_HANDLE;unsupported->TD.ERROR_HANDLE | none | stop | Every PayrollTimeDefinition parent or TimeDefinitionUsage child request |
| TD.SELECT_OPERATION | decision | 50 | evaluate_result | create->TD.CREATE_DEPENDENCY_READY;delete->TD.DELETE_IMPACT_READY;assign_usage->TD.USAGE_ASSIGN_READY;remove_usage->TD.USAGE_REMOVE_READY;parent_update->TD.ERROR_HANDLE;invalid->TD.ERROR_HANDLE | TD.RESOLVE_IDENTITY | stop | Select parent create, parent delete, usage assignment, usage removal, or unsupported parent update after identity resolution |
| TD.VALIDATE_CREATE_DAT | step | 120 | validate_input | valid->TD.CREATE_PREVIEW;invalid->TD.ERROR_HANDLE | TD.VALIDATE_CREATE_SCHEMA | stop | Validate exact parent-create DAT content, preserved values, and fingerprint |
| TD.VALIDATE_DELETE_DAT | step | 125 | validate_input | valid->TD.DELETE_PREVIEW;invalid->TD.ERROR_HANDLE | TD.VALIDATE_DELETE_SCHEMA | stop | Validate complete parent deletion contains one parent DELETE with only its natural key and no child DELETE rows |
| TD.VALIDATE_USAGE_ASSIGN_DAT | step | 130 | validate_input | valid->TD.USAGE_ASSIGN_PREVIEW;invalid->TD.ERROR_HANDLE | TD.VALIDATE_USAGE_ASSIGN_SCHEMA | stop | Validate exact usage MERGE contains only the child natural key and preserved meaning |
| TD.VALIDATE_USAGE_REMOVE_DAT | step | 135 | validate_input | valid->TD.USAGE_REMOVE_PREVIEW;invalid->TD.ERROR_HANDLE | TD.VALIDATE_USAGE_REMOVE_SCHEMA | stop | Validate exact usage DELETE contains only the child natural key and preserved meaning |
