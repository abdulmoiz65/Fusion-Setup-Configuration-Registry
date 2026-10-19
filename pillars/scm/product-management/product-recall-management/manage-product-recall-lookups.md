---
task_code: "ORA_MANAGE_PRODUCT_RECALL_LOOKUPS"
task_name: "Manage Product Recall Lookups"
parent_skill_id: "scm.product-management.product-recall-management"
pillar: "SCM"
offering: "Product Management"
functional_area: "Product Recall Management"
functional_area_code: "ORA_ENQ_PRODUCT_RECALL_MANAGEMENT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Product Recall Lookups

## Setup Task Metadata

- Task name: `Manage Product Recall Lookups`
- Task code: `ORA_MANAGE_PRODUCT_RECALL_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Lookup Management Routing

Route all lookup reads and approved lookup-code maintenance for this task to
`core.fusion-api.apps-common`. That core skill owns OAuth, lookup-category
discovery, Fusion REST transport, and the read-before-write approval gate.

Use the following lookup types as the task allowlist:

### User-extensible lookups

- `ORA_SCH_CLASSIFICATION`
- `ORA_SCH_PRM_PRODUCT_TYPES`
- `ORA_SCH_PRM_SKIP_TASKS_ACTIONS`
- `ORA_SCH_RECALL_WITHDRAW_REASON`

### System lookups

- `ORA_SCH_DELETION_TYPE`
- `ORA_SCH_DISPOSITION_METHOD`
- `ORA_SCH_INBOUND_TXN_TYPE`
- `ORA_SCH_IN_RECALL_NOTICE_TYPE`
- `ORA_SCH_LINE_DETAILS_ACTION`
- `ORA_SCH_MAIL_SERVER_TYPE`
- `ORA_SCH_PRM_AI_MATCH_TYPE`
- `ORA_SCH_NOTICE_TYPE`
- `ORA_SCH_PRM_AI_RECALL_STATUS`
- `ORA_SCH_PRM_BYPASS_TASK_METHOD`
- `ORA_SCH_PRM_COUNT_TASK_STATUS`
- `ORA_SCH_PRM_DOC_EXTR_STATUS`
- `ORA_SCH_PRM_DOC_RECEIVED_MODE`
- `ORA_SCH_PRM_INBOUND_RES_METHOD`
- `ORA_SCH_PRM_MODE_OF_CAPTURE`
- `ORA_SCH_PRM_RECALL_MAT_STATUS`
- `ORA_SCH_PRM_SKIP_TASKS_STATUS`
- `ORA_SCH_PRM_TASK_EVENT`
- `ORA_SCH_PRODUCT_TRACE_GROUPING`
- `ORA_SCH_RECALL_COPY_ACTION`
- `ORA_SCH_RECALL_DEVICE_CLASS`
- `ORA_SCH_RECALL_HEADER_STATUS`
- `ORA_SCH_RECALL_LINE_STATUS`
- `ORA_SCH_REC_LOT_SER_OPTIONS`
- `ORA_SCH_REC_SERIAL_MODE`
- `ORA_SCH_REPLACEMENT_TYPE`
- `ORA_SCH_SOURCE_TYPE`
- `ORA_SCH_TASK_STATUS`
- `ORA_SCH_TRACE_STATUS`

Only the four types under **User-extensible lookups** may be extended through
this task. Treat the 29 types under **System lookups** as system-managed: read
them for reference, but do not add, change, or delete their codes.

For each type, `core.fusion-api.apps-common` must first determine the exact
lookup category through its read-only discovery order. It must stop on an
authorization failure and obtain explicit approval immediately before any
create, update, or delete.

## Run Book Routing

Route Run Book planning, selection, task dashboards, task details, and task
status tracking for this setup task to `core.runbook`. Use it to view or select
the applicable Run Book and to inspect this task's progress or associated Data
Loader status. Creating a Run Book or changing a task's comments, status, or
completion percentage requires the explicit authorization required by
`core.runbook`.

When a selected Run Book has an active `runID` and Run Book Task Validation is
enabled, let `core.data-loader` perform that validation as part of an import;
do not invoke Run Book REST operations as an import shortcut.

## CSV Export, Import, and Validation Metadata

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with
   `shared.validation.setup-data-validator`.
3. Route every CSV/FSM setup-data import through `core.data-loader`. It owns
   source validation, immutable approval preview, explicit approval, upload,
   initiation, and any enabled Run Book Task Validation.
4. Route lookup reads and approved lookup-code maintenance through
   `core.fusion-api.apps-common`; do not use `core.data-loader` for a direct
   lookup REST operation.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Product Recall Management`
- Setup task name: `Manage Product Recall Lookups`
- Setup task code: `ORA_MANAGE_PRODUCT_RECALL_LOOKUPS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Product Recall Lookups` under `Product Recall Management`.
