---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.enrollment-authorizations"
name: "Enrollment Authorizations Setup Task Guidance"
description: "Provides task-specific setup guidance for Enrollment Authorizations under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_AUTHORIZATION"
task_name: "Enrollment Authorizations"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitLegalDisclaimers"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
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
  - "hdl_preflight_result"
  - "load_diagnostic"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.benefits-configuration.benefits-general-configuration"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.diagnostics.role-access-check"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/enrollment-authorizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/enrollment-authorizations/current/"
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
side_effects:
  - "Reads selected-environment benefitProgramsLOV and benefitPlansLOV when the active workflow authorizes reference validation."
required_privileges:
  - "Read access to selected-environment benefit program and plan LOVs for supplied names."
---

# Enrollment Authorizations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Enrollment Authorizations` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_AUTHORIZATION`
- task_name: `Enrollment Authorizations`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `benefitLegalDisclaimers`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Enrollment Authorizations` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Enrollment Authorizations`
- Task code: `BEN_MANAGE_AUTHORIZATION`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitLegalDisclaimers`

## HDL Business Object and Routing

Use `core.data-loader` for all Enrollment Authorizations imports. The supported HDL business object is `benefitLegalDisclaimers`; do not substitute the setup-task label, a guessed REST resource, FSM CSV, browser entry, or another import route.

Generate or retrieve the current Data Loader sample before preparing a DAT. The live sample is authoritative for the case-sensitive filename stem, METADATA header, section hierarchy, user keys, required attributes, permitted RestAction values, and delete support. Do not infer legal-disclaimer attributes, identity fields, or action syntax from this task name.

When `StartDate` or `EndDate` is present in the current sample and supplied for a record, normalize its date-only value to `YYYY-MM-DD` before creating the immutable artifact. Preserve a blank optional `EndDate`; reject a malformed, time-bearing, or timezone-bearing value rather than silently changing its meaning.

For each supplied `benefitLegalDisclaimers.ProgramName` or `PlanName`, use the
read-only [reference lookup rules](ora-resource/ora_reference_lookups.md) to
require an exact `Name` match in `benefitProgramsLOV` or `benefitPlansLOV`.
Run these checks through `core.fusion-api.rest-api-client` only when the active
project workflow selects the lookup step. A 403 records
`unverified_forbidden` without failing field validation; it does not verify
the value. Resolve access or use another workflow-approved authoritative
check before a live load. Keep DAT validation and loading on `core.data-loader`.

## HDL Operations and Gates

| Requested operation | HDL route | Control point |
| --- | --- | --- |
| Create or merge | Prepare a benefitLegalDisclaimers DAT only from the current sample. | Preflight the immutable artifact and obtain Data Loader approval before upload. |
| Update | Prepare an update DAT only when the current sample supports the required identity and action. | Do not guess user keys or PATCH semantics; revalidate and obtain new approval. |
| Delete | Prepare a delete DAT only when current metadata supports deletion and the user explicitly requests it. | Treat as destructive and require explicit approval immediately before upload. |
| Read or verify | Inspect workflow-selected metadata or data-load status. | A read does not authorize a subsequent load. |

## Preflight and Approval Gates

1. Confirm task `BEN_MANAGE_AUTHORIZATION`, object `benefitLegalDisclaimers`, intended environment, and active project Run Book.
2. Generate or retrieve the current sample; validate source filename, headers, action syntax, user keys, required values, record relationships, and date values. Normalize supplied `StartDate` and `EndDate` values to `YYYY-MM-DD` before artifact immutability is established.
3. Validate each supplied ProgramName and PlanName independently through its
   selected read-only LOV. Record `valid`, `invalid`, `ambiguous`, or
   `unverified_forbidden` per row and field. Stop on an ambiguous identity,
   missing prerequisite, unsupported action, schema mismatch, or CSV route.
4. Preflight the final immutable archive through `core.data-loader`.
5. Use the current Data Loader approval gate immediately before upload or initiation. Any source, environment, Run Book, object, or artifact change invalidates approval.

## Failure Handling

Load task-local `ora-resource/ora_input_validation.md`,
`ora_reference_lookups.md`, and `ora_error_handling.md` before preflight or
live activity. Never automatically retry an upload, initiation, update, or
delete. On failure or an uncertain outcome, retain sanitized artifact and
request evidence, reconcile through the selected read-only status route, and
require new approval for any later load.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.




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

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
