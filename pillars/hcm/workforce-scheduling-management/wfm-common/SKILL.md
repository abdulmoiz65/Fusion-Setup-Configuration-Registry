---
skill_id: "hcm.workforce-scheduling-management.wfm-common"
name: "WFM Common Implementation Guidance"
description: "Provides HCM Workforce Scheduling Management implementation guidance for the WFM Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
functional_area: "WFM Common"
functional_area_code: "ORA_WFM_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce scheduling management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "wfm_common_scope"
  - "wfm_common_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/wfm-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/wfm-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/wfm-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_HTS_MANAGE_SHIFTS"
  - "ORA_HTS_WORK_PATTERN_TEMPLATES"
  - "PER_MANAGE_CALENDAR_EVENT"
  - "ORA_HWM_MANAGE_REPEATING_PERIODS"
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

# WFM Common Implementation Guidance

## Purpose

Provides HCM Workforce Scheduling implementation guidance for the WFM Common functional area.

## When to Use

Use this functional-area skill after Workforce Scheduling scope is confirmed and the project needs wfm common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Scheduling Management` (`ORA_WORKFORCE_SCHEDULING_MANAGEMENT`)
- Functional area / Setup Object: `WFM Common` (`ORA_WFM_COMMON`)

## Setup Tasks

1. [Enterprise Shifts](enterprise-shifts/SKILL.md) (`ORA_HTS_MANAGE_SHIFTS`)
2. [Work Pattern Templates](work-pattern-templates/SKILL.md) (`ORA_HTS_WORK_PATTERN_TEMPLATES`)
3. [Manage Calendar Events](manage-calendar-events/SKILL.md) (`PER_MANAGE_CALENDAR_EVENT`)
4. [Repeating Time Periods](repeating-time-periods/SKILL.md) (`ORA_HWM_MANAGE_REPEATING_PERIODS`)

## Inputs

- `implementation_objective`
- `project_context`
- `wfm_common_scope`
- `wfm_common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
