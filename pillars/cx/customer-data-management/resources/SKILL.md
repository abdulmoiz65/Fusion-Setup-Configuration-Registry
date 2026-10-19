---
skill_id: "cx.customer-data-management.resources"
name: "Resources Implementation Guidance"
description: "Provides CX Customer Data Management implementation guidance for the Resources functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Resources"
functional_area_code: "ORA_CRM_RESOURCES"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "resources_scope"
  - "resources_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HZ_MANAGE_RESOURCES"
  - "HZ_MANAGE_RESOURCE_ROLES"
  - "HZ_MANAGE_RESOURCE_ROLE_LOOKUPS"
  - "HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_RESOURCE_LOOKUPS"
  - "HZ_MANAGE_RESOURCE_PROFILE_OPTIONS"
  - "HZ_MANAGE_RESOURCE_TEAM_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_RUN_REPORTING_HIERARCHY_GENERATION"
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

# Resources Implementation Guidance

## Purpose

Provides CX Customer Data Management implementation guidance for the Resources functional area.

## When to Use

Use this functional-area skill after Customer Data Management scope is confirmed and the project needs resources setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Customer Data Management` (`ZCH_CDM`)
- Functional area / Setup Object: `Resources` (`ORA_CRM_RESOURCES`)

## Setup Tasks

1. [Manage Resources](manage-resources/SKILL.md) (`HZ_MANAGE_RESOURCES`)
2. [Manage Resource Roles](manage-resource-roles/SKILL.md) (`HZ_MANAGE_RESOURCE_ROLES`)
3. [Manage Resource Role Lookups](manage-resource-role-lookups/SKILL.md) (`HZ_MANAGE_RESOURCE_ROLE_LOOKUPS`)
4. [Manage Resource Role Descriptive Flexfields](manage-resource-role-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS`)
5. [Manage Resource Lookups](manage-resource-lookups/SKILL.md) (`HZ_MANAGE_RESOURCE_LOOKUPS`)
6. [Manage Resource Profile Options](manage-resource-profile-options/SKILL.md) (`HZ_MANAGE_RESOURCE_PROFILE_OPTIONS`)
7. [Manage Resource Team Descriptive Flexfields](manage-resource-team-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_RESOURCE_TEAM_DESCRIPTIVE_FLEXFIELDS`)
8. [Run Reporting Hierarchy Generation](run-reporting-hierarchy-generation/SKILL.md) (`HZ_RUN_REPORTING_HIERARCHY_GENERATION`)

## Inputs

- `implementation_objective`
- `project_context`
- `resources_scope`
- `resources_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## REST Header Policy

Every Fusion REST call declared by this Resources functional area or any of its
task-local guidance must include the request header
`Rest-Framework-Version: 9`. Preserve any endpoint-specific `Accept` and
`Content-Type` headers in addition to this required header.
