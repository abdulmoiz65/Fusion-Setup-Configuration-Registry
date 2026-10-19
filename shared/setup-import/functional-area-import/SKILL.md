---
skill_id: "shared.setup-import.functional-area-import"
name: "Functional Area Import"
description: "Imports Oracle Fusion setup CSV ZIP artifacts for a functional area using the shared FSM CSV import engine."
layer: "shared"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "offering_identifier"
  - "functional_area_identifier"
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
    default_location: "project/{project_id}/artifacts/shared/setup-import/functional-area-import/"
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
  - "Submits setup functional-area CSV import processes that can change Fusion configuration."
  - "Writes import metadata and process logs to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to discover setup feature codes and run setup offering CSV import scoped by FunctionalAreaCode"
---

# Functional Area Import

## Purpose

Imports setup data for one Oracle Fusion functional area from a CSV ZIP package.
This is a hierarchy wrapper over `shared.setup-import.fsm-csv-import`; it
resolves Offering and Functional Area feature codes when names are supplied,
then delegates create/poll/log-download behavior to the shared FSM CSV import
engine.

This is a configuration-changing workflow. Confirm the target Fusion
environment, offering, functional area, and ZIP path before submitting the
import.

## REST Flow

1. Resolve `OfferingCode` from
   the effective offering catalog, and
   `FunctionalAreaCode` from
   the effective functional-area catalog when names
   are supplied; fall back to the Fusion `features` resource when the local
   catalog has no match.
2. Base64-encode the ZIP file.
3. Create a `setupOfferingCSVImports` process with both `OfferingCode` and
   `FunctionalAreaCode`.
4. Poll `SetupOfferingCSVImportProcess/{ProcessId}` for up to 3 minutes.
5. Download `ProcessLog` after completion.


## Project Scripts

Run from the repository root:

```bash
python3 shared/setup-import/functional-area-import/scripts/import_setup_functional_area_csv.py \
  --offering-name "Order Management" \
  --functional-area-name "Order Management" \
  --zip-file project/{project_id}/exports/setup-export/functional-area-export/doo_orchestration/ora_doo_order_management/export.zip \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15
```

When codes are already known:

```bash
python3 shared/setup-import/functional-area-import/scripts/import_setup_functional_area_csv.py \
  --offering-code DOO_ORCHESTRATION \
  --functional-area-code ORA_DOO_ORDER_MANAGEMENT \
  --zip-file project/{project_id}/exports/setup-export/functional-area-export/doo_orchestration/ora_doo_order_management/export.zip \
  --project-id "{project_id}" \
  --token-cache auto \
  --wait-seconds 180 \
  --poll-interval 15
```

## Required Inputs

If the user asks to import setup data but does not provide a ZIP path or
uploaded ZIP, ask for it before running the import:

```text
Please provide the setup data ZIP file path to import for <functional area name>.
```

## Final Response

Include:

- Offering name/code and Functional Area name/code
- ZIP file path used
- `ProcessId`
- Import log path, if retrieved
- Whether polling completed or timed out after 3 minutes

## Implementation Notes

Do not duplicate FSM CSV import REST mechanics in this skill. Keep feature code
lookup here, and call `shared.setup-import.fsm-csv-import` for process creation,
polling, process-log download, diagnostics, and artifact packaging.
