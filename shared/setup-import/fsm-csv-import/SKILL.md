---
skill_id: "shared.setup-import.fsm-csv-import"
name: "FSM CSV Import"
description: "Shared implementation engine for Oracle Fusion FSM CSV import process creation, polling, diagnostics, and process-log retrieval."
layer: "shared"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs: 
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
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
  - "Submits setup task or setup offering CSV import processes that can change Fusion configuration."
  - "Polls Fusion import process status and downloads ProcessLog artifacts."
required_privileges: 
  - "Fusion privileges appropriate to create and retrieve FSM CSV import processes"
---

# FSM CSV Import

## Purpose

Provides the shared low-level FSM CSV import engine used by hierarchy-specific
setup import skills. This skill owns the REST mechanics for creating import
processes, polling process status, downloading import process logs, and
resolving offering/functional-area feature codes.

## When to Use

Use higher-level skills for user-facing hierarchy semantics:

- `shared.setup-import.task-level-import` for setup task CSV import workflows.
- `shared.setup-import.functional-area-import` for functional-area scoped setup
  CSV imports.
- `shared.setup-import.offering-import` for offering scoped setup CSV imports.

## REST Resources

Task-level imports use:

```text
POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVImports
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess/{ProcessId}/child/SetupTaskCSVImportProcessResult/{ProcessId}/enclosure/ProcessLog
```

Offering and functional-area imports use:

```text
POST /fscmRestApi/resources/11.13.18.05/setupOfferingCSVImports
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVImports/{OfferingCode}/child/SetupOfferingCSVImportProcess/{ProcessId}
GET  /fscmRestApi/resources/11.13.18.05/setupOfferingCSVImports/{OfferingCode}/child/SetupOfferingCSVImportProcess/{ProcessId}/child/SetupOfferingCSVImportProcessResult/{ProcessId}/enclosure/ProcessLog
```

`FunctionalAreaCode` is optional in the `setupOfferingCSVImports` payload. When
it is supplied, the import is scoped to that functional area; when omitted, the
import is offering scoped.

Oracle references:

- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Task_CSV_Import.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/api-setup-task-csv-imports.html


## Inputs

- `fusion_environment_context`
- `import_scope`: `task`, `offering`, or `functional-area`.
- `request_payload`: `TaskCode` for task scope, or `OfferingCode` with optional
  `FunctionalAreaCode` for offering and functional-area scope.
- `setup_data_zip_path`
- `execution_options`: token cache, wait timeout, polling interval, output
  directory, and optional project ID.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`
- `import_process_log`

## Implementation Notes

Run scripts from the repository root. The shared implementation lives in:

```text
shared/setup-import/fsm-csv-import/scripts/fsm_csv_import_engine.py
```

Hierarchy skills should call the shared engine instead of duplicating REST
endpoint construction, base64 ZIP encoding, process polling, log retrieval,
feature-code lookup, or artifact naming.

Do not print access tokens, refresh tokens, client secrets,
`.fusionaim_token.json` contents, Authorization headers, or full base64 ZIP
payloads.
