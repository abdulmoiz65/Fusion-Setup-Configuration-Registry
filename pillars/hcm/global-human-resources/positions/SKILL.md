---
skill_id: "hcm.global-human-resources.positions"
name: "Positions Implementation Guidance"
description: "Provides HCM Global Human Resources implementation guidance for the Positions functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Positions"
functional_area_code: "ORA_POSITIONS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "positions_scope"
  - "positions_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PER_MANAGE_POSITION"
  - "ORA_PER_MANAGE_HCM_POSITION_HIERARCHY"
  - "CUSTOM_POSITION_BUDGETS"
  - "ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING"
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

# Positions Implementation Guidance

## Purpose

Provides HCM Global Human Resources implementation guidance for the Positions functional area.

## When to Use

Use this functional-area skill after Global Human Resources scope is confirmed and the project needs positions setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Human Resources` (`ORA_GLOBAL_HUMAN_RESOURCES`)
- Functional area / Setup Object: `Positions` (`ORA_POSITIONS`)

## Setup Tasks

1. [Manage Positions](manage-positions/SKILL.md) (`PER_MANAGE_POSITION`)
2. [Manage HCM Position Hierarchy](manage-hcm-position-hierarchy/SKILL.md) (`ORA_PER_MANAGE_HCM_POSITION_HIERARCHY`)
3. [Position Budgets](position-budgets/SKILL.md) (`CUSTOM_POSITION_BUDGETS`)
4. [Manage Assignment Flexfield Mapping](manage-assignment-flexfield-mapping/SKILL.md) (`ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING`)

## Inputs

- `implementation_objective`
- `project_context`
- `positions_scope`
- `positions_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Conditional Cross-Skill Coordination

For planning only, when the requested position outcome uses organizational, location, job, or grade context, coordinate with [Legal and Legislative Organizations](../legal-and-legislative-organizations/SKILL.md), [Departments](../departments/SKILL.md), [Locations](../locations/SKILL.md), [Jobs](../jobs/SKILL.md), and [Grades](../grades/SKILL.md). These are not manifest dependencies or execution gates; resolve only the references required by the requested setup.

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
