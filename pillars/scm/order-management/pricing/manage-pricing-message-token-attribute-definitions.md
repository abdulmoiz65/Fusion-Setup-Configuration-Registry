---
task_code: "ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS"
task_name: "Manage Pricing Message Token Attribute Definitions"
parent_skill_id: "scm.order-management.pricing"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "pricingMessageTokenAttributes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Message Token Attribute Definitions

## Setup Task Metadata

- Task name: `Manage Pricing Message Token Attribute Definitions`
- Task code: `ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `pricingMessageTokenAttributes`


## Read-only REST Discovery

For a live inventory of token attribute definitions, use the parent Pricing
skill's read-only REST workflow through `core.fusion-api.rest-api-client`.
This discovery route permits GET only; do not create, update, delete, import,
or submit token attributes through this skill. GET
`/fscmRestApi/resources/11.13.18.05/pricingMessageTokenAttributes` with
`expand=pricingMessageTokenAttributeDetails` to include each definition's
token attributes. Use `MsgTokenAttrDefnId` for a single definition's
`/child/pricingMessageTokenAttributeDetails` GET. Page the parent and, when
necessary, child collections before claiming a complete list. Detail
`TokenName` values include attributes that are not selected; report
`AttributeSelectedFlag` and `UsedFlag` when presenting them. An empty setup-task
CSV export is not proof that predefined definitions or details do not exist.

## CSV Export and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Treat the registered `pricingMessageTokenAttributes` Data Loader business object as catalog metadata. This skill does not create or update token attribute definitions or details; do not run an import for them through this skill.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Message Token Attribute Definitions`
- Setup task code: `ORA_QP_MANAGE_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS`




## Inspect Fusion Data Loader Sample Metadata

Use this read-only workflow when `dataloader_import_mode: "REST"` and sample metadata is needed for the task’s business object.

1. Confirm that `pricingMessageTokenAttributes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "pricingMessageTokenAttributes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields for metadata inspection only. Sample generation uses read-only Fusion metadata and does not upload or import data.
5. Do not use the editable workbook to prepare or submit a load through this skill; token attribute definition and detail writes are outside its scope.

## Usage

Use this metadata file when planning, sequencing, exporting, or validating setup data for `Manage Pricing Message Token Attribute Definitions` under `Pricing`.

## Oracle Documentation

- [Manage Pricing Message Tokens (26C)](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faupr/manage-pricing-message-tokens.html) identifies the Setup and Maintenance task and explains how token attributes supply runtime values for pricing messages.
- [Create and manage pricing message token attribute definitions (26D readiness)](https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/order26d/26D-order-mgmt-wn-f50336.htm) confirms the same task for the redesigned page. The optional Redwood page is controlled by `ORA_QP_PRICING_MESSAGE_TOKEN_ATTRIBUTE_DEFINITIONS_REDWOOD_ENABLED`; Oracle states that the default is `No` and that the underlying task functionality is unchanged.
