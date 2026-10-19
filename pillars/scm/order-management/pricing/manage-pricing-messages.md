---
task_code: "ORA_QP_MANAGE_PRICING_MESSAGES"
task_name: "Manage Pricing Messages"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "pricingMessages"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Messages

## Setup Task Metadata

- Task name: `Manage Pricing Messages`
- Task code: `ORA_QP_MANAGE_PRICING_MESSAGES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Top-level Data Loader Business Object: `pricingMessages`
- Token-association child component: `pricingMessageTokens` in `pricingMessages.dat`

## Read-only REST Discovery

For a live inventory of Pricing messages, use the parent Pricing skill's
read-only REST workflow through `core.fusion-api.rest-api-client`. This
discovery route permits GET only; do not create, update, delete, import, or
submit messages or their tokens while fulfilling a fetch request. GET
`/fscmRestApi/resources/11.13.18.05/pricingMessages` with
`expand=pricingMessageTokens` to include the tokens attached to each message.
Use `PricingMessageId` for a single parent's
`/child/pricingMessageTokens` GET. Page the parent and, when necessary, child
collections before claiming a complete list. The message `Name` is distinct
from a child `TokenName`; an empty setup-task CSV export is not proof that
predefined messages or attached tokens do not exist.

## Existing-message Updates

This skill permits updates to an existing Pricing message only through the
parent Pricing skill's `core.data-loader` workflow. Resolve and GET the
existing `PricingMessageId` and complete child-token collection. For a missing
token, validate and load only the child association before the text update.
For an explicitly requested token removal, validate a child-only Data Loader
`DELETE|pricingMessageTokens` source using the unique live child key and parent;
never delete the `pricingMessages` parent or shared token attribute definition.
Confirm child-load completion and the expected child state before loading a
separate update-only parent `MessageText` source. Stop after each successful
initiation until the user requests status, as `core.data-loader` requires.
Never use a direct REST write or assume child registration alone makes a source
loadable. `pricingMessageTokens` is a child of top-level `pricingMessages`, not
a standalone Data Loader Business Object, and both sections use
`pricingMessages.dat`. Child sections may differ across
environments or template revisions; always validate against the current selected
environment's template and operation metadata.
A fetch request remains GET only.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Route any existing-message text change or explicitly requested token-association add/delete through `core.data-loader` only. Resolve top-level `pricingMessages` and its `pricingMessageTokens` child; do not submit the child as a standalone Business Object. Require live operation support, exact child keys, a usable UCM template section or validated adapter for the child, and an update-only parent mapping before preparing a load. Fail closed when the selected operation or section is absent from current metadata.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Messages`
- Setup task code: `ORA_QP_MANAGE_PRICING_MESSAGES`




## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `pricingMessages` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "pricingMessages" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook only after the required parent and child load mappings are validated. A root-only sample does not authorize an association add or delete.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Pricing Messages` under `Pricing`.

## Oracle Documentation

- [Manage Pricing Messages (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/manage-pricing-messages.html) identifies the Setup and Maintenance task and explains how messages use token names from the applicable pricing entity.
- [Create and manage pricing messages (26D readiness)](https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/order26d/26D-order-mgmt-wn-f50334.htm) confirms that the redesigned page retains the existing message and token behavior and names the required management privilege.
- [Data Deletion Using HCM Data Loader](https://docs.oracle.com/en/cloud/saas/human-resources/fahdl/data-deletion-using-hcm-data-loader.html) documents child-component `DELETE` instructions. The selected Fusion environment's live Data Loader child metadata and DAT template remain authoritative for `pricingMessageTokens` support and keys.
