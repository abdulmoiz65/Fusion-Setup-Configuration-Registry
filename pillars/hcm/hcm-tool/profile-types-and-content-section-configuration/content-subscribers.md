---
task_code: "HRT_MANAGE_CONTENT_SUBSCRIBERS"
task_name: "Content Subscribers"
parent_skill_id: "hcm.hcm-tool.profile-types-and-content-section-configuration"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Types and Content Section Configuration"
functional_area_code: "CUSTOM_PROFILE_TYPES_AND_CONTENT_SECTION"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Content Subscribers

## Setup Task Metadata

- Task name: `Content Subscribers`
- Task code: `HRT_MANAGE_CONTENT_SUBSCRIBERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Types and Content Section Configuration`
- Setup task name: `Content Subscribers`
- Setup task code: `HRT_MANAGE_CONTENT_SUBSCRIBERS`

For a current-instance export of the global subscriber catalog, use data mode
through `shared.setup-export.task-level-export` and preserve its returned ZIP
unchanged. Require explicit approval immediately before the live export. Do not
substitute this task for Profile Types-owned subscriber section-property rows;
export both tasks separately when both scopes are requested.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Content Subscribers` under `Profile Types and Content Section Configuration`.
