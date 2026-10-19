---
skill_id: "hcm.global-human-resources.legal-and-legislative-organizations"
name: "Legal and Legislative Organizations Implementation Guidance"
description: "Provides HCM Global Human Resources implementation guidance for the Legal and Legislative Organizations functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Legal and Legislative Organizations"
functional_area_code: "ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "legal_and_legislative_organizations_scope"
  - "legal_and_legislative_organizations_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION"
  - "PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION"
  - "PER_MANAGE_LEGISLATIVE_DATA_GROUPS"
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

# Legal and Legislative Organizations Implementation Guidance

## Purpose

Provides HCM Global Human Resources implementation guidance for the Legal and Legislative Organizations functional area.

## When to Use

Use this functional-area skill after Global Human Resources scope is confirmed and the project needs legal and legislative organizations setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Human Resources` (`ORA_GLOBAL_HUMAN_RESOURCES`)
- Functional area / Setup Object: `Legal and Legislative Organizations` (`ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`)

## Setup Tasks

1. [Manage Legal Entity HCM Information](manage-legal-entity-hcm-information/SKILL.md) (`PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION`)
2. [Manage Legal Reporting Unit HCM Information](manage-legal-reporting-unit-hcm-information/SKILL.md) (`PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION`)
3. [Manage Legislative Data Groups](manage-legislative-data-groups/SKILL.md) (`PER_MANAGE_LEGISLATIVE_DATA_GROUPS`)

## Inputs

- `implementation_objective`
- `project_context`
- `legal_and_legislative_organizations_scope`
- `legal_and_legislative_organizations_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
