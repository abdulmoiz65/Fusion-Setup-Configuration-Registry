---
skill_id: "hcm.workforce-scheduling-management.workforce-scheduling-common"
name: "Workforce Scheduling Common Implementation Guidance"
description: "Provides HCM Workforce Scheduling Management implementation guidance for the Workforce Scheduling Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
functional_area: "Workforce Scheduling Common"
functional_area_code: "ORA_WORKFORCE_SCHEDULING_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce scheduling management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "workforce_scheduling_common_scope"
  - "workforce_scheduling_common_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/workforce-scheduling-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/workforce-scheduling-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/workforce-scheduling-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
  - "FND_MANAGE_COMMON_LOOKUPS"
  - "FND_MANAGE_STANDARD_LOOKUPS"
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
  - "FND_MANAGE_KEY_FLEXFIELDS"
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

# Workforce Scheduling Common Implementation Guidance

## Purpose

Provides HCM Workforce Scheduling implementation guidance for the Workforce Scheduling Common functional area.

## When to Use

Use this functional-area skill after Workforce Scheduling scope is confirmed and the project needs Workforce Scheduling Common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Scheduling Management` (`ORA_WORKFORCE_SCHEDULING_MANAGEMENT`)
- Functional area / Setup Object: `Workforce Scheduling Common` (`ORA_WORKFORCE_SCHEDULING_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Standard Lookups](manage-standard-lookups/SKILL.md) (`FND_MANAGE_STANDARD_LOOKUPS`)
5. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
6. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
7. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)
8. [Manage Key Flexfields](manage-key-flexfields/SKILL.md) (`FND_MANAGE_KEY_FLEXFIELDS`)

## Common Applications Provider Invocation

Before proposing a Common Applications configuration change, invoke the named
provider through its route, retain the provider's current-state and
product-recommended-state evidence, and compare the two. The consuming skill
only presents that evidence and requests confirmation for a required change;
the provider retains setup-task, validation, execution, and CRUD ownership.

| Provider dependency | Provider product/team | Invocation route | Required route field | FSM source references |
|---|---|---|---|---|
| core.fusion-api.apps-common.profile-options | Common Applications / ApplCore | manage-profile-options | profileOptionCode: an exact confirmed product identifier | Manage Administrator Profile Values |
| core.fusion-api.apps-common.lookups.references | Common Applications / ApplCore | manage-lookups | lookupType: an exact confirmed product identifier | Manage Common Lookups; Manage Extended Lookup Codes |

The labels in the FSM source-reference column are traceability evidence, not
substitutes for a runtime identifier. Do not derive, normalize, or invent
`profileOptionCode` or `lookupType`. If it is not confirmed, return the
unresolved provider gap and stop before invoking the provider. Apply a change
only when the provider evidence identifies a difference required for the
requested implementation outcome and the user confirms the exact provider-owned
change.

## Inputs

- `implementation_objective`
- `project_context`
- `common_scope`
- `common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
