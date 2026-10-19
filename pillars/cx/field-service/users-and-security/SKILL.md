---
skill_id: "cx.field-service.users-and-security"
name: "Users and Security Implementation Guidance"
description: "Provides CX Field Service implementation guidance for the Users and Security functional area."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
type: "planning"
execution_mode: "assisted"
owner_team: "CX field service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "users_and_security_scope"
  - "users_and_security_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS"
  - "ORA_ASE_IMPORT_USERS_AND_ROLES"
  - "ORA_ASE_IMPORT_USER_LOGIN_HISTORY"
  - "ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS"
  - "PER_MANAGE_HCM_ROLE_PROVISIONING_RULES"
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

# Users and Security Implementation Guidance

## Purpose

Provides CX Field Service implementation guidance for the Users and Security functional area.

## When to Use

Use this functional-area skill after Field Service scope is confirmed and the project needs users and security setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Field Service` (`ORA_FIELD_SERVICE`)
- Functional area / Setup Object: `Users and Security` (`ORA_ASK_USERS_AND_SECURITY`)

## Setup Tasks

1. [Run User and Roles Synchronization Process](run-user-and-roles-synchronization-process/SKILL.md) (`PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS`)
2. [Import Users and Roles into Application Security](import-users-and-roles-into-application-security/SKILL.md) (`ORA_ASE_IMPORT_USERS_AND_ROLES`)
3. [Import User Login History](import-user-login-history/SKILL.md) (`ORA_ASE_IMPORT_USER_LOGIN_HISTORY`)
4. [Run Resource Type Preparation Process for Field Service](run-resource-type-preparation-process-for-field-service/SKILL.md) (`ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS`)
5. [Manage HCM Role Provisioning Rules](manage-hcm-role-provisioning-rules/SKILL.md) (`PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`)

## Inputs

- `implementation_objective`
- `project_context`
- `users_and_security_scope`
- `users_and_security_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
