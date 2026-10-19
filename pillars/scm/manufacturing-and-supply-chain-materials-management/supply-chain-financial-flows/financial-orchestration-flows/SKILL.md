---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows.financial-orchestration-flows"
name: "Financial Orchestration Flows Setup Task Guidance"
description: "Plans Financial Orchestration Flow Agreement, PTR and FTR setup through name-first effective-dated resolution, registered parent-child linkage and gated Data Loader transport."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
task_code: "ORA_FOS_MANAGE_SUPPLY_CHAIN_FINANCIAL_TRADE_AGREEMENTS_NEW"
task_name: "Financial Orchestration Flows"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "financialOrchestrationTradeAgreements"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.2.7"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-orchestration-flows/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/financial-orchestration-flows/current/"
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

# Financial Orchestration Flows Setup Task Guidance

## Purpose

Provide Agreement, Primary Trade Relation (PTR) and Financial Trade Relation (FTR) rules for the registered business object financialOrchestrationTradeAgreements. Its hierarchy is Agreement → PTR → FTR; the APEX display label Transfer Pricing Rules does not identify a different task.

## Supported Scope

Agreement creation, current-version correction of Description/Priority/financial qualifier and explicitly requested Status, parent-only DRAFT description-changing dated Insert, PTR/FTR creation and correction, and PTR deletion use core.data-loader. Resolve a requested Status against FOS_AGREEMENT_STATUS and include its LookupCode only when the current correction contract exposes Status; Fusion validates whether the transition is allowed. Fusion validates Agreement name and Priority conflicts during create; do not run a separate pre-create uniqueness lookup. A new PTR requires at least one FTR. Shipment PTR creation never sends or validates a Selling Trade Organization. For a new FTR chain, an omitted first selling trade organization uses the first eligible selling-BU organization for Procurement and stays blank for Shipment or Internal Transfer. Every omitted buying trade organization defaults from its buying BU, and each later omitted selling trade organization inherits the preceding buying organization. Operation boundaries are enforced in ora_design_enforcement.md; all lookup and validation mechanics live in the owning resources below.

## Task Rules

Use the compiled ora-resource/ora_rule_registry.json under the framework's task-node execution guide. The resource ownership is:

| Resource | Task-specific responsibility |
|---|---|
| ora-resource/ora_input_validation.md | Required inputs, resolved fields, effective context, parent/child keys and changed lookup context |
| ora-resource/ora_reference_lookups.md | Live names/IDs, dated targets, side-specific LOVs and deployed key metadata |
| ora-resource/ora_dependency_readiness.md | Applicable parent, registration and financial dependencies |
| ora-resource/ora_defaulting_rules.md | Agreement defaults, FTR trade-organization defaults and preserved correction/Insert values |
| ora-resource/ora_design_enforcement.md | Supported operation, topology and deletion-impact gates |
| ora-resource/ora_error_handling.md | FOF diagnostics and operation-specific readback requirements |

## Setup Task Metadata Contract

- task_code: `ORA_FOS_MANAGE_SUPPLY_CHAIN_FINANCIAL_TRADE_AGREEMENTS_NEW`
- task_name: `Financial Orchestration Flows`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Supply Chain Financial Flows`
- functional_area_code: `ORA_FOS_SUPPLY_CHAIN_FIN_FLOW`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `financialOrchestrationTradeAgreements`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `financialOrchestrationTradeAgreements` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "financialOrchestrationTradeAgreements" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.
