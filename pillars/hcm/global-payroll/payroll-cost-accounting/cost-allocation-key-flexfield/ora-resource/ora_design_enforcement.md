# Cost Allocation Key Flexfield Design Enforcement

This resource enforces the confirmed CSV hierarchy and KFF design boundaries before a package can be handed to the shared FSM import workflow.

## Enforcement Order

| Sequence | Step | What Must Happen | Evidence |
|---|---|---|---|
| 1 | Confirm package boundary | Confirm task/flow identity, COST/801 root, metadata, seven filenames, and headers | E1 |
| 2 | Confirm hierarchy | Validate structure, segment, label, instance, and instance-segment parent keys | E1; E2 |
| 3 | Confirm external readiness | Validate value sets, trees, label references, and deployment evidence where applicable | E2; E3 |
| 4 | Enforce unsupported-operation boundaries | Reject delete-by-omission, translation migration, value-set creation, LDG association, SLA mapping, HDL, transactional costing, and direct KFF REST mutation | E1; E4 |
| 5 | Require post-import verification | Do not claim success until shared import results and KFF redeployment outcome are recorded | E3; E5 |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? | Evidence |
|---|---|---|---|---|---|---|
| Every package | Error | resolve_fsm_package_contract | Task identity, flow, root, metadata, file inventory, or header is mismatched | Re-export the exact task template or correct the package without changing its schema | Yes | E1 |
| Structures or segments are added or changed | Error | resolve_structure_hierarchy | Duplicate key, unknown parent, conflicting ColumnName, inconsistent sequence, or independent instance segment | Correct the root-relative design; preserve a structure's segment set and order in each instance | Yes | E1; E2 |
| A supplied value set, tree, or label needs external confirmation | Error | resolve_dependency_validation_result | Current shared validation evidence is missing or failed | Resolve the prerequisite outside this task and revalidate | No | E1; E3 |
| A label definition is absent from the package | Error | resolve_segment_label_reference | The label cannot be confirmed as exported, seeded, or target-valid | Stop rather than fabricate a global label definition | No | E1 |
| Any request proposes deletion by omitted CSV row | Error | resolve_operation_record | Requested effect depends on omission deleting a target row | Return the unsupported operation boundary | No | E4 |
| Any request proposes CSV translation migration, direct KFF REST mutation, HDL, value-set creation, LDG association, SLA mapping, or transactional costing | Error | resolve_operation_record | Requested effect is outside task-level FSM CSV KFF setup | Route to the owning setup task or workflow | No | E1; E4 |
| A KFF movement or import is ready to complete | Error | resolve_dependency_validation_result | Deployment readiness or post-import redeployment result is absent or failed | Stop and report the deployment result; do not claim functional completion | No | E3; E5 |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File | Evidence |
|---|---|---|---|---|
| resolve_fsm_package_contract | Every package | task_code; package_identity; package_release; root_kff_identity; applicable_csv_files | ora_reference_lookups.md | E1 |
| resolve_structure_hierarchy | Hierarchy rows are present | resolved_structure; resolved_segment; resolved_instance; parent_child_validation_result | ora_reference_lookups.md | E1 |
| resolve_dependency_validation_result | External dependencies or deployment apply | dependency_status; value_set_status; tree_status; deployment_readiness; deployment_result | ora_reference_lookups.md | E3 |
| resolve_segment_label_reference | A label definition is omitted | resolved_segment_label; label_reference_status | ora_reference_lookups.md | E1 |
| resolve_operation_record | An authoring or import effect is requested | requested_business_effect; approval_state; post_import_verification | ora_reference_lookups.md | E1 |

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | Requires revalidation for a future release |
| E2 | [Key Flexfield Structure Instances and Segment Instances](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/key-flexfield-structure-instances-and-segment-instances.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Task CSV field mutability remains TBD |
| E3 | [Business Objects for Moving Common Reference Objects](https://docs.oracle.com/en/cloud/saas/applications-common/26b/facia/business-objects-for-moving-common-reference-objects.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Import/deployment outcome must be recorded per run |
| E4 | [Key Information About Setup Data Export and Import Processes](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/key-information-about-setup-data-export-and-import-processes.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | XML is outside this CSV-only resource |
| E5 | [Payroll Cost Allocation Key Flexfield Setup](https://docs.oracle.com/en/cloud/saas/human-resources/faipc/payroll-cost-allocation-key-flexfield-setup.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | LDG association and SLA mapping remain separate tasks |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_ENFORCE_PACKAGE_DESIGN | decision | 50 | design_enforcement | enforced->KFFCSV_GATE_OPERATION;blocked->KFFCSV_HANDLE_DESIGN_ERROR | KFFCSV_APPLY_DEFAULTS | stop | Package dependencies are resolved and the requested business effect is in scope |
