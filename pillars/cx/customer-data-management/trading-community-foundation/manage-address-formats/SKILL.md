---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-address-formats"
name: "Manage Address Formats Setup Task Guidance"
description: "Exports or imports the complete Manage Address Formats setup-task data as an unfiltered Oracle Fusion FSM package, including cross-environment imports whose single approval explicitly covers a bounded source-target revision-mismatch fallback. Use only for whole-task FSM export/import; route exports through the shared task-level exporter and imports through core.data-loader validation with this task's native FSM adapter. Refuse record-level maintenance, filtered or template exports, undisclosed revision overrides, and execution that bypasses the approved route."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_ADDRESS_FORMATS"
task_name: "Manage Address Formats"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.14.0"
inputs:
  - "operation"
  - "project_id"
  - "fusion_environment_context"
  - "setup_data_zip_path"
  - "execution_options"
  - "execution_approval"
outputs:
  - "consolidated_approval_preview"
  - "configuration_export"
  - "export_submission_record"
  - "data_load_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.setup-import.fsm-csv-import"
  - "core.data-loader"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.project-mgmt.project-workspace-initializer"
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
oracle_supplied_guidance_files:
  - purpose: "Validate the fixed whole-task operation and single-approval contract before export or import."
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Find the live task by its fixed name and validate the exact fixed TaskCode without depending on optional hierarchy fields."
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Classify failures, preserve ProcessId diagnostics, and prevent unsafe resubmission."
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Task-local validation, live lookup, and error-handling rules are compiled and ready."
state_updates:
  - "exports"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-address-formats/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/current/"
    versioning_policy: "append-only"
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
  - "After explicit approval, creates and polls one whole-task FSM export process and writes its ZIP or process log to the project workspace."
  - "After explicit approval, imports one immutable whole-task FSM ZIP through the Data Loader-authorized shared task-level FSM adapter and can change address-format configuration in the target Fusion environment."
  - "Writes redacted preview, execution, diagnostic, run, artifact-registry, state, and token-usage records under the selected project workspace."
required_privileges:
  - "Fusion privileges to discover the setup task and run setup task CSV exports."
  - "Fusion privileges to submit, inspect, and retrieve logs for setup task CSV imports."
---

# Manage Address Formats Setup Task Guidance

## Purpose and Boundary

Export or import the complete FSM setup package for `Manage Address Formats`.
Fix the task identity to `HZ_MANAGE_ADDRESS_FORMATS` under `Trading Community
Foundation`.

Do not use this skill for planning, standalone validation, template generation,
filtered exports, or individual address-style inspection or maintenance.
Validation is permitted only as mandatory preparation for an export or import.

## Supported Operations

1. `export`: export every setup-data object owned by the fixed task as one
   unfiltered, non-template FSM package through
   `shared.setup-export.task-level-export`.
2. `import`: import one complete, unchanged FSM ZIP for the fixed task through
   mandatory `core.data-loader` validation and approval, then execute only
   through this skill's `native-fsm-import` as the selected native FSM
   adapter.

Treat a migration request as two operations. Complete and persist the source
export before starting a separate target import preflight and approval.

## One Consolidated Approval

Use exactly one conversational approval point for each export or import.
Gather and validate every detail before asking for approval. Project creation,
local task-context refresh, authentication, browser sign-in, source review,
metadata checks, preview generation, Task Hook validation, and approval-envelope
creation are preparation steps and require no business-operation approval.

For an import, bind the approval to an initial submission with
`SourceTargetDiffOkFlag=N` and one conditional fallback with
`SourceTargetDiffOkFlag=Y` only if Fusion explicitly rejects the first
submission for a source-target revision mismatch. Disclose that bounded
two-submission behavior in the summary. The same approval authorizes the
conditional fallback because its target, task, archive bytes, hash, adapter,
and execution options remain immutable.

The only approval or acknowledgement response this skill may ask the user to
send is the standalone word `approve`, and only after the complete immutable
execution summary is ready. Factual questions remain permitted only for a
genuinely missing value that cannot be resolved safely from durable context.
Never ask the user to reply with `ready`, `continue`, `approve`, or any other
acknowledgement to start, finish, or resume authentication. Never ask whether
the user approves opening a login page, starting the OAuth callback listener,
using the configured local token cache, refreshing authentication, or running
read-only preflight checks.

## Authentication Is Unapproved Preparation

Run authentication as one uninterrupted preparation phase before the execution
approval summary:

1. Use the configured environment and the prescribed local, gitignored file
   token cache from the first authentication attempt. Reuse a valid cached
   token; otherwise start exactly one OAuth callback listener in a persistent
   execution session and open the configured identity-provider page.
2. If the identity provider requires interactive user input, provide only an
   informational update such as: `Complete the Oracle sign-in in the browser
   window; preparation will continue automatically.` Do not request a reply,
   confirmation, approval, or sentinel word.
3. Keep waiting on the same login process and callback. After authentication
   succeeds, continue environment identity, privilege, task, package, adapter,
   Task Hook, and preview validation automatically from the same waiting
   process, without a conversational handoff.
4. Do not launch repeated login flows merely because the first listener has not
   produced output yet. Poll or wait on that listener until it completes or its
   declared timeout is reached.
5. If authentication ultimately fails or times out, report an authentication
   blocker and the concrete remediation. Do not present an execution approval
   summary, do not ask for `approve`, and do not ask the user to reply `ready`.
   When authentication later becomes available, resume preparation directly.

Authentication permission prompts imposed by the host runtime are platform
controls, not conversational approvals owned by this skill. Do not add a
second chat approval around them.

Complete this preparation bundle first:

1. Resolve the project, configured environment, fixed task, operation, scope,
   source or output path, execution options, and overwrite state from supplied
   inputs and durable context. Ask a factual question only when a value remains
   ambiguous or unsafe.
2. If no implementation project exists, create the repository-prescribed draft
   project. If its local task context is missing or stale, run the project
   workspace initializer's artifact-only refresh. Do not create or update a
   live Oracle Run Book.
3. Complete OAuth authentication and source or target identity checks under
   `Authentication Is Unapproved Preparation`. Treat interactive browser
   sign-in as authentication, never as a chat checkpoint or export/import
   approval.
4. Finish catalog, privilege, live task, path, overwrite, package, Data Loader,
   Task Hook, and immutable-preview checks that apply to the selected operation.

After preparation succeeds, render the execution summary as a CommonMark bullet
list with one labeled detail per item, in this order:

- Environment: source for export or target for import.
- Operation: `export` or `import`.
- Task name: `Manage Address Formats`.
- Task code: `HZ_MANAGE_ADDRESS_FORMATS`.
- Scope: the exact whole-task scope.
- File name: for export, the planned pattern `<environment>_setup_task_csv_export_hz_manage_address_formats_<ProcessId>.zip`
  and note that Fusion assigns `ProcessId`; for import, the exact ZIP basename.
- File path: output directory plus the planned pattern for export; exact absolute
  ZIP path for import.
- SHA-256: `Computed after download; unavailable before approval` for export;
  verified archive hash for import.
- Execution adapter: the selected shared adapter.
- Execution options: wait, polling, and applicable fallback settings.
- Revision mismatch fallback: import only; bounded initial `N` and exact-mismatch-only `Y` behavior.
- Side effect: the precise Fusion mutation and local artifacts produced.
Do not collapse these details into prose or a table, and do not omit the file
items merely because an export filename and hash are finalized after approval.

Ask the user once to reply exactly `approve`. That single approval authorizes
only the immutable operation shown:

- Export: one FSM export submission, polling, and result retrieval.
- Import: one initial `setupTaskCSVImports` submission of the validated FSM ZIP
  and, only for Fusion's explicit revision-mismatch rejection, one conditional
  override submission of those same immutable bytes, followed by polling and
  result retrieval through the selected shared adapter.

Downstream approval records are internal representations of that same approval.
Do not prompt again at a task-local, Task Hook, adapter, upload, initiation, or
polling boundary. A change to any preview-bound value invalidates approval and
requires a new prepared summary.

An `approve` message received before a ready immutable summary is not usable.
Continue or repair preparation without asking for another acknowledgement;
after preparation succeeds, present the one complete summary and make the
operation's single approval request.

If a local failure provably happens before the first POST, permit one bounded
recovery without another approval only when the preview fingerprint and every
bound value are unchanged and audit evidence confirms no POST was attempted.
If a POST was attempted or its outcome is uncertain, approval is consumed and
automatic resubmission is forbidden, except for the exact revision-mismatch
fallback already disclosed and bound in the import preview.

## Direct Export Trigger and Resume

Treat `export manage address formats task`, `export fsm task Manage Address
Formats`, and equivalent whole-task wording as a complete export request. Infer
`operation=export`, the fixed task identity, `template_only=false`,
`export_criteria=[]`, `wait_seconds=300`, and `poll_interval=10`. Resolve the
single configured Fusion environment and project without an approval prompt.

Run all safe preparation in the same turn. Persist the redacted ready preview:

```text
project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/current/export-approval-preview.json
```

The preview must have `status=ready_for_approval` and bind its fingerprint to:

- project ID and source environment
- operation, task name, and task code
- whole-task, unfiltered, non-template scope
- output directory and shared export adapter
- empty export criteria
- wait and polling options
- exact live lookup artifact and lookup result

Compute the fingerprint from a canonical JSON representation of those bound
values, excluding timestamps, status, and the fingerprint field itself. Never
persist a token, secret, authorization header, or token-cache content.

Present the same values and ask exactly for `approve`. On the next standalone
`approve`, load the persisted preview, recompute its fingerprint, recheck all
bound values and the destination state, and immediately run the one shared
export command. Do not repeat discovery or request another approval. Capture
the `ProcessId`, poll it, retrieve `FileContent` or `ProcessLog`, verify and
register the artifact, update project state, append token usage, and report the
result. If no valid ready preview exists, repair preflight and present a new
summary; never treat an unbound approval as permission for a POST.

## Fixed Task Context

- Pillar: `CX`
- Offering: `Customer Data Management`
- Offering code: `ZCH_CDM`
- Functional area: `Trading Community Foundation`
- Functional area code: `ORA_HZ_CDM_FOUNDATION`
- Task name: `Manage Address Formats`
- Task code: `HZ_MANAGE_ADDRESS_FORMATS`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a task-code, offering, or functional-area override.

## Whole-Task FSM Export

1. Resolve or create the project, refresh missing local task-context artifacts,
   and select the configured source Fusion environment. Complete authentication,
   environment identity, privilege, destination-path, and overwrite checks as
   read-only preparation without a login approval or `ready` handshake.
2. Use the shared task-name lookup without hierarchy filters:

   ```bash
   python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
     --task-name "Manage Address Formats" \
     --token-cache auto \
     --output project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/current/setup-task-search.json \
     --json \
     --print
   ```

   Require exactly one returned row with the exact `TaskName`,
   `TaskCode=HZ_MANAGE_ADDRESS_FORMATS`, `AvailableFlag=Y`, and
   `CSVExportImportSupportedFlag=Y`. Live setup-task responses may omit offering
   and functional-area fields; validate hierarchy from the effective catalog
   and persisted task context. Fail closed on contradictory nonblank hierarchy
   data or zero/multiple exact rows. Never select the first search result merely
   because it appears first.
3. Fix `template_only=false` and `export_criteria=[]`. Refuse every record,
   country, address-style, business-object, attribute, and template filter.
4. Persist the immutable `export-approval-preview.json`, show the single
   execution summary, and ask once for `approve` as defined above. Do not route
   export preview creation through `core.data-loader`, its Task Hook, or any
   archive-verification command. An export has no ZIP or archive SHA-256 before
   Fusion completes it.
5. After approval verification, invoke the shared exporter exactly once:

   ```bash
   python3 -u shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --data \
     --task-code HZ_MANAGE_ADDRESS_FORMATS \
     --offering-name "Customer Data Management" \
     --functional-area-name "Trading Community Foundation" \
     --project-id "{project_id}" \
     --output-dir project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-address-formats/ \
     --token-cache auto \
     --wait-seconds 300 \
     --poll-interval 10
   ```

   Use a persistent execution session with unbuffered output. Empty initial
   output is not failure and must not trigger another export.
6. Persist the returned `ProcessId` immediately, then poll and retrieve results
   only for that process. On `COMPLETED` or `COMPLETED_WARNINGS`, verify the ZIP,
   compute its SHA-256, register it, and update project state. On
   `COMPLETED_ERRORS`, retrieve and persist `ProcessLog` when available.
7. On timeout, preserve the same `ProcessId`, last status, and elapsed time.
   Resume only that process after a later status request; never submit a
   replacement export automatically.

If execution ends after the POST but before the `ProcessId` is observable,
reconcile with a read-only export-process lookup using the environment, task
code, and run-start window. Resume exactly one matching process. Fail closed on
zero, multiple, or unidentifiable candidates; a new POST requires a new preview
and approval.

## Whole-Task FSM Import Through the Data Loader-Authorized FSM Adapter

1. Resolve or create the project and select the configured target environment.
   Require one explicit ZIP path; reject loose CSV files, multiple archives,
   directory scans, edited archives, and repacked archives.
2. Ensure the project has a current task-context entry resolving the sequence,
   exact task name/code, and this skill path. Refresh only local artifacts when
   needed; do not create a live Oracle Run Book.
3. Complete authentication under `Authentication Is Unapproved Preparation`,
   then target identity, privilege, route, and source-path checks before preview
   creation. Do not pause for a `ready` response after sign-in.
4. Verify a readable ZIP containing exactly one member whose basename is
   `ASM_SETUP_CSV_METADATA.xml`. Require its single `ObjectShortName` to equal
   `HZ_MANAGE_ADDRESS_FORMATS`. Preserve the archive byte for byte and compute
   its SHA-256.
5. Route the import through `core.data-loader` with the fixed task context and
   `dataloader_import_mode=FSM`. Data Loader owns source review, Task Hook
   validation, adapter selection, immutable preview, approval-envelope
   creation, and approved-payload release. It does not require its generic UCM
   uploader to be the execution adapter.
6. During adapter selection, inspect the target pod's live
   `dataLoaderDataSets/describe` action metadata. Never add `runID`,
   `sourceType`, or another property to an ADF action unless that exact action
   advertises the property. For this setup-task FSM package, select
   `cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import` and its `setupTaskCSVImports` route.
   Do not select `core/data-loader/scripts/upload_and_initiate.py`; generic
   Data Loader upload/initiation is not the native setup-task CSV import
   contract for this package.
7. Build the Data Loader Task Hook preview over the exact immutable archive.
   Require it to retain `executionRoute=data-loader`,
   `executionAdapter=cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import`,
   `packageType=FSM`, `revisionMismatchPolicy=auto_override_on_exact_mismatch`,
   `sourceTargetDiffOkFlagSequence=[N,Y_on_exact_revision_mismatch]`, the fixed task name/code,
   absolute archive path, archive SHA-256, `wholeTask=true`, `waitSeconds=180`,
   and `pollInterval=15`. The adapter and revision policy are preview-bound;
   changing either invalidates approval.
8. After every preflight check passes, display the one immutable-operation
   summary and ask once for the standalone response `approve`. On that message,
   record Task Hook approval internally, verify the archive hash again, persist
   the approved envelope, and release that exact payload to the selected task-local
   adapter without another prompt.
9. Invoke the task-local adapter exactly once:

   ```bash
   python3 -u pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/scripts/import_manage_address_formats.py \
     --zip-file "{setup_data_zip_path}" \
     --task-validation-envelope project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/current/import-approval-envelope.json \
     --token-cache auto \
     --wait-seconds 180 \
     --poll-interval 15 \
     --output-dir project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/imports/
   ```

   This adapter owns the bounded `setupTaskCSVImports` submission sequence,
   immediate `ProcessId` capture, polling, and `ProcessLog` retrieval. Do not
   call its endpoint or scripts before Data Loader releases the approved payload.
10. The approved command sends `SourceTargetDiffOkFlag=N` first. If and only if
    Fusion returns the explicit HTTP 400 source-target revision-mismatch
    rejection without a `ProcessId`, continue automatically with
    `SourceTargetDiffOkFlag=Y` under the same approval. Permit no more than this
    one fallback submission. Stop on any other response, uncertain outcome, or
    failure, and never ask for a second approval for the preview-bound fallback.
11. Do not upload this FSM ZIP through `uploadDataLoaderFile`, call
    `initiateDataLoad`, or send `sourceType: FSM`. Any changed target, archive
    bytes, hash, task context, adapter, revision policy, or execution option
    invalidates approval.
12. Persist the accepted result and redacted diagnostics. If the adapter returns
    a `ProcessId`, resume or inspect only that process and never resubmit while
    its outcome is uncertain.

## User Experience Contract

Keep the workflow calm, predictable, and easy to resume:

1. During preparation, send short progress updates only when the stage changes:
   authentication, package validation, live task validation, and approval-ready.
   Never expose endpoint trivia, raw JSON, Base64 content, or internal rule names.
2. Present exactly one approval summary using the labeled list defined above.
   Explain the revision fallback as a safety behavior, not as a second import:
   `Fusion is tried with revision protection first; only an explicit revision
   mismatch permits one retry of the same package.`
3. After approval, report `Import accepted` as soon as Fusion returns a
   `ProcessId`. State whether the revision fallback was `not needed` or `applied
   once`.
4. On completion, lead with the outcome and show only the target, task, status,
   ProcessId, immutable ZIP/hash, and artifact links. Put technical diagnostics
   after the outcome and only when they help resolve a failure.
5. On timeout, say `The import is still running; no new submission is needed`,
   show the same ProcessId and last status, and offer the status-only continuation.
6. On a blocked preflight, identify the single failed check and the concrete
   correction. Do not ask for approval until the full immutable summary is ready.
7. On an uncertain POST response, say that no retry was made and that the next
   action is read-only reconciliation. Never imply that the import failed merely
   because a ProcessId was not observable.

## Error and Retry Contract

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

- Refresh a cache-managed token once after a read-only 401 or 403. A second
  authentication response blocks execution. During the approved adapter POST
  sequence, a cache-managed 401/403 may also refresh once; resume the same `N`
  or `Y` stage and never restart from `N` after reaching `Y`.
- Treat HTTP 400 action error `27503` from generic `initiateDataLoad` as an
  adapter-contract defect. Stop, preserve whether UCM upload already succeeded
  and its content ID when available, and do not retry that generic route or
  upload the archive again.
- Never retry an export POST or an import POST automatically except for the
  preview-approved Manage Address Formats fallback from `N` to `Y` after
  Fusion's exact revision-mismatch rejection. Limit that fallback to one second
  submission of the same immutable operation.
- On timeout or failure, report environment, operation, task code, `ProcessId`
  or request ID, last status, elapsed time, diagnostic artifact, and one safe
  next action.
- Never print or persist tokens, secrets, authorization headers, token-cache
  contents, full Base64 payloads, or sensitive customer data.

## Result Contract

For export, report source environment, fixed task name/code, `ProcessId`, status,
ZIP or log path, enclosure type, and ZIP SHA-256 when available. For import,
return the Data Loader-authorized shared adapter result and report target, task
name/code, immutable ZIP path and hash, `ProcessId`, status, and available
process log. Lead with `Import accepted`, `Import completed`, `Import completed
with errors`, or `Import is still running`. State revision fallback as `not
needed` or `applied once`; never expose `N`/`Y` without the plain-language label.
Record the skill run and token usage for every durable project activity.

## Refusal Rules

- Refuse individual address-style creation, editing, deletion, reordering, or
  inspection.
- Refuse filtered, partial, criteria-based, and template/specification exports.
- Refuse task-code overrides, loose CSV files, edited or repacked ZIPs, and
  packages that Data Loader cannot confirm as the fixed FSM task.
- Refuse the generic `uploadDataLoaderFile` plus `initiateDataLoad` route when
  live action metadata does not advertise every proposed payload property.
- Refuse direct endpoint, script, or adapter execution that bypasses the
  operation-specific approval workflow.

## Golden Scenarios

| Request | Expected route |
|---|---|
| Export all address formats from the configured environment | Gather and validate all inputs, persist one export preview, ask once for approval, then run one shared FSM export and persist the ZIP, hash, and process result |
| Import the complete exported ZIP | Finish Data Loader and Task Hook preflight, select this skill's native FSM adapter, show one immutable summary, ask once for approval, and submit the bounded initial-plus-exact-mismatch-fallback sequence |
| Fusion rejects import for a revision mismatch | Under the already approved bounded fallback, immediately resubmit the same immutable operation once with `SourceTargetDiffOkFlag=Y`, then poll the returned ProcessId without another approval |
| Export only one country or address style | Refuse partial scope without making a Fusion call |
| Create or edit an address style | Refuse record-level maintenance without making a Fusion call |
| Export polling times out | Preserve the ProcessId and resume only that process after a later status request |

## Sources

- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `shared/setup-export/task-level-export/SKILL.md`
- `shared/setup-import/fsm-csv-import/SKILL.md`
- `core/data-loader/SKILL.md`
- `https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html`
- `https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-imports.html`
