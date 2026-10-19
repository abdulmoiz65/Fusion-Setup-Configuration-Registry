---
skill_id: "hcm.goal-management.goal-management-common.manage-profile-options"
name: "Manage Profile Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Profile Options under the Goal Management Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Management Common"
functional_area_code: "ORA_GOAL_MANAGEMENT_COMMON"
task_code: "FND_MANAGE_PROFILE_OPTIONS"
task_name: "Manage Profile Options"
parent_skill_id: "hcm.goal-management.goal-management-common"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.profile-options"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
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

# Manage Profile Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Profile Options` under `Goal Management Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_PROFILE_OPTIONS`
- task_name: `Manage Profile Options`
- parent_skill_id: `hcm.goal-management.goal-management-common`
- pillar: `HCM`
- offering: `Goal Management`
- functional_area: `Goal Management Common`
- functional_area_code: `ORA_GOAL_MANAGEMENT_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Profile Options` under `Goal Management Common`.

## Goal Management best-practice context

Consult sections 2-8 of the [HCM Goal Management best-practice
reference](../best-practice-rules/hcm-goal-management/README.md)
for profile-option and feature-control design. The reference never validates a
profile code or authorizes a change: resolve exact tenant metadata and retain
the declared provider, export/import, validation, and approval workflow.

## Setup Task Metadata

- Task name: `Manage Profile Options`
- Task code: `FND_MANAGE_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is catalog metadata only in this Goal Management
facade. It does not authorize this skill to export, construct, validate, or import
a dependency mutation package. Route any dependency maintenance to the owning
provider named in [Dependent Setup Routing](../../goal-management-common/dependent-setup-routing.md);
that provider chooses its supported single-record or bulk/setup-import workflow.

Use this task metadata when invoking those skills:

- Offering: `Goal Management`
- Functional area / Setup Object: `Goal Management Common`
- Setup task name: `Manage Profile Options`
- Setup task code: `FND_MANAGE_PROFILE_OPTIONS`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.goal-management.goal-management-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.


## Migrated shared routing: profile options

This skill is a Goal Management delegation facade. It may request provider
reads, but it never constructs or executes a profile mutation. A configured
value mutation is an independent provider-owned route; multiple changes require
the provider's supported bulk/setup-import workflow and must not be simulated
as a loop of single REST writes.

# Goal Management Profile-Option Routing

## Scope

The **Goal Management Skill Dependencies** baseline identifies the P0
Application Profile Option Foundation Skill as a dependency of Review Periods,
Goal Plans, Performance Library Goals, and Development Library Goals. This
resource applies that dependency to the four local product routes.

## Canonical provider

The required external capability is
`core.fusion-api.apps-common.profile-options`, owned by **Common Applications /
ApplCore**. This Goal Management branch does not own, modify, or create
that Core capability. It invokes the declared repository dependency
`core.fusion-api.apps-common` only when that dependency exposes the required
Profile Options capability.

Pass every exact consultant-supplied profile option code unchanged as
`ProfileOptionName`; the provider reads the `profileOptions` definition and the
appropriate value resource. A supplied code is not assumed to be valid, Goal
Management-specific, enabled, or updatable until the provider verifies it.

## Semantic resolution during intake

### Task validation resources

Use the compiled [task registry](ora-resource/ora_rule_registry.json) and its
source guidance for this task's validation:

- [Input validation](ora-resource/ora_input_validation.md)
- [Provider lookups](ora-resource/ora_reference_lookups.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)

The registry validates this delegation facade only. Its ready terminal does not
authorize or execute a profile update, and it does not order other setup tasks.
Keep the semantic catalog below: it is a runtime dependency of intake even when
this task is not selected as a standalone Run Book task.

When the consultant supplies a behavior rather than a profile code, use the
declarative [profile-option semantic catalog](ora-resource/profile-option-semantic-catalog.json)
through [the intake resolver](../implementation-intake/scripts/resolve_goal_management_profile_options.py).
Resolve a code, owning product, requested stored value, and a declared default
level only when exactly one catalog entry and one entry-specific value meaning
match. Match intent and prose value aliases only as whole words or phrases, honor
explicit negation, and fail closed when wording is neutral, uncertain, or
contradictory. Treat an explicit `requested_value` as an exact supported meaning
or alias, never as a substring. Record every default explicitly in the review
package.

The catalog maps values per profile; it never applies a global `Yes`/`No` to
`Y`/`N` rule. If profile ownership, intent, value meaning, or required level
cannot be resolved or defaulted, ask one targeted consultant question. Current
tenant metadata still validates the definition, valid levels, permitted values,
and effective value before a preview or execution.

| Request | Provider operation | Result |
| --- | --- | --- |
| "Show/read/check profile option `CODE`" | `read_definition` or `read_effective` | Current definition or effective value, with scope provenance |
| "Set/update profile option `CODE`" | Handoff to `hcm.goal-management.goal-management-common.manage-administrator-profile-values` | Route value maintenance to `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`; stop for provider-owned exact-value preview and explicit approval |
| Required Profile Options capability is unavailable | N/A | Return `PROVIDER_SKILL_UNAVAILABLE`; do not create a local replacement |
| Code is unknown, missing, or ambiguous | `read_definition` | Record `validation_gap` with provider diagnostics; never guess a code |

## HCM Foundation FSM source metadata

Preserve the following source references as metadata only. They are not
alternative execution routes, APIs, or local skills:

- Manage Workforce Records Profile Option Values
- Manage Workforce Records Employment Profile Option Values
- Payroll Employment Hierarchy Profile Option Values
- Manage Administrator Profile Values
- Manage Profile Options
- Manage Address Validation Profile Options

## Known Goal Management references

| Product route | Confirmed code or code family | Use |
| --- | --- | --- |
| Review Periods | No object-specific code confirmed | Accept any exact consultant-supplied code through the common provider |
| Goal Plans | `HRG_GP_MAX_THREADS`, `HRG_GP_MINCOUNT_EACHTHREAD`, `HRG_GP_MINCOUNT_LASTTHREAD` | Read/explain assignment-throughput behavior; this product task never tunes them |
| Goal Plans | `ORA_HCM_VBCS_PWA_ENABLED`, `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` | Readiness check for Redwood Goal Center UI validation |
| Goal Management | `HRG_USE_GOAL_MANAGEMENT`, `HRG_COMPLETED_GOAL_EDIT_OPTIONS`, `ORA_HRG_DEFAULT_GOAL_SORT_OPTION`, `ORA_HRG_GOALS_SEARCH_BY_PERSON`, `ORA_HRG_REQUEST_FEEDBACK_ENABLED` | Read only when the corresponding Goal Management behavior is in scope |
| Performance Library Goals | `HRG_ALLOW_DECIMALS_IN_WEIGHTS` | Read before a fractional-weight mutation |
| Development Library Goals | `HRG_ALLOW_DECIMALS_IN_WEIGHTS` | Read before a fractional-weight mutation |
| Career Development | `ORA_HRD_COMPLETED_GOAL_EDIT_OPTIONS`, `ORA_HRD_DELETE_HR_ASSIGNED_GOALS`, `ORA_HRD_INACTIVATE_HR_ASSIGNED_GOALS`, `ORA_HRD_CAREER_AMBASSADORS_ENABLED` | Read only when the associated development-goal or Career Ambassadors behavior is in scope |

The table is a known-reference list, not an allowlist. A consultant can supply
another exact code for any product route. Keep the profile request separate
from the product-object request and preserve independent approval boundaries.
