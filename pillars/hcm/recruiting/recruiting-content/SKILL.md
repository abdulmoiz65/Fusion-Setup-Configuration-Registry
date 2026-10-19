---
skill_id: "hcm.recruiting.recruiting-content"
name: "Recruiting Content Implementation Guidance"
description: "Provides HCM Recruiting implementation guidance for the Recruiting Content functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Content"
functional_area_code: "ORA_RECRUITING_CONTENT"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "recruiting_content_scope"
  - "recruiting_content_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_IRC_WHATSAPP_TEMPLATE_LIB"
  - "ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION"
  - "ORA_IRC_MANAGE_CSP_REASONS"
  - "ORA_IRC_MANAGE_ORGANIZATION_DESCRIPTION_LIBRARY"
  - "ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION"
  - "ORA_IRC_DESIGN_CAMPAIGN_EMAIL_TEMPLATES"
  - "ORA_IRC_MANAGE_NOTIFICATION_LIBRARY"
  - "ORA_IRC_COMPUTED_FIELDS_CONFIGURATION"
  - "ORA_IRC_MANAGE_AGENCIES"
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

# Recruiting Content Implementation Guidance

## Purpose

Provides HCM Recruiting implementation guidance for the Recruiting Content functional area.

## When to Use

Use this functional-area skill after Recruiting scope is confirmed and the project needs recruiting content setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Recruiting` (`ORA_RECRUITING`)
- Functional area / Setup Object: `Recruiting Content` (`ORA_RECRUITING_CONTENT`)

## Setup Tasks

1. [WhatsApp Notification Template Library](whatsapp-notification-template-library/SKILL.md) (`ORA_IRC_WHATSAPP_TEMPLATE_LIB`)
2. [Candidate Selection Process Configuration](candidate-selection-process-configuration/SKILL.md) (`ORA_IRC_CANDIDATE_SELECTION_PROCESS_CONFIGURATION`)
3. [Candidate Selection Process Reasons](candidate-selection-process-reasons/SKILL.md) (`ORA_IRC_MANAGE_CSP_REASONS`)
4. [Recruiting Content Library](recruiting-content-library/SKILL.md) (`ORA_IRC_MANAGE_ORGANIZATION_DESCRIPTION_LIBRARY`)
5. [Candidate Pool Management Process Configuration](candidate-pool-management-process-configuration/SKILL.md) (`ORA_IRC_CANDIDATE_POOL_PROCESS_CONFIGURATION`)
6. [Manage HTML Email Templates](manage-html-email-templates/SKILL.md) (`ORA_IRC_DESIGN_CAMPAIGN_EMAIL_TEMPLATES`)
7. [Recruiting Notification Library](recruiting-notification-library/SKILL.md) (`ORA_IRC_MANAGE_NOTIFICATION_LIBRARY`)
8. [Job Application Computed Fields Configuration](job-application-computed-fields-configuration/SKILL.md) (`ORA_IRC_COMPUTED_FIELDS_CONFIGURATION`)
9. [Recruiting Agencies](recruiting-agencies/SKILL.md) (`ORA_IRC_MANAGE_AGENCIES`)

## Inputs

- `implementation_objective`
- `project_context`
- `recruiting_content_scope`
- `recruiting_content_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
