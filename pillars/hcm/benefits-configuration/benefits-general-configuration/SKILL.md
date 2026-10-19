---
skill_id: "hcm.benefits-configuration.benefits-general-configuration"
name: "Benefits General Configuration Implementation Guidance"
description: "Provides HCM Benefits Configuration implementation guidance for the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "benefits_general_configuration_scope"
  - "benefits_general_configuration_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "BEN_MANAGE_BENEFIT_GROUPS"
  - "BEN_MANAGE_BENEFIT_BALANCE"
  - "ORA_CONFIGURE_FEATURE_PREFERENCES"
  - "BEN_MANAGE_AUTHORIZATION"
  - "BEN_MANAGE_REGULATIONS"
  - "BEN_MANAGE_GROUP_SPACE"
  - "BEN_MANAGE_PROGRAMS_PLAN_YEARS"
  - "BEN_MANAGE_BENEFICIARY_ORGANIZATION"
  - "BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR"
  - "BEN_MANAGE_BENEFIT_PROVIDER_ORG"
  - "BEN_MANAGE_REGULATORY_BODY"
  - "BEN_MANAGE_LEGAL_ENTITY_INFORMATION"
  - "BEN_MANAGE_BENEFIT_REPORTING_GROUPS"
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

# Benefits General Configuration Implementation Guidance

## Purpose

Provides HCM Benefits Configuration implementation guidance for the Benefits General Configuration functional area.

## When to Use

Use this functional-area skill after Benefits Configuration scope is confirmed and the project needs benefits general configuration setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Benefits Configuration` (`ORA_BENEFITS_CONFIG`)
- Functional area / Setup Object: `Benefits General Configuration` (`ORA_BENEFITS_GENERAL_CONFIGURATION`)

## Setup Tasks

1. [Benefit Groups](benefit-groups/SKILL.md) (`BEN_MANAGE_BENEFIT_GROUPS`)
2. [Benefit Balances](benefit-balances/SKILL.md) (`BEN_MANAGE_BENEFIT_BALANCE`)
3. [Configure Benefits Feature Preferences](configure-benefits-feature-preferences/SKILL.md) (`ORA_CONFIGURE_FEATURE_PREFERENCES`)
4. [Enrollment Authorizations](enrollment-authorizations/SKILL.md) (`BEN_MANAGE_AUTHORIZATION`)
5. [Regulations](regulations/SKILL.md) (`BEN_MANAGE_REGULATIONS`)
6. [Benefit Self-Service Configuration](benefit-self-service-configuration/SKILL.md) (`BEN_MANAGE_GROUP_SPACE`)
7. [Year Periods and Billing Calendars](year-periods-and-billing-calendars/SKILL.md) (`BEN_MANAGE_PROGRAMS_PLAN_YEARS`)
8. [Manage Beneficiary Organizations](manage-beneficiary-organizations/SKILL.md) (`BEN_MANAGE_BENEFICIARY_ORGANIZATION`)
9. [Manage Third-Party Administrators](manage-third-party-administrators/SKILL.md) (`BEN_MANAGE_THIRD_PARTY_ADMINISTRATOR`)
10. [Manage Benefit Providers](manage-benefit-providers/SKILL.md) (`BEN_MANAGE_BENEFIT_PROVIDER_ORG`)
11. [Manage Regulatory Bodies](manage-regulatory-bodies/SKILL.md) (`BEN_MANAGE_REGULATORY_BODY`)
12. [Configure Default Benefits Relationships](configure-default-benefits-relationships/SKILL.md) (`BEN_MANAGE_LEGAL_ENTITY_INFORMATION`)
13. [Benefit Reporting Groups](benefit-reporting-groups/SKILL.md) (`BEN_MANAGE_BENEFIT_REPORTING_GROUPS`)

## Inputs

- `implementation_objective`
- `project_context`
- `benefits_general_configuration_scope`
- `benefits_general_configuration_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For a routed HDL task, confirm date-effectivity, `effectiveOf` availability, and
supported operations separately for every included DAT section using current
target-environment Data Loader metadata before deriving row controls. Where a
section exposes `effectiveOf`, derive it from each row's exact operation and
required date; serialize any embedded date as `YYYY-MM-DD`. Omit `effectiveOf`
from sections that do not expose it. Stop artifact preparation when a section's
date-effective contract is missing or ambiguous; do not infer it from another
section or from the task name. The task-local operation mapping remains the
authority for supported actions and required dates.

For Manage Beneficiary Organizations, follow the
[Organization HDL workflow](manage-beneficiary-organizations/SKILL.md) before
preparing input or requesting upload approval. The configured object is
`Organization`; existing tasks retain their own workflows.

For Manage Regulatory Bodies, follow the
[Organization HDL workflow](manage-regulatory-bodies/SKILL.md) before preparing
input or requesting upload approval. The configured object is `Organization`.
