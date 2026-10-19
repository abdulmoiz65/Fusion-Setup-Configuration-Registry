---
task_code: "ORA_CJM_MANAGE_CHANNEL_PROFILE_OPTIONS"
task_name: "Manage Channel Profile Options"
parent_skill_id: "scm.order-management.channel-revenue-management"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Channel Profile Options

## Setup Task Metadata

- Task name: `Manage Channel Profile Options`
- Task code: `ORA_CJM_MANAGE_CHANNEL_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Profile Option Value Routing

For effective-value reads and configured-value review, create, update, or
delete activity, default to `core.fusion-api.apps-common`. That entry point
must select `core.fusion-api.apps-common.profile-options` for the
profile-option workflow. This default applies to every resolved Channel
Revenue Management profile-option code.

Task-scoped Channel Revenue Management resource rules supplement this route
only when an approved, code-specific validation or live-lookup contract is
documented. They do not create a static value list, range, or lookup mapping
for other profile-option codes; Apps Common reads the current Fusion profile
definition and performs the standard profile-option workflow for those codes.

Do not use FSM, CSV import, `core.data-loader`, browser interaction, or a
direct REST client to mutate a configured value for this profile option. Before
any write, read the exact profile definition and relevant Site, Product, or
User value; confirm that the selected level is enabled and updatable; then
obtain explicit approval for the target environment, level, current state, and
proposed value. Do not automatically retry a failed or indeterminate write.

Use `core.data-loader` only when the supplied source is independently validated
as a supported Fusion import artifact for non-profile-value task setup data.
It is not a fallback for an Apps Common authentication, authorization,
validation, transport, API, or write failure, and it must not be used to
mutate configured profile-option values.

### User-Scope Identity Resolution

For a User-level profile value, resolve the supplied username
case-insensitively through the Apps Common profile-options workflow before
building the write preview. Continue only when the lookup returns exactly one
Fusion user. Use the returned canonical username in the item route and the
returned User GUID as `LevelValue` in a create request; never send the supplied
username variant as a GUID. No match or more than one case-insensitive match is
a validation blocker, not a Data Loader fallback or a reason to guess a user.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

These CSV routes apply only to supported task setup-data activities. They do
not override the Apps Common route for configured-value activity on
`CJM_CURRENCY_CONVERSION_TYPE`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Profile Options`
- Setup task code: `ORA_CJM_MANAGE_CHANNEL_PROFILE_OPTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Profile Options` under `Channel Revenue Management`.
