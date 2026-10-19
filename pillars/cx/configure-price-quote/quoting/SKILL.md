---
skill_id: "cx.configure-price-quote.quoting"
name: "Quoting Implementation Guidance"
description: "Provides CX Configure Price Quote implementation guidance for the Quoting functional area."
layer: "pillar"
pillar: "CX"
offering: "Configure Price Quote"
functional_area: "Quoting"
functional_area_code: "CUSTOM_QUOTING"
type: "planning"
execution_mode: "assisted"
owner_team: "CX configure price quote pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "quoting_scope"
  - "quoting_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/quoting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/quoting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/configure-price-quote/quoting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks: []
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

# Quoting Implementation Guidance

## Purpose

Provides CX Configure Price Quote implementation guidance for the Quoting functional area.

## When to Use

Use this functional-area skill after Configure Price Quote scope is confirmed and the project needs quoting setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Configure Price Quote` (`ORA_CONFIGURE_PRICE_QUOTE`)
- Functional area / Setup Object: `Quoting` (`CUSTOM_QUOTING`)

## Setup Tasks

No Quoting setup-task skill is shipped in this release. Route CPQ Integration
Center administration to the CPQ owner until the supported Data Loader workflow
is available.

See the [26D removal and handoff record](references/26d-integration-skill-removal.md)
for affected capabilities, existing-project handling, and recovery guidance.

## Inputs

- `implementation_objective`
- `project_context`
- `quoting_scope`
- `quoting_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Do not schedule the withdrawn CPQ integration tasks for automated execution in
26D. Record the CPQ-owner handoff and any resulting blocker in the project plan.
Track token usage for any generated project artifact or skill-run record using
the manifest policy.
