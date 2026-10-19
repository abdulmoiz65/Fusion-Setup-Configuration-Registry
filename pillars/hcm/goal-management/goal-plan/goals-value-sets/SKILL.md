---
skill_id: "hcm.goal-management.goal-plan.goals-value-sets"
name: "Goals Value Sets Setup Task Guidance"
description: "Provides task-specific setup guidance for Goals Value Sets under the Goal Plan functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Plan"
functional_area_code: "ORA_GOAL_PLAN"
task_code: "HRG_MANAGE_GOALS_VALUE_SETS"
task_name: "Goals Value Sets"
parent_skill_id: "hcm.goal-management.goal-plan"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
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
  - "core.fusion-api.apps-common.value-sets"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/goals-value-sets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/goals-value-sets/current/"
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

# Goals Value Sets Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Goals Value Sets` under `Goal Plan`.

## Setup Task Skill Contract

- task_code: `HRG_MANAGE_GOALS_VALUE_SETS`
- task_name: `Goals Value Sets`
- parent_skill_id: `hcm.goal-management.goal-plan`
- pillar: `HCM`
- offering: `Goal Management`
- functional_area: `Goal Plan`
- functional_area_code: `ORA_GOAL_PLAN`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Goals Value Sets` under `Goal Plan`.

## Setup Task Metadata

- Task name: `Goals Value Sets`
- Task code: `HRG_MANAGE_GOALS_VALUE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is catalog metadata only in this Goal Management
facade. It does not authorize this skill to export, construct, validate, or import
a dependency mutation package. Route any dependency maintenance to the owning
provider named in [Dependent Setup Routing](../../goal-management-common/dependent-setup-routing.md);
that provider chooses its supported single-record or bulk/setup-import workflow.

Use this task metadata when invoking those skills:

- Offering: `Goal Management`
- Functional area / Setup Object: `Goal Plan`
- Setup task name: `Goals Value Sets`
- Setup task code: `HRG_MANAGE_GOALS_VALUE_SETS`




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

Use the parent functional-area skill `hcm.goal-management.goal-plan` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.


## Migrated shared routing: Goal Management value sets

# Goal Management Value-Set Routing

## Scope

The **Goal Management Skill Dependencies** baseline identifies the P0
Application Value Set Foundation Skill as a dependency of Review Periods, Goal
Plans, Performance Library Goals, and Development Library Goals. This resource
defines the route for a consultant-supplied exact value-set code.

## Canonical provider

This Goal Plan task contributes product context only. Product validation may
use provider reads, but value-set maintenance remains an independent Apps
Common operation and is never embedded in a Goal Plan payload.

The required external capability is
`core.fusion-api.apps-common.value-sets`, owned by **Common
Applications / ApplCore**. This Goal Management branch does not own,
modify, or create that Core capability. It invokes the declared repository
dependency `core.fusion-api.apps-common` only when that dependency exposes the
required Value Set capability.

Pass the exact supplied value-set code and allow the provider to resolve one
returned `valueSets_Id`. Match only the exact returned value-set code; do not
infer an ID from the code or choose an ambiguous/display-name match.

| Request | Provider behavior |
| --- | --- |
| Read a value-set definition, validation table, or values | Resolve exact code to one returned ID, then read the requested resource |
| Required Value Set capability is unavailable | Return `PROVIDER_SKILL_UNAVAILABLE`; do not create a local replacement |
| Code is missing or ambiguous | Record `validation_gap` with `MISSING` or `AMBIGUOUS`; stop before a child-value operation |
| Create, update, or delete a child value | Use the exact returned parent and child identities, preview current state, and require explicit approval |
| Create or alter a root value-set definition | Return unsupported-route blocker until current Oracle guidance advertises a supported route |

## Product-local boundaries

| Product route | Value-set behavior |
| --- | --- |
| Review Periods | Route any consultant-supplied exact code to the common provider |
| Goal Plans | Route any consultant-supplied exact code to the common provider |
| Performance Library Goals | The Target Outcome `ValueSetName` returned by current subscription metadata remains a `contentItemsLov` selector; exact Foundation value-set work routes to the common provider separately |
| Development Library Goals | The Target Outcome `ValueSetName` returned by current subscription metadata remains a `contentItemsLov` selector; exact Foundation value-set work routes to the common provider separately |

This is not an allowlist. Keep product and value-set work as independent child
routes, with independent approval boundaries.

`PER_EXTRA_INFORMATION_VS` is an example only, not an allowlist. An unfamiliar
exact code follows the same provider resolution contract and returns
`validation_gap` if it cannot be confirmed.

## HCM Foundation FSM source metadata

Preserve the following source references as metadata only. They are not
alternative execution routes, APIs, or local skills:

- Manage Value Sets for Global Human Resources
- Payroll Value Sets
- Time and Labor Value Sets
- Manage Value Sets
- Manage Global Absences Value Sets
