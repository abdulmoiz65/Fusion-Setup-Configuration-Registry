---
skill_id: "hcm.workforce-time-management.time-and-labor-common"
name: "Time and Labor Common Implementation Guidance"
description: "Provides HCM Workforce Time Management implementation guidance for the Time and Labor Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Common"
functional_area_code: "ORA_TIME_AND_LABOR_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "time_and_labor_common_scope"
  - "time_and_labor_common_requirements"
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
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.apps-common.lookups"
uses_core:
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-common/current/"
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

# Common Implementation Guidance

## Purpose

Provides HCM Time and Labor implementation guidance for the Common functional area.

## When to Use

Use this functional-area skill after Time and Labor scope is confirmed and the project needs common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Workforce Time Management` (`ORA_WORKFORCE_TIME_MANAGEMENT`)
- Functional area / Setup Object: `Time and Labor Common` (`ORA_TIME_AND_LABOR_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Standard Lookups](manage-standard-lookups/SKILL.md) (`FND_MANAGE_STANDARD_LOOKUPS`)
5. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
6. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
7. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)
8. [Manage Key Flexfields](manage-key-flexfields/SKILL.md) (`FND_MANAGE_KEY_FLEXFIELDS`)

## Resource Read Order

For a provider-dependent implementation request, read
`ora-resource/ora_design_enforcement.md` after confirming Common scope and
before querying a provider, comparing configuration state, or proposing a
change.

## Common Applications Provider Dependencies

This consuming skill queries the Common Applications / ApplCore provider before
it proposes a provider-dependent Time and Labor configuration. It does not own
or reproduce provider execution, CRUD behavior, request construction, retry
behavior, or setup-task implementation.

| Foundation Skill | Provider Skill | Provider References | Route | Runtime Identifier Input | Preserved FSM Source References |
|---|---|---|---|---|---|
| Application Profile Option Foundation Skill | core.fusion-api.apps-common.profile-options | core/fusion-api/apps-common/profile-options/references | manage-profile-options | profileOptionCode supplied by the consuming skill | Manage Profile Values |
| Application Lookup Foundation Skill | core.fusion-api.apps-common.lookups | core/fusion-api/apps-common/lookups/references | manage-lookups | lookupType supplied by the consuming skill | Manage Common Lookups; Manage Extended Lookup Codes; Common Lookups; HCM Extended Lookup Code |

### Provider Invocation Contract

1. Determine whether the requested Time and Labor outcome depends on a profile
   option or Common Applications lookup.
2. Require the consuming skill to supply the applicable exact
   `profileOptionCode` or `lookupType` at runtime. Treat the supplied runtime
   value as the provider identifier; do not derive it from an FSM label or ask
   for separate PM confirmation.
3. Invoke the declared provider before proposing a configuration change. Use
   route `manage-profile-options` with `profileOptionCode`, or route
   `manage-lookups` with `lookupType`. Pass the exact consuming-skill value
   unchanged.
4. Retain provider evidence for the before state and compare it with the
   product-recommended state. Show the evidence and validation result.
5. If current state already meets the recommendation, propose no change.
6. If a change is required for the requested implementation outcome, present
   the exact provider-owned change and obtain explicit user confirmation.
7. Let the provider skill perform its own approved mutation and verification.
   Return before state, after state, validation results, and every unresolved
   provider or identifier gap.

### Runtime Identifier Contract

- The consuming skill supplies the exact `profileOptionCode` at runtime. Pass
  that value unchanged to `manage-profile-options`; `Manage Profile Values` is
  retained only as an FSM source reference.
- The consuming skill supplies every applicable exact `lookupType` at runtime.
  Pass each value unchanged to `manage-lookups`; `Common Lookups`,
  `HCM Extended Lookup Code`, `Manage Common Lookups`, and
  `Manage Extended Lookup Codes` are retained as source context and do not
  require a separate PM-confirmation step.
- Use provider skill `core.fusion-api.apps-common.lookups` and load the
  applicable provider guidance from
  `core/fusion-api/apps-common/lookups/references/` before invoking
  `manage-lookups`. The provider is resolved; only a missing runtime identifier,
  missing access, or incomplete provider evidence is an unresolved gap.

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
