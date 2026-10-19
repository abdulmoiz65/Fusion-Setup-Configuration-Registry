---
skill_id: "hcm.compensation.compensation-data-and-batch-controls"
name: "Compensation Data and Batch Controls Implementation Guidance"
description: "Provides HCM Compensation implementation guidance for the Compensation Data and Batch Controls functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Compensation Data and Batch Controls"
functional_area_code: "ORA_COMPENSATION_DATA_AND_BATCH_CONTROLS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "compensation_data_and_batch_controls_scope"
  - "compensation_data_and_batch_controls_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/compensation-data-and-batch-controls/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/compensation-data-and-batch-controls/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/compensation-data-and-batch-controls/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_CMP_MANAGE_EXTERNAL_COMPENSATION_DATA_LOOKUPS"
  - "CMP_CONFIGURE_COMPENSATION_BATCH_PARAMETERS"
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

# Compensation Data and Batch Controls Implementation Guidance

## Purpose

Provides HCM Compensation implementation guidance for the Compensation Data and Batch Controls functional area.

## When to Use

Use this functional-area skill after Compensation scope is confirmed and the project needs compensation data and batch controls setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Compensation` (`ORA_COMPENSATION`)
- Functional area / Setup Object: `Compensation Data and Batch Controls` (`ORA_COMPENSATION_DATA_AND_BATCH_CONTROLS`)

## Setup Tasks

1. [Manage External Compensation Data Lookups](manage-external-compensation-data-lookups/SKILL.md) (`ORA_CMP_MANAGE_EXTERNAL_COMPENSATION_DATA_LOOKUPS`)
2. [Configure Compensation Batch Parameters](configure-compensation-batch-parameters/SKILL.md) (`CMP_CONFIGURE_COMPENSATION_BATCH_PARAMETERS`)

## Inputs

- `implementation_objective`
- `project_context`
- `compensation_data_and_batch_controls_scope`
- `compensation_data_and_batch_controls_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
