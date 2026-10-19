---
skill_id: "hcm.hcm-tool.person-notes-visibility"
name: "Person Notes Visibility Implementation Guidance"
description: "Provides HCM HCM Tool implementation guidance for the Person Notes Visibility functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Person Notes Visibility"
functional_area_code: "CUSTOM_PERSON_NOTES"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "person_notes_visibility_scope"
  - "person_notes_visibility_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/person-notes-visibility/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/person-notes-visibility/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/person-notes-visibility/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_HRT_MANAGE_FEEDBACK_VISIBILITY"
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

# Person Notes Visibility Implementation Guidance

## Purpose

Provides HCM HCM Tool implementation guidance for the Person Notes Visibility functional area.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed and the project needs person notes visibility setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Person Notes Visibility` (`CUSTOM_PERSON_NOTES`)

## Setup Tasks

1. [Manage Feedback Visibility](manage-feedback-visibility/SKILL.md) (`ORA_HRT_MANAGE_FEEDBACK_VISIBILITY`)

## Inputs

- `implementation_objective`
- `project_context`
- `person_notes_visibility_scope`
- `person_notes_visibility_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
