---
skill_id: "hcm.recruiting.recruiting-common"
name: "Recruiting Common Implementation Guidance"
description: "Provides HCM Recruiting implementation guidance for the Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Common"
functional_area_code: "ORA_RECRUITING_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "recruiting_common_scope"
  - "recruiting_common_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FND_MANAGE_ATTACHMENT_ENTITIES"
  - "FND_MANAGE_ATTACHMENT_CATEGORIES"
  - "ORA_FND_APP_DOCUMENT_FILE_FORMATS"
  - "ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS"
  - "ORA_FND_SUGGESTION_GROUPS"
  - "ORA_FND_MANAGE_INDEX_CONFIGURATION"
  - "FND_MANAGE_COMMON_LOOKUPS"
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
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

# Recruiting Common Implementation Guidance

## Purpose

Provides HCM Recruiting implementation guidance for the Common functional area.

## When to Use

Use this functional-area skill after Recruiting scope is confirmed and the project needs recruiting common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Recruiting` (`ORA_RECRUITING`)
- Functional area / Setup Object: `Recruiting Common` (`ORA_RECRUITING_COMMON`)

## Setup Tasks

1. [Manage Attachment Entities](manage-attachment-entities/SKILL.md) (`FND_MANAGE_ATTACHMENT_ENTITIES`)
2. [Manage Attachment Categories](manage-attachment-categories/SKILL.md) (`FND_MANAGE_ATTACHMENT_CATEGORIES`)
3. [Manage Attachment File Formats](manage-attachment-file-formats/SKILL.md) (`ORA_FND_APP_DOCUMENT_FILE_FORMATS`)
4. [Manage Applications Core Global Search Configurations](manage-applications-core-global-search-configurations/SKILL.md) (`ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS`)
5. [Manage Applications Core Global Search Suggestion Groups](manage-applications-core-global-search-suggestion-groups/SKILL.md) (`ORA_FND_SUGGESTION_GROUPS`)
6. [Manage Search Indexes](manage-search-indexes/SKILL.md) (`ORA_FND_MANAGE_INDEX_CONFIGURATION`)
7. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
8. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
9. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
10. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
11. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
12. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)

## Inputs

- `implementation_objective`
- `project_context`
- `recruiting_common_scope`
- `recruiting_common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
