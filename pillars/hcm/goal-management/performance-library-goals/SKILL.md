---
skill_id: "hcm.goal-management.performance-library-goals"
name: "Performance Library Goals Implementation Guidance"
description: "Provides HCM Goal Management implementation guidance for the Performance Library Goals functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Performance Library Goals"
functional_area_code: "ORA_PERFORMANCE_LIBRARY_GOALS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "performance_library_goals_scope"
  - "performance_library_goals_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/performance-library-goals/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/performance-library-goals/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/performance-library-goals/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRG_MANAGE_GOAL_LIBRARY"
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

# Performance Library Goals Implementation Guidance

## Purpose

Provides HCM Goal Management implementation guidance for the Performance Library Goals functional area.

## When to Use

Use this functional-area skill after Goal Management scope is confirmed and the project needs performance library goals setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Goal Management` (`ORA_GOAL_MANAGEMENT`)
- Functional area / Setup Object: `Performance Library Goals` (`ORA_PERFORMANCE_LIBRARY_GOALS`)

## Setup Tasks

1. [Goal Library](goal-library/SKILL.md) (`HRG_MANAGE_GOAL_LIBRARY`)

## Inputs

- `implementation_objective`
- `project_context`
- `performance_library_goals_scope`
- `performance_library_goals_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
