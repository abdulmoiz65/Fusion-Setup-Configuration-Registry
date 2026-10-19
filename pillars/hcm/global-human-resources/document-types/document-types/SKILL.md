---
skill_id: "hcm.global-human-resources.document-types.document-types"
name: "Document Types Setup Task Guidance"
description: "Plans, validates, reads, and performs approved Oracle HCM Document Type and Document Type Delivery Preference changes, including deterministic PAYROLL hierarchy reconciliation."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Document Types"
functional_area_code: "ORA_DOCUMENT_TYPES"
task_code: "PER_DEFINE_DOCUMENT_TYPE"
task_name: "Document Types"
parent_skill_id: "hcm.global-human-resources.document-types"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "DocumentType"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM global human resources pillar team"
version: "0.4.0"
inputs:
  - "operation"
  - "environment"
  - "document_type_selector"
  - "document_type_values"
  - "delivery_preference_values"
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "normalized_scope"
  - "setup_task_plan"
  - "setup_data_routing"
  - "immutable_preview"
  - "execution_result"
  - "verification_result"
  - "diagnostics"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Validated for Data Loader DocumentType operations"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/document-types/document-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/document-types/document-types/current/"
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
  - "Reads Document Types, Delivery Preferences, countries, payroll statutory units, legal employers, and live API metadata from the selected Fusion environment."
  - "Authors validated Data Loader XLSX, DAT, ZIP, preview, diagnostic, and verification artifacts in the selected project workspace."
  - "After exact preview and standalone approval, core.data-loader may upload and initiate the approved Document Type load."
  - "After an exact REST preview and standalone approval, the task attachment adapter may POST a new file to an existing Document Type attachments child resource."
  - "After an exact REST preview and standalone approval, the task create adapter may POST a Document Type without HierarchyCode and then add its approved attachment."
required_privileges:
  - "View or Manage Document Types and Document Type Delivery Preferences, as required by the operation"
  - "HCM Data Loader upload and load privileges for Data Loader mutations"
  - "Access to the Document Types REST resource and required LOV resources"
---

# Document Types Setup Task Guidance

## Purpose

Read and manage Document Types and their Delivery Preferences using current
Fusion contracts, deterministic hierarchy reconciliation, immutable previews,
explicit approval, and post-mutation verification.

## Task Overview

Use this task to plan and govern `Document Types` configuration in Global Human Resources.

- **Task identity:** `PER_DEFINE_DOCUMENT_TYPE` — Document Types.
- **Scope:** HCM → Global Human Resources → Document Types.
- **Catalog routing:** CSV export/import support is `Y`; edits, deletes, Delivery Preferences, and creates that include Delivery Preferences use Core Data Loader with `DocumentType`. A create without Delivery Preferences uses the declared REST create route because HDL incorrectly requires `HierarchyCode` for its generated default preference. Existing-parent attachment adds use the declared REST attachment route.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_DEFINE_DOCUMENT_TYPE`
- task_name: `Document Types`
- parent_skill_id: `hcm.global-human-resources.document-types`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Document Types`
- functional_area_code: `ORA_DOCUMENT_TYPES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `DocumentType`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, reading, creating, editing, deleting, importing,
or validating Document Types or Document Type Delivery Preferences.

## Setup Task Metadata

- Task name: `Document Types`
- Task code: `PER_DEFINE_DOCUMENT_TYPE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `DocumentType`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import ordinary setup changes with `core.data-loader` using `Document Type` as the BusinessObject.

## Loader Workbook Authoring

`core.data-loader` is the sole owner of generating and populating the
reviewable `DocumentType.xlsx` workbook. This task skill supplies the reviewed
Document Type and Delivery Preference attribute mapping, validation rules, and
route selection; it must not create, modify, or provide a fallback writer for
XLSX workbooks.

- Provide the mapped values and rows to `core.data-loader`, which generates the
  live workbook and creates the immutable ZIP preview.
- Validate the generated workbook with `core.data-loader` before upload and
  initiation.
- Never treat local spreadsheet preparation, schema validation, archive
  creation, or approval-preview generation as approval for a Fusion mutation.
  The task still requires the exact immutable preview and the existing
  standalone approval gate immediately before upload and initiation.

## CRUD and Reference Routing

### Live-State Preflight

Before every create, edit, delete, retry, or reconciliation, query the selected
Fusion environment for the exact current business key. Earlier run records,
approved archives, local workbooks, and prior chat results are not evidence of
current Fusion state.

- For a create request, zero exact current matches means the create path is
  available. Do not stop or ask about a record merely because a prior artifact
  says it was created; a user may have deleted it manually.
- For an edit or delete request, require one exact current match and use only
  the ID freshly resolved for that run.
- If the live state differs from prior artifacts, rebuild the source and preview
  from the live state without treating the difference as a user-input gap.

- Read Document Types only through `hrDocumentTypes`. Resolve and search the `DocumentType` attribute: support exact-name resolution and explicit `q=DocumentType like '%term%'` searches using the caller-supplied term; do not query the unsupported `Name` attribute. For a single resolved match, use its item read for full functional details.
- For a file attachment on a Document Type, populate the live `DocumentTypeAttachment` child section. Set `DataTypeCode=FILE`, set `File` to the exact safe basename supplied to Core Data Loader with `--blob-file`, preserve the requested `FileName` and `Title`, and set the MIME type resolved from the actual file (for example, `image/png`). Use the parent keys exposed by the current live template; on edit, resolve the exact current parent and any targeted attachment before authoring the child row. Core Data Loader packages the referenced file as `BlobFiles/<basename>` and blocks missing, orphaned, unsafe, empty, or unreferenced attachment members. Never place a PNG, PDF, or other attachment at the ZIP root.
- `HierarchyCode` is not an intake requirement for Document Type creation. For a create with no explicitly requested Delivery Preferences, do not ask for, default, infer, or require `GENERAL` or `PAYROLL`. Route the parent through `scripts/document_type_create.py`, whose exact parent payload contains only reviewed business fields and omits `HierarchyCode`. Hierarchy validation applies only when Delivery Preferences are part of the requested operation.
- Before previewing that REST create, require the live `hrDocumentTypes/describe` contract to advertise collection `create` by `POST`, require `DocumentType` and `CategoryCode`, and mark `HierarchyCode` nonmandatory. Re-read the exact name and require zero current matches. If a file is requested, validate the nested attachment create contract and bind the file bytes, MIME type, parent payload, child payload, adapter, target environment, and all fingerprints into one immutable preview.
- Before adding a new file attachment to an existing Document Type, inspect both contracts. If HDL exposes only the system-generated mandatory `AttachedDocumentId`, do not author a child MERGE. Require the live `hrDocumentTypes/{id}/child/attachments/describe` contract to advertise collection `create` by `POST`, `FileContents` as an attachment, and a generated `AttachedDocumentId`; then route through `scripts/document_type_attachment.py`. Do not ask the user for `AttachedDocumentId`, reuse another ID, or treat `Title` or `FileName` as an HDL key. An existing attachment replacement remains a separate operation and requires one exact attachment and its current ID.
- Read Document Type Delivery Preferences only through `hrDocumentTypes/{id}/child/documentDeliveryPreference`, after resolving the parent Document Type ID.
- Before authoring a Delivery Preferences mutation, read the exact parent item and preserve its nonblank current `HierarchyCode` on the root `DocumentType` source row. Never infer or hard-code the hierarchy, and block preview if it is unavailable.
- Resolve a supplied delivery-preference country through `hcmCountriesLov`. When live loader metadata exposes `Country`, write the current `CountryName` display value (for example, `United States`); write the territory code (for example, `US`) only when the exact live attribute is `LegislationCode`. Never place a territory code in `Country`.
- Resolve a supplied payroll statutory unit through `payrollStatutoryUnitsLOV` with `findByWord`. Compare `PayrollStatutoryUnitName` to the caller value after trimming both values and require exactly one current exact match. Preserve the exact returned text, including significant surrounding whitespace, and the current `OrganizationId`. On a Data Loader anchor row, use canonical `PayrollStatutoryUnitName` and leave `PsuId` blank; Data Loader Department or Location rows use numeric `PsuId` with blank name.
- Treat a Department or Location preference as a hierarchy pair, not a standalone row. For a `PAYROLL` parent, author the `Payroll Statutory Unit` anchor row plus each requested lower-level row. For a `GENERAL` parent, author the `Legal Employer` anchor row plus each requested lower-level row. Use the canonical organization name on the anchor and the resolved numeric organization ID on lower-level rows. On reconciliation after a partial or successful prior load, read current preferences and author only missing or explicitly changed rows; do not duplicate an existing anchor or lower-level row. For a Location child, use the current returned `LevelCode`, organization identity, and `LevelId` equal to the resolved Location ID as the live business identity. A null returned `LocationId` does not mean the row is absent when those fields and `LocationName` match.
- For an existing Delivery Preference mode-only edit, require exactly one current matching child and use its freshly read `DocumentDeliveryPreferenceId`. Preserve every unrequested mode from that row, include only the explicitly changed child in the mutation source, and leave an unchanged hierarchy anchor out of the edit package.
- Source keys are technical execution identity, not business input. Never ask the user to supply them. For a Data Loader create that genuinely requires a child source key, generate a deterministic collision-checked pair and keep it scoped to the new child. Never copy source keys from another row or place child keys on the existing parent.
- Select the route during reconciliation, before building an artifact. Use the declared REST parent-create route for a Document Type create without Delivery Preferences. Use Data Loader for edits, deletes, Delivery Preferences, and creates that include Delivery Preferences. Use the declared REST child-create route to add a new file attachment to an existing Document Type. If no declared contract can represent the operation, stop with a catalog mismatch.
- If a user asks to create, edit, or delete a Document Type or Document Type Delivery Preferences, invoke this task and follow the compiled graph. `DOCT.LOADER_READY` routes through `core.data-loader`.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. For Data Loader, keep control until an immutable ZIP preview exists. For REST create or attachment add, create an immutable preview containing environment, exact business identity, fields, attachment metadata, file SHA-256, payload SHA-256, endpoint, adapter fingerprint, and live-contract evidence. Present the exact operation and preview fingerprint, then wait for standalone `approve`.
- Execute an approved hierarchy-free create with `scripts/document_type_create.py execute`. It must re-prove absence, revalidate the live parent and attachment contracts, verify all fingerprints, create the parent once without `HierarchyCode`, add the approved attachment, and verify both through fresh bounded reads. If the parent succeeds and the attachment fails, persist a partial result and stop without retrying or deleting the parent.
- Execute an approved existing-parent attachment preview with `scripts/document_type_attachment.py execute`. It must re-resolve the exact parent, revalidate the live describe contract, reject a same-name attachment, verify the file and payload fingerprints, and only then invoke `core.fusion-api.rest-api-client`. Verify the new child with a fresh bounded read. Never reuse approval after any target, contract, file, or payload change.
- Never use browser automation, an undeclared direct REST write, FSM import, or another utility as a fallback for an undeclared or failed Data Loader route.
- For reads, use bounded paging and resolve a zero, one, or many-match outcome only after all required pages are evaluated.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Document Types`
- Setup task name: `Document Types`
- Setup task code: `PER_DEFINE_DOCUMENT_TYPE`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `operation`
- `environment`
- `document_type_selector`
- `document_type_values`
- `delivery_preference_values`

## Outputs

- `normalized_scope`
- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `immutable_preview`
- `execution_result`
- `verification_result`
- `diagnostics`

## Implementation Notes

Use the parent functional-area skill `hcm.global-human-resources.document-types` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Failure and Redaction

Classify failures using the task-local error guidance, preserve only the
required sanitized diagnostics, and stop before retry or route substitution.
Never print or persist credentials, tokens, token caches, secrets, full payloads,
or sensitive customer data.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)
