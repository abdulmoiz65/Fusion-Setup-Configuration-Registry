---
task_code: "HRT_MANAGE_PROFILE_TYPES"
task_name: "Profile Types"
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

# Profile Types

## Setup Task Metadata

- Task name: `Profile Types`
- Task code: `HRT_MANAGE_PROFILE_TYPES`
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

For an FSM ZIP, Core Data Loader completes immutable preflight and approval,
then routes the approved package through its authorized task-level adapter.
Require the returned `ProcessId` and ProcessLog; do not use generic Data Loader
initiation.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Types and Content Section Configuration`
- Setup task name: `Profile Types`
- Setup task code: `HRT_MANAGE_PROFILE_TYPES`

For a current-instance data export, use data mode and persist the unchanged ZIP
under the project export workspace. Require explicit approval immediately before
the shared exporter creates the Fusion export process. A request for one seeded
Profiles V2 type is filtered scope: use export criteria only when live task or
provider metadata confirms the exact criterion fields. Never use the seeded
type ID/key as `ProfileTypeCode` or `ProfileUsageCode`, and never silently widen
an unconfirmed filtered request to a full-task export.




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Profile Types` under `Profile Types and Content Section Configuration`.
