---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.regulations"
name: "Benefit Regulations Setup Task Guidance"
description: "Provides date-effective HDL guidance for Benefit Regulations under Benefits General Configuration."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_REGULATIONS"
task_name: "Regulations"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitRegulations"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "requested_operation"
  - "effective_date_context"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "effective_of_derivation"
  - "hdl_preflight_result"
  - "load_diagnostic"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.benefits-configuration.benefits-general-configuration"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/regulations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/regulations/current/"
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

# Benefit Regulations Setup Task Guidance

## Purpose

Plan, validate, and prepare date-effective HDL for `benefitRegulations`. This
skill does not authorize, upload, or retry a Fusion load.

## HDL Route and Source of Truth

Use `core.data-loader` and the current `benefitRegulations` HDL sample. The
sample is authoritative for the DAT filename, section hierarchy, headers,
required attributes, user keys, permitted `RestAction` values, and supported
date-effective operations. Confirm date-effectivity and `effectiveOf` availability
for every included section separately; omit `effectiveOf` from a section that
does not expose it and stop if the section contract is missing or ambiguous.
Do not substitute CSV, REST, browser entry, a task
label, or a guessed object or field.

## Deriving `effectiveOf`

Derive `effectiveOf` per HDL row only for sections whose current sample exposes
it and supports the requested operation; never accept a caller-authored range
string or infer a child contract from its parent.
Require an ISO date (`YYYY-MM-DD`) for every applicable range directive. An
omitted create start date may use the target environment's current date only
after explicit user confirmation. Non-create operations never default the
operation effective date, range, deletion scope, or destructive intent.
For a supported Create, Update, or Correction row whose current section exposes
`EffectiveEndDate`, default an omitted value to the end-of-time date
`4712/12/31` and serialize it as `4712-12-31` in the ISO DAT field. Preserve
an explicitly supplied valid end date. An End date operation requires an
explicit end date and never uses this default.
Serialize every required date inside the derived `effectiveOf` as `YYYY-MM-DD`
with zero-padded month and day. Reject an invalid or ambiguous date instead
of guessing its format, and inspect the final DAT for that exact format.

| Requested operation | Derived `effectiveOf` | Required date or intent |
| --- | --- | --- |
| Create | `RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Explicit or explicitly confirmed create start date |
| Update | `RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Explicit update effective date |
| Correction | `RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Exact existing slice start date |
| End date | `RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate as YYYY-MM-DD>` | Explicit end date |
| Delete changes | `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Explicit date and delete-changes scope |
| ZAP | `RangeMode=ZAP` | Explicit destructive intent |

Apply a mapping only if the current HDL sample supports that operation. The
range directive belongs inside `effectiveOf`, not in a separate DAT column.
For updates, corrections, end dates, delete changes, and ZAP, resolve the exact
existing identity and date-effective slice before preparing the artifact.

## Gates

1. Confirm task `BEN_MANAGE_REGULATIONS`, object `benefitRegulations`, target
   environment, requested operation, and active Run Book.
2. Retrieve the current HDL sample and validate the source against it.
3. Confirm each included section's date-effective contract, then derive and
   inspect `effectiveOf` in every row whose section exposes it in the final
   immutable DAT or ZIP. Verify it is absent from all other sections.
4. Preflight through `core.data-loader`; any source, target, object, effective
   date, or artifact change invalidates that result and any prior approval.
5. Use the Data Loader approval workflow immediately before a live upload or
   initiation. Never retry a mutation automatically.

## Failure Handling

Load `ora-resource/ora_input_validation.md` and
`ora-resource/ora_error_handling.md` before preflight or live activity. Persist
only sanitized diagnostics: task code, environment, artifact reference,
request/process identifiers, status, and recommended next action. Never persist
or disclose credentials, tokens, private keys, full base64 payloads, or
customer-sensitive values.

## Implementation Notes

Use the parent functional-area skill for sequencing and scope decisions. Track
token usage for any generated project artifact or skill-run record using the
manifest policy.
