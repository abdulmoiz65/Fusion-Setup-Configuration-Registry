---
skill_id: "hcm.hcm-communicate.employee-communications"
name: "Employee Communications Implementation Guidance"
description: "Provides HCM HCM Communicate implementation guidance for the Employee Communications functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
functional_area: "Employee Communications"
functional_area_code: "ORA_IRC_EMPLOYEE_CAMPAIGNS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm communicate pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "employee_communications_scope"
  - "employee_communications_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_IRC_EMP_CAMP_INFORMATION"
  - "ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES"
  - "ORA_IRC_EMP_CAMP_COMM_TEAMS"
  - "ORA_IRC_EMP_CAMP_SMS_CONFIG"
  - "ORA_IRC_EMP_EXT_INTEGRATIONS"
  - "ORA_IRC_EMP_CAMP_DEEP_LINKS"
  - "ORA_IRC_EMP_CAMP_VANITY_CONFIG"
  - "ORA_IRC_COMMUNICATE_LOOKUPS"
  - "ORA_IRC_EMP_CAMP_ELIGIBILITY_PROFILE"
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

# Employee Communications Implementation Guidance

## Purpose

Provides HCM HCM Communicate implementation guidance for the Employee Communications functional area.

## When to Use

Use this functional-area skill after HCM Communicate scope is confirmed and the project needs employee communications setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Communicate` (`ORA_IRC_HCM_COMMUNICATE`)
- Functional area / Setup Object: `Employee Communications` (`ORA_IRC_EMPLOYEE_CAMPAIGNS`)

## Setup Tasks

1. [Manage Communicate Info](manage-communicate-info/SKILL.md) (`ORA_IRC_EMP_CAMP_INFORMATION`)
2. [Manage Email Templates](manage-email-templates/SKILL.md) (`ORA_IRC_DESIGN_EMP_CAMPAIGN_EMAIL_TEMPLATES`)
3. [Manage Communication Teams](manage-communication-teams/SKILL.md) (`ORA_IRC_EMP_CAMP_COMM_TEAMS`)
4. [Manage SMS Configuration](manage-sms-configuration/SKILL.md) (`ORA_IRC_EMP_CAMP_SMS_CONFIG`)
5. [Manage External Integrations](manage-external-integrations/SKILL.md) (`ORA_IRC_EMP_EXT_INTEGRATIONS`)
6. [Manage Predefined Links](manage-predefined-links/SKILL.md) (`ORA_IRC_EMP_CAMP_DEEP_LINKS`)
7. [Manage Email Profiles](manage-email-profiles/SKILL.md) (`ORA_IRC_EMP_CAMP_VANITY_CONFIG`)
8. [Manage Communicate Lookups](manage-communicate-lookups/SKILL.md) (`ORA_IRC_COMMUNICATE_LOOKUPS`)
9. [Manage Predefined Audience Criteria](manage-predefined-audience-criteria/SKILL.md) (`ORA_IRC_EMP_CAMP_ELIGIBILITY_PROFILE`)

## Inputs

- `implementation_objective`
- `project_context`
- `employee_communications_scope`
- `employee_communications_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
