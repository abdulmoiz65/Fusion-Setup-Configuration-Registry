---
skill_id: "shared.setup-import.task-level-import"
name: "Task Level Import"
description: "Imports Oracle Fusion setup task CSV ZIP artifacts for a specific task and retrieves the import process log."
layer: "shared"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "setup_task_identifier"
  - "setup_data_zip_path"
  - "execution_options"
outputs:
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
  - "import_process_log"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
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
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/shared/setup-import/task-level-import/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to a Fusion environment when approved."
  - "Submits setup task CSV import processes that can change Fusion configuration."
  - "Writes import metadata and process logs to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to discover setup tasks and run setup task CSV import"
---

# Task Level Import

Use this skill to import Oracle Fusion setup data for a specific setup task from
a CSV export ZIP. This is a configuration-changing workflow, so confirm the
target Fusion environment, setup task, and ZIP path before submitting the import.

Use `shared.setup-import.offering-import` for offering-scoped CSV ZIP imports
and `shared.setup-import.functional-area-import` for functional-area scoped CSV
ZIP imports. This skill remains the task-specific wrapper.

## Workflow

1. Authenticate with Fusion Cloud using `core.auth.fusion-oauth-authentication`
   when login or token refresh is needed.
2. Ask the user for the setup data ZIP file path if they have not provided one.
3. Resolve the setup task code from task name, optionally filtered by Offering
   and Functional Area.
4. Confirm the resolved task and ZIP path before submitting the import.
5. Base64-encode the ZIP and create a setup task CSV import through
   `setupTaskCSVImports`.
6. Poll `SetupTaskCSVImportProcess/{ProcessId}` for up to 3 minutes.
7. Retrieve `ProcessLog` when the import completes, or stop polling and tell the
   user to manually prompt before retrying that `ProcessId`.
8. Store import logs and metadata under
   `project/{project_id}/artifacts/shared/setup-import/task-level-import/<task_name>`
   when a project workspace is in use.

## Project Assumptions

- Run from the repository root.
- Use `core/auth/fusion-oauth-authentication` for
  Fusion login, authentication, and access token refresh.
- The default Fusion environment properties file is
  `core/auth/fusionEnv.properties`.
- Use this skill's scripts for setup task import:
  - `shared/setup-import/task-level-import/scripts/find_setup_task_code.py`
  - `shared/setup-import/task-level-import/scripts/create_setup_task_csv_import.py`
  - `shared/setup-import/task-level-import/scripts/get_setup_task_csv_import_result.py`
  - `shared/setup-import/task-level-import/scripts/import_setup_task_csv.py`
- Use the local setup task catalog at
  `knowledge/setup-task-catalog/release/setupTasksAll.json`
  for task-code lookup fallback and `CSVExportImportSupportedFlag` checks before
  submitting CSV imports.
- Prefer file token cache `.fusionaim_token.json` because macOS Keychain may be
  unreadable from the shell.
- Do not print access tokens, client secrets, `.fusionaim_token.json` contents,
  or full base64 ZIP payloads.
- Network access to Fusion REST normally requires command approval/escalation.

## Required Inputs

If the user asks to import setup data but does not provide a ZIP path or uploaded
ZIP, ask for it before running the import:

```text
Please provide the setup data ZIP file path to import for <task name>.
```

If the user provides a file path, pass it with `--zip-file`. The script validates
that the file exists and starts with a ZIP signature.

## Login

For login, authentication, or token refresh, use
`core.auth.fusion-oauth-authentication`. After authentication, pass
`--token-cache auto` to this skill's scripts.

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py \
  --token-cache auto
```

## Find the Task Code

Use the task lookup script when the user provides a task name:

```bash
python3 shared/setup-import/task-level-import/scripts/find_setup_task_code.py \
  --task-name "Manage Item Organizations" \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --token-cache auto \
  --output project/{project_id}/artifacts/shared/setup-import/task-level-import/manage_item_organizations/setup_task_search.md \
  --print
```

If exact Offering or Functional Area filters return no rows, broaden to task
name only and inspect returned metadata.

Oracle reference:
https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Find_SetupTask_Code.html

## Import and Download Log

For most requests, use the orchestration script:

```bash
python3 shared/setup-import/task-level-import/scripts/import_setup_task_csv.py \
  --task-name "Manage Item Organizations" \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --zip-file project/{project_id}/exports/product_management/item_organizations/manage_item_organizations/export.zip \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15 \
  --output-dir project/{project_id}/artifacts/shared/setup-import/task-level-import/manage_item_organizations
```

If the task code is already known:

```bash
python3 shared/setup-import/task-level-import/scripts/import_setup_task_csv.py \
  --task-code EGP_MANAGE_ITEM_ORGANIZATIONS \
  --task-name "Manage Item Organizations" \
  --zip-file project/{project_id}/exports/product_management/item_organizations/manage_item_organizations/export.zip \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15 \
  --output-dir project/{project_id}/artifacts/shared/setup-import/task-level-import/manage_item_organizations
```

The script creates a setup task import through `setupTaskCSVImports`, polls
`SetupTaskCSVImportProcess/{ProcessId}`, and downloads `ProcessLog` after
completion.

Oracle references:

- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Task_CSV_Import.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/api-setup-task-csv-imports.html

## If Polling Times Out

If the import is not complete within 3 minutes, stop polling. Report the
`TaskCode`, `ProcessId`, and last status to the user. Tell the user to manually
prompt before checking the results of that `ProcessId` again and retrieving the
import process artifacts.

Retry with:

```bash
python3 shared/setup-import/task-level-import/scripts/get_setup_task_csv_import_result.py \
  --task-code EGP_MANAGE_ITEM_ORGANIZATIONS \
  --process-id 100003586108233 \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15 \
  --output project/{project_id}/artifacts/shared/setup-import/task-level-import/manage_item_organizations/import_process_log.txt
```

## Final Response

Include:

- Task name and resolved `TaskCode`
- ZIP file path used
- `ProcessId`
- Import log path, if retrieved
- Whether polling completed or timed out after 3 minutes
