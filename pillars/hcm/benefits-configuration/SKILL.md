---
skill_id: "hcm.benefits-configuration"
name: "Benefits Configuration"
description: "Coordinates HCM implementation guidance for the Benefits Configuration offering."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "benefits_configuration_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/current/"
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

# Benefits Configuration

## Purpose

Coordinates implementation work for offering `Benefits Configuration` (`ORA_BENEFITS_CONFIG`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_BENEFITS_CONFIG`
Functional area count: `30`
Setup task count: `103`

- `ORA_BENEFITS_ABSENCE`: Benefits Absence
- `ORA_BENEFITS_COMMON`: Benefits Common
- `ORA_BENEFITS_SALARY_AND_BASE_PAY`: Benefits Salary and Base Pay
- `ORA_BENEFITS_ENTERPRISE`: Benefits Enterprise
- `ORA_BENEFITS_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Benefits Legal and Legislative Organizations
- `ORA_BENEFITS_DEPARTMENTS`: Benefits Departments
- `ORA_BENEFITS_DOCUMENT_TYPES`: Benefits Document Types
- `ORA_BENEFITS_EMPLOYMENT_ACTIONS_FRAMEWORK`: Benefits Employment Actions Framework
- `ORA_BENEFITS_GRADES`: Benefits Grades
- `ORA_BENEFITS_JOBS`: Benefits Jobs
- `ORA_BENEFITS_LOCATIONS`: Benefits Locations
- `ORA_BENEFITS_PERSON_RECORD`: Benefits Person Record
- `ORA_BENEFITS_POSITIONS`: Benefits Positions
- `ORA_BENEFITS_COLLECTIVE_AGREEMENTS`: Benefits Collective Agreements
- `ORA_BENEFITS_HCM_TREES`: Benefits HCM Trees
- `ORA_BENEFITS_SENIORITY_DATES`: Benefits Seniority Dates
- `ORA_BENEFITS_SUPPLEMENTARY_ORGANIZATIONS`: Benefits Supplementary Organizations
- `ORA_BENEFITS_HCM_SECURITY_PROFILE`: Benefits HCM Security Profile
- `ORA_BENEFITS_HCM_DATA_ROLE`: Benefits HCM Data Role
- `ORA_BENEFITS_ELEMENTS_EARNINGS_AND_DEDUCTIONS`: Benefits Elements, Earnings and Deductions
- `ORA_BENEFITS_HCM_EXTRACT`: Benefits HCM Extract
- `ORA_BENEFITS_PAYROLL_BALANCES`: Benefits Payroll Balances
- `ORA_BENEFITS_PAYROLL_TOOLS`: Benefits Payroll Tools
- `ORA_BENEFITS_SECURITY_CONSOLE`: Benefits Security Console
- `ORA_BENEFITS_TIME_AND_LABOR`: Benefits Time and Labor
- `ORA_BENEFITS_GENERAL_CONFIGURATION`: Benefits General Configuration
- `ORA_BENEFITS_ELIGIBILITY`: Benefits Eligibility
- `ORA_BENEFITS_PROGRAM_AND_PLAN_HIERARCHY`: Benefits Program and Plan Hierarchy
- `ORA_BENEFITS_RATES`: Benefits Rates
- `ORA_BENEFITS_BILLING`: Benefits Billing
