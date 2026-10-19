---
skill_id: "hcm.hcm-tool.approval-options.bypass-approvals"
name: "Bypass Approvals Setup Task Guidance"
description: "Provides task-specific setup guidance for Bypass Approvals under the Approval Options functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Approval Options"
functional_area_code: "CUSTOM_APPROVAL_OPTIONS"
task_code: "CUSTOM_BYPASS_APPROVALS"
task_name: "Bypass Approvals"
parent_skill_id: "hcm.hcm-tool.approval-options"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "bypassApprovalsCases"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-options/bypass-approvals/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-options/bypass-approvals/current/"
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

# Bypass Approvals Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Bypass Approvals` under `Approval Options`.

## Setup Task Skill Contract

- task_code: `CUSTOM_BYPASS_APPROVALS`
- task_name: `Bypass Approvals`
- parent_skill_id: `hcm.hcm-tool.approval-options`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Approval Options`
- functional_area_code: `CUSTOM_APPROVAL_OPTIONS`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `bypassApprovalsCases`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Bypass Approvals` under `Approval Options`.

## Setup Task Metadata

- Task name: `Bypass Approvals`
- Task code: `CUSTOM_BYPASS_APPROVALS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `bypassApprovalsCases`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Bypass Approvals Mutation Routing

Route every Bypass Approvals mutation through `core.data-loader` using the registered REST business object `bypassApprovalsCases`. The business object is the routing key; do not substitute a similarly named object, construct an endpoint from the task label, or use a direct REST call outside this Data Loader-authorized route.

### Current-state flag semantics

- `ApprovalDisabledFlag: true` means Bypass Approvals is **enabled**: the transaction bypasses the approval route.
- `ApprovalDisabledFlag: false` means Bypass Approvals is **disabled**: the transaction follows the approval route.

Treat this field as the authoritative readback for the Bypass Approvals setting. Its name is inverted relative to the user-facing setting, so state the mapped meaning explicitly in previews and verification results.

1. Apply the parent Approval Options process scope gate and resolve exactly one approval process before preparing a mutation.
2. Confirm that the selected operation is the registered `bypassApprovalsCases` action and validate the request against the task's Bypass Approvals request-payload schema and the runtime-advertised action link. Do not infer an action URL, method, or media type.
3. Bind the mutation only to the resolved `processId` and `approvalOptionsId`. Prepare an immutable preview identifying the target environment, process, action, and requested bypass value.
4. Obtain explicit user approval immediately before the first state-changing request. A changed process, identifier, action link, or payload invalidates the preview and requires a new approval.
5. Dispatch the approved request through `core.data-loader`, with `core.fusion-api.rest-api-client` used only as the Data Loader-authorized REST execution adapter for the discovered action link. Do not retry a live mutation automatically.
6. Perform a fresh read through the parent process scope gate and report the resulting Bypass Approvals setting. If the action link, contract, or verification field is unavailable, fail closed and record the route gap; do not attempt an alternate endpoint.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `bypassApprovalsCases` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "bypassApprovalsCases" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



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

Use the parent functional-area skill `hcm.hcm-tool.approval-options` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
