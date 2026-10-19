# Cost Allocation Key Flexfield CSV Input Validation

This resource validates task-level Functional Setup Manager CSV packages for the predefined Payroll Cost Allocation Key Flexfield. It does not authorize an import or a direct flexfield mutation.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver | Evidence |
|---|---|---|---|---|---|---|
| Task package identity | TaskCode; ObjectType; CreatedByFlow; package identity; package release | Block package authoring or import | Obtain the package metadata and retain it in the sanitized operation record | Every export inspection, authoring, validation, or import | resolve_fsm_package_contract | E1; E2 |
| Cost Allocation KFF root | KeyFlexfieldCode=COST; ApplicationId=801 in every applicable root or parent-reference row | Block | Correct the package to the confirmed task root; do not create another root | Every package | resolve_fsm_package_contract | E1 |
| Complete task package | ASM_SETUP_CSV_METADATA.xml and all seven confirmed CSV files with exact template headers | Block | Re-export the task template or restore the missing file with its header | Every authoring or import package | resolve_fsm_package_contract | E1; E2 |
| Sanitized operation record | Task code; source and target environment when applicable; package identity and release; root identity; applicable CSV files and Rule IDs; requested effect; dependency result; preview fingerprint when applicable; approval state when required; import, verification, and deployment results when available | Block | Create or complete the task-level record through the selected shared workflow without secrets | Every authoring or import operation | resolve_operation_record | E1 |
| External dependency evidence | Validated result for each supplied DefaultValueSetCode, ValueSetCode, and nonblank TreeCode; deployment readiness when migration is requested | Block | Complete the shared reference-data validation workflow and attach only its sanitized result | New or changed external reference, or a package for import | resolve_dependency_validation_result | E3; E4 |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver | Evidence |
|---|---|---|---|---|
| A structure instance references a StructureCode | Require one root-matching structure in the package or validated target result | Block on an unresolved or ambiguous parent | resolve_structure_hierarchy | E1; E5 |
| An instance segment is supplied | Require its SegmentCode in the parent instance's structure and preserve the structure segment arrangement | Block on an instance-only, missing, or cross-structure segment | resolve_structure_hierarchy | E1; E5 |
| A segment-label definition is absent from the package but its assignment is supplied | Treat as unresolved seeded/reference data rather than automatically invalid | Require a validated reference result before rejecting or authoring a definition | resolve_segment_label_reference | E1; E3 |
| A package requests import | Require the shared validation result, task/package match, exact preview fingerprint when applicable, and current approval before the shared import workflow | Stop before import when any gate is absent | resolve_operation_record | E1; E2 |

## Field Validation

| Check | What Happens | Applies When | Resolver | Evidence |
|---|---|---|---|---|
| Task metadata is PAY_MANAGE_KEY_FLEXFIELD_FOR_COST_ALLOCATION, TASK, and TASK_CSV | Reject a package created for a different task or flow | Before import | resolve_fsm_package_contract | E1 |
| The seven names and headers exactly match the observed 11.13.26.10.0 template contract | Reject altered, missing, or substituted CSV schemas; retain a header-only file when it has no data rows | Every package | resolve_fsm_package_contract | E1; E2 |
| Parent root columns consistently identify COST and 801 | Reject mismatched KFF code or application ID | Every applicable CSV row | resolve_fsm_package_contract | E1 |
| StructureCode is unique under COST/801; SegmentCode is unique under its StructureCode; StructureInstanceCode is unique under COST/801 | Reject duplicate or ambiguous business keys | New or changed rows | resolve_structure_hierarchy | E1 |
| Each structure segment has a valid, non-conflicting ColumnName and internally consistent SequenceNumber | Reject duplicate physical-column use or conflicting segment order | New or changed structure segments | resolve_structure_hierarchy | E1; E6 |
| Each supplied DefaultValueSetCode or ValueSetCode has a validated target dependency result | Block rather than create or copy an unverified value set | A value-set reference is supplied | resolve_dependency_validation_result | E1; E3 |
| Each supplied TreeCode has a validated compatible target tree dependency result | Block rather than infer or default a tree | TreeCode is nonblank | resolve_dependency_validation_result | E1; E5 |
| Supported flag values follow the observed package contract; DefaultType, QueryRequiredType, RangeType, field mandatory matrix, and field mutability are only used when confirmed | Reject an unsupported supplied value; do not invent missing semantics | New or changed rows | resolve_fsm_package_contract | E1; E6 |
| Audit attributes are not synthesized as new business data | Reject invented CreationDate, CreatedBy, LastUpdateDate, LastUpdatedBy, or LastUpdateLogin values | New rows | resolve_operation_record | E1; E2 |
| Omitted package rows are not treated as delete instructions | Stop and route an explicit delete request; do not remove target records by omission | Every package comparison | resolve_operation_record | E2; E3 |

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | Revalidate schema and metadata on a future package release |
| E2 | [Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/25d/oafsm/export-and-import-csv-file-packages.html) | Public Oracle documentation | Confirmed | 25d, reviewed 2026-08-18 | Generic FSM behavior; does not confirm task-specific field mutability |
| E3 | [Key Information About Setup Data Export and Import Processes](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/key-information-about-setup-data-export-and-import-processes.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Generic FSM behavior |
| E4 | [Payroll Cost Allocation Key Flexfield Setup](https://docs.oracle.com/en/cloud/saas/human-resources/faipc/payroll-cost-allocation-key-flexfield-setup.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Functional guidance, not a CSV schema |
| E5 | [Key Flexfield Structure Instances and Segment Instances](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/key-flexfield-structure-instances-and-segment-instances.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Does not define task CSV fields |
| E6 | [Flexfield Segment Properties](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oaext/flexfield-segment-properties.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | RangeType enum for this task remains TBD |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_VALIDATE_PACKAGE | decision | 10 | validate_input | valid->KFFCSV_RESOLVE_PACKAGE_REFERENCES;invalid->KFFCSV_HANDLE_INPUT_ERROR | none | stop | A task-level CSV export, template, authored package, or import request is supplied |
