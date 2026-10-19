---
task_code: "BEN_MANAGE_PROGRAMS_PLAN_YEARS"
task_name: "Year Periods and Billing Calendars"
parent_skill_id: "hcm.benefits-configuration.benefits-billing"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Billing"
functional_area_code: "ORA_BENEFITS_BILLING"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "benefitBillCalendars"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Year Periods and Billing Calendars

## Setup Task Metadata

- Task name: `Year Periods and Billing Calendars`
- Task code: `BEN_MANAGE_PROGRAMS_PLAN_YEARS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `benefitBillCalendars`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Year Periods and Billing Calendars` under `Benefits Billing`.
