---
skill_id: "scm.product-management.structures.manage-item-structure-type-details"
name: "Manage Item Structure Type Details Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Item Structure Type Details under the Structures functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Structures"
functional_area_code: "EGO_ADVANCED_PRODUCT_STRUCT"
task_code: "EGP_MANAGE_ITEM_STRUCTURE_TYPE_DETAILS"
task_name: "Manage Item Structure Type Details"
parent_skill_id: "scm.product-management.structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.12"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/manage-item-structure-type-details/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/manage-item-structure-type-details/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Manage Item Structure Type Details Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Item Structure Type Details` under `Structures`.

## Setup Task Skill Contract

- task_code: `EGP_MANAGE_ITEM_STRUCTURE_TYPE_DETAILS`
- task_name: `Manage Item Structure Type Details`
- parent_skill_id: `scm.product-management.structures`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Structures`
- functional_area_code: `EGO_ADVANCED_PRODUCT_STRUCT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Item Structure Type Details` under `Structures`.

## Setup Task Metadata

- Task name: `Manage Item Structure Type Details`
- Task code: `EGP_MANAGE_ITEM_STRUCTURE_TYPE_DETAILS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Structures`
- Setup task name: `Manage Item Structure Type Details`
- Setup task code: `EGP_MANAGE_ITEM_STRUCTURE_TYPE_DETAILS`

## Reference Designator Options

Use the Reference Designator Range Indicator to select the special character that represents a reference-designator range. `None` is the default. Resolve a supplied code or meaning to one enabled, effective value from lookup type `ORA_EGP_COMP_REF_DES_RANGE_IND`; request another value only when that lookup cannot resolve it uniquely.

Comma-separated reference designators are supported as individual values. A range uses the selected range character, for example `RX01-RX05` when hyphen is selected. The range expansion behavior is available in the item-structure and change-order user interfaces; clients such as import, REST, and SOAP do not expand or collapse entered ranges.

Quantity Related is enabled by default for engineering and commercial items; users can still change it while maintaining individual structures.

## Parent Structure Type and Child Structure Name

For Item Structure Type setup, distinguish the seeded parent structure type
from the child structure names maintained beneath it. Preserve the exported
parent `StructureTypeId` and its business key; do not create a new parent ID
for a request that adds a structure name. The FSM CSV objects are:

- `EGP_STRUCTURE_TYPE.csv` for parent controls, including Component Item
  Sequence Increment, Quantity Related, and Reference Designator Range
  Indicator.
- `ORA_EGP_STRUCTURE_TYPE_NAME.csv` for the child internal name, display name,
  description, lifecycle validation, and Use Primary for Expansion values.
- `ORA_EGP_STRUCTURE_TYPE_ATT_CATEGORY_NAME.csv` for parent attachment
  categories.

Before preparing an FSM archive, export the current setup data. Preserve
the exact exported parent row in `EGP_STRUCTURE_TYPE.csv` whenever an archive
contains a child row in `ORA_EGP_STRUCTURE_TYPE_NAME.csv`. The parent row and
child row must carry the same exported `StructureTypeId`. For a child-only
request, copy that parent row unchanged; apply a parent-control change in that
row only when the request explicitly includes one. This archive relationship
does not authorize creating, replacing, or otherwise changing the seeded
parent. Do not include unchanged existing child rows.

Validate attachment categories only when the request supplies one or the target
setup explicitly requires one. Add the required new child row and do not add a
duplicate attachment-category row when the exact canonical category name is
already present in the export. When neither condition applies, preserve an
empty attachment list and do not block validation.

For a child-name FSM import, a Data Loader dataset upload or initiation status
is not setup-success evidence by itself. Inspect the FSM process log for a
skipped parent-row warning and confirm the requested child row in a fresh,
populated setup-data export before reporting completion.

Oracle's Setup and Maintenance user interface requires an effective start date
when a structure name is created. FSM templates can omit an effective-start-date
field. When the current template omits it, continue with the authorized FSM
import without adding a column or requiring a date; the import creates the
structure name without an effective-start-date value in the archive.

## Effective-Start-Date Handling

For each new structure name, inspect the populated FSM template before
preparing the selected route:

1. For the UI route, require the user to supply an effective start date and
   use that exact date in the runbook.
2. For FSM, populate an effective-start-date value only when the current
   template explicitly exposes a field and the user supplies a value.
3. When the FSM template omits the field, continue with the FSM archive. Do
   not add an undocumented column, request a UI date, or infer a current date.
4. Record the template-column check and the chosen handling in the validation
   evidence. Post-import verification confirms that the requested structure
   name was created; it must not claim a date that the FSM archive did not
   represent.

## Structure-Type Design Validation and Approval

For any request to create, retire, or change an item structure type, read these
task-local resources before preparing a plan, validation result, or import
handoff:

- `ora-resource/ora_input_validation.md`
- `ora-resource/ora_reference_lookups.md`
- `ora-resource/ora_defaulting_rules.md`
- `ora-resource/ora_design_enforcement.md`
- `ora-resource/ora_error_handling.md`
- `ora-resource/ora_rule_registry.json`

Follow the compiled task-node sequence in `ora_rule_registry.json`:

1. Validate the requested child display name, supplied optional settings,
   effective-date handling, and any required attachment categories. When an
   internal name is omitted, use the display name as the internal name; allow
   an empty description. When omitted, default Enable Lifecycle Validation and
   Use Primary for Expansion to false (unchecked). Preserve the seeded parent
   identifier supplied by exported data and do not generate a new
   `StructureTypeId` when adding a structure name. For an FSM archive with a
   child row, include the exact matching parent `EGP_STRUCTURE_TYPE.csv` row
   from the same fresh export.
2. When a Reference Designator Range Indicator or range is requested, resolve
   it through `resolve_rd_range_indicator_lookup_value`. Accept the supplied
   value when it resolves uniquely to an enabled, effective value in
   `ORA_EGP_COMP_REF_DES_RANGE_IND`; otherwise, request a resolvable value.
3. Preserve the seeded parent structure type. Do not delete, repurpose, or
   retire it, and do not delete or repurpose a structure name already assigned
   to items. For each FSM child row, stage the matching parent row with the
   same exported `StructureTypeId`; retain all parent values unless the request
   explicitly changes a parent control. Resolve attachment-category names from
   the populated export using their exact target-environment spelling before
   deciding whether an additive category row is needed.

These resources validate and govern the task design only. They do not authorize
a direct Fusion write. Route any approved setup-data import through
`core.data-loader` using the FSM workflow above, including its own preflight,
approval, audit, and diagnostic controls.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.product-management.structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
