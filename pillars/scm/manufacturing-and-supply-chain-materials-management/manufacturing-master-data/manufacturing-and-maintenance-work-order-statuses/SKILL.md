---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data.manufacturing-and-maintenance-work-order-statuses"
name: "Manufacturing and Maintenance Work Order Statuses Setup Task Guidance"
description: "Provides task-specific setup guidance for Manufacturing and Maintenance Work Order Statuses under the Manufacturing Master Data functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Manufacturing Master Data"
functional_area_code: "ORA_WIS_COMMON_MFG_WORK_SETUP"
task_code: "ORA_REDWOOD_MANUFACTURING_WORK_ORDER_STATUSES"
task_name: "Manufacturing and Maintenance Work Order Statuses"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "workOrderStatuses"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/manufacturing-master-data/manufacturing-and-maintenance-work-order-statuses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/manufacturing-master-data/manufacturing-and-maintenance-work-order-statuses/current/"
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

# Manufacturing and Maintenance Work Order Statuses Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manufacturing and Maintenance Work Order Statuses` under `Manufacturing Master Data`.

## Setup Task Skill Contract

- task_code: `ORA_REDWOOD_MANUFACTURING_WORK_ORDER_STATUSES`
- task_name: `Manufacturing and Maintenance Work Order Statuses`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.manufacturing-master-data`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Manufacturing Master Data`
- functional_area_code: `ORA_WIS_COMMON_MFG_WORK_SETUP`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `workOrderStatuses`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manufacturing and Maintenance Work Order Statuses` under `Manufacturing Master Data`.

## Setup Task Metadata

- Task name: `Manufacturing and Maintenance Work Order Statuses`
- Task code: `ORA_REDWOOD_MANUFACTURING_WORK_ORDER_STATUSES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `workOrderStatuses`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data only through `core.data-loader`, with REST Data Loader as the default and primary route and `workOrderStatuses` as the exact registered Business Object.

### Import Route and Approval Gate

- Do not call a Fusion REST endpoint, REST Data Loader adapter, FSM import endpoint, import job, or script directly from this task skill. Every import, including an FSM fallback, must be orchestrated by `core.data-loader`.
- Before preparing an import, use `core.data-loader` to retrieve Data Loader metadata read-only and confirm that `workOrderStatuses` remains a registered Business Object for the requested operation. If it is not confirmed, stop and ask the user; never substitute or invent a REST Business Object.
- Complete the `core.data-loader` source review, live metadata and schema validation, task validation, and immutable upload-artifact preparation before requesting approval. Do not upload or initiate an import until the user explicitly approves that exact validated artifact and target environment.
- Preserve only redacted diagnostics and audit details in project artifacts. Never record or display access tokens, authorization codes, client secrets, cookies, or unredacted sensitive payload values.

### Conditional FSM Fallback

CSV export/import is catalog-supported, so retain FSM export/import capability. It is not an equal import route: use FSM only when `core.data-loader` REST preflight or read-only metadata validation establishes that REST cannot perform the requested operation. `core.data-loader` must preserve the validation evidence, prepare an immutable FSM import artifact, and obtain the user's explicit approval for that exact artifact before it performs the FSM import. Do not execute FSM directly from this skill.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Manufacturing Master Data`
- Setup task name: `Manufacturing and Maintenance Work Order Statuses`
- Setup task code: `ORA_REDWOOD_MANUFACTURING_WORK_ORDER_STATUSES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `workOrderStatuses` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "workOrderStatuses" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later `core.data-loader` preparation, preflight-validation, immutable-artifact, and approval workflow.



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
