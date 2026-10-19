---
skill_id: "cx.sales.sales-catalog-and-products"
name: "Sales Catalog and Products Implementation Guidance"
description: "Provides CX Sales implementation guidance for the Sales Catalog and Products functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Catalog and Products"
functional_area_code: "ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "sales_catalog_and_products_scope"
  - "sales_catalog_and_products_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-catalog-and-products/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS"
  - "CUSTOM_MANAGE_SALES_FUNCTIONAL_AREA_CATALOG"
  - "CUSTOM_MANAGE_SALES_INDEX"
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

# Sales Catalog and Products Implementation Guidance

## Purpose

Provides CX Sales implementation guidance for the Sales Catalog and Products functional area.

## When to Use

Use this functional-area skill after Sales scope is confirmed and the project needs sales catalog and products setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Sales` (`ORA_MIDSIZE_SALES`)
- Functional area / Setup Object: `Sales Catalog and Products` (`ORA_QSC_DEFINE_SALES_CATALOG_AND_PRODUCTS`)

## Setup Tasks

1. [Manage Product Group Profile Option Values](manage-product-group-profile-option-values/SKILL.md) (`QSC_MANAGE_PRODUCT_GROUP_PROFILE_OPTIONS`)
2. [Manage Sales Functional Area Catalog](manage-sales-functional-area-catalog/SKILL.md) (`CUSTOM_MANAGE_SALES_FUNCTIONAL_AREA_CATALOG`)
3. [Manage Sales Index](manage-sales-index/SKILL.md) (`CUSTOM_MANAGE_SALES_INDEX`)

## Inputs

- `implementation_objective`
- `project_context`
- `sales_catalog_and_products_scope`
- `sales_catalog_and_products_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skill for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
