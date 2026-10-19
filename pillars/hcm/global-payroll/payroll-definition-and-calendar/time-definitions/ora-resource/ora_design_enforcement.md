# Payroll Time Definition Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve representation and route | Keep the nested task, HDL mode, PayrollTimeDefinition BO, and core.data-loader route; never substitute direct mutation REST. |
| 2 | Bootstrap local context | Resolve or safely create exact local task context before task-routed validation without separate approval. |
| 3 | Preserve supplied values | Trim and retain parent business values and UsageType meanings; examples, export codes, and lookup codes are not substitution sources or allowlists. |
| 4 | Resolve true identities | Resolve LDG, parent natural key, optional child natural key, and base or period references exactly in the selected LDG. |
| 5 | Construct deterministic DAT | Build parent MERGE, parent natural-key DELETE, child natural-key MERGE, or child natural-key DELETE without internal IDs. |
| 6 | Complete continuous preflight | Continue from DAT construction through live schema validation, task-rule preview, fingerprinting, authorization checks, and one approval request in the same run. |
| 7 | Protect target configuration | Release only unchanged approved DAT once through core.data-loader and distinguish initiation from later status or read-back. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every supported mutation | Blocker | verify_authorization_ldg_scope | Route is not core.data-loader HDL with PayrollTimeDefinition, target or LDG access fails, or approval is not bound to exact preview | Complete all read-only preflights and request one approval for immutable DAT | No |
| Every task-routed request | Blocker | bootstrap_task_context | Existing task context conflicts with active project, catalog task, nested skill, or sequence | Stop and disclose the field; bootstrap only a missing safe context | No |
| Parent create | Blocker | resolve_payroll_time_definition | Required identity is missing, export evidence is unusable or explicitly relevant, parent key exists, a true reference fails, or TimeDefinitionId or GUID is supplied | Preserve supplied values and build MERGE only after zero-candidate and reference checks | No |
| Parent create business values | Blocker |  | A direct value is altered, translated, replaced, or rejected only because unfamiliar or absent from lookup evidence | Preserve the trimmed value and let Fusion Data Loader validate it after approval | No |
| Parent delete identity | Blocker | resolve_payroll_time_definition | Supplied TimeDefinitionCode or DefinitionName plus LDG does not resolve once, both supplied forms resolve different GroupingKeys, or DELETE does not use the resolved ShortName | Resolve parent identity first, then use the derived TimeDefinitionCode and LegislativeDataGroupName only | No |
| Parent delete impact | Blocker | assess_payroll_time_definition_delete_impact | The fresh export shows a parent whose BaseTimeDefinitionCode or PeriodTimeDefinitionCode equals the target DefinitionName in the same LDG, or an explicitly exposed ownership field marks the target delivered or protected | List exact usage meanings as cascade-delete impact without requiring child DELETE rows. Correct dependent definitions or stop for an explicit protected marker. Disclose unavailable ownership and cross-consumer resolvers as nonblocking warnings and let Fusion Data Loader enforce referential integrity. | No |
| Parent update | Blocker |  | A rename or any parent business-field change is requested | Return unsupported update; never emulate through delete and recreate | No |
| Usage assignment | Blocker | resolve_payroll_time_definition | Parent count is not one, exact joined-parent child count is not zero, UsageType is blank or unsafe, child MERGE uses IDs or UsageTypeCode, or the unqualified child export value identifies a different or unreconcilable parent | Use joined parent ShortName as TimeDefinitionCode with LegislativeDataGroupName and preserved UsageType meaning; a value equal to the joined parent DefinitionName is a nonblocking display-name projection | No |
| Usage removal | Blocker | resolve_payroll_time_definition | Parent count is not one, exact joined-parent child count is not one, child DELETE uses IDs or UsageTypeCode, or the unqualified child export value identifies a different or unreconcilable parent | Use the exact practical child natural key derived from the joined parent ShortName; disclose but do not block an unqualified value equal to that parent DefinitionName | No |
| Usage export-lag fallback | Blocker | resolve_recent_successful_payroll_time_definition | A zero-row export is used without exact immutable DAT plus successful terminal ProcessId evidence or authenticated exact read-back from the same target, task, and LDG; or any evidence is preview-only, initiated-only, failed, unknown-status, cross-target, or conflicting | Treat zero rows as a visibility-lag warning only after qualified successful evidence proves the exact parent and child natural key | No |
| Usage meaning | Blocker |  | Supplied meaning is rejected for lacking local evidence or replaced by an underlying lookup code | Preserve any nonblank DAT-safe trimmed meaning and let Fusion validate it | No |
| DAT continuity | Blocker | validate_payroll_time_definition_dat | DAT or project-artifact creation is treated as terminal before schema validation, preview, fingerprint, and approval | Continue through the branch approval node in the same run | No |
| Internal-ID privacy | Blocker | validate_payroll_time_definition_dat | TimeDefinitionId or TimeDefinitionUsageId appears in natural-key DAT, approval display, downloadable preview, or routine output | Remove internal IDs and use the verified natural key | No |
| Recognized documented type | Blocker |  | Required field, blank rule, date/number shape, or period-basis XOR rule fails | Correct the structural issue without creating a closed type allowlist | No |
| Unrecognized definition type | Blocker |  | Value is blocked only because not listed in examples | Preserve it and let Fusion validate it | Yes |
| Bulk import | Blocker | resolve_payroll_time_definition | Duplicate or cyclic keys, cross-LDG references, unmapped columns, wrong parent-child order, or changed approved scope | Correct and order rows, then renew approval for changed scope | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| bootstrap_task_context | Before task-routed validation | TaskContextPath, Sequence, TaskName, TaskCode, SkillPath, Offering, FunctionalArea | ora_reference_lookups.md |
| resolve_legislative_data_group | Every request | LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode | ora_reference_lookups.md |
| resolve_payroll_time_definition | Every parent/child operation and base or period reference | ParentCandidateCount, ChildCandidateCount, GroupingKey, parent and child natural-key values, reference codes | ora_reference_lookups.md |
| resolve_recent_successful_payroll_time_definition | Usage assignment or removal after zero export candidates immediately following a create | TimeDefinitionCode, DefinitionName, LegislativeDataGroupName, UsageType, SuccessfulProcessId or AuthenticatedReadBack, ExportVisibilityLagWarning | ora_reference_lookups.md |
| assess_payroll_time_definition_delete_impact | Parent delete | UsageCount, CascadeUsageMeanings, DependentDefinitionCount, DeliveredOwnershipCheckAvailability, ExplicitProtectedResult, DeleteImpactWarnings, DeleteImpactSummary | ora_reference_lookups.md |
| validate_payroll_time_definition_dat | After deterministic DAT construction | BusinessObject, DatFilename, Operation, Component, SourceFingerprint, SchemaValidationResult | ora_reference_lookups.md |
| verify_authorization_ldg_scope | Immediately before approved loader release | AuthorizedTarget, Operation, LegislativeDataGroupName, PreviewFingerprint, ApprovalEvidence | ora_reference_lookups.md |

## Registered Contract

| Topic | Captured Rule |
|---|---|
| Registered BO | Seeded DB ADF_VO PayrollTimeDefinition, processing order 6600, DAT filename PayrollTimeDefinition.dat, operations MERGE and DELETE. |
| PayrollTimeDefinitionVO key mapping | TimeDefinitionCode persists to ShortName and DefinitionName persists separately. BaseTimeDefinitionCode and PeriodTimeDefinitionCode resolve against DefinitionName in the same LDG. |
| TimeDefinitionUsageVO key mapping | Child TimeDefinitionCode maps to the parent ShortName; LegislativeDataGroupName and UsageType complete the child natural key. |
| Parent create key | TimeDefinitionCode persists as ShortName plus LegislativeDataGroupName; DefinitionName persists separately as the user-facing name. |
| Parent delete key | Resolve supplied code against ShortName or supplied DefinitionName against DefinitionName, then emit derived ShortName as TimeDefinitionCode plus LegislativeDataGroupName only; never require, substitute, or expose TimeDefinitionId. |
| Parent delete usage cascade | Existing TimeDefinitionUsage rows do not block complete parent deletion. Disclose every exact UsageType meaning as cascade-delete impact and emit only the parent natural-key DELETE, with no child DELETE rows. |
| Parent updateability | Registered parent business attributes are not updatable; usage maintenance is a child operation, not a parent-field edit. |
| Child component | TimeDefinitionUsage with registered MERGE and DELETE support. |
| Child natural key | TimeDefinitionCode plus LegislativeDataGroupName plus UsageType; internal IDs are optional private evidence only. |
| UsageType handling | Preserve the trimmed business meaning supplied by the user; never substitute UsageTypeCode. Balance Retrieval is an example, not a default or allowlist. |
| Task-export identity | Join usage parent ShortName and LDG to parent ShortName and LDG. Resolve supplied code by ShortName, supplied name by DefinitionName, deduplicate parents by GroupingKey, derive canonical HDL code from ShortName, and evaluate child by joined parent plus exact UsageType. If unqualified usage TimeDefinitionCode equals the same joined parent DefinitionName, disclose display-name projection and retain ShortName for HDL; only unreconcilable or cross-parent mismatch blocks. Base and period reference values resolve by DefinitionName, not ShortName. |
| Recent successful HDL fallback | For a usage operation only, a usable zero-row export immediately after create may yield to exact immutable DAT plus successful terminal ProcessId evidence, or authenticated exact read-back, from the same target/task/LDG. Reuse only the proven code and child key, disclose task export visibility lag, and never accept preview-only, initiated-only, failed, unknown-status, cross-target, or conflicting evidence. |
| Warning boundary | COMPLETED_WARNINGS and unavailable optional details are disclosed but nonblocking unless failed, truncated, unusable, inconsistent, or explicitly relevant. |
| Execution boundary | DAT construction, schema validation, preview, and approval are continuous. Submit unchanged approved bytes once through core.data-loader; later status/read-back is separately requested. |

## Operation-Scoped Readiness

Parent create is ready for preview after basic inputs, safe DAT, LDG/reference resolution, zero ShortName candidates, live BO validation, and task-rule preview. Usage assignment/removal are ready after exact parent/child cardinality and child schema validation, with child TimeDefinitionCode derived from parent ShortName. Parent business-field update is unsupported. Parent delete natural-key syntax is verified and is ready for preview after one exact parent resolved by code or DefinitionName, zero exported base or period dependents whose reference value equals the target DefinitionName, and no explicitly exposed protected marker, regardless of usage count. Exact usage meanings are disclosed as cascade-delete impact, and no child DELETE rows are emitted for complete parent deletion. Delivered ownership and unrelated balance, event, element, and other cross-consumer resolvers remain **TBD** when unavailable, but the source makes those gaps nonblocking preview warnings and assigns authoritative referential-integrity validation to Fusion Data Loader after approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TD.BUILD_CREATE_DAT | step | 80 | design_enforcement | built->TD.VALIDATE_CREATE_SCHEMA;blocked->TD.ERROR_HANDLE | TD.CREATE_DEPENDENCY_READY | stop | Construct parent MERGE from preserved normalized supplied values and continue preflight |
| TD.BUILD_DELETE_DAT | step | 85 | design_enforcement | built->TD.VALIDATE_DELETE_SCHEMA;blocked->TD.ERROR_HANDLE | TD.DELETE_IMPACT_READY | stop | Construct one parent natural-key DELETE without TimeDefinitionId or child DELETE rows and continue preflight |
| TD.BUILD_USAGE_ASSIGN_DAT | step | 90 | design_enforcement | built->TD.VALIDATE_USAGE_ASSIGN_SCHEMA;blocked->TD.ERROR_HANDLE | TD.USAGE_ASSIGN_READY | stop | Construct TimeDefinitionUsage MERGE from parent code, LDG, and preserved UsageType meaning |
| TD.BUILD_USAGE_REMOVE_DAT | step | 95 | design_enforcement | built->TD.VALIDATE_USAGE_REMOVE_SCHEMA;blocked->TD.ERROR_HANDLE | TD.USAGE_REMOVE_READY | stop | Construct TimeDefinitionUsage DELETE from parent code, LDG, and preserved UsageType meaning |
