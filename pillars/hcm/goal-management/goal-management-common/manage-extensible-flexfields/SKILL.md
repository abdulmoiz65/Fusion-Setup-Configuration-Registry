---
skill_id: "hcm.goal-management.goal-management-common.manage-extensible-flexfields"
name: "Manage Extensible Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Extensible Flexfields under the Goal Management Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Management Common"
functional_area_code: "ORA_GOAL_MANAGEMENT_COMMON"
task_code: "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
task_name: "Manage Extensible Flexfields"
parent_skill_id: "hcm.goal-management.goal-management-common"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
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
  - "core.fusion-api.apps-common.extensible-flexfields"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-extensible-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-extensible-flexfields/current/"
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

# Manage Extensible Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Extensible Flexfields` under `Goal Management Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_EXTENSIBLE_FLEXFIELDS`
- task_name: `Manage Extensible Flexfields`
- parent_skill_id: `hcm.goal-management.goal-management-common`
- pillar: `HCM`
- offering: `Goal Management`
- functional_area: `Goal Management Common`
- functional_area_code: `ORA_GOAL_MANAGEMENT_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Extensible Flexfields` under `Goal Management Common`.

## Setup Task Metadata

- Task name: `Manage Extensible Flexfields`
- Task code: `FND_MANAGE_EXTENSIBLE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is catalog metadata only in this Goal Management
facade. It does not authorize this skill to export, construct, validate, or import
a dependency mutation package. Route any dependency maintenance to the owning
provider named in [Dependent Setup Routing](../../goal-management-common/dependent-setup-routing.md);
that provider chooses its supported single-record or bulk/setup-import workflow.

Use this task metadata when invoking those skills:

- Offering: `Goal Management`
- Functional area / Setup Object: `Goal Management Common`
- Setup task name: `Manage Extensible Flexfields`
- Setup task code: `FND_MANAGE_EXTENSIBLE_FLEXFIELDS`




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

Use the parent functional-area skill `hcm.goal-management.goal-management-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

This skill is a Goal Management delegation facade that preserves catalog
identity only and delegates every EFF read,
export, import, deployment, and setup mutation to
`core.fusion-api.apps-common.extensible-flexfields`. It must not construct a
Goal Management REST mutation or register an EFF mutation API as Goal
Management-owned.
