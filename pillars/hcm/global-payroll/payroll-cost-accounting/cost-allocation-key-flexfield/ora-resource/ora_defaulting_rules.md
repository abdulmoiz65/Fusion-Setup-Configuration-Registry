# Cost Allocation Key Flexfield Defaulting Rules

Only documented task identity is fixed. No configuration property is inferred from a different structure, instance, row, or release-specific export example.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver | Evidence |
|---|---|---|---|---|---|
| KeyFlexfieldCode | COST | A package is authored for this exact task after the package contract is confirmed | No | resolve_fsm_package_contract | E1 |
| ApplicationId | 801 | A package is authored for this exact task after the package contract is confirmed | No | resolve_fsm_package_contract | E1 |
| Structure Delimiter | No default; preserve exported value or require an explicit design choice | A new or modified structure is authored | No | resolve_operation_record | E2 |
| EnabledFlag; DynamicCombinationCreationAllowed; ShorthandAliasEnabledFlag; RequiredFlag; DisplayFlag; BIEnabledFlag | No default; preserve an exported value or require an explicit supported value | A new or modified property is authored | No | resolve_operation_record | E1; E3 |
| DefaultType; DefaultValue; DefaultValueNumber; QueryRequiredType; RangeType | No default; use only a confirmed compatible value | The property is supplied | No | resolve_operation_record | E1; E4 |
| Audit attributes | Do not synthesize new values | New rows are authored | No | resolve_operation_record | E1; E5 |
| TreeCode | No default; blank remains no tree dependency | An instance segment is authored | No | resolve_operation_record | E1; E3 |

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | Observed values are not universal defaults |
| E2 | [Considerations for Managing Key Flexfields](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/considerations-for-managing-key-flexfields.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Delimiter choice remains design-specific |
| E3 | [Key Flexfield Structure Instances and Segment Instances](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/key-flexfield-structure-instances-and-segment-instances.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Exact CSV enum values remain TBD |
| E4 | [Flexfield Segment Properties](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oaext/flexfield-segment-properties.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Task-level RangeType enum remains TBD |
| E5 | [Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/25d/oafsm/export-and-import-csv-file-packages.html) | Public Oracle documentation | Confirmed | 25d, reviewed 2026-08-18 | Audit-field input behavior is task-specific |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_APPLY_DEFAULTS | step | 40 | apply_default | applied-or-not-needed->KFFCSV_ENFORCE_PACKAGE_DESIGN | KFFCSV_CHECK_DEPENDENCY_READINESS | stop | Dependencies are ready and a package is being authored or validated |
