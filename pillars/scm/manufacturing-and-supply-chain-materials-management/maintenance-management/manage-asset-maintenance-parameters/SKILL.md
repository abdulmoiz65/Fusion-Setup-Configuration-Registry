---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.maintenance-management.manage-asset-maintenance-parameters"
name: "Manage Asset Maintenance Parameters Setup Task Guidance"
description: "Routes Asset Maintenance Parameters setup data through the published assetSystemOptions Data Loader REST business object."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Maintenance Management"
functional_area_code: "ORA_MNT_MGMT"
task_code: "ORA_MANAGE_ASSET_MAINTENANCE_PARAMS"
task_name: "Manage Asset Maintenance Parameters"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.maintenance-management"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "assetSystemOptions"
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
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/maintenance-management/manage-asset-maintenance-parameters/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/maintenance-management/manage-asset-maintenance-parameters/current/"
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

# Manage Asset Maintenance Parameters Setup Task Guidance

## Purpose

Routes Manage Asset Maintenance Parameters setup data through the published
assetSystemOptions Data Loader REST business object.

## Setup Task Skill Contract

- task_code: ORA_MANAGE_ASSET_MAINTENANCE_PARAMS
- task_name: Manage Asset Maintenance Parameters
- parent_skill_id: scm.manufacturing-and-supply-chain-materials-management.maintenance-management
- pillar: SCM
- offering: Manufacturing and Supply Chain Materials Management
- functional_area: Maintenance Management
- functional_area_code: ORA_MNT_MGMT
- dataloader_import_mode: REST
- businessObject: assetSystemOptions

## Download Fusion Data Loader Sample

1. Confirm assetSystemOptions is the published Data Loader REST business object.
2. Generate the default editable XLSX sample through core.data-loader:

   python3 core/data-loader/scripts/generate_sample_dat.py assetSystemOptions --output-dir "<project-artifact-directory>"

3. Keep the editable sample, attribute-details workbook, and key-fields workbook together.
4. Review the generated headers and key fields before preparing source data. Metadata retrieval is read-only and does not upload or import data.

## Data Loader Run Book Route

1. A request may supply either a supported setup-data artifact or an explicit supported parameter change. When no artifact is supplied, core.data-loader first generates the live `assetSystemOptions` update XLSX sample and uses that generated workbook as the source artifact.
2. For an explicit enable or disable request, populate only the matching live-schema field in the generated workbook. Do not invent columns, a DAT layout, a REST payload, or an endpoint.
3. Route source-data validation, immutable preview, approval, submission, status, and execution history exclusively through core.data-loader.
4. Immediately before upload or initiation, Data Loader validates that the final immutable artifact and `assetSystemOptions` are within the active Run Book scope.
5. This pillar skill does not construct a REST payload, select a REST endpoint, or issue a direct Fusion REST write.

## Usage

Use this skill when planning, sequencing, validating, or preparing setup data for
Manage Asset Maintenance Parameters under Maintenance Management.

## Inputs

- implementation_objective
- project_context
- setup_task_scope
- setup_data_artifacts

## Outputs

- setup_task_plan
- setup_data_routing
- validation_checkpoints
- skill_run_record
- token_usage_record

## Implementation Notes

Use the parent functional-area skill for functional-area sequencing and scope
decisions. The Run Book and core.data-loader own execution, approval, and
Fusion write processing.
