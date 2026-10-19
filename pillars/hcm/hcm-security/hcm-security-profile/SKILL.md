---
skill_id: "hcm.hcm-security.hcm-security-profile"
name: "HCM Security Profile Implementation Guidance"
description: "Provides HCM HCM Security implementation guidance for the HCM Security Profile functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Security"
functional_area: "HCM Security Profile"
functional_area_code: "ORA_HCM_SECURITY_PROFILE"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm security pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_security_profile_scope"
  - "hcm_security_profile_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-security-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-security-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-security/hcm-security-profile/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PER_MANAGE_LEGISLATIVE_DATA_GROUP_SECURITY_PROFILE"
  - "PER_MANAGE_COUNTRY_SECURITY_PROFILE"
  - "PER_MANAGE_POSITION_SECURITY_PROFILE"
  - "ORA_PER_MANAGE_HCM_EXCLUSION_RULES"
  - "PER_MANAGE_PERSON_AND_ASSIGNMENT_SECURITY_PROFILE"
  - "PER_MANAGE_ORGANIZATION_SECURITY_PROFILE"
  - "ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE"
  - "ORA_IRC_CAND_SRCH_SEC_PROFILES"
  - "ORA_IRC_MANAGE_JOB_REQUISITION_SECURITY_PROFILE"
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

# HCM Security Profile Implementation Guidance

## Purpose

Provides HCM HCM Security implementation guidance for the HCM Security Profile functional area.

## When to Use

Use this functional-area skill after HCM Security scope is confirmed and the project needs hcm security profile setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Security` (`ORA_HCM_SECURITY`)
- Functional area / Setup Object: `HCM Security Profile` (`ORA_HCM_SECURITY_PROFILE`)

## Setup Tasks

1. [Manage Legislative Data Group Security Profile](manage-legislative-data-group-security-profile/SKILL.md) (`PER_MANAGE_LEGISLATIVE_DATA_GROUP_SECURITY_PROFILE`)
2. [Manage Country Security Profile](manage-country-security-profile/SKILL.md) (`PER_MANAGE_COUNTRY_SECURITY_PROFILE`)
3. [Manage Position Security Profile](manage-position-security-profile/SKILL.md) (`PER_MANAGE_POSITION_SECURITY_PROFILE`)
4. [Manage HCM Exclusion Rules](manage-hcm-exclusion-rules/SKILL.md) (`ORA_PER_MANAGE_HCM_EXCLUSION_RULES`)
5. [Manage Person Security Profile](manage-person-security-profile/SKILL.md) (`PER_MANAGE_PERSON_AND_ASSIGNMENT_SECURITY_PROFILE`)
6. [Manage Organization Security Profile](manage-organization-security-profile/SKILL.md) (`PER_MANAGE_ORGANIZATION_SECURITY_PROFILE`)
7. [Manage Transaction Security Profile](manage-transaction-security-profile/SKILL.md) (`ORA_PER_MANAGE_TRANSACTION_SECURITY_PROFILE`)
8. [Candidate Security Profiles](candidate-security-profiles/SKILL.md) (`ORA_IRC_CAND_SRCH_SEC_PROFILES`)
9. [Job Requisition Security Profiles](job-requisition-security-profiles/SKILL.md) (`ORA_IRC_MANAGE_JOB_REQUISITION_SECURITY_PROFILE`)

## Inputs

- `implementation_objective`
- `project_context`
- `hcm_security_profile_scope`
- `hcm_security_profile_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.
