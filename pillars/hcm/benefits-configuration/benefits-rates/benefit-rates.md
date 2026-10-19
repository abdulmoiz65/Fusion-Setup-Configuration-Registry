---
task_code: "BEN_MANAGE_BENEFIT_RATES"
task_name: "Benefit Rates"
parent_skill_id: "hcm.benefits-configuration.benefits-rates"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Rates"
functional_area_code: "ORA_BENEFITS_RATES"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "HDL"
businessObject: "BenefitsStandardRate"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Benefit Rates

## Setup Task Metadata

- Task name: `Benefit Rates`
- Task code: `BEN_MANAGE_BENEFIT_RATES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `HDL`
- Business Object: `BenefitsStandardRate`

## HDL Object Selection

The generated `businessObject` metadata above is the standard-rate default,
not a restriction on explicit variable-rate-profile requests. Use the
[parent skill's upload routing table](SKILL.md#upload-routing) to select the
root for each source: `BenefitsStandardRate` for standard rates and its
`ExtraInputValue` / `VrpAssociation` children, or `VariableRateProfile` for
profiles. Both routes retain this task identity and core.data-loader's
validation, Task Hook, approval, upload, and status workflow. Children are not
independent root business objects.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Benefit Rates` under `Benefits Rates`.
