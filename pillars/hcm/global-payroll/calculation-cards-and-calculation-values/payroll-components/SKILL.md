---
skill_id: "hcm.global-payroll.calculation-cards-and-calculation-values.payroll-components"
name: "Payroll Components Setup Task Guidance"
description: "Provides task-specific setup guidance for Payroll Components under the Calculation Cards and Calculation Values functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Calculation Cards and Calculation Values"
functional_area_code: "ORA_CALCULATION_CARDS_AND_CALCULATION_VALUES"
task_code: "SUPPLEMENTAL_PAYROLL_COMPONENTS"
task_name: "Payroll Components"
parent_skill_id: "hcm.global-payroll.calculation-cards-and-calculation-values"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/calculation-cards-and-calculation-values/payroll-components/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/calculation-cards-and-calculation-values/payroll-components/current/"
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

# Payroll Components Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Payroll Components` under `Calculation Cards and Calculation Values`.

## Setup Task Skill Contract

- task_code: `SUPPLEMENTAL_PAYROLL_COMPONENTS`
- task_name: `Payroll Components`
- parent_skill_id: `hcm.global-payroll.calculation-cards-and-calculation-values`
- pillar: `HCM`
- offering: `Payroll`
- functional_area: `Calculation Cards and Calculation Values`
- functional_area_code: `ORA_CALCULATION_CARDS_AND_CALCULATION_VALUES`
- available_flag: `Y`
- export_import_supported_flag: `UNKNOWN`
- csv_export_import_supported_flag: `UNKNOWN`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Payroll Components` under `Calculation Cards and Calculation Values`.

## Setup Task Metadata

- Task name: `Payroll Components`
- Task code: `SUPPLEMENTAL_PAYROLL_COMPONENTS`
- Available: `Y`
- Export/import supported: `UNKNOWN`
- CSV export/import supported: `UNKNOWN`
- CSV export/import routing: `not supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `UNKNOWN`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


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

Use the parent functional-area skill `hcm.global-payroll.calculation-cards-and-calculation-values` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
