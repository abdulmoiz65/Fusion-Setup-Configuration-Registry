---
skill_id: "shared.setup-export.task-level-export"
name: "Task Level Export"
description: "Discovers Oracle Fusion setup task codes and exports task-level CSV template/spec packages by default; exports setup data only when explicitly requested."
layer: "shared"
pillar: "Common"
type: "export"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs:
  - "execution_result"
  - "template_package"
  - "diagnostics"
  - "audit_summary"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.fsm-csv-export"
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
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to a Fusion environment when approved."
  - "Uses the shared FSM CSV export engine to create setup task CSV export or template export processes in Fusion."
  - "Writes exported ZIP or process log artifacts to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to discover setup tasks and run setup task CSV export"
---

# Task Level Export

Use this skill to export a setup-task CSV template/spec package by default. Use
it to capture the current Fusion configuration baseline only when the request
explicitly asks for setup data. This skill owns task discovery and task-level
validation, then delegates raw FSM CSV export mechanics to
`shared.setup-export.fsm-csv-export`.

The workflow is:

1. Authenticate with Fusion Cloud using `core.auth.fusion-oauth-authentication`
   when login or token refresh is needed.
2. Find the setup task code from a task name, optionally filtered by Offering
   and Functional Area.
3. Check `CSVExportImportSupportedFlag`; if it is not `Y`, do not create a setup
   task CSV export and tell the user the export may not work.
4. Default to `setupTaskCSVTemplateExports`; create a populated setup task CSV
   export through `setupTaskCSVExports` only for an explicit setup-data request.
5. Use the shared engine to poll the export process by `ProcessId`.
6. Use the shared engine to download `FileContent` when successful, or
   `ProcessLog` when the export fails.
7. Store the ZIP/log locally under
   `project/{project_id}/exports/<offering>/<functional-area>/<task_name>`.
   Resolve those path parts from matching pillar skill metadata and write them
   in kebab case.

Unless the user explicitly asks for setup data, use template/spec mode. This
mode calls `setupTaskCSVTemplateExports` and downloads only the CSV
template/spec package. Use `--data` only when the user explicitly requests the
current setup values; it calls `setupTaskCSVExports` instead.

## Project Assumptions

- Run from the repository root.
- Use `core/auth/fusion-oauth-authentication` for
  Fusion login, authentication, and access token refresh.
- The default Fusion environment properties file is
  `core/auth/fusionEnv.properties`.
- Use this skill's scripts for setup task discovery and export:
  - `shared/setup-export/task-level-export/scripts/find_setup_task_code.py`
  - `shared/setup-export/task-level-export/scripts/create_setup_task_csv_export.py`
  - `shared/setup-export/task-level-export/scripts/get_setup_task_csv_export_result.py`
  - `shared/setup-export/task-level-export/scripts/export_setup_task_csv.py`
- Use the shared FSM CSV export implementation engine for raw `TaskCode`
  create/poll/download/package behavior:
  - `shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py`
  - `shared/setup-export/fsm-csv-export/scripts/fsm_csv_export_engine.py`
- Use the local setup task catalog at
  `knowledge/setup-task-catalog/release/setupTasksAll.json`
  for task-code lookup fallback and `CSVExportImportSupportedFlag` checks when
  live Fusion metadata is unavailable or a task code is supplied directly.
- Resolve pillar context from the functional-area `SKILL.md` and setup-task
  metadata files such as `pillars/*/<offering>/<functional-area>/<task>.md`
  before writing exports. Matching task metadata provides authoritative
  `offering`, `functional_area`, `functional_area_code`, `task_code`, and
  `task_name` metadata for output paths and future pillar-specific
  directives.
- Prefer file token cache `.fusionaim_token.json` because macOS Keychain may be
  unreadable from the shell.
- Do not print access tokens, client secrets, or the contents of
  `.fusionaim_token.json`.
- Network access to Fusion REST normally requires command approval/escalation.

## Login

For login, authentication, or token refresh, use
`core.auth.fusion-oauth-authentication`. After authentication, pass
`--token-cache auto` to this skill's scripts.

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py \
  --token-cache auto
```

## Find the Task Code

Use the task lookup script first when the user provides a task name:

```bash
python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
  --task-name "Manage Item Organizations" \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --token-cache auto \
  --output project/{project_id}/artifacts/product_management/item_organizations/manage_item_organizations/setup_task_search.md \
  --print
```

If exact Offering or Functional Area filters return no rows, broaden to task
name only and inspect returned metadata:

```bash
python3 shared/setup-export/task-level-export/scripts/find_setup_task_code.py \
  --task-name "Manage Item Organizations" \
  --token-cache auto \
  --json \
  --output project/{project_id}/artifacts/offering/functional_area/manage_item_organizations/setup_task_search.json \
  --print
```

Choose the exact `TaskName` match when present. Confirm
`CSVExportImportSupportedFlag` is `Y` before exporting.

Oracle reference:
https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Find_SetupTask_Code.html

## Export and Download

For a template/spec request—or an export request without an explicit data
request—use the orchestration script with no mode flag:

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-name "Manage Item Organizations" \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 300 \
  --poll-interval 15
```

The script derives the default output directory as:

```text
project/{project_id}/exports/<offering-kebab>/<functional-area-kebab>/<setup-task-name-kebab>
```

If only a task code is provided, include `--offering-name` and
`--functional-area-name` when possible so the default output folder is
meaningful:

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-code EGP_MANAGE_ITEM_ORGANIZATIONS \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 300 \
  --poll-interval 15
```

The script checks `CSVExportImportSupportedFlag` before creating an export. If
CSV export/import is not supported, it stops before calling the shared
`fsm-csv-export` engine. By default, the shared engine creates a template/spec
export through `setupTaskCSVTemplateExports`, polls
`SetupTaskCSVTemplateExportProcess/{ProcessId}`, and downloads the result. On
success, it writes a ZIP; on failure, it writes the process log.

For an explicit setup-data request, pass `--data`:

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-name "Manage Item Organizations" \
  --offering-name "Product Management" \
  --functional-area-name "Item Organizations" \
  --project-id "{project_id}" \
  --token-cache auto \
  --data \
  --wait-seconds 300 \
  --poll-interval 15
```

`--data` creates the export through `setupTaskCSVExports`, polls
`SetupTaskCSVExportProcess/{ProcessId}`, and downloads
`SetupTaskCSVExportProcessResult/{ProcessId}/enclosure/FileContent`.

### Filtered Setup-Task Export

For an explicitly requested data export limited to a business-object criterion,
pass `--data` and one or more
criteria in a JSON array using `--export-criteria` or
`--export-criteria-file`. The task-level exporter adds that array to the create
request as `SetupTaskCSVExportCriteria`. Every criterion is bound to the
selected task code; a supplied, different `TaskCode` is rejected before Fusion
is called. Criteria are not supported for template/spec exports.

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-code HZ_MANAGE_RESOURCE_ROLES \
  --data \
  --export-criteria '[{"TaskCode":"HZ_MANAGE_RESOURCE_ROLES","BusinessObjectCode":"JTF_RS_ROLES_B","AttributeSet":"Set1","AttributeName":"RoleTypeCode","AttributeValue":"CHANNEL_SALES"}]' \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 300 \
  --poll-interval 15
```

Equivalent request-body fragment:

```json
{
  "TaskCode": "HZ_MANAGE_RESOURCE_ROLES",
  "SetupTaskCSVExportCriteria": [
    {
      "TaskCode": "HZ_MANAGE_RESOURCE_ROLES",
      "BusinessObjectCode": "JTF_RS_ROLES_B",
      "AttributeSet": "Set1",
      "AttributeName": "RoleTypeCode",
      "AttributeValue": "CHANNEL_SALES"
    }
  ],
  "SetupTaskCSVExportProcess": [
    { "TaskCode": "HZ_MANAGE_RESOURCE_ROLES" }
  ]
}
```

Oracle references:

- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Task_CSV_Export.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/api-setup-task-csv-exports.html
- https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvexports-post.html


## If Polling Times Out

If the export is not complete within `--wait-seconds`, report the `TaskCode`,
`ProcessId`, and the last status to the user. Wait for the user to ask for retry
before polling again.

Retry with:

```bash
python3 shared/setup-export/task-level-export/scripts/get_setup_task_csv_export_result.py \
  --task-code EGP_MANAGE_ITEM_ORGANIZATIONS \
  --process-id 100003586108233 \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 300 \
  --poll-interval 15 \
  --output project/{project_id}/exports/product_management/item_organizations/manage_item_organizations/exfh-test_setup_task_csv_export_egp_manage_item_organizations_100003586108233.zip
```

The result helper requires `--template-only` when polling a template/spec
process. Omit it only when retrying an explicitly requested setup-data process.

## After Download

Verify and extract the artifact:

```bash
unzip -l project/{project_id}/exports/<offering>/<functional-area>/<task_name>/<export-file>.zip
unzip -o project/{project_id}/exports/<offering>/<functional-area>/<task_name>/<export-file>.zip \
  -d project/{project_id}/exports/<offering>/<functional-area>/<task_name>/<export-folder>
```

In the final response, include:

- Task name and resolved `TaskCode`
- `ProcessId`
- ZIP or log file path
- Extracted folder path, if extracted
- Whether `FileContent` or `ProcessLog` was retrieved

## Shared Engine Boundary

Do not duplicate setup task CSV export process mechanics in this skill. Keep
task lookup, task-name disambiguation, local setup-task catalog fallback, and
`CSVExportImportSupportedFlag` checks here. Use
`shared.setup-export.fsm-csv-export` for raw `TaskCode` process creation,
polling, result download, log fallback, retry handling, and artifact packaging.
