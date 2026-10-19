---
skill_id: "hcm.compensation.workforce-compensation-plan.manage-workforce-compensation-lookups"
name: "Manage Workforce Compensation Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Workforce Compensation Lookups under the Workforce Compensation Plan functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Workforce Compensation Plan"
functional_area_code: "ORA_WORKFORCE_COMPENSATION_PLAN"
task_code: "CMP_MANAGE_COMPENSATION_BUDGET_LOOKUPS"
task_name: "Manage Workforce Compensation Lookups"
parent_skill_id: "hcm.compensation.workforce-compensation-plan"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
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
  - "hcm.compensation.compensation-common.manage-common-lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/workforce-compensation-plan/manage-workforce-compensation-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/workforce-compensation-plan/manage-workforce-compensation-lookups/current/"
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

# Manage Workforce Compensation Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Workforce Compensation Lookups` under `Workforce Compensation Plan`.

## Setup Task Skill Contract

- task_code: `CMP_MANAGE_COMPENSATION_BUDGET_LOOKUPS`
- task_name: `Manage Workforce Compensation Lookups`
- parent_skill_id: `hcm.compensation.workforce-compensation-plan`
- pillar: `HCM`
- offering: `Compensation`
- functional_area: `Workforce Compensation Plan`
- functional_area_code: `ORA_WORKFORCE_COMPENSATION_PLAN`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Workforce Compensation Lookups` under `Workforce Compensation Plan`.

## Setup Task Metadata

- Task name: `Manage Workforce Compensation Lookups`
- Task code: `CMP_MANAGE_COMPENSATION_BUDGET_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Workforce Compensation Lookup Scope

This task is restricted to these exact seeded lookup types. Do not add, infer,
or operate on any other lookup type.

| Lookup type |
| --- |
| `CMP_CWB_CUST_COL_46_LIST` |
| `CMP_CWB_CUST_COL_47_LIST` |
| `CMP_CWB_CUST_COL_48_LIST` |
| `CMP_CWB_CUST_COL_49_LIST` |
| `CMP_CWB_CUST_COL_50_LIST` |
| `CMP_MD_COMPENSATION_GROUP` |
| `CMP_BUDGET_AUDIT_REASONS` |

Route all lookup operations through the Compensation Common task skill
`hcm.compensation.compensation-common.manage-common-lookups`. Do not invoke
`core.fusion-api.apps-common` directly and do not add task-local OAuth,
token-cache, HTTP-client, or Compensation-specific lookup logic. Pass the
exact lookup type and requested lookup-code operation to the Common task skill;
it owns delegation to the shared core skill. The supplied scope does not
identify a lookup category, so the Common task skill must use the core skill's
read-only category-discovery sequence before an operation; never infer the
category from a lookup-type name.

| Target | Allowed operations | Disallowed operations |
| --- | --- | --- |
| Parent seeded lookup type | Read only | Create, update, delete |
| Lookup code and its related details within an in-scope parent type | Read, create, update, delete | Every operation outside the seven listed parent types |

Before an allowed lookup-code create, update, or delete, retrieve the exact
in-scope parent through the Common task skill. For a create, check the target
lookup code for duplicates; for an update or delete, retrieve the exact target
lookup code. Present the target and intended change, and obtain explicit
approval. Do not retry a mutating operation automatically. If the caller asks
to create, update, or delete a parent lookup type, or names an unlisted type,
refuse the request.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Compensation`
- Functional area / Setup Object: `Workforce Compensation Plan`
- Setup task name: `Manage Workforce Compensation Lookups`
- Setup task code: `CMP_MANAGE_COMPENSATION_BUDGET_LOOKUPS`




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

Use the parent functional-area skill `hcm.compensation.workforce-compensation-plan` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
