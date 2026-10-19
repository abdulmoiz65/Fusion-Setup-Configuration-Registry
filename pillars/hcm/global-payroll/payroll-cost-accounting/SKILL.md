---
skill_id: "hcm.global-payroll.payroll-cost-accounting"
name: "Payroll Cost Accounting Implementation Guidance"
description: "Provides HCM Global Payroll implementation guidance for the Payroll Cost Accounting functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Cost Accounting"
functional_area_code: "ORA_PAYROLL_COSTING"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "payroll_cost_accounting_scope"
  - "payroll_cost_accounting_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-cost-accounting/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PAY_MANAGE_KEY_FLEXFIELD_FOR_COST_ALLOCATION"
  - "PAY_MANAGE_DEPARTMENT_COSTING"
  - "PAY_MANAGE_ELEMENT_CRITERIA_COSTING"
  - "PAY_MANAGE_JOB_COSTING"
  - "ORA_COSTING_OF_LOCATIONS"
  - "PAY_MANAGE_PAYMENT_SOURCE_COSTING"
  - "PAY_MANAGE_PAYROLL_COSTING"
  - "PAY_MANAGE_POSITION_COSTING"
  - "ORA_PAY_PAYROLL_COSTING_VALUE_SETS"
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

# Payroll Cost Accounting Implementation Guidance

## Purpose

Provides HCM Payroll implementation guidance for the Payroll Cost Accounting functional area.

## When to Use

Use this functional-area skill after Payroll scope is confirmed and the project needs payroll costing setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Payroll` (`ORA_GLOBAL_PAYROLL`)
- Functional area / Setup Object: `Payroll Cost Accounting` (`ORA_PAYROLL_COSTING`)

## Setup Tasks

1. [Cost Allocation Key Flexfield](cost-allocation-key-flexfield/SKILL.md) (`PAY_MANAGE_KEY_FLEXFIELD_FOR_COST_ALLOCATION`)
2. [Costing of Departments](costing-of-departments/SKILL.md) (`PAY_MANAGE_DEPARTMENT_COSTING`)
3. [Costing of Elements](costing-of-elements/SKILL.md) (`PAY_MANAGE_ELEMENT_CRITERIA_COSTING`)
4. [Costing of Jobs](costing-of-jobs/SKILL.md) (`PAY_MANAGE_JOB_COSTING`)
5. [Costing of Locations](costing-of-locations/SKILL.md) (`ORA_COSTING_OF_LOCATIONS`)
6. [Costing of Payment Sources](costing-of-payment-sources/SKILL.md) (`PAY_MANAGE_PAYMENT_SOURCE_COSTING`)
7. [Costing of Payrolls](costing-of-payrolls/SKILL.md) (`PAY_MANAGE_PAYROLL_COSTING`)
8. [Costing of Positions](costing-of-positions/SKILL.md) (`PAY_MANAGE_POSITION_COSTING`)
9. [Payroll Costing Value Sets](payroll-costing-value-sets/SKILL.md) (`ORA_PAY_PAYROLL_COSTING_VALUE_SETS`)

## Inputs

- `implementation_objective`
- `project_context`
- `payroll_costing_scope`
- `payroll_costing_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
