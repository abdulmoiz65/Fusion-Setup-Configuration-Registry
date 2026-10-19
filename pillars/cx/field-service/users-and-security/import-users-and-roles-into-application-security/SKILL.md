---
skill_id: "cx.field-service.users-and-security.import-users-and-roles-into-application-security"
name: "Import Users and Roles into Application Security Setup Task Guidance"
description: "Routes Import Users and Roles into Application Security to the shared user-security workflow for approved ESS scheduling and monitoring."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "ORA_ASE_IMPORT_USERS_AND_ROLES"
task_name: "Import Users and Roles into Application Security"
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
version: "0.1.6"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "ess_delegation_contract"
outputs:
  - "setup_task_plan"
  - "ess_job_submission_plan"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
depends_on:
  - "common.security-console.user-security-common"
  - "schemas/ess-delegation-contract.schema.json"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/import-users-and-roles-into-application-security/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/import-users-and-roles-into-application-security/current/"
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

# Import Users and Roles into Application Security Setup Task Guidance

## Purpose

Routes `Import Users and Roles into Application Security` under `Users and Security` to the shared user-security workflow for ESS scheduling and monitoring.

## Canonical ESS Delegation Contract

Use only `schemas/ess-delegation-contract.schema.json` version `1.0`. Pass a
complete `classification_request` envelope to the Common skill, including task
identity, target environment context, schedule/parameter overrides, polling
options, and `explicit_submission_approval: false`. The request-parameter and
schedule fragment below is legacy guidance and is not a valid invocation by
itself.

Propagate `common.security-console.user-security-common`'s unidentified
submission recovery response unchanged; do not add a task-owned retry or lookup.

## Setup Task Skill Contract

- task_code: `ORA_ASE_IMPORT_USERS_AND_ROLES`
- task_name: `Import Users and Roles into Application Security`
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

Use this skill when the `Import Users and Roles into Application Security` ESS process must be planned, scheduled, submitted, or monitored for Field Service.

## Execution Route

Route every invocation of this task to `common.security-console.user-security-common` with:

- Task name: `Import Users and Roles into Application Security`
- Task code: `ORA_ASE_IMPORT_USERS_AND_ROLES`
- Pillar context: `CX` / `Field Service` / `Users and Security`
- Requested shared-skill action: Run the `Import Users and Roles into
  Application Security` ESS job.

Do not use CSV export/import or `core.data-loader` for this task. The effective catalog marks CSV export/import as unsupported; the configured execution route is the shared ESS workflow.

## Shared Skill Invocation Inputs

Pass the following task-specific request fields to
`common.security-console.user-security-common` for every invocation. The
shared workflow combines these fields with its configured job-definition and
application contract, then owns submission approval and monitoring.

```json
{
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
```

Resolve the schedule placeholders immediately before the shared workflow
displays the exact submission for approval. Do not pass a task-level
`jobDefinitionId` or `application`; the shared skill owns those configured
defaults.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `ess_delegation_contract`

## Outputs

- `setup_task_plan`
- `ess_job_submission_plan`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.field-service.users-and-security` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
