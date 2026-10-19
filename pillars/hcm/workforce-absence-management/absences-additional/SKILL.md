---
skill_id: "hcm.workforce-absence-management.absences-additional"
name: "Absences Additional Implementation Guidance"
description: "Provides HCM Workforce Absence Management implementation guidance for the Absences Additional functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absences Additional"
functional_area_code: "ORA_ABSENCES_ADDITIONAL"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "1.0.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "absences_additional_scope"
  - "absences_additional_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS"
  - "ORA_ANC_MANAGE_LEAVE_AGREEMENTS"
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

# Absences Additional Implementation Guidance

## Purpose

Provides HCM Workforce Absence Management implementation guidance for the Absences Additional functional area.

## When to Use

Use this functional-area skill after Workforce Absence Management scope is confirmed and the project needs absences additional setup planning, baseline export, import sequencing, or validation checkpoints.

## Route by Requested Scope

After `router.implementation-router` selects the project and catalog context,
route a request to create, view, or maintain one absence certification or leave
agreement to its nested setup-task skill. The presence of other tasks in the
project or Run Book does not turn a standalone object request into a
functional-area sequencing request.

The offering-task-map-builder and task-dependency-resolver dependencies apply
when constructing a functional-area setup plan or dependency-ordered import
sequence. Do not invoke FSM/BOSS task discovery as a prerequisite for a
standalone setup-task operation or to obtain a Task Hook selection sequence.
For that operation, follow the selected task's catalog/context readiness and
Data Loader workflow. If functional-area sequencing is actually requested,
retain the resolver's discovery, ordering, and failure-handling requirements;
a local task selection index is not dependency-order evidence.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Absence Management` (`ORA_WORKFORCE_ABSENCE_MANAGEMENT`)
- Functional area / Setup Object: `Absences Additional` (`ORA_ABSENCES_ADDITIONAL`)

## Setup Tasks

1. [Absence Certifications](absence-certifications/SKILL.md) (`ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS`)
2. [Leave Agreements](leave-agreements/SKILL.md) (`ORA_ANC_MANAGE_LEAVE_AGREEMENTS`)

## Inputs

- `implementation_objective`
- `project_context`
- `absences_additional_scope`
- `absences_additional_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

Read the shared [lifecycle and acceptance contract](references/absence-additional-lifecycle.md)
for Absence Certifications and Leave Agreements. Both tasks reuse the existing
[portable source preparation](../absence/references/portable-source-preparation.md)
helpers in the Absence functional-area skill. Keep task-specific helpers in
the owning nested task's `scripts/` folder.
