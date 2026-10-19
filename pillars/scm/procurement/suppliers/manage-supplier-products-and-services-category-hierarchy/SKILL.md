---
skill_id: "scm.procurement.suppliers.manage-supplier-products-and-services-category-hierarchy"
name: "Manage Supplier Products and Services Category Hierarchy Setup Task Guidance"
description: "Supplier category hierarchy placeholder that delegates execution to Manage Procurement Category Hierarchy."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "POR_MANAGE_SUPPLIER_PRODUCTS_AND_SERVICES_CATEGORY_HIERARCHY"
task_name: "Manage Supplier Products and Services Category Hierarchy"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.4"
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
  - "scm.procurement.procurement-foundation.manage-procurement-category-hierarchy"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-supplier-products-and-services-category-hierarchy/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-supplier-products-and-services-category-hierarchy/current/"
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

# Manage Supplier Products and Services Category Hierarchy Setup Task Guidance

## Purpose

Provide a supplier-facing placeholder for `Manage Supplier Products and Services Category Hierarchy` that delegates execution to [Manage Procurement Category Hierarchy](../../procurement-foundation/manage-procurement-category-hierarchy/SKILL.md).

## Delegated Execution

Invoke `scm.procurement.procurement-foundation.manage-procurement-category-hierarchy` with the supplied objective, project context, supplier category scope, setup-task identity, and artifacts. Let that skill determine the required inputs, execution route, validation, approvals, and next steps. Return its results for this supplier task; do not duplicate its workflow here.

Preserve the supplier task identity `POR_MANAGE_SUPPLIER_PRODUCTS_AND_SERVICES_CATEGORY_HIERARCHY` throughout delegation. The delegated skill's own task code is not interchangeable with this supplier task. The delegate must confirm that its workflow supports the supplied supplier scope and task identity before execution; if it does not, report the delegation gap instead of executing a different setup task.

## Setup Task Skill Contract

- task_code: `POR_MANAGE_SUPPLIER_PRODUCTS_AND_SERVICES_CATEGORY_HIERARCHY`
- task_name: `Manage Supplier Products and Services Category Hierarchy`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill for supplier category hierarchy setup delegated to Manage Procurement Category Hierarchy.

## Setup Task Metadata

- Task name: `Manage Supplier Products and Services Category Hierarchy`
- Task code: `POR_MANAGE_SUPPLIER_PRODUCTS_AND_SERVICES_CATEGORY_HIERARCHY`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported through the delegated workflow`
- Data Loader import mode: `FSM`
- Business Object: ``

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

Use the parent functional-area skill `scm.procurement.suppliers` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
