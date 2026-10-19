---
skill_id: "cx.subscriptions.foundation-setup"
name: "Foundation Setup Implementation Guidance"
description: "Provides CX Subscriptions implementation guidance for the Foundation Setup functional area."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Foundation Setup"
functional_area_code: "CUSTOM_FOUNDATION_SETUP"
type: "planning"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "foundation_setup_scope"
  - "foundation_setup_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/foundation-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/foundation-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/foundation-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_SUBSCRIPTION_PROFILES"
  - "CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS"
  - "CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET"
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

# Foundation Setup Implementation Guidance

## Purpose

Provides CX Subscriptions implementation guidance for the Foundation Setup functional area.

## When to Use

Use this functional-area skill after Subscriptions scope is confirmed and the project needs foundation setup setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`)
- Functional area / Setup Object: `Foundation Setup` (`CUSTOM_FOUNDATION_SETUP`)

## Setup Tasks

1. [Manage Subscription Profiles](manage-subscription-profiles.md) (`CUSTOM_MANAGE_SUBSCRIPTION_PROFILES`)
2. [Manage Subscription Validations](manage-subscription-validations.md) (`CUSTOM_MANAGE_SUBSCRIPTION_VALIDATIONS`)
3. [Event Notification Rules and Templates Set](event-notification-rules-and-templates-set.md) (`CUSTOM_EVENT_NOTIFICATION_RULES_AND_TEMPLATES_SET`)

## Request Routing

Route every request whose primary object is a **Subscription Profile** or
**Subscription Profiles** to [Manage Subscription Profiles](manage-subscription-profiles.md)
(`CUSTOM_MANAGE_SUBSCRIPTION_PROFILES`), including queries, lookups, lists,
reviews, creation, updates, and Data Loader workbook requests.

For a query, lookup, list, or review, use the task's declared read-only
`list_subscription_profiles` lookup. For creation, update, or import, use the
task's declared `core.data-loader` route; do not construct a writable REST
request. Do not treat **Balance Profile** as a synonym because it belongs to
Usage Rating Setup and has a separate task and object model.

## Inputs

- `implementation_objective`
- `project_context`
- `foundation_setup_scope`
- `foundation_setup_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
