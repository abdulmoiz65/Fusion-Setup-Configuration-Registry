---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-site-assignments"
name: "Import Supplier Site Assignments"
description: "Prepares and submits Supplier Site Assignment FBDI packages through the registered Supplier Site Assignment Data Loader business object."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Site Assignments"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Site Assignment"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs: ["supplier_site_assignment_source_data_or_fbdi_package", "target_environment", "optional_batch_id", "project_context", "execution_approval"]
outputs: ["supplier_site_assignment_fbdi_package", "package_validation_result", "import_preview", "data_loader_execution_result", "load_status_and_errors", "skill_run_record", "token_usage_record"]
depends_on: ["scm.procurement.suppliers.import-suppliers", "scm.procurement.suppliers.import-suppliers.import-supplier-sites", "core.data-loader"]
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-site-assignments/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-site-assignments/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Site Assignment FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, the import can create or update supplier site assignments."
required_privileges: ["Access to the selected Fusion environment through the configured Data Loader connection."]
---

# Import Supplier Site Assignments

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filename

`PozSiteAssignmentsInt.csv`. Apply the parent's
[filename-hint rules](../SKILL.md#fbdi-registration-selection).

## Purpose

Prepare and execute only an approved Supplier Site Assignment FBDI package
against the selected Fusion environment.

Use Core's resolved FBDI registration for the requested Supplier Site Assignments
import. Prepare, validate, preview, submit, and monitor through
`core.data-loader`; do not submit the underlying ESS process or change
`POZ_SITE_ASSIGNMENTS_INT` directly.

## Preflight

Before any Fusion-changing action, confirm the target environment, Data Loader
session and access, live registration contract, source/package structure,
required supplier, site, and business-unit references, optional batch scope,
and whether the run is preview or live. Stop before preview for an invalid
package or unresolved business input.

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

## Registered Contract

Verify the live registration before package preparation. The current
registration is scoped by optional `BATCH_ID` and monitors
`POZ_SITE_ASSIGNMENTS_INT` with `LOAD_REQUEST_ID`. It uses the registered
arguments and observability configuration; never hardcode or override them in
the source package.

## Workflow

1. Obtain the current Supplier Site Assignment FBDI template. Preserve its
   headers, supplier/site/business-unit references, and CSV/control-file rules.
2. Build and validate an immutable ZIP matching the live registered prefixes.
   Exclude internal request IDs, statuses, and rejection fields.
3. Use Core's final preview and approval under the parent's workflow rules.
4. Submit the retained package through Core's approved-artifact workflow. When status is
   requested, use its registered summary and rejection details through Core.

## Entity Dependency

Import a Site Assignment only after the referenced Supplier Site has been
processed successfully. Confirm that prerequisite with the user before live
submission; do not block package preparation when the user confirms the Site
is already available. Because Sites and Site Assignments aren't supported
for `PROSPECTIVE` suppliers, the parent Supplier must be `SPEND_AUTHORIZED`.

Do not retry an uncertain or rejected submission without reconciliation, a
corrected package, fresh validation, and explicit replacement approval.
