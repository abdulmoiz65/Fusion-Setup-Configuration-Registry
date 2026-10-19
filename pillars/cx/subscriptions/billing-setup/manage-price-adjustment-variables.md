---
task_code: "CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES"
task_name: "Manage Price Adjustment Variables"
parent_skill_id: "cx.subscriptions.billing-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Billing Setup"
functional_area_code: "CUSTOM_BILLING_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "subscriptionPriceAdjustmentVariables"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Price Adjustment Variables

## Setup Task Metadata

- Task name: `Manage Price Adjustment Variables`
- Task code: `CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `subscriptionPriceAdjustmentVariables`

## Terminology and Routing

Treat the following implementer requests as the same setup scope and route them to this task: `Manage Price Adjustment Variables`, `Track Price Adjustment Variables`, `Advanced Pricing Term Variables`, `Flexible Pricing Term Option`, and `Formula Driven Flexible Pricing Term Adjustments`.

Route all of these terms to `CUSTOM_MANAGE_PRICE_ADJUSTMENT_VARIABLES` under **CX > Subscriptions > Billing Setup**. Do not route them to price adjustment categories unless the request explicitly asks to create or change a Price Adjustment Category or Price Element.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `subscriptionPriceAdjustmentVariables` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionPriceAdjustmentVariables" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Date-Effective Value Data Loader Rules

Use these rules when adding values to an existing Subscription Price Adjustment Variable:

1. Retrieve the existing parent and its current values before preparing a source. Do not recreate a parent that already exists.
2. Default parent `ActiveFlag` to `true` when the implementer does not provide an active-state choice. Show that default in the approval preview.
3. Format child `StartDate` and `EndDate` as `YYYY/MM/DD` (for example, `2028/01/01`). Do not use `YYYY-MM-DD` in the Data Loader workbook.
4. Use `VariableNumber` as the parent-link surrogate key in each `priceAdjustmentVariableValues` child row.
5. For a values-only load, leave the parent sheet header-only. Do not add a parent reference row; `VariableNumber` on each child row is the surrogate key that preserves the existing parent relationship.
6. Set child `RestAction` to `POST`. Each child row requires `VariableNumber`, `VariableValue`, `StartDate`, and `RestAction`; include `EndDate` when the effective period is bounded.
7. Detect duplicate or overlapping value periods before preview. When a requested period or value already exists, show the existing `VariableNumber` and the matching value record, then ask the implementer to choose an update of that existing record or creation of a distinct, non-overlapping record. Require explicit approval for the chosen operation.
8. Validate the exact workbook against the live UCM template, present the immutable preview, and require explicit approval before upload.
9. After Data Loader submission, check the request status every 30 seconds until it reaches a terminal state. Report the data-set name, status, total, loaded, and failed counts after every check.
10. On `Succeeded`, retrieve the parent and its date-effective values from Fusion. Report every returned non-who column and omit only `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, and `LastUpdateLogin`.
11. On `Warning` or `Error`, report every actionable diagnostic in business terms: affected object or source row, stage, message, and the corrective action. Retrieve the parent and values to determine whether any rows completed; preserve partial completion and do not automatically retry, recreate the parent, or resubmit unchanged source data.

## Multiple-Variable Data Loader Sequencing

When a request creates multiple new variables and their values:

1. Put all new parent variables in one parent-only workbook with parent `RestAction=POST`; do not include child value rows in that load.
2. Submit the parent load, monitor it to a terminal result, and retrieve every parent by `VariableNumber` before continuing.
3. Put all approved child value rows in one values-only workbook. Leave the parent sheet header-only, then set each child `RestAction=POST` with its matching `VariableNumber`.
4. Validate, preview, and obtain approval for the child-values archive. Do not submit it if any parent is missing, inactive, ambiguous, or failed to load.
5. If the child load returns an overlap or orphan diagnostic, stop and reconcile the returned records. Do not replay the unchanged child archive.



## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Price Adjustment Variables` under `Billing Setup`.
