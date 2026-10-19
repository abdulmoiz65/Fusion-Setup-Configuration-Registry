---
skill_id: "hcm.recruiting.candidate-experience-configuration"
name: "Candidate Experience Configuration Implementation Guidance"
description: "Provides HCM Recruiting implementation guidance for the Candidate Experience Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Candidate Experience Configuration"
functional_area_code: "ORA_CANDIDATE_EXPERIENCE_CONFIGURATION"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "candidate_experience_scope"
  - "candidate_experience_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/candidate-experience-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/candidate-experience-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/candidate-experience-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_IRC_CONFIGURE_CAREER_SITE"
  - "ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION"
  - "ORA_IRC_DOI_MANAGEMENT"
  - "ORA_IRC_APPLY_FLOW_CONFIGURATION"
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

# Candidate Experience Configuration Implementation Guidance

## Purpose

Provides HCM Recruiting implementation guidance for the Candidate Experience Configuration functional area.

## When to Use

Use this functional-area skill after Recruiting scope is confirmed and the project needs Candidate Experience Configuration setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Recruiting` (`ORA_RECRUITING`)
- Functional area / Setup Object: `Candidate Experience Configuration` (`ORA_CANDIDATE_EXPERIENCE_CONFIGURATION`)

## Setup Tasks

1. [Career Sites Configuration](career-sites-configuration/SKILL.md) (`ORA_IRC_CONFIGURE_CAREER_SITE`)
2. [Configure Candidate Experience CAPTCHA Provider](configure-candidate-experience-captcha-provider/SKILL.md) (`ORA_IRC_CAPTCHA_PROVIDER_CONFIGURATION`)
3. [Double Opt In Management](double-opt-in-management/SKILL.md) (`ORA_IRC_DOI_MANAGEMENT`)
4. [Job Application Flow Configuration](job-application-flow-configuration/SKILL.md) (`ORA_IRC_APPLY_FLOW_CONFIGURATION`)

## Inputs

- `implementation_objective`
- `project_context`
- `candidate_experience_scope`
- `candidate_experience_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
