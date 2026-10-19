---
task_code: "ORA_RCS_MANAGE_UOM_PROFILE"
task_name: "Manage Units of Measure Profiles"
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
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Units of Measure Profiles

## Setup Task Metadata

- Task name: `Manage Units of Measure Profiles`
- Task code: `ORA_RCS_MANAGE_UOM_PROFILE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Direct profile-option route: `core.fusion-api.apps-common`

## Profile Option Routing

Route direct profile-option reads and approved configured-value maintenance to
`core.fusion-api.apps-common`, which must select its `profile-options` nested
skill. Use only these exact `ProfileOptionName` values for this task:

| Profile option code | Level | Required value constraint |
| --- | --- | --- |
| `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` | Site | A UOM class for service duration (for example, `Time`). |
| `ORA_RCS_HOUR_UOM` | Site | A UOM representing one hour and belonging to the class configured by `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION`. |
| `INV_QUANTITY_DECIMAL_PRECISION` | Site | The decimal precision used for quantity fields. |
| `ORA_RCS_PACKAGING_STRING_DISPLAY_FIELD` | Site | The packaging attribute selected for display. |
| `ORA_RCS_PACKAGING_STRING_ORDER` | Site | The order in which packaging-string attributes are displayed. |
| `RCS_DEFAULT_UOM_SERVICE_DURATION_CLASS` | Site | A UOM class for service duration. |
| `RCS_DURATION_DECIMAL_PRECISION` | Site | The decimal precision used to round lead-time values. |

Read the profile definition and current Site value before a change. For any
write, validate the target environment, UOM-class identity, and intended
stored value, then obtain explicit approval immediately before the single
mutation. Do not implement task-local OAuth or REST transport.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.
4. Route direct reads and approved value maintenance for the listed profile
   option codes through `core.fusion-api.apps-common`; do not use
   `core.data-loader` for an individual profile-option REST operation.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Units of Measure Profiles`
- Setup task code: `ORA_RCS_MANAGE_UOM_PROFILE`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Units of Measure Profiles` under `Items`.

## Sources

- `core/fusion-api/apps-common/SKILL.md`
- `core/fusion-api/apps-common/profile-options/SKILL.md`
- `core/fusion-api/apps-common/profile-options/references/profile-options.md`
- [Oracle: How Work Orders Are Scheduled](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/faumf/how-work-orders-are-scheduled.html)
