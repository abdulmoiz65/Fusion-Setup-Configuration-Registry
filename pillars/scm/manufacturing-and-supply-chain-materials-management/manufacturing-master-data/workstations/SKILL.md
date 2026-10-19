---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data.workstations"
name: "Workstations Setup Task Guidance"
description: "Provides task-specific setup guidance for Workstations under the Manufacturing Master Data functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Manufacturing Master Data"
functional_area_code: "ORA_WIS_COMMON_MFG_WORK_SETUP"
task_code: "ORA_WIS_WORKSTATIONS"
task_name: "Workstations"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "workstations"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/manufacturing-master-data/workstations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/manufacturing-master-data/workstations/current/"
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

# Workstations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Workstations` under `Manufacturing Master Data`.

## Setup Task Skill Contract

- task_code: `ORA_WIS_WORKSTATIONS`
- task_name: `Workstations`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Manufacturing Master Data`
- functional_area_code: `ORA_WIS_COMMON_MFG_WORK_SETUP`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `workstations` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "workstations" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Inspect the generated outputs for `WorkstationDFF`. The shared `core.data-loader` generator does not exclude that section for this task. If it is present, stop the REST Data Loader route for the requested DFF data; do not change the shared generator or send a task-local REST create or update. DFF maintenance follows the generic DFF FSM route only after the relevant DFF deployment status is `Deployed`; an `Edited` or in-progress deployment can produce an export template with no DFF data.
6. Only when the generated output has no `WorkstationDFF`, use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Workstations` under `Manufacturing Master Data`.

## Setup Task Metadata

- Task name: `Workstations`
- Task code: `ORA_WIS_WORKSTATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using workstations as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Manufacturing Master Data`
- Setup task name: `Workstations`
- Setup task code: `ORA_WIS_WORKSTATIONS`

## Workstations Execution Route Selection

Use `core.data-loader` for both Workstations routes. Do not send a task-local REST POST or PATCH request.

| Requested Workstations input | Route | Required proof before any Fusion write |
| --- | --- | --- |
| A fresh task CSV ZIP containing `ASM_SETUP_CSV_METADATA.xml` | FSM Import/Export. `core.data-loader` preserves the validated FSM ZIP and sends it as an FSM source. | A newly exported `ORA_WIS_WORKSTATIONS` template, a validated immutable ZIP, and explicit approval for that exact ZIP. |
| A Data Loader XLSX workbook for the registered `workstations` business object | REST through Data Loader. `core.data-loader` validates the workbook against live Data Loader metadata before it prepares the load. | A successful read-only Data Loader lookup confirming that `workstations` is registered, a generated sample workbook, a validated immutable upload artifact, and explicit approval for that exact artifact. |

The task catalog proves that `ORA_WIS_WORKSTATIONS` supports task CSV export/import. The registered Data Loader business-object check is a separate live verification; do not claim REST execution is proven until the `workstations` lookup succeeds.


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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
