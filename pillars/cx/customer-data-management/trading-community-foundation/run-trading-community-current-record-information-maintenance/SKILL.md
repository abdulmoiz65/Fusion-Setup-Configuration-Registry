---
skill_id: "cx.customer-data-management.trading-community-foundation.run-trading-community-current-record-information-maintenance"
name: "Run Trading Community Current Record Information Maintenance"
description: "Builds, previews, submits, and tracks the Maintain Party and Location Current Record Information Oracle Fusion ESS process without querying or gating on unrelated Scheduler jobs. Use it for the Run Trading Community Current Record Information Maintenance FSM task, including party/location maintenance and worker synchronization by person type, inclusive date range, or person numbers."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_RUN_TRADING_COMM_CURRENT_RECORD_INFO_MAINTENANCE"
task_name: "Run Trading Community Current Record Information Maintenance"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "verification"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.1.1"
inputs:
  - "job_parameters_text"
  - "fusion_environment_context"
  - "project_id"
  - "execution_intent"
  - "execution_approval"
  - "execution_options"
  - "request_id"
outputs:
  - "normalized_job_parameters"
  - "effective_selection"
  - "ignored_parameters"
  - "ess_request_payload"
  - "execution_preview"
  - "ess_submission_checkpoint"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
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
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-current-record-information-maintenance/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-current-record-information-maintenance/current/"
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
  - "Connects to the configured Oracle Fusion ESS Scheduler REST API after exact-target checks and explicit execution approval."
  - "Submits Maintain Party and Location Current Record Information, which updates current party/location profiles or synchronizes HCM workers to person parties according to the approved scope."
  - "May refresh the local gitignored OAuth token cache through the invoked ESS core skill."
required_privileges:
  - "Run Trading Community Current Record Information Maintenance privilege"
  - "Application Implementation Consultant or Master Data Management Application Administrator role, or equivalent access"
---

# Run Trading Community Current Record Information Maintenance

## Purpose

Accept the parameters for `Run Trading Community Current Record Information
Maintenance` in plain business language, normalize them into the fixed
five-position ESS contract, validate and preview the effective scope, and use
the existing ESS core service to submit or resume the process after all gates
pass.

Oracle displays the scheduled process as `Maintain Party and Location Current
Record Information`. It updates the current effective profile for people,
organizations, and locations, or synchronizes HCM workers to person parties.

## Setup Task and ESS Contract

- Task code: `HZ_RUN_TRADING_COMM_CURRENT_RECORD_INFO_MAINTENANCE`
- Application: `CrmEss`
- Job definition: `JobDefinition://oracle/apps/ess/cdm/foundation/parties/CurrentDateRecordSync`
- Submit endpoint: `POST /ess/rest/scheduler/v1/requests`
- Track endpoint: `GET /ess/rest/scheduler/v1/requests/{requestId}`
- Parameter count: exactly five positional `STRING` parameters
- Client safety: `retries: 0`, one POST per approval, checkpoint before polling
- CSV export/import: not supported by the effective setup-task catalog
- Submission isolation: validate and submit only the request described by the
  current preview. Do not list, inspect, poll, or gate submission on unrelated
  Scheduler requests.

Use the fixed application, job definition, argument order, and transport codes.
Do not derive them from display labels or the FSM task code.

| Position | Canonical field | Fixed transport contract |
|---:|---|---|
| `submit.argument1` | `synchronization_type` | `ORA_PARTY_DENORM` for Party and location; `ORA_PERSON_SYNC` for Worker |
| `submit.argument2` | `person_type` | `EMP`, `CWK`, `PWK`, `EX_EMP`, `EX_CWK`, `EX_PWK`, `NONW`, `EX_NONW`, `PURGED`, or blank |
| `submit.argument3` | `from_date` | Valid `YYYY-MM-DD` date or blank |
| `submit.argument4` | `to_date` | Valid `YYYY-MM-DD` date or blank |
| `submit.argument5` | `person_numbers` | One or more comma-separated person numbers, or blank |

Preserve all five positions. For an unset value, include the parameter object
without a `value` property. Do not send JSON null, an empty string, or `#NULL`.

## Inputs

- `job_parameters_text`: plain-language process settings.
- `fusion_environment_context`: exact target Fusion environment; resolve it only
  when exactly one configured environment is active.
- `project_id`: required for live submission so the approval preview, payload,
  and request checkpoint survive interruption.
- `execution_intent`: `preview` or `execute`. Retain an initial run instruction
  while collecting missing parameters, but do not treat it as final approval.
- `execution_approval`: explicit confirmation given after the consolidated
  preview. Bind it to the target environment, operation, payload fingerprint,
  and correlation description.
- `execution_options`: optional bounded `wait_seconds` and `poll_interval`.
- `request_id`: optional positive ESS request ID used only to resume tracking.

## Plain-Text Normalization

Normalize the user's text into this canonical model before invoking the
builder:

| Canonical field | Requirement | Accepted canonical values |
|---|---|---|
| `synchronization_type` | Required | `ORA_PARTY_DENORM`, `ORA_PERSON_SYNC` |
| `person_type` | Optional; Worker only | One fixed person-type code |
| `from_date` | Optional pair; Worker only | ISO `YYYY-MM-DD` |
| `to_date` | Optional pair; Worker only | ISO `YYYY-MM-DD` |
| `person_numbers` | Optional; Worker only | Comma- or whitespace-separated values |

Use these conventional English mappings:

| Conventional label | Fixed code |
|---|---|
| Employee | `EMP` |
| Contingent Worker | `CWK` |
| Pending Worker | `PWK` |
| Ex-Employee | `EX_EMP` |
| Ex-Contingent Worker | `EX_CWK` |
| Ex-Pending Worker | `EX_PWK` |
| Nonworker | `NONW` |
| Ex-Nonworker | `EX_NONW` |
| Purged Worker | `PURGED` |

The first eight visible person-type labels come from the environment's
`PER_PERSON_TYPES_TL.USER_PERSON_TYPE` and can vary by customer and language.
Treat the codes as fixed. Use the conventional mappings only when the English
label is unambiguous; for an unfamiliar localized or configured label, request
the fixed code rather than guessing. `PURGED` and its Purged Worker label are
defined directly by the process view object.

Normalize spaces and commas between person numbers to one comma. Preserve the
token text and order, including leading zeroes. Do not deduplicate or expand
ranges.

### Parameter Intake

On a bare invocation, ask once:

```text
Please provide the maintenance settings.

- Synchronization: Party and location, or Worker
- For Worker only, optionally provide one of these scopes:
  - Person type
  - From and To dates in YYYY-MM-DD format
  - One or more person numbers
```

Apply these rules:

1. Require an explicit synchronization type for predictable automation. Although
   Fusion technically accepts a blank value and runs both branches, do not use
   that implicit combined scope in an automated request.
2. Do not ask for Worker filters when Party and location is selected.
3. Do not ask a second round of optional questions after the required
   synchronization type is known. Unspecified Worker filters remain blank.
4. Preserve an initial execution intent while collecting missing values, but
   require approval after showing the resolved preview.
5. Stop and clarify ambiguous dates, localized person-type labels without a
   fixed code, or an unresolved target environment.

## Deterministic Payload Builder

Write the canonical object to a temporary or project-local JSON file and run
from the repository root:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-current-record-information-maintenance/scripts/build_current_record_request.py \
  --input <canonical-parameters.json> \
  --description "FDOS:current-record-maintenance:<project_id>:<run_id>" \
  --payload-output <ess-request.json> \
  --report-output <request-preview.json>
```

The builder writes the executable Scheduler payload separately from the full
preview. It fails closed when an output exists. Use a new run path, or use
`--force` only after explicit overwrite approval. Never let an output replace
the canonical input or let the payload and report share a path.

## Validation and Effective-Scope Rules

1. Require `synchronization_type` and accept only the two fixed codes.
2. For `ORA_PARTY_DENORM`, require arguments 2 through 5 to remain blank.
3. For `ORA_PERSON_SYNC`, allow person type, date range, and person numbers to
   remain blank; that means all applicable worker types without those filters.
4. Require From Date and To Date together or leave both blank.
5. Require valid ISO dates and `from_date <= to_date`.
6. Treat To Date as inclusive. Send the entered value unchanged; disclose that
   the package internally adds one day.
7. Validate person type against the nine fixed codes.
8. When person numbers are supplied, treat them as the effective selection.
   Person type and date values may remain in their positional arguments, but
   report them in `ignored_parameters` and disclose that the package gives
   person numbers precedence.
9. Reject unknown canonical fields, empty person-number lists, ambiguous
   synchronization values, and unsupported argument combinations before any
   side effect.

## Preview and Approval

Always persist and show one consolidated business preview before submission:

```markdown
Maintain Party and Location Current Record Information

- Environment: <environment name and host>
- Synchronization: <Party and location or Worker> (<fixed code>)
- Person type: <conventional label and code, or Not specified>
- Date range: <from> through <to> inclusive, or Not specified
- Person numbers: <normalized values, or Not specified>
- Effective selection: <party/location, worker filters, all applicable workers, or listed person numbers>
- Ignored because person numbers take precedence: <fields, or None>
- Status tracking: <bounded wait and poll interval>

Submit this exact ESS request to the environment above? Reply Yes to approve this one submission, or tell me what to change.
```

Do not expose application names, job-definition paths, positional argument
names, core skill IDs, or checkpoint paths in the normal business preview.
Persist them in the technical preview and show them on request or for diagnosis.

Require explicit approval after presenting the exact target, operation, and
payload-derived scope. An earlier `run`, `submit`, or `proceed` instruction is
execution intent, not approval for the final payload. Invalidate approval when
the environment, any parameter, the payload fingerprint, or the correlation
description changes.

## Preflight Gates

Before live submission:

1. Require the exact environment identity, required role or privilege, project
   path, canonical input, payload, approval binding, and writeable artifact
   paths.
2. Do not query the Scheduler collection or inspect any existing request before
   submission. Existing, queued, running, or completed requests are outside this
   skill run and must not block the approved request.
3. When active current/past Employee or Contingent Worker synchronization is
   explicitly intended, surface the Full Mode prerequisite: both
   `ORA_HZ_ENABLE_MPLCRI_ACTIVE_WORKER` and
   `HRC_DISABLE_HCM_EVENTS_PROCESSING` must be enabled. Do not modify these
   profile options in this skill. Warn that enabling
   `HRC_DISABLE_HCM_EVENTS_PROCESSING` disables HCM events and should be limited
   to a tightly controlled interval.
4. Never substitute browser automation, direct REST, a loader, or an import
   route for the declared ESS workflow.

## Live Execution

Use the two-phase pattern:

1. Treat the approved payload as the only request in scope. Do not list or
   inspect other Scheduler jobs before the POST.
2. Persist normalized parameters, effective selection, ignored parameters,
   exact payload, payload fingerprint, correlation description, environment,
   approval evidence, and UTC submission window under the declared artifact
   folder.
3. Invoke `core.fusion-api.ess-job-submitter` with the generated
   `--payload-file`, `--submit-only`, `--retries 0`, and `--output` pointing to
   `ess-submission-checkpoint.json`.
4. Require one positive `execution_result.requestId`. Persist and report it
   before polling.
5. Invoke the core skill separately with `--request-id <requestId>`, bounded
   `--wait-seconds`, `--poll-interval`, and `--output` pointing to
   `ess-execution-result.json`.
6. Poll only the request ID returned by this submission. Never query or track a
   different request as part of the current run.
7. Never combine submission and long polling in one process. Never
   automatically repeat the submission POST.
8. On timeout, retain the same request ID and resume tracking only when asked.
9. When `request_id` is supplied, reconcile it to this exact application and
   job definition, then track only. Do not rebuild or resubmit the request.

## Uncertain Submission Recovery

If submission may have reached Fusion but the checkpoint is missing or
unreadable, do not submit again. Use `core.fusion-api.rest-api-client` for a
workflow-selected read-only Scheduler query using:

- exact correlation description
- application `CrmEss`
- exact `CurrentDateRecordSync` job definition
- UTC submission window
- complete five-position parameter contract

Accept recovery only when exactly one request matches. Persist its request ID
before polling. Treat zero or multiple matches as `approval_blocker`; do not
issue a replacement POST.

## Errors and Diagnostics

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

On timeout or failure, persist and report the environment, stage, task code,
application, job definition, request ID and ECID when available, last ESS
state, elapsed time, safe Fusion message, artifact references, and recommended
resume or correction action. Retrieve and persist the process log or status
payload when available.

Refresh a cache-managed token after 401 or 403 at most once. Never retry a live
POST without reconciliation and new explicit approval. Never print or persist
credentials, tokens, token-cache contents, authorization headers, private keys,
or sensitive worker data.

## References

- Oracle scheduled-process behavior and parameters:
  `https://docs.oracle.com/en/cloud/saas/sales/fasqa/maintain-party-and-location-current-record-information.html`
- Oracle Scheduler REST submission contract:
  `https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html`
