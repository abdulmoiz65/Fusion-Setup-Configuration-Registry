---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-business-classifications"
name: "Import Supplier Business Classifications"
description: "Prepares and submits Supplier Business Classification FBDI packages through the registered Data Loader business object."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Business Classifications"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Business Classifications"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs: ["supplier_business_classification_source_data_or_fbdi_package", "target_environment", "optional_batch_id", "project_context", "execution_approval"]
outputs: ["supplier_business_classification_fbdi_package", "package_validation_result", "import_preview", "data_loader_execution_result", "load_status_and_errors", "skill_run_record", "token_usage_record"]
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-business-classifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-business-classifications/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Business Classification FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, the import can create or update supplier classifications."
required_privileges: ["Access to the selected Fusion environment through the configured Data Loader connection."]
---

# Import Supplier Business Classifications

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filename

`PozSupBusClassInt.csv`. Apply the parent's
[filename-hint rules](../SKILL.md#fbdi-registration-selection).

## Purpose

Prepare and execute only an approved Supplier Business Classification FBDI
package against the selected Fusion environment.

Use Core's package-based FBDI selection and verify that the resolved contract
covers the requested Supplier Business Classifications import. Do not reuse
Supplier, Site, or Contact mappings. Route package preparation, validation,
approval, submission, and monitoring exclusively through `core.data-loader`.
Do not submit ESS, call UCM, or modify interface or rejection tables directly.

## Preflight

Before any Fusion-changing action, confirm the target environment, Data Loader
session and access, live registration contract, source/package structure,
required supplier and classification references, optional batch scope, and
whether the run is preview or live. Stop before preview for an invalid package
or unresolved business input.

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

Prepare the current FBDI template without changing headers, classification
references, supporting agency/certification fields, or control-file structure.
Use one nonblank `BATCH_ID` where the template supports it. Exclude internal
load, request, status, and rejection fields from source rows.

## Entity Dependency

Import a Business Classification only after its parent Supplier has been
processed successfully. Confirm that prerequisite with the user before live
submission; do not block package preparation when the user confirms the
Supplier is already available. The referenced Classification must be valid. A
Certifying Agency must already exist unless the template row explicitly creates
it with the supported create-agency option.

Before the live action, validate the package against the registered contract.
Use Core's final preview and approval under the parent's workflow rules, then
submit the retained package through Core's approved-artifact workflow. When status is requested,
interpret results and rejected rows through Core using the live registration. Reconcile an
uncertain request before any replacement package or retry.
