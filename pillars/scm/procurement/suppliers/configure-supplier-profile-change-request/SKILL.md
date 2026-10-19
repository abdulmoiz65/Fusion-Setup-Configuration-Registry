---
skill_id: "scm.procurement.suppliers.configure-supplier-profile-change-request"
name: "Configure Supplier Profile Change Request Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Supplier Profile Change Request under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "ORA_POZ_CONFIGURE_SUPPLIER_PROFILE_CHANGE_REQUEST"
task_name: "Configure Supplier Profile Change Request"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-supplier-profile-change-request/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/configure-supplier-profile-change-request/current/"
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

# Configure Supplier Profile Change Request Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Supplier Profile Change Request` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `ORA_POZ_CONFIGURE_SUPPLIER_PROFILE_CHANGE_REQUEST`
- task_name: `Configure Supplier Profile Change Request`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Supplier Profile Change Request` under `Suppliers`.

## Setup Task Metadata

- Task name: `Configure Supplier Profile Change Request`
- Task code: `ORA_POZ_CONFIGURE_SUPPLIER_PROFILE_CHANGE_REQUEST`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `supplierEntityConfigurations`, `supplierOptions`

## Related Descriptive Flexfield Tasks

This task configures profile-change-request behavior; it does not create or
deploy Descriptive Flexfield definitions. Route a DFF requirement by its
business scope:

- Supplier Profile or Supplier Sites: [Manage Supplier Descriptive Flexfields](../manage-supplier-descriptive-flexfields/SKILL.md)
- Supplier Addresses: [Manage Trading Community Organization Site Descriptive Flexfields](../../../../cx/customer-data-management/trading-community-foundation/manage-trading-community-organization-site-descriptive-flexfields/SKILL.md)
- Supplier contact: [Manage Trading Community Person Descriptive Flexfields](../../../../cx/customer-data-management/trading-community-foundation/manage-trading-community-person-descriptive-flexfields/SKILL.md)
- Supplier Bank Accounts: [Manage Supplier Bank Account Descriptive Flexfields](../manage-supplier-bank-account-descriptive-flexfields/SKILL.md)

After the relevant DFF definition is deployed, use this task only to configure
the profile-change-request behavior that makes the relevant profile, Supplier
Sites, Supplier Addresses, contact, or bank-account change available to
suppliers.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using supplierEntityConfigurations, supplierOptions as the Business Objects.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Configure Supplier Profile Change Request`
- Setup task code: `ORA_POZ_CONFIGURE_SUPPLIER_PROFILE_CHANGE_REQUEST`

## Shared Business-Object Boundaries

This task shares `supplierEntityConfigurations` with `Configure Supplier
Registration` and the seeded `supplierOptions` row with both `Configure
Supplier Registration` and `Configure Supplier Notifications`.

| Business Object | This Task May Change | Reserved for Other Tasks |
|---|---|---|
| `supplierEntityConfigurations` | `InternalChangeMgmtCode`, `SupplierInitiatedChangeMgmtProspectiveCode`, `SupplierInitiatedChangeMgmtSpendAuthorizedCode` | Registration: `RegistrationProspectiveCode`, `RegistrationSpendAuthorizedCode` |
| `supplierOptions` | `InternalChangeBankAccAttachmentsRequiredFlag`, `SupplierPortalChangeBankAccAttachmentsRequiredFlag` | Registration: `AutoCreateSiteAssignmentFlag`, `ExternalRegBankAccAttachmentsRequiredFlag`, `ExternalRegCompanyDetailsAttachmentsRequiredCode`, `ExternalRegSuccessMessage`, `ExternalRegSupplierIdRequiredFlag`, `ExternalRegWelcomeMessage`, `InternalRegSupplierBusRelationDefaultCode`, `InternalRegSupplierIdRequiredFlag`, `SourcingSupplierBusRelationDefaultCode`, `SourcingSupplierIdRequiredFlag`, `SSPSupplierBusRelationDefaultCode`, `SSPSupplierIdRequiredFlag`; Notifications: `NotifyPriorToExpirationDays`, `ReminderFrequencyDays` |

Resolve the existing shared row through the documented read-only lookup,
execute shared-row tasks serially, and re-read after an earlier task succeeds.
Every Data Loader artifact must contain only this task's owned attributes.

## Preparation and Verification

Use the [read-only lookup rules](ora-resource/ora_reference_lookups.md) to
identify the selected existing entity rows and exactly one seeded
`SupplierOptionsConfigId`. Bind each selected entity to its returned
`SupplierProfileEntityId`; never substitute an entity code, display name, or
sample value for the numeric key. Stop on a missing or ambiguous match rather
than creating an entity or another Supplier Options row.

Validate approval codes and attachment-flag representations against the
task's input rules and current loader metadata. Registration states such as
Enabled, Hidden, and Required are not approval decisions. Prepare only the
resolved keys, supported update operation, and explicitly requested task-owned
fields. Omit Preserve choices and unrelated registration/notification fields;
do not send blank or null values merely to represent no requested change.
Disclose any supplied out-of-scope change instead of silently applying it.

Submit through Core Data Loader's existing preview and approval workflow.
After completion, re-read the affected entities and attachment flags, compare
every requested setting, and confirm preservation of the shared registration
settings. Report mismatches or unavailable verification separately from job
status; a successful load alone does not establish that each value was applied.
Do not automatically resubmit a mismatch or an uncertain outcome.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Use Provided Configuration First

Reuse supplied answers, requirements, spreadsheets, images, tables, and text.
Map each choice to this task, its Internal, Supplier Initiated — Prospective,
or Supplier Initiated — Spend Authorized context, and entity/setting, retaining
a sheet/cell, image region, or statement reference. Accept clearly labeled
formats without repetition or reformatting; an optional layout is
`Task | Context | Entity/Setting | Requested Value`.

Distinguish desired changes from current-state screenshots, exports, and
examples. A cropped, disabled, or unreadable control is not No Approval.
Ask only for missing in-scope decisions needed for the change, unreadable
values (in a readable format), ambiguous context, unsupported choices, or
conflicts. Resolve conflicting answers only through clarification or explicit
user supersession; do not restart completed question groups.

Validate approval and attachment choices against the input rules, selected
entity, and current metadata. Apply common answers only within their stated
context and configurable entities; approval answers do not decide bank-account
attachment requirements. Resolve conflicting Supplier Portal attachment
choices before preparing its shared flag. Blanks are missing answers, not
No Approval, false, or Clear. Preserve unrequested settings and accept explicit
Preserve decisions.

Skip completed questions. Before Core Data Loader's preview/approval, show one
current-versus-requested summary with each entity separately, source references,
and preserved settings. A file or interpretation confirmation is not execution
approval; use Core's gate without adding another confirmation.

## Guided Configuration Questions

Use Supplier Profile Change Request terminology. For choices still missing
after **Use Provided Configuration First**, ask at most one consolidated
question per relevant context, one context at a time. List unresolved
in-scope entities separately and request `Approval Required`, `No Approval`,
or Preserve. Skip completed and out-of-scope contexts. A common answer is
acceptable only when its scope is explicit.

Before asking, obtain a fresh read-only configuration lookup and display the
current value for each in-scope entity and bank-account attachment control
through the documented read-only lookup workflow. Supplied snapshots do not
replace this target-environment lookup. Label it **Current value**, not a
product default; if lookup is unavailable, state that the value is unverified
and do not invent a default.

1. **Internal Profile Management**: Organization Details and Income Tax;
   Addresses; Contacts; Contact User Account; Sites; Payment Methods; Bank
   Accounts; Payment Attributes; Business Classifications; Products and
   Services. Also ask whether bank-account attachments are required for
   internal changes.
2. **Supplier Initiated — Prospective**: Organization Details; Tax Details;
   Addresses; Contacts; Contact User Account; Sites; Payment Methods; Bank
   Accounts; Business Classifications; Products and Services.
3. **Supplier Initiated — Spend Authorized**: Organization Details; Tax
   Details; Addresses; Contacts; Contact User Account; Sites; Payment Methods;
   Bank Accounts; Business Classifications; Products and Services.

When either supplier-initiated context includes a requested bank-account
attachment-policy change, collect the shared Supplier Portal attachment flag
once, alongside the first applicable context. Reuse a supplied answer for both
contexts; ask only if missing or conflicting. Do not require this separate
decision for an approval-only change.

Require an explicit common answer or per-entity decision only for the selected
changes, not every entity or context. Treat a blank supplied answer as missing;
confirm whether an unavailable control is non-configurable using current
metadata rather than an incomplete screenshot. Exclude verified
non-configurable areas and Preserve choices from the change artifact. Map only
selected, configurable changes to this task's owned attributes in **Shared
Business-Object Boundaries**; preserve all other rows and attributes.

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.procurement.suppliers` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
