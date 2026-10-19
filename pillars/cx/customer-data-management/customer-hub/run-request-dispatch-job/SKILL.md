---
skill_id: "cx.customer-data-management.customer-hub.run-request-dispatch-job"
name: "Run Request Dispatch Job"
description: "Plans, previews, submits, schedules Oracle-supported recurring runs, or tracks the source-verified Customer Hub Request Dispatch ESS job with guarded approval and retry controls."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
task_code: "ZCH_RUN_REQUEST_DISPATCH_JOB"
task_name: "Run Request Dispatch Job"
parent_skill_id: "cx.customer-data-management.customer-hub"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.3.0"
inputs:
  - "execution_intent"
  - "fusion_environment_context"
  - "schedule_intent"
  - "refresh_metadata_policy"
  - "dispatch_job_timeout"
  - "requestId"
  - "execution_options"
  - "project_id"
outputs:
  - "execution_preview"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.ess-job-submitter"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/run-request-dispatch-job/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/run-request-dispatch-job/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/run-request-dispatch-job/current/"
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
  - "After the technical job identity is validated, an immutable preview is approved, and the exact target is confirmed, may submit the Request Dispatch ESS process once through core.fusion-api.ess-job-submitter."
  - "A recurring submission may continue processing future eligible duplicate-resolution requests according to its approved schedule until changed or cancelled outside this skill."
  - "May refresh the local gitignored OAuth token cache through core.fusion-api.ess-job-submitter."
required_privileges:
  - "ZCH_RUN_TRADING_COMMUNITY_REQUEST_DISPATCH_JOB_PRIV"
---

# Run Request Dispatch Job

## Purpose

Safely plan, preview, submit, schedule, or track the Customer Hub Request Dispatch scheduled process. Oracle identifies the Scheduled Processes display name as `Schedule Duplicate Resolution Requests`.

This is an ESS execution task, not setup-data export/import. Do not invoke `core.data-loader` or task-level CSV export.

## Setup Task Skill Contract

- task_code: `ZCH_RUN_REQUEST_DISPATCH_JOB`
- task_name: `Run Request Dispatch Job`
- parent_skill_id: `cx.customer-data-management.customer-hub`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Customer Hub`
- functional_area_code: `ZCH_CUST_HUB_OPT`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use for advisory guidance, an immutable execution preview, a new on-demand submission, recurring-schedule planning, or status tracking for an existing positive `requestId`.

## Confirmed Oracle Behavior

- On-demand mode submits the process for immediate execution.
- Advanced mode supports immediate or recurring execution using a selected frequency and start date.
- Product documentation describes eligible requests as Pending or Submitted. The reviewed source revision selects `PENDING` and `PROCESSING`; disclose this version-specific difference instead of claiming one status set universally.
- The documentation and reviewed job contract do not expose a request-specific filter.
- Record the returned Process ID and use that same ID to review status in Scheduled Processes.
- On-demand and recurring scheduling use the same parent job definition.
- `RequestDispatchJob` is the dispatcher. Do not directly submit the related child `RequestProcessJob` (`Process Duplicate Resolution Requests`).

## Technical Contract Readiness

| Field | Status | Rule |
|---|---|---|
| Setup task code | Confirmed: ZCH_RUN_REQUEST_DISPATCH_JOB | Fixed by the effective setup-task catalog. |
| Scheduled-process display name | Confirmed: Schedule Duplicate Resolution Requests | Use for UI identification and status review only. |
| jobDefinitionId | Confirmed: JobDefinition://oracle/apps/ess/cdm/hubBase/reqDispatcher/RequestDispatchJob | Scheduler REST URI derived from the reviewed `RequestDispatchJob.xml` identity and validated against the repository ESS URI convention. |
| job package | Confirmed: oracle.apps.ess.cdm.hubBase.reqDispatcher | Fixed by reviewed job metadata. |
| application | Confirmed: CrmEss | Fixed by `SYS_effectiveApplication` in reviewed job metadata. |
| product | Confirmed: ZCH | Fixed by `SYS_product` in reviewed job metadata. |
| implementation | Confirmed: oracle.apps.cdm.hubBase.reqDispatcher.dispatch.RequestDispatcher | ESS JavaJobType implementation; informational, not a REST request parameter. |
| requestParameters | Confirmed: two ordered STRING parameters | Use `submit.argument1` for Refresh Metadata and `submit.argument2` for Dispatch Job Timeout. |
| required privilege | Documented: ZCH_RUN_TRADING_COMMUNITY_REQUEST_DISPATCH_JOB_PRIV | Assume the current user has access. Do not request privilege confirmation or role evidence before preview or submission. |

The reviewed job metadata also declares internal execution fields such as `jobDefinitionApplication=ZCH`, `SYS_className`, `jobPackageName`, and `SYS_retries`. They are not additional business submission parameters and must not be copied into `requestParameters`. Do not confuse internal `jobDefinitionApplication=ZCH` with the Scheduler REST `application=CrmEss` field.

Reviewed security metadata grants the privilege to the Customer Data Management Administration and Data Steward Manager roles. This is informational only: assume the current user has the required access and do not ask them to confirm the privilege or role. If Fusion actually rejects the operation, report the returned authorization error.

## Parameter Contract

| Position | UI Field | Accepted User Value | Scheduler Value | Default |
|---|---|---|---|---|
| 1 | Refresh Metadata | Refresh metadata on every schedule | ALWAYS | No |
| 1 | Refresh Metadata | Refresh metadata when needed | IF_NEEDED | Yes, when omitted |
| 1 | Refresh Metadata | Never refresh metadata | NEVER | No |
| 1 | Refresh Metadata | Explicit blank or null | Empty string placeholder | No; only when explicitly requested |
| 2 | Dispatch Job Timeout | Custom whole-number text | Exact supplied value | 120 when omitted |

Always preserve the two positional names and order. Map UI labels or case-insensitive internal codes to the uppercase internal value for `submit.argument1`. If the caller omits Refresh Metadata, default it to `IF_NEEDED`; if the caller explicitly requests blank/null, send an empty STRING value so the earlier positional placeholder remains present. Reject any other nonblank value.

For `submit.argument2`, default to the STRING value `120`. A caller may override it with exact whole-number text, such as the screenshot-confirmed `290`. The supplied evidence does not establish a supported minimum or maximum, so do not invent a range; reject nonnumeric text and disclose that Fusion performs final range validation.

## On-Demand REST Contract Shape

```json
{
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/cdm/hubBase/reqDispatcher/RequestDispatchJob",
  "application": "CrmEss",
  "product": "ZCH",
  "requestParameters": [
    {
      "name": "submit.argument1",
      "paramType": "STRING",
      "value": "IF_NEEDED"
    },
    {
      "name": "submit.argument2",
      "paramType": "STRING",
      "value": "120"
    }
  ]
}
```

This example shows both defaults. Replace only the two parameter values according to the validated rules above. Use this contract only for the parent dispatcher. Scheduling fields, if requested and supported by the core executor, are additional previewed request fields; they do not change the fixed job identity or positional parameter names.

## General Recurring REST Contract

Recurring execution uses the Oracle Scheduler `schedule` object supported by
`core.fusion-api.ess-job-submitter`. Accept every Scheduler-supported RFC 5445
frequency: `SECONDLY`, `MINUTELY`, `HOURLY`, `DAILY`, `WEEKLY`, `MONTHLY`, and
`YEARLY`. A schedule may contain one or more recurrence objects; Oracle treats
their generated occurrences as a union. It may also contain optional ISO 8601
`inclusions` and `exclusions`.

Require all of the following before building a recurring preview:

- one IANA/Olson time zone in `schedule.timezone`;
- one or more items in `schedule.recurrences`;
- an Oracle-supported RFC 5445 RRULE in every recurrence's `icalString`;
- explicit offset-bearing ISO 8601 `startDate` and `endDate` values for every
  recurrence, to seconds and without fractional seconds;
- an `endDate` later than `startDate` for every recurrence;
- offset-bearing ISO 8601 values, to seconds and without fractional seconds,
  for every optional inclusion or exclusion.

Validate each RRULE semantically and preserve the approved `icalString`
byte-for-byte in the submission payload. Reject `UNTIL`, `COUNT`, `BYSETPOS`,
and `WKST`; numeric positions below `-1`; an expression containing both
`BYMONTH` and `BYWEEKNO`; or an expression containing all three of `BYDAY`,
`BYMONTHDAY`, and `BYYEARDAY`. Other RFC 5445 recurrence parts are allowed when
they satisfy Oracle Scheduler's documented restrictions. Do not invent a
frequency-specific template or silently normalize the user's rule.

Do not combine `schedule` with `scheduleId`, top-level `startTime`, or top-level
`endTime`. Do not default the recurrences, start, end, time zone, inclusions, or
exclusions. The user must provide or explicitly accept every schedule value
because the recurring parent can create future ESS occurrences until the last
approved end date. Set top-level `executePast` to `false` so delayed submission
does not generate occurrences whose scheduled times are already in the past.

This synthetic example demonstrates a union of a daily rule and a weekly rule,
plus an explicit inclusion and exclusion:

```json
{
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/cdm/hubBase/reqDispatcher/RequestDispatchJob",
  "application": "CrmEss",
  "product": "ZCH",
  "requestParameters": [
    {
      "name": "submit.argument1",
      "paramType": "STRING",
      "value": "IF_NEEDED"
    },
    {
      "name": "submit.argument2",
      "paramType": "STRING",
      "value": "120"
    }
  ],
  "schedule": {
    "timezone": "Asia/Kolkata",
    "recurrences": [
      {
        "icalString": "FREQ=DAILY;INTERVAL=1;BYHOUR=9;BYMINUTE=0;BYSECOND=0;",
        "startDate": "2026-10-01T09:00:00+05:30",
        "endDate": "2026-11-01T09:00:00+05:30"
      },
      {
        "icalString": "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,WE,FR;BYHOUR=14;BYMINUTE=0;BYSECOND=0;",
        "startDate": "2026-10-01T14:00:00+05:30",
        "endDate": "2026-11-01T14:00:00+05:30"
      }
    ],
    "inclusions": [
      "2026-10-10T11:00:00+05:30"
    ],
    "exclusions": [
      "2026-10-12T09:00:00+05:30"
    ]
  },
  "executePast": false,
  "retries": 0
}
```

The example values are not defaults and must never be submitted unchanged
unless they exactly match the user's requested schedule. A recurring preview
must show every recurrence, inclusion, and exclusion in local time and UTC so
the user can verify union, exception, daylight-saving, and offset effects before
approval.

## Preflight Checks

Before a new submission, require exactly one target environment, a validated Refresh Metadata selection, a validated Dispatch Job Timeout, an explicit schedule choice, a writable project-artifact destination when persistence is requested, and standalone approval bound to the exact immutable preview. For recurrence, also require an IANA/Olson time zone, one or more valid bounded recurrence objects, valid optional inclusions and exclusions, `executePast=false`, and no `scheduleId` or top-level start/end fields. Assume the user has `ZCH_RUN_TRADING_COMMUNITY_REQUEST_DISPATCH_JOB_PRIV`; privilege evidence is not a preflight input or approval blocker. Stop before side effects when any other required value is missing, ambiguous, or changed.

Never print or persist access tokens, refresh tokens, client secrets, authorization headers, token-cache contents, or sensitive request data. Redact protected values from previews, diagnostics, and project artifacts.

## Execution Workflow

1. Classify the request as advisory, preview-only, new on-demand submission, recurring schedule, or tracking an existing `requestId`.
2. For tracking, use `core.fusion-api.ess-job-submitter --request-id <requestId>` with bounded polling. Never turn a status request into a new submission.
3. For a new submission, resolve exactly one target environment, apply the fixed parent-job identity, map/default `submit.argument1` and `submit.argument2`, assume required access, and resolve either on-demand execution or the complete bounded recurring schedule.
4. Disclose that the process can act on all eligible duplicate-resolution requests without a request-specific filter. State that public documentation says Pending or Submitted while the reviewed source revision selects `PENDING` and `PROCESSING`.
5. Present an immutable preview containing environment, job identity, schedule, Refresh Metadata label and internal code, Dispatch Job Timeout, the exact ordered request-parameter array, business impact, `retries=0`, and a preview fingerprint. For recurrence, include every exact RRULE, time zone, local and UTC start/end value, inclusion, exclusion, union behavior, recurring-parent impact, and the exact `schedule` object.
6. Stop and require a later standalone approval for that exact preview. Any change invalidates approval.
7. After approval, submit the exact previewed JSON payload once through `core.fusion-api.ess-job-submitter` using its payload input with `--submit-only --retries 0`; record the returned one-time or recurring-parent `requestId` and stop.
8. Check status only for that existing request ID when explicitly requested. Never automatically resubmit after timeout, transport failure, missing response, or terminal failure.

## Scheduling Boundary

Oracle Scheduler REST accepts an inline `schedule` object with an Olson/IANA
time zone and recurrence objects whose required `icalString` follows RFC 5445.
This skill supports all Scheduler-documented recurrence frequencies, multiple
recurrences, and optional inclusions and exclusions. Require the exact RRULEs,
bounded start and end date/times for every recurrence, time zone, exceptions,
target environment, and explicit approval that clearly states the continuing
future impact. Reject unbounded recurrence objects, `scheduleId`, top-level
`startTime` or `endTime`, fractional-second timestamps, or any RRULE construct
that violates the documented Oracle restrictions above.

Require `executePast=false` for every recurring preview. Oracle Scheduler's
default can generate schedule instances in the past, so omitting or enabling
this field is outside this skill's supported recurrence contract.

The recurring request is still one approved POST. It creates a recurring parent
that may produce future child occurrences until the approved end date. Do not
replace recurring behavior with client-side repeated POST requests or a Codex
automation.

## Setup Task Metadata

- Task name: `Run Request Dispatch Job`
- Task code: `ZCH_RUN_REQUEST_DISPATCH_JOB`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `ESS`
- Business Object: ``

## CSV and Data Loader Boundary

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route this task to `shared.setup-export.task-level-export`, setup-data CSV validation, FSM import, or `core.data-loader`. Its supported execution route is ESS after the technical contract and approval gates are complete.




## Approval and Retry Boundaries

- An initial request to run or schedule the job authorizes validation and preview only.
- Only standalone approval authorizes the exact previewed ESS submission.
- Recurring approval must include every RRULE, start, end, time zone, inclusion, exclusion, target, union behavior, and continuing all-eligible-request impact.
- Never retry an uncertain ESS POST or create a replacement request automatically.
- Authentication may refresh once after a rejected cached token, but that does not authorize replaying an uncertain submission.
- Scheduler `Succeeded` proves process completion, not that every duplicate-resolution request was merged, linked, or otherwise resolved successfully.

## Source Boundaries

- Oracle task documentation: `https://docs.oracle.com/en/cloud/saas/customer-data-management/fagcd/run-the-request-dispatch-job.html`
- Oracle Scheduler submit schema: `https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html`
- Reviewed FusionApps source evidence: `SetupTaskSD.xml`, `submitRequestPageDef.xml`, `RequestDispatchJob.xml`, `CdmHubBaseEssBundle.xlf`, `jazn-data.xml`, `RequestDispatcher.java`, `RequestDispatcherAMImpl.java`, and `RequestProcessJob.xml`.
- User-supplied Scheduled Processes UI and completed Process Details screenshots confirming the Refresh Metadata choices, positional values, default timeout 120, explicit blank/null, and custom timeout 290.
- Scheduler executor: `core.fusion-api.ess-job-submitter`
- Effective catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

Use the parent functional-area skill `cx.customer-data-management.customer-hub` for functional-area sequencing. Read `ora-resource/ora_rule_registry.json` and its source files before validation or execution. Track token usage for generated project artifacts using the manifest policy.
