---
skill_id: "cx.sales-marketing.customer-center"
name: "Customer Center Implementation Guidance"
description: "Provides CX Sales Marketing implementation guidance for the Customer Center functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales Marketing"
functional_area: "Customer Center"
functional_area_code: "CSC_CUST_CENTER"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales marketing pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "customer_center_scope"
  - "customer_center_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales-marketing/customer-center/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales-marketing/customer-center/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales-marketing/customer-center/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ZCC_MANAGE_CTD_PROFILE_OPTIONS"
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

# Customer Center Implementation Guidance

## Purpose

Provides CX Sales Marketing implementation guidance for the Customer Center functional area.

## When to Use

Use this functional-area skill after Sales Marketing scope is confirmed and the project needs customer center setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Sales Marketing` (`MKT_MARKETING`)
- Functional area / Setup Object: `Customer Center` (`CSC_CUST_CENTER`)

## Setup Tasks

1. [Manage Contact Center Profile Options](manage-contact-center-profile-options/SKILL.md) (`ZCC_MANAGE_CTD_PROFILE_OPTIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `customer_center_scope`
- `customer_center_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
