---
skill_id: "hcm.workforce-time-management"
name: "Workforce Time Management"
description: "Coordinates HCM implementation guidance for the Workforce Time Management offering."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
source_catalog: "knowledge/setup-task-catalog/effective/Offerings_catalog.json"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Workforce Time Management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "workforce_time_management_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/current/"
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

# Workforce Time Management

## Purpose

Coordinates implementation work for offering `Workforce Time Management` (`ORA_WORKFORCE_TIME_MANAGEMENT`) under the `HCM` pillar.

## Routing Responsibility

Use `core.fusion-dev.pillar-skill-gen` to create functional-area child skills registered under this offering in the effective catalog.

## Functional Areas From Effective Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_WORKFORCE_TIME_MANAGEMENT`
Functional area count: `14`
Setup task count: `50`

- `ORA_TIME_AND_LABOR_COMMON`: Time and Labor Common
- `ORA_TIME_AND_LABOR_ENTERPRISE`: Time and Labor Enterprise
- `ORA_TIME_AND_LABOR_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Time and Labor Legal and Legislative Organizations
- `ORA_TIME_AND_LABOR_HCM_TOOL`: Time and Labor HCM Tool
- `ORA_TIME_AND_LABOR_PERSON_RECORD`: Time and Labor Person Record
- `ORA_TIME_AND_LABOR_EMPLOYMENT_ACTIONS_FRAMEWORK`: Time and Labor Employment Actions Framework
- `ORA_TIME_AND_LABOR_ELEMENTS_EARNINGS_AND_DEDUCTIONS`: Time and Labor Elements, Earnings and Deductions
- `ORA_TIME_AND_LABOR_WFM_COMMON`: Time and Labor WFM Common
- `ORA_TIME_AND_LABOR_PAYROLL_TOOLS`: Time and Labor Payroll Tools
- `ORA_TIME_AND_LABOR_FOUNDATION`: Time and Labor Foundation
- `ORA_TIME_AND_LABOR_ADDITIONAL`: Time and Labor Additional
- `ORA_TIME_CLOCK_DEVICE`: Time Clock Device
- `ORA_TIME_AND_LABOR_RULES`: Time and Labor Rules
- `ORA_WFM_PROCESSES`: WFM Processes
