# Cost Allocation Key Flexfield Dependency Readiness

The task package is not self-contained for Payroll Costing Value Sets, trees, Legislative Data Group association, or Subledger Accounting mapping. This resource validates readiness; it does not create those dependencies.

## Required Dependency Order

| Sequence | Dependency | What Must Happen | Evidence |
|---|---|---|---|
| 1 | Task package identity | Confirm the selected TASK/TASK_CSV package, release, root COST/801, metadata, seven filenames, and headers | E1 |
| 2 | KFF hierarchy | Validate root, structures, segments, labels, instances, and instance segments in parent-first order | E1 |
| 3 | Value sets and trees | Validate every supplied DefaultValueSetCode, ValueSetCode, and nonblank TreeCode in the target through shared validation evidence | E1; E2 |
| 4 | Flexfield movement readiness | Confirm documented deployment eligibility before migration when applicable | E3 |
| 5 | Import and post-import verification | Use shared FSM import only after the required operation record, preview, and approval gates; then verify import and deployment outcomes | E2; E3 |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| package_contract | Selected task package | Yes | Every export, authoring, validation, or import | Verify | Sanitized package metadata and CSV inventory | resolve_fsm_package_contract | Prevents cross-task, cross-root, and schema mismatches | Re-export or select the Cost Allocation Key Flexfield task package | task_code; package_release; root_kff_identity; applicable_csv_files | E1 |
| hierarchy_integrity | Parent-child KFF hierarchy | Yes | Package contains rows beyond the root | Verify | Parsed package rows | resolve_structure_hierarchy | Structures, segments, labels, instances, and instance segments have exact parents | Correct the parent key or remove the unsupported row | resolved_structure; resolved_segment; resolved_instance | E1; E4 |
| value_set_readiness | Payroll Costing Value Set | Conditional | DefaultValueSetCode or ValueSetCode is supplied | Verify | Sanitized shared reference-data validation result | resolve_dependency_validation_result | Value sets are external to the observed task package | Create or migrate the value set through its own supported setup path, then revalidate | value_set_status; unresolved_dependencies | E2; E4 |
| tree_readiness | Tree dependency | Conditional | TreeCode is nonblank | Verify | Sanitized shared reference-data validation result | resolve_dependency_validation_result | A tree-backed segment requires a compatible target tree dependency | Resolve the tree and compatibility outside this task, then revalidate | tree_status; unresolved_dependencies | E4 |
| seeded_label_readiness | Seeded or target segment-label reference | Conditional | An assignment has no exported definition row | Verify | Sanitized shared reference-data validation result | resolve_segment_label_reference | Ready-to-use data may be omitted from an export | Validate the label reference; do not create a synthetic definition | resolved_segment_label; label_reference_status | E2 |
| deployment_readiness | Source and target flexfield deployment state | Conditional | Setup is moved or modified | Verify | Sanitized shared validation and post-import result | resolve_dependency_validation_result | Eligible Application Key Flexfields must meet documented deployment status and imports can trigger redeployment | Stop on a failed deployment result and obtain remediation before claiming completion | deployment_readiness; deployment_result | E3 |
| ldg_association | KFF instance to Legislative Data Group association | Conditional | The requested effect includes an LDG association | Blocked | Request scope | resolve_operation_record | The association is outside the observed KFF CSV hierarchy | Route to the Legislative Data Groups task; do not author a KFF CSV row | requested_business_effect | E5 |
| sla_mapping | Subledger Accounting mapping | Conditional | The requested effect includes accounting mapping | Blocked | Request scope | resolve_operation_record | SLA mapping is outside this KFF task package | Route to the applicable SLA setup task | requested_business_effect | E5 |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? | Evidence |
|---|---|---|---|
| Satisfied | All required package and sanitized shared validation results are current and successful | Lookup through shared workflow only; no create in this task | E1 |
| Blocked | A parent, value set, tree, deployment result, task identity, approval, LDG association, or SLA mapping is missing or out of scope | No | E1; E2 |
| TBD | Field-level mandatory, mutability, enum, custom-label, or direct target lookup contract is not authoritatively established | No; resolve evidence before relying on the affected operation | E1 |

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | Future releases must be revalidated |
| E2 | [Key Information About Setup Data Export and Import Processes](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/key-information-about-setup-data-export-and-import-processes.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Generic FSM rules |
| E3 | [Business Objects for Moving Common Reference Objects](https://docs.oracle.com/en/cloud/saas/applications-common/26b/facia/business-objects-for-moving-common-reference-objects.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Deployment status must be evidenced per operation |
| E4 | [Payroll Cost Allocation Key Flexfield Structure](https://docs.oracle.com/en/cloud/saas/human-resources/fapus/payroll-cost-allocation-key-flexfield-structure.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Value-set definition is a separate setup capability |
| E5 | [Payroll Cost Allocation Key Flexfield Setup](https://docs.oracle.com/en/cloud/saas/human-resources/faipc/payroll-cost-allocation-key-flexfield-setup.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | LDG and SLA setup are outside these CSV files |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_CHECK_DEPENDENCY_READINESS | decision | 30 | resolve_dependency | ready->KFFCSV_APPLY_DEFAULTS;blocked->KFFCSV_HANDLE_DEPENDENCY_ERROR | KFFCSV_RESOLVE_PACKAGE_REFERENCES | stop | The local lookup result has resolved the package hierarchy and dependency evidence |
