---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.receipt-accounting.manage-receipt-accounting-profile-options"
name: "Manage Receipt Accounting Profile Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Receipt Accounting Profile Options under the Receipt Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Receipt Accounting"
functional_area_code: "CMR_RECEIPT_ACCOUNTING"
task_code: "ORA_MANAGE_RECEIPT_ACCOUNTING_PROFILE_OPTIONS"
task_name: "Manage Receipt Accounting Profile Options"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.receipt-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
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
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/receipt-accounting/manage-receipt-accounting-profile-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/receipt-accounting/manage-receipt-accounting-profile-options/current/"
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

# Manage Receipt Accounting Profile Options Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Receipt Accounting Profile Options` under `Receipt Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_RECEIPT_ACCOUNTING_PROFILE_OPTIONS`
- task_name: `Manage Receipt Accounting Profile Options`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.receipt-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Receipt Accounting`
- functional_area_code: `CMR_RECEIPT_ACCOUNTING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Receipt Accounting Profile Options` under `Receipt Accounting`.

## Setup Task Metadata

- Task name: `Manage Receipt Accounting Profile Options`
- Task code: `ORA_MANAGE_RECEIPT_ACCOUNTING_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Receipt Accounting`
- Setup task name: `Manage Receipt Accounting Profile Options`
- Setup task code: `ORA_MANAGE_RECEIPT_ACCOUNTING_PROFILE_OPTIONS`

## Apps Common Profile Options Workflow

Route every `Manage Receipt Accounting Profile Options` request to
`core.fusion-api.apps-common`. Apps Common selects its `profile-options`
nested skill for profile-option definition and value operations. This task must
not bypass Apps Common by selecting a REST client or nested skill directly.

1. Read the profile definition by `ProfileOptionName` and identify the intended
   site, product, or user level.
2. For a configured-value change, read the current child value and verify that
   the selected level is enabled and updatable.
3. Resolve a user-level target through `profileUsers` before creating or
   changing a user-level value.
4. Present the exact environment, profile option, level, target, current value,
   and proposed value for explicit approval immediately before a write.
5. Do not retry a profile-option POST, PATCH, or DELETE automatically.

The generated CSV/FSM workflow remains available only for catalog-supported
setup-data export and import artifacts. It does not replace the Apps Common
route for any Receipt Accounting profile-option request.

## Receipt Accounting Profile Options

The following profile definitions belong to the Receipt Accounting application
context (`ApplicationId=10096`):

- `ORA_CMR_AUDIT_ACCRUALS_REDWOOD_ENABLED`
- `ORA_CMR_CUTOFF_RULES_REDWOOD_ENABLED`
- `ORA_CMR_EXCEPTIONS_REDWOOD_ENABLED`
- `ORA_CMR_HIDE_INFOLETS`
- `ORA_CMR_IGNORE_AP_ERV_TERV`
- `ORA_CMR_IGNORE_AP_INV_VAR_ALL`
- `ORA_CMR_LANDING_PAGE_REDWOOD_ENABLED`
- `ORA_CMR_MANAGE_ACCRUALS_REDWOOD_ENABLED`
- `ORA_CMR_REVIEW_DISTRIBUTIONS_REDWOOD_ENABLED`

Use the option name exactly as listed. Confirm the definition and per-level
enabled and updatable flags at runtime because availability and scope can vary
by environment and release.




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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.receipt-accounting` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
