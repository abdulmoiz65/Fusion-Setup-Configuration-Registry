---
skill_id: "scm.product-management.items.manage-item-attribute-groups-and-attributes"
name: "Manage Item Attribute Groups and Attributes Setup Task Guidance"
description: "Provides task-specific setup guidance and Extensible Flexfield routing for Manage Item Attribute Groups and Attributes under the Items functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "EGO_MANAGE_ITEM_ATTRIBUTE_GROUPS_AND_ATTRIBUTES"
task_name: "Manage Item Attribute Groups and Attributes"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
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
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-item-attribute-groups-and-attributes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-item-attribute-groups-and-attributes/current/"
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
  - "After exact approval, may submit deployment of the selected Item Extensible Flexfield through core.fusion-api.apps-common."
required_privileges:
  - "Fusion privileges required by the selected setup-task export, Data Loader, and Item Extensible Flexfield deployment workflows."
---

# Manage Item Attribute Groups and Attributes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Item Attribute Groups and Attributes` under `Items`.

## Setup Task Skill Contract

- task_code: `EGO_MANAGE_ITEM_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`
- task_name: `Manage Item Attribute Groups and Attributes`
- parent_skill_id: `scm.product-management.items`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Items`
- functional_area_code: `ORA_EGP_FA_ITEMS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Item Attribute Groups and Attributes` under `Items`.

## Extensible Flexfield Routing

This task configures the Item Extensible Flexfield `EGO_ITEM_EFF`. Route the
request through `core.fusion-api.apps-common.extensible-flexfields`.

The setup data route and the deployment route are separate:

- Export the task setup data through `shared.setup-export.task-level-export`.
- Import an approved FSM CSV package only through `core.data-loader`.
- Deploy `EGO_ITEM_EFF` only after a successful import, or after a confirmed
  direct UI configuration change that requires redeployment. The delegated EFF
  workflow owns the approval-gated deployment request and deployment-status
  check; this skill must not construct direct REST requests.

Creating or editing an attribute group, or creating an item class associated
with an attribute group, requires redeploying the extensible flexfield. Confirm
successful deployment from its status and deployment date.

## Setup Task Metadata

- Task name: `Manage Item Attribute Groups and Attributes`
- Task code: `EGO_MANAGE_ITEM_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Item Extensible Flexfield code: `EGO_ITEM_EFF`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.
5. After a successful import, route required deployment and deployment-status
   work for `EGO_ITEM_EFF` through
   `core.fusion-api.apps-common.extensible-flexfields`. Obtain explicit
   approval immediately before the deployment request.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Item Attribute Groups and Attributes`
- Setup task code: `EGO_MANAGE_ITEM_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`




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

Use the parent functional-area skill `scm.product-management.items` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
