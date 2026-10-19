---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.cost-books"
name: "Cost Books Setup Task Guidance"
description: "Provides task-specific setup guidance for Cost Books under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_COST_BOOKS"
task_name: "Cost Books"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "costAccountingCostBooks"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
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
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.data-loader.task-hook"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-books/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-books/current/"
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

# Cost Books Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Cost Books` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_COST_BOOKS`
- task_name: `Cost Books`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `costAccountingCostBooks`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Cost Books` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Cost Books`
- Task code: `ORA_CST_COST_BOOKS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `costAccountingCostBooks`

## Task-Local Validation and Execution Path

Before planning, validating, exporting, importing, or executing Cost Books
work, use the task-local resources shipped with this skill:

1. Load [ora-resource/ora_rule_registry.json](ora-resource/ora_rule_registry.json)
   and select exactly one entry matching task code `ORA_CST_COST_BOOKS` and
   task name `Cost Books`. Require task and reachable-node readiness
   `status: ready` with no blocking reasons.
2. Start at `start_node`. Before every reached node, require each prerequisite
   to have passed, evaluate `applies_when`, and read the matching source rule.
   Follow only the declared transition for the observed outcome. Stop on a
   missing, ambiguous, failed, or approval-blocked result; do not invent a path
   or bypass a reached gate.
3. Load [ora_input_validation.md](ora-resource/ora_input_validation.md) before
   the workflow. For an update or delete without `CostBookId`, complete the
   exact-match lookup defined in
   [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md) through
   `core.fusion-api.rest-api-client`.
4. Load [ora_error_handling.md](ora-resource/ora_error_handling.md) before
   preview or a later Data Loader operation. Record task identity, reached node
   IDs, outcomes, sanitized evidence, blockers, and a safe resume step in the
   skill-run record.

For imports, route the prepared artifact only through `core.data-loader` as a
task-routed load. Its `core.data-loader.task-hook` lifecycle owns final Task
Context binding, rule resolution, preview, approval, and verification. Follow
`core/data-loader/references/task-rule-registry-execution.md` for that
lifecycle. Do not invoke Task Validator directly or add a second import
approval. All writes use `core.data-loader`; direct REST writes are prohibited.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using costAccountingCostBooks as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Cost Books`
- Setup task code: `ORA_CST_COST_BOOKS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `costAccountingCostBooks` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "costAccountingCostBooks" \
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
