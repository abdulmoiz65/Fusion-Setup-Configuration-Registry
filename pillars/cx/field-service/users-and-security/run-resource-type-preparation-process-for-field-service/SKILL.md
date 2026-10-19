---
skill_id: "cx.field-service.users-and-security.run-resource-type-preparation-process-for-field-service"
name: "Run Resource Type Preparation Process for Field Service Setup Task Guidance"
description: "Provides task-specific setup guidance for Run Resource Type Preparation Process for Field Service under the Users and Security functional area."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS"
task_name: "Run Resource Type Preparation Process for Field Service"
parent_skill_id: "cx.field-service.users-and-security"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX field service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "ess_delegation_contract"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "payload_preview"
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.field-service.users-and-security"
  - "schemas/ess-delegation-contract.schema.json"
uses_core:
  - "core.fusion-api.ess-job-submitter"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/run-resource-type-preparation-process-for-field-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/run-resource-type-preparation-process-for-field-service/current/"
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
  - "Delegates approved Resource Type Preparation Process ESS submissions and status tracking to core.fusion-api.ess-job-submitter."
required_privileges:
  - "Fusion privileges required to submit and view the configured ESS job."
---

# Run Resource Type Preparation Process for Field Service Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Run Resource Type Preparation Process for Field Service` under `Users and Security`.

## Canonical ESS Delegation Contract

Use only `schemas/ess-delegation-contract.schema.json` version `1.0`. This
skill validates a complete `approved_submission` envelope before calling the
core submitter. Its `request_payload` is the exact approved Scheduler body;
`ess_request_payload` is retired. The job contract, approval hash, target
environment, and polling options must be present in the same envelope.

## Setup Task Skill Contract

- task_code: `ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS`
- task_name: `Run Resource Type Preparation Process for Field Service`
- parent_skill_id: `cx.field-service.users-and-security`
- pillar: `CX`
- offering: `Field Service`
- functional_area: `Users and Security`
- functional_area_code: `ORA_ASK_USERS_AND_SECURITY`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Run Resource Type Preparation Process for Field Service` under `Users and Security`.

## Setup Task Metadata

- Task name: `Run Resource Type Preparation Process for Field Service`
- Task code: `ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `ESS`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Preflight Checks

Load `ora-resource/ora_error_handling.md` before preview or live execution and
apply its disclosure and stop-before-retry rules alongside this skill's
preflight checks.

Before calling `core.fusion-api.ess-job-submitter` or any other side-effecting
operation, complete and persist these preflight checks under the active project
workspace:

1. Confirm the target Fusion environment identity, required ESS privileges, OAuth scopes, and usable session or token-cache state. Classify missing or invalid authentication as `auth_expired_or_invalid`; classify a rejected refreshed session or missing privilege as `authorization_or_privilege`.
2. Confirm this task's catalog identity (`ORA_FFS_RUN_RESOURCE_TYPE_PREPARATION_PROCESS`) and the exact `CrmEss` job contract. Treat a missing or ambiguous task, application, or job definition as `input_validation` or `catalog_or_metadata_mismatch` and stop before invoking the submitter.
3. Validate the default or user-edited payload as JSON. Require one resolved IANA timezone, the `FREQ=HOURLY;INTERVAL=6;` recurrence, an offset-bearing start timestamp, an end timestamp exactly ten calendar years after the start timestamp, and valid polling options.
4. Confirm that payload previews, execution plans, diagnostics, and result files resolve beneath this task's declared project artifact directory. Classify an unsafe or unwritable destination as `artifact_persistence` and make no Fusion call.
5. Identify whether the requested action is preview or live execution. For live execution, display the final immutable payload and exact target environment, then require explicit approval immediately before the first ESS submission. Without approval, classify the stop as `approval_blocker`.

Persist redacted diagnostics for authentication, authorization, transport, Fusion API, timeout, and process failures. For `transport_or_environment` failures, retry only read-only checks with bounded attempts. For `process_timeout`, preserve the request ID, last status, elapsed wait, and next-check path. Do not retry a live ESS submission after any failure or indeterminate outcome without fresh explicit approval.

## ESS Execution Workflow

When the implementation objective is to run `Run Resource Type Preparation Process for Field Service`, delegate the ESS operation to `core.fusion-api.ess-job-submitter`. Do not call Fusion Scheduler REST APIs, handle OAuth tokens, or implement polling directly in this skill.

1. Generate the Default ESS Request Payload below when the caller does not supply a reviewed `ess_request_payload`. Resolve `current_iana_timezone` to the target environment's current IANA time zone, set both timestamps in that zone with their UTC offset, and calculate the end timestamp as exactly ten calendar years after the start timestamp. A caller-provided payload is an editable replacement and must be fully revalidated.
2. Display the fully resolved payload as JSON and let the user modify it. Revalidate the edited payload, target environment, schedule, and polling options; persist the redacted immutable approval payload as `payload_preview`.
3. Immediately before submission, present the exact target environment and approved immutable payload and obtain explicit approval to submit the mutating ESS request.
4. After approval, call `core.fusion-api.ess-job-submitter` with the approved payload, configured polling options, and managed external token-cache reference. Persist the returned request ID, status summary, and diagnostics in the project workspace. On a polling timeout, report the request ID, last status, elapsed wait, and the read-only next-check path. Do not retry a submission after an uncertain or failed request without fresh explicit approval.

`core.fusion-api.ess-job-submitter` owns OAuth refresh, REST submission, polling, and redaction of credentials. This skill owns Field Service task sequencing, exact job-contract validation, approval gating, and project-level audit artifacts.

### Default ESS Request Payload

Unless the user supplies a reviewed replacement payload, call
`core.fusion-api.ess-job-submitter` with this resolved template:

```json
{
  "description": "Run Resource Type Preparation Process for Field Service - Every 6 hours",
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/crm/fieldservice/core/FfsCorePrepareResourceTypesJob",
  "application": "CrmEss",
  "schedule": {
    "timezone": "{current_iana_timezone}",
    "recurrences": [
      {
        "icalString": "FREQ=HOURLY;INTERVAL=6;",
        "startDate": "{current_timestamp_in_current_timezone}",
        "endDate": "{current_timestamp_in_current_timezone_plus_10_calendar_years}"
      }
    ]
  }
}
```

The payload shown to the user for editing and approval must contain the actual
resolved IANA time zone and timestamps, not these placeholders. Do not submit
the template itself.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `ess_delegation_contract`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `payload_preview`
- `execution_result`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.field-service.users-and-security` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Failure Handling and Recovery

- Classify missing job fields or an ambiguous catalog match as `input validation` or `catalog mismatch`; do not invoke the submitter.
- Classify authentication, authorization, transport, Fusion API, timeout, and process failures using the submitter's diagnostics. Persist only redacted diagnostics and returned external identifiers.
- The submitter may refresh a rejected cached token once. Do not retry an ESS submission, import, or other mutation after a failure or indeterminate outcome without explicit user approval.
- For a timeout, retain the request ID and use the submitter's read-only tracking route for the next check. For a terminal failure, retain the status payload or process log when available and present the recommended recovery action.
