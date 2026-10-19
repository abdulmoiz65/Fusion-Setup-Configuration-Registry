---
skill_id: "erp.financials.financial-reporting-structures.manage-account-combinations"
name: "Manage Account Combinations Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Account Combinations under the Financial Reporting Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Financial Reporting Structures"
functional_area_code: "ORA_ASK_FIN_REPORTING_STRUCT"
task_code: "GL_MANAGE_ACCOUNT_COMBINATIONS"
task_name: "Manage Account Combinations"
parent_skill_id: "erp.financials.financial-reporting-structures"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FBDI"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-account-combinations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/financial-reporting-structures/manage-account-combinations/current/"
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

# Manage Account Combinations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Account Combinations` under `Financial Reporting Structures`.

## Setup Task Skill Contract

- task_code: `GL_MANAGE_ACCOUNT_COMBINATIONS`
- task_name: `Manage Account Combinations`
- parent_skill_id: `erp.financials.financial-reporting-structures`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Financial Reporting Structures`
- functional_area_code: `ORA_ASK_FIN_REPORTING_STRUCT`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `FBDI`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Account Combinations` under `Financial Reporting Structures`.

## Setup Task Metadata

- Task name: `Manage Account Combinations`
- Task code: `GL_MANAGE_ACCOUNT_COMBINATIONS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `FBDI`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so FSM CSV export/import is not supported for this task. This task's approved create/manage path is the FBDI package defined in its task-local `ora-resource` contract.

Route every FBDI validation, package handoff, upload, initiation, monitoring, and troubleshooting request through `core/data-loader`. Do not invoke ERP Integrations, ESS jobs, or any other product-specific adapter directly. `core/data-loader` owns the immutable artifact, Task Hook validation, approval boundary, and any later import execution. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

For natural-language input without an Import Group Identifier, generate a fresh local `yyyyMMddHHmmss` identifier before CSV validation; do not ask the user for it.

## Documentation Lookup Boundary

Use this task's local `ora-resource` contract and `core/data-loader` for normal CSV, ZIP, and import-flow handling. Do not browse Oracle documentation merely to rediscover those established rules or follow related-topic links by default. Consult official Oracle documentation only when a required fact is absent or ambiguous in the local contract, or when release-specific compatibility must be verified.

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

Use the parent functional-area skill `erp.financials.financial-reporting-structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
