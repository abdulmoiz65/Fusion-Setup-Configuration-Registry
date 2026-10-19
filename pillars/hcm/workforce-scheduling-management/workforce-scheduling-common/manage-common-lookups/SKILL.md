---
skill_id: "hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups"
name: "Manage Common Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Common Lookups under the Workforce Scheduling Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
functional_area: "Workforce Scheduling Common"
functional_area_code: "ORA_WORKFORCE_SCHEDULING_COMMON"
task_code: "FND_MANAGE_COMMON_LOOKUPS"
task_name: "Manage Common Lookups"
parent_skill_id: "hcm.workforce-scheduling-management.workforce-scheduling-common"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce scheduling management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/workforce-scheduling-common/manage-common-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/workforce-scheduling-common/manage-common-lookups/current/"
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

# Manage Common Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Common Lookups` under `Workforce Scheduling Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_COMMON_LOOKUPS`
- task_name: `Manage Common Lookups`
- parent_skill_id: `hcm.workforce-scheduling-management.workforce-scheduling-common`
- pillar: `HCM`
- offering: `Workforce Scheduling Management`
- functional_area: `Workforce Scheduling Common`
- functional_area_code: `ORA_WORKFORCE_SCHEDULING_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Common Lookups` under `Workforce Scheduling Common`.

## Setup Task Metadata

- Task name: `Manage Common Lookups`
- Task code: `FND_MANAGE_COMMON_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Apps Common Lookup Routing

- Core skill route: `core.fusion-api.apps-common.lookups`
- Owning core-skill team: `Common Applications / ApplCore`
- Consumer dependency: `Application Lookup Foundation Skill`
- Required consumer input: the exact, source-backed lookup type (`LookupType`)
  required by the consuming product
- Workforce Scheduling FSM source references:
  - `Manage Common Lookups`
  - `Manage Extended Lookup Codes`

### Scoped Reference Routing

| Scoped reference | Lookup category | Lookup subfunction |
| --- | --- | --- |
| `Common Lookups` | Common | `common-lookups.md` |
| `HCM Extended Lookup Code` | Product-specific or generic | `generic-lookups.md` |
| `Manage Common Lookups` | Common | `common-lookups.md` |
| `Manage Extended Lookup Codes` | Product-specific or generic | `generic-lookups.md` |

Select other lookup subfunctions by the consuming product's source-backed
lookup category:

| Lookup category | Lookup subfunction |
| --- | --- |
| Common | `common-lookups.md` |
| Product-specific or generic | `generic-lookups.md` |
| Set-enabled | `set-enabled-lookups.md` |
| Standard | `standard-lookups.md` |

### Validation Gap

The scoped lookup references classify the work but do not provide an exact
product `LookupType` identifier. Stop lookup read or update routing until the
consuming product supplies that source-backed identifier. Do not use `Common
Lookups`, `HCM Extended Lookup Code`, `Manage Common Lookups`, or `Manage
Extended Lookup Codes` as an inferred REST `LookupType`.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Preserve `Manage Common Lookups` and `Manage Extended Lookup Codes` as the
   Workforce Scheduling FSM source references for setup traceability.
5. Select the lookup subfunction using the lookup category table above.
6. Route lookup setup work to `core.fusion-api.apps-common.lookups`, passing
   only the consuming product's exact source-backed `LookupType`. The provider
   resolves and returns eligible `LookupCode` values; do not pass `LookupCode`
   as provider input.
7. When the exact `LookupType` is unresolved, record the validation gap above
   and stop before invoking the core skill.

Use this task metadata when invoking those skills:

- Offering: `Workforce Scheduling Management`
- Functional area / Setup Object: `Workforce Scheduling Common`
- Setup task name: `Manage Common Lookups`
- Setup task code: `FND_MANAGE_COMMON_LOOKUPS`




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

Use the parent functional-area skill `hcm.workforce-scheduling-management.workforce-scheduling-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
