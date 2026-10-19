---
skill_id: "hcm.global-human-resources.employment-actions-framework.manage-assignment-status"
name: "Manage Assignment Status Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Assignment Status under the Employment Actions Framework functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Employment Actions Framework"
functional_area_code: "ORA_EMPLOYMENT_ACTIONS_FRAMEWORK"
task_code: "PER_MANAGE_ASSIGNMENT_STATUS"
task_name: "Manage Assignment Status"
parent_skill_id: "hcm.global-human-resources.employment-actions-framework"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Assignment-status input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency and reference readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact status and lookup resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting and preservation rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "CSV/XLSX route enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Read, Data Loader, approval, and reconciliation failure handling"
    location: "ora-resource/ora_error_handling.md"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/employment-actions-framework/manage-assignment-status/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/employment-actions-framework/manage-assignment-status/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Manage Assignment Status Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Assignment Status` under `Employment Actions Framework`.

## Task Overview

Use this task to plan and govern `Manage Assignment Status` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_ASSIGNMENT_STATUS` — Manage Assignment Status.
- **Scope:** HCM → Global Human Resources → Employment Actions Framework.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `FSM` with no declared Data Loader business object.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_ASSIGNMENT_STATUS`
- task_name: `Manage Assignment Status`
- parent_skill_id: `hcm.global-human-resources.employment-actions-framework`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Employment Actions Framework`
- functional_area_code: `ORA_EMPLOYMENT_ACTIONS_FRAMEWORK`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Assignment Status` under `Employment Actions Framework`.

## Setup Task Metadata

- Task name: `Manage Assignment Status`
- Task code: `PER_MANAGE_ASSIGNMENT_STATUS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import the exported FSM setup CSV ZIP with `core.data-loader`; the archive must retain `ASM_SETUP_CSV_METADATA.xml` so the shared loader classifies it as FSM and Fusion executes `submitTaskCSVImport`.

## Supported Operations and CSV Authoring

This task supports read, create, and edit only. Delete is unsupported: do not prepare a delete package or invoke Fusion for a delete request.

- Read `assignmentStatuses` by `AssignmentStatusCode` for a supplied code and by `UserStatus` for a supplied display name; do not query a generic name field.
- For a read, complete every applicable resolver and return the final result in the same turn; do not pause at an intermediate lookup.
- For create or edit, run every applicable declared read and task rule in graph order. In the same turn, obtain a fresh same-task FSM export, populate and validate it from the resolved business values, and continue to `AS.LOADER_READY`; a missing prior ZIP is not a blocker or user input. Invoke `core.data-loader` and keep control until Core returns the immutable ZIP preview. Then wait for standalone `approve`, import once through `submitTaskCSVImport`, and reconcile with a fresh read/export. Retain the exact FSM metadata and object CSV names; do not convert the package into an HCM Data Loader business-object ZIP.
- Resolve lookup-backed values through [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md); retain verified stored codes, never inferred display values.
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- Require `UserStatus`, `AssignmentStatusCode`, `PaySystemStatus`, `PerSystemStatus`, and `StartDate` for a create. Resolve Country to `LegislationCode`; when Original Assignment Status is supplied, resolve its exact current `AssignmentStatusTypeId` and write it to `OrigAssignStatusTypeId`. Treat `AssignmentStatusCode`, `PaySystemStatus`, and `PerSystemStatus` as read-only on edit; preserve unchanged exported values and do not treat an `AssignmentStatusCode` edit as a create. Do not overwrite unrelated rows or retry an uncertain load automatically.
- No mutating Fusion REST calls are permitted.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Employment Actions Framework`
- Setup task name: `Manage Assignment Status`
- Setup task code: `PER_MANAGE_ASSIGNMENT_STATUS`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.global-human-resources.employment-actions-framework` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
