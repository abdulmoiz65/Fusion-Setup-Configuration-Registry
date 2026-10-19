---
skill_id: "hcm.global-human-resources.global-human-resources-common"
name: "Global Human Resources Common Implementation Guidance"
description: "Provides HCM Global Human Resources implementation guidance for the Global Human Resources Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Global Human Resources Common"
functional_area_code: "ORA_GLOBAL_HUMAN_RESOURCES_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "global_human_resources_common_scope"
  - "global_human_resources_common_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/global-human-resources-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/global-human-resources-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/global-human-resources-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
  - "FND_MANAGE_COMMON_LOOKUPS"
  - "FND_MANAGE_STANDARD_LOOKUPS"
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
  - "FND_MANAGE_KEY_FLEXFIELDS"
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

# Global Human Resources Common Implementation Guidance

## Purpose

Provides HCM Global Human Resources implementation guidance for the Global Human Resources Common functional area.

## When to Use

Use this functional-area skill after Global Human Resources scope is confirmed and the project needs Global Human Resources Common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Human Resources` (`ORA_GLOBAL_HUMAN_RESOURCES`)
- Functional area / Setup Object: `Global Human Resources Common` (`ORA_GLOBAL_HUMAN_RESOURCES_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Standard Lookups](manage-standard-lookups/SKILL.md) (`FND_MANAGE_STANDARD_LOOKUPS`)
5. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
6. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
7. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)
8. [Manage Key Flexfields](manage-key-flexfields/SKILL.md) (`FND_MANAGE_KEY_FLEXFIELDS`)

## Inputs

- `implementation_objective`
- `project_context`
- `global_human_resources_common_scope`
- `global_human_resources_common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
