---
skill_id: "hcm.compensation.salary-and-base-pay"
name: "Salary and Base Pay Implementation Guidance"
description: "Provides HCM Compensation implementation guidance for the Salary and Base Pay functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Salary and Base Pay"
functional_area_code: "ORA_SALARY_AND_BASE_PAY"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "salary_and_base_pay_scope"
  - "salary_and_base_pay_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/salary-and-base-pay/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/salary-and-base-pay/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/salary-and-base-pay/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CMP_MANAGE_BASE_PAY_LOOKUPS"
  - "CMP_MANAGE_SALARY_BASIS"
  - "ORA_COMPENSATION_ZONES"
  - "ORA_CMP_MANAGE_SALARY_RANGE_DIFFERENTIALS"
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

# Salary and Base Pay Implementation Guidance

## Purpose

Provides HCM Compensation implementation guidance for the Salary and Base Pay functional area.

## When to Use

Use this functional-area skill after Compensation scope is confirmed and the project needs salary and base pay setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Compensation` (`ORA_COMPENSATION`)
- Functional area / Setup Object: `Salary and Base Pay` (`ORA_SALARY_AND_BASE_PAY`)

## Setup Tasks

1. [Manage Base Pay Lookups](manage-base-pay-lookups/SKILL.md) (`CMP_MANAGE_BASE_PAY_LOOKUPS`)
2. [Salary Basis](salary-basis/SKILL.md) (`CMP_MANAGE_SALARY_BASIS`)
3. [Compensation Zones](compensation-zones/SKILL.md) (`ORA_COMPENSATION_ZONES`)
4. [Salary Range Differentials](salary-range-differentials/SKILL.md) (`ORA_CMP_MANAGE_SALARY_RANGE_DIFFERENTIALS`)

## Inputs

- `implementation_objective`
- `project_context`
- `salary_and_base_pay_scope`
- `salary_and_base_pay_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
