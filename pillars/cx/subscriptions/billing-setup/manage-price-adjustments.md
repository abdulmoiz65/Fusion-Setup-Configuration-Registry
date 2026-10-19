---
task_code: "CUSTOM_MANAGE_PRICE_ADJUSTMENTS"
task_name: "Manage Price Adjustments"
parent_skill_id: "cx.subscriptions.billing-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Billing Setup"
functional_area_code: "CUSTOM_BILLING_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "priceAdjustmentCategories"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Price Adjustments

## Setup Task Metadata

- Task name: `Manage Price Adjustments`
- Task code: `CUSTOM_MANAGE_PRICE_ADJUSTMENTS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `priceAdjustmentCategories`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.

## Creation Inventory and Placement Workflow

Before preparing or requesting approval for any new Price Adjustment Category or Price Element:

1. Retrieve the complete current `priceAdjustmentCategories` inventory from Fusion; do not use a cached inventory.
2. Present all current Adjustment Categories and all current Price Elements in separate sequence-ordered tables before asking for placement or a sequence.
3. For each Adjustment Category, show code, name, sequence, bill-line attribute, display preference, charge-level flag, user-enterable flag, allow-after-activation flag, and allow-overapplication flag. For each Price Element, show code, name, sequence, bill-line attribute, and display preference.
4. If the request does not include an exact sequence or a placement reference, ask the implementer to choose a position from the displayed inventory or provide an exact numeric sequence. Do not suggest a sequence without resolving the requested neighboring records.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `priceAdjustmentCategories` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "priceAdjustmentCategories" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Price Adjustments` under `Billing Setup`.
