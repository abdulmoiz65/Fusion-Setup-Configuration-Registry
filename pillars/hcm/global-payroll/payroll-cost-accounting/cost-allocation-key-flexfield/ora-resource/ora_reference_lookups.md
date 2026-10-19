# Cost Allocation Key Flexfield Reference Lookups

These are local, sanitized-record lookups. The task has no direct runtime LOV REST endpoint and must use the selected shared FSM export, validation, reference-data validation, and import workflows for any Fusion access.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches | Evidence |
|---|---|---|---|---|---|---|
| resolve_fsm_package_contract | A package is inspected, authored, validated, or proposed for import | Sanitized package metadata; ASM_SETUP_CSV_METADATA.xml; seven CSV filenames and headers; root rows | Match exactly TaskCode=PAY_MANAGE_KEY_FLEXFIELD_FOR_COST_ALLOCATION, ObjectType=TASK, CreatedByFlow=TASK_CSV, KeyFlexfieldCode=COST, ApplicationId=801, and the observed seven-file/header contract | task_code; package_identity; package_release; root_kff_identity; applicable_csv_files; metadata_sequence | Stop as package mismatch; do not import or substitute another task package | E1 |
| resolve_operation_record | An authoring or import operation is requested | Sanitized task operation record | Require every required operation-record field and a current preview/approval fingerprint when the selected framework requires them | source_environment; target_environment; requested_business_effect; applicable_rule_ids; dependency_validation_result; approval_state; import_result; post_import_verification; deployment_result | Stop as missing operation record or approval blocker | E1 |
| resolve_structure_hierarchy | A package contains structures, segments, instances, or instance segments | Parsed root, structure, structure-segment, structure-instance, and structure-instance-segment CSV rows | Match root first; then StructureCode; then StructureCode plus SegmentCode; then StructureInstanceCode plus SegmentCode | resolved_structure; resolved_segment; resolved_instance; parent_child_validation_result | Stop as missing parent, duplicate key, cross-structure segment, or inconsistent sequence | E1; E2 |
| resolve_segment_label_reference | A segment-label assignment or definition is supplied | Parsed segment-label CSV rows and sanitized shared reference-data validation result | Match SegmentLabelCode in exported definitions or a validated seeded/target reference result; package omission alone is not a no-match | resolved_segment_label; label_reference_status | Stop as unresolved reference; do not create a synthetic label definition | E1; E3 |
| resolve_dependency_validation_result | An external value-set, tree, deployment, or import dependency must be evaluated | Sanitized outcome from shared setup-data-validator and reference-data-validator workflows | Require one current result for every applicable dependency and target environment | dependency_status; value_set_status; tree_status; deployment_readiness; unresolved_dependencies | Stop as dependency blocker; no direct lookup or creation occurs in this task resource | E1; E4 |

## Lookup Execution Rules

| Situation | What Happens | Evidence |
|---|---|---|
| No direct task LOV or mutation endpoint is documented | Keep lookup execution within the shared FSM workflows and operation record; do not call or invent a direct KFF REST route | E1 |
| Source package contains a blank TreeCode | Do not infer a tree dependency | E1 |
| Source package contains a nonblank TreeCode | Require a validated dependency result for the target tree and compatible segment value set | E1; E2 |
| A ready-to-use or seeded label is absent from exported definitions | Do not treat absence alone as invalid; require a validated target/reference result when the assignment is used | E1; E4 |

## Evidence Register

| Evidence | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| E1 | Supplied task CSV template, data export, and ASM_SETUP_CSV_METADATA.xml described in the request | Task CSV evidence | Observed | 11.13.26.10.0 | No target-environment observation was supplied |
| E2 | [Key Flexfield Structure Instances and Segment Instances](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/key-flexfield-structure-instances-and-segment-instances.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Does not provide a task-level CSV lookup API |
| E3 | [Overview of Key Flexfields](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/overview-of-key-flexfields.html) | Public Oracle documentation | Confirmed | Current, reviewed 2026-08-18 | Seeded-label availability remains release-specific |
| E4 | [Key Information About Setup Data Export and Import Processes](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/key-information-about-setup-data-export-and-import-processes.html) | Public Oracle documentation | Confirmed | 26b, reviewed 2026-08-18 | Shared workflow owns actual Fusion requests |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| KFFCSV_RESOLVE_PACKAGE_REFERENCES | decision | 20 | evaluate_result | resolved->KFFCSV_CHECK_DEPENDENCY_READINESS;unresolved->KFFCSV_HANDLE_DEPENDENCY_ERROR | KFFCSV_VALIDATE_PACKAGE | stop | Package validation succeeded and hierarchy, labels, external references, or deployment readiness must be resolved |
