---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-data-styles"
name: "Manage Data Styles Setup Task Guidance"
description: "Exports or imports the complete Manage Data Styles setup-task data as an unfiltered Oracle Fusion FSM package. Use only for whole-task FSM export/import; route every import through core.data-loader and refuse record-level maintenance, filtered or template exports, and direct REST or loader execution."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_DATA_STYLES"
task_name: "Manage Data Styles"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.2.0"
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
    default_location: "project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-data-styles/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-data-styles/current/"
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
  - "After the separate core.data-loader approval gate, imports one immutable whole-task FSM ZIP and can change data-style configuration in the target Fusion environment."
  - "Writes redacted execution, diagnostic, run, artifact-registry, state, and token-usage records under the selected project workspace."
required_privileges:
  - "Fusion privileges to discover the setup task and run setup task CSV exports."
  - "Fusion privileges to submit, inspect, and retrieve logs for setup task CSV imports."
---

# Manage Data Styles Setup Task Guidance

## Purpose and Boundary

Use this skill only to export or import the complete FSM setup package for
`Manage Data Styles`. Fix the task identity to `HZ_MANAGE_DATA_STYLES` under
`Trading Community Foundation`.

Do not use this skill for planning, sequencing, standalone validation, template
generation, filtered exports, or individual data-style inspection or
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

## Fixed Task Context

- Pillar: `CX`
- Offering: `Customer Data Management`
- Functional area: `Trading Community Foundation`
- Functional area code: `ORA_HZ_CDM_FOUNDATION`
- Task name: `Manage Data Styles`
- Task code: `HZ_MANAGE_DATA_STYLES`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a task-code, offering, or functional-area override.

## Whole-Task FSM Export

1. Require `project_id` and the named source Fusion environment. Resolve the
   live task by the exact fixed task code and confirm
   `CSVExportImportSupportedFlag=Y`; fail closed on a mismatch.
2. Fix `template_only=false` and `export_criteria=[]`. Refuse every filter,
   business-object subset, and template/specification request.
3. Show the source environment, task name/code, unfiltered whole-task scope,
   output directory, and one-process impact. Obtain explicit approval
   immediately before the export POST.
4. Invoke `shared.setup-export.task-level-export` exactly once with the fixed
   context. Use its shared FSM engine for submission, polling, ZIP or
   `ProcessLog` retrieval, and packaging; do not implement task-local REST.
   Run the approved command with unbuffered output:

   ```bash
   python3 -u shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --data \
     --task-code HZ_MANAGE_DATA_STYLES \
     --offering-name "Customer Data Management" \
     --functional-area-name "Trading Community Foundation" \
     --project-id "{project_id}" \
     --output-dir project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-data-styles/ \
     --token-cache auto \
     --wait-seconds 300 \
     --poll-interval 10
   ```

   If the command runner yields a session or cell identifier, wait on that same
   process until it exits. The `-u` option exposes the shared exporter's
   `Started ... process: <ProcessId>` line without changing shared code.
   Capture that identifier in the task skill's run record. Empty initial output
   is not failure, and must not trigger a replacement export.
5. Persist the `ProcessId` as soon as it is returned. On success, verify the ZIP,
   calculate SHA-256, store it in the declared export directory, register it,
   and update project state.
6. On timeout, preserve the same `ProcessId`, last status, and elapsed time.
   Resume only that process after a later request; never submit a replacement
   export automatically.

## Whole-Task FSM Import Through Data Loader

1. Require `project_id`, the named target Fusion environment, and one explicit
   ZIP path. Reject loose CSV files, multiple archives, and directory scans.
2. Verify that the file is a readable ZIP containing exactly one member whose
   basename is `ASM_SETUP_CSV_METADATA.xml`, and require its single
   `ObjectShortName` to equal `HZ_MANAGE_DATA_STYLES`. Preserve the archive
   byte for byte and calculate its SHA-256.
3. Invoke `core.data-loader` with the fixed task context and
   `dataloader_import_mode=FSM`. Let Data Loader own source review, task
   validation, FSM adapter selection, immutable preview creation, approval,
   upload/initiation, and user-friendly reporting. Start with:

   ```bash
   python3 core/data-loader/scripts/upload_and_initiate.py "{setup_data_zip_path}"
   ```

   Require the task-routed preview and approval envelope to retain
   `executionRoute=data-loader`, `sourceType=FSM`, the exact task code/name,
   absolute archive path, archive SHA-256, and `wholeTask=true`.
4. Treat the initial import request as validation only. Display the exact target,
   fixed task code, ZIP path and hash, and impact statement; stop before the
   first POST. Continue only after the separate user message required by
   `core.data-loader` approves that immutable artifact. Then use Data Loader's
   approved task-routed command with the envelope returned by Task Hook:

   ```bash
   python3 core/data-loader/scripts/upload_and_initiate.py "{setup_data_zip_path}" \
     --task-routed \
     --task-validation-envelope "{task_validation_envelope_path}" \
     --approve-upload
   ```
5. Do not invoke `setupTaskCSVImports`, a shared import script, UCM upload, or a
   product adapter directly from this skill. Any changed target, archive bytes,
   task context, or execution option invalidates approval and restarts Data
   Loader preflight.
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

- Refuse individual data-style creation, editing, deletion, or inspection.
- Refuse filtered, partial, criteria-based, and template/specification exports.
- Refuse task-code overrides, loose CSV files, edited or repacked ZIPs, and
  packages that Data Loader cannot confirm as the fixed FSM task.
- Refuse direct endpoint, script, or adapter execution that bypasses the
  required approval workflow.

## Golden Scenarios

| Request | Expected route |
|---|---|
| Export all data styles from TEST | Approve and run one unfiltered FSM task export; persist the ZIP, hash, and process result |
| Import the complete exported ZIP into UAT | Run `core.data-loader` preflight, require its separate immutable-artifact approval, and submit one FSM import |
| Export only one data style | Refuse partial scope without making a Fusion call |
| Create or edit a data style | Refuse record-level maintenance without making a Fusion call |

## Sources

- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `shared/setup-export/task-level-export/SKILL.md`
- `core/data-loader/SKILL.md`
