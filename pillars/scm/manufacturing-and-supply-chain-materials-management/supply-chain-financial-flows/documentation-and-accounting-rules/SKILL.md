---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows.documentation-and-accounting-rules"
name: "Documentation and Accounting Rules Setup Task Guidance"
description: "Provides task-specific setup guidance for Documentation and Accounting Rules under the Supply Chain Financial Flows functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
task_code: "ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW"
task_name: "Documentation and Accounting Rules"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "financialOrchestrationDocumentationAndAccountingRules"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.7.11"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/documentation-and-accounting-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/documentation-and-accounting-rules/current/"
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

# Documentation and Accounting Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Documentation and Accounting Rules` under `Supply Chain Financial Flows`.

## Setup Task Skill Contract

- task_code: `ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW`
- task_name: `Documentation and Accounting Rules`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Supply Chain Financial Flows`
- functional_area_code: `ORA_FOS_SUPPLY_CHAIN_FIN_FLOW`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `financialOrchestrationDocumentationAndAccountingRules`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `financialOrchestrationDocumentationAndAccountingRules` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "financialOrchestrationDocumentationAndAccountingRules" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Documentation and Accounting Rules` under `Supply Chain Financial Flows`.

## Setup Task Metadata

- Task name: `Documentation and Accounting Rules`
- Task code: `ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `financialOrchestrationDocumentationAndAccountingRules`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `financialOrchestrationDocumentationAndAccountingRules` as the Business Object.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Supply Chain Financial Flows`
- Setup task name: `Documentation and Accounting Rules`
- Setup task code: `ORA_FOS_DEFINE_TRADE_AND_ACCOUNTING_RULES_NEW`




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

- When `CurrencyOption` is `ORA_STANDARD_CURRENCY`, accept a Standard Currency name or Currency Code from the request. Resolve it through the preferred-currencies lookup and populate `StandardCurrency` with the returned `CurrencyCode`; do not pass through an unverified user value.
- Before packaging a start-date correction, exercise the synthetic cases in [the start-date correction regression scenarios](tests/fixtures/dar_start_date_correction_cases.md). The accepted case must pass the `ora_input_validation.md` DAT assertion; each invalid case must stop packaging and identify the violated condition. These cases supplement, and do not replace, the current generated Data Loader template and live record lookup.
