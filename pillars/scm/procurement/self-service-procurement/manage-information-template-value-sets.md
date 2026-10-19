---
task_code: "POR_MANAGE_INFORMATION_TEMPLATE_VALUE_SETS"
task_name: "Manage Information Template Value Sets"
parent_skill_id: "scm.procurement.self-service-procurement"
pillar: "SCM"
offering: "Procurement"
functional_area: "Self Service Procurement"
functional_area_code: "PO_SSP_DEPLOYED"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Information Template Value Sets

## Setup Task Metadata

- Task name: `Manage Information Template Value Sets`
- Task code: `POR_MANAGE_INFORMATION_TEMPLATE_VALUE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Direct value-set route: `core.fusion-api.apps-common`

## Value Set Routing

Route value-set definition reads, table-validation metadata reads, valid-value
reads, and approved child-value maintenance for this task to
`core.fusion-api.apps-common`.

Require an exact Fusion-returned `valueSets_Id` before using an item or child
endpoint. When a request starts from a value-set code or name, query the
`valueSets` collection and continue only after one exact record is resolved;
do not derive an identifier from the code, name, or display label.

For the resolved value set, let `core.fusion-api.apps-common`:

1. Read `/valueSets/{valueSets_Id}` to retrieve the value-set definition.
2. Read the `validationTable` and `values` child resources when the request
   needs table-validation metadata or valid values.
3. Stop a request to create, update, or delete the root value-set definition;
   the Apps Common route supports root definition reads only.
4. For a proposed child-value write, validate the exact environment,
   `valueSets_Id`, returned child identifier when applicable, current value,
   intended value, request payload, and required Fusion privileges.
5. Present the exact target and change for explicit approval immediately before
   one child-value `POST`, `PATCH`, or `DELETE`; do not retry a mutating request
   automatically.
6. Return redacted execution evidence including the operation, endpoint path,
   HTTP outcome, and request ID or ECID when Fusion supplies one.

Use response identifiers exactly as returned by Fusion. Do not implement
task-local OAuth or REST transport.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.
4. Route direct value-set definition, validation-table, and valid-value reads,
   plus approved child-value maintenance, through
   `core.fusion-api.apps-common`; do not use `core.data-loader` for an
   individual value-set REST operation.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Self Service Procurement`
- Setup task name: `Manage Information Template Value Sets`
- Setup task code: `POR_MANAGE_INFORMATION_TEMPLATE_VALUE_SETS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing,
validating setup data, or reading and maintaining valid values for
`Manage Information Template Value Sets` under `Self Service Procurement`.

## Sources

- `core/fusion-api/apps-common/SKILL.md`
- `core/fusion-api/apps-common/references/value-sets.md`
