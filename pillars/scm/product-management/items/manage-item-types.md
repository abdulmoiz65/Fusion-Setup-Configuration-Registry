---
task_code: "EGP_MANAGE_ITEM_TYPES"
task_name: "Manage Item Types"
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
lookup_code: "EGP_ITEM_TYPE"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Item Types

## Setup Task Metadata

- Task name: `Manage Item Types`
- Task code: `EGP_MANAGE_ITEM_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Core routing skill: `core.fusion-api.apps-common`
- Lookup code: `EGP_ITEM_TYPE`

## Application Common Lookup Routing

Route Item Types lookup work to `core.fusion-api.apps-common` with lookup
code `EGP_ITEM_TYPE`. The core skill selects the applicable lookup workflow
and owns lookup-resource access; do not call a Fusion lookup endpoint directly
from this task guidance.

Oracle Product Management documentation identifies `EGP_ITEM_TYPE` as the
lookup type used to add user item types through the Manage Item Types task.
Source: [How can I modify the default value for the User Item Type attribute?](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faipr/how-can-i-modify-the-default-value-for-the-user-item-type-attribute.html).

Provide the following routing context:

- Lookup code: `EGP_ITEM_TYPE`
- Offering: `Product Management`
- Functional area: `Items`
- Setup task: `Manage Item Types` (`EGP_MANAGE_ITEM_TYPES`)

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Item Types`
- Setup task code: `EGP_MANAGE_ITEM_TYPES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Item Types` under `Items`.
