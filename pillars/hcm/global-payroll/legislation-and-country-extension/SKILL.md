---
skill_id: "hcm.global-payroll.legislation-and-country-extension"
name: "Legislation and Country Extension Implementation Guidance"
description: "Provides HCM Global Payroll implementation guidance for the Legislation and Country Extension functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Legislation and Country Extension"
functional_area_code: "ORA_LEGISLATION_AND_COUNTRY_EXTENSION"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "legislation_and_country_extension_scope"
  - "legislation_and_country_extension_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/legislation-and-country-extension/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/legislation-and-country-extension/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/legislation-and-country-extension/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PAY_CONFIGURE_LEGISLATIONS_FOR_HUMAN_RESOURCES"
  - "PAY_CONFIGURE_PAYROLL_LEGISLATION"
  - "ORA_PAY_MANAGE_PAYROLL_PRODUCT_USAGES"
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

# Legislation and Country Extension Implementation Guidance

## Purpose

Provides HCM Payroll implementation guidance for the Legislation and Country Extension functional area.

## When to Use

Use this functional-area skill after Payroll scope is confirmed and the project needs legislation and country extension setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Payroll` (`ORA_GLOBAL_PAYROLL`)
- Functional area / Setup Object: `Legislation and Country Extension` (`ORA_LEGISLATION_AND_COUNTRY_EXTENSION`)

## Setup Tasks

1. [Configure Legislations for Human Resources](configure-legislations-for-human-resources/SKILL.md) (`PAY_CONFIGURE_LEGISLATIONS_FOR_HUMAN_RESOURCES`)
2. [Configure Payroll Legislations](configure-payroll-legislations/SKILL.md) (`PAY_CONFIGURE_PAYROLL_LEGISLATION`)
3. [Features by Country or Territory](features-by-country-or-territory/SKILL.md) (`ORA_PAY_MANAGE_PAYROLL_PRODUCT_USAGES`)

## Inputs

- `implementation_objective`
- `project_context`
- `legislation_and_country_extension_scope`
- `legislation_and_country_extension_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
