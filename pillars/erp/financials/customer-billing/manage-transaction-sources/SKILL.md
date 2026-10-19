---
skill_id: "erp.financials.customer-billing.manage-transaction-sources"
name: "Manage Transaction Sources Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Transaction Sources under the Customer Billing functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_TRANSACTION_SOURCES"
task_name: "Manage Transaction Sources"
parent_skill_id: "erp.financials.customer-billing"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-transaction-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-transaction-sources/current/"
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

<!-- fscr-supported-operations: create, update -->

# Manage Transaction Sources Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Transaction Sources` under `Customer Billing`.

## Setup Task Skill Contract

- task_code: `AR_MANAGE_TRANSACTION_SOURCES`
- task_name: `Manage Transaction Sources`
- parent_skill_id: `erp.financials.customer-billing`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Customer Billing`
- functional_area_code: `ORA_FIN_CUST_BILL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Transaction Sources` under `Customer Billing`.

## Setup Task Metadata

- Task name: `Manage Transaction Sources`
- Task code: `AR_MANAGE_TRANSACTION_SOURCES`
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
- Functional area / Setup Object: `Customer Billing`
- Setup task name: `Manage Transaction Sources`
- Setup task code: `AR_MANAGE_TRANSACTION_SOURCES`

## Source-Backed Task Behavior

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: ORA_AR_TXN_BATCH_SOURCE::AutoTrxNumberingFlag, ORA_AR_TXN_BATCH_SOURCE::BatchSourceType, ORA_AR_TXN_BATCH_SOURCE::Description, ORA_AR_TXN_BATCH_SOURCE::InvalidLinesRule, ORA_AR_TXN_BATCH_SOURCE::LastBatchNum, ORA_AR_TXN_BATCH_SOURCE::Name, ORA_AR_TXN_BATCH_SOURCE::SetCode, ORA_AR_TXN_BATCH_SOURCE::StartDate, ORA_AR_TXN_BATCH_SOURCE::Status -->
<!-- fscr-update-fields: ORA_AR_TXN_BATCH_SOURCE::Description -->

- Treat `Name` plus `SetCode` as the portable business key for both `AR_BATCH_SOURCE` and `ORA_AR_TXN_BATCH_SOURCE`; do not use environment-specific numeric identifiers as input identity.
- Support only the evidence-backed `create` and `update` lifecycle operations, and keep all package generation, validation, determinism, rollback, and reconciliation work offline until a separately approved Data Loader import.
- Apply the evidence-backed relationship-partition ownership matrix: create targets `ORA_AR_TXN_BATCH_SOURCE` and reconciles through `AR_BATCH_SOURCE`. For update, first require the exact `Name` plus `SetCode` key to occur once across the fresh package and in exactly one entity; target and reconcile through that export-owning entity. Stop when the key is absent, duplicated, or present in both entities, and never move an existing row between package projections.
- Preserve the exact two-entity CSV schemas, header order, metadata node paths, every unspecified row, and every unspecified non-audit value; fail closed when a supplied template or baseline disagrees with the adapter contract.
- Keep Manual and Imported transaction-source semantics separate: `BatchSourceType=INV` is the Manual branch, while fields evidenced only for Imported sources apply only when `BatchSourceType=FOREIGN`; `InvalidLinesRule=Reject` is also evidenced for the Manual create path.
- On create, require `Name`, `SetCode`, `Description`, `BatchSourceType`, and `StartDate`; also require an integer `LastBatchNum` of at least 1 when `AutoTrxNumberingFlag=Y`, including a defaulted Y. The new numbering sequence uses this value directly as its start; do not invent or substitute a number.
- On create, default omitted fields to `Status=A`, `BatchSourceType=INV`, `AutoTrxNumberingFlag=Y`, and `InvalidLinesRule=Reject`; preserve any explicit value that is valid under the fixed value contract.
- Resolve grouping rule, reference-data set, document type, credit transaction source, legal entity, and transaction type from portable names, codes, sets, or identifiers; never invent a numeric identifier.
- Preserve the ordered self-reference contract: resolve `BatchSourceName` with `CmBatchSrcSetCode` after the credit-source entity is available, and block ambiguous or missing matches.
- Exclude Fusion who columns and the derived display fields `DefaultInvTrxType` and `LegalEntityName` from developer-supplied serialization.
- Treat `Description` as the only source-backed supported update field. Do not add evidence-unresolved fields to the `fscr-update-fields` allowlist or describe them as supported.
- For a non-key, non-audit field on the exact export-owning update entity whose update contract remains explicitly unresolved, first run every known deterministic type, value, length, resolver, identity, and package validation. If those checks pass, disclose the evidence gap and offer the governed application-validation path only with explicit implementor approval bound to the exact update operation, entity, fields, environment, and immutable candidate. Approval to try a value does not prove Fusion supports it.
- Keep `SalesTerritoryRule`, `ControlTrxCompletionFlag`, and `UsageCategoryCode` unresolved for update. Preserve their Partial resolver/value evidence: reject a known invalid value or a natural-language value that cannot be deterministically mapped, but do not turn incomplete evidence into an absolute unsupported-product conclusion for an exact package value that passes all deterministic checks.
- Never offer an unresolved-field override for `Name`, `SetCode`, audit or identity controls, source-proven unsupported fields, package-integrity requirements, authorization controls, or a field on an entity that does not own the exact fresh-export key. `AR_BATCH_SOURCE` remains non-targetable for create; it is eligible for update only when it uniquely owns that key, and none of its fields becomes source-backed supported merely because the entity is targetable.
- Treat physical deletion as evidence-unresolved. Never describe Status or EndDate retirement as delete or soft delete, and block deletion until an exact source-backed mechanism, owner, key, child/cascade, irreversibility, and recovery contract exists.
- After every existing source, field, ownership, and requirement check passes, an update whose requested values exactly equal the fresh baseline for one unique Name-plus-SetCode export owner returns `NO_OP` without an import ZIP. The result retains input/design hashes and business summary, with null candidate hash and empty inventory; never submit it to Data Loader. Already-restored update rollback follows the same rule. Any real change or create keeps the normal package and approval workflow.
- Keep Fusion writes outside this skill: Run Book owns normalized task intent and orchestration, Data Loader owns immutable preview and approved import, and no import, retry, or cleanup is authorized by static readiness.




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

Use the parent functional-area skill `erp.financials.customer-billing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For direct task entry containing another active setup-task request, return to the Customer Billing parent scope-confirmation gate before preparing an MTS package. Explicitly excluded document context does not expand the selected task scope.
