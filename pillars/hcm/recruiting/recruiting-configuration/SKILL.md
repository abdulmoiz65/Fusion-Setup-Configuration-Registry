---
skill_id: "hcm.recruiting.recruiting-configuration"
name: "Recruiting Configuration Implementation Guidance"
description: "Provides HCM Recruiting implementation guidance for the Recruiting Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "recruiting_configuration_scope"
  - "recruiting_configuration_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES"
  - "ORA_IRC_MESSAGING_CONFIGURATION"
  - "ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION"
  - "ORA_IRC_MANAGE_OM_GIG_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD"
  - "ORA_IRC_MP_SITE_CONFIGURATION"
  - "ORA_IRC_MP_SITE_GIG_CONFIGURATION"
  - "ORA_IRC_MANAGE_JOB_REQUISITION_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_IRC_MP_ELIGIBILITY_PROFILE"
  - "ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD"
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

# Recruiting Configuration Implementation Guidance

## Purpose

Provides HCM Recruiting implementation guidance for the Recruiting Configuration functional area.

## When to Use

Use this functional-area skill after Recruiting scope is confirmed and the project needs recruiting configuration setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Recruiting` (`ORA_RECRUITING`)
- Functional area / Setup Object: `Recruiting Configuration` (`ORA_RECRUITING_CONFIGURATION`)

## Setup Tasks

1. [Recruiting and Candidate Experience Profile Option Values](recruiting-and-candidate-experience-profile-option-values/SKILL.md) (`ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES`)
2. [Recruiting Messaging Configuration](recruiting-messaging-configuration/SKILL.md) (`ORA_IRC_MESSAGING_CONFIGURATION`)
3. [Enterprise Recruiting and Candidate Experience Information](enterprise-recruiting-and-candidate-experience-information/SKILL.md) (`ORA_IRC_MANAGE_ENTERPRISE_RECRUITING_AND_CANDIDATE_EXPERIENCE_INFORMATION`)
4. [Gig Descriptive Flexfields](gig-descriptive-flexfields/SKILL.md) (`ORA_IRC_MANAGE_OM_GIG_DESCRIPTIVE_FLEXFIELDS`)
5. [Referral Descriptive Flexfields](referral-descriptive-flexfields/SKILL.md) (`ORA_IRC_REFERRAL_DESCRIPTIVE_FLEXFIELD`)
6. [Opportunity Marketplace Jobs Configurations](opportunity-marketplace-jobs-configurations/SKILL.md) (`ORA_IRC_MP_SITE_CONFIGURATION`)
7. [Opportunity Marketplace Gigs Configurations](opportunity-marketplace-gigs-configurations/SKILL.md) (`ORA_IRC_MP_SITE_GIG_CONFIGURATION`)
8. [Job Requisition Descriptive Flexfields](job-requisition-descriptive-flexfields/SKILL.md) (`ORA_IRC_MANAGE_JOB_REQUISITION_DESCRIPTIVE_FLEXFIELDS`)
9. [Opportunity Marketplace Eligibility Profiles](opportunity-marketplace-eligibility-profiles/SKILL.md) (`ORA_IRC_MP_ELIGIBILITY_PROFILE`)
10. [Job Offers Descriptive Flexfields](job-offers-descriptive-flexfields/SKILL.md) (`ORA_IRC_MANAGE_JOB_OFFERS_DESCRIPTIVE_FLEXFIELD`)

## Inputs

- `implementation_objective`
- `project_context`
- `recruiting_configuration_scope`
- `recruiting_configuration_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
