---
skill_id: "erp.financials.payables.manage-payment-options"
name: "Manage Payment Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Payment Options under the Payables functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Payables"
functional_area_code: "FIN_PAYABLES_DEPLOYED"
task_code: "AP_MANAGE_PAYMENT_OPTIONS"
task_name: "Manage Payment Options"
parent_skill_id: "erp.financials.payables"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/payables/manage-payment-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/payables/manage-payment-options/current/"
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

# Manage Payment Options Setup Task Guidance

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AP_SYSTEM_PARAMETER::BuName, AP_SYSTEM_PARAMETER::EnterpriseId, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes, AP_SYSTEM_PARAMETER::TermName -->
<!-- fscr-update-fields: AP_SYSTEM_PARAMETER::WhenToAccountPmt, AP_SYSTEM_PARAMETER::PostDatedPaymentsFlag, AP_SYSTEM_PARAMETER::AllowSupplierBankOverride, AP_SYSTEM_PARAMETER::PayDocCategoryOverride, AP_SYSTEM_PARAMETER::AllowPymtThirdPartyOvrd, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes -->

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Payment Options` under `Payables`.

## Supported Operations

This task supports creating a new Payment Options setup row and updating an exact existing setup row. It does not support delete or end-date operations. Only the operation-specific fields documented in [Input Validation](ora-resource/ora_input_validation.md) and [Design Enforcement](ora-resource/ora_design_enforcement.md) are permitted; all other fields remain blocked.

## Task Behavior

Use this task to configure Payment-owned values for the shared Payables system
options row, including payment accounting timing, post-dated payment policy,
bank-charge responsibility, rate requirements, and payment terms. An update
preserves unrelated Invoice Options values; do not use this task to change
Invoice-owned settings.

- Build every candidate from the exact Manage Payment Options package and a
  fresh, uniquely matched business-unit baseline. Preserve the package root,
  CSV headers and order, and all baseline values except the Payment-owned
  values explicitly requested for change.
- Validate the resulting complete shared row with the Invoice Options field
  contract before preview. This protects Invoice-owned prerequisites and
  preservation rules, but does not authorize this task to add, default, or
  change Invoice-owned values. Invoke only the sibling validator, not the full
  Invoice Options skill, to avoid a recursive workflow.
- Do not infer a Payment Options value from an export. Validate supplied values
  only against their documented field contract; preserve an omitted optional
  field exactly as it appears in the baseline. Do not add a CSV column that is
  absent from the exact task template.
- Before normalization, run `scripts/resolve_lookup_prerequisites.py` for an
  applicable read-only preflight. Preserve an advisory lookup result with the
  requested value; Fusion performs the final target-context validation during
  the approved import.
- Route every import through `core.data-loader` in FSM mode. A candidate still
  requires an immutable preview and explicit approval before submission.

## Setup Task Skill Contract

- task_code: `AP_MANAGE_PAYMENT_OPTIONS`
- task_name: `Manage Payment Options`
- parent_skill_id: `erp.financials.payables`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Payables`
- functional_area_code: `FIN_PAYABLES_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Payment Options` under `Payables`.

## Setup Task Metadata

- Task name: `Manage Payment Options`
- Task code: `AP_MANAGE_PAYMENT_OPTIONS`
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

- Offering: `Financials`
- Functional area / Setup Object: `Payables`
- Setup task name: `Manage Payment Options`
- Setup task code: `AP_MANAGE_PAYMENT_OPTIONS`




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

`AP_SYSTEM_PARAMETER` is a shared row, but Invoice Options and Payment Options
own different fields. Before normalization, run
`scripts/resolve_lookup_prerequisites.py`. It performs the relevant read-only
Invoice Options check, records advisory results, and never writes to Fusion.

For every Payment Options create or update, validate the complete resulting row
against the Invoice Options contract. This ensures an update cannot bypass an
Invoice-owned prerequisite, default, or preservation rule. Conversely, an
Invoice Options update validates its resulting Payment-owned values with this
contract. An Invoice Options create validates only Payment values supplied by
the requester; it never adds optional Payment values. This dependency does not
mean that either task should guess or populate fields from the other page.
Invoke only the sibling validator, not the full Invoice Options skill, to avoid
a recursive workflow.

For one business unit, a single NLP request that includes both Payment Options
and Invoice Options changes is one shared-row transaction. Merge all requested
fields into one canonical `AP_SYSTEM_PARAMETER` row before candidate generation
and validate both contracts against it. When any Invoice Options field is
present, the Invoice Options package is the sole writer; do not generate or
submit a second Payment Options full-row package. Use this Payment Options
package only for a payment-only request.

Use the parent functional-area skill `erp.financials.payables` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
