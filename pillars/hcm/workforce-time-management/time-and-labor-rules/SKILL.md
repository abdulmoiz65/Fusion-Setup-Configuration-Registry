---
skill_id: "hcm.workforce-time-management.time-and-labor-rules"
name: "Time and Labor Rules Implementation Guidance"
description: "Provides HCM Workforce Time Management implementation guidance for the Time and Labor Rules functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Rules"
functional_area_code: "ORA_TIME_AND_LABOR_RULES"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "time_and_labor_rules_scope"
  - "time_and_labor_rules_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_HWM_MANAGE_RULE_SETS"
  - "ORA_HWM_MANAGE_RULE_TEMPLATES"
  - "ORA_HWM_MANAGE_RULES"
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

# Time and Labor Rules Implementation Guidance

## Purpose

Provides HCM Time and Labor implementation guidance for the Time and Labor Rules functional area.

## When to Use

Use this functional-area skill after Time and Labor scope is confirmed and the project needs time and labor rules setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Time Management` (`ORA_WORKFORCE_TIME_MANAGEMENT`)
- Functional area / Setup Object: `Time and Labor Rules` (`ORA_TIME_AND_LABOR_RULES`)

## Setup Tasks

1. [Time Rule Sets](time-rule-sets/SKILL.md) (`ORA_HWM_MANAGE_RULE_SETS`)
2. [Time Rule Templates](time-rule-templates/SKILL.md) (`ORA_HWM_MANAGE_RULE_TEMPLATES`)
3. [Time Rules](time-rules/SKILL.md) (`ORA_HWM_MANAGE_RULES`)

## Inputs

- `implementation_objective`
- `project_context`
- `time_and_labor_rules_scope`
- `time_and_labor_rules_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
