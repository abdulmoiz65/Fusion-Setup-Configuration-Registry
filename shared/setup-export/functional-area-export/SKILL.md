---
skill_id: "shared.setup-export.functional-area-export"
name: "Functional Area Export"
description: "Exports Oracle Fusion functional-area CSV template/spec packages by default; exports setup data only when explicitly requested."
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
  - "export_package"
  - "template_package"
  - "process_log"
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
  - "Uses the shared FSM CSV export engine to create a setup offering CSV export or template export scoped by FunctionalAreaCode."
  - "Writes exported ZIP or process log artifacts to the local workspace."
required_privileges:
  - "Fusion privileges appropriate to find setup feature codes and run setup offering CSV export"
---

# Functional Area Export

## Purpose

Exports a CSV template/spec package for one Oracle Fusion functional area by
default. It exports setup data only when explicitly requested. This is a
hierarchy wrapper over `shared.setup-export.fsm-csv-export`; it resolves
Offering and Functional Area feature codes when names are supplied, then
delegates create/poll/download/package behavior to the shared FSM CSV export
engine.

## REST Flow

1. Resolve `OfferingCode` from
   the effective offering catalog, and
   `FunctionalAreaCode` from
   the effective functional-area catalog when the
   user supplies names instead of codes; fall back to the Fusion `features`
   resource when the local catalog has no match.
2. By default, create a `setupOfferingCSVTemplateExports` process with both
   codes.
3. Poll `SetupOfferingCSVTemplateExportProcess/{ProcessId}`.
4. Download `FileContent` on success or `ProcessLog` on error.

Unless the user explicitly asks for setup data, use the template/spec route:
`setupOfferingCSVTemplateExports` with both `OfferingCode` and
`FunctionalAreaCode`, polling `SetupOfferingCSVTemplateExportProcess/{ProcessId}`
and downloading only the template/spec ZIP from `FileContent`. Pass `--data`
only for an explicit setup-data request; it uses `setupOfferingCSVExports`,
which returns CSV files populated with current values.

Oracle references:

- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Find_Offering_Code.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/Offering_CSV_Export.html
- https://docs.oracle.com/en/cloud/saas/applications-shared/26b/farca/api-setup-offering-csv-exports.html

## Project Scripts

Run from the repository root:

```bash
python3 shared/setup-export/functional-area-export/scripts/export_functional_area_csv.py \
  --offering-name "Order Management" \
  --functional-area-name "Order Management" \
  --token-cache auto \
  --wait-seconds 300
```

For an explicit setup-data request:

```bash
python3 shared/setup-export/functional-area-export/scripts/export_functional_area_csv.py \
  --offering-name "Order Management" \
  --functional-area-name "Order Management" \
  --data \
  --token-cache auto \
  --wait-seconds 300
```

When codes are already known:

```bash
python3 shared/setup-export/functional-area-export/scripts/export_functional_area_csv.py \
  --offering-code DOO_ORCHESTRATION \
  --functional-area-code ORA_DOO_ORDER_MANAGEMENT \
  --token-cache auto \
  --wait-seconds 300
```

The script imports:

```text
shared/setup-export/fsm-csv-export/scripts/fsm_csv_export_engine.py
```

## Inputs

- `fusion_environment_context`
- `request_payload`: offering name/code and functional area name/code.
- `execution_options`: token cache, polling interval, wait timeout, output
  directory, optional existing `ProcessId`, and optional explicit `data` mode;
  template/spec mode is the default.

## Outputs

- `export_package`
- `template_package`
- `process_log`
- `diagnostics`
- `audit_summary`

## Implementation Notes

Do not duplicate FSM CSV export REST mechanics in this skill. Keep code lookup
and hierarchy-specific validation here, and call `shared.setup-export.fsm-csv-export`
for process creation, polling, download, diagnostics, and artifact packaging.
