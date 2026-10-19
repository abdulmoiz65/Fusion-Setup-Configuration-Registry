---
skill_id: "hcm.global-payroll.calculation-cards-and-calculation-values.calculation-value-definitions"
name: "Calculation Value Definitions Setup Task Guidance"
description: "Provides task-specific setup guidance for Calculation Value Definitions under the Calculation Cards and Calculation Values functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Calculation Cards and Calculation Values"
functional_area_code: "ORA_CALCULATION_CARDS_AND_CALCULATION_VALUES"
task_code: "PAY_MANAGE_DEDUCTION_RANGES"
task_name: "Calculation Value Definitions"
parent_skill_id: "hcm.global-payroll.calculation-cards-and-calculation-values"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/calculation-cards-and-calculation-values/calculation-value-definitions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/calculation-cards-and-calculation-values/calculation-value-definitions/current/"
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

# Calculation Value Definitions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Calculation Value Definitions` under `Calculation Cards and Calculation Values`.

## Setup Task Skill Contract

- task_code: `PAY_MANAGE_DEDUCTION_RANGES`
- task_name: `Calculation Value Definitions`
- parent_skill_id: `hcm.global-payroll.calculation-cards-and-calculation-values`
- pillar: `HCM`
- offering: `Payroll`
- functional_area: `Calculation Cards and Calculation Values`
- functional_area_code: `ORA_CALCULATION_CARDS_AND_CALCULATION_VALUES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Calculation Value Definitions` under `Calculation Cards and Calculation Values`.

## Setup Task Metadata

- Task name: `Calculation Value Definitions`
- Task code: `PAY_MANAGE_DEDUCTION_RANGES`
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

- Offering: `Global Payroll`
- Functional area / Setup Object: `Calculation Cards and Calculation Values`
- Setup task name: `Calculation Value Definitions`
- Setup task code: `PAY_MANAGE_DEDUCTION_RANGES`


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
