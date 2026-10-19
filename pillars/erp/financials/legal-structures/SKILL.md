---
skill_id: "erp.financials.legal-structures"
name: "Legal Structures Implementation Guidance"
description: "Provides ERP Financials implementation guidance for the Legal Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Legal Structures"
functional_area_code: "ORA_ASK_LEGAL_STRUCTURES"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "legal_structures_scope"
  - "legal_structures_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "XLE_MANAGE_LEGAL_ADDRESSES"
  - "XLE_MANAGE_LEGAL_ENTITY"
  - "XLE_MANAGE_LEGAL_ENTITY_REGISTRATIONS"
  - "XLE_MANAGE_LEGAL_REPORTING_UNIT"
  - "XLE_MANAGE_LEGAL_REPORTING_UNIT_REGISTRATIONS"
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

# Legal Structures Implementation Guidance

## Purpose

Provides ERP Financials implementation guidance for the Legal Structures functional area.

## When to Use

Use this functional-area skill after Financials scope is confirmed and the project needs legal structures setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Financials` (`XLE_FINANCIALS_JUR`)
- Functional area / Setup Object: `Legal Structures` (`ORA_ASK_LEGAL_STRUCTURES`)

## Setup Tasks

1. [Manage Legal Addresses](manage-legal-addresses/SKILL.md) (`XLE_MANAGE_LEGAL_ADDRESSES`)
2. [Manage Legal Entity](manage-legal-entity/SKILL.md) (`XLE_MANAGE_LEGAL_ENTITY`)
3. [Manage Legal Entity Registrations](manage-legal-entity-registrations/SKILL.md) (`XLE_MANAGE_LEGAL_ENTITY_REGISTRATIONS`)
4. [Manage Legal Reporting Unit](manage-legal-reporting-unit/SKILL.md) (`XLE_MANAGE_LEGAL_REPORTING_UNIT`)
5. [Manage Legal Reporting Unit Registrations](manage-legal-reporting-unit-registrations/SKILL.md) (`XLE_MANAGE_LEGAL_REPORTING_UNIT_REGISTRATIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `legal_structures_scope`
- `legal_structures_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

Apply these cross-task prerequisites when building the setup sequence:

- Complete `Manage Legal Addresses` before any task that requires a new legal address; an already validated existing address may satisfy that dependency.
- Complete `Manage Legal Entity` before creating its registrations or legal reporting units.
- Complete `Manage Legal Reporting Unit` before creating registrations for that legal reporting unit.
