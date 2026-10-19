---
skill_id: "hcm.goal-management.goal-plan.worker-goal-descriptive-flexfields"
name: "Worker Goal Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Worker Goal Descriptive Flexfields under the Goal Plan functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Plan"
functional_area_code: "ORA_GOAL_PLAN"
task_code: "HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD"
task_name: "Worker Goal Descriptive Flexfields"
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
  - "core.fusion-api.apps-common.descriptive-flexfields"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/worker-goal-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/worker-goal-descriptive-flexfields/current/"
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

# Worker Goal Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Worker Goal Descriptive Flexfields` under `Goal Plan`.

## Setup Task Skill Contract

- task_code: `HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD`
- task_name: `Worker Goal Descriptive Flexfields`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Worker Goal Descriptive Flexfields` under `Goal Plan`.

## Setup Task Metadata

- Task name: `Worker Goal Descriptive Flexfields`
- Task code: `HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD`
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
- Setup task name: `Worker Goal Descriptive Flexfields`
- Setup task code: `HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD`




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


## Migrated shared routing: Goal Management descriptive flexfields

# Goal Management Flexfield Foundation Routing

This Goal Plan task contributes product context and catalog identity only.
Flexfield export, import, deployment, and setup mutation belong to the Apps
Common Descriptive Flexfields provider and retain a separate approval boundary.

## Ownership and execution boundary

The required external capability is
`core.fusion-api.apps-common.descriptive-flexfields`, owned by
**Common Applications / ApplCore**. This Goal Management branch does not
own, modify, or create that Core capability. It invokes the declared repository
dependency `core.fusion-api.apps-common` only when that dependency exposes the
required Descriptive Flexfield capability. For every Worker Goal Setting caller,
use the exact catalog task
`HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD` (*Worker Goal Descriptive
Flexfields*) in functional area `HRG_WORKER_GOALS`.

The common provider owns task resolution, support-flag checks, task-level CSV
export, validated import package handling, import polling, and durable process
diagnostics. Do not configure a DFF through an HCM business-object REST
payload, a `libraryGoals` child payload, or a direct Fusion REST route.

## Confirmed environment evidence

The supplied Goal Management **Manage Descriptive Flexfields** view shows the
following deployed Repository DFFs. This is a code register for routing and
verification, not a segment-mapping contract and not an allowlist.

| Exact flexfield code | Display name | Screenshot evidence | Product routes that may request it |
| --- | --- | --- | --- |
| `HRG_GOALS` | `HRG_GOALS` | Descriptive Flexfield; deployed successfully; description begins “Worker Goals and alignm...” | Review Periods, Goal Plans, Performance Library Goals, Development Library Goals |
| `HRG_GOAL_ACCESS` | `HRG_GOAL_ACCESS` | Descriptive Flexfield; deployed successfully; description begins “Access provided by work...” | Review Periods, Goal Plans, Performance Library Goals, Development Library Goals |
| `HRG_GOAL_PLANS_B` | `HRG_GOAL_PLANS_B` | Descriptive Flexfield; deployed successfully; description “Goal Plan details” | Review Periods, Goal Plans, Performance Library Goals, Development Library Goals |

A consultant-supplied exact DFF code that is not listed above must still route
to the common provider. Do not infer a code from a display name, truncated
description, object name, or a segment label.

`PER_RATES_DF` is an example only, not an allowlist. It follows the same exact
code verification rule as every consultant-supplied DFF code.

## Required routing contract

| Input | Required for | Rule |
| --- | --- | --- |
| `flexfield_code` | Every DFF request | Exact code only; reject display-name or partial-code matching. |
| `flexfield_operation` | Every DFF request | `export`, `inspect`, or `import`; classify `inspect` as read-only. |
| `flexfield_context_code` | Context-specific request | Retain only as a requested filter; verify it against current configuration. |
| `flexfield_segment_code` | Segment-specific request | Retain only as a requested filter; verify it against current configuration. |
| `flexfield_setup_task_csv_zip` | Import | Require a validated package for the exact resolved task. |

Before export or import, resolve the exact task and verify both
`ExportImportSupportedFlag=Y` and `CSVExportImportSupportedFlag=Y`. The local
catalog currently records both values as `Y`, but current task resolution must
repeat the gate for each run.

## Product and DFF split rules

When a request contains a Goal Management product operation and a DFF request,
create two independent child routes:

1. the selected product task; and
2. `core.fusion-api.apps-common` for the DFF task.

Product `dff_changes` describes data on an already configured runtime object.
It is allowed only when current runtime metadata confirms the exact writable
attribute and the caller requested it explicitly. It never authorizes DFF
configuration, deployment, segment maintenance, or a setup-data import.

DFF export/inspection can proceed after normal read readiness. A DFF import
requires the common provider's exact package preview and a fresh explicit
approval for the named environment and package, separate from any product
object approval. If the current configuration does not establish the supplied
code, context, or segment uniquely, return `catalog_or_metadata_mismatch` and
`validation_gap` and stop without guessing. If the declared provider capability
is unavailable, return `PROVIDER_SKILL_UNAVAILABLE`; do not create a local
replacement.

## HCM Foundation FSM source metadata

Preserve the following source references as metadata only. They are not
alternative execution routes, APIs, or local skills. The Application Flexfield
Foundation prompt routes Descriptive Flexfield work only; Extensible and Key
Flexfield entries below do not authorize local inferred operations.

- Manage Organization Structure Descriptive Flexfields
- Manage Organization Structure Extensible Flexfields
- Manage Grade Descriptive Flexfields
- Manage Workforce Structures Descriptive Flexfields
- Manage Workforce Structures Extensible Flexfields
- Manage Person Descriptive Flexfields
- Manage Person Extensible Flexfield
- Manage Employment Descriptive Flexfields
- Manage Employment Extensible Flexfields
- Manage Key Flexfields
- Document Records Descriptive Flexfields
- Document Type Descriptive Flexfields
- Descriptive Flexfields for Payroll
- Extensible Flexfields for Payroll
- Manage Descriptive Flexfields
- Manage Extensible Flexfields
