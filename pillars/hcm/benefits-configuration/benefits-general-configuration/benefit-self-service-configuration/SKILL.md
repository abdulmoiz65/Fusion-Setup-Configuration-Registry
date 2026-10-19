---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.benefit-self-service-configuration"
name: "Benefit Self-Service Configuration Setup Task Guidance"
description: "Provides task-specific setup guidance for Benefit Self-Service Configuration under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_GROUP_SPACE"
task_name: "Benefit Self-Service Configuration"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitSelfServiceConfigurations"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-self-service-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/benefit-self-service-configuration/current/"
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
  - "Reads selected-environment commonLookupsLOV when the active workflow authorizes reference validation."
required_privileges:
  - "Read access to selected-environment commonLookupsLOV for supplied reference fields."
---

# Benefit Self-Service Configuration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Benefit Self-Service Configuration` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_GROUP_SPACE`
- task_name: `Benefit Self-Service Configuration`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `HDL`
- businessObject: `benefitSelfServiceConfigurations`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Benefit Self-Service Configuration` under `Benefits General Configuration`.

## Setup Task Metadata

- Task name: `Benefit Self-Service Configuration`
- Task code: `BEN_MANAGE_GROUP_SPACE`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitSelfServiceConfigurations`

## HDL Business Object and Routing

`CSVExportImportSupportedFlag` is `N`; FSM CSV export/import is not a supported route for this task. This does not prohibit the explicitly selected HDL route.

Use `core.data-loader` for data-changing Benefit Self-Service Configuration activity. The sole approved HDL business object is `benefitSelfServiceConfigurations`. Do not replace it with the setup-task label, a guessed REST resource, browser entry, FSM CSV, or another loader route.

Before creating a DAT, generate or retrieve the current Fusion Data Loader sample for `benefitSelfServiceConfigurations`. That sample is authoritative for the case-sensitive filename stem, `METADATA` header, section hierarchy, supported `RestAction` values, required attributes, user keys, effective dating, and delete support. Do not infer any of these from the task or object name.

When a `benefitSelfServiceConfigurations.AllowUnrestrictedProcessingTypeMeaning`
value is supplied and the current sample confirms that attribute, validate it
through the read-only [reference lookups](ora-resource/ora_reference_lookups.md)
using `LookupType=BEN_ALLOW_SS_UNRST_PROCG`. For a supplied
`SelfServiceEnrollmentPathMeaning`, first confirm that the current
`benefitSelfServiceConfigurations` sample exposes that exact field. Only then
validate it with `LookupType=ORA_BEN_SS_PATH_SELECTION`. Do not infer this
field's presence from `benefitFeaturePreferences` or copy another object's
field into this skill's DAT. If the self-service sample lacks the field,
report the mapping mismatch and omit it from the artifact. Use
`core.fusion-api.rest-api-client` only when the active project workflow
selects these read-only lookups. A 403 records `unverified_forbidden` without
failing field validation or stopping independent checks. It does not verify
the value; resolve access or use another workflow-approved authoritative
check before a live load. Keep DAT validation and loading on
`core.data-loader`.

## Defaulting Rules

`CustomSurrogateUserKey` is a dummy technical attribute. Do not request it from the user or treat it as a record-identity input. Always populate it with the literal value `UPSERT` in each applicable `benefitSelfServiceConfigurations` DAT row.

## Input Validation and Preflight

Perform every check before an artifact becomes immutable or a Fusion-changing action begins:

1. Confirm task `BEN_MANAGE_GROUP_SPACE`, object `benefitSelfServiceConfigurations`, project Run Book status `active`, intended environment, and requested operation.
2. Reject absent or ambiguous record identity, duplicate source identities, unsupported action semantics, malformed or stale sample headers, and values that do not satisfy the current sample's required fields and reference values. Validate each supplied `AllowUnrestrictedProcessingTypeMeaning` and sample-confirmed `SelfServiceEnrollmentPathMeaning` through its selected read-only LOV; record `valid`, `invalid`, `ambiguous`, or `unverified_forbidden` per row and field. Supply `CustomSurrogateUserKey=UPSERT` without requesting user input.
3. Validate the DAT filename, encoding, `METADATA`/data-row column alignment, section hierarchy, record relationships, and any sample-declared date or effective-dating format. Format a supplied `SelfServiceEffectiveDate` as date-only `YYYY-MM-DD`; reject a malformed, time-bearing, or timezone-bearing value rather than silently changing its meaning. Preserve row-level validation errors; do not silently coerce other values.
4. Confirm prerequisite benefits configuration is ready through the selected workflow. An HTTP 403 from the conditional LOV check does not fail field validation; retain `unverified_forbidden` and continue independent checks. Require authoritative verification before live load if reference setup could not be verified.
5. Build a versioned immutable DAT/archive, capture its checksum, and preflight it through `core.data-loader`. A source, target, object, operation, or artifact change requires a new preflight.

## HDL Operations and Approval Gates

| Requested operation | HDL route | Control point |
| --- | --- | --- |
| Create or merge | Prepare a `benefitSelfServiceConfigurations` DAT solely from the current sample. | Validate and preflight the immutable artifact; obtain the Data Loader workflow approval immediately before upload. |
| Update | Prepare an update only when current metadata supports the required identity and action. | Do not guess PATCH or merge semantics; revalidate and obtain fresh approval. |
| Delete | Use a delete DAT only when the current sample supports deletion and the user explicitly requests it. | Treat as destructive and require explicit approval immediately before upload. |
| Read or verify | Inspect workflow-selected metadata or load status. | Read-only inspection does not authorize a later load. |

Any live action is governed by `core.data-loader`'s approval workflow. This skill must not initiate an upload or load merely because a plan, sample, preview, or artifact was approved earlier.

## Error Handling and Diagnostics

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`.

- Fail closed before side effects on invalid input, ambiguous identities, unsupported CSV routing, missing sample guidance, inactive Run Book, privilege failure, overwrite conflict, or missing approval.
- A cache-managed 401/403 may refresh once. Retry read-only transport failures only with bounded attempts. Never automatically retry a live upload, initiation, create, update, or delete; an idempotency key or fresh explicit approval is required.
- For the conditional `commonLookupsLOV` checks, a 403 is `unverified_forbidden`, not an invalid field value; do not throw a field-validation error. It still requires authoritative verification before live load.
- On a timeout, stop polling and record the environment, operation, task code, object, ProcessId/requestId, last status, elapsed wait, and next-check path. Do not submit a second load.
- On terminal failure or partial completion, retrieve the available process log or status payload; preserve successful row outcomes and an `errors` array for failed rows.
- Persist sanitized `hdl_preflight_result` and `load_diagnostic` artifacts under this skill's declared project workspace. Include status, stage, failure class, message, recommended action, environment, artifact references, checksum, and external identifiers. Never print or persist credentials, tokens, token caches, private keys, customer-sensitive values, or full payload contents.

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
- `hdl_preflight_result`
- `load_diagnostic`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Read the task-local `ora-resource/ora_reference_lookups.md` before reference validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
