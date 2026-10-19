---
skill_id: "cx.sales.sales-foundation"
name: "Sales Foundation Implementation Guidance"
description: "Provides CX Sales implementation guidance for the Sales Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Foundation"
functional_area_code: "ORA_ZBS_SALES_FOUNDATION"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "sales_foundation_scope"
  - "sales_foundation_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_ZMM_MANAGE_ACTIVITY_TYPE_SUBTYPE"
  - "ORA_ZMM_MANAGE_ACTIVITY_PROFILE_OPTIONS"
  - "ZBS_MANAGE_SALES_NOTE_TYPE"
  - "ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING"
  - "ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS"
  - "ORA_CONFIGURE_ELASTIC_SEARCHES"
  - "FND_MANAGE_AUDIT_POLICIES"
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

# Sales Foundation Implementation Guidance

## Purpose

Provides CX Sales implementation guidance for the Sales Foundation functional area.

## When to Use

Use this functional-area skill after Sales scope is confirmed and the project needs sales foundation setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Sales` (`ORA_MIDSIZE_SALES`)
- Functional area / Setup Object: `Sales Foundation` (`ORA_ZBS_SALES_FOUNDATION`)

## Setup Tasks

1. [Manage Activity Type and Subtype](manage-activity-type-and-subtype/SKILL.md) (`ORA_ZMM_MANAGE_ACTIVITY_TYPE_SUBTYPE`)
2. [Manage Activity Profile Options](manage-activity-profile-options/SKILL.md) (`ORA_ZMM_MANAGE_ACTIVITY_PROFILE_OPTIONS`)
3. [Manage Sales Note Type](manage-sales-note-type/SKILL.md) (`ZBS_MANAGE_SALES_NOTE_TYPE`)
4. [Manage Sales Note Type Mapping](manage-sales-note-type-mapping/SKILL.md) (`ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING`)
5. [Manage Activity Standard Lookups](manage-activity-standard-lookups/SKILL.md) (`ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS`)
6. [Configure Adaptive Search](configure-adaptive-search/SKILL.md) (`ORA_CONFIGURE_ELASTIC_SEARCHES`)
7. [Manage Audit Policies](manage-audit-policies/SKILL.md) (`FND_MANAGE_AUDIT_POLICIES`)

## Inputs

- `implementation_objective`
- `project_context`
- `sales_foundation_scope`
- `sales_foundation_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Execution Route Selection

Select an execution route from the requester’s explicit instruction; do not infer a browser-driven UI action from a create or update request.

- For `Manage Activity Profile Options`, route Inventory and Review through its export-reconciliation plus Apps Common read contract, and route every configured-value Create, Update, Delete, Set, Remove, or BulkSet through `core.fusion-api.apps-common`. The task's FSM/CSV catalog flags do not authorize a profile-value mutation package.
- For `Manage Activity Standard Lookups`, route Review through exact Apps Common reads and route lookup-code Create, Update, Deactivate, or safe Delete through `core.fusion-api.apps-common`. The task's FSM/CSV catalog flags do not make Data Loader the default lookup-code CRUD route; use its package workflow only for an explicit Export, Import, or supported translation request.
- For `Manage Audit Policies`, route Account, Contact, Household, and their live-resolved child-object audit checks or approved mutations through `manage-audit-policies/SKILL.md`, which delegates all Fusion operations to `core.fusion-api.audit-setup`. Do not substitute the task's wider FSM/CSV route for these audit-policy operations.
- For other tasks, an explicit CSV, FSM, Data Loader, import, or bulk-maintenance request uses the task-specific current package and routes through `shared.setup-export.task-level-export`, both shared validators, and `core.data-loader`.
- For other tasks, an explicit manual or guided-UI request uses the documented setup-task procedure. Browser control is not an alternate import adapter and must not replace the selected Data Loader route.
- If a requested mutation for another task does not name a route, prepare the validated plan and request a route selection before attempting a live action.
- `Manage Sales Note Type` (`ZBS_MANAGE_SALES_NOTE_TYPE`) uses FSM as its Data Loader import mode.
