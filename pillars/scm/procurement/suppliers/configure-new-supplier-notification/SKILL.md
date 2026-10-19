---
skill_id: "scm.procurement.suppliers.configure-new-supplier-notification"
name: "Configure New Supplier Notification Setup Task Guidance"
description: "Configures supplier notification enablement, GLOBAL email content, country document rows, and approved file attachments using Data Loader and a task-specific REST adapter."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "ORA_POZ_CONFIGURE_NEW_SUPPLIER_NOTIFICATION"
task_name: "Configure New Supplier Notification"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "supplierOptions"
  - "newSupplierNotification"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "SCM procurement pillar team"
version: "0.2.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input and attachment validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Current notification and attachment contracts"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Approval, verification, and recovery"
    location: "ora-resource/ora_error_handling.md"
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-new-supplier-notification/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-new-supplier-notification/current/"
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
  - "Reads notification settings, country document rows, attachment contracts, and country references from the selected Fusion environment."
  - "Creates local Data Loader workbooks, attachment approval previews, and execution/verification records."
  - "After Core Data Loader approval, may update notification settings or perform standalone country-row configuration."
  - "After approval of the requested document changes, the task-specific REST adapter may create a missing non-GLOBAL country row and upload its reviewed files; existing rows are reused."
required_privileges:
  - "Access to view and manage Supplier Notification configuration and attachments, as required by the operation."
  - "Data Loader upload and load privileges for ordinary configuration changes."
  - "REST create privileges for country document rows and their attachment child resources when the combined operation is requested."
  - "Access to the notification REST resources and required country references."
---

# Configure New Supplier Notification Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure New Supplier Notification` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `ORA_POZ_CONFIGURE_NEW_SUPPLIER_NOTIFICATION`
- task_name: `Configure New Supplier Notification`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `supplierOptions`, `newSupplierNotification`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and Fusion Data Loader samples are needed for this task's business objects.

1. Confirm that `supplierOptions` and `newSupplierNotification` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
    "supplierOptions" \
    "newSupplierNotification" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Supplied Task Inputs

Apply [Supplier input reuse](../SKILL.md#reuse-supplied-supplier-inputs).
Reuse supplied values and source references; distinguish requested changes from
current-state exports/examples. Ask one concise question only for unresolved
in-scope decisions:

- Content: notification enablement, GLOBAL Email Subject, and GLOBAL Email Body,
  only when that setting is being changed.
- Documents: operation and country-to-file assignments. Resolve supplied country
  names/codes through the live reference; never infer GLOBAL or a file's country.
  Default an omitted title to the filename. Comments are optional: preserve
  existing comments and omit them on a new row unless supplied.

Do not ask for generated IDs, files on a content-only request, or email changes
on an attachment-only request. Read current values and identities through the
task's lookups; label them Current value, not defaults, or unverified if unavailable.
Before the selected route's approval gate, summarize current versus requested
values, source references, and preserved settings. Input confirmation is not
execution approval; do not duplicate the route's approval gate.

## Notification Content and Country Scope

Email Subject and Email Body are configured on the GLOBAL notification.
Country-specific document configuration covers Tax Country, User Comments,
and Attachments, not email overrides. GLOBAL cannot be deleted or reassigned.
Verify requested fields and operations against current metadata; this scope
does not establish writability for every country.

Subject (maximum 255 characters) and rich-text Body are required when enabled;
existing valid content can satisfy this without resubmission. Disabled
notification permits empty content. Preserve all unrequested fields/documents.
Blank or omitted values normally mean Preserve, not false or Clear; ask only
if a missing decision is necessary for the requested change.

For an explicit clear or blank-value negative test, retain that intent instead
of silently preserving. Email Body clearing uses an explicit null at the
notification service, but Data Loader clearing semantics remain unverified.
Verify the selected transport before translating blanks/nulls or using a clear
marker. If unsupported, report the gap; do not invent a marker or bypass Data
Loader through direct REST.

## FSM Export Header Mapping

Use explicit mappings for supplied task-export CSVs rather than fuzzy matching.
Confirm target attributes and value types against the selected environment's
current loader metadata before preparing a supported Core input. These mappings
do not make the unchanged export files native loader inputs.

For multiple task-export CSVs, prepare a separate supported XLSX workbook for
each registered business object using these mappings and live loader metadata.
Submit the workbooks together through Core Data Loader, not multiple CSVs as
combined session inputs. Preserve source values and intentional blank-value
tests; format conversion does not establish clearing semantics. Distinguish an
unsupported input combination from malformed CSV content.

| Export file | CSV header | Target attribute or handling |
|---|---|---|
| `ORA_POZ_ENABLE_NEW_SUPPLIER_NOTIFICATION.csv` | `SupplierOptionsCode` | Seeded export identity `ORA_POZ_SUPPLIER_OPTIONS_CODE`; resolve `SupplierOptionsConfigId`, never copy the text into its numeric key. Clarify unknown identities. |
| `ORA_POZ_ENABLE_NEW_SUPPLIER_NOTIFICATION.csv` | `EnableNewSuppNotification` | `EnableNewSupplierNotificationFlag`; interpret Y/N as Yes/No and serialize using live loader metadata. |
| `ORA_POZ_NEW_SUPPLIER_NOTIFICATION.csv` | `ConfigCountryCode` | `TaxCountryCode`; resolve the selected country's existing `NewSupplierNotificationId`, or follow the missing-country create flow. GLOBAL is required for email content, not for every document row. Resolve display names to country codes; neither is a numeric key. |
| `ORA_POZ_NEW_SUPPLIER_NOTIFICATION.csv` | `EmailBody` | GLOBAL `EmailBody`; preserve exact supplied rich text. |
| `ORA_POZ_NEW_SUPPLIER_NOTIFICATION.csv` | `EmailSubject` | GLOBAL `EmailSubject`; preserve exact supplied content. |
| `ORA_POZ_NEW_SUPPLIER_NOTIFICATION.csv` | `UserComments` | Selected document row's `UserComments`; require live field/operation support, do not discard populated comments or turn an attachment-only add into a parent update. |

Unknown headers, conflicting aliases, unresolved identities, unsupported
nonblank values, or country-specific content requests require clarification or
a contract blocker before preparation. The notification export has no binary
attachment column: a separately supplied file is a document-operation input,
not a value to insert into an ordinary CSV string field. Use the declared
attachment route below. After completion, compare requested values with fresh
reads; an accepted load alone does not prove they were applied.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure New Supplier Notification` under `Suppliers`.

## Setup Task Metadata

- Task name: `Configure New Supplier Notification`
- Task code: `ORA_POZ_CONFIGURE_NEW_SUPPLIER_NOTIFICATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects, in loader order: `supplierOptions`, `newSupplierNotification`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `supplierOptions` and `newSupplierNotification` as the business objects.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Configure New Supplier Notification`
- Setup task code: `ORA_POZ_CONFIGURE_NEW_SUPPLIER_NOTIFICATION`

## Shared Business-Object Boundaries

This task changes two distinct business objects.

| Business Object | This Task May Change | Shared-Object Rule |
|---|---|---|
| `supplierOptions` | `EnableNewSupplierNotificationFlag` | This is the seeded singleton shared with Configure Supplier Registration, Configure Supplier Profile Change Request, and Configure Supplier Notifications. Resolve exactly one current row, execute shared-row tasks serially, re-read after an earlier shared task succeeds, and include only this task's flag in its Data Loader artifact. |
| `newSupplierNotification` | GLOBAL `EmailSubject` and `EmailBody`; requested document-row `TaxCountryCode` and `UserComments` only under an established live operation contract; supporting documents through its declared `attachments` child route | Resolve the single GLOBAL notification for content or GLOBAL attachment changes. For country attachments resolve that country's existing document row independently; never fall back to GLOBAL. Do not include `supplierOptions` fields in this artifact. Preserve unrequested content and existing attachments. |

Ordinary configuration changes use `core.data-loader`. Country documents use
the task-local combined REST adapter through unchanged Core OAuth and REST
primitives, following HCM's parent-create-plus-attachment pattern. Run Book task
attachments remain a separate `core.runbook` operation.

## Combined Country Documents Execution

Read the [input rules](ora-resource/ora_input_validation.md),
[lookups](ora-resource/ora_reference_lookups.md), and
[approval/recovery rules](ora-resource/ora_error_handling.md). Treat a country's
document row and requested files as one business operation. Ask the user to
**review and approve the requested changes**, without emphasizing approval counts.

Invoke Core's `fusion_rest_client.py` for every request, following the HCM
attachment pattern. Core alone reads environment properties and handles OAuth,
tokens, destination authorization, and HTTP. The optional `--properties` value is
an opaque path passed to Core; omit it to use Core's configured default. Never
open, parse, hash, or cache that properties file in Supplier code. The host uses
Core's selected environment when presenting approval. The adapter binds only
the selected Core CLI/profile path, not the file's contents or a cross-request
environment snapshot; stable target binding across separate CLI calls remains
a Core execution-context limitation, not a Supplier-side guarantee.

1. **Resolve and preflight.** Invoke
   [supplier_notification_documents.py](scripts/supplier_notification_documents.py)
   `preview` with `--country`, repeated `--file`, optional matching `--title`
   values, optional new-row `--comments` and Core `--properties` path, and a new `--output`.
   Validate the country through live `territoriesLOV`; GLOBAL needs no territory
   lookup. Reuse exactly one existing row. Multiple matches block; zero matches
   select creation only for a non-GLOBAL country. Never fall back to GLOBAL or
   create a missing GLOBAL row.
2. **Validate both contracts and all files before approval.** For a missing
   country, require collection POST create, generated `NewSupplierNotificationId`,
   and create-capable `TaxCountryCode`/optional `UserComments`. The parent
   payload contains only those document-row fields—no GLOBAL email content,
   enablement, or generated keys. Validate the nested attachment create contract
   before the parent exists: POST create, attachment-typed `FileContents`, and
   generated `AttachedDocumentId`. Existing rows use their live child describe.
   Require readable nonempty regular files, safe unique filenames, MIME types,
   titles, and no conflicting existing attachments across all required pages.
   Default category to `TO_SUPPLIER` and entity scope to `POZ_NEW_SUPP_DOC_CONFIG`;
   do not ask the user to supply or confirm either. Use the existing child
   describe to confirm writable `CategoryName`, then explicitly send the default.
   The exact notification attachment-child endpoint binds the entity. Do not add
   a separate category/entity lookup or approval, or invent an `EntityName`
   upload field. Reject conflicting entity values only when already exposed by
   the existing contract or verification response.
3. **Review the requested changes.** Use the Core/orchestration environment
   context; display country, create-or-reuse decision, parent fields, and every
   file/title/type/size. Bind the selected Core route, parent identity or proven
   absence, ordered operations, file/payload hashes, live contracts,
   preserved content, and executor fingerprint into the immutable preview.
   Display its fingerprint, not binary/base64, and obtain approval covering the
   entire operation. No intermediate approval is needed for its already reviewed
   uploads. Ordinary configuration or earlier previews do not authorize it.
4. **Execute the approved flow once.** Invoke `execute` with `--preview`,
   `--approved-preview-sha256`, and `--properties`. Revalidate all files,
   contracts, country identity/absence, duplicates, and fingerprints before the
   first write. Changed state requires a fresh preview and approval. Create the
   missing country row once, resolve its generated identity, and revalidate its
   child contract; then upload the approved files sequentially without an
   asynchronous Data Loader handoff. Existing rows receive child POSTs only.
   The adapter journals dispatch to prevent replay; no mutation is retried.
5. **Verify and report the business outcome.** Confirm country identity/fields,
   every uploaded filename/title, and preservation of GLOBAL email content,
   existing documents, and unrequested values. Compare downloaded bytes with
   approved hashes when supported; otherwise report metadata-only verification.
   Use the existing verification read to confirm `CategoryName = TO_SUPPLIER`
   and, when exposed, `EntityName = POZ_NEW_SUPP_DOC_CONFIG`. A missing or incorrect
   category, or conflicting entity, requires reconciliation, not replay.
   Parent creation alone is not completion. On failure, stop the batch and
   report the parent and each file independently, retaining successful work.
   Follow the error reference for reconciliation; never recreate, roll back,
   or automatically resend completed operations.

The existing-parent-only
[supplier_notification_attachment.py](scripts/supplier_notification_attachment.py)
remains available for an explicitly selected attachment-only operation, but
cannot create a country row. Do not mix approvals between the two adapters.
Replacement/deletion and existing-row comment changes remain separate supported
configuration operations, not implicit parts of an add.

The product limit is **10 MB combined attachments per country**, including
retained files. Treat it as guidance, not a mandatory local aggregate-size gate;
unknown retained sizes alone do not block preparation. Report a Fusion size-limit
rejection without automatic retry.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.procurement.suppliers` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

Never print or persist credentials, tokens, token caches, private keys,
binary/base64 file contents, or full sensitive payloads in previews or diagnostics.
Record only sanitized execution evidence in the project workspace.

- [Input validation](ora-resource/ora_input_validation.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Error handling](ora-resource/ora_error_handling.md)
