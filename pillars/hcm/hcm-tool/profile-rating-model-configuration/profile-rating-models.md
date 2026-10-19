---
task_code: "HRT_MANAGE_PROFILE_RATING_MODELS"
task_name: "Profile Rating Models"
parent_skill_id: "hcm.hcm-tool.profile-rating-model-configuration"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Rating Model Configuration"
functional_area_code: "CUSTOM_PROFILE_RATING_MODEL"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Profile Rating Models

## Setup Task Metadata

- Task name: `Profile Rating Models`
- Task code: `HRT_MANAGE_PROFILE_RATING_MODELS`
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
- Functional area / Setup Object: `Profile Rating Model Configuration`
- Setup task name: `Profile Rating Models`
- Setup task code: `HRT_MANAGE_PROFILE_RATING_MODELS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Profile Rating Models` under `Profile Rating Model Configuration`.

## V1 Execution Contract

- The functional-area skill owns one create-or-reuse request and its complete
  header, levels, applicable optional components, translations, validation,
  read-back, and downstream handoffs.
- Keep `FSM` as the catalog import route. Use `core.data-loader` to inspect the
  current task/package contract before authoring or importing any source.
- `Rating Model` HDL is an alternative only when the target environment's
  current **View Business Objects** metadata proves the full component
  hierarchy and attributes needed by the approved blueprint.
- REST is read-only, release-gated evidence. The source-backed
  `talentRatingModels` resource is unlisted; never call its create, update,
  delete, or batch write operations.
- V1 never updates or deletes an existing model. It either reuses one exact
  suitable model or prepares one new model after the normal Data Loader
  immutable-preview approval.
- Downstream associations remain with the consumer-owning setup skills.
