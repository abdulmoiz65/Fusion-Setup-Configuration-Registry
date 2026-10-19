# Payroll Costing Value Sets Input Validation

This resource validates only the task-specific Functional Setup Manager (FSM) CSV contract for `ORA_PAY_PAYROLL_COSTING_VALUE_SETS`. Export, import submission, approval, and generic reference-data processing remain owned by the task's declared shared workflows.

## Confirmed Task CSV Contract

| Contract Item | Required Value | Evidence |
|---|---|---|
| Task code | ORA_PAY_PAYROLL_COSTING_VALUE_SETS | SUP-REQ task contract and supplied package metadata excerpt |
| Task identity before import | ObjectShortName = ORA_PAY_PAYROLL_COSTING_VALUE_SETS; ObjectType = TASK; CreatedByFlow = TASK_CSV_SERVICE | TARGET-EXPORT-300103767070301 observed target package metadata on 2026-08-19 |
| Root business object | FND_APP_FLEX_VALUE_SET | SUP-REQ supplied ASM_SETUP_CSV_METADATA.xml evidence |
| Task scope | moduleType = LBA; moduleKey = HcmPayCostTop; mode = search | SUP-REQ supplied ASM_SETUP_CSV_METADATA.xml evidence |
| Service metadata | oracle.apps.fnd.applcore.flex.webservice.ValueSetWS; BatchSize = 500 | SUP-REQ supplied ASM_SETUP_CSV_METADATA.xml evidence for release 11.13.26.10.0 |
| Supported setup-data route | Task-level FSM CSV export, template export, package inspection, validation, import, and post-import verification through the declared shared workflows | Task SKILL.md and OHC-FSM-CSV |
| Excluded routes | Direct Value Set REST mutation, HDL, transactional payroll costing, alternate related-value import, XML, and generic loaders | SUP-REQ scope boundary |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Sanitized operation record | Task code; target environment; package identity; package release; root business object; module scope; applicable ModuleId; applicable CSV files; affected ValueSetCode values; requested behavior; applicable Rule IDs; dependency result; import result; post-import result; redeployment result when applicable | Block the task-specific package handoff | Supply the missing sanitized operational evidence without credentials, tokens, cookies, or session identifiers | Every task-level export, authoring, validation, import, or verification request | |
| Package task identity | ObjectShortName; ObjectType; CreatedByFlow; BusinessObjectShortName; moduleType; moduleKey | Block the package | Inspect ASM_SETUP_CSV_METADATA.xml and require the confirmed exact values | Every import and package-validation request | inspect_task_csv_package_metadata |
| Package hierarchy and schema | Package release and all six named CSV files with their exact template headers | Block the package | Re-export the template for the target release or repair the package without deleting a header-only file | Every authoring, validation, or import request | inspect_task_csv_package_metadata |
| Root Value Set authoring input | ValueSetCode; target-evidence-backed ModuleId; ValueSetIdentifier when the confirmed target contract requires it; requested validation model; requested data type and subtype; requested property changes | Block the authoring request | Provide the exact business values and confirmed target evidence; do not derive ValueSetIdentifier | Create or modify a root Value Set row | verify_target_module_evidence |
| Value-row input | Parent ValueSetCode; datatype-compatible value field; EnabledFlag when supplied; active dates when supplied | Block the affected value row | Provide a resolvable parent and a value representation compatible with the parent Value Set | Create, update, enable, or disable a maintained value | resolve_parent_value_set_reference |
| Related Value Set input | Both Value Set codes; relationship state; mapped values when creating a relationship | Block the relationship | Provide two eligible Independent Value Sets and complete the mappings before enabling a new relationship | Create, update, enable, or disable a related Value Set relationship | resolve_related_value_pair |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The package metadata identifies another task, object type, flow, root business object, module type, or module key | Blocked | Stop; obtain a package exported for this exact task and scope | inspect_task_csv_package_metadata |
| A new or modified root Value Set is requested and the target ModuleId is not corroborated for the target environment and release | Blocked | Stop; obtain the successful target-reference validation result before authoring | verify_target_module_evidence |
| A dependent or subset model refers to an Independent parent | Ready only when the parent is resolved by the package or validated target evidence | Preserve the exact parent reference; stop on an unresolved or cyclic dependency | resolve_parent_value_set_reference |
| A Table validation model is requested | Ready only when source metadata is validated by the declared reference-data workflow | Preserve the confirmed table contract; stop rather than inventing SQL or a table representation | verify_table_validation_source_evidence |
| A related relationship or mapping is requested | Ready only when both members and every mapped value resolve and the pair orientation is confirmed for this task contract | Keep a new relationship disabled until mappings are complete; stop on unresolved orientation | resolve_related_value_pair |
| A security-enabled or protected Value Set is affected | Ready only when the target security and protection evidence permits the requested behavior | Stop a protected mutation; do not synthesize a security object name | verify_value_set_security_evidence |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ValueSetCode is present and unique in the applicable target scope | Block a missing or duplicate create identity; never use Description as identity | Create a root Value Set | verify_target_module_evidence |
| ValueSetIdentifier is explicitly supplied from confirmed evidence when the target contract needs it | Block a guessed or code-derived identifier | Root row contains ValueSetIdentifier | |
| ModuleId is target-environment evidence, not an unverified copy of the observed release value | Block authoring until corroborated target evidence is available | Create or modify a root Value Set | verify_target_module_evidence |
| Independent UI validation is represented by INDEP only when Independent was explicitly requested | Accept INDEP for that confirmed mapping; block another unconfirmed stored validation code | ValidationType is supplied | |
| Character UI data type is represented by VARCHAR2 and Text subtype by TEXT only when those meanings were explicitly requested | Accept the confirmed pair; block an unconfirmed stored data-type or subtype code | ValueDataType or ValueSubtype is supplied | |
| MaximumLength is a positive value compatible with the selected confirmed data type | Block an absent, nonpositive, or incompatible length | MaximumLength is supplied or required by the confirmed model | |
| Precision and Scale are supplied only for a compatible numeric definition | Block incompatible numeric attributes | Precision or Scale is supplied | |
| Only datatype-compatible minimum and maximum attributes are populated | Block conflicting or incompatible typed range fields | Any MinimumValue or MaximumValue field is supplied | |
| Flags and date values preserve the target template representation | Block an unconfirmed flag encoding or invalid date representation; preserve the exported date format | A flag or date is supplied | |
| Each child value references exactly one parent ValueSetCode and uses a value field compatible with the parent data type | Block the child row | A Value Set Values row is supplied | resolve_parent_value_set_reference |
| EndDateActive is not earlier than StartDateActive | Block the affected value row | Both active dates are supplied | |
| Audit fields are not synthesized as business data | Block a user-authored CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, or LastUpdateLogin value unless target evidence explicitly requires it | Any audit field is changed | |
| Table validation includes valid confirmed source metadata and is not combined with invented user-maintained list behavior | Block the authoring request | A validation-table row is supplied | verify_table_validation_source_evidence |
| Validation View Object authoring uses a confirmed task-level contract | Block the authoring request while the contract remains unconfirmed | A validation-view-object row is supplied | |
| Related Value Set rows retain the confirmed pair orientation and referenced values exist in their respective members | Block the relationship or mapping | A related Set or related-value row is supplied | resolve_related_value_pair |
| No operation treats an omitted record as a delete | Block the request | A requested operation relies on removing a CSV row or omitting it from the package | |

## Confirmed Stored-Code Mappings

| Functional UI Meaning | Stored CSV Value | Evidence Status | Safe Use |
|---|---|---|---|
| Independent validation | INDEP | Observed in Payroll Costing task export, release 11.13.26.10.0 | Only for an explicit Independent request |
| Character data type | VARCHAR2 | Observed in Payroll Costing task export, release 11.13.26.10.0 | Only for an explicit Character request |
| Text subtype | TEXT | Observed in Payroll Costing task export, release 11.13.26.10.0 | Only for an explicit Text request |

## Confirmed Six-File Template Schema

| Node | CSV File | Exact Header | Evidence |
|---|---|---|---|
| 1 | FND_APP_FLEX_VALUE_SET.csv | ValueSetCode; ModuleId; ValueSetIdentifier; Description; ValidationType; ValueDataType; ValueSubtype; MaximumLength; Precision; Scale; UppercaseOnlyFlag; ZeroFillFlag; SecurityEnabledFlag; DataSecurityObjectName; MinimumValue; MinimumValueNumber; MinimumValueDate; MinimumValueTimestamp; MaximumValue; MaximumValueNumber; MaximumValueDate; MaximumValueTimestamp; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin; IndependentValueSetCode | SUP-REQ template and normal-export excerpt |
| 2 | ORA_FND_APP_FLEX_VALUE_SET_VALUE.csv | FND_APP_FLEX_VALUE_SET.ValueSetCode; Value; IndependentValue; IndependentValueNumber; IndependentValueDate; IndependentValueTimestamp; ValueNumber; ValueDate; ValueTimestamp; TranslatedValue; Description; EnabledFlag; StartDateActive; EndDateActive; SummaryFlag; FlexValueAttribute1; FlexValueAttribute2; FlexValueAttribute3; FlexValueAttribute4; FlexValueAttribute5; FlexValueAttribute6; SortOrder; ExternalDataSource; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin | SUP-REQ template and normal-export excerpt |
| 3 | ORA_FND_APP_FLEX_VALUE_SET_VALIDATION_TABLE.csv | FND_APP_FLEX_VALUE_SET.ValueSetCode; FromClause; WhereClause; OrderByClause; ValueColumnName; IdColumnName; DescriptionColumnName; EnabledFlagColumnName; StartDateColumnName; EndDateColumnName; ValueAttributesTableAlias; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin | SUP-REQ template and normal-export excerpt |
| 4 | ORA_APPLICATION_FLEXFIELD_VALUE_SET_VALIDATION_VIEW_OBJECT.csv | FND_APP_FLEX_VALUE_SET.ValueSetCode; ViewObjectName; ValueAttributeName; ValueAttributeType; ValueAttributeLength; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin | SUP-REQ template and normal-export excerpt |
| 5 | ORA_APPLICATION_FLEXFIELD_RELATED_VALUE_SET.csv | FND_APP_FLEX_VALUE_SET.ValueSetCode; ValueSetCode1; EnabledFlag; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin | SUP-REQ template and normal-export excerpt |
| 6 | ORA_APPLICATION_FLEXFIELD_RELATED_VALUE_SET_VALUE.csv | FND_APP_FLEX_VALUE_SET.ValueSetCode; ORA_APPLICATION_FLEXFIELD_RELATED_VALUE_SET.ValueSetCode1; Value1; Value2; EnabledFlag; CreationDate; CreatedBy; LastUpdateDate; LastUpdatedBy; LastUpdateLogin | SUP-REQ template and normal-export excerpt |

The semicolon-separated display above preserves the supplied column order. The actual CSV header must use the exact comma-separated header exported for the target package release.

## Known Limitations and TBD Items

| Item | Status | Runtime Treatment | Evidence |
|---|---|---|---|
| Stored CSV code for Format Only, Dependent, Subset, and Table validation | TBD | Do not author or normalize the stored code until target metadata or authoritative task evidence confirms it | SUP-REQ evidence matrix |
| Stored CSV code for Number, Date, Date Time, and additional subtypes | TBD | Do not author or normalize the stored code | SUP-REQ evidence matrix |
| Requiredness and mutability of every root and child attribute | TBD | Preserve target-export behavior; block a requested change not confirmed for the target schema | SUP-REQ limitations |
| Validation View Object row authoring semantics | TBD | Keep the confirmed file schema, but block row authoring | SUP-REQ limitations |
| Related Value Set pair orientation in this FSM CSV contract | TBD | Do not infer or swap Value1 and Value2 | SUP-REQ limitations |
| Delete contract for task-level CSV | TBD | Do not offer deletion by row omission or another substitute route | SUP-REQ and OHC-FSM-CSV |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| PCVS.VALIDATE_PACKAGE | step | 1 | validate_input | passed->PCVS.CHECK_DEPENDENCIES;failed->PCVS.FAILED | none | stop | Every task-level CSV package, authoring, import, or verification request | |
