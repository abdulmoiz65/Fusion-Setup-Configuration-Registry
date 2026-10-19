---
skill_id: "hcm.hcm-communicate.employee-communications.manage-sms-configuration"
name: "Manage SMS Configuration Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage SMS Configuration under the Employee Communications functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Communicate"
functional_area: "Employee Communications"
functional_area_code: "ORA_IRC_EMPLOYEE_CAMPAIGNS"
task_code: "ORA_IRC_EMP_CAMP_SMS_CONFIG"
task_name: "Manage SMS Configuration"
parent_skill_id: "hcm.hcm-communicate.employee-communications"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm communicate pillar team"
version: "0.3.0"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-sms-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-communicate/employee-communications/manage-sms-configuration/current/"
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

# Manage SMS Configuration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage SMS Configuration` under `Employee Communications`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_EMP_CAMP_SMS_CONFIG`
- task_name: `Manage SMS Configuration`
- parent_skill_id: `hcm.hcm-communicate.employee-communications`
- pillar: `HCM`
- offering: `HCM Communicate`
- functional_area: `Employee Communications`
- functional_area_code: `ORA_IRC_EMPLOYEE_CAMPAIGNS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage SMS Configuration` under `Employee Communications`.

## Capabilities

- Review the current SMS configuration.
- Set up Twilio or Syniverse as the SMS provider.
- Configure the account name, message limit, description, and optional footer.
- Explain the remaining activation steps and help confirm that only one SMS
  configuration is active.

Creating an SMS configuration does not automatically activate it. Clearly tell
the user when activation is still required.

## Example Requests

- “Set up Twilio for HCM Communicate.”
- “Create a Syniverse SMS configuration with a message limit of 1600.”
- “Show me the current SMS configuration.”
- “What steps remain before the new SMS configuration is active?”

## Setup Task Metadata

- Task name: `Manage SMS Configuration`
- Task code: `ORA_IRC_EMP_CAMP_SMS_CONFIG`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

## User-Facing Response Style

Use plain business language for Manage SMS Configuration requests. Ask for and
report only the provider name, account name, optional description, message
limit, optional footer, and the next business action.

When asking for a provider, present only these options: **Twilio** or
**Syniverse**. Do not show provider codes, identifiers, defaults, or account
types.

Do not include provider identifiers, account-type codes, task codes, CSV
column names, FSM terminology, archive details, API paths, credentials, or
secrets in normal user-facing messages. Keep those details internal for
validation and execution. If the core Data Loader workflow requires an
immutable approval preview or result report, return that required report
unchanged; otherwise provide a concise business summary.

After a successful creation, always state whether a manual follow-up remains.
When activation was requested, provide these business steps:

1. Open **Manage SMS Configuration**.
2. Deactivate the currently active SMS configuration, if there is one.
3. Activate the newly created configuration.
4. Confirm that exactly one SMS configuration is active.

When activation was not requested, state that no manual action is needed to
complete the creation, and offer the activation steps only on request.

Use this task metadata when invoking those skills:

- Offering: `HCM Communicate`
- Functional area / Setup Object: `Employee Communications`
- Setup task name: `Manage SMS Configuration`
- Setup task code: `ORA_IRC_EMP_CAMP_SMS_CONFIG`




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

Use the parent functional-area skill `hcm.hcm-communicate.employee-communications` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
