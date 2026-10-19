---
skill_id: "cx.sales.accounts-and-contacts.manage-customer-center-assignment-objects"
name: "Manage Customer Center Assignment Objects Setup Task Guidance"
description: "Exports or imports the complete Manage Customer Center Assignment Objects setup-task data as an unfiltered Oracle Fusion FSM package. Use only for whole-task FSM export/import; route every import through core.data-loader and refuse record-level maintenance, filtered or template exports, and direct REST or loader execution."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Accounts and Contacts"
functional_area_code: "ORA_SVC_ACCOUNTS_AND_CONTACTS"
task_code: "ZCM_MANAGE_CUSTOMER_CENTER_ASSIGNMENT_OBJECTS"
task_name: "Manage Customer Center Assignment Objects"
parent_skill_id: "cx.sales.accounts-and-contacts"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.3.0"
inputs:
  - "operation"
  - "project_id"
  - "fusion_environment_context"
  - "setup_data_zip_path"
  - "execution_options"
  - "execution_approval"
outputs:
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
  - "exports"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/sales/accounts-and-contacts/manage-customer-center-assignment-objects/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/accounts-and-contacts/manage-customer-center-assignment-objects/current/"
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
  - "After the skill's single import approval gate, imports one immutable whole-task FSM ZIP and can change configuration owned by Manage Customer Center Assignment Objects in the target Fusion environment."
  - "Writes redacted execution, diagnostic, run, artifact-registry, state, and token-usage records under the selected project workspace."
required_privileges:
  - "Fusion privileges to discover the setup task and run setup task CSV exports."
  - "Fusion privileges to submit, inspect, and retrieve logs for setup task CSV imports."
---

# Manage Customer Center Assignment Objects Setup Task Guidance

## Purpose and Boundary

Use this skill only to export or import the complete FSM setup package for
`Manage Customer Center Assignment Objects`. Fix the task identity to `ZCM_MANAGE_CUSTOMER_CENTER_ASSIGNMENT_OBJECTS` under
`Accounts and Contacts`.

Do not use this skill for planning, sequencing, standalone validation, template
generation, filtered exports, or individual customer-center-assignment-object inspection or
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

## Single-Approval User Experience

For each export or import operation, complete all safe, read-only preparation
before asking the user to approve anything. Intake questions, authentication,
validation, preview generation, and corrections are preparation steps, not
approval gates.

When preparation passes, present one compact execution summary containing the
environment, operation, fixed task name/code, exact scope, artifact path and
SHA-256 when applicable, output path, and side effect. Ask the user to reply
exactly `approve`. That one approval authorizes the one immutable operation
shown in the summary:

- for export, one FSM export submission plus polling and result retrieval;
- for import, one upload and initiation of the validated FSM ZIP.

Pass that approval through the selected shared or core workflow. Do not ask
again at a task-local, Task Hook, adapter, upload, or initiation boundary.
Downstream approval records are internal representations of the same user
approval, not new prompts.

If input is missing, validation fails, the environment is ambiguous, or an
explicit exception is required, stop with a friendly correction or blocker.
Do not label the correction as an approval request. Any change to the approved
environment, task, scope, archive bytes, hash, output path, or execution options
invalidates the approval and requires a new prepared summary.

## Fixed Task Context

- Pillar: `CX`
- Offering: `Sales`
- Functional area: `Accounts and Contacts`
- Functional area code: `ORA_SVC_ACCOUNTS_AND_CONTACTS`
- Task name: `Manage Customer Center Assignment Objects`
- Task code: `ZCM_MANAGE_CUSTOMER_CENTER_ASSIGNMENT_OBJECTS`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a task-code, offering, or functional-area override.

## Whole-Task FSM Export

1. Require `project_id` and the named source Fusion environment. Complete
   authentication, environment identity, privilege, live exact-task lookup,
   `CSVExportImportSupportedFlag=Y`, destination-path, and overwrite checks
   as read-only preflight; fail closed on a mismatch or blocker.
2. Fix `template_only=false` and `export_criteria=[]`. Refuse every filter,
   business-object subset, and template/specification request.
3. Build the single execution summary with the source environment, task
   name/code, unfiltered whole-task scope, output directory, and one-process
   impact. Ask exactly once for `approve`; do not ask for approval during
   discovery, authentication, validation, or output preparation.
4. Invoke `shared.setup-export.task-level-export` exactly once with the fixed
   context. Use its shared FSM engine for submission, polling, ZIP or
   `ProcessLog` retrieval, and packaging; do not implement task-local REST.
   Run the approved command with unbuffered output:

   ~~~bash
   python3 -u shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --data \
     --task-code ZCM_MANAGE_CUSTOMER_CENTER_ASSIGNMENT_OBJECTS \
     --offering-name "Sales" \
     --functional-area-name "Accounts and Contacts" \
     --project-id "{project_id}" \
     --output-dir project/{project_id}/exports/sales/accounts-and-contacts/manage-customer-center-assignment-objects/ \
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

1. Require `project_id`, the named target Fusion environment, and one explicit
   ZIP path. Complete authentication, target identity, privilege, route, and
   source-path checks as read-only preflight. Reject loose CSV files, multiple
   archives, and directory scans.
2. Verify that the file is a readable ZIP containing exactly one member whose
   basename is `ASM_SETUP_CSV_METADATA.xml`, and require its single
   `ObjectShortName` to equal `ZCM_MANAGE_CUSTOMER_CENTER_ASSIGNMENT_OBJECTS`. Preserve the archive
   byte for byte and calculate its SHA-256.
3. Invoke `core.data-loader` with the fixed task context and
   `dataloader_import_mode=FSM`. Let Data Loader own source review, task
   validation, FSM adapter selection, immutable preview creation,
   upload/initiation, and user-friendly reporting. Run its non-mutating
   preflight first:

   ~~~bash
   python3 core/data-loader/scripts/upload_and_initiate.py "{setup_data_zip_path}"
   ~~~

   Complete Task Hook validation and build the task-routed immutable preview
   before prompting the user. Require the preview and later approval envelope to retain
   `executionRoute=data-loader`, `sourceType=FSM`, the exact task code/name,
   absolute archive path, archive SHA-256, and `wholeTask=true`.
4. After every preflight check passes, display one user-friendly execution
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
5. Do not invoke `setupTaskCSVImports`, a shared import script, UCM upload, or a
   product adapter directly from this skill. Do not use an approval prompt to
   waive a validation problem: resolve it or report a blocker before the
   single execution summary. Any changed target, archive bytes, task context,
   or execution option invalidates approval and restarts Data Loader preflight.
6. Persist the accepted execution result and available redacted diagnostics in
   the declared report path. Check status only when the user asks, and never
   resubmit an import while its outcome is uncertain.

## Error and Retry Contract

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

- Refresh a cache-managed token once after a read-only 401 or 403. A second
  authentication response blocks execution.
- Never retry an export or import POST automatically. Require a new immutable
  preview and explicit approval before any new submission.
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

- Refuse individual customer-center-assignment-object creation, editing, deletion, or inspection.
- Refuse filtered, partial, criteria-based, and template/specification exports.
- Refuse task-code overrides, loose CSV files, edited or repacked ZIPs, and
  packages that Data Loader cannot confirm as the fixed FSM task.
- Refuse direct endpoint, script, or adapter execution that bypasses the
  required approval workflow.

## Golden Scenarios

| Request | Expected route |
|---|---|
| Export all Manage Customer Center Assignment Objects setup data from TEST | Approve and run one unfiltered FSM task export; persist the ZIP, hash, and process result |
| Import the complete exported ZIP into UAT | Finish Data Loader and Task Hook preflight, show one immutable-operation summary, request one approval, and submit one FSM import |
| Export only one customer-center-assignment-object | Refuse partial scope without making a Fusion call |
| Create or edit a customer-center-assignment-object | Refuse record-level maintenance without making a Fusion call |

## Sources

- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `shared/setup-export/task-level-export/SKILL.md`
- `core/data-loader/SKILL.md`
