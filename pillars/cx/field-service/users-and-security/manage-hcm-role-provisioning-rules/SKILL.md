---
skill_id: "cx.field-service.users-and-security.manage-hcm-role-provisioning-rules"
name: "Manage HCM Role Provisioning Rules Setup Task Guidance"
description: "Provides CX Field Service task routing for Manage HCM Role Provisioning Rules and delegates export, validation, and approval-gated import to the shared HCM role-provisioning-rules workflow."
layer: "pillar"
pillar: "CX"
offering: "Field Service"
functional_area: "Users and Security"
functional_area_code: "ORA_ASK_USERS_AND_SECURITY"
task_code: "PER_MANAGE_HCM_ROLE_PROVISIONING_RULES"
task_name: "Manage HCM Role Provisioning Rules"
parent_skill_id: "cx.field-service.users-and-security"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX field service pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "source_environment"
  - "target_environment"
  - "requested_operation"
  - "setup_archive"
  - "user_input_file"
  - "execution_approval"
  - "runbook_response_artifact"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "manage_hcm_role_provisioning_rules_result"
  - "skill_run_record"
  - "token_usage_record"
  - "data_loader_run_context"
  - "runbook_status_dashboard"
depends_on:
  - "common.security-console.manage-hcm-role-provisioning-rules"
  - "core.runbook"
uses_core:
  - "core.runbook"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/manage-hcm-role-provisioning-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/manage-hcm-role-provisioning-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/field-service/users-and-security/manage-hcm-role-provisioning-rules/current/data-loader-run-context.properties"
    versioning_policy: "replace-after-confirmation"
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

# Manage HCM Role Provisioning Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage HCM Role Provisioning Rules` under `Users and Security`.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`
- task_name: `Manage HCM Role Provisioning Rules`
- parent_skill_id: `cx.field-service.users-and-security`
- pillar: `CX`
- offering: `Field Service`
- functional_area: `Users and Security`
- functional_area_code: `ORA_ASK_USERS_AND_SECURITY`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage HCM Role Provisioning Rules` under `Users and Security`.

## Setup Task Metadata

- Task name: `Manage HCM Role Provisioning Rules`
- Task code: `PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Shared Workflow Delegation

`CSVExportImportSupportedFlag` is `Y`; all setup-data activity for this task
must be delegated to `common.security-console.manage-hcm-role-provisioning-rules`.
That shared skill owns task-level export, archive and reference validation, and
the immutable approval-gated Data Loader import route. This pillar skill must
not call Fusion, OAuth, FSM, UCM, REST, export, validation, or Data Loader
clients directly.

Invoke the shared skill with the caller's `project_context`,
`source_environment`, `target_environment`, `requested_operation`,
`setup_task_scope` as `hcm_role_provisioning_rule_scope`, `setup_archive`,
`user_input_file`, and `execution_approval`, plus this fixed task identity:

- Setup task name: `Manage HCM Role Provisioning Rules`
- Setup task code: `PER_MANAGE_HCM_ROLE_PROVISIONING_RULES`
- Offering: `Field Service`
- Functional area / Setup Object: `Users and Security`

Propagate the shared skill's export, validation, approval-preview, execution,
and diagnostic outputs without weakening its preflight or approval gates. A
new or modified archive, scope, target environment, or validation result is a
new request and must be revalidated by the shared workflow. This nested skill
does not authorize an import.

## Field Service Run Book to Data Loader Wiring

This task skill owns only the Field Service handoff artifact. It does not
modify `core.data-loader`, `core.runbook`, or the shared security-console
workflow.

When a Run Book was created for this project and its Data Loader import must
update that Run Book task, generate the task-owned run context before invoking
the shared workflow:

```text
python3 scripts/prepare_data_loader_run_context.py \
  --project-root project/{project_id}
```

The script reads only the persisted Run Book creation response at
`state/runbook/current/create-runbook-response.json`, validates its positive
integer `workerJourneyId`, and writes the task-owned context to:

```text
artifacts/pillars/cx/field-service/users-and-security/manage-hcm-role-provisioning-rules/current/data-loader-run-context.properties
```

Pass that exact path to the shared workflow as `data_loader_run_context`. For
its existing Data Loader delegation, the shared workflow must pass it unchanged
as `--run-config <data_loader_run_context>`. This provides Field Service Run
Book details to the shared Data Loader without changing shared routing,
validation, approval, upload, or retry controls. If the Run Book response is
missing, malformed, or changed, stop with an artifact-persistence blocker and
do not fall back to a global Data Loader configuration.

## Run Book Status Presentation

For an explicit status request after this task's Data Loader initiation, do not
return a counts-only summary. Resolve the `workerJourneyId` from this task's
persisted `runbook_response_artifact`, then delegate the read-only status
request to `core.runbook` using its **dashboard** operation with that exact
journey ID. Return the complete `markdown` field unchanged so the user sees:

- the Run Book title;
- the task-count summary; and
- the Field Service - Users and Security task table.

Do not request a dashboard automatically after initiation and do not poll Data
Loader. The initiation result remains the exact shared Data Loader result. A
dashboard is produced only when the caller explicitly asks for Run Book status.

## Failure Handling and Redaction

Propagate failure classifications and recommended next actions from
`common.security-console.manage-hcm-role-provisioning-rules`. Stop on input
validation, catalog mismatch, authorization, transport/environment, Fusion
API, timeout, process-failed, artifact-persistence, or approval-blocker
outcomes; do not retry an export, upload, import, or replacement action from
this pillar skill.

Persist and report only the shared workflow's redacted diagnostics. Never
expose or store credentials, OAuth tokens, authorization codes, private keys,
customer security configuration, full sensitive payloads, or unredacted error
responses in this pillar skill or its project artifacts.




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

Use the parent functional-area skill `cx.field-service.users-and-security` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
