---
skill_id: "cx.sales.accounts-and-contacts.manage-oracle-data-as-a-service-attribute-mapping-and-preferences"
name: "Manage Oracle Data as a Service Attribute Mapping and Preferences"
description: "Exports, prepares, validates, and imports selected Oracle Data as a Service attribute-mapping or enrichment-preference rows through the task-level FSM CSV workflow. Use when users need to change existing seeded rows for ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES; refuse new rows, deletions, whole-baseline imports, and execution outside the approved FSM route."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Accounts and Contacts"
functional_area_code: "ORA_SVC_ACCOUNTS_AND_CONTACTS"
task_code: "ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES"
task_name: "Manage Oracle Data as a Service Attribute Mapping and Preferences"
parent_skill_id: "cx.sales.accounts-and-contacts"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.3.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "operation"
  - "row_changes"
  - "fresh_setup_task_export"
  - "fresh_target_attribute_metadata"
outputs:
  - "setup_task_export_result"
  - "selected_row_change_preview"
  - "fusion_attribute_validation_result"
  - "prepared_setup_data_zip"
  - "setup_data_validation_result"
  - "data_loader_approval_preview"
  - "setup_data_import_result"
  - "post_import_verification_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/exports/sales/accounts-and-contacts/manage-oracle-data-as-a-service-attribute-mapping-and-preferences/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/accounts-and-contacts/manage-oracle-data-as-a-service-attribute-mapping-and-preferences/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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
  - "Creates a task-level FSM export process when approved and writes export artifacts to the project workspace."
  - "Reads target-environment Fusion object metadata when a requested change includes FusionObjectName or FusionAttributeName."
  - "Writes a selected-row FSM import ZIP and immutable preview to the project workspace."
  - "Submits one approved task-level FSM import through core.data-loader and polls the returned process identifier."
required_privileges:
  - "Fusion privileges appropriate to export and import setup task CSV data"
  - "Fusion privileges to read Sales object metadata"
---

# Manage Oracle Data as a Service Attribute Mapping and Preferences

## Purpose

Change only explicitly requested existing rows for task
`ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES`. A normal FSM export can omit
unchanged seeded rows, so this skill uses the sanitized complete seeded-row
catalog in `assets/seeded-attribute-mappings.csv` as a fallback row source.

## Supported Operations

- Export the current task package from one selected Fusion environment.
- Prepare one or more selected existing rows for import.
- Validate and preview the exact selected-row ZIP.
- Import the approved ZIP through `core.data-loader` in FSM mode.
- Resume status polling for an already captured process identifier.
- Re-export and verify the requested fields after import.

Do not create rows, delete rows, reset the complete task, or import the complete
seeded catalog.

## Selected-Row Contract

1. Identify a row with the exact composite key `AttributeCategory` plus
   `DaasAttributeName`. Require exactly one match in the complete seeded catalog.
2. Accept changes only for `AutofillBlank`, `AutoupdateNonBlank`,
   `FusionObjectName`, and `FusionAttributeName`. The two preference flags accept
   only `Y` or `N`. When either mapping field changes, require fresh target-pod
   object metadata and validate the effective `FusionObjectName` and nonblank
   `FusionAttributeName` by exact case-sensitive `AttributeCode` match.
3. Export the current task before package preparation. For each selected row and
   CSV member, preserve the current exported row when present; otherwise copy
   the row from the complete seeded catalog. Apply only the requested fields.
4. Write only selected rows to both Oracle members:
   `ORA_ZCM_DATA_CLOUD_ENRICH_PREFERENCE.csv` and
   `ORA_ZCM_DATA_CLOUD_MAPPING_PREFERENCE.csv`. Preserve the fresh export's
   member names, per-member header order, metadata, and ZIP structure.
5. Reject a request when the two member schemas differ from the catalog, a key
   is missing or duplicated, a requested field is outside the allowlist, live
   attribute metadata is missing or incomplete, or an effective object/attribute
   pair is invalid.

The import changes only rows present in the prepared CSV members. Do not add
unrequested rows as a precaution and do not infer deletion from omitted rows.

## Friendly Preference Questions

Ask about preferences using the labels shown in **Manage Enrichment Preferences
and Attribute Mapping for Oracle Data as a Service**. Do not lead with CSV
column names or `Y`/`N` unless the user asks for the technical representation.

| UI label to use with the user | How to ask | FSM field/value |
|---|---|---|
| **Don't Apply Blank Values** | “Should **Don't Apply Blank Values** be on or off for this attribute?” | `AutofillBlank`: on = `Y`; off = `N` |
| **Don't Overwrite** | “Should **Don't Overwrite** be on or off for this attribute?” | `AutoupdateNonBlank`: on = `N`; off = `Y` |

For example, normalize “leave existing values unchanged” to **Don't Overwrite:
on** (`AutoupdateNonBlank=N`), and normalize “allow enrichment to overwrite
existing values” to **Don't Overwrite: off** (`AutoupdateNonBlank=Y`). Repeat
the readable label and its on/off value in the selected-row and approval
previews; include the technical field/value only as supporting detail.

**Display During Real-time Enrichment** is a distinct UI checkbox. It is not
one of the four editable fields in this selected-row FSM package. When a user
asks to change it, clearly explain that this package cannot perform that change,
do not translate it to either preference flag, and keep it out of the import
change document. Offer the task's UI/manual configuration route as the separate
next action.

## Workflow

1. Resolve or create the implementation project through the implementation
   router and select the exact source/target environment.
2. Route a fresh unfiltered task export through
   `shared.setup-export.task-level-export` using task code
   `ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES`. Persist its `ProcessId`, status,
   ZIP, and SHA-256.
3. Normalize the user's requested rows into a JSON change document:

   ```json
   {
     "changes": [
       {
         "AttributeCategory": "ACCOUNT_CONFIG_B",
         "DaasAttributeName": "Account/Industry",
         "set": {"AutofillBlank": "N"}
       }
     ]
   }
   ```

4. When a change includes `FusionObjectName` or `FusionAttributeName`, resolve
   the effective object name from the fresh-export row or seeded fallback plus
   the requested changes. For every distinct nonblank effective object, route a
   read-only GET through `core.fusion-api.rest-api-client`:

   ```text
   /crmRestApi/resources/11.13.18.05/objectMetadata/{FusionObjectName}/child/attributes
   ```

   Request `fields=AttributeCode`, `limit=1000`, `offset=0`, `onlyData=true`,
   and `totalResults=true`. Require `hasMore=false` and
   `count=totalResults=items.length`; otherwise stop instead of validating a
   partial catalog. Keep raw responses in a temporary local location and retain
   only their hashes, counts, requested-pair results, and sanitized target
   identity in the project preview.
5. Build the selected-row package locally. Supply one fresh response for every
   effective object used by a mapping change:

   ```bash
   python3 pillars/cx/sales/accounts-and-contacts/manage-oracle-data-as-a-service-attribute-mapping-and-preferences/scripts/prepare_daas_attribute_mapping_import.py \
     --export-zip "{fresh_export_zip}" \
     --changes "{changes_json}" \
     --fusion-attributes "Account={temporary_account_attributes_json}" \
     --target-environment "{sanitized_target_environment}" \
     --output-zip "{prepared_import_zip}" \
     --preview "{selected_row_preview_json}"
   ```

   Omit the two metadata arguments only when no requested change includes either
   mapping field. An empty `FusionAttributeName` is an explicit unmapping and is
   allowed; a nonblank attribute requires a nonblank, metadata-resolved object.
6. Validate that the preview lists only the requested keys, the correct before
   and after values, exact object/attribute validation evidence when applicable,
   the two CSV members, and the final ZIP SHA-256.
7. Route the immutable ZIP to `core.data-loader` with
   `dataloader_import_mode=FSM`, the exact task context, target environment,
   validation evidence, and archive SHA-256. Data Loader owns the import
   approval preview and the single approval gate.
8. After approval, submit once, capture the returned process identifier, and
   poll only that process. Do not replay an uncertain or timed-out import.
9. Re-export the task and compare the requested fields for each selected key.
   Persist a verification result without importing again.

## Project Artifacts

Keep the source export, normalized changes, selected-row preview, prepared ZIP,
SHA-256, Data Loader approval envelope, import status/log, verification result,
skill-run record, and token-usage record under `project/{project_id}`. Never
persist credentials, token caches, authorization headers, or the raw attached
source archive's environment-specific metadata.

## Failure and Retry Boundary

Use the task-local `ora-resource` rules for validation, dependency readiness,
design enforcement, approval, and errors. Refresh a cache-managed token once
only when the routed workflow permits it. Never retry an export or import POST
automatically. On timeout, report the same task code, process identifier, last
status, elapsed time, diagnostic path, and status-only continuation.

## Preflight and Redaction

Before any external operation, preflight the operation, exact environment,
privileges, task/catalog flags, source paths, fresh-export ZIP, metadata task
binding, CSV schemas, selected row keys, requested fields, complete live
attribute metadata for mapping changes, destination paths, validation evidence,
and approval requirements. Stop before side effects when any check is missing,
ambiguous, unsupported, or unsafe.

Redact credentials, tokens, authorization headers, opaque protected URLs,
customer data, raw Base64 file content, and environment-specific source
metadata from console output, previews, diagnostics, and durable artifacts.
Persist only the sanitized identifiers and evidence required to resume or audit
the declared workflow.

## Sources

- `assets/seeded-attribute-mappings.json`
- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `shared/setup-export/task-level-export/SKILL.md`
- `core/fusion-api/rest-api-client/SKILL.md`
- `core/data-loader/SKILL.md`
- https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html
- https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-imports.html
- https://docs.oracle.com/en/cloud/saas/sales/fadsi/add-fields-to-the-mapping.html
- https://docs.oracle.com/en/cloud/saas/customer-data-management/fagcd/configure-enrichment-preferences.html
- https://docs.oracle.com/en/cloud/saas/sales/faaps/api-object-metadata-attributes.html
