---
skill_id: "hcm.global-payroll"
name: "Global Payroll"
description: "Coordinates HCM implementation guidance for the Global Payroll offering."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Global Payroll pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "global_payroll_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/current/"
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

# Global Payroll

## Purpose

Coordinates implementation work for offering `Global Payroll` (`ORA_GLOBAL_PAYROLL`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_GLOBAL_PAYROLL`
Functional area count: `20`
Setup task count: `106`

- `ORA_PAYROLL_COMMON`: Payroll Common
- `ORA_PAYROLL_ENTERPRISE`: Payroll Enterprise
- `ORA_PAYROLL_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Payroll Legal and Legislative Organizations
- `ORA_PAYROLL_DEFINITION_AND_CALENDAR`: Payroll Definition and Calendar
- `ORA_ELEMENTS_EARNINGS_AND_DEDUCTIONS`: Elements, Earnings and Deductions
- `ORA_PAYROLL_HCM_SECURITY_PROFILE`: Payroll HCM Security Profile
- `ORA_PAYROLL_HCM_DATA_ROLE`: Payroll HCM Data Role
- `ORA_PAYROLL_CHART_OF_ACCOUNTS`: Payroll Chart of Accounts
- `ORA_PAYROLL_LEDGER_STRUCTURE`: Payroll Ledger Structure
- `ORA_PAYROLL_BANKING_AND_PAYMENTS`: Payroll Banking and Payments
- `ORA_PAYROLL_TOOLS`: Payroll Tools
- `ORA_LEGISLATION_AND_COUNTRY_EXTENSION`: Legislation and Country Extension
- `ORA_PAYROLL_PROCESS_RULE_AND_FLOW`: Payroll Process Rule and Flow
- `ORA_HCM_EXTRACT`: HCM Extract
- `ORA_PAYROLL_ORGANIZATION_CARDS`: Payroll Organization Cards
- `ORA_PAYROLL_RATES_AND_VALUES`: Payroll Rates and Values
- `ORA_CALCULATION_CARDS_AND_CALCULATION_VALUES`: Calculation Cards and Calculation Values
- `ORA_PAYROLL_BALANCES`: Payroll Balances
- `ORA_PAYROLL_COSTING`: Payroll Cost Accounting
- `ORA_PAYROLL_PAYMENTS_AND_PAYSLIP`: Payroll Payments and Payslip
