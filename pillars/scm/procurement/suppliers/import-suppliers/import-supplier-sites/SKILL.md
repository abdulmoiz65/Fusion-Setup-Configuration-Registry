---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-sites"
name: "Import Supplier Sites"
description: "Prepares and submits Supplier Site FBDI packages through the registered Supplier Site Data Loader business object."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Sites"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Site"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs: ["supplier_site_source_data_or_fbdi_package", "target_environment", "optional_batch_id", "project_context", "execution_approval"]
outputs: ["supplier_site_fbdi_package", "package_validation_result", "import_preview", "data_loader_execution_result", "load_status_and_errors", "skill_run_record", "token_usage_record"]
depends_on: ["scm.procurement.suppliers.import-suppliers", "scm.procurement.suppliers.import-suppliers.import-supplier-addresses", "core.data-loader"]
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-sites/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-sites/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Site FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, the import can create or update supplier sites and any companion records intentionally included in the approved package."
required_privileges: ["Access to the selected Fusion environment through the configured Data Loader connection."]
---

# Import Supplier Sites

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filenames

`PozSupplierSitesInt.csv`; `PozSupThirdPartyInt.csv` for third-party payment
relationships when requested. Apply the parent's
[filename-hint rules](../SKILL.md#fbdi-registration-selection).

## Purpose

Prepare and execute only an approved Supplier Site FBDI package against the
selected Fusion environment.

Use Core's resolved FBDI registration for the requested Supplier Sites import.
Route validation, upload, submission, and monitoring through `core.data-loader`.
Do not use this task for Supplier Address or Supplier Site Assignment imports.
Do not submit ESS, call UCM, or modify interface or rejection tables directly.

## Preflight

Before any Fusion-changing action, confirm the target environment, Data Loader
session and access, live registration contract, source/package structure,
required supplier references, optional batch scope, companion members when
applicable, and whether the run is preview or live. Stop before preview for an
invalid package or unresolved business input.

## Failure Handling and Data Protection

Classify invalid source data, package structure, or missing business input as
`input_validation`; do not submit. Classify a missing or changed Data Loader
contract as `catalog_or_metadata_mismatch`; stop rather than guessing job
mappings, tables, or argument positions. For authentication, authorization,
transport, or Fusion failures, retain only redacted diagnostics and the request
identifier; do not retry a live import without a corrected immutable
replacement package and new approval. On monitoring timeout, preserve the last
status and request ID and ask whether to resume monitoring. Never persist or
display credentials, tokens, token caches, private keys, full source rows, or
full package/base64 content.

The Site registration can support companion FBDI members. Include them only
when the requested business outcome and the selected current template require
their data; do not add empty or unrelated companion members. When a companion
member is included, preserve it and use the registered primary interface table
for monitoring.

Prepare only the requested sites, preserve template structure and parent
supplier references, and use `BATCH_ID` only when supported. Validate against
live metadata. Use Core's final preview and approval under the parent's workflow
rules, then submit the retained package through Core's approved-artifact workflow. Reconcile
uncertain outcomes before retrying.

## Entity Dependency

Import a Supplier Site only after the referenced Supplier and Supplier Address
have been processed successfully. Confirm those prerequisites with the user
before live submission; do not block package preparation when they confirm the
required records are already available. The Supplier must be `SPEND_AUTHORIZED`;
`PROSPECTIVE` suppliers cannot have Supplier Sites. A successfully processed
Site is required before its Site Assignments can be imported.
