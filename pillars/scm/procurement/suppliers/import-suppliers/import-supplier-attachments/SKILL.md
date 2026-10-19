---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-attachments"
name: "Import Supplier Attachments"
description: "Prepares and submits Supplier Attachment FBDI packages through the registered Supplier Attachment Data Loader business object."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Attachments"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Attachment"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs: ["supplier_attachment_source_data_or_fbdi_package", "target_environment", "optional_batch_id", "project_context", "execution_approval"]
outputs: ["supplier_attachment_fbdi_package", "package_validation_result", "import_preview", "data_loader_execution_result", "load_status_and_errors", "skill_run_record", "token_usage_record"]
depends_on: ["scm.procurement.suppliers.import-suppliers", "core.data-loader"]
uses_core: ["core.data-loader", "core.project-mgmt.artifact-version-manager", "core.project-mgmt.artifact-registry-manager", "core.project-mgmt.project-state-manager"]
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
state_updates: ["configuration_blueprints", "reports", "token_usage_records"]
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-attachments/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-attachments/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Attachment FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, the import can add or update supplier attachment metadata and linked content."
required_privileges: ["Access to the selected Fusion environment through the configured Data Loader connection."]
---

# Import Supplier Attachments

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filenames

`PozSupAttachmentsInt.csv` for Supplier attachments,
`PozSupSiteAttachmentsInt.csv` for Site attachments, and
`PozSupBusClassAttachmentsInt.csv` for Business Classification attachments.
Populate only the requested levels. Apply the parent's
[filename-hint rules](../SKILL.md#fbdi-registration-selection).
These CSV members are separate from the attachment-content ZIP below.

## Purpose

Prepare and execute only an approved Supplier Attachment FBDI package against
the selected Fusion environment.

Use Core's resolved FBDI registration for the requested Supplier Attachments
import. Prepare, validate, preview, submit, and monitor only
through `core.data-loader`; do not submit ESS, upload to UCM, or modify
interface/rejection tables directly.

## Preflight

Before any Fusion-changing action, confirm the target environment, Data Loader
session and access, live registration contract, source/package structure,
required supplier references, optional batch scope, and whether the run is
preview or live. Stop before preview for an invalid package or unresolved
business input.

## Failure Handling and Data Protection

Classify invalid source data, package structure, or missing business input as
`input_validation`; do not submit. Classify a missing or changed Data Loader
contract as `catalog_or_metadata_mismatch`; stop rather than guessing job
mappings, tables, or argument positions. For authentication, authorization,
transport, or Fusion failures, retain only redacted diagnostics and the request
identifier; do not retry a live import without a corrected immutable
replacement package and new approval. On monitoring timeout, preserve the last
status and request ID and ask whether to resume monitoring. Never persist or
display credentials, tokens, token caches, private keys, attachment content,
full source rows, or full package/base64 content.

## Preparation

1. Download the current Supplier Attachment FBDI template for the target
   release and preserve its headers, member naming, attachment references, and
   content conventions exactly.
2. For File-type attachments, prepare a separate attachment-content ZIP and
   ensure it is uploaded to UCM account `prc/supplier/import` in the target
   environment before the import runs. Reuse an already uploaded ZIP when
   applicable. In each FBDI row, `File Attachments .ZIP` must match the uploaded
   ZIP filename and `File/Text/URL` must match the complete internal file path
   (for example, `Policies.zip` and `SupplierPolicies/Terms.pdf`). Text and URL
   attachments do not require an attachment-content ZIP.
3. Use a supported Core upload workflow with its approval gates. If none is
   available for the content ZIP, explain the manual UCM-upload prerequisite
   and obtain confirmation that it is complete before submitting the import;
   do not implement a Supplier-side upload or assume the FBDI upload stages the
   attachment files.
4. Build the separate FBDI CSV ZIP for only the requested attachment rows. Use
   the registration's file prefixes and optional `BATCH_ID` scope; never add
   load/request/status fields. Do not merge the content ZIP into the CSV ZIP
   unless the supported live contract explicitly requires it.
5. Read live registration metadata and validate the immutable FBDI ZIP before any
   approval. Attachment content, references, and parent supplier identity must
   be complete and internally consistent.

See Oracle's [Supplier Attachment import requirements](https://docs.oracle.com/en/cloud/saas/procurement/26c/oapro/create-suppliers-with-the-import-suppliers-process.html).

## Entity Dependency

Attachments aren't part of the default Supplier dependency sequence. When they
are explicitly requested, import them only after the referenced Supplier,
Supplier Site, or Business Classification has been processed successfully.
Confirm the applicable prerequisite with the user before live submission; do
not block package preparation when they confirm the referenced record exists.

## Execution

Use Core's final preview and approval under the parent's workflow rules, then
submit the retained package through Core's approved-artifact workflow. When status is requested,
use the registration's observability contract through Core for row errors.

Reconcile uncertain results before retrying. For rejected rows, correct only
the source rows, rebuild the ZIP, and request replacement approval.
