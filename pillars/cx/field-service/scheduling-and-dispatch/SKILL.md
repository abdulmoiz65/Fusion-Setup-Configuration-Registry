---
skill_id: "cx.field-service.scheduling-and-dispatch"
name: "Scheduling and Dispatch Implementation Guidance"
description: "Provides CX Field Service implementation guidance for the Scheduling and Dispatch functional area."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Scheduling and Dispatch"
functional_area_code: "ORA_FFS_FA_SCHEDULING_AND_DISPATCH"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX field service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "scheduling_and_dispatch_scope"
  - "scheduling_and_dispatch_requirements"
  - "task_skill_id"
  - "execution_direction"
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
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/scheduling-and-dispatch/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/scheduling-and-dispatch/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/scheduling-and-dispatch/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_FFS_TS_RESOURCE_TYPES"
  - "ORA_FFS_TS_WORK_SKILLS"
  - "ORA_FFS_TS_WORK_ZONES"
  - "ORA_FFS_TS_TIME_SLOTS"
  - "ORA_FFS_TS_ACTIVITY_TYPES"
  - "ORA_FFS_TS_SHIFTS_AND_SCHEDULES"
  - "ORA_FFS_TS_LINK_TEMPLATES"
  - "ORA_FFS_TS_ORGANIZATIONS"
  - "ORA_FFS_FIELD_RESOURCES"
  - "ORA_FFS_TS_FILTERS"
  - "ORA_RCL_FIELD_SERVICE_TECHNICIANS"
  - "ORA_RCL_RESOURCE_TO_ITEM_MAPPING"
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

# Scheduling and Dispatch Implementation Guidance

## Purpose

Provides CX Field Service implementation guidance for the Scheduling and Dispatch functional area.

## When to Use

Use this functional-area skill after Field Service scope is confirmed and the project needs scheduling and dispatch setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Field Service` (`ORA_FIELD_SERVICE`)
- Functional area / Setup Object: `Scheduling and Dispatch` (`ORA_FFS_FA_SCHEDULING_AND_DISPATCH`)

## Setup Tasks

1. [Resource Types](resource-types/SKILL.md) (`ORA_FFS_TS_RESOURCE_TYPES`)
2. [Work Skills](work-skills/SKILL.md) (`ORA_FFS_TS_WORK_SKILLS`)
3. [Work Zones](work-zones/SKILL.md) (`ORA_FFS_TS_WORK_ZONES`)
4. [Time Slots](time-slots/SKILL.md) (`ORA_FFS_TS_TIME_SLOTS`)
5. [Activity Types](activity-types/SKILL.md) (`ORA_FFS_TS_ACTIVITY_TYPES`)
6. [Shifts and Schedules](shifts-and-schedules/SKILL.md) (`ORA_FFS_TS_SHIFTS_AND_SCHEDULES`)
7. [Link Templates](link-templates/SKILL.md) (`ORA_FFS_TS_LINK_TEMPLATES`)
8. [Organizations](organizations/SKILL.md) (`ORA_FFS_TS_ORGANIZATIONS`)
9. [Field Resources](field-resources/SKILL.md) (`ORA_FFS_FIELD_RESOURCES`)
10. [Filters](filters/SKILL.md) (`ORA_FFS_TS_FILTERS`)
11. [Field Service Technicians](field-service-technicians/SKILL.md) (`ORA_RCL_FIELD_SERVICE_TECHNICIANS`)
12. [Resource to Item Mapping](resource-to-item-mapping/SKILL.md) (`ORA_RCL_RESOURCE_TO_ITEM_MAPPING`)

## Shared Task Orchestration

The Field Service pillar's [`scripts/task_orchestration.py`](../scripts/task_orchestration.py)
owns the common task workflow: validation, direction handoff, immutable preview,
checksum-bound approval, ordered write, verification, and safe failure handling.
A task-local `scripts/task_adapter.py` owns only its workbook mapping, reference
lookups, payload construction, and business-field verification. Do not add task
rules to the shared runner.

## Inputs

- `implementation_objective`
- `project_context`
- `scheduling_and_dispatch_scope`
- `scheduling_and_dispatch_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
