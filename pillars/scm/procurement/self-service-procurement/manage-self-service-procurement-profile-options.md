---
task_code: "POR_MANAGE_SELF_SERVICE_PROCUREMENT_PROFILE_OPTIONS"
task_name: "Manage Self Service Procurement Profile Options"
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

# Manage Self Service Procurement Profile Options

## Setup Task Metadata

- Task name: `Manage Self Service Procurement Profile Options`
- Task code: `POR_MANAGE_SELF_SERVICE_PROCUREMENT_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Direct profile-option route: `core.fusion-api.apps-common`

## Profile Option Routing

Route profile-option definition reads, configured-value reads, effective-value
verification, and approved configured-value maintenance for this task to
`core.fusion-api.apps-common`. Use each code below as the exact
`ProfileOptionName`; do not resolve or mutate a profile option by its display
label:

- `POR_REQUESTED_DATE_OFFSET`
- `POR_ASSIGN_REQ_SAME_BUYER`
- `POR_RETAIN_LAST_ASSIGNED_BUYER`
- `POR_DISPLAY_CATEGORY_ITEM_COUNT`
- `POR_SEARCH_RESULTS_SKIN`

Treat this list as the task allowlist. Stop before making a Fusion call when a
request contains a different profile option code or an ambiguous identity.

For each allowed code, let `core.fusion-api.apps-common`:

1. Read `/profileOptions/{ProfileOptionName}` to resolve the profile definition
   and its enabled and updatable levels.
2. Read the current site-, product-, or user-level value through the applicable
   `profileOptions` child resource. Use `profileValues` only to verify the
   effective value for the authenticated user session.
3. For a proposed write, validate the exact environment, profile level, level
   key, current value, intended value, and
   `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` privilege.
4. Present the exact target and change for explicit approval immediately before
   one `POST`, `PATCH`, or `DELETE`; do not retry a mutating request
   automatically.
5. Return redacted execution evidence including the operation, endpoint path,
   HTTP outcome, and request ID or ECID when Fusion supplies one.

Use `SITE` for the site-level item key, the application short name for a
product-level `LevelValue`, and a Fusion-resolved user GUID when creating a
user-level value. Never use a `profileValues_Id` as a `profileOptions` key, and
do not implement task-local OAuth or REST transport.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.
4. Route direct reads and approved configured-value maintenance for the five
   allowed profile option codes through `core.fusion-api.apps-common`; do not
   use `core.data-loader` for an individual profile-option REST operation.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Self Service Procurement`
- Setup task name: `Manage Self Service Procurement Profile Options`
- Setup task code: `POR_MANAGE_SELF_SERVICE_PROCUREMENT_PROFILE_OPTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Self Service Procurement Profile Options` under `Self Service Procurement`.

## Sources

- `core/fusion-api/apps-common/SKILL.md`
- `core/fusion-api/apps-common/references/profile-options.md`
- Developer-provided Fusion Setup UI profile option codes, received
  `2026-08-20`
