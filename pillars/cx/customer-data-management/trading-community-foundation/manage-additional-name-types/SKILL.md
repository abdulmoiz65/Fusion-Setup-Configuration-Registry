---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-additional-name-types"
name: "Manage Additional Name Types Setup Task Guidance"
description: "Exports or imports the complete Manage Additional Name Types setup-task data as an unfiltered Oracle Fusion FSM package, gathering project context, authentication, validation, and the immutable preview before one consolidated approval. Use only for whole-task FSM export/import; route every import through core.data-loader and refuse record-level maintenance, filtered or template exports, and direct REST or loader execution."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_ADDITIONAL_NAME_TYPES"
task_name: "Manage Additional Name Types"
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
version: "0.5.1"
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
  - purpose: "Validate the fixed whole-task operation contract before export or import."
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Search the live task by its fixed name, then select and validate the exact fixed TaskCode without requiring hierarchy fields that the setupTasks resource may omit."
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Classify failures, preserve identifiers, and prevent unsafe resubmission."
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Task-local validation, live lookup, and error-handling rules are compiled and ready."
state_updates:
  - "exports"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-additional-name-types/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-additional-name-types/current/"
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
  - "After the skill's single import approval gate, imports one immutable whole-task FSM ZIP and can change configuration owned by Manage Additional Name Types in the target Fusion environment."
  - "Writes redacted execution, diagnostic, run, artifact-registry, state, and token-usage records under the selected project workspace."
required_privileges:
  - "Fusion privileges to discover the setup task and run setup task CSV exports."
  - "Fusion privileges to submit, inspect, and retrieve logs for setup task CSV imports."
---

# Manage Additional Name Types Setup Task Guidance

## Purpose and Boundary

Use this skill only to export or import the complete FSM setup package for
`Manage Additional Name Types`. Fix the task identity to
`HZ_MANAGE_ADDITIONAL_NAME_TYPES` under `Trading Community Foundation`.

Do not use this skill for planning, sequencing, standalone validation, template
generation, filtered exports, or individual additional-name-type inspection or
maintenance. Validation is permitted only as a mandatory preflight for an
export or import.

## Supported Operations

1. `export`: export every setup-data object owned by the fixed task as one
   unfiltered, non-template FSM package through
   `shared.setup-export.task-level-export`.
2. `import`: import one complete, unchanged FSM ZIP for the fixed task through
   the mandatory `core.data-loader` workflow.

Treat a migration request as these two operations in sequence. Finish and
persist the source export before starting a separate target import preflight
and approval.

## One Consolidated Approval

Use exactly one conversational approval point for each export or import
operation. Gather and validate every detail first. Never ask the user to
approve project creation, local Run Book artifact refresh, task-context
creation, authentication, browser sign-in, source review, metadata checks,
preview generation, Task Hook validation, or approval-envelope creation.
Those are preparation steps.

Complete the preparation bundle before mentioning approval:

1. Resolve the project, environment, fixed task, operation, source or output
   path, scope, execution options, and overwrite state from supplied inputs and
   durable project context. Ask concise factual questions only for values that
   cannot be resolved safely; do not frame them as approvals.
2. If no implementation project exists, create the repository-prescribed draft
   project and inform the user. If the selected project lacks a current local
   task context, run the project workspace initializer's artifact-only refresh:

   ~~~bash
   python3 core/project-mgmt/project-workspace-initializer/scripts/create_project_runbook.py \
     --project-root project/{project_id} \
     --refresh-artifacts
   ~~~

   This command must not create or update a live Oracle Run Book. Do not stop to
   ask the user to authorize this local, non-mutating prerequisite.
3. Complete OAuth authentication and target/source identity checks before
   building the approval summary. Open the configured OAuth URL in the default
   browser when interactive sign-in is required and wait for the callback.
   Treat browser sign-in as authentication, not as an execution approval.
4. Finish catalog, privilege, path, ZIP, task metadata, Data Loader, Task Hook,
   destination, overwrite, and immutable-preview checks. Persist the exact
   preview that downstream approval records will reference.

Only after the complete bundle passes, present one compact execution summary
containing the environment, operation, fixed task name/code, exact scope,
artifact path and SHA-256 when applicable, output path, execution options, and
side effect. Ask the user once to reply exactly `approve`. That one approval
authorizes the one immutable operation shown in the summary:

- for export, one FSM export submission plus polling and result retrieval;
- for import, one upload and initiation of the validated FSM ZIP.

Pass that approval through the selected shared or core workflow. Do not ask
again at a task-local, Task Hook, adapter, upload, or initiation boundary.
Downstream approval records are internal representations of the same user
approval, not new prompts. Never bypass host security controls; satisfy any
platform-required login or tool permission during preparation when possible
and do not reinterpret it as another business-operation approval.

If input is missing, validation fails, the environment is ambiguous, or an
explicit exception is required, stop with a friendly correction or blocker.
Do not label the correction as an approval request. Any change to the approved
environment, task, scope, archive bytes, hash, output path, or execution options
invalidates the approval and requires a new prepared summary.

An approval is not consumed by a failure that provably occurs before the first
live POST, such as a local browser-launch, token-cache access, file-permission,
or approval-envelope persistence failure. Correct that preparation failure and
resume the exact approved operation without asking again, but only when the
environment, task, scope, archive bytes and hash, output path, execution
options, and preview fingerprint are unchanged and audit evidence confirms
that no live POST was attempted. Permit at most one bounded recovery for that
pre-POST failure. If a POST was attempted, accepted, timed out, or has an
uncertain outcome, the approval is consumed; never resubmit automatically.

## Direct Export Trigger and Resume

Treat `export fsm task Manage Additional Name Types` and equivalent whole-task
export wording as a complete export request. Infer `operation=export`, the
fixed task identity, `template_only=false`, `export_criteria=[]`, the standard
300-second wait, and the 10-second poll interval. Resolve the project and the
single configured Fusion environment from durable context. Ask a factual
question only when more than one viable environment or project remains, or an
overwrite conflict cannot be resolved safely.

Run every preparation step in the same turn, then persist the redacted ready
preview at:

```text
project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-additional-name-types/current/export-approval-preview.json
```

Set `status=ready_for_approval` and bind the preview fingerprint to the project,
source environment, operation, task name/code, whole-task scope, output
directory, adapter, template flag, empty export criteria, wait seconds, poll
interval, and live lookup artifact. Include no token, secret, authorization
header, or token-cache content. Present the same bound values to the user and
ask exactly for `approve`; do not finish the turn with a plan when preparation
has succeeded.

When the next user message is exactly `approve`, load the persisted ready
preview, verify its fingerprint and bound values are unchanged, and immediately
run the one shared export command in this skill. Do not repeat discovery, ask
another business approval, or stop after process submission: capture the
`ProcessId`, poll it, retrieve `FileContent` or `ProcessLog`, verify and register
the artifact, update project state, append token usage, and report the result.
If no valid ready preview exists, complete or repair preflight and present a new
summary; never reinterpret an unbound approval as permission for a POST.

## Fixed Task Context

- Pillar: `CX`
- Offering: `Customer Data Management`
- Offering code: `ZCH_CDM`
- Functional area: `Trading Community Foundation`
- Functional area code: `ORA_HZ_CDM_FOUNDATION`
- Task name: `Manage Additional Name Types`
- Task code: `HZ_MANAGE_ADDITIONAL_NAME_TYPES`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a task-code, offering, or functional-area override.

## Whole-Task FSM Export

1. Resolve or create `project_id`, refresh missing local task-context artifacts,
   and resolve the named source Fusion environment without an approval prompt.
   Complete authentication, environment identity, privilege, destination-path,
   and overwrite checks as read-only preflight. Use the existing shared
   task-name lookup without hierarchy filters, then select the one result whose
   `TaskCode` and `TaskName` exactly match the fixed task identity:

   ~~~bash
   python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
     --task-name "Manage Additional Name Types" \
     --token-cache auto \
     --output project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-additional-name-types/current/setup-task-search.json \
     --json \
     --print
   ~~~

   From the returned rows, require exactly one live row with
   `TaskCode=HZ_MANAGE_ADDITIONAL_NAME_TYPES`, the exact task name,
   `AvailableFlag=Y`, and `CSVExportImportSupportedFlag=Y`. The documented
   `setupTasks` response may omit `OfferingName`, `OfferingCode`,
   `FunctionalAreaName`, and `FunctionalAreaCode`; validate that hierarchy from
   the effective catalog and persisted task context, and do not reject the task
   merely because those live fields are absent or blank. If Fusion returns a
   nonblank hierarchy value on the exact row that contradicts the
   catalog-backed context, or if zero or multiple rows have the exact fixed
   code and name, fail closed before approval or POST. Ignore non-exact search
   results; never select the first row merely because it was returned first.
2. Fix `template_only=false` and `export_criteria=[]`. Refuse every filter,
   business-object subset, and template/specification request.
3. Write `export-approval-preview.json` with `status=ready_for_approval`, the
   immutable bound fields and preview fingerprint defined above. Build the
   single execution summary from that artifact with the source environment,
   task name/code, unfiltered whole-task scope, output directory, polling
   options, and one-process impact. Ask exactly once for `approve`; do not ask
   for approval during discovery, authentication, validation, or output
   preparation.
4. Invoke `shared.setup-export.task-level-export` exactly once with the fixed
   context. Use its shared FSM engine for submission, polling, ZIP or
   `ProcessLog` retrieval, and packaging; do not implement task-local REST.
   Run the approved command with unbuffered output:

   ~~~bash
   python3 -u shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --data \
     --task-code HZ_MANAGE_ADDITIONAL_NAME_TYPES \
     --offering-name "Customer Data Management" \
     --functional-area-name "Trading Community Foundation" \
     --project-id "{project_id}" \
     --output-dir project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-additional-name-types/ \
     --token-cache auto \
     --wait-seconds 300 \
     --poll-interval 10
   ~~~

   If the command runner yields a session or cell identifier, wait on that same
   process until it exits. The `-u` option exposes the shared exporter's
   `Started ... process: <ProcessId>` line without changing shared code.
   Capture that identifier in the task skill's run record. Empty initial output
   is not failure and must not trigger a replacement export.
5. Persist the `ProcessId` as soon as it is returned. On success, verify the ZIP,
   calculate SHA-256, store it in the declared export directory, register it,
   and update project state.
6. On timeout, preserve the same `ProcessId`, last status, and elapsed time.
   Resume only that process after a later request; never submit a replacement
   export automatically.

## Whole-Task FSM Import Through Data Loader

1. Resolve or create `project_id`, the named target Fusion environment, and one
   explicit ZIP path. Reuse durable project inputs instead of asking the user
   to restate them. Reject loose CSV files, multiple archives, and directory
   scans.
2. Ensure that the project contains a current task-context entry resolving
   sequence, exact task name/code, and this skill path. If it is missing or
   stale, run the local `--refresh-artifacts` command from the consolidated
   preparation bundle and continue automatically. Never ask for separate Run
   Book artifact authorization and never create a live Oracle Run Book as an
   import prerequisite.
3. Complete OAuth authentication, browser callback when required, target
   identity, required privilege, route, and source-path checks before creating
   the approval preview. Confirm that the same cached authentication mechanism
   is available to the eventual Data Loader command; do not defer first-time
   login until after approval.
4. Verify that the file is a readable ZIP containing exactly one member whose
   basename is `ASM_SETUP_CSV_METADATA.xml`, and require its single
   `ObjectShortName` to equal `HZ_MANAGE_ADDITIONAL_NAME_TYPES`. Preserve the
   archive byte for byte and calculate its SHA-256.
5. Invoke `core.data-loader` with the fixed task context and
   `dataloader_import_mode=FSM`. Let Data Loader own source review, task
   validation, FSM adapter selection, immutable preview creation,
   upload/initiation, and user-friendly reporting. Run its non-mutating
   preflight first:

   ~~~bash
   python3 core/data-loader/scripts/upload_and_initiate.py "{setup_data_zip_path}"
   ~~~

   Complete Task Hook validation and build the task-routed immutable preview
   before mentioning approval. Require the preview and later approval envelope
   to retain `executionRoute=data-loader`, `sourceType=FSM`, the exact task
   code/name, absolute archive path, archive SHA-256, and `wholeTask=true`.
6. After every preflight check passes, display one user-friendly execution
   summary with the exact target, fixed task name/code, ZIP path and hash,
   whole-task scope, validation status, and configuration-changing impact.
   Ask exactly once for the separate message `approve`; stop before the first
   POST. On that message, record Task Hook approval for the displayed preview,
   verify the archive hash again, create the approval envelope, and immediately
   use Data Loader's approved task-routed command without another prompt:

   ~~~bash
   python3 core/data-loader/scripts/upload_and_initiate.py "{setup_data_zip_path}" \
     --task-routed \
     --task-validation-envelope "{task_validation_envelope_path}" \
     --approve-upload
   ~~~
7. Treat Task Hook preview approval, archive verification, approval-envelope
   persistence, command authorization, upload authorization, and initiation
   authorization as internal representations of the one user approval. Do not
   expose them as additional user approval points. If an authentication or
   local-permission failure occurs before the first POST, apply the bounded
   pre-POST recovery rule and reuse the same approval only when the immutable
   preview fingerprint is unchanged.
8. Do not invoke `setupTaskCSVImports`, a shared import script, UCM upload, or a
   product adapter directly from this skill. Do not use an approval prompt to
   waive a validation problem: resolve it or report a blocker before the
   single execution summary. Any changed target, archive bytes, task context,
   or execution option invalidates approval and restarts Data Loader preflight.
9. Persist the accepted execution result and available redacted diagnostics in
   the declared report path. Check status only when the user asks, and never
   resubmit an import while its outcome is uncertain.

## Error and Retry Contract

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

- Refresh a cache-managed token once after a read-only 401 or 403. A second
  authentication response blocks execution.
- Permit one recovery of an unchanged approved operation only when audit
  evidence proves the failure occurred before the first live POST. This is a
  continuation of the same approved operation, not a new submission.
- Never retry an export or import POST automatically. After a POST attempt or
  uncertain response, require a new immutable preview and explicit approval
  before any new submission.
- On timeout or failure, report the environment, operation, task code,
  `ProcessId` or request ID when available, last status, elapsed time,
  diagnostic artifact, and recommended next action.
- Never print or persist tokens, secrets, authorization headers, token-cache
  contents, full Base64 payloads, or sensitive customer data.

## Result Contract

For export, report the source environment, fixed task name/code, `ProcessId`,
status, ZIP or log path, enclosure type, and ZIP SHA-256 when available. For
import, return the complete `core.data-loader` Markdown result and report the
target environment, fixed task name/code, immutable ZIP path and hash, status,
and available process log. Record the skill run and token usage for every
durable project activity.

## Refusal Rules

- Refuse individual additional-name-type creation, editing, deletion, or inspection.
- Refuse filtered, partial, criteria-based, and template/specification exports.
- Refuse task-code overrides, loose CSV files, edited or repacked ZIPs, and
  packages that Data Loader cannot confirm as the fixed FSM task.
- Refuse direct endpoint, script, or adapter execution that bypasses the
  required approval workflow.

## Golden Scenarios

| Request | Expected route |
|---|---|
| Export all Manage Additional Name Types setup data from TEST | Approve and run one unfiltered FSM task export; persist the ZIP, hash, and process result |
| Import the complete exported ZIP into UAT | Finish Data Loader and Task Hook preflight, show one immutable-operation summary, request one approval, and submit one FSM import |
| Import when local task context is missing | Refresh local artifact-only Run Book context automatically, finish authentication and validation, then ask once for the consolidated import approval |
| Authentication cache is inaccessible after approval but before any POST | Repair authentication once and continue the unchanged approved operation without another user approval |
| Export only one additional-name-type | Refuse partial scope without making a Fusion call |
| Create or edit an additional-name-type | Refuse record-level maintenance without making a Fusion call |

## Sources

- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `shared/setup-export/task-level-export/SKILL.md`
- `core/data-loader/SKILL.md`
- `https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/Find_SetupTask_Code.html`
