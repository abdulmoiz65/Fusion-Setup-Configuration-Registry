---
skill_id: "hcm.compensation"
name: "Compensation"
description: "Coordinates HCM implementation guidance for the Compensation offering."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Compensation pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "compensation_requirements"
outputs:
  - "offering_scope"
  - "functional_area_skill_plan"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
  - "core.project-mgmt.project-state-manager"
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
  - "scope"
  - "skill_path"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
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

# Compensation

## Purpose

Coordinates implementation work for offering `Compensation` (`ORA_COMPENSATION`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_COMPENSATION`
Functional area count: `15`
Setup task count: `50`

- `ORA_COMPENSATION_COMMON`: [Compensation Common](compensation-common/SKILL.md)
- `ORA_EMPLOYMENT_ACTIONS_FRAMEWORK`: Employment Actions Framework
- `ORA_GRADES`: Grades
- `ORA_DOCUMENT_TYPES`: Document Types
- `ORA_PAYROLL_TOOLS`: Payroll Tools
- `ORA_ELEMENTS_EARNINGS_AND_DEDUCTIONS`: Elements, Earnings and Deductions
- `ORA_PAYROLL_RATES_AND_VALUES`: Payroll Rates and Values
- `ORA_PAYROLL_BALANCES`: Payroll Balances
- `ORA_ABSENCE`: Absence
- `ORA_SALARY_AND_BASE_PAY`: Salary and Base Pay
- `ORA_INDIVIDUAL_COMPENSATION_PLANS_AND_HISTORY`: Individual Compensation Plans and History
- `ORA_WORKFORCE_COMPENSATION_PLAN`: Workforce Compensation Plan
- `ORA_GRADE_STEP_PROGRESSION`: Grade Step Progression
- `ORA_TOTAL_COMPENSATION_STATEMENTS`: Total Compensation Statements
- `ORA_COMPENSATION_DATA_AND_BATCH_CONTROLS`: Compensation Data and Batch Controls
