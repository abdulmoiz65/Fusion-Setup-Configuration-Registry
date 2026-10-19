---
task_code: "ORA_QP_MANAGE_PRICING_BASES"
task_name: "Manage Pricing Bases"
parent_skill_id: "scm.order-management.pricing"
depends_on:
  - "ORA_QP_MANAGE_PRICE_ELEMENTS"
pillar: "SCM"
offering: "Order Management"
functional_area: "Pricing"
functional_area_code: "ORA_FOM_PRICING"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "qpPricingBases"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Pricing Bases

## Setup Task Metadata

- Task name: `Manage Pricing Bases`
- Task code: `ORA_QP_MANAGE_PRICING_BASES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `qpPricingBases`

## Dependency

Complete `Manage Price Elements` (`ORA_QP_MANAGE_PRICE_ELEMENTS`) before preparing, validating, or importing Pricing Bases setup data.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader` using qpPricingBases as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Pricing`
- Setup task name: `Manage Pricing Bases`
- Setup task code: `ORA_QP_MANAGE_PRICING_BASES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `qpPricingBases` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "qpPricingBases" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Pricing Bases` under `Pricing`.
