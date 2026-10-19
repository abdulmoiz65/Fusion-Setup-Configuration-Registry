---
task_code: "EGP_MANAGE_DEFAULT_ITEM_CLASS"
task_name: "Manage Default Item Class"
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

# Manage Default Item Class

## Setup Task Metadata

- Task name: `Manage Default Item Class`
- Task code: `EGP_MANAGE_DEFAULT_ITEM_CLASS`
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
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Default Item Class`
- Setup task code: `EGP_MANAGE_DEFAULT_ITEM_CLASS`

## FSM Import Package Contract

For every `Manage Default Item Class` import, include these required data members at the ZIP root, followed by `ASM_SETUP_CSV_METADATA.xml` from the same exported template package:

1. `EGP_ITEM_CLASS.csv` - include the `ROOT_ICC` item-class row using the complete, unchanged current-template header and column order.
2. `ORA_EGP_ITEM_CLASS_PHASE_ASSIGNMENT.csv` - include the lifecycle-phase assignment rows for `ROOT_ICC` using the complete, unchanged current-template header and column order.

Include `ORA_ITEM_CLASS_ATTACH_CATEGORY.csv` only when the user provides attachment categories to associate with `ROOT_ICC`; otherwise omit that CSV member from the upload ZIP.

Always default `EntityName` to `ITEM_ENTITY`; the user cannot override this value.

Do not submit a phase-assignment-only package. Preserve all template-defined fields, leave only template-permitted optional fields blank, and validate every included CSV member against the exact template before approval. `ROOT_ICC` remains mandatory and cannot be overridden.


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Default Item Class` under `Items`.

## Invocation Triggers

Interpret the following case-insensitive phrases as an explicit request to execute `Manage Default Item Class` for the listed operation. `root ic` and `ROOT ICC` are aliases for this task only; the enforced item class code remains `ROOT_ICC`.

| Operation | Trigger Phrases | Required Route |
|---|---|---|
| Export | export root ic; export ROOT ICC; export default item class | shared.setup-export.task-level-export |
| Import | import root ic; import ROOT ICC; import default item class | core.data-loader |

For either operation, use task code `EGP_MANAGE_DEFAULT_ITEM_CLASS` and follow the task's applicable validation and template gates.
