---
skill_id: "hcm.recruiting.recruiting-foundation"
name: "Recruiting Foundation Implementation Guidance"
description: "Provides HCM Recruiting implementation guidance for the Recruiting Foundation functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "recruiting_foundation_scope"
  - "recruiting_foundation_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES"
  - "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS"
  - "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS"
  - "ORA_IRC_MANAGE_LABELS"
  - "ORA_IRC_GEO_HRCHY"
  - "ORA_IRC_GEO_HRCHY_STRUCTURE"
  - "ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES"
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

# Recruiting Foundation Implementation Guidance

## Purpose

Provides HCM Recruiting implementation guidance for the Recruiting Foundation functional area.

## When to Use

Use this functional-area skill after Recruiting scope is confirmed and the project needs recruiting foundation setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Recruiting` (`ORA_RECRUITING`)
- Functional area / Setup Object: `Recruiting Foundation` (`ORA_RECRUITING_FOUNDATION_DATA`)

## Setup Tasks

1. [Configure Recruiting Interaction Categories](configure-recruiting-interaction-categories/SKILL.md) (`ORA_IRC_CONFIGURE_RECRUITING_INTERACTION_CATEGORIES`)
2. [Recruiting and Candidate Experience Value Sets](recruiting-and-candidate-experience-value-sets/SKILL.md) (`ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_VALUE_SETS`)
3. [Recruiting and Candidate Experience Lookups](recruiting-and-candidate-experience-lookups/SKILL.md) (`ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_LOOKUPS`)
4. [Manage Recruiting Labels](manage-recruiting-labels/SKILL.md) (`ORA_IRC_MANAGE_LABELS`)
5. [Geography Hierarchies](geography-hierarchies/SKILL.md) (`ORA_IRC_GEO_HRCHY`)
6. [Geography Hierarchy Structure](geography-hierarchy-structure/SKILL.md) (`ORA_IRC_GEO_HRCHY_STRUCTURE`)
7. [Candidate Dimension Source Names](candidate-dimension-source-names/SKILL.md) (`ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES`)

## Inputs

- `implementation_objective`
- `project_context`
- `recruiting_foundation_scope`
- `recruiting_foundation_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
