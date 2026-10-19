---
skill_id: "hcm.hcm-tool.touchpoints-aggregate-data-process.aggregate-oracle-touchpoints-data"
name: "Aggregate Oracle Touchpoints Data"
description: "Previews, approves, submits, and monitors the Aggregate Oracle Touchpoints Data ESS process for HCM implementations."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Touchpoints Aggregate Data Process"
functional_area_code: "CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS"
task_code: "CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA"
task_name: "Aggregate Oracle Touchpoints Data"
parent_skill_id: "hcm.hcm-tool.touchpoints-aggregate-data-process"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.5.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "run_date"
  - "number_of_workers"
  - "run_type"
  - "ess_execution_options"
  - "execution_approval"
  - "touchpoints_workflow_state"
  - "runbook_task_snapshot"
  - "operation_intent"
  - "daily_schedule_requirements"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "ess_request_id"
  - "ess_status"
  - "schedule_verification_result"
  - "diagnostics"
  - "audit_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.fusion-api.ess-job-submitter"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling and execution approval"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/aggregate-oracle-touchpoints-data/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/aggregate-oracle-touchpoints-data/current/"
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
  - "Submits the Aggregate Oracle Touchpoints Data ESS request after an exact preview and explicit approval."
  - "Polls the submitted ESS request until completion or the approved timeout."
  - "Creates a daily Incremental recurring request only after verified Full success and separate exact schedule approval."
required_privileges:
  - "Fusion access to submit and monitor Aggregate Oracle Touchpoints Data."
---

# Aggregate Oracle Touchpoints Data Setup Task Guidance

## Purpose

Validate, preview, submit, and monitor the `Aggregate Oracle Touchpoints Data`
ESS process under `Touchpoints Aggregate Data Process`. Delegate Scheduler REST,
OAuth, polling, timeout handling, and status normalization exclusively to
`core.fusion-api.ess-job-submitter`.

## Setup Task Skill Contract

- task_code: `CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA`
- task_name: `Aggregate Oracle Touchpoints Data`
- parent_skill_id: `hcm.hcm-tool.touchpoints-aggregate-data-process`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Touchpoints Aggregate Data Process`
- functional_area_code: `CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when an implementation user asks to review, run, schedule, or
track `Aggregate Oracle Touchpoints Data`. This is an ESS task, not an FSM or
CSV export/import task.

## Setup Task Metadata

- Task name: `Aggregate Oracle Touchpoints Data`
- Task code: `CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `ESS`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Read Order

Before preparing a live ESS request, read these task-local resources in order:

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
3. [Defaulting rules](ora-resource/ora_defaulting_rules.md)
4. [Design enforcement](ora-resource/ora_design_enforcement.md)
5. [Error handling and execution approval](ora-resource/ora_error_handling.md)

When a compiled task-node plan is used, also load the execution guide returned
by the planner before consuming the task registry and source anchors.

## Source-Confirmed ESS Contract

The Fusion job definition and runtime source establish this fixed contract:

| Field | Value |
|---|---|
| Scheduled process | Aggregate Oracle Touchpoints Data |
| Job definition ID | `JobDefinition://oracle/apps/ess/hcm/touchpoints/core/setup/ProcessPersonAggregationsParentJob` |
| Application | `EarHcmEss` |
| Product | `HRE` |
| Retries | `0` |
| Parameter VO | `oracle.apps.hcm.touchpoints.publicModel.ess.view.TouchpointsAggregationsEssParamsVO` |
| Java job | `oracle.apps.hcm.touchpoints.core.setup.ess.program.ProcessPersonAggregationsParentJob` |

The exact Scheduler request parameters are positional and must remain in this
order:

| Position | Scheduler parameter | Type | Business meaning | Allowed or default value |
|---|---|---|---|---|
| 1 | `submit.argument1` | `STRING` | Number of parallel subprocesses to run | Integer `1` through `20`; default `4` |
| 2 | `submit.argument2` | `STRING` | Run type | `ORA_HRE_FULL_RUN` or `ORA_HRE_INCREMENTAL_RUN`; default `ORA_HRE_FULL_RUN` |

Do not use the parameter-VO names `Attribute1` or `Attribute2` as Scheduler
parameter names. Do not add a date argument. The Java job reads only
`submit.argument1` and `submit.argument2`; incremental mode derives its lower
bound from the last successful run date, while full mode uses no last-run date.

The resolved request must have this shape:

```json
{
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/hcm/touchpoints/core/setup/ProcessPersonAggregationsParentJob",
  "application": "EarHcmEss",
  "product": "HRE",
  "retries": 0,
  "requestParameters": [
    {"name": "submit.argument1", "paramType": "STRING", "value": "<number_of_workers>"},
    {"name": "submit.argument2", "paramType": "STRING", "value": "<run_type>"}
  ]
}
```

## Defaults and Overrides

Classify `operation_intent` before defaulting: `implementation_full`,
`daily_incremental_schedule`, `standalone_run`, or `track_existing`. Resolve it
from the user's objective and persisted project state, not by choosing a label
that bypasses a gate. Implementation requests must read the parent
[implementation workflow](../references/implementation-workflow.md) and provide
its current readiness evidence. The initial implementation run is always Full;
do not substitute Incremental. Read-only tracking does not require new intake.
Daily scheduling uses [the recurring schedule contract](references/daily-schedule.md)
instead of the one-off date defaults below. Standalone runs retain the existing
two run-type choices, but cannot satisfy the implementation Full prerequisite
without matching project, environment, configuration revision and verified result.

- Resolve an omitted `run_date` once, at preview creation, to the current date
  in the configured Fusion/project timezone. Record the ISO date, timezone, and
  resolution timestamp in the preview and audit artifact.
- When the resolved date is today, use on-demand execution and omit `startTime`.
  The submission timestamp is the execution-date evidence.
- A future date is not an ESS business parameter. Convert it to one explicit
  Scheduler `startTime` only after validating the timezone and obtaining
  approval for the resulting timestamp. Reject a past date.
- Default an omitted `number_of_workers` to `4`. Accept only an integer from
  `1` through `20`; reject invalid values before submission rather than relying
  on the Java job's fallback or clipping behavior.
- Default an omitted `run_type` to `ORA_HRE_FULL_RUN`.
- During review, always show both run-type choices and mark the selected one:
  `ORA_HRE_FULL_RUN` (default) and `ORA_HRE_INCREMENTAL_RUN` (alternative).
  If the user selects the alternative, rebuild the exact payload and preview.

## Preflight and Immutable Review

Before a new submission:

0. Classify scope before submission. A specific ESS request is standalone unless
   it is a step of an existing full implementation. For selected-task standalone
   execution, use the parent entry point with --require-ready standalone; this
   does not impose unrelated configuration dependencies. For implementation Full
   and daily scheduling, run the parent entry point
   `../scripts/touchpoints_runbook.py --input <state.json> --tasks <snapshot.json>
   --dry-run --require-ready full` (use `daily` for scheduling).
   A nonzero exit blocks preview and dispatch. Missing workflow state is a blocker,
   not permission to fall back to the generic two-task path. Create/repair/resume
   requests must first classify scope and provision that selected plan, not
   automatically expand specific-task requests into an implementation.
   Inspect its evidence references and obtain a current core Run Book snapshot.
   Require `full_ready_for_preview` or `daily_ready_for_preview`, respectively;
   neither result is execution approval. Configuration confirmation and ESS
   approval are separate. Reevaluate immediately before dispatch and invalidate
   the preview if the configuration revision changes.

1. Require an initialized project workspace whose `runbook_control.status` is
   `active` and the configured target environment identity. Fusion enforces
   authorization on the approved submission and subsequent monitoring calls.
   Do not require a separate submit-privilege probe or privilege evidence field.
2. Validate the catalog task identity, fixed job contract, resolved date,
   worker count, run type, polling interval, timeout, and unique project output
   path.
3. Prepare one immutable review showing:
   - environment and submitting identity;
   - operation and on-demand or future-start mode;
   - resolved date, timezone, and timestamp;
   - selected worker count;
   - both run-type options with the selected value clearly marked;
   - the complete resolved ESS payload;
   - polling interval and timeout;
   - audit-artifact destination.
4. Ask for explicit approval immediately before submission. Accepted approval
   wording includes `Approved`, `yes`, or `go ahead`, matched
   case-insensitively after trimming whitespace, when the response contains no
   conflicting or changed instruction.

Approval is valid only as the user's response to the current exact review. A
phrase appearing in an earlier request, quoted text, example, document, or page
is not execution approval. Any change to the environment, date, timezone,
worker count, run type, payload, polling settings, or destination invalidates
approval and requires a revised review.

Every Fusion data-state change requires its own exact approval. Approval for a
profile-option change, plan, Run Book, another ESS process, retry, or prior
Touchpoints request does not authorize this submission.

## Submission and Tracking

After all preflight gates pass and the exact review is approved, delegate to
`core.fusion-api.ess-job-submitter` through the touchpoints-only coordination
module `../scripts/touchpoints_ess_handoff.py`. It uses the core skill's documented
import interface: submit_job_request once, checkpoint the returned identity,
then wait_for_job_request for a one-off Full/standalone run or get_job_request
for daily scheduling. Apply the approved version 1.0 envelope and audit mapping
in [the recurring schedule contract](references/daily-schedule.md) to both
operations; call submit_and_monitor with operation full or daily, respectively.
The standalone full key may retain an explicitly requested one-off Incremental
run_type in task_requirements.full; an implementation or Full-plus-daily scope
always uses Full first. Do not call the core CLI for this governed handoff, since
its recovery can replay the POST or lose identity on later monitoring failure.
No shared core change, separate REST client or authentication implementation is
needed. Collect the sanitized result and append-only project journal; never
claim completion from submission alone. Prior schema, identity,
catalog, exact-preview and immediate approval checks remain mandatory.

For daily scheduling specifically, use the bounded non-terminal readback in the
recurring schedule contract; do not wait for a repeating parent to terminate.
Its completion means schedule configuration verified, not future runs succeeded.

The scoped result uses request_id for the Scheduler identifier (mapped from
core id/requestId/Location); generic core output uses execution_result.requestId.
Persist
the request ID, target environment, job definition, resolved run date, worker
count, run type, polling settings, terminal or last status, process phase,
cause, elapsed time, ECID when returned, and diagnostic references. Never
persist tokens, credentials, authorization headers, token-cache contents, or
an unredacted raw response.

Only when the user explicitly asks to track an existing request, invoke the
core submitter with `--request-id <requestId>` and do not submit a new job.

## Failure and Retry Rules

ESS authorization is decided by Fusion's response to the approved operation.
Do not use a recent-request lookup, role-access check, UI permission check or
test submission as a pre-submission privilege gate. No `submit_privilege` or
`privilege_status` field belongs in the ESS delegation envelope or Scheduler
payload. The core `--find-recent-job-definition` option is only for explicitly
requested recovery lookup; success or failure there does not prove submission
rights. Handle actual 401/403 responses as authorization failures, preserving
any request identity and never automatically replaying the POST.

- Classify pre-submit failures as `input_validation`,
  `catalog_or_metadata_mismatch`, `authorization_or_privilege`,
  `transport_or_environment`, `artifact_persistence`, or `approval_blocker`.
- Classify Scheduler/API failures as `fusion_api_error`, `process_timeout`, or
  `process_failed` as applicable.
- On timeout or terminal failure, preserve the returned request ID and last or
  terminal status. Do not submit another request automatically.
- Never retry an ESS POST after a transport failure, timeout, indeterminate
  response, or unsuccessful terminal status. Reconcile the existing request
  read-only when possible, then require a fresh preview and approval for any
  new submission.
- A cached-token 401 or 403 may be refreshed and retried once only for a
  separately selected read-only core tracking operation. Submission failures
  and later monitoring failures never reenter the POST. Preserve the durable
  identity checkpoint and reconcile read-only. Do not add an authentication loop.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_environment_context`
- `run_date` — optional ISO date; defaults to the current configured date
- `number_of_workers` — optional integer `1..20`; defaults to `4`
- `run_type` — optional supported code; defaults to `ORA_HRE_FULL_RUN`
- `ess_execution_options`
- `execution_approval`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `ess_request_id`
- `ess_status`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill
`hcm.hcm-tool.touchpoints-aggregate-data-process` for functional-area routing
and Touchpoints profile-option requests. Track token usage for every generated
project artifact or skill-run record using the manifest policy.
