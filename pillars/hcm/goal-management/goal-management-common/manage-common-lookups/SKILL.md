---
skill_id: "hcm.goal-management.goal-management-common.manage-common-lookups"
name: "Manage Common Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Common Lookups under the Goal Management Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Management Common"
functional_area_code: "ORA_GOAL_MANAGEMENT_COMMON"
task_code: "FND_MANAGE_COMMON_LOOKUPS"
task_name: "Manage Common Lookups"
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
  - "core.fusion-api.apps-common.lookups"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-common-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-management-common/manage-common-lookups/current/"
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

# Manage Common Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Common Lookups` under `Goal Management Common`.

## Setup Task Skill Contract

- task_code: `FND_MANAGE_COMMON_LOOKUPS`
- task_name: `Manage Common Lookups`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Common Lookups` under `Goal Management Common`.

## Goal Management best-practice context

Consult sections 2-7 and 9 of the [HCM Goal Management best-practice
reference](../best-practice-rules/hcm-goal-management/README.md)
for lookup governance, high-impact lookup review, and migration sequencing.
The reference is advisory; resolve exact lookup identity and reference-data
context in the target tenant and retain the declared provider, validation, and
approval workflow.

## Setup Task Metadata

- Task name: `Manage Common Lookups`
- Task code: `FND_MANAGE_COMMON_LOOKUPS`
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
- Setup task name: `Manage Common Lookups`
- Setup task code: `FND_MANAGE_COMMON_LOOKUPS`




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


## Migrated shared routing: common lookups

This skill is a Goal Management delegation facade. Product validation may use
the owning provider's read interface. Every lookup create, update, delete, or
bulk maintenance request is an independent Apps Common operation; this skill
must not construct its payload or register its API as Goal Management-owned.

# Goal Management Lookup Routing

## Scope

The **Goal Management Skill Dependencies** baseline identifies the P0
Application Lookup Foundation Skill as a dependency of Review Periods, Goal
Plans, Performance Library Goals, and Development Library Goals. This resource
defines the route for a consultant-supplied exact lookup type or lookup code.

## Canonical provider

The required external capability is
`core.fusion-api.apps-common.lookups`, owned by **Common
Applications / ApplCore**. This Goal Management branch does not own,
modify, or create that Core capability. It invokes the declared repository
dependency `core.fusion-api.apps-common` only when that dependency exposes the
required Lookup capability.

Pass `LookupType` exactly as supplied, with an optional exact `LookupCode`.
The shared provider owns category selection and resource-specific identity
rules; do not infer a lookup type from a display meaning or product field.

| Supplied context | Provider behavior |
| --- | --- |
| Exact category is known | Use the supplied Common, Standard, Generic, or Set-Enabled route |
| Category is unknown | Read-only discovery: Common, Standard, Generic, then Set-Enabled; stop at the first exact match |
| Generic lookup | Require exact `ApplicationCode` before treating a result as authoritative |
| Set-Enabled lookup mutation | Require exact returned code-item identity and reference-data-set context |
| `401` or `403` from a candidate route | Stop as authorization/privilege failure; do not try another category |
| Required Lookup capability is unavailable | Return `PROVIDER_SKILL_UNAVAILABLE`; do not create a local replacement |
| Exact lookup type cannot be confirmed | Record `validation_gap`; do not invent a lookup type or category |

## Lookup subfunction binding

Select the provider subfunction only after the exact type/category is
confirmed. These filenames are external provider metadata, not local skills.

| Confirmed lookup type/category | Required provider reference |
| --- | --- |
| Common | `common-lookups.md` |
| Product-specific or Generic | `generic-lookups.md` |
| Set-Enabled | `set-enabled-lookups.md` |
| Standard | `standard-lookups.md` |

`HZ_GEOGRAPHY_USAGE` and `HZ_GEO_DISPLAY_ONLY` are examples only, not an
allowlist. An unfamiliar exact type follows the same current-provider discovery
contract and returns `validation_gap` if it cannot be confirmed.

## HCM Foundation FSM source metadata

Preserve the following source references as metadata only. They are not
alternative execution routes, APIs, or local skills:

- Manage Organization Lookups
- Manage Location Lookups
- Manage Job Lookups
- Manage Position Lookups
- Manage Person Lookups
- Manage Bargaining Unit Lookup
- Manage Assignment Grade Lookups
- Manage Work Terms and Assignment Lookups
- Manage Employment Contract Lookups
- Manage Termination Lookups
- Document Type Lookups
- Manage Payroll Lookups for China
- Manage Payroll Lookups for UK
- Payroll Lookups
- Workforce Management Lookups
- Manage Common Lookups
- Manage Extended Lookup Codes
- Manage Global Absences Lookups
- Manage Assignment Responsibility Lookups

## Product-local validation remains separate

| Product route | Runtime validation lookup | Foundation management route |
| --- | --- | --- |
| Review Periods | `ACTIVE_INACTIVE` through public `commonLookups/{LookupType}?expand=lookupCodes` | Any consultant lookup read or maintenance request uses Apps Common |
| Goal Plans | No Goal Plan-specific lookup type is asserted by this branch | Any consultant lookup read or maintenance request uses Apps Common |
| Performance Library Goals | `HRG_PERF_GOAL_CATEGORY`, `HRG_SUB_TYPE_CODE`, `HRG_GOAL_MEASUREMENT_LEVEL`, `HRG_PRIORITY`, `HRG_GOAL_TASK_TYPE`, `HRG_GOAL_QUANTITATIVE_UOM`, and `HRG_GOAL_TYPE` through public `commonLookups/{LookupType}?expand=lookupCodes` | Exact lookup request uses Apps Common |
| Development Library Goals | `HRG_DEV_GOAL_CATEGORY`, `HRG_GOAL_MEASUREMENT_LEVEL`, `HRG_PRIORITY`, `HRG_GOAL_TASK_TYPE`, `HRG_GOAL_QUANTITATIVE_UOM`, and `HRG_GOAL_TYPE` through public `commonLookups/{LookupType}?expand=lookupCodes` | Exact lookup request uses Apps Common |

For every product-local validation lookup, retain only codes with
`EnabledFlag=Y` whose active date range includes the current date. Resolve an
exact code or an unambiguous normalized meaning; otherwise return the current
code/meaning list and require a selection. Never use an ADF
`commonLookupsLOV`, an `rv:` revision, or a captured tenant value.

The table is not an allowlist. For an unfamiliar exact lookup type, use the
provider's discovery contract and return diagnostics rather than guessing.
Keep product and lookup operations as independent child routes. Every lookup
write requires provider-owned current-state preview and explicit approval.

## Goal Management runtime adapter

For a Goal Management payload, route a `common_lookup_resolution_request` to
Apps Common with `lookup_type`, exactly one requested `code` or `meaning`, and
the run date. The Goal Management adapter
`scripts/resolve_effective_lookup_code.py` accepts the Apps Common response and applies this pillar's enabled/effective and unambiguous-match rules. It does not accept credentials or invoke REST. A missing or ambiguous result is `NOT_ABLE_TO_EXECUTE` before a
mutation, not a fallback to a captured value.
