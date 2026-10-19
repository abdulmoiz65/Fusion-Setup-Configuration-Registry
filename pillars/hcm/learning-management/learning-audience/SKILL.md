---
skill_id: "hcm.learning-management.learning-audience"
name: "Learning Audience Implementation Guidance"
description: "Provides HCM Learning Management implementation guidance for the Learning Audience functional area."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Audience"
functional_area_code: "ORA_LEARNING_AUDIENCE"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM learning management pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "learning_audience_scope"
  - "learning_audience_requirements"
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
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-audience/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-audience/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-audience/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA"
  - "CUSTOM_MANAGE_USER_GROUPS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May submit an explicitly approved Learning Audience mutation through the selected Data Loader workflow."
  - "May create one managerCriteria or participantCriteria child through the core Fusion REST client only under the documented existing-parent fallback and after separate payload approval."
required_privileges:
  - "Access to the target Fusion environment and privileges for the selected read or mutation operation."
---

# Learning Audience Implementation Guidance

## Purpose

Provides HCM Learning Management implementation guidance for the Learning Audience functional area.

## When to Use

Use this functional-area skill after Learning Management scope is confirmed and the project needs learning audience setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Learning Management` (`ORA_LEARNING_MANAGEMENT`)
- Functional area / Setup Object: `Learning Audience` (`ORA_LEARNING_AUDIENCE`)
- Membership and task order: [effective task hierarchy](../../../../knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json)
- Approved taxonomy: [Learning taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/learning-taxonomy/)

The catalog-code alignment does not rename this folder or its canonical skill
ID, `hcm.learning-management.learning-audience`. Both tasks retain their
`CUSTOM_` task codes and existing Data Loader business-object mappings.

## Setup Tasks

1. [Manage Learning Audience Criteria](manage-learning-audience-criteria.md) (`CUSTOM_MANAGE_LEARNING_AUDIENCE_CRITERIA`)
2. [Manage User Groups](manage-user-groups.md) (`CUSTOM_MANAGE_USER_GROUPS`)

## Inputs

- `implementation_objective`
- `project_context`
- `learning_audience_scope`
- `learning_audience_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Both tasks use the flat metadata files above and share `ora-resource/` guidance.
Read [sources and input validation](ora-resource/ora_input_validation.md) for
the task contracts and [dependency readiness](ora-resource/ora_dependency_readiness.md)
for the HCM Tool handoff. Catalog identity does not establish live provider
readiness or change the selected execution route and approval requirements.
Track token usage for any generated project artifact or skill-run record using
the manifest policy.
