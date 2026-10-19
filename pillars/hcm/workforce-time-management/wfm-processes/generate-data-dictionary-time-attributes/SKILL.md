---
skill_id: "hcm.workforce-time-management.wfm-processes.generate-data-dictionary-time-attributes"
name: "Generate Data Dictionary Time Attributes Setup Task Guidance"
description: "Provides task-specific setup guidance for Generate Data Dictionary Time Attributes under the WFM Processes functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "WFM Processes"
functional_area_code: "ORA_WFM_PROCESSES"
task_code: "ORA_HWM_GENERATE_DATA_DICTIONARY_TIME_ATTRIBUTES"
task_name: "Generate Data Dictionary Time Attributes"
parent_skill_id: "hcm.workforce-time-management.wfm-processes"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/wfm-processes/generate-data-dictionary-time-attributes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/wfm-processes/generate-data-dictionary-time-attributes/current/"
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

# Generate Data Dictionary Time Attributes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Generate Data Dictionary Time Attributes` under `WFM Processes`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_GENERATE_DATA_DICTIONARY_TIME_ATTRIBUTES`
- task_name: `Generate Data Dictionary Time Attributes`
- parent_skill_id: `hcm.workforce-time-management.wfm-processes`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `WFM Processes`
- functional_area_code: `ORA_TIME_AND_LABOR_WFM_PROCESSES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Generate Data Dictionary Time Attributes` under `WFM Processes`.

## Setup Task Metadata

- Task name: `Generate Data Dictionary Time Attributes`
- Task code: `ORA_HWM_GENERATE_DATA_DICTIONARY_TIME_ATTRIBUTES`
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

Use this task metadata when invoking those skills:

- Offering: `Time and Labor`
- Functional area / Setup Object: `WFM Processes`
- Setup task name: `Generate Data Dictionary Time Attributes`
- Setup task code: `ORA_HWM_GENERATE_DATA_DICTIONARY_TIME_ATTRIBUTES`

## ESS execution: Generate Data Dictionary Time Attributes

ESS execution is an additional task capability. It does not replace the
catalog-backed FSM export/import route above.

Use `core.fusion-api.ess-job-submitter` for all Scheduler submission and
tracking. Do not create a task-specific ESS client, Scheduler REST client,
OAuth flow, or polling implementation.

### Verified Scheduler contract

- Job definition: `JobDefinition://oracle/apps/ess/hcm/wfm/repositoryDataDictionary/TimeAttributeFieldGenerationJob`
- Application: `EarHcmEss`
- Product: `HCM`
- Job package: `/oracle/apps/ess/hcm/wfm/repositoryDataDictionary`
- Job name: `TimeAttributeFieldGenerationJob`
- Job-definition application metadata: `HWM`
- Parameter VO: `oracle.apps.hcm.wfm.repositoryDataDictionary.publicEssModel.view.TimeAttributeFieldGenerationParametersVO`
- Schedule: immediate only. Do not set recurrence, delayed start, `schedule`,
  `scheduleId`, `startTime`, or `endTime`.

### Task-owned parameter contract

| Scheduler parameter | Task input | Rule |
|---|---|---|
| `submit.argument1` | Include Payroll Time Type | Required. Accept only `Y` or `N`; default an omitted value to `Y`. |
| `submit.argument4` | Legislative Data Group | The LDG scope decision is required: explicitly choose all LDGs or one specific LDG. For all LDGs, omit this argument. For a specific LDG, resolve the selected LOV value through the current target environment's `GET {HCM_BASE}/legislativeDataGroupsLOV` response and send the resolved ID. Do not hard-code an ID. |

Do not send `submit.argument2` or `submit.argument3`: no supported task input
maps to them. Do not manufacture blank parameters or any additional arguments.

### Approval, submission, and monitoring

1. Validate Include Payroll Time Type, then require an explicit Legislative
   Data Group scope decision before building a payload: all LDGs, or one
   specific LDG. Omit `submit.argument4` only after the user chooses all LDGs;
   otherwise resolve the selected Legislative Data Group ID.
2. Preview the target environment, job definition, application, product,
   immediate schedule behavior, and a redacted resolved payload. If a
   specific LDG was selected, show its resolved display value and ID.
3. Require explicit approval immediately before the first live submission.
   Revalidate the payload if an editable value or target environment changes.
4. Invoke `core.fusion-api.ess-job-submitter` once with the approved payload.
   Preserve its returned `execution_result.requestId` with the job definition,
   target environment, purpose, and status in the task audit record.
5. Monitor that same request ID through the shared core capability. On a
   timeout or later status request, resume tracking by request ID; never
   automatically resubmit after timeout, failure, or an uncertain response.
6. Return the terminal ESS status and redacted diagnostics. A terminal
   successful Scheduler status is the task's execution-completion check; do
   not claim an additional business-data verification that is not evidenced.

### ESS acceptance criteria

Task-local pure-payload tests are in
`tests/test_time_attribute_ess_payload.py`. Run them with:

```text
python -m unittest pillars/hcm/workforce-time-management/wfm-processes/generate-data-dictionary-time-attributes/tests/test_time_attribute_ess_payload.py
```

The tests cover task-owned payload construction. Verify the following during
implementation review; do not add product-specific submitter or polling code:

- An omitted Include Payroll Time Type defaults to `Y`; supplied values other
  than `Y` and `N` block payload preview.
- Payload construction blocks until the user explicitly chooses all LDGs or a
  specific LDG. The all-LDG choice omits `submit.argument4`; a specific choice
  requires a resolved ID.
- A selected Legislative Data Group resolves through
  `GET {HCM_BASE}/legislativeDataGroupsLOV`; zero or multiple matches block
  submission, and the resolved ID is used instead of a hard-coded value.
- The preview presents the exact target environment and redacted resolved
  request immediately before explicit approval.
- The shared ESS submitter returns and preserves one request ID for a
  successful submission.
- Terminal polling and subsequent status checks use that same request ID.
- Failure, timeout, and uncertain-response handling show redacted diagnostics
  and do not resubmit automatically.




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

Use the parent functional-area skill `hcm.workforce-time-management.wfm-processes` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
