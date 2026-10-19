---
task_code: "EGO_MANAGE_ADVANCED_ITEM_PROFILE_OPTIONS"
task_name: "Manage Advanced Item Profile Options"
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
profile_option_codes:
  - "EGP_ITEM_IMPORT_DEFAULT_CATG"
  - "EGO_UNASSIGN_PACK_CATALOG_CATEGORY"
  - "EGI_ALLOW_ITEM_CREATE_DQ_MATCH_FOUND"
  - "ORA_EGO_ENFORCE_DATA_SECURITY"
  - "ORA_EGP_ITEM_SEARCH_TYPE_DELAY"
  - "EGO_VER_LINE_ACTIVATE_MAX_PARALLEL_THREADS"
  - "ORA_EGP_ENABLE_SMART_SPREADHSEET_ITEM_BATCH_OPTIONS"
  - "ORA_EGP_ITEM_SEARCH_CHAR_LIMIT"
  - "EGI_PUBLICATION_SIZE_OF_ZIP_FILE"
  - "EGP_UCM_URL"
  - "EGO_ASSIGN_PACK_ORG"
  - "EGO_DEFAULT_STYLE_CATALOG"
  - "EGO_DEFAULT_STYLE_ITEM_ORG"
  - "EGO_DEFAULT_STYLE_SUP_SITE_ORG"
  - "EGO_GATHER_STATS"
  - "EGI_PUBLICATION_ITEMS_PER_PAYLOAD"
  - "EGI_PUBLICATION_NUMBER_OF_PAYLOADS"
  - "EGO_ASSIGN_PACK_SUP_SITE_ORG"
  - "EGO_DEFAULT_STYLE_PEOPLE"
  - "EGO_VER_LINE_ACTIVATE_COUNT_PER_THREAD"
  - "ORA_EGP_EXPORT_ITEM_ROWLIMIT"
  - "ORA_EGP_SKIP_ELASTIC_SEARCH_INGEST"

source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Advanced Item Profile Options

## Setup Task Metadata

- Task name: `Manage Advanced Item Profile Options`
- Task code: `EGO_MANAGE_ADVANCED_ITEM_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``
- Core routing skill: `core.fusion-api.apps-common`

## Application Common Profile Option Routing

Advanced Item Profile Options are available only with an Oracle Product Hub
license and product-data-steward privileges. Route eligible configuration work
to `core.fusion-api.apps-common` as a profile option request. The core skill
selects its Profile Options workflow and owns Fusion resource access; do not
call a Fusion profile option endpoint directly from this task guidance.

### Fetching Advanced Item Profile Options

For a request to fetch or display values for this setup task, use only the
codes in `profile_option_codes` above. Do not broaden the result set to all
options owned by the `EGP` application, because that includes options outside
the **Manage Advanced Item Profile Options** task.

Retrieve only the Site-level configuration for each listed code:

1. Read the profile definition and confirm that the `SITE` level is enabled.
2. Read its `siteProfileOptionValues` child resource.
3. Display one row per listed profile option with the profile option code,
   display name, Site-level status, and Site-level value. Show an unset value
   as `—`.

Exclude product- and user-level values from this task's fetch output. If a
listed profile has Site level disabled, include it with the status
`Disabled` and do not substitute a value from another level.

The task catalog identifies these 22 codes for this task. Consult Oracle's
[Advanced Item Profile Options](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faipr/advanced-item-profile-options.html)
documentation when the catalog needs to be revised:

- `EGP_ITEM_IMPORT_DEFAULT_CATG`
- `EGO_UNASSIGN_PACK_CATALOG_CATEGORY`
- `EGI_ALLOW_ITEM_CREATE_DQ_MATCH_FOUND`
- `ORA_EGO_ENFORCE_DATA_SECURITY`
- `ORA_EGP_ITEM_SEARCH_TYPE_DELAY`
- `EGO_VER_LINE_ACTIVATE_MAX_PARALLEL_THREADS`
- `ORA_EGP_ENABLE_SMART_SPREADHSEET_ITEM_BATCH_OPTIONS`
- `ORA_EGP_ITEM_SEARCH_CHAR_LIMIT`
- `EGI_PUBLICATION_SIZE_OF_ZIP_FILE`
- `EGP_UCM_URL`
- `EGO_ASSIGN_PACK_ORG`
- `EGO_DEFAULT_STYLE_CATALOG`
- `EGO_DEFAULT_STYLE_ITEM_ORG`
- `EGO_DEFAULT_STYLE_SUP_SITE_ORG`
- `EGO_GATHER_STATS`
- `EGI_PUBLICATION_ITEMS_PER_PAYLOAD`
- `EGI_PUBLICATION_NUMBER_OF_PAYLOADS`
- `EGO_ASSIGN_PACK_SUP_SITE_ORG`
- `EGO_DEFAULT_STYLE_PEOPLE`
- `EGO_VER_LINE_ACTIVATE_COUNT_PER_THREAD`
- `ORA_EGP_EXPORT_ITEM_ROWLIMIT`
- `ORA_EGP_SKIP_ELASTIC_SEARCH_INGEST`

The task catalog is the authoritative scope for retrieval. Do not add related
item profile options unless the task catalog is explicitly updated.

Provide the following routing context:

- Offering: `Product Management`
- Functional area: `Items`
- Setup task: `Manage Advanced Item Profile Options` (`EGO_MANAGE_ADVANCED_ITEM_PROFILE_OPTIONS`)

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Advanced Item Profile Options`
- Setup task code: `EGO_MANAGE_ADVANCED_ITEM_PROFILE_OPTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Advanced Item Profile Options` under `Items`.
