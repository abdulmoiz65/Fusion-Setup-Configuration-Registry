---
skill_id: "cx.subscriptions.billing-setup"
name: "Billing Setup Implementation Guidance"
description: "Provides CX Subscriptions implementation guidance for the Billing Setup functional area."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Billing Setup"
functional_area_code: "CUSTOM_BILLING_SETUP"
type: "planning"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "billing_setup_scope"
  - "billing_setup_requirements"
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
  - "shared.validation.setup-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/billing-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/billing-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/billing-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_PRICE_ADJUSTMENTS"
  - "CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES"
  - "CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION"
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

# Billing Setup Implementation Guidance

## Purpose

Provides CX Subscriptions implementation guidance for the Billing Setup functional area.

## When to Use

Use this functional-area skill after Subscriptions scope is confirmed and the project needs billing setup setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`)
- Functional area / Setup Object: `Billing Setup` (`CUSTOM_BILLING_SETUP`)

## Setup Tasks

1. [Manage Price Adjustments](manage-price-adjustments.md) (`CUSTOM_MANAGE_PRICE_ADJUSTMENTS`)
2. [Manage Price Adjustment Variables](manage-price-adjustment-variables.md) (`CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES`)
3. [Manage Milestone Templates for Billing and Revenue Recognition](manage-milestone-templates-for-billing-and-revenue-recognition.md) (`CUSTOM_MANAGE_MILESTONE_TEMPLATES_FOR_BILLING_AND_REVENUE_RECOGNITION`)

## Terminology-Based Routing

Route `Track Price Adjustment Variables`, `Advanced Pricing Term Variables`, `Flexible Pricing Term Option`, and `Formula Driven Flexible Pricing Term Adjustments` to [Manage Price Adjustment Variables](manage-price-adjustment-variables.md) (`CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES`). Treat these terms as synonyms for the same Billing Setup task.

## Inputs

- `implementation_objective`
- `project_context`
- `billing_setup_scope`
- `billing_setup_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
