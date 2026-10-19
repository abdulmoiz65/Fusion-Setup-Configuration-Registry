---
skill_id: "hcm.global-human-resources.person-record"
name: "Person Record Implementation Guidance"
description: "Provides HCM Global Human Resources implementation guidance for the Person Record functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Person Record"
functional_area_code: "ORA_PERSON_RECORD"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "person_record_scope"
  - "person_record_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PER_MANAGE_PERSON_TYPES"
  - "ORA_PER_MANAGE_PERSON_NAME_STYLES"
  - "PER_MANAGE_PERSON_NAME_FORMATS"
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

# Person Record Implementation Guidance

## Purpose

Provides HCM Global Human Resources implementation guidance for the Person Record functional area.

## When to Use

Use this functional-area skill after Global Human Resources scope is confirmed and the project needs person record setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Human Resources` (`ORA_GLOBAL_HUMAN_RESOURCES`)
- Functional area / Setup Object: `Person Record` (`ORA_PERSON_RECORD`)

## Setup Tasks

1. [Manage Person Types](manage-person-types/SKILL.md) (`PER_MANAGE_PERSON_TYPES`)
2. [Manage Person Name Styles](manage-person-name-styles/SKILL.md) (`ORA_PER_MANAGE_PERSON_NAME_STYLES`)
3. [Manage Person Name Formats](manage-person-name-formats/SKILL.md) (`PER_MANAGE_PERSON_NAME_FORMATS`)

## Inputs

- `implementation_objective`
- `project_context`
- `person_record_scope`
- `person_record_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
