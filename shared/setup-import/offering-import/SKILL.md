---
skill_id: "shared.setup-import.offering-import"
name: "Offering Import"
description: "Imports Oracle Fusion setup CSV ZIP artifacts for an offering using the shared FSM CSV import engine."
layer: "shared"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "offering_identifier"
  - "setup_data_zip_path"
  - "execution_options"
outputs:
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
  - "import_process_log"
  - "token_usage_record"
depends_on:
  - "shared.setup-import.fsm-csv-import"
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
    default_location: "project/{project_id}/artifacts/shared/setup-import/offering-import/"
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
  - "Submits setup offering CSV import processes that can change Fusion configuration."
  - "Writes import metadata and process logs to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to discover setup feature codes and run setup offering CSV import"
---

# Offering Import

## Purpose

Imports setup data for a full Oracle Fusion offering from a CSV ZIP package.
This is a hierarchy wrapper over `shared.setup-import.fsm-csv-import`; it
resolves `OfferingCode` when a name is supplied, then delegates
create/poll/log-download behavior to the shared FSM CSV import engine.

This is a configuration-changing workflow. Confirm the target Fusion
environment, offering, and ZIP path before submitting the import.

## REST Flow

1. Resolve `OfferingCode` from the effective offering catalog when the user
   supplies an offering name; fall back to the Fusion `features` resource when
   the local catalog has no match.
2. Base64-encode the ZIP file.
3. Create a `setupOfferingCSVImports` process with `OfferingCode` and
   `SetupOfferingCSVImportProcess`.
4. Poll `SetupOfferingCSVImportProcess/{ProcessId}` for up to 3 minutes.
5. Download `ProcessLog` after completion.


## Project Scripts

Run from the repository root:

```bash
python3 shared/setup-import/offering-import/scripts/import_setup_offering_csv.py \
  --offering-name "Order Management" \
  --zip-file project/{project_id}/exports/setup-export/offering-export/doo_orchestration/export.zip \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15
```

When the offering code is already known:

```bash
python3 shared/setup-import/offering-import/scripts/import_setup_offering_csv.py \
  --offering-code DOO_ORCHESTRATION \
  --zip-file project/{project_id}/exports/setup-export/offering-export/doo_orchestration/export.zip \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15
```

## Required Inputs

If the user asks to import setup data but does not provide a ZIP path or
uploaded ZIP, ask for it before running the import:

```text
Please provide the setup data ZIP file path to import for <offering name>.
```

## Final Response

Include:

- Offering name/code
- ZIP file path used
- `ProcessId`
- Import log path, if retrieved
- Whether polling completed or timed out after 3 minutes

## Implementation Notes

Do not duplicate FSM CSV import REST mechanics in this skill. Keep offering code
lookup here, and call `shared.setup-import.fsm-csv-import` for process creation,
polling, process-log download, diagnostics, and artifact packaging.
