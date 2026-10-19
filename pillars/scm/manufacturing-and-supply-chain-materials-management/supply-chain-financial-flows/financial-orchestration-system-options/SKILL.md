---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows.financial-orchestration-system-options"
name: "Financial Orchestration System Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Financial Orchestration System Options under the Supply Chain Financial Flows functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
task_code: "ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW"
task_name: "Financial Orchestration System Options"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "financialOrchestrationSystemOptions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.4"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-orchestration-system-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-orchestration-system-options/current/"
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

# Financial Orchestration System Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Financial Orchestration System Options` under `Supply Chain Financial Flows`.

## Setup Task Skill Contract

- task_code: `ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW`
- task_name: `Financial Orchestration System Options`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Supply Chain Financial Flows`
- functional_area_code: `ORA_FOS_SUPPLY_CHAIN_FIN_FLOW`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `financialOrchestrationSystemOptions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

`REST` identifies the Data Loader adapter for this business object. REST is
lookup-only for this task; Data Loader is the only write route.

1. Confirm that `financialOrchestrationSystemOptions` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "financialOrchestrationSystemOptions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Financial Orchestration System Options` under `Supply Chain Financial Flows`.

## Setup Task Metadata

- Task name: `Financial Orchestration System Options`
- Task code: `ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `financialOrchestrationSystemOptions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

## Default Import Route

Use `core.data-loader` as the default route for every Financial Orchestration
System Options create or update requested as an import. Prepare and validate an
immutable Data Loader artifact, then require a separate explicit approval before
upload and initiation. Do not use direct Fusion REST for writes.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Supply Chain Financial Flows`
- Setup task name: `Financial Orchestration System Options`
- Setup task code: `ORA_FOS_MANAGE_SYSTEM_OPTIONS_NEW`




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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Guardrails

Apply every guardrail below before preparing or executing a Financial
Orchestration System Options create, update, delete, or Data Loader import.

| ID | Guardrail | Required behavior |
| --- | --- | --- |
| G-01 | Singleton record | Create only after a fresh zero-record lookup; update or delete only the one resolved record; stop on more than one record. |
| G-02 | Scoped payload | Include only fields explicitly requested and approved; preserve unmentioned values. |
| G-03 | Validation organization | Resolve exactly one Item Validation Organization; never substitute zero, ambiguous, or similarly named results. |
| G-04 | Set Service Item | A non-null `ServiceItemId` requires effective `GPOServiceItem = "Y"` and an item selected from the Service Item LOV for the resolved validation organization. |
| G-05 | Clear Service Item | `ServiceItemId: null` requires an explicit clear request and is allowed whether effective `GPOServiceItem` is `Y` or `N`; an omitted Service Item preserves its existing value. |
| G-06 | No implicit enablement | Selecting a Service Item must not implicitly enable `GPOServiceItem`; it must already be effective as `Y` or be explicitly included and approved in the same payload. |
| G-07 | Batch size | `PayloadSize` is an explicit business decision; do not infer it. |
| G-08 | Boolean options | Send `TradeTax`, `IgnoreBillOnly`, and `ProcessRMA` only as explicit `Y` or `N` values when changing them. |
| G-09 | Concurrency | Immediately before preparing an update load, re-read the exact record and retain its current version for the Data Loader row. |
| G-10 | Approval | Present the exact environment, operation, target record, and loader attributes, then obtain explicit approval immediately before upload and initiation. |
| G-11 | Stop on uncertain writes | Do not automatically retry a failed, timed-out, rejected, or unknown-outcome mutation; re-read the state and require fresh approval. |
| G-12 | Credential handling | Keep credentials and tokens out of project artifacts and tracked files; use permission-restricted temporary local material and remove it after the operation. |
| G-13 | First LOV selection | Select the first returned Service Item only when the user explicitly requests that ordering; otherwise present the available LOV values and require an explicit selection. |
| G-14 | Data Loader approval boundary | Prepare and validate the immutable loader source first; do not upload or initiate it until the user separately approves that exact validated load. |
| G-15 | Scoped Data Loader updates | An update row must include the system-option key, `RestAction`, and only explicitly requested attributes; blank unrequested cells preserve existing option values. |
| G-16 | Data Loader Service Item selection | A loader update that sets `ServiceItemId` must use an explicitly selected LOV value for the current validation organization and require effective `GPOServiceItem = "Y"`; do not treat a prior selection or display order as current consent. |
