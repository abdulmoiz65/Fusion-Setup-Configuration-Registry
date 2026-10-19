---
skill_id: "scm.procurement.suppliers.configure-supplier-registration"
name: "Configure Supplier Registration Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Supplier Registration under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "POZ_CONFIGURE_SUPPLIER_REGISTRATION"
task_name: "Configure Supplier Registration"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "supplierEntityConfigurations"
  - "supplierOptions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
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
  - "core.data-loader"
uses_core:
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-supplier-registration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-supplier-registration/current/"
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
side_effects: []
required_privileges: []
---

# Configure Supplier Registration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Supplier Registration` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `POZ_CONFIGURE_SUPPLIER_REGISTRATION`
- task_name: `Configure Supplier Registration`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `supplierEntityConfigurations`, `supplierOptions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `supplierEntityConfigurations`, `supplierOptions` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "supplierEntityConfigurations" \
     "supplierOptions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Supplier Registration` under `Suppliers`.

## Setup Task Metadata

- Task name: `Configure Supplier Registration`
- Task code: `POZ_CONFIGURE_SUPPLIER_REGISTRATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects, in loader order: `supplierEntityConfigurations`, `supplierOptions`

## Related Descriptive Flexfield Tasks

This task configures supplier-registration behavior; it does not create or
deploy Descriptive Flexfield definitions. Route a DFF requirement by its
business scope:

- Supplier registration header: [Manage Supplier Registration Descriptive Flexfields](../manage-supplier-registration-descriptive-flexfields/SKILL.md)
- Supplier Addresses: [Manage Trading Community Organization Site Descriptive Flexfields](../../../../cx/customer-data-management/trading-community-foundation/manage-trading-community-organization-site-descriptive-flexfields/SKILL.md)
- Supplier contact: [Manage Trading Community Person Descriptive Flexfields](../../../../cx/customer-data-management/trading-community-foundation/manage-trading-community-person-descriptive-flexfields/SKILL.md)

After the relevant DFF definition is deployed, use this task only to configure
the registration behavior that exposes it in the applicable registration flow.
Supplier Registration REST exposes no Supplier Sites, Bank Accounts, or global
DFF collection; do not add those scopes to this task without current REST
metadata that shows the corresponding collection.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using supplierEntityConfigurations, supplierOptions as the Business Objects.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Configure Supplier Registration`
- Setup task code: `POZ_CONFIGURE_SUPPLIER_REGISTRATION`

## FSM Export Header Mapping (26D)

Use these explicit mappings, not fuzzy matching, for 26D task-export CSVs.
Verify targets against the selected environment's current loader metadata.
This is source-preparation guidance, not Core aliases or native combined
support for the unchanged CSV pair.

### POZ_SUP_ONBOARD_CONFIG.csv

An export filename may have a download suffix such as `(1)`. Its field meaning
does not change with that suffix.

| FSM CSV header | Loader attribute or handling | Meaning and value handling |
|---|---|---|
| SupplierProfileEntity | Resolve the entity code to the existing SupplierProfileEntityId | Export values such as ADDRESSES and CONTACT_USER_ACCOUNT identify the profile component by code, not its localized display name. Use the current entity collection to resolve exactly one row; do not copy the code into the numeric ID. |
| RegProspective | RegistrationProspectiveCode | Registration component state for Prospective suppliers; validate ENABLED, REQUIRED, or HIDDEN against the component-specific rules. |
| RegSpendAuth | RegistrationSpendAuthorizedCode | Registration component state for Spend Authorized suppliers; apply the same component-specific validation. |
| ChangeMgmtProspective | SupplierInitiatedChangeMgmtProspectiveCode; not owned by this task | Supplier-initiated profile change approval for Prospective suppliers; a nonblank requested change belongs to Configure Supplier Profile Change Request. |
| ChangeMgmtSpendAuth | SupplierInitiatedChangeMgmtSpendAuthorizedCode; not owned by this task | Supplier-initiated profile change approval for Spend Authorized suppliers; not a registration state. |
| ChangeMgmtInternal | InternalChangeMgmtCode; not owned by this task | Internal profile change approval; not a registration state. |

### ORA_POZ_SUP_DEFBUSREL.csv

| FSM CSV header | Loader attribute or handling | Meaning and value handling |
|---|---|---|
| SupplierOptionsCode | Export identity only; resolve SupplierOptionsConfigId through read_registration_supplier_options | The seeded export code ORA_POZ_SUPPLIER_OPTIONS_CODE identifies Supplier Options. It is not a loader field or numeric ID; never accept the fuzzy suggestion SupplierOptionsCode to SupplierOptionsConfigId. |
| SourcingBusRelDefault | SourcingSupplierBusRelationDefaultCode | Default business relationship for Sourcing supplier registration. |
| SspBusRelDefault | SSPSupplierBusRelationDefaultCode | Default business relationship for Self Service Procurement supplier registration. |
| InternalBusRelDefault | InternalRegSupplierBusRelationDefaultCode | Default business relationship for internal supplier registration. |
| EnableAutoCreateSiteAssign | AutoCreateSiteAssignmentFlag | Whether site assignments are created automatically after spend authorization approval. |
| SspRegAtLeastOneReqVal | SSPSupplierIdRequiredFlag | Whether Self Service Procurement registration requires at least one supplier identifier. |
| ExtRegAttachReqBusRel | ExternalRegCompanyDetailsAttachmentsRequiredCode | Business relationship scope requiring Company Details attachments for external registration: Prospective, Spend Authorized, or Both; validate the corresponding stored code against the live contract. |
| ExtregRequireTaxidFlag | ExternalRegSupplierIdRequiredFlag | Whether external registration requires at least one supplier identifier; not a requirement for Taxpayer ID specifically. |
| IntregRequireTaxidFlag | InternalRegSupplierIdRequiredFlag | Whether internal registration requires at least one supplier identifier. |
| SourcingRequireTaxidFlag | SourcingSupplierIdRequiredFlag | Whether Sourcing registration requires at least one supplier identifier. |
| ExtRegBankaccAttachReq | ExternalRegBankAccAttachmentsRequiredFlag | Whether external registration requires bank-account attachments. |
| IntChgBankaccAttachReq | InternalChangeBankAccAttachmentsRequiredFlag; not owned by this task | Internal profile change bank-account attachment requirement; belongs to Configure Supplier Profile Change Request. |
| ExtChgBankaccAttachReq | SupplierPortalChangeBankAccAttachmentsRequiredFlag; not owned by this task | Supplier portal profile change bank-account attachment requirement; belongs to Configure Supplier Profile Change Request. |
| ExternalRegWelcomeMessage | ExternalRegWelcomeMessage | Exact external-registration welcome message content. |
| ExternalRegSuccessMessage | ExternalRegSuccessMessage | Exact external-registration success message content. |

Validate relationship/attachment enums against the relevant registration source
and live contract; the table does not expand supported choices. Interpret Y/N
as Yes/No and serialize flags using the live loader's Boolean representation.
Resolve existing keys through the [read-only lookup rules](ora-resource/ora_reference_lookups.md),
never by copying export codes into numeric IDs.

Blank configuration cells mean Preserve: record that decision before defaulting
and omit the attribute, rather than sending blank, false, or a clear marker.
Accept only ORA_POZ_SUPPLIER_OPTIONS_CODE as a supplied SupplierOptionsCode;
clarify unknown identities. Disclose nonblank changes owned by another task and
route them there, rather than dropping or applying them here. Unknown headers,
conflicting aliases, unresolved keys, and unsupported nonblank values block
preparation until resolved.

Prepare only registration-owned fields and resolved existing keys, retaining
mapping evidence. Use Core's validation, immutable preview, and approval gates.
After completion, re-read and compare every requested value; job success alone
does not prove each setting was applied.

## Shared Business-Object Boundaries

Both registered Data Loader business objects are shared with `Configure Supplier Profile Change Request`. Before preparing either artifact, use the task's read-only lookup rule; serialize the two tasks and re-read the affected row after the earlier task completes.

| Business Object | This Task May Change | Other Shared-Task Attributes |
|---|---|---|
| `supplierEntityConfigurations` | `RegistrationProspectiveCode`, `RegistrationSpendAuthorizedCode` | Profile Change Request: `InternalChangeMgmtCode`, `SupplierInitiatedChangeMgmtProspectiveCode`, `SupplierInitiatedChangeMgmtSpendAuthorizedCode` |
| `supplierOptions` | `AutoCreateSiteAssignmentFlag`, `ExternalRegBankAccAttachmentsRequiredFlag`, `ExternalRegCompanyDetailsAttachmentsRequiredCode`, `ExternalRegSuccessMessage`, `ExternalRegSupplierIdRequiredFlag`, `ExternalRegWelcomeMessage`, `InternalRegSupplierBusRelationDefaultCode`, `InternalRegSupplierIdRequiredFlag`, `SourcingSupplierBusRelationDefaultCode`, `SourcingSupplierIdRequiredFlag`, `SSPSupplierBusRelationDefaultCode`, `SSPSupplierIdRequiredFlag` | Profile Change Request: `InternalChangeBankAccAttachmentsRequiredFlag`, `SupplierPortalChangeBankAccAttachmentsRequiredFlag`; Configure Supplier Notifications: `NotifyPriorToExpirationDays`, `ReminderFrequencyDays` |

For `supplierOptions`, resolve exactly one existing `SupplierOptionsConfigId`; never create another singleton row. Each immutable Data Loader artifact must contain only the fields owned by its task. `core.data-loader` remains the only mutation route.

## Use Provided Configuration First

Reuse supplied answers, requirements, spreadsheets, images, tables, and text.
Map each choice to this task, its registration relationship/control group,
and entity/setting, retaining a sheet/cell, image region, or statement reference.
Accept clearly labeled formats without repetition or reformatting; an optional
layout is `Task | Context | Entity/Setting | Requested Value`.

Distinguish desired changes from current-state screenshots, exports, and
examples; do not infer registration choices from profile-change policies.
Ask only for missing in-scope decisions needed for the change, unreadable
values (in a readable format), unclear context, unsupported choices, or
conflicts. Resolve conflicting answers only through clarification or explicit
user supersession; do not restart completed question groups.

Validate choices against component-specific rules and current metadata.
Apply common answers only to their stated scope and supported entities.
Blanks are missing answers, not Hidden, false, or Clear, except for FSM
configuration cells explicitly defined as Preserve above. Preserve unrequested
settings and accept explicit Preserve decisions; defaults must not override
supplied values or Preserve.

Skip completed questions. Before Core Data Loader's preview/approval, show one
current-versus-requested summary with each entity separately, source references,
and preserved settings. A file or interpretation confirmation is not execution
approval; use Core's gate without adding another confirmation.

## Guided Configuration Questions

Use Supplier Registration configuration terminology. Only for choices still
missing after **Use Provided Configuration First**, collect answers in a small
number of consolidated prompts, listing each relevant entity separately.
Skip completed groups and do not ask about settings outside the requested
scope.

Before asking, obtain a fresh read-only configuration lookup and display the
current value for each in-scope entity, control, and message through the
documented read-only lookup workflow. Supplied snapshots do not replace this
target-environment lookup. Label it **Current value**, not a product default;
if the lookup is unavailable, state that the current value is unverified and
do not invent a default.

1. Ask **one consolidated question** for the registration state of all listed
   entities for **Prospective** suppliers:
   - Contact User Account — choose `Enabled` or `Required`
   - Addresses — choose `Enabled`, `Hidden`, or `Required`
   - Business Classifications — choose `Enabled`, `Hidden`, or `Required`
   - Bank Accounts — choose `Enabled`, `Hidden`, or `Required`
   - Products and Services — choose `Enabled`, `Hidden`, or `Required`
   - Questionnaire — choose a state supported by the component-specific
     validation rules and current metadata; the documented choices are
     `Enabled` or `Hidden`
   Company Details and Contacts are always required and non-configurable on
   this page; state that fixed behavior but do not request values or include
   them in the import artifact.
2. Ask **one separate consolidated question** for the registration state of
   all listed entities for **Spend Authorized** suppliers:
   - Contact User Account — choose `Enabled` or `Required`
   - Addresses — choose `Enabled`, `Hidden`, or `Required`
   - Business Classifications — choose `Enabled`, `Hidden`, or `Required`
   - Bank Accounts — choose `Enabled`, `Hidden`, or `Required`
   - Products and Services — choose `Enabled`, `Hidden`, or `Required`
   - Questionnaire — choose a state supported by the component-specific
     validation rules and current metadata; the documented choices are
     `Enabled` or `Hidden`
   Company Details and Contacts remain always required and non-configurable.
3. Ask for the **External registration** controls in one prompt:
   - Require supplier identifier
   - Require attachments for Company Details: `Both`, `Prospective`, or
     `Spend Authorized`
   - Require attachments for Bank Accounts
4. Ask for the **Internal registration** controls in one prompt:
   - Default business relationship: `Prospective` or `Spend Authorized`
   - Require supplier identifier
5. Ask for the **Self service procurement** controls in one prompt:
   - Default business relationship: `Prospective` or `Spend Authorized`
   - Require supplier identifier
6. Ask whether to **Autocreate site assignments for spend authorized
   suppliers** after approval.
7. Ask whether to change either External registration message. If yes, obtain
   the exact rich-text content for the Welcome Message and/or Success Message;
   otherwise preserve the current message values.

If a requested UI choice is unavailable in current live metadata, pause and
ask the user whether to preserve the current value or select another available
choice. Import only this task's owned attributes from **Shared Business-Object
Boundaries**.

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
