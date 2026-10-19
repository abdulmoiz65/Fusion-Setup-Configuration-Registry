---
skill_id: "scm.product-management.items.manage-import-maps"
name: "Manage Import Maps Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Import Maps under the Items functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "EGI_MANAGE_IMPORT_MAPS"
task_name: "Manage Import Maps"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "itemImportMaps"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.3.4"
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
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-import-maps/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-import-maps/current/"
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
side_effects:
  - "Reads itemClasses through core.fusion-api.rest-api-client for create-only ROOT_ICC defaulting on the REST Data Loader route."
  - "Reads standardLookups and lookupCodes through core.fusion-api.apps-common.lookups for import-map format resolution on the REST Data Loader route."
  - "Reads the selected target environment's importMapAttributes resource through core.fusion-api.rest-api-client during REST and FSM destination validation."
  - "Reads the selected target environment's importMapFunctions resource through core.fusion-api.rest-api-client during REST transformation validation."
  - "Routes an immutable FSM task-level ZIP and task context to core.data-loader; Data Loader owns preflight, Task Hook validation, approval, upload, and import initiation."
required_privileges:
  - "Fusion privileges to read itemClasses in the selected target environment."
  - "Fusion privileges to read standardLookups and their lookupCodes children in the selected target environment."
  - "Fusion privileges to read the importMapAttributes resource in the selected target environment."
  - "Fusion privileges to read the importMapFunctions resource in the selected target environment."
  - "Fusion Data Loader privileges to upload and initiate the FSM ZIP for task EGI_MANAGE_IMPORT_MAPS after approval."
---

# Manage Import Maps Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Import Maps` under `Items`.

## Setup Task Skill Contract

- task_code: `EGI_MANAGE_IMPORT_MAPS`
- task_name: `Manage Import Maps`
- parent_skill_id: `scm.product-management.items`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Items`
- functional_area_code: `ORA_EGP_FA_ITEMS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `itemImportMaps`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Import Maps` under `Items`.

## Setup Task Metadata

- Task name: `Manage Import Maps`
- Task code: `EGI_MANAGE_IMPORT_MAPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `itemImportMaps`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Select the import route from the requested operation and artifact type:
   - use `core.data-loader` with `itemImportMaps` for the REST Data Loader route;
   - use `core.data-loader` with the immutable ZIP and task code `EGI_MANAGE_IMPORT_MAPS` for the FSM task-level ZIP route.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Import Maps`
- Setup task code: `EGI_MANAGE_IMPORT_MAPS`

## Task Rule Execution

Before route-specific validation or artifact preparation, load
`ora-resource/ora_rule_registry.json` through the required ora-resource
execution guide and planner. Use the REST Data Loader route for `itemImportMaps`
workbook or DAT work, and use the FSM route for an FSM task-level ZIP.

`core.data-loader` owns orchestration for both routes. For the FSM route, it
preserves the final immutable ZIP, prepares and verifies the preflight, invokes
Task Hook with task code `EGI_MANAGE_IMPORT_MAPS`, retains the approved task
validation envelope, and owns approval-bound upload and import initiation.
Status and diagnostic requests remain separate Data Loader operations.

Use the task-local resources as the canonical rule sources:

| Behavior | Canonical resource |
|---|---|
| Route selection, archive validation, and mapping-pair validation | `ora-resource/ora_input_validation.md` |
| REST transformation design gates | `ora-resource/ora_design_enforcement.md` |
| Lookup paths, field mappings, cache behavior, and match rules | `ora-resource/ora_reference_lookups.md` |
| Lookup and handoff readiness | `ora-resource/ora_dependency_readiness.md` |
| Create defaults and `IgnoreFlag` normalization | `ora-resource/ora_defaulting_rules.md` |
| Failure classification, disclosure, refusal, and terminals | `ora-resource/ora_error_handling.md` |

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `itemImportMaps` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "itemImportMaps" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Validation Evidence

Use the synthetic cases in
`tests/fixtures/manage-import-maps-scenarios.json` with the reviewer procedure
in `tests/golden-scenarios.md` to verify the documented REST Data Loader and
FSM task-level ZIP branches. The fixtures are deterministic review evidence
only: they must not perform network requests, generate or upload an import
artifact, mutate Fusion, or authorize a later execution.

Any rule change that affects a fixture's expected path, terminal, defaults,
mapped values, warning, blocker, or refusal must update the fixture and receive
a fresh recorded review. A changed request, lookup result, archive, or preview
continues to invalidate prior execution approval under the task-local rules.

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

Use the parent functional-area skill `scm.product-management.items` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
