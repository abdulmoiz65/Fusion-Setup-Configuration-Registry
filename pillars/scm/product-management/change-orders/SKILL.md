---
skill_id: "scm.product-management.change-orders"
name: "Change Orders Implementation Guidance"
description: "Provides SCM Product Management implementation guidance for the Change Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Change Orders"
functional_area_code: "EGO_CHANGE_ORDERS"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "change_orders_scope"
  - "change_orders_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "EGO_MANAGE_CHANGE_PRIORITIES"
  - "EGO_MANAGE_CHANGE_REASONS"
  - "ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP"
  - "EGO_MANAGE_CHANGE_ORDER_DFFS"
  - "EGO_MANAGE_CHANGE_ORDER_LINES_DFFS"
  - "ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES"
  - "EGO_MANAGE_CHANGE_STATUSES"
  - "CUSTOM_EGP_FBDI_IMPORT_CHANGE_ORDERS"
  - "EGO_MANAGE_CHANGE_ORDER_TYPES"
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

# Change Orders Implementation Guidance

## Purpose

Provides SCM Product Management implementation guidance for the Change Orders functional area.

## When to Use

Use this functional-area skill after Product Management scope is confirmed and the project needs change orders setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Product Management` (`PIM_PROD_MNG`)
- Functional area / Setup Object: `Change Orders` (`EGO_CHANGE_ORDERS`)
- Effective task-index source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

The task index uses the effective catalog, including the catalog-backed custom
`CUSTOM_EGP_FBDI_IMPORT_CHANGE_ORDERS` task. Use that effective source for
Change Orders task discovery when it differs from an offering-level release
catalog snapshot.

## Setup Tasks

1. [Manage Change Priorities](manage-change-priorities.md) (`EGO_MANAGE_CHANGE_PRIORITIES`)
2. [Manage Change Reasons](manage-change-reasons.md) (`EGO_MANAGE_CHANGE_REASONS`)
3. [Manage Workflow Rejection Reasons](manage-workflow-rejection-reasons.md) (`ORA_MANAGE_WORKFLOW_REJECT_REASON_LOOKUP`)
4. [Manage Change Order and New Item Request Header Descriptive Flexfields](manage-change-order-and-new-item-request-header-descriptive-flexfields/SKILL.md) (`EGO_MANAGE_CHANGE_ORDER_DFFS`)
5. [Manage Change Order and New Item Request Line Descriptive Flexfields](manage-change-order-and-new-item-request-line-descriptive-flexfields/SKILL.md) (`EGO_MANAGE_CHANGE_ORDER_LINES_DFFS`)
6. [Manage Change Attribute Groups and Attributes](manage-change-attribute-groups-and-attributes/SKILL.md) (`ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`)
7. [Manage Change Statuses](manage-change-statuses/SKILL.md) (`EGO_MANAGE_CHANGE_STATUSES`)
8. [Change Orders Import](change-orders-import/SKILL.md) (`CUSTOM_EGP_FBDI_IMPORT_CHANGE_ORDERS`)
9. [Manage Change Order Types](manage-change-order-types/SKILL.md) (`EGO_MANAGE_CHANGE_ORDER_TYPES`)

## Inputs

- `implementation_objective`
- `project_context`
- `change_orders_scope`
- `change_orders_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
