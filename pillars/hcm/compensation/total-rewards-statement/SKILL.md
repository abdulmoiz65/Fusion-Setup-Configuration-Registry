---
skill_id: "hcm.compensation.total-rewards-statement"
name: "Total Rewards Statement Implementation Guidance"
description: "Provides HCM Compensation implementation guidance for the Total Rewards Statement functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Total Rewards Statement"
functional_area_code: "ORA_TOTAL_REWARDS_STATEMENT"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "total_rewards_statement_scope"
  - "total_rewards_statement_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/total-rewards-statement/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/total-rewards-statement/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/total-rewards-statement/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CMS_MANAGE_COMPENSATION_ITEMS"
  - "CMS_MANAGE_COMPENSATION_CATEGORIES"
  - "CMS_MANAGE_GLOBAL_OPTIONS"
  - "CMS_MANAGE_STATEMENT_DEFINITIONS"
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

# Total Compensation Statements Implementation Guidance

## Purpose

Provides HCM Compensation implementation guidance for the Total Compensation Statements functional area.

## When to Use

Use this functional-area skill after Compensation scope is confirmed and the project needs total compensation statements setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Compensation` (`ORA_COMPENSATION`)
- Functional area / Setup Object: `Total Compensation Statements` (`ORA_TOTAL_COMPENSATION_STATEMENTS`)

## Setup Tasks

1. [Compensation Items](compensation-items/SKILL.md) (`CMS_MANAGE_COMPENSATION_ITEMS`)
2. [Compensation Categories](compensation-categories/SKILL.md) (`CMS_MANAGE_COMPENSATION_CATEGORIES`)
3. [Configure Global Settings](configure-global-settings/SKILL.md) (`CMS_MANAGE_GLOBAL_OPTIONS`)
4. [Statement Definitions](statement-definitions/SKILL.md) (`CMS_MANAGE_STATEMENT_DEFINITIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `total_compensation_statements_scope`
- `total_compensation_statements_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
