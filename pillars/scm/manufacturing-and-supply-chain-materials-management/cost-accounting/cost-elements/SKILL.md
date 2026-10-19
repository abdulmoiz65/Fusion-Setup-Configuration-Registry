---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.cost-elements"
name: "Cost Elements Setup Task Guidance"
description: "Provides task-specific setup guidance for Cost Elements under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_COST_ELEMENTS"
task_name: "Cost Elements"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "costAccountingCostElements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-elements/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-elements/current/"
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

# Cost Elements Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Cost Elements` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_COST_ELEMENTS`
- task_name: `Cost Elements`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `costAccountingCostElements`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Cost Elements` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Cost Elements`
- Task code: `ORA_CST_COST_ELEMENTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `costAccountingCostElements`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using costAccountingCostElements as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Cost Elements`
- Setup task code: `ORA_CST_COST_ELEMENTS`

## Cost Element Association Data Loader Contract

Use `costAccountingCostElements` as the parent REST business object for all Data Loader preparation and import. `costAccountingCostElementAnalysisGroups` is its nested child REST resource; use it only to associate an existing Cost Element with an existing Cost Analysis Group and Analysis Code. Route every preview and import through `core.data-loader`—this skill never submits direct REST writes.

| Requested operation | Parent action | Child resource action |
|---|---|---|
| Cost Element only | Create a parent Cost Element | Do not include a child entry. |
| Cost Element with association | Create a parent Cost Element | Provide the correlated parent and child values, including child `RestAction` `POST`, to `core.data-loader` for source generation and serialization. |
| Association for an existing Cost Element | Identify the existing parent Cost Element | Add the association through `costAccountingCostElementAnalysisGroups` with `RestAction` `POST`; do not recreate the parent. |
| Remove an existing association | Keep the existing parent Cost Element unchanged | Resolve the exact existing `ElementAnalysisGroupId`, then submit only that child mapping with `RestAction` `DELETE`. |
| Remove an existing Cost Element | Identify the existing parent Cost Element | Submit the parent `DELETE` through Data Loader without pre-checking child mappings or other references; Fusion evaluates the complete dependency state. |

Resolve the required type, set, organization, Analysis Group, and Analysis Code values through the task's `ora-resource` rules before handing the parent and child values to `core.data-loader` in its Excel template. Core Data Loader owns the import-source generation.

### Child Association Data Loader Contract

All association writes use `core.data-loader`; direct REST writes are not allowed.

- To add an association, use the existing parent `CostElementId` and a child row with `RestAction` `POST`, the resolved `AnalysisGroupId`, `AnalysisGroupCode`, and `AnalysisCode`. Do not use `CREATE` or `MERGE` as the child `RestAction`.
- To remove an association, first perform the read-only nested-child lookup `costAccountingCostElements/{{costElementId}}/child/costAccountingCostElementAnalysisGroups`, requesting `ElementAnalysisGroupId`, `CostElementId`, `AnalysisGroupId`, `AnalysisGroupCode`, `AnalysisId`, and `AnalysisCode`. Match the requested existing mapping exactly. Stop if it is absent or ambiguous.
- A removal child row must contain `ElementAnalysisGroupId`, `CostElementId`, and `RestAction` `DELETE`. It must not include parent Cost Element changes.
- For an association-only add or removal, provide the resolved parent and child association values to `core.data-loader`. It owns the Data Loader source, parent/child serialization, validation, approval, and execution; this skill does not generate a DAT.

### Combined Create and Association Contract

For a new Cost Element and one or more new associations in the same load, do not
leave the child's parent context blank and do not invent a persistent
`CostElementId`. Fusion assigns that ID while creating the parent. Instead,
correlate every child row with the same parent alternate key:

- parent `CostElementCode` and `CostElementSetId` are required;
- child `CostElementCode` and `CostElementSetId` must exactly equal those
  parent values;
- child `CostElementId` is blank for a new parent;
- child `RestAction` is `POST`, with the resolved `AnalysisGroupId`,
  `AnalysisGroupCode`, and `AnalysisCode`.

Provide the parent and child values together to `core.data-loader`. It owns the
Data Loader source generation, parent/child serialization, validation, approval,
and execution; this skill does not generate a DAT.

### Lifecycle and Change Controls

- After creation, do not change `CostElementCode`, `CostElementType`, or the Cost Element Set (`CostElementSetId` / Common Set). Treat a request to change any of these values as blocked; create and use a suitable separate Cost Element when a different value is required.
- A Cost Element-to-Analysis Group mapping can be edited or removed at any time. Do not block a mapping-only change merely because the Cost Element is mapped to a Cost Component Group that is referenced by a Cost Profile.
- Before preparing a parent delete, do not independently validate Analysis Group child mappings, Cost Component Groups, Cost Profiles, overhead rules, rates, or costing transactions. Submit the parent delete through Data Loader and let Fusion evaluate the complete dependency state. If Fusion rejects the delete, retain the Cost Element and disclose the returned dependency error.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `costAccountingCostElements` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "costAccountingCostElements" \
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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.cost-accounting` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
