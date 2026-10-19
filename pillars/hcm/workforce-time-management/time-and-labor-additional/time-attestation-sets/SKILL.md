---
skill_id: "hcm.workforce-time-management.time-and-labor-additional.time-attestation-sets"
name: "Time Attestation Sets Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Attestation Sets under the Time and Labor Additional functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Additional"
functional_area_code: "ORA_TIME_AND_LABOR_ADDITIONAL"
task_code: "ORA_HWM_MANAGE_ATTESTATION_SETS"
task_name: "Time Attestation Sets"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-additional"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
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
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-additional/time-attestation-sets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-additional/time-attestation-sets/current/"
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

# Time Attestation Sets Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Attestation Sets` under `Time and Labor Additional`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_ATTESTATION_SETS`
- task_name: `Time Attestation Sets`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-additional`
- pillar: `HCM`
- offering: `Workforce Time Management`
- functional_area: `Time and Labor Additional`
- functional_area_code: `ORA_TIME_AND_LABOR_ADDITIONAL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Attestation Sets` under `Time and Labor Additional`.

## Catalog and Route Gate

The effective catalog marks export/import and CSV export/import support as `Y` for this task. Route setup data through the FSM CSV workflow. A fresh, same-task FSM export remains authoritative for the package shape, object CSV layout, fields, keys, and allowed values. If that export cannot be obtained or validated, stop and record the evidence gap; do not infer a REST, HCM Data Loader, or other import route.

## Supported Operations and Data Contract

Supported operations are create and edit of Time Attestation Set records through an approved, task-scoped FSM CSV package only after the route gate passes. The validated reference export confirms the parent member `ORA_HWM_ATTESTATION_SET.csv` with `ItrSetName`, `ItrSetId`, `ViewInstanceName`, `GroupingKey`, `ItrSetDescription`, and `ModuleId`; and the line member `ORA_HWM_ATTESTATION_SET_LNS.csv` with `ORA_HWM_ATTESTATION_SET.ItrSetName`, `ItrSetName`, `ProcessingOrder`, `ItrSetLnId`, `ViewInstanceName`, `GroupingKey`, `QstnrVersionNum`, `QuestionnaireCode`, `TriggerEventCs`, `DisplayLevel`, `QuestionnaireName`, `TcatName`, `ItrSetId`, `QuestionnaireId`, and `TimeCategoryId`. Preserve the exported parent-to-line linkage and grouping-key pattern. An Attestation Set may have no line rows; when a line row exists, `ProcessingOrder` is mandatory and numeric.

## FSM CSV Create or Edit Flow

1. Validate task-specific inputs, dependencies, supported create or edit operation, and the current operation rules.
2. Obtain a fresh export for `ORA_HWM_MANAGE_ATTESTATION_SETS` from the same target environment.
3. Populate only the approved task-specific change; retain all unrelated exported values exactly as exported.
4. Validate that the ZIP retains exact-case `ASM_SETUP_CSV_METADATA.xml`, the task-scoped object CSV, valid keys, approved row scope, and no unsupported member changes.
5. Generate the Complete Business Summary and Defaults Applied from verified structured values after validation, lookup resolution, and defaulting.
6. Complete Core Data Loader validation, persist the immutable preflight artifact, and complete Task Hook validation for the exact validated ZIP.
7. Display one direct link to the exact validated ZIP immediately after the Complete Business Summary and Defaults Applied.
8. Request one approval immediately before upload and import, after every validation gate passes; `core.data-loader` owns that approval and one FSM submission.
9. Reconcile the result through the task's documented read or fresh-export path, using the export-confirmed selectors.

## Safety and Refusal Rules

- Do not change unrelated exported values, convert the FSM package to an HCM Data Loader archive, or make direct Fusion REST mutations.
- Do not reuse stale exports, validated ZIPs, or Core Data Loader approval evidence.
- Do not automatically retry a failed, partial, timed-out, or uncertain import.
- Stop if a fresh same-task export cannot be obtained or validated, FSM evidence does not prove the expected import route, or approval is missing or stale.
- On a failed, partial, timed-out, or uncertain import, preserve redacted diagnostics, reconcile current state, and stop.




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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-additional` for functional-area sequencing and scope decisions. The task-local `ora-resource` files own input validation, design gates, and failure behavior. Track token usage for any generated project artifact or skill-run record using the manifest policy.
