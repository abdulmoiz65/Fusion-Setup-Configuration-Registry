---
skill_id: "hcm.hcm-tool.approval-task.configure-task"
name: "Configure task Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure task under the Approval Task functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Approval Task"
functional_area_code: "CUSTOM_APPROVAL_TASK"
task_code: "CUSTOM_CONFIGURE_TASK"
task_name: "Configure task"
parent_skill_id: "hcm.hcm-tool.approval-task"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "businessProcessApprovalRulesTasks"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.1.1"
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
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.data-loader.task-rest"
  - "core.fusion-api.hcm-approval-rules-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-task/configure-task/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-task/configure-task/current/"
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
  - "May execute an explicitly approved writeTaskConfiguration action through the registered businessProcessApprovalRulesTasks adapter."
required_privileges:
  - "Fusion privileges sufficient to read and update HCM approval task configuration."
---

# Configure task Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure task` under `Approval Task`.

## Setup Task Skill Contract

- task_code: `CUSTOM_CONFIGURE_TASK`
- task_name: `Configure task`
- parent_skill_id: `hcm.hcm-tool.approval-task`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Approval Task`
- functional_area_code: `CUSTOM_APPROVAL_TASK`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `businessProcessApprovalRulesTasks`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure task` under `Approval Task`.

## Setup Task Metadata

- Task name: `Configure task`
- Task code: `CUSTOM_CONFIGURE_TASK`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `businessProcessApprovalRulesTasks`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Registered Task-Configuration Write Adapter

`businessProcessApprovalRulesTasks` is the registered Data Loader business
object for the task-configuration write action. Use it as the registered
`writeTaskConfiguration` adapter; it is a task REST operation, not a CSV, ZIP,
or generic Data Loader-file import.

The documented action contract is:

| Field | Required value |
|---|---|
| Method and path | POST `/hcmRestApi/resources/11.13.18.05/businessProcessApprovalRulesTasks/action/writeTaskConfiguration` |
| Content type | `application/vnd.oracle.adf.action+json` |
| processId | The one exact ProcessId resolved by the approval-process finder |
| Json | The complete reviewed task configuration serialized as a JSON string |
| commitNeededFlag | `true` or `false`; default to `true` only when the requester leaves it unset |

Route a write through `core.data-loader.task-rest`, its Task Hook validation,
and the shared REST client. Before dispatch, read the current configuration,
preserve all unchanged settings, create an immutable preview with the exact
environment and body, and obtain explicit approval immediately before the POST.
Never retry an uncertain write.

The supplied internal HCM Config Task export is the contract source for the
action's endpoint, field names, serialization shape, and example sections
(`accessList`, `notificationActions`, and `taskLevelConfigMap`). Preserve every
section returned by the target; `accessList` is optional when the target read
does not return it. Use its example
as a structural contract only: do not copy its values over a target process.
Build `Json` from the target process's complete current configuration plus only
the approved changes.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `businessProcessApprovalRulesTasks` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "businessProcessApprovalRulesTasks" \
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

Use the parent functional-area skill `hcm.hcm-tool.approval-task` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
