---
skill_id: "hcm.global-human-resources.hcm-trees.manage-organization-trees"
name: "Manage Organization Trees Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Organization Trees under the HCM Trees functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "HCM Trees"
functional_area_code: "ORA_HCM_TREES"
task_code: "PER_MANAGE_ORGANIZATION_TREE"
task_name: "Manage Organization Trees"
parent_skill_id: "hcm.global-human-resources.hcm-trees"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
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
uses_core:
  - "core.fusion-api.apps-common.trees"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/hcm-trees/manage-organization-trees/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/hcm-trees/manage-organization-trees/current/"
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

# Manage Organization Trees Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Organization Trees` under `HCM Trees`.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_ORGANIZATION_TREE`
- task_name: `Manage Organization Trees`
- parent_skill_id: `hcm.global-human-resources.hcm-trees`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `HCM Trees`
- functional_area_code: `ORA_HCM_TREES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Organization Trees` under `HCM Trees`.

For every create, read, update, or delete operation on an organization tree, invoke `core.fusion-api.apps-common.trees`. It owns tree lookup, planning, validation, approval, execution, and verification; do not use another tree route.

For a new tree version, ask for its effective start date but bind `EffectiveEndDate` internally as `4712-12-31` when omitted. For an existing-version change, preserve every unrequested current value; do not apply creation defaults.

## Setup Task Metadata

- Task name: `Manage Organization Trees`
- Task code: `PER_MANAGE_ORGANIZATION_TREE`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

No Data Loader business object is configured for this task. Do not invoke `core.data-loader` or generate a Data Loader sample. Route every tree create, read, update, and delete operation through `core.fusion-api.apps-common.trees`.

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

Use the parent functional-area skill `hcm.global-human-resources.hcm-trees` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
