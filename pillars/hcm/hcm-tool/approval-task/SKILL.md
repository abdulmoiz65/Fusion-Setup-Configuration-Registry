---
skill_id: "hcm.hcm-tool.approval-task"
name: "Approval Task Implementation Guidance"
description: "Provides HCM HCM Tool implementation guidance for the Approval Task functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Approval Task"
functional_area_code: "CUSTOM_APPROVAL_TASK"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "approval_task_scope"
  - "approval_task_requirements"
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
  - "core.data-loader.task-rest"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-task/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-task/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-task/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_CONFIGURE_TASK"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May route an explicitly approved task-configuration write through the nested Configure task skill."
required_privileges:
  - "Fusion privileges sufficient to read and update HCM approval task configuration."
---

# Approval Task Implementation Guidance

## Purpose

Provides HCM HCM Tool implementation guidance for the Approval Task functional area.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed and the project needs approval task setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Approval Task` (`CUSTOM_APPROVAL_TASK`)

## Setup Tasks

1. [Configure task](configure-task/SKILL.md) (`CUSTOM_CONFIGURE_TASK`)

## Task-Configuration Write Routing

For a requested Approval Task configuration change, route to the nested
`Configure task` skill. Its registered write adapter is the Data Loader
business object `businessProcessApprovalRulesTasks`, using the documented
`writeTaskConfiguration` action. Do not treat CSV import support as a
requirement for that REST action.

## Inputs

- `implementation_objective`
- `project_context`
- `approval_task_scope`
- `approval_task_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. For configuration writes, preserve the nested skill's read → complete-configuration → immutable-preview → explicit-approval gate. Track token usage for any generated project artifact or skill-run record using the manifest policy.
