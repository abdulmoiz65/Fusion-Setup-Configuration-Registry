---
skill_id: "scm.procurement.suppliers.import-suppliers.import-supplier-contacts"
name: "Import Supplier Contacts"
description: "Prepares and submits Supplier Contact FBDI packages through the registered Supplier Contact Data Loader business object. It validates the current contact import template and routes the approved immutable package exclusively through core.data-loader."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_name: "Import Supplier Contacts"
parent_skill_id: "scm.procurement.suppliers.import-suppliers"
dataloader_import_mode: "FBDI"
businessObject: "Supplier Contact"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs:
  - "supplier_contact_source_data_or_fbdi_package"
  - "target_environment"
  - "optional_batch_id"
  - "project_context"
  - "execution_approval"
outputs:
  - "supplier_contact_fbdi_package"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-contacts/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-supplier-contacts/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
side_effects:
  - "Prepares Supplier Contact FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, core.data-loader uploads the approved package and submits the registered Supplier Contact FBDI import to the selected Fusion environment."
  - "The import can create or update supplier contacts and contact addresses represented by the approved source data; Fusion processing is not automatically reversible."
required_privileges:
  - "Access to the selected Fusion environment through the configured Data Loader connection."
---

# Import Supplier Contacts

## Supplied Import Inputs

Follow the parent rules for [supported operations](../SKILL.md#supported-operations),
[Core registration selection](../SKILL.md#fbdi-registration-selection), and
[input reuse](../SKILL.md#reuse-supplied-import-inputs). Keep this entity's scope
and approval gate. Reuse applicable explicit prerequisite confirmations; ask
only when missing or unclear.

Apply the parent's [Core workflow and approval rules](../SKILL.md#core-workflow-and-approval).

## Expected CSV Filenames

`PozSupContactsInt.csv` for contacts and `PozSupContactAddressesInt.csv` for
contact-address associations. Populate only the requested entities. Apply the
parent's [filename-hint rules](../SKILL.md#fbdi-registration-selection).

## Purpose

Use this skill to prepare, validate, preview, submit, and monitor a Supplier
Contact FBDI import. It supports contacts, contact-address associations, or
both; it is not the Supplier Site Contacts import.

## Registered Data Loader Contract

Use Core's package-based FBDI selection. Verify that the resolved registration
supports the requested contact/contact-address members; the table below is
task-scope reference information, not a BO-name lookup.

| Setting | Value |
|---|---|
| Import entity | Supplier Contacts |
| UCM account | `prc/supplier/import` |
| Contact data-file prefix | `PozSupContactsInt` |
| Contact-address data-file prefix | `PozSupContactAddressesInt` |
| Primary interface table | `POZ_SUP_CONTACTS_INT` |
| Related interface table | `POZ_SUP_CONTACT_ADDRESSES_INT` |
| Request column | `LOAD_REQUEST_ID` |
| Import scope | `BATCH_ID` when supplied |

A registration may also expose Site Contact members. Do not include
`PozSupSiteContactsInt` data unless the requested operation is explicitly the
separate Supplier Site Contacts import.

Data Loader owns the registered ESS arguments, upload, submission, polling,
and diagnostics. Do not submit the ESS job, call UCM, or invoke ERP
Integrations REST directly from this task.

## Source and Package Preparation

1. Obtain the current Supplier Contact Import workbook/control-file template
   for the target release. Treat its active sheet, column sequence, required
   fields, and CSV conventions as authoritative.
2. Prepare contact rows, contact-address rows, or both, according to the
   requested outcome. Do not require new contact rows for associations to an
   existing Contact. Preserve the current template's exact header/order and
   parent-child references.
3. Use one nonblank `BATCH_ID` for all rows when the template supports it. If
   the supplied data has no batch identifier, retain it blank rather than
   fabricating one.
4. Create a ZIP containing only the applicable supported members that match
   the registered contact/contact-address prefixes. Reject path traversal,
   duplicate members, unsupported files, and packages with no rows for either
   requested entity. A contact-address-only package may omit contact data rows;
   preserve any empty-member requirements of the current template.
5. Validate member names, template layout, parent-child completeness, and
   intended row count. Delegate immutable artifact preparation and integrity
   handling to Core; after approval, do not reread original sources or create
   separate Supplier-managed validation snapshots.

Do not add `LOAD_REQUEST_ID`, `REQUEST_ID`, status, rejection, or other
internal interface values to source data. Fusion/Data Loader assigns them.

## Entity Dependency

Import a Contact only after its parent Supplier has been processed
successfully. Confirm that prerequisite with the user before live submission;
do not block package preparation when the user confirms the Supplier is
already available. A Contact Address requires both the referenced Supplier Address
and a Contact that is created in the same package or already exists. A
contact-address-only package is valid when its referenced Contact and Supplier
Address already exist. Validate that the live registration supports the
association-only scope; if its validation, batch resolver, or observability
requires contact rows, report the registration mismatch rather than adding
unrequested contacts or bypassing Core validation.
When contact-address rows are included, also confirm with the user that the
referenced Supplier Address and Contact prerequisite is already satisfied; do
not require the Supplier Address skill to run for a contacts-only package.

## Mandatory Execution Route

1. Run preflight before any Fusion-changing action: validate target environment
   identity, Data Loader session/access, source/ZIP shape, contact parent
   references, optional batch scope, and whether the operation is preview or
   live. Stop before preview on an invalid ZIP or unresolved source ambiguity.
2. Let `core.data-loader` identify the FBDI registration from the prepared ZIP
   and live metadata. Validate the exact package and requested contact scope
   against the resolved contract.
3. Let Data Loader derive optional `BATCH_ID` scope and apply the registered
   Supplier Contact import arguments. Do not override argument positions.
4. Use Core's final preview and approval under the parent's workflow rules.
5. After approval, submit the retained package through Core's approved-artifact workflow.
   A changed ZIP, target, or business scope requires a replacement preview and
   approval.
6. When status is requested, monitor through Data Loader. Treat `PROCESSED` as success, `REJECTED` as
   error, and null/other status as pending. Return actionable rejected-contact
   diagnostics from the registered Data Loader contract.

## Retry, Failure Handling, and Diagnostics

- Classify invalid source data, ZIP structure, or missing business input as
  `input_validation`; do not submit or retry until corrected.
- Classify a missing/changed Data Loader contract as
  `catalog_or_metadata_mismatch`; stop instead of guessing mappings or tables.
- For authentication, authorization, transport, or Fusion failures, retain the
  redacted Data Loader diagnostic and request identifier where present. Retry
  only bounded read-only recovery; never retry a live import without explicit
  approval for the exact replacement package.
- On a monitoring timeout, preserve the last status and request identifier,
  stop polling, and ask whether to resume monitoring; do not resubmit the ZIP.
- Keep project evidence within the parent's Core workflow rules.
  Never persist or display credentials,
  tokens, token caches, private keys, full source rows, or full package/base64
  content.

## Communication

Report the business result first: requested contacts, target environment,
batch scope, import state, and actionable rejected rows. Keep implementation
details concise unless requested. Ask for approval only for the live import,
after preparation and validation are complete.
