---
skill_id: "erp.financials.general-ledger.review-and-submit-accounting-configuration"
name: "Review and Submit Accounting Configuration Setup Task Guidance"
description: "Resolves an exact primary-ledger accounting configuration from a filtered Specify Ledger Options export and Fusion LOVs, validates mandatory ledger options, builds the AccountingConfigSetup ESS request for configuration-wide or single-secondary scope, and submits or resumes the approved request."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "General Ledger"
functional_area_code: "ORA_FIN_GENERAL_LEDGER"
task_code: "GL_REVIEW_AND_SUBMIT_ACCOUNTING_CONFIGURATION"
task_name: "Review and Submit Accounting Configuration"
parent_skill_id: "erp.financials.general-ledger"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "verification"
execution_mode: "hybrid"
owner_team: "ERP financials pillar team"
version: "0.2.1"
inputs:
  - "primary_ledger_name"
  - "requested_scope"
  - "secondary_ledger_name"
  - "fusion_environment_context"
  - "project_id"
  - "execution_intent"
  - "execution_options"
  - "request_id"
outputs:
  - "scoped_export_receipt"
  - "lov_resolution"
  - "ledger_options_validation"
  - "ess_request_payload"
  - "execution_preview"
  - "ess_submission_checkpoint"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/review-and-submit-accounting-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/review-and-submit-accounting-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/review-and-submit-accounting-configuration/current/"
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
  - "Queries read-only Fusion ledger, accounting-calendar, and chart-of-accounts LOV resources."
  - "Creates filtered Specify Ledger Options export processes after exact-payload approval."
  - "Submits Complete Accounting Configuration through the Fusion ESS Scheduler after a separate exact-payload approval."
  - "May create a second filtered export process, with separate approval, to verify the completed configuration."
  - "May refresh the local gitignored OAuth token cache through invoked core skills."
required_privileges:
  - "Fusion privileges to read ledger, accounting-calendar, and chart-of-accounts LOVs"
  - "Fusion privileges to run and download Setup Task CSV exports"
  - "Fusion privileges to submit and monitor Complete Accounting Configuration"
---

# Review and Submit Accounting Configuration

## Purpose

Use this skill to complete one General Ledger accounting configuration from an
exact primary-ledger scope. It resolves runtime values from a current filtered
`GL_SPECIFY_LEDGER_OPTIONS` export and read-only LOVs, validates that mandatory
ledger options are present, builds the fixed `AccountingConfigSetup` ESS
request, obtains approval bound to the exact payload, and delegates submission
and polling to `core.fusion-api.ess-job-submitter`.

This task does not create or edit a ledger, ledger options, a secondary ledger,
or a relationship. Return any failed readiness check to its owning General
Ledger task.

## Required Inputs

| Input | Required | Contract |
|---|---|---|
| Primary ledger name | Yes | Exact, case-sensitive Fusion ledger name. This is also the accounting-configuration root used by the filtered export. |
| Requested scope | Yes | `primary-only`, `configuration`, `primary-and-related`, or `single-secondary`. |
| Secondary ledger name | Conditional | Required only for `single-secondary`; the parent primary ledger name remains required. |
| Fusion environment | Yes | One exact configured environment; preview and approval are environment-bound. |
| Project ID | Yes for live work | Durable receipts, diagnostics, request ID, status, and token usage are recorded without credentials or token contents. |
| Execution intent | Yes | `preview`, `execute`, or resume by an existing positive `request_id`. |
| Execution options | No | Bounded `wait_seconds` and `poll_interval`; defaults come from the ESS core skill. |

Do not accept only a secondary-ledger name. The ESS job always derives the
accounting configuration from `PRIMARY_LEDGER_ID`, including in
`SECONDARY_LEDGER` mode.

## Scope Semantics

| Requested scope | `FROM_PAGE` | Primary values | Secondary values | Runtime meaning |
|---|---|---|---|---|
| `primary-only` | `REVIEW_SUBMIT` | Populated | Seven empty strings | Allowed only when the filtered configuration contains no `SECONDARY` or `ALC` candidate row. |
| `configuration` | `REVIEW_SUBMIT` | Populated | Seven empty strings | The job processes the primary and independently resolves every eligible related ledger in the configuration. |
| `primary-and-related` | `REVIEW_SUBMIT` | Populated | Seven empty strings | Same payload as `configuration`; require at least one related candidate so the requested meaning is not misleading. |
| `single-secondary` | `SECONDARY_LEDGER` | Populated | Populated from one exact `SECONDARY` row | Completes one exact secondary-ledger branch; never select an `ALC` row. |

`REVIEW_SUBMIT` has no supported “primary plus selected secondaries” array.
Never send one parent request per secondary. Eligible `SECONDARY` and `ALC`
relationships are discovered by the job; balance-only and self-relations are
excluded by product logic. Because the filtered options export does not prove
relationship-level eligibility, `primary-only` fails closed whenever any
related candidate appears.

## Resource Read Order

Load only this `SKILL.md` and the task-local `ora-resource/` package. For a new
request, read the resources in this order:

1. `ora_input_validation.md`
2. `ora_dependency_readiness.md`
3. `ora_reference_lookups.md`
4. `ora_defaulting_rules.md`
5. `ora_design_enforcement.md`
6. `ora_error_handling.md`
7. `ora_rule_registry.json`

The complete export, LOV, ESS envelope, ordered 40-parameter mapping,
submission, polling, and recovery contracts are maintained in those files.
Do not look for task-local `references/`, `scripts/`, or `tests/` directories.

## Workflow

1. Normalize the ledger names by trimming outer whitespace only. Preserve
   case and internal whitespace. Reject blank names and ambiguous scope.
2. Load the repository Ora-Resource Task Node execution guide, compile/plan if
   needed, and require a ready `ora_rule_registry.json` plan. The registry
   validates the request; it does not itself authorize a Fusion mutation.
3. Use `core.fusion-api.rest-api-client` and its standard Fusion REST route to
   query `ledgersLOV` by exact primary name. Require one row with category
   `PRIMARY`; retain `LedgerId` and `ChartOfAccountsId`.
4. Build the exact filtered export request below. Show the target environment,
   operation, and body, then obtain explicit approval immediately before
   invoking `shared.setup-export.task-level-export`. Approval for an earlier
   plan, another export, or the later ESS request is not sufficient.
5. Poll the returned export `ProcessId` within the configured bound and
   download `FileContent`. On failure retrieve `ProcessLog`. On timeout stop
   with `TaskCode`, `ProcessId`, last state, elapsed time, and next-check path;
   do not create another export automatically.
6. Require `ASM_SETUP_CSV_METADATA.xml`,
   `ORA_GL_PRIMARY_LEDGER_CONFIG.csv`, and `GL_PRIMARY_LEDGER.csv`. Require
   metadata task `GL_SPECIFY_LEDGER_OPTIONS`, type `EXPORT`, and a terminal
   completed status. Filter ledger rows by
   `ORA_GL_PRIMARY_LEDGER_CONFIG.Name = <primary ledger name>` rather than using
   unrelated rows that may coexist in the ZIP.
7. Require exactly one scoped `PRIMARY` row whose `Name` is the requested
   primary. For `single-secondary`, require exactly one scoped row whose exact
   name is requested and category is `SECONDARY`. Classify other scoped
   `SECONDARY` and `ALC` rows only as related candidates.
8. Validate mandatory options on the primary and, for `single-secondary`, the
   target secondary. `RetEarnCcidSegments`—the physical export field for the
   Retained Earnings Account—must contain at least one nonblank segment.
   `FirstLedgerPeriodName`, `CurrencyCode`, `PeriodSetName`,
   `AccountedPeriodType`, and `StructureInstanceCode` must be nonblank;
   `EnableAverageBalancesFlag` must be `Y` or `N`. For configuration-wide
   scope, return every child options issue to its owning setup task before
   submission.
9. Query and cross-check the LOVs defined below. Use
   `ledgersLOV.ChartOfAccountsId` as the payload COA ID. It must equal
   `chartOfAccountsLOV.StructureInstanceNumber`; never substitute
   `StructureInstanceId`. Use the one compatible calendar row's `CalendarId`.
10. Assemble the request deterministically in memory from the exact mappings
    and order in `ora_defaulting_rules.md`. Validate the completed envelope and
    every parameter against `ora_input_validation.md`. Do not use an ad hoc
    template, task-local executable, positional guess, or manually edited
    carry-forward payload. Keep any transient payload file untracked and
    persist only governed receipts and fingerprints.
11. Show the final execution preview: environment, job definition, business
    scope, affected candidate ledgers, mandatory-option result, full request
    payload, payload fingerprint, and the warning that successful completion
    makes foundational accounting-configuration choices no longer editable.
12. Obtain explicit approval immediately before the exact ESS POST. Any
    material environment, scope, export, LOV, parameter, or payload change
    invalidates approval and requires a new preview.
13. Submit exactly once with `core.fusion-api.ess-job-submitter` using its
    `--payload-file` route. Persist a submission checkpoint containing the
    payload fingerprint and returned `requestId` before continuing. Never
    automatically replay a failed, timed-out, or indeterminate POST.
14. Poll only `GET /ess/rest/scheduler/v1/requests/{requestId}`. Success requires
    `state = SUCCEEDED` and `processPhase = Complete`. On terminal failure,
    collect the status payload, child request IDs, error type, ECID, and process
    log when available.
15. After success, preview a fresh identical filtered export as post-submit
    verification. Obtain separate approval immediately before creating that
    export process. Verify the same configuration scope and record the final
    state; do not use a successful HTTP response alone as completion evidence.

## Filtered Export Contract

The export criterion is built only after the exact primary ledger LOV resolves
its positive `LedgerId`:

```json
{
  "TaskCode": "GL_SPECIFY_LEDGER_OPTIONS",
  "SetupTaskCSVExportCriteria": [
    {
      "TaskCode": "GL_SPECIFY_LEDGER_OPTIONS",
      "BusinessObjectCode": "GL_PRIMARY_LEDGER",
      "AttributeSet": "Set1",
      "AttributeName": "PRIMARY_LEDGER_ID",
      "AttributeValue": "<PRIMARY_LEDGER_ID>"
    }
  ],
  "SetupTaskCSVExportProcess": [
    {"TaskCode": "GL_SPECIFY_LEDGER_OPTIONS"}
  ]
}
```

Reject any caller-supplied change to the task code, business object, attribute
set, attribute name, or criterion TaskCode. Do not use an SL ID as
`PRIMARY_LEDGER_ID`.

## LOV Contract

All calls are read-only and route through `core.fusion-api.rest-api-client`.
Escape Fusion string literals and URL-encode query values through that client;
do not concatenate an untrusted name into a URL.

| Value | Request | Match and mapping |
|---|---|---|
| Primary or target ledger | `GET /fscmRestApi/resources/11.13.18.05/ledgersLOV` with `q=Name='<exact name>'`, `onlyData=true`, `limit=10` | Exactly one. Cross-check name, category, period set, and period type. Map `LedgerId` and `ChartOfAccountsId`. |
| Calendar | `GET /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV` with `q=PeriodSetName='<exact export value>'`, `onlyData=true`, `limit=10` | Exactly one row whose `PeriodType` equals export `AccountedPeriodType`. Map `CalendarId`. |
| Chart of accounts | `GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV` with `q=StructureInstanceNumber=<ChartOfAccountsId>`, `onlyData=true`, `limit=10` | Exactly one. Cross-check `StructureInstanceCode`. Payload uses `ChartOfAccountsId`/`StructureInstanceNumber`, not `StructureInstanceId`. |

Use the builder once for the primary LOV triple. In `single-secondary`, perform
and provide a second independent ledger/calendar/COA triple for the secondary.
Do not reuse primary values unless both independent matches prove equality.

## Payload Assembly and Existing Client Route

The source of truth for payload construction is the table-first contract in
`ora-resource/ora_defaulting_rules.md`. Build the envelope in memory, append
the 40 parameter objects in exact position order, serialize every parameter
value as a string, and calculate the SHA-256 fingerprint from canonical JSON
with sorted object keys and compact separators. The resource contract defines
the target-ledger rules for positions 38 through 40.

`core.fusion-api.fsm-rest-client` is not a direct arbitrary-endpoint client. Its
own routing contract delegates standard Fusion REST calls to
`core.fusion-api.rest-api-client/scripts/fusion_rest_client.py`. That generic
client accepts `/ess/rest/scheduler/v1/requests`, `--method POST`, and
`--body-file`, so it is technically capable of the submit call after approval.
For this task, use the more specific existing executor because it also performs
the required singular-request tracking:

```bash
python3 core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py \
  --payload-file <transient-approved-request.json> \
  --wait-seconds <bounded-seconds> \
  --poll-interval <bounded-seconds>
```

To resume without resubmitting, invoke the same core script with
`--request-id <existing-request-id>`. The task-local resources document the
exact client boundary, response contract, approval rules, and no-replay policy.

## Resume and Retry

When a positive `request_id` is supplied, do not create another scoped export
or submit another request merely to resume tracking. Confirm the request job
definition and scope from the stored checkpoint, then use the ESS core skill's
`--request-id` path.

After a client timeout or lost submit response, reconcile the original narrow
submission window and checkpoint through read-only evidence. If no exact
identity can be established, classify the state as indeterminate and stop. A
new POST always requires a new preview and explicit approval.

## Error Handling

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

### Preflight and Redaction

Preflight every side effect by validating the exact environment, required
privileges, task and job identities, supported scope, current export shape,
mandatory option values, LOV cardinality and cross-checks, JSON payload shape,
safe transient/project paths, prior-request state, and the approval required
for that specific step.

Redaction is mandatory: never print credentials, Authorization headers, access
or refresh tokens, client secrets, private keys, or token-cache contents. Do
not persist those values in project diagnostics, checkpoints, or artifacts.

Refresh an eligible cached token once after a 401/403. Do not retry a final
authorization failure. Only read-only GET/status transport failures may use
bounded retries. Never automatically retry a scoped-export POST, ESS POST, or
post-submit export POST.

Diagnostics must record status, stage, failure class, message, recommended
action, environment, task/job identity, sanitized artifact references,
`ProcessId`/`requestId`/ECID when available, and the last observed state. Never
print or persist credentials, authorization headers, token-cache contents,
private keys, or full sensitive payloads in reusable repository content.

## Outputs and Token Usage

Persist the governed validation, request fingerprint, submission checkpoint,
terminal result, diagnostics, and skill-run record under the active project
workspace using the manifest paths. Register durable artifacts and update only
the declared project state. Append token usage with exact accounting when
available, otherwise the repository `chars/4` estimate.
