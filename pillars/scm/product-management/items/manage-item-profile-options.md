---
task_code: "EGP_MANAGE_ITEM_PROFILE_OPTIONS"
task_name: "Manage Item Profile Options"
parent_skill_id: "scm.product-management.items"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
profile_option_codes:
  - "EGP_DISPLAY_IMAGES"
  - "ORA_EGP_TPI_UPDATEABLE"
  - "EGP_CONVERSION_MODE"
  - "EGP_ITEM_IMPORT_ITEMS_PER_THREAD"
  - "EGP_ITEM_IMPORT_NUMBER_OF_THREADS"
  - "EGP_UPDATEABLE_ITEM"

source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Item Profile Options

## Setup Task Metadata

- Task name: `Manage Item Profile Options`
- Task code: `EGP_MANAGE_ITEM_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Core routing skill: `core.fusion-api.apps-common`

## Application Common Profile Option Routing

Route Item Profile Options configuration work to
`core.fusion-api.apps-common` as a profile option request. The core skill
selects its Profile Options workflow and owns Fusion resource access; do not
call a Fusion profile option endpoint directly from this task guidance.

Oracle's [Item Profile Options](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faipr/item-profile-options.html)
documentation identifies the following codes for this setup area:

- `EGP_DISPLAY_IMAGES`
- `EGP_UPDATEABLE_ITEM`
- `EGP_ITEM_IMPORT_ITEMS_PER_THREAD`
- `EGP_ITEM_IMPORT_NUMBER_OF_THREADS`
- `ORA_EGP_TPI_UPDATEABLE`
- `EGP_CONVERSION_MODE`

Provide the following routing context:

- Offering: `Product Management`
- Functional area: `Items`
- Setup task: `Manage Item Profile Options` (`EGP_MANAGE_ITEM_PROFILE_OPTIONS`)

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Item Profile Options`
- Setup task code: `EGP_MANAGE_ITEM_PROFILE_OPTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Item Profile Options` under `Items`.
