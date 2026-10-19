---
skill_id: "erp.financials.general-ledger"
name: "General Ledger Implementation Guidance"
description: "Provides ERP Financials implementation guidance for the General Ledger functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "General Ledger"
functional_area_code: "ORA_FIN_GENERAL_LEDGER"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "general_ledger_scope"
  - "general_ledger_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "GL_MANAGE_PRIMARY_LEDGERS"
  - "GL_SPECIFY_LEDGER_OPTIONS"
  - "GL_MANAGE_SECONDARY_LEDGERS"
  - "GL_COMPLETE_PRIMARY_TO_SECONDARY_LEDGER_MAPPING"
  - "GL_REVIEW_AND_SUBMIT_ACCOUNTING_CONFIGURATION"
  - "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER"
  - "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES"
  - "GL_ASSIGN_LEGAL_ENTITIES"
  - "GL_MANAGE_REPORTING_CURRENCIES"
  - "GL_MANAGE_LEDGER_SETS"
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

# General Ledger Implementation Guidance

## Purpose

Provides ERP Financials implementation guidance for the General Ledger functional area.

## When to Use

Use this functional-area skill after Financials scope is confirmed and the project needs general ledger setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Financials` (`XLE_FINANCIALS_JUR`)
- Functional area / Setup Object: `General Ledger` (`ORA_FIN_GENERAL_LEDGER`)

## Setup Tasks

1. [Manage Primary Ledgers](manage-primary-ledgers/SKILL.md) (`GL_MANAGE_PRIMARY_LEDGERS`)
2. [Specify Ledger Options — Primary Ledger Context](specify-ledger-options-primary-ledger/SKILL.md) (`GL_SPECIFY_LEDGER_OPTIONS`)
3. [Manage Secondary Ledgers](manage-secondary-ledgers/SKILL.md) (`GL_MANAGE_SECONDARY_LEDGERS`)
4. [Specify Ledger Options — Secondary Ledger Context](specify-ledger-options-secondary-ledger/SKILL.md) (`GL_SPECIFY_LEDGER_OPTIONS`)
5. [Complete Primary to Secondary Ledger Mapping](complete-primary-to-secondary-ledger-mapping/SKILL.md) (`GL_COMPLETE_PRIMARY_TO_SECONDARY_LEDGER_MAPPING`)
6. [Review and Submit Accounting Configuration](review-and-submit-accounting-configuration/SKILL.md) (`GL_REVIEW_AND_SUBMIT_ACCOUNTING_CONFIGURATION`)
7. [Assign Balancing Segment Values to Ledger](assign-balancing-segment-values-to-ledger/SKILL.md) (`GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER`)
8. [Assign Balancing Segment Values to Legal Entities](assign-balancing-segment-values-to-legal-entities/SKILL.md) (`GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`)
9. [Assign Legal Entities](assign-legal-entities/SKILL.md) (`GL_ASSIGN_LEGAL_ENTITIES`)
10. [Manage Reporting Currencies](manage-reporting-currencies/SKILL.md) (`GL_MANAGE_REPORTING_CURRENCIES`)
11. [Manage Ledger Sets](manage-ledger-sets/SKILL.md) (`GL_MANAGE_LEDGER_SETS`)

## Inputs

- `implementation_objective`
- `project_context`
- `general_ledger_scope`
- `general_ledger_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
