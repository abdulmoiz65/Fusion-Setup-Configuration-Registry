---
skill_id: "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
name: "Manage Administrator Profile Values Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Administrator Profile Values under the Global Human Resources Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Global Human Resources Common"
functional_area_code: "ORA_GLOBAL_HUMAN_RESOURCES_COMMON"
task_code: "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
task_name: "Manage Administrator Profile Values"
parent_skill_id: "hcm.global-human-resources.global-human-resources-common"
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
  - "core.fusion-api.apps-common"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/global-human-resources-common/manage-administrator-profile-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/global-human-resources-common/manage-administrator-profile-values/current/"
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
side_effects:
  - "After exact approval, creates, edits, or deletes the selected profile value through core.fusion-api.apps-common."
required_privileges:
  - "Access to read and change the selected profile option value."
---

# Manage Administrator Profile Values Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Administrator Profile Values` under `Global Human Resources Common`.

## Task Overview

Use this task to plan and govern profile-value setup in Global Human Resources.

- **Task identity:** `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES` — Manage Administrator Profile Values.
- **Scope:** HCM → Global Human Resources → Global Human Resources Common.
- **Declared routing:** the catalog marks CSV export/import as `Y`; this task's detailed routing is through `core.fusion-api.apps-common`, as defined below.
- **Read next:** [task contract](#setup-task-skill-contract), [usage](#usage), and [Apps Common CRUD routing](#apps-common-crud-routing). Those sections are authoritative for operation-specific inputs, approvals, and restrictions.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- task_name: `Manage Administrator Profile Values`
- parent_skill_id: `hcm.global-human-resources.global-human-resources-common`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Global Human Resources Common`
- functional_area_code: `ORA_GLOBAL_HUMAN_RESOURCES_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Administrator Profile Values` under `Global Human Resources Common`.

## Setup Task Metadata

- Task name: `Manage Administrator Profile Values`
- Task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Apps Common CRUD Routing

The catalog export/import flags remain task metadata. Route every read, create, edit, and delete request only through `core.fusion-api.apps-common`; do not use Core Data Loader, FSM import, direct REST payload construction, or an alternate export/import route.

Require exactly one profile option identifier: `ProfileOptionName` or `ProfileOptionCode`. For every operation, collect the level and level value when applicable; for a mutation, collect the requested value. Resolve ambiguity before execution, preview the exact target and requested delta, require explicit approval, invoke the shared capability once, and re-read to reconcile the outcome. Do not retry an uncertain mutation automatically.

Reject a request that supplies neither identifier or both. Return the exact resolved Profile Option, level, level value, and resulting value or an explicit missing/ambiguous outcome. Do not implement a separate profile-option API or export/import path.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Global Human Resources Common`
- Setup task name: `Manage Administrator Profile Values`
- Setup task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`




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

Use the parent functional-area skill `hcm.global-human-resources.global-human-resources-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
