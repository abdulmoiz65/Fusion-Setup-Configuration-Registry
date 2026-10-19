---
skill_id: "cx.field-service.users-and-security.run-user-and-roles-synchronization-process"
name: "Run User and Roles Synchronization Process Setup Task Guidance"
description: "Provides task-specific setup guidance for Run User and Roles Synchronization Process under the Users and Security functional area."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS"
task_name: "Run User and Roles Synchronization Process"
parent_skill_id: "cx.field-service.users-and-security"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX field service pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/run-user-and-roles-synchronization-process/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/run-user-and-roles-synchronization-process/current/"
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

# Run User and Roles Synchronization Process Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Run User and Roles Synchronization Process` under `Users and Security`.

## Canonical ESS Delegation Contract

Use only `schemas/ess-delegation-contract.schema.json` version `1.0`. Submit a
`classification_request` to `common.security-console.user-security-common`;
it must contain the task identity, environment context, requested payload
overrides, polling options, and `explicit_submission_approval: false`. The
Common skill alone resolves the job contract and creates the approved payload.
The nested `request_payload` and duplicated approval example below is legacy
guidance and must not be used.

Propagate `common.security-console.user-security-common`'s unidentified
submission recovery response unchanged; do not add a task-owned retry or lookup.

## Setup Task Skill Contract

- task_code: `PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS`
- task_name: `Run User and Roles Synchronization Process`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Run User and Roles Synchronization Process` under `Users and Security`.

## Setup Task Metadata

- Task name: `Run User and Roles Synchronization Process`
- Task code: `PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `ESS`
- Business Object: ``

## Run Synchronization Process

When this skill is run to execute the synchronization process, invoke
`common.security-console.user-security-common`. That shared skill owns the
FSM-task execution classification and, for approved ESS tasks, routes
submission and status tracking to `core.fusion-api.ess-job-submitter`. Do not
call the Fusion ESS REST API directly or invoke the core ESS skill from this
pillar skill.

### Shared Skill Invocation Contract

On every invocation of this pillar skill for this setup task, invoke
`common.security-console.user-security-common` with the following input
mapping. Ask the shared skill to run the ESS job for **Run User and Roles
Synchronization Process** by constructing `requested_fsm_tasks` exactly as
shown. Do not supply a default ESS payload; provide only the request
parameters, environment context, and execution options.

### Default Monitoring Timeout

Unless the caller explicitly supplies `execution_options.monitoring_timeout_seconds`,
set it to `420` (7 minutes). Use the same value as the ESS submitter's
`wait_seconds` limit. A caller-supplied timeout overrides this default and
must be included in the approval presented immediately before submission.

```json
{
  "implementation_objective": "<implementation_objective input>",
  "project_context": "<project_context input>",
  "requested_fsm_tasks": [
    {
      "task_name": "Run User and Roles Synchronization Process",
      "task_code": "PER_USER_AND_ROLES_SYNCHRONIZE_DETAILS",
      "fusion_environment_context": "<fusion_environment_context input>",
      "request_payload": {
        "requestParameters": []
      },
      "execution_options": {
        "monitoring_timeout_seconds": 420,
        "poll_interval_seconds": "<execution_options.poll_interval_seconds or default>",
        "explicit_submission_approval": "<execution_options.explicit_submission_approval>"
      },
      "explicit_submission_approval": "<execution_options.explicit_submission_approval>"
    }
  ]
}
```

Always pass `request_payload.requestParameters` as `[]`. Preserve the caller's
`fusion_environment_context` and `execution_options`, except to add the
default `monitoring_timeout_seconds: 420` when it is absent. The shared skill
receives the task context, classifies it as `ESS`, resolves its configured job
contract, and enforces its own approval gates.

The shared skill confirms that this FSM task is classified as `ESS`; it must
not infer the job contract from the task code. It then validates the exact
Oracle `jobDefinitionId`, request parameters, privileges, timeout, and
approval before using its core dependency. Use the shared skill's
`task_execution_classification`, `ess_job_submission_plan`, and
`execution_audit` outputs as this skill's execution result. If the request
times out or fails, retain the returned diagnostics and follow the shared
skill's retry and tracking guidance; do not resubmit without idempotency or
fresh explicit approval.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


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
- `task_execution_classification`
- `completion_evidence_checklist`
- `ess_job_submission_plan`
- `execution_audit`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.field-service.users-and-security` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
