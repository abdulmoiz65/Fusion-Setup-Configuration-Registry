---
skill_id: "cx.customer-data-management.enterprise-profile"
name: "Enterprise Profile Implementation Guidance"
description: "Provides CX Customer Data Management implementation guidance for the Enterprise Profile functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Enterprise Profile"
functional_area_code: "ORA_ASK_ENTERPRISE_PROFILE"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "enterprise_profile_scope"
  - "enterprise_profile_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HZ_MANAGE_GEOGRAPHIES"
  - "HZ_RUN_MAINTAIN_GEOGRAPHY_NAME_REFERENCING"
  - "HZ_MANAGE_HIERARCHY_LOOKUPS"
  - "ORA_HZ_RUN_GEOCODE_LOADER"
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

# Enterprise Profile Implementation Guidance

## Purpose

Provides CX Customer Data Management implementation guidance for the Enterprise Profile functional area.

## When to Use

Use this functional-area skill after Customer Data Management scope is confirmed and the project needs enterprise profile setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Customer Data Management` (`ZCH_CDM`)
- Functional area / Setup Object: `Enterprise Profile` (`ORA_ASK_ENTERPRISE_PROFILE`)

## Setup Tasks

1. [Manage Geographies](manage-geographies/SKILL.md) (`HZ_MANAGE_GEOGRAPHIES`)
2. [Run Maintain Geography Name Referencing](run-maintain-geography-name-referencing/SKILL.md) (`HZ_RUN_MAINTAIN_GEOGRAPHY_NAME_REFERENCING`)
3. [Manage Hierarchy Lookups](manage-hierarchy-lookups/SKILL.md) (`HZ_MANAGE_HIERARCHY_LOOKUPS`)
4. [Run Geocode Generation](run-geocode-generation/SKILL.md) (`ORA_HZ_RUN_GEOCODE_LOADER`)

## Inputs

- `implementation_objective`
- `project_context`
- `enterprise_profile_scope`
- `enterprise_profile_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
