---
skill_id: "shared.setup-export.fsm-csv-export"
name: "FSM CSV Export"
description: "Shared implementation engine for Oracle Fusion FSM CSV export process creation, polling, diagnostics, and artifact packaging."
layer: "shared"
pillar: "Common"
type: "export"
execution_mode: "automated"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "export_scope"
  - "request_payload"
  - "execution_options"
outputs:
  - "export_package"
  - "template_package"
  - "process_log"
  - "process_status"
  - "diagnostics"
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
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to a Fusion environment when approved."
  - "Creates setup task or setup offering CSV export or template export processes in Fusion."
  - "Polls Fusion export process status and downloads FileContent or ProcessLog artifacts."
required_privileges:
  - "Fusion privileges appropriate to create and retrieve FSM CSV export packages"
---

# FSM CSV Export

## Purpose

Provides the shared low-level FSM CSV export engine used by hierarchy-specific
setup export skills. This skill owns the REST mechanics for creating export
processes, polling process status, downloading export ZIP files or process logs,
and writing package artifacts.

Use higher-level skills for user-facing hierarchy semantics:

- `shared.setup-export.task-level-export` for setup task name/code workflows.
- `shared.setup-export.functional-area-export` for functional-area scoped setup
  data exports.
- `shared.setup-export.offering-export` for offering scoped setup data exports.

## REST Resources

Task-level exports use:

```text
POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports/{TaskCode}/child/SetupTaskCSVExportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports/{TaskCode}/child/SetupTaskCSVExportProcess/{ProcessId}/child/SetupTaskCSVExportProcessResult/{ProcessId}/enclosure/FileContent
```

`POST setupTaskCSVExports` accepts an optional
`SetupTaskCSVExportCriteria` child array in the same request body. The shared
engine supports this only for task-scoped data exports; it is not sent to the
template/spec endpoint.

Task-level template/spec exports use:

```text
POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports/{TaskCode}/child/SetupTaskCSVTemplateExportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports/{TaskCode}/child/SetupTaskCSVTemplateExportProcess/{ProcessId}/child/SetupTaskCSVTemplateExportProcessResult/{ProcessId}/enclosure/FileContent
```

Offering and functional-area exports use:

```text
GET  /fscmRestApi/resources/11.13.18.05/features
POST /fscmRestApi/resources/11.13.18.05/setupOfferingCSVExports
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVExports/{OfferingCode}/child/SetupOfferingCSVExportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVExports/{OfferingCode}/child/SetupOfferingCSVExportProcess/{ProcessId}/child/SetupOfferingCSVExportProcessResult/{ProcessId}/enclosure/FileContent
```

Offering and functional-area template/spec exports use:

```text
GET  /fscmRestApi/resources/11.13.18.05/features
POST /fscmRestApi/resources/11.13.18.05/setupOfferingCSVTemplateExports
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVTemplateExports/{OfferingCode}/child/SetupOfferingCSVTemplateExportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVTemplateExports/{OfferingCode}/child/SetupOfferingCSVTemplateExportProcess/{ProcessId}/child/SetupOfferingCSVTemplateExportProcessResult/{ProcessId}/enclosure/FileContent
```

When the user asks for a "template", "templates", "spec", "specification", or
"template spec", use `--template-only` (or `--template` / `--spec`) so Fusion
returns only CSV template/spec files. Do not use the normal CSV export endpoint
for those requests because it returns setup CSV files populated with current
environment values.

Oracle references:

- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Find_Offering_Code.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Offering_CSV_Export.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/api-setup-offering-csv-exports.html

## Project Scripts

Run from the repository root.

Raw task-code export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope task \
  --task-code ORA_FOM_MANAGE_ORDER_MANAGEMENT_EXTENSIONS \
  --token-cache auto \
  --wait-seconds 300
```

Raw task-code template/spec export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope task \
  --task-code ORA_FOM_MANAGE_ORDER_MANAGEMENT_EXTENSIONS \
  --template-only \
  --token-cache auto \
  --wait-seconds 300
```

Raw offering-code export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope offering \
  --offering-code DOO_ORCHESTRATION \
  --token-cache auto \
  --wait-seconds 300
```

Raw offering-code template/spec export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope offering \
  --offering-code DOO_ORCHESTRATION \
  --template-only \
  --token-cache auto \
  --wait-seconds 300
```

Raw functional-area export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope functional-area \
  --offering-code DOO_ORCHESTRATION \
  --functional-area-code ORA_DOO_ORDER_MANAGEMENT \
  --token-cache auto \
  --wait-seconds 300
```

Raw functional-area template/spec export:

```bash
python3 shared/setup-export/fsm-csv-export/scripts/fsm_csv_export.py \
  --scope functional-area \
  --offering-code DOO_ORCHESTRATION \
  --functional-area-code ORA_DOO_ORDER_MANAGEMENT \
  --template-only \
  --token-cache auto \
  --wait-seconds 300
```

## Inputs

- `fusion_environment_context`
- `export_scope`: `task`, `offering`, or `functional-area`.
- `request_payload`: `TaskCode` for task scope, or `OfferingCode` with optional
  `FunctionalAreaCode` for offering and functional-area scope.
- `execution_options`: token cache, wait timeout, polling interval, output
  directory, optional existing `ProcessId`, and optional `template_only` mode.

## Outputs

- `export_package`: decoded ZIP file from `FileContent`.
- `template_package`: decoded ZIP file from `FileContent` when
  `template_only` mode is used.
- `process_log`: process log text when Fusion completes with errors or
  `--download-log` is supplied.
- `process_status`: `ProcessId`, `ProcessCompletedFlag`, `StatusCode`, and
  result metadata.
- `diagnostics`: REST error details and retry notes.

## Implementation Notes

This skill is an implementation engine, not the preferred user-facing workflow.
Hierarchy skills should call these scripts or import `fsm_csv_export_engine.py`
instead of duplicating REST endpoint construction, process polling, base64 ZIP
decoding, log fallback, token retry, or artifact naming.

Shared workflows that have offering, functional-area, or setup-task context
should resolve matching pillar skill metadata before deciding project paths or
pillar-specific behavior. The reusable helper lives at:

```text
shared/setup-export/fsm-csv-export/scripts/pillar_skill_metadata.py
```

Use `core.auth.fusion-oauth-authentication` for login and token refresh. Do not
print access tokens, refresh tokens, client secrets, `.fusionaim_token.json`
contents, or Authorization headers.
