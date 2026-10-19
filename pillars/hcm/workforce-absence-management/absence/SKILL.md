---
skill_id: "hcm.workforce-absence-management.absence"
name: "Absence Implementation Guidance"
description: "Provides HCM Workforce Absence Management implementation guidance for the Absence functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absence"
functional_area_code: "ORA_ABSENCE"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "1.0.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "absence_scope"
  - "absence_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_ANC_MANAGE_ABSENCE_REASONS"
  - "ORA_ANC_MANAGE_ABSENCE_TYPES"
  - "ORA_ANC_MANAGE_ABSENCE_PLANS"
  - "ORA_ANC_MANAGE_ABSENCE_CATEGORIES"
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

# Absence Implementation Guidance

## Purpose

Provides HCM Workforce Absence Management implementation guidance for the Absence functional area.

## When to Use

Use this functional-area skill after Workforce Absence Management scope is confirmed and the project needs absence setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Absence Management` (`ORA_WORKFORCE_ABSENCE_MANAGEMENT`)
- Functional area / Setup Object: `Absence` (`ORA_ABSENCE`)

## Setup Tasks

1. [Absence Reasons](absence-reasons/SKILL.md) (`ORA_ANC_MANAGE_ABSENCE_REASONS`)
2. [Absence Types](absence-types/SKILL.md) (`ORA_ANC_MANAGE_ABSENCE_TYPES`)
3. [Absence Plans](absence-plans/SKILL.md) (`ORA_ANC_MANAGE_ABSENCE_PLANS`)
4. [Absence Categories](absence-categories/SKILL.md) (`ORA_ANC_MANAGE_ABSENCE_CATEGORIES`)

## Conditional Reason-to-Type Association Flow

When an implementation request names an absence reason to associate with an
absence type, orchestrate the existing nested task skills in this order:

1. Route the exact reason name and legislation to `Absence Reasons`.
2. If exactly one reason is found, retain only its validated reference for the
   downstream type request.
3. If no reason is found and the request permits creation, complete the
   `Absence Reasons` Data Loader preview, approval, submission, and successful
   status verification before continuing.
4. If the reason lookup is ambiguous, the reason creation lacks required data,
   or the reason load fails or is unresolved, stop. Do not prepare or submit
   the absence type.
5. Route the resolved reason reference to `Absence Types`, which owns the
   association payload and its separate preview and approval gate.

This is a conditional orchestration rule. It does not replace the catalog task
sequence or permit either nested setup-task skill to perform the other task's
mutation.

## Inputs

- `implementation_objective`
- `project_context`
- `absence_scope`
- `absence_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Shared Absence Source Preparation

Keep the shared offline source helpers in this functional-area skill's
`scripts/` folder. [Portable Source Preparation](references/portable-source-preparation.md)
documents the contract used by Absence Types, Plans, Categories, Reasons,
and the Absence Certifications and Leave Agreements sibling tasks. Those tasks
reuse the same helpers; they do not copy them or replace core Data Loader
formatting, execution, or approval gates.

The certification-specific History resolver belongs to
[Absence Certifications](../absences-additional/absence-certifications/SKILL.md)
and is reused for certification deletion evidence validation.
