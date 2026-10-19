---
skill_id: "hcm.goal-management.goal-management-common"
name: "Goal Management Common Implementation Guidance"
description: "Provides HCM Goal Management implementation guidance for the Goal Management Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Management Common"
functional_area_code: "ORA_GOAL_MANAGEMENT_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "goal_management_common_scope"
  - "goal_management_common_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/current/"
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
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
  - "FND_MANAGE_KEY_FLEXFIELDS"
  - "FND_MANAGE_REFERENCE_DATA_SETS"
  - "FND_MANAGE_CURRENCIES"
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

# Goal Management Common Implementation Guidance

## Purpose

Provides HCM Goal Management implementation guidance for the Goal Management Common functional area.

## When to Use

Use this functional-area skill after Goal Management scope is confirmed and the project needs common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Goal Management` (`ORA_GOAL_MANAGEMENT`)
- Functional area / Setup Object: `Goal Management Common` (`ORA_GOAL_MANAGEMENT_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
5. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
6. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)
7. [Manage Key Flexfields](manage-key-flexfields/SKILL.md) (`FND_MANAGE_KEY_FLEXFIELDS`)
8. [Manage Reference Data Sets](manage-reference-data-sets/SKILL.md) (`FND_MANAGE_REFERENCE_DATA_SETS`)
9. [Manage Currencies](manage-currencies/SKILL.md) (`FND_MANAGE_CURRENCIES`)

## Inputs

- `implementation_objective`
- `project_context`
- `goal_management_common_scope`
- `goal_management_common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For a Goal Management REST mutation, ESS submission, or other live operation,
apply the shared [Goal Management approval convention](approval-convention.md).
Keep fingerprints and structured approval envelopes as internal integrity
bindings; never require a consultant to copy a SHA-256 value to approve an
unchanged preview. A `core.data-loader` route continues to use Core's
authoritative approval contract.

## Current Common-task routing

The generated child skills preserve catalog task identity and add Goal
Management business context. They are delegation facades, not owners of shared
setup REST mutations. Read and apply
[Goal Management Dependent Setup Routing](dependent-setup-routing.md) before
selecting any Common dependency operation.

Goal Management may invoke an owning provider's read interface to resolve an
existing value needed by a Goal Management object. Any create, update, delete,
deployment, import, or setup maintenance request must leave Goal Management as
an independent child route. `Manage Reference Data Sets` and `Manage
Currencies` remain catalog-backed identities, but their execution belongs to
the owning Common or manual workflow. Do not register their mutation APIs as
Goal Management-owned.

When a prompt contains a product-object request and Common work, create two
independent child routes. Approval for one child never authorizes the other.
For multiple dependency changes, use only the owning provider's declared bulk
or setup-import route; never loop single-record REST writes from this skill.
