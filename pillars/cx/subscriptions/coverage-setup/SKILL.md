---
skill_id: "cx.subscriptions.coverage-setup"
name: "Coverage Setup Implementation Guidance"
description: "Provides CX Subscriptions implementation guidance for the Coverage Setup functional area."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Coverage Setup"
functional_area_code: "CUSTOM_COVERAGE_SETUP"
type: "planning"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "coverage_setup_scope"
  - "coverage_setup_requirements"
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
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/coverage-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/coverage-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/coverage-setup/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_STANDARD_COVERAGE"
  - "CUSTOM_MANAGE_AVAILABILITY"
  - "CUSTOM_MANAGE_DEFAULT_COVERAGE"
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

# Coverage Setup Implementation Guidance

## Purpose

Provides CX Subscriptions implementation guidance for the Coverage Setup functional area.

## When to Use

Use this functional-area skill after Subscriptions scope is confirmed and the project needs coverage setup setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Subscriptions` (`CUSTOM_SUBSCRIPTIONS`)
- Functional area / Setup Object: `Coverage Setup` (`CUSTOM_COVERAGE_SETUP`)

## Setup Tasks

1. [Manage Standard Coverage](manage-standard-coverage.md) (`CUSTOM_MANAGE_STANDARD_COVERAGE`)
2. [Manage Availability](manage-availability.md) (`CUSTOM_MANAGE_AVAILABILITY`)
3. [Manage Default Coverage](manage-default-coverage.md) (`CUSTOM_MANAGE_DEFAULT_COVERAGE`)

## Inputs

- `implementation_objective`
- `project_context`
- `coverage_setup_scope`
- `coverage_setup_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
