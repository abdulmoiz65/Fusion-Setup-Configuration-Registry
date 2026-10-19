---
task_code: "ORA_RCS_MANAGE_MFG_PLANT_PROFILE"
task_name: "Manage Plant Profiles"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.facilities"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Facilities"
functional_area_code: "ORA_RCS_FACILITIES"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Plant Profiles

## Setup Task Metadata

- Task name: `Manage Plant Profiles`
- Task code: `ORA_RCS_MANAGE_MFG_PLANT_PROFILE`
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
skill. The sole allowed `ProfileOptionName` for this task is
`RCS_DEFAULT_MFG_PLANT_ORG`:

| Profile option code | Level | Required value constraint |
| --- | --- | --- |
| `RCS_DEFAULT_MFG_PLANT_ORG` | User | An existing manufacturing plant organization available to the user. |

Read the profile definition and its current scoped value before a change. For
any write, validate the level, scope key, target environment, and intended
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

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Facilities`
- Setup task name: `Manage Plant Profiles`
- Setup task code: `ORA_RCS_MANAGE_MFG_PLANT_PROFILE`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Plant Profiles` under `Facilities`.

## Sources

- `core/fusion-api/apps-common/SKILL.md`
- `core/fusion-api/apps-common/profile-options/SKILL.md`
- `core/fusion-api/apps-common/profile-options/references/profile-options.md`
- [Oracle: How You Set Up Manufacturing](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faims/how-you-set-up-manufacturing.html)
