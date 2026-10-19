---
skill_id: "scm.product-management.advanced-catalogs.manage-catalog-mappings"
name: "Manage Catalog Mappings Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Catalog Mappings under the Advanced Catalogs functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Advanced Catalogs"
functional_area_code: "EGI_ADVANCED_CATALOGS"
task_code: "EGI_MANAGE_CATALOG_MAPPINGS"
task_name: "Manage Catalog Mappings"
parent_skill_id: "scm.product-management.advanced-catalogs"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader.task-hook"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/advanced-catalogs/manage-catalog-mappings/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/advanced-catalogs/manage-catalog-mappings/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Catalog mapping CSV contract and per-detail-row validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Source-category, target-category, and ROOT_ICC item-class lookup contracts"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Task-specific failure classification, disclosure, and refusal behavior"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "CSV binding, read-only reference lookup, aggregate validation, and refusal rules are defined. Shared validation, Data Loader Task Hook evaluation, import preview, approval, and live verification remain required."
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

# Manage Catalog Mappings Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Catalog Mappings` under `Advanced Catalogs`.

## Setup Task Skill Contract

- task_code: `EGI_MANAGE_CATALOG_MAPPINGS`
- task_name: `Manage Catalog Mappings`
- parent_skill_id: `scm.product-management.advanced-catalogs`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Advanced Catalogs`
- functional_area_code: `EGI_ADVANCED_CATALOGS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Catalog Mappings` under `Advanced Catalogs`.

## Setup Task Metadata

- Task name: `Manage Catalog Mappings`
- Task code: `EGI_MANAGE_CATALOG_MAPPINGS`
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
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Advanced Catalogs`
- Setup task name: `Manage Catalog Mappings`
- Setup task code: `EGI_MANAGE_CATALOG_MAPPINGS`

## Task Rules

Use the resources declared in `oracle_supplied_guidance_files` as the task-specific runtime contract. Read the applicable rules before task-rule evaluation and load error handling before preview or import:

| Resource | Responsibility |
|---|---|
| [Input validation](ora-resource/ora_input_validation.md) | Mapping-header and mapping-detail CSV shape, parent-child binding, and per-row validation context |
| [Reference lookups](ora-resource/ora_reference_lookups.md) | Read-only source-category, target-category, and ROOT_ICC item-class resolution |
| [Error handling](ora-resource/ora_error_handling.md) | Aggregated findings, safe disclosure, and stop-before-import behavior |

Use `shared.validation.setup-data-validator` and `shared.validation.reference-data-validator` for generic artifact and reference checks. Those shared validators do not evaluate task-specific Ora Resource rules; retain their validated candidate evidence for Data Loader's single [Task Hook](../../../../../core/data-loader/task-hook/SKILL.md).

For a task-routed load, the Task Hook owns resolution and evaluation of the [compiled task registry](ora-resource/ora_rule_registry.json) against the final immutable artifact. Follow the Task Hook's returned execution guide and the Data Loader preview, approval, and archive-verification lifecycle. Do not invoke Task Validator directly or add a second evaluator or import approval. A structurally ready rule plan is not evaluated rules, successful validation, or permission to mutate Fusion.




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

Use the parent functional-area skill `scm.product-management.advanced-catalogs` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
