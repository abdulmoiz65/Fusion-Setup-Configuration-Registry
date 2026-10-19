---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows.financial-qualifiers"
name: "Financial Qualifiers Setup Task Guidance"
description: "Provides task-specific setup guidance for Financial Qualifiers under the Supply Chain Financial Flows functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
task_code: "ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW"
task_name: "Financial Qualifiers"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "financialOrchestrationQualifiers"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-qualifiers/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-qualifiers/current/"
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

# Financial Qualifiers Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Financial Qualifiers` under `Supply Chain Financial Flows`.

## Setup Task Skill Contract

- task_code: `ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW`
- task_name: `Financial Qualifiers`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Supply Chain Financial Flows`
- functional_area_code: `ORA_FOS_SUPPLY_CHAIN_FIN_FLOW`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `financialOrchestrationQualifiers`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `financialOrchestrationQualifiers` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "financialOrchestrationQualifiers" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Financial Qualifiers` under `Supply Chain Financial Flows`.

## Setup Task Metadata

- Task name: `Financial Qualifiers`
- Task code: `ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `financialOrchestrationQualifiers`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Supply Chain Financial Flows`
- Setup task name: `Financial Qualifiers`
- Setup task code: `ORA_FOS_MANAGE_TRADE_QUALIFIER_NEW`

## Qualifier LOV References

Use the task-local [lookup guidance](ora-resource/ora_reference_lookups.md)
before preparing a Data Loader REST import. The following user-supplied endpoints provide
reference data only; they do not authorize a Fusion write:

- Business Flow: use the filtered `ORA_FOS_AGREEMENT_TYPE_FOR_VAL` finder in the lookup guidance.
- Parameter: select the business-flow-specific parameter LOV in the lookup guidance.
- Rule value: resolve YES/NO values or ship-from organizations through the matching value LOV.
- Operator: use the `FOS_QUALIFIER_OPERATORS` lookup type.
- Conjunction: resolve only when a rule contains multiple conditions.

The Data Loader REST sample and its generated schema remain the source of truth
for applicability, lookup type, exact-match behavior, and field mappings. Do
not infer those details from the LOV endpoint names or response fields.

Before a preview or import, read [input validation](ora-resource/ora_input_validation.md),
[dependency readiness](ora-resource/ora_dependency_readiness.md),
[lookup guidance](ora-resource/ora_reference_lookups.md), and
[error handling](ora-resource/ora_error_handling.md).

## Duplicate-Name Gate

Before generating a preflight artifact, requesting upload approval, or
submitting a qualifier import, query the selected environment for an exact
`QualifierRuleSetName` match:

`financialOrchestrationQualifiers?fields=QualifierRuleSetName&onlyData=true&limit=25&q=QualifierRuleSetName%3D%27<encoded-exact-name>%27`

Send `REST-Framework-Version: 9`. If the response contains the exact supplied
name, stop the workflow: do not create, upload, submit, or overwrite a
qualifier. Report that the name already exists and require a different name.
This is a read-only preflight check; do not rely on a Data Loader duplicate
error as the uniqueness validation.

## Delete Gate

For a delete request, first retrieve the selected qualifier through the
documented delete-eligibility lookup. Deletion is permitted only when the
returned `UsedInFlow` property is JSON `null`. Any other value, including an
empty string, `false`, an omitted property, or an unreadable response, blocks
deletion. Do not prepare a delete source, request approval, or submit a delete
load until this gate passes.

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
