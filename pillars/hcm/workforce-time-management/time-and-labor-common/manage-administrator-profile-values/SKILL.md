---
skill_id: "hcm.workforce-time-management.time-and-labor-common.manage-administrator-profile-values"
name: "Manage Administrator Profile Values Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Administrator Profile Values under the Time and Labor Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Common"
functional_area_code: "ORA_TIME_AND_LABOR_COMMON"
task_code: "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
task_name: "Manage Administrator Profile Values"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-common"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-common/manage-administrator-profile-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-common/manage-administrator-profile-values/current/"
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

# Manage Administrator Profile Values Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Administrator Profile Values` under `Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- task_name: `Manage Administrator Profile Values`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-common`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `Common`
- functional_area_code: `ORA_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Administrator Profile Values` under `Common`.

## Setup Task Metadata

- Task name: `Manage Administrator Profile Values`
- Task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Time and Labor`
- Functional area / Setup Object: `Common`
- Setup task name: `Manage Administrator Profile Values`
- Setup task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`

## Profile Option Routing

Route administrator profile-value work through the existing
`core.fusion-api.apps-common.profile-options` foundation route; do not create
or use a Time and Labor-specific core profile-option skill. Common
Applications / ApplCore owns this provider's execution, CRUD behavior, and
setup-task ownership. The Application Profile Option Foundation Skill is owned
by Common Applications / ApplCore. Before proposing a configuration change,
invoke route `manage-profile-options` with payload field `profileOptionCode`,
using the exact value supplied by the consuming skill. Pass that value
unchanged and retain the provider's current-state evidence and validation
result; do not require separate PM confirmation.

Compare the provider current state with the product-recommended state and show
the before/after comparison. Apply a provider-owned change only when it is
required by the requested implementation outcome and the user explicitly
confirms the exact target and proposed change. Return the before/after state,
validation result, and any unresolved provider gap; do not construct or submit
provider CRUD requests from this consuming skill.

### Runtime Identifier Contract

The consuming skill supplies the exact `profileOptionCode` at runtime. Use that
value unchanged for the provider invocation. The scoped FSM source reference
`Manage Administrator Profile Values` is context only and must not replace the
runtime identifier. Stop only when `profileOptionCode` is missing; do not add a
separate PM-confirmation or `ProfileOptionName` requirement.

### FSM Source Metadata

- `Manage Administrator Profile Values`


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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
