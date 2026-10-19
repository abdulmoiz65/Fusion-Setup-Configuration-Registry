---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-addresses"
name: "Import Supplier Addresses"
description: "Prepares and submits Supplier Address FBDI packages through the registered Supplier Address Data Loader business object. Use for supplier-address imports, not Supplier Site imports."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Addresses"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Address"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs:
  - "supplier_address_source_data_or_fbdi_package"
  - "target_environment"
  - "optional_batch_id"
  - "project_context"
  - "execution_approval"
outputs:
  - "supplier_address_fbdi_package"
  - "package_validation_result"
  - "import_preview"
  - "data_loader_execution_result"
  - "load_status_and_errors"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "scm.procurement.suppliers.import-suppliers"
  - "core.data-loader"
uses_core:
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
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
state_updates: ["configuration_blueprints", "reports", "token_usage_records"]
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-addresses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-addresses/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Address FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, the import can create or update supplier addresses."
required_privileges:
  - "Access to the selected Fusion environment through the configured Data Loader connection."
---

# Import Supplier Addresses

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filename

`PozSupAddressesInt.csv`. Apply the parent's
[filename-hint rules](../SKILL.md#fbdi-registration-selection).

## Purpose

Prepare and execute only an approved Supplier Address FBDI package against the
selected Fusion environment.

Use the live Data Loader registration as the execution authority. Prepare,
validate, preview, submit, and monitor Supplier Address FBDI packages only
through `core.data-loader`; do not call UCM, ESS, or interface tables directly.

## Registered Data Loader Contract

| Setting | Value |
|---|---|
| Import entity | Supplier Addresses |
| UCM account | `prc/supplier/import` |
| Scope | `BATCH_ID` when supplied |

Use Core's resolved FBDI registration for file prefixes, primary interface
table, arguments, scope resolver, and diagnostics. The table above is task-scope
reference information; do not perform a BO-name lookup or reuse another
Supplier entity's contract.

## Preflight

Before any Fusion-changing action, confirm the target environment, Data Loader
session and access, live registration contract, source/package structure,
required parent references, optional batch scope, and whether the run is
preview or live. Stop before preview for an invalid package or unresolved
business input.

## Entity Dependency

Import an Address only after its parent Supplier has been processed
successfully. Confirm that prerequisite with the user before live submission;
do not block package preparation when the user confirms the Supplier is
already available. An Address is a prerequisite for a new Supplier Site that
references it.

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

## Workflow

1. Obtain the current Supplier Address FBDI template for the target release.
   Preserve its exact sheets, headers, column order, and parent references.
2. Build a ZIP with only the requested address data members. Use one nonblank
   `BATCH_ID` when the template supports it; otherwise leave it blank.
3. Validate the ZIP and its member names against live registration metadata.
   Do not include `LOAD_REQUEST_ID`, `REQUEST_ID`, statuses, rejection values,
   or internal interface IDs in source data.
4. Use Core's final preview and approval under the parent's workflow rules.
5. Submit the retained package through Core's approved-artifact workflow. When status is
   requested, use the registration's summary and error contract through Core.

## Recovery and Communication

Never resubmit an uncertain request. Reconcile it first; correct only rejected
rows, rebuild the package, and obtain new approval. Report the business result,
counts, batch, status, and actionable rejected rows before implementation detail.
