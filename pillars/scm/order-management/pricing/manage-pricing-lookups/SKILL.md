---
skill_id: "scm.order-management.pricing.manage-pricing-lookups"
name: "Manage Pricing Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Pricing Lookups under the Pricing functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
task_code: "ORA_QP_MANAGE_PRICING_LOOKUPS"
task_name: "Manage Pricing Lookups"
parent_skill_id: "scm.order-management.pricing"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "pricing_lookup_type"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/pricing/manage-pricing-lookups/current/"
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

# Manage Pricing Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, and import guidance for `Manage Pricing Lookups` under `Pricing`.

## Setup Task Skill Contract

- task_code: `ORA_QP_MANAGE_PRICING_LOOKUPS`
- task_name: `Manage Pricing Lookups`
- parent_skill_id: `scm.order-management.pricing`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Pricing`
- functional_area_code: `ORA_FOM_PRICING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, or importing setup data for `Manage Pricing Lookups` under `Pricing`.

## Setup Task Metadata

- Task name: `Manage Pricing Lookups`
- Task code: `ORA_QP_MANAGE_PRICING_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export and Import Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Lookups`
- Setup task code: `ORA_QP_MANAGE_PRICING_LOOKUPS`

## Apps Common Lookup Routing

Route every lookup-type, lookup-code, translation, or reference-data-set
request through `core.fusion-api.apps-common`. Pass `pricing_lookup_type` as
the exact `LookupType` request field and constrain it to the Standard Lookup
allowlist in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md).
Do not select a direct REST endpoint from this task skill.

Apps Common owns validation of the selected lookup resource and request body.

This task prescribes the supported lookup-type boundary only; it does not
prescribe a lookup code or lookup value. Obtain the exact lookup code and value
from the approved business requirement and applicable Oracle source before
execution.

The Apps Common skill selects its `lookups` child skill and performs lookup-view
routing. Keep Pricing setup-task context and filter conditions with the request.
For a write, it requires the target environment, exact lookup type/code, and
payload, followed by explicit approval immediately before mutation. Do not use
this task skill to infer an unknown lookup type or retry a failed write.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `pricing_lookup_type`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.order-management.pricing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
