---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping.ship-confirm-rules"
name: "Ship Confirm Rules Setup Task Guidance"
description: "Provides task-specific setup guidance for Ship Confirm Rules under the Shipping functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Shipping"
functional_area_code: "WSH_ENABLE_SHIPPING"
task_code: "ORA_SHIP_CONFIRM_RULES"
task_name: "Ship Confirm Rules"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "shipConfirmRules"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/ship-confirm-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/ship-confirm-rules/current/"
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

# Ship Confirm Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Ship Confirm Rules` under `Shipping`.

## Setup Task Skill Contract

- task_code: `ORA_SHIP_CONFIRM_RULES`
- task_name: `Ship Confirm Rules`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.shipping`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Shipping`
- functional_area_code: `WSH_ENABLE_SHIPPING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `shipConfirmRules`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `shipConfirmRules` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "shipConfirmRules" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Ship Confirm Rules` under `Shipping`.

## Setup Task Metadata

- Task name: `Ship Confirm Rules`
- Task code: `ORA_SHIP_CONFIRM_RULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `shipConfirmRules`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. For the default route, prepare and import Ship Confirm Rules through `core.data-loader` using the registered `shipConfirmRules` REST business object.
2. Use `shared.validation.setup-data-validator` and the task-local lookup/normalization rules before the immutable-artifact approval gate.
3. Use the FSM package route only when the user explicitly requests FSM Export or FSM Import.

An export/import-supported catalog flag does not switch the default route from REST to FSM.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Shipping`
- Setup task name: `Ship Confirm Rules`
- Setup task code: `ORA_SHIP_CONFIRM_RULES`


## Explicit FSM Package Contract

- Apply this section only after an explicit FSM Export or FSM Import request.
- Exported package members: `WSH_SHIP_CONFIRM_RULE.csv` and `ASM_SETUP_CSV_METADATA.xml`.
- Preserve the exported CSV header, metadata XML, encoding, and package structure.
- Treat the exported template as authoritative for `ActionFlag` and all supported columns; do not invent an `ActionFlag` default.
- Run the ordinary Data Loader validation, Task Hook validation, immutable-artifact approval, and FSM import workflow before a Fusion submission.



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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.shipping` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
