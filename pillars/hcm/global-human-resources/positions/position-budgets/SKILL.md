---
skill_id: "hcm.global-human-resources.positions.position-budgets"
name: "Position Budgets Setup Task Guidance"
description: "Provides task-specific setup guidance for Position Budgets under the Positions functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Positions"
functional_area_code: "ORA_POSITIONS"
task_code: "CUSTOM_POSITION_BUDGETS"
task_name: "Position Budgets"
parent_skill_id: "hcm.global-human-resources.positions"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "PositionBudget"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.0"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
  - "hcm.global-human-resources.enterprise.manage-enterprise-hcm-information"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/position-budgets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/position-budgets/current/"
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

# Position Budgets Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Position Budgets` under `Positions`.

## Task Overview

Use this task to plan and govern `Position Budgets` configuration in Global Human Resources.

- **Task identity:** `CUSTOM_POSITION_BUDGETS` — Position Budgets.
- **Scope:** HCM → Global Human Resources → Positions.
- **Catalog routing:** CSV export/import support is `N`; the declared Data Loader mode is `REST` with `PositionBudget`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `CUSTOM_POSITION_BUDGETS`
- task_name: `Position Budgets`
- parent_skill_id: `hcm.global-human-resources.positions`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Positions`
- functional_area_code: `ORA_POSITIONS`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `PositionBudget`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Position Budgets` under `Positions`.

## Setup Task Metadata

- Task name: `Position Budgets`
- Task code: `CUSTOM_POSITION_BUDGETS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `PositionBudget`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `PositionBudget` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "PositionBudget" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Core Data Loader preparation, immutable preview, and approval workflow.

## CRUD Routing

- Do not run export as a prerequisite.
- Treat `positionBudgets` and `position-budgets` as aliases for Position Budgets.
- Read and search requests use the read-only REST resource `/hcmRestApi/resources/{version}/positionBudgets`.
- Create, edit, and delete requests use `core.data-loader`. Run every applicable declared read and task rule in graph order. When the graph returns `PB.LOADER_READY`, invoke Core as a task-routed request with task metadata, project context, `PositionBudget`, operation, and resolved business values. Keep control until Core returns the immutable ZIP preview; do not pause at an intermediate validation, lookup, dependency, mapping, template, or source step. Then wait for standalone `approve`; ask only for unresolved business input.
- Do not issue mutating Fusion REST calls for Position Budgets. Core Data Loader owns mutation preparation, immutable preview, explicit approval, submission, and post-run diagnostics.

## Allocate By Prerequisite

Route requests for read, create, update, or delete of the profile option value `ORA_PER_POSITION_BUDGETING_ENABLED` through `hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values`. Do not construct a profile-option API request or use another setup task. Before Position Budget create or edit, use that task to read `ProfileOptionCode=ORA_PER_POSITION_BUDGETING_ENABLED`. Continue only when the resolved value is `Y`; block `N`, no match, ambiguity, or a read failure.

For every Position Budget create request, after the profile gate passes, invoke `hcm.global-human-resources.enterprise.manage-enterprise-hcm-information` to fetch the `Position Budget Configuration` context details and resolve its `AllocateBy` segment. Do not invent a context endpoint or assume an Allocate By value. Apply the same enterprise-skill dependency before an edit.

The supported nonblank values are:

- `Department`
- `Location`
- `Department and Location`

If `AllocateBy` is blank, stop before create or edit. If it must change, route the edit through `Manage Enterprise HCM Information`, then re-read the setting before preparing the Position Budget mutation.

## Required Inputs and Validation

For a Position Budget create request, collect:

- `Name`
- `Code`
- `BudgetPeriodStartYear` (present to users as **Budget Period Start Year**)

For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as `Y` and false or No as `N`; preserve `Y` or `N`; do not add an omitted attribute or change REST read values.

`BudgetPeriodStartYear` must be a four-digit year in the current, prior, or next calendar year. Do not substitute relative labels such as “this year.”

Apply the Allocate By result before invoking Core Data Loader:

| Allocate By | Required input | Resolved loader value |
|---|---|---|
| `Department` | Department | `DepartmentId` |
| `Location` | Location | `LocationId` |
| `Department and Location` | Department and Location | `DepartmentId` and `LocationId` |

Resolve supplied department and location values through the approved read/LOV path before preview. Do not send display names where the integration requires IDs.

`AllocatedHeadcount`, `AllocatedFTE`, and `AllocatedAmount` are individually optional, but at least one is required. Reject a request that omits all three.

## Mutation Safety

For edit, first read the uniquely selected Position Budget and confirm that each requested change is supported by the current business-object metadata. Pass only validated changes through a sparse Core Data Loader workbook, follow it through immutable ZIP preview, obtain explicit approval, submit once, and re-read to verify the outcome.

For delete, first read and show the selected record’s name, code, Budget Period Start Year, department, location, and allocation values. Position Budgets have no date-effective delete path. Require explicit confirmation identifying the selected budget, then perform the one approved delete through `core.data-loader`; do not substitute a date-end operation or retry automatically.

Keep `PositionBudgetId`, `DepartmentId`, and `LocationId` internal. Use them only for system routing and record resolution; never show them in user-facing search, detail, preview, success, or delete-confirmation output.

For a search that returns zero or more than one candidate, do not select a record. Request a narrower name, code, or an explicit selected result.



## Uniform Authoring and Read Contract

- Interpret each supplied business attribute within its intended parent or child section using the current operation-specific Data Loader metadata and REST `describe`. Match the exact technical name first, then an exact normalized display label or declared alias, then one unique case-, space-, and punctuation-insensitive match. If multiple fields remain plausible, show their business labels and ask the user to choose; if none match, report the field as unsupported. Never guess or copy a value between fields.
- For create or edit, map only resolved user values to the exact business-object section, resolve references through declared task resolvers, preserve omitted existing values, and author only requested or operation-required rows and fields through the existing mutation route.
- Determine mandatory input only from current operation-specific metadata and operation-required business identity. Never require or populate a nonmandatory field merely because it appears in a template, example, or response. EFF or Additional Information contexts and segments are always optional and must never be requested as a prerequisite; emit an EFF row only when the user explicitly requests that change, using only its resolved context, identity, changed values, and any fields current metadata requires for that included row.
- Never hard-code a business value from an example. Apply a fixed default only when the task defaulting rules and current metadata confirm it for the exact operation; otherwise omit an optional field or ask only when current metadata marks it required. Fixed technical discriminators are allowed only where the task contract requires them to identify the exact business-object section.
- For a normal read, present business-facing labels and values. Do not show WHO or history columns such as `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, or `LastUpdateLogin`, or primary/surrogate identifiers, unless the user explicitly asks for them; retain identifiers internally for linking and mutation.
- When the user asks for complete details, read the exact parent without a restrictive field projection, expand every task-supported child or EFF collection by following server-returned links, paginate every collection, and return all current business attributes and child values after the same WHO/ID filtering. State when no supported child collection exists or none is returned; never invent a child path.

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

Use the parent functional-area skill `hcm.global-human-resources.positions` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.


## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Error handling](ora-resource/ora_error_handling.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
