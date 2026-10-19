---
skill_id: "scm.product-management.catalogs"
name: "Catalogs Implementation Guidance"
description: "Provides SCM Product Management implementation guidance for the Catalogs functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Catalogs"
functional_area_code: "ORA_EGP_FA_CATALOGS"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "catalogs_scope"
  - "catalogs_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/catalogs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/catalogs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/catalogs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "EGP_MANAGE_DEFAULT_CATALOGS"
  - "EGP_MANAGE_CATALOG_ATTRIBUTES"
  - "EGP_MANAGE_CATEGORY_ATTRIBUTES"
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

# Catalogs Implementation Guidance

## Purpose

Provides SCM Product Management implementation guidance for the Catalogs functional area.

## When to Use

Use this functional-area skill after Product Management scope is confirmed and the project needs catalogs setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Product Management` (`PIM_PROD_MNG`)
- Functional area / Setup Object: `Catalogs` (`ORA_EGP_FA_CATALOGS`)

## Setup Tasks

1. [Manage Functional Area Catalogs](manage-functional-area-catalogs/SKILL.md) (`EGP_MANAGE_DEFAULT_CATALOGS`)
2. [Manage Catalog Descriptive Flexfields](manage-catalog-descriptive-flexfields/SKILL.md) (`EGP_MANAGE_CATALOG_ATTRIBUTES`)
3. [Manage Category Descriptive Flexfields](manage-category-descriptive-flexfields/SKILL.md) (`EGP_MANAGE_CATEGORY_ATTRIBUTES`)

## Inputs

- `implementation_objective`
- `project_context`
- `catalogs_scope`
- `catalogs_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
