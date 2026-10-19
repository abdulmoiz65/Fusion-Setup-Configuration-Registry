---
skill_id: "hcm.hcm-communicate.employee-communications.manage-external-integrations"
name: "Manage External Integrations Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage External Integrations under the Employee Communications functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
functional_area: "Employee Communications"
functional_area_code: "ORA_IRC_EMPLOYEE_CAMPAIGNS"
task_code: "ORA_IRC_EMP_EXT_INTEGRATIONS"
task_name: "Manage External Integrations"
parent_skill_id: "hcm.hcm-communicate.employee-communications"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm communicate pillar team"
version: "0.2.0"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-external-integrations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-external-integrations/current/"
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

# Manage External Integrations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage External Integrations` under `Employee Communications`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_EMP_EXT_INTEGRATIONS`
- task_name: `Manage External Integrations`
- parent_skill_id: `hcm.hcm-communicate.employee-communications`
- pillar: `HCM`
- offering: `HCM Communicate`
- functional_area: `Employee Communications`
- functional_area_code: `ORA_IRC_EMPLOYEE_CAMPAIGNS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: not applicable to the FSM Data Loader route
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage External Integrations` under `Employee Communications`.

## Capabilities

- Check whether Microsoft Teams or Slack is currently enabled.
- Export the current integration settings for review.
- Guide the user through enabling Microsoft Teams or Slack and collect the
  information needed for setup.

Only make a setting change when a supported setup method is available and the
required review is complete.

## Example Requests

- “Is Microsoft Teams enabled?”
- “Export my current integration settings.”
- “Help me enable Slack for HCM Communicate.”

## Setup Task Metadata

- Task name: `Manage External Integrations`
- Task code: `ORA_IRC_EMP_EXT_INTEGRATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: not applicable to the FSM Data Loader route

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `HCM Communicate`
- Functional area / Setup Object: `Employee Communications`
- Setup task name: `Manage External Integrations`
- Setup task code: `ORA_IRC_EMP_EXT_INTEGRATIONS`




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

Use the parent functional-area skill `hcm.hcm-communicate.employee-communications` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
