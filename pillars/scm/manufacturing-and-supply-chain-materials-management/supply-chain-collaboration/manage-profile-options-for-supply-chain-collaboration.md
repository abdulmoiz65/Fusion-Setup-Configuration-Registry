---
task_code: "ORA_VCS_MANAGE_SUPPY_CHAIN_COLLAB_PROFILE_OPTIONS"
task_name: "Manage Profile Options for Supply Chain Collaboration"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-collaboration"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Collaboration"
functional_area_code: "ORA_VCS_SUPPLY_COLLABORATION"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/release/setupTasksAll.json"
uses_core:
  - "core.fusion-api.apps-common"
---

# Manage Profile Options for Supply Chain Collaboration

## Setup Task Metadata

- Task name: `Manage Profile Options for Supply Chain Collaboration`
- Task code: `ORA_VCS_MANAGE_SUPPY_CHAIN_COLLAB_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `shared.setup-import.task-level-import`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Supply Chain Collaboration`
- Setup task name: `Manage Profile Options for Supply Chain Collaboration`
- Setup task code: `ORA_VCS_MANAGE_SUPPY_CHAIN_COLLAB_PROFILE_OPTIONS`

## Profile Option API Routing

Route profile-option read and maintenance requests for this task to
`core.fusion-api.apps-common`, which must select its `profile-options` nested
skill. Use the applicable profile option code, requested operation, and target
level or scope; do not add Fusion authentication or REST transport logic to
this task guidance. For writes, use the core skill's read-first and explicit-
approval requirements.

| Profile option code |
| --- |
| `ORA_VCS_SC_CONFIGURATION_PAGES_REDWOOD_ENABLED` |
| `ORA_VCS_SC_NETWORK_PAGES_REDWOOD_ENABLED` |
| `ORA_VCS_SC_OVERVIEW_ORDER_FORECAST_PAGES_REDWOOD_ENABLED` |
| `ORA_VCS_SC_SUPPLY_DATA_PAGES_REDWOOD_ENABLED` |
| `ORA_VCS_VMI_CONFIGURATION_PAGES_REDWOOD_ENABLED` |
| `ORA_VCS_VMI_NETWORK_PAGE_REDWOOD_ENABLED` |
| `ORA_VCS_VMI_TRANSACTION_PAGES_REDWOOD_ENABLED` |


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Profile Options for Supply Chain Collaboration` under `Supply Chain Collaboration`.
