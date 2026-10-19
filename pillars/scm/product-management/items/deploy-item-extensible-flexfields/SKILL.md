---
skill_id: "scm.product-management.items.deploy-item-extensible-flexfields"
name: "Deploy Item Extensible Flexfields Setup Task Guidance"
description: "Routes approval-gated deployment and deployment-status work for a selected Item extensible flexfield through Apps Common."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "EGO_DEPLOY_EFFS"
task_name: "Deploy Item Extensible Flexfields"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/deploy-item-extensible-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/deploy-item-extensible-flexfields/current/"
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

# Deploy Item Extensible Flexfields Setup Task Guidance

## Purpose

Provides task-specific planning and approval-gated deployment routing for a
selected Item extensible flexfield under `Items`.

## Setup Task Skill Contract

- task_code: `EGO_DEPLOY_EFFS`
- task_name: `Deploy Item Extensible Flexfields`
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

Use this skill when a completed Item extensible-flexfield configuration needs
deployment or its deployment status needs to be checked under `Items`.

## Setup Task Metadata

- Task name: `Deploy Item Extensible Flexfields`
- Task code: `EGO_DEPLOY_EFFS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Extensible Flexfield Deployment Routing

Deployment is separate from CSV transport: it compiles an already-configured
flexfield and does not import setup data. Route the specialized work through
`core.fusion-api.apps-common`, selecting its Extensible Flexfields deployment
workflow.

1. Require the exact Flexfield Code selected in **Deploy Item Extensible
   Flexfields**, the target environment, and evidence that the relevant
   configuration change or approved FSM import completed successfully.
2. Do not treat an observed UI result as a default. For example,
   `EGO_ITEM_EFF` was observed as Item Extended Attributes, but the caller
   must explicitly select the code to deploy.
3. Have Apps Common resolve the EFF deployment identifiers and use its
   approval-gated REST deployment/status workflow. This task does not call
   REST or a loader directly.
4. Obtain explicit approval immediately before a live deployment. Report the
   selected code, environment, safe deployment status, date, and sanitized
   error details; do not retry automatically.

Use `shared.setup-export.task-level-export` and `core.data-loader` only when
the selected EFF's separate setup-data export or approved FSM import workflow
is in scope. Validate those artifacts with the shared validation skills before
the deployment preflight.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Deploy Item Extensible Flexfields`
- Setup task code: `EGO_DEPLOY_EFFS`




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
