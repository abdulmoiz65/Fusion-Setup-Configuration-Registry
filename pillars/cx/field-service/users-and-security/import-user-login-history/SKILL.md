---
skill_id: "cx.field-service.users-and-security.import-user-login-history"
name: "Import User Login History Setup Task Guidance"
description: "Provides task-specific setup guidance for Import User Login History under the Users and Security functional area."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "ORA_ASE_IMPORT_USER_LOGIN_HISTORY"
task_name: "Import User Login History"
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
  - "ess_job_submission_plan"
  - "ess_job_execution_result"
  - "ess_job_diagnostics"
  - "ess_job_audit_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "common.security-console.user-security-common"
  - "schemas/ess-delegation-contract.schema.json"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/import-user-login-history/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/import-user-login-history/current/"
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
  - "Delegates Import User Login History ESS scheduling and execution to common.security-console.user-security-common; that skill requires explicit approval before submitting the job."
required_privileges:
  - "Fusion privileges appropriate to submit and monitor the approved Import User Login History ESS job"
---

# Import User Login History Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Import User Login History` under `Users and Security`.

## Canonical ESS Delegation Contract

Use only `schemas/ess-delegation-contract.schema.json` version `1.0`. This
pillar skill supplies a `classification_request`, never an `ess_job_contract`:
the Common skill owns approved job-definition defaults and builds the core
payload. The older `ess_job_contract` example below is legacy guidance and
must not be used for a live invocation.

Propagate `common.security-console.user-security-common`'s unidentified
submission recovery response unchanged; do not add a task-owned retry or lookup.

## Setup Task Skill Contract

- task_code: `ORA_ASE_IMPORT_USER_LOGIN_HISTORY`
- task_name: `Import User Login History`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Import User Login History` under `Users and Security`.

## ESS Execution Route

When this skill is called to perform the task, invoke
`common.security-console.user-security-common` for **Import User Login
History** (`ORA_ASE_IMPORT_USER_LOGIN_HISTORY`) and ask it to run the ESS job.
Pass this task contract to the shared skill:

```json
{
  "requested_fsm_tasks": [
    {
      "taskName": "Import User Login History",
      "taskCode": "ORA_ASE_IMPORT_USER_LOGIN_HISTORY"
    }
  ],
  "ess_job_contract": {
    "jobDefinitionId": "JobDefinition://oracle/apps/ess/hcm/users/AseInactiveUsersDataLoadJob",
    "application": "EarHcmEss",
    "requestParameters": [],
    "schedule": {
      "timezone": "{current_iana_timezone}",
      "recurrences": [
        {
          "icalString": "FREQ=DAILY;INTERVAL=1;",
          "startDate": "{current_timestamp_in_current_timezone}",
          "endDate": "{current_timestamp_in_current_timezone_plus_10_calendar_years}"
        }
      ]
    }
  }
}
```

Resolve the three schedule placeholders immediately before presenting the
submission payload: use the active IANA time zone, the current timestamp in
that time zone, and the timestamp exactly 10 calendar years later. Do not
submit placeholder values literally.

The shared skill must validate the resolved schedule and job contract, target
environment, privileges, and polling settings, then display the complete
payload and obtain explicit user approval before it calls
`core.fusion-api.ess-job-submitter`. Return its execution result, diagnostics,
and audit summary to this skill. Do not use `core.data-loader` for this ESS
task.

## Preflight Checks

Before delegating an ESS submission, confirm all of the following:

1. The requested task is exactly `Import User Login History`
   (`ORA_ASE_IMPORT_USER_LOGIN_HISTORY`) and remains classified as `ESS` by
   `common.security-console.user-security-common`.
2. The target Fusion environment identity, required privileges, and session
   authorization are confirmed.
3. The job definition, application, and `requestParameters: []` match the
   shared skill's default contract unless the caller explicitly provides a
   validated replacement.
4. The schedule placeholders are resolved to valid values; the start time is
   not after the end time; the recurrence is supported; and the ESS job accepts
   scheduled execution.
5. The project workspace is available for the execution audit and diagnostics.
6. The complete resolved payload, polling interval, timeout, and target
   environment have been displayed, and the user has explicitly approved the
   live submission.

Fail closed with `input_validation`, `catalog_or_metadata_mismatch`,
`authorization_or_privilege`, or `approval_blocker` as applicable. Do not
delegate a live ESS call when any preflight check fails.

## Failure Handling

Classify a delegation or ESS outcome as `input_validation`,
`catalog_or_metadata_mismatch`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

For a rejected or failed submission, retain the shared skill's structured
execution result, diagnostics, and audit summary. Preserve the job definition,
target environment, request ID, process ID, ECID, last status, elapsed time,
and a concise recommended action in the project audit when available. For a
timeout, stop polling and ask for fresh approval before resuming tracking or
submitting another request. Do not retry a live ESS submission after a failure,
timeout, or indeterminate result without an idempotency-safe recovery path or
fresh explicit approval. If the audit cannot be persisted, return an
`artifact_persistence` failure without discarding the safe diagnostic summary.

## Security and Redaction

Redact credentials, OAuth access or refresh tokens, token-cache contents,
private keys, tenant secrets, customer data, and sensitive request values from
the task response and every persisted execution audit. Never print, persist, or
include these values in diagnostics, approval prompts, completion evidence, or
test fixtures. Retain only sanitized identifiers and diagnostics needed for
recovery, such as the request ID, process ID, ECID, job definition, status,
and target-environment label.

## Setup Task Metadata

- Task name: `Import User Login History`
- Task code: `ORA_ASE_IMPORT_USER_LOGIN_HISTORY`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `ESS`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. This task's execution route is the ESS workflow above. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


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
- `ess_job_submission_plan`
- `ess_job_execution_result`
- `ess_job_diagnostics`
- `ess_job_audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.field-service.users-and-security` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
