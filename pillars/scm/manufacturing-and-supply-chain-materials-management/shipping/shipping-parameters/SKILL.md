---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping.shipping-parameters"
name: "Shipping Parameters Setup Task Guidance"
description: "Provides task-specific setup guidance for Shipping Parameters under the Shipping functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Shipping"
functional_area_code: "WSH_ENABLE_SHIPPING"
task_code: "ORA_SHIPPING_PARAMETERS"
task_name: "Shipping Parameters"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "configureShippingParameters"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/shipping-parameters/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/shipping-parameters/current/"
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
  - "Reads Shipping Parameters Data Loader metadata and approved standard lookup values through authorized read-only routes."
  - "Writes generated Data Loader sample workbooks and validation evidence under project/{project_id}."
  - "Delegates an approved Shipping Parameters import to core.data-loader; upload and import remain subject to its approval workflow."
required_privileges:
  - "Read access to Shipping Parameters metadata and the referenced standard lookup values in the selected Fusion environment."
  - "Write access to the selected local project workspace."
  - "Privileges required by core.data-loader to validate, upload, initiate, and inspect the configureShippingParameters data load when execution is approved."
---

# Shipping Parameters Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Shipping Parameters` under `Shipping`.

## Setup Task Skill Contract

- task_code: `ORA_SHIPPING_PARAMETERS`
- task_name: `Shipping Parameters`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.shipping`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Shipping`
- functional_area_code: `WSH_ENABLE_SHIPPING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `configureShippingParameters`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Shipping Parameters` under `Shipping`.

## Setup Task Metadata

- Task name: `Shipping Parameters`
- Task code: `ORA_SHIPPING_PARAMETERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Data Loader business object: `configureShippingParameters`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `configureShippingParameters`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Shipping`
- Setup task name: `Shipping Parameters`
- Setup task code: `ORA_SHIPPING_PARAMETERS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `configureShippingParameters` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "configureShippingParameters" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Local Execution Contract

### Preconditions

- A valid `project_id` and writable project workspace are available.
- The selected Fusion environment identity and required read privileges are
  confirmed before a lookup or metadata read.
- `configureShippingParameters` is confirmed as the registered Data Loader
  business object.
- Input data has passed the task-local friendly-value checks in
  `ora-resource/ora_input_validation.md`.

### Postconditions and Evidence

- Persist and register the JSON artifacts described above, including redacted
  lookup-validation evidence and any blocking issues.
- Record the skill run and token usage using the manifest's declared locations.
- A failed or ambiguous lookup stops before Data Loader handoff and records a
  redacted diagnostic according to `ora-resource/ora_error_handling.md`.
- Route read-only lookup calls through `core.fusion-api.rest-api-client`.
  Delegate import only to `core.data-loader`; its approval workflow is the
  required gate before a live import.

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.shipping` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
