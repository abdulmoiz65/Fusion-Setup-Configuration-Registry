---
skill_id: "cx.sales.territories.manage-territory-geographies"
name: "Manage Territory Geographies Setup Task Guidance"
description: "Prepares and validates new Territory Geography CSV rows and routes upload and initiation exclusively through core.data-loader CX Import for the Manage Territory Geographies task under CX Sales Territories."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Territories"
functional_area_code: "ORA_TRT_TERRITORIES"
task_code: "MOT_MANAGE_TERRITORY_GEOGRAPHIES"
task_name: "Manage Territory Geographies"
parent_skill_id: "cx.sales.territories"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.3.1"
inputs:
  - "territory_geography_rows_or_csv"
  - "fusion_environment_context"
  - "project_id"
  - "task_context"
  - "execution_intent"
  - "execution_approval"
outputs:
  - "territory_geography_csv"
  - "territory_geography_validation"
  - "data_loader_handoff"
  - "data_loader_preflight"
  - "task_hook_preview_and_approval"
  - "data_load_initiation_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.sales.territories"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader.task-hook"
  - "core.project-mgmt.artifact-version-manager"
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
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/territories/manage-territory-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/territories/manage-territory-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/territories/manage-territory-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Territory Geography CSV and request validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Environment, approval, privilege, and import dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Live Import Management object metadata and content-account verification"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Native Data Loader routing defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "New-record intent, native execution, and immutable artifact enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure classification, disclosure, timeout, and retry rules"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status:
  source_alignment: "Current Oracle Territory Geography CSV guidance and core.data-loader CX Import contract"
  execution_contract: "Pillar prepares domain data; core.data-loader owns conversion, preflight, Task Hook, approval, Documents upload, and initiateDataLoad"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Oracle Fusion Cloud 26C or a compatible current release"
side_effects:
  - "Creates local CSV, validation, and Data Loader handoff artifacts."
  - "Reads declared Import Management metadata during Task Hook validation."
  - "Only core.data-loader uploads approved CSV members and initiates the CX data load."
required_privileges:
  - "Geography Administration duty (ORA_GEO_ADMIN_DUTY)"
  - "Fusion Data Loader CX Import metadata and initiation privileges"
  - "Documents upload access to the target-verified Territory Geography import account"
---

# Manage Territory Geographies

## Purpose

Prepare new territory geography hierarchies and hand them to
[Data Loader](../../../../../core/data-loader/SKILL.md) as CX Import data for
`GeoTerritoryInterface`. The task's catalog flags prohibit FSM setup imports;
they do not prohibit the separate CX Import route.

## Execution ownership

Core Data Loader is the sole upload and initiation route. Follow its current
SKILL.md and user-friendly output contract; do not use SOAP staging, direct
Import Activities submission, task-local transport callbacks, or a custom
`cxUploadContract` profile. The former task-local upload/report commands and
`finalize-preview` are retired and fail before any external action.

The pillar accepts new-record intent only. Do not promise server-enforced
`CREATE_ONLY`: the native Data Loader contract does not expose that setting.
If the request requires a server-enforced create-only mode, stop with a contract
gap before approval. Never inject ImportMode, Activate, Schedule, or a
server-issued content reference into the native initiation payload.

## Prepare source

Read [input validation](ora-resource/ora_input_validation.md) and use the local
helper. It writes CSV, local validation, and a non-authorizing Data Loader
handoff, without generating an import payload or approval.

```bash
python3 pillars/cx/sales/territories/manage-territory-geographies/scripts/territory_geography_import.py prepare \
  --records-json <rows.json> \
  --output-dir project/{project_id}/artifacts/pillars/cx/sales/territories/manage-territory-geographies/current/
```

Use `--input-csv` instead for an existing CSV; `template --output <file.csv>`
creates a header-only template. Existing artifacts require explicit overwrite
approval. `prepare --dry-run` validates without writing files.

The eleven-column base contract, optionally followed by `GeoParentName5`, is:

```text
GeographyOrZoneName,LanguageCode,SourceId,ParentSourceId,GeographyOrZoneType,ZoneCode,CountryName,GeoParentName1,GeoParentName2,GeoParentName3,GeoParentName4
```

Accept a JSON array or `records` array. Preserve names, language codes, numeric
identifier text, postal codes, and geography-parent paths. Require one first-row
root, unique unsigned Oracle Long SourceIds, and parents earlier in the file.
Country structures and master geography paths remain target prerequisites;
do not invent an exact-match check against `geoZones`.

## Data Loader and Task Hook sequence

1. Resolve the active project/Run Book and explicit environment through the
   implementation router. Read Data Loader and
   [Task Hook](../../../../../core/data-loader/task-hook/SKILL.md). A pending,
   failed, or unknown Run Book blocks submission.
2. Invoke ordinary CX preflight with the prepared CSV. Use the selected OAuth
   properties and Run Book configuration, rather than changing another
   environment's configuration. Core obtains live CX metadata and persists the
   immutable archive and preflight. Do not ask for approval yet.

```bash
python3 core/data-loader/scripts/upload_and_initiate.py <prepared.csv> \
  --cx-import --cx-import-object-code GeoTerritoryInterface --task-routed \
  --properties <selected-properties> --run-config <selected-run-config> \
  --preflight-envelope-output <internal-preflight.json>
```

3. Require `taskRouted=true`, `mappingComplete=true`, `sourceType=ORA_CX_IMPORT`,
   the exact object code, matching environment/Run Book, and an artifact digest
   matching the persisted archive. Immediately run Task Hook:

```bash
python3 core/data-loader/task-hook/scripts/task_hook.py data-load \
  --task-context <task-context.json> \
  --task-name "Manage Territory Geographies" --sequence <task-sequence>
```

4. Read its returned execution guide, registry, and reachable resources,
   including [error handling](ora-resource/ora_error_handling.md). Evaluate the
   non-write rules against the exact final archive and preflight, including the
   declared metadata GET. Registry `ready` means executable rules, not completed
   validation. Resolve the UCM account from live target metadata and require it
   to match core preflight; do not hardcode an account name. Record ordered
   evidence; block on any unresolved finding.
5. Call `build-data-load-preview --input-stdin` with `taskContextPath`,
   `taskName`, `sequence`, `finalData` containing the final `archiveSha256`, and
   ordered `ruleResults`. The registry's readiness gate checks validation and
   integrity, not prior approval: approval follows preview creation.
6. Return the normal Data Loader approval-required report only after all rules
   pass. A later contextual affirmative, or unambiguous same-request
   auto-approval wording accepted by core, authorizes that exact load. Then call
   `approve-data-load-preview --input-stdin`, followed by
   `verify-approved-data-load-archive --input-stdin --archive <final-archive>`.
   Persist its returned `taskValidationEnvelope` unchanged. Never reconstruct it.
7. Submit through the native approved-preflight path only:

```bash
python3 core/data-loader/scripts/upload_and_initiate.py \
  --approved-preflight-envelope <internal-preflight.json> \
  --task-validation-envelope <verified-task-envelope.json> --approve-upload \
  --properties <selected-properties> --run-config <selected-run-config>
```

Core reuses the immutable artifact, uploads its CSV members through Documents,
and invokes `initiateDataLoad` with `sourceType=ORA_CX_IMPORT` and
`cxImportObjectName=GeoTerritoryInterface`. It owns reference propagation and
optional Run Book parameters. Do not refresh metadata, rebuild files, or rerun
rules after approval. Pass `--cx-import-high-volume-load` during preflight only
when the user explicitly requested high-volume/bulk loading; it is not a default.

## Result and recovery

Redact secrets, tokens, authorization codes, protected payloads, and raw responses from project diagnostics as required by [error handling](ora-resource/ora_error_handling.md).

Return the helper's complete Markdown report verbatim. Accepted initiation is
terminal for the submission request; it is not proof that all rows loaded.
Do not automatically poll, query errors, repair Import Activities, or retrieve
reports. On an explicit status/results request use core Data Loader's
`get_data_load_info.py` and its declared monitoring contract.

Keep uncertain or partial uploads/initiation blocked until reconciled under a
supported workflow. Retain existing artifacts and checkpoints, including legacy
SOAP checkpoints; never clear them, edit a preflight profile, or create another
upload to bypass uncertainty. This correction does not provide a resume route
for previously staged SOAP documents or authorize their resubmission.

Persist local pillar preparation and failed routing evidence under the declared
project paths, record the durable skill run and token usage, and keep Data Loader
internal envelopes private. Core owns its initiation report and cleanup; do not
add auxiliary reports to its accepted-initiation response.

## Source guidance

Use current [Oracle Territory Geography import guidance](https://docs.oracle.com/en/cloud/saas/sales/faiem/import-your-territory-geographies-data.html)
and its [CSV example](https://docs.oracle.com/en/cloud/saas/customer-data-management/fageo/example-of-importing-territory-geography-data.html)
for domain fields. Native Data Loader transport, approval, and completion rules
are governed by core, rather than the separate Import Activities examples.
