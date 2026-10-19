---
task_code: "ORA_RCS_MANAGE_CALENDAR_PROFILE_OPTION"
task_name: "Manage SCM Enterprise Calendar Profile Option"
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

# Manage SCM Enterprise Calendar Profile Option

## Setup Task Metadata

- Task name: `Manage SCM Enterprise Calendar Profile Option`
- Task code: `ORA_RCS_MANAGE_CALENDAR_PROFILE_OPTION`
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
`ZCA_COMMON_CALENDAR` (Accounting Calendar Default).

Use the Site level and set its value to the selected enterprise accounting
calendar. The selected value must be the same calendar used by CRM, as the
task catalog requires. Read the profile definition and current Site value
before a change; validate the target environment and calendar identity, then
obtain explicit approval immediately before the single mutation. Do not
implement task-local OAuth or REST transport.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.
4. Route direct reads and approved value maintenance for
   `ZCA_COMMON_CALENDAR` through `core.fusion-api.apps-common`; do not use
   `core.data-loader` for this individual profile-option REST operation.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Facilities`
- Setup task name: `Manage SCM Enterprise Calendar Profile Option`
- Setup task code: `ORA_RCS_MANAGE_CALENDAR_PROFILE_OPTION`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage SCM Enterprise Calendar Profile Option` under `Facilities`.

## Sources

- `core/fusion-api/apps-common/SKILL.md`
- `core/fusion-api/apps-common/profile-options/SKILL.md`
- `core/fusion-api/apps-common/profile-options/references/profile-options.md`
- [Oracle: Create the Accounting Calendar](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faicf/create-the-accounting-calendar.html)
