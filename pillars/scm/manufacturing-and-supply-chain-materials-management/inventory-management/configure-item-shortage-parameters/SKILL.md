---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.inventory-management.configure-item-shortage-parameters"
name: "Configure Item Shortage Parameters Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Item Shortage Parameters under the Inventory Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Inventory Management"
functional_area_code: "ORA_WSH_INVENTORY_MGMT"
task_code: "ORA_INV_CONFIGURE_ITEM_SHORTAGE_PARAMETERS"
task_name: "Configure Item Shortage Parameters"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.inventory-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "ruleConfigurationHeaders"
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
  - "data_loader_sample_bundle"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
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
  - "baselines"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_baseline"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/data-loader-sample/"
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

# Configure Item Shortage Parameters Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Item Shortage Parameters` under `Inventory Management`.

## Setup Task Skill Contract

- task_code: `ORA_INV_CONFIGURE_ITEM_SHORTAGE_PARAMETERS`
- task_name: `Configure Item Shortage Parameters`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.inventory-management`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Inventory Management`
- functional_area_code: `ORA_WSH_INVENTORY_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `ruleConfigurationHeaders`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Item Shortage Parameters` under `Inventory Management`.

## Setup Task Metadata

- Task name: `Configure Item Shortage Parameters`
- Task code: `ORA_INV_CONFIGURE_ITEM_SHORTAGE_PARAMETERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `ruleConfigurationHeaders`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using ruleConfigurationHeaders as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Inventory Management`
- Setup task name: `Configure Item Shortage Parameters`
- Setup task code: `ORA_INV_CONFIGURE_ITEM_SHORTAGE_PARAMETERS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `ruleConfigurationHeaders` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "ruleConfigurationHeaders" \
     --output-dir "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/data-loader-sample/"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Persist `data-loader-sample-bundle.json` beside the workbooks. It must validate against `schemas/configuration-baseline.schema.json` and list the editable sample, attribute-details, and key-fields workbook as `xlsx` artifacts with each relative location and SHA-256 checksum.
6. Register the bundle with `core.project-mgmt.artifact-registry-manager`, update the project baseline state, and include the bundle and three workbook references in the `artifact_refs` array of the skill-run record.
7. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `data_loader_sample_bundle`
- `skill_run_record`
- `token_usage_record`

## Machine-Readable Output Artifact Contract

Contract version: `1.1`. Persist durable metadata, diagnostics, and run records as UTF-8 JSON or Markdown only at the manifest-declared project location. The only binary exception is the three core-generated XLSX workbooks in the declared `data-loader-sample/` directory; do not persist output artifacts in this skill package.

| Declared output | Machine-readable representation | Schema-backed envelope or record | Artifact type and location | Required linkage and validation |
|---|---|---|---|---|
| `setup_task_plan` | A `configuration_blueprint` artifact that identifies `ORA_INV_CONFIGURE_ITEM_SHORTAGE_PARAMETERS`, the selected business object, ordered planning steps, status, and any blocking reason | `schemas/project-artifact.schema.json` | `configuration_blueprint` at `project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/` | Validate the artifact metadata before persistence; record its versioned artifact reference in the skill-run record. |
| `setup_data_routing` | A `configuration_blueprint` artifact that identifies `ruleConfigurationHeaders`, `core.data-loader` as the execution owner, and the task’s export/import route | `schemas/project-artifact.schema.json` | `configuration_blueprint` at `project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/` | Validate the artifact metadata before persistence; include the plan artifact reference and record this artifact reference in the skill-run record. |
| `validation_checkpoints` | A `validation_result` JSON record with checkpoint name, status, evidence reference, and sanitized diagnostic when blocked | `schemas/validation-result.schema.json` | `validation_result` at `project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/` | Validate against the validation-result schema before persistence; reference the applicable plan or routing artifact. |
| `data_loader_sample_bundle` | A `configuration_baseline` JSON document named `data-loader-sample-bundle.json`, with source instance, capture time, task scope, and exactly the editable sample, attribute-details, and key-fields workbooks as `xlsx` artifact entries containing their relative locations and SHA-256 checksums | `schemas/configuration-baseline.schema.json` for the bundle; `schemas/project-artifact.schema.json` for its registry record | `configuration_baseline` and its three core-generated XLSX workbooks at `project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-item-shortage-parameters/current/data-loader-sample/` | Validate the bundle before persistence; register its artifact metadata in `artifact-index.json`; update the project baseline state; and reference the bundle plus all three workbook paths in the skill-run record. A missing workbook, checksum, registry record, or skill-run reference makes the sample bundle incomplete. |
| `skill_run_record` | A skill-run JSON record | `schemas/skill-run.schema.json` | `skill_run` at `project/{project_id}/state/runs/` | Validate against the skill-run schema; list all persisted artifact references in `artifact_refs`. |
| `token_usage_record` | The append-only token-usage Markdown record declared in this manifest | `schemas/skill-run.schema.json` token-usage object when included in a skill-run record | `token_usage_record` at `project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md` | Preserve every manifest-required token field and link the log reference from the skill-run record. |

Consumers must treat a missing schema-valid artifact, missing artifact reference, or a `blocked` validation result as an incomplete planning outcome. `core.project-mgmt.artifact-registry-manager` owns artifact registration; `core.project-mgmt.project-state-manager` owns durable run-state updates.

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.inventory-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
