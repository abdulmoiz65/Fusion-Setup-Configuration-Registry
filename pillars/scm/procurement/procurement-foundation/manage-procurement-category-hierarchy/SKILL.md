---
skill_id: "scm.procurement.procurement-foundation.manage-procurement-category-hierarchy"
name: "Manage Procurement Category Hierarchy Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Procurement Category Hierarchy under the Procurement Foundation functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Procurement Foundation"
functional_area_code: "ORA_PO_PROC_FOUNDATION_FA"
task_code: "POR_MANAGE_AGENT_ASSIGNMENTS_CATEGORY_HIERARCHY"
task_name: "Manage Procurement Category Hierarchy"
parent_skill_id: "scm.procurement.procurement-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/procurement-foundation/manage-procurement-category-hierarchy/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/procurement-foundation/manage-procurement-category-hierarchy/current/"
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

# Manage Procurement Category Hierarchy Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Procurement Category Hierarchy` under `Procurement Foundation`.

## Setup Task Skill Contract

- task_code: `POR_MANAGE_AGENT_ASSIGNMENTS_CATEGORY_HIERARCHY`
- task_name: `Manage Procurement Category Hierarchy`
- parent_skill_id: `scm.procurement.procurement-foundation`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Procurement Foundation`
- functional_area_code: `ORA_PO_PROC_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Procurement Category Hierarchy` under `Procurement Foundation`.

## Setup Task Metadata

- Task name: `Manage Procurement Category Hierarchy`
- Task code: `POR_MANAGE_AGENT_ASSIGNMENTS_CATEGORY_HIERARCHY`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

This task currently supports FSM only. Use the task's exported FSM package and exact task code for setup data operations. No task-specific REST endpoint or REST business object is configured. The routed skills own preflight, approval, execution, and diagnostics; use the approval workflow in `core.data-loader` for imports without adding a second approval gate.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Procurement Foundation`
- Setup task name: `Manage Procurement Category Hierarchy`
- Setup task code: `POR_MANAGE_AGENT_ASSIGNMENTS_CATEGORY_HIERARCHY`




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

Use the parent functional-area skill `scm.procurement.procurement-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
