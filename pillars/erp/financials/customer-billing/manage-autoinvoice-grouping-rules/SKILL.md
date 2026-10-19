---
skill_id: "erp.financials.customer-billing.manage-autoinvoice-grouping-rules"
name: "Manage AutoInvoice Grouping Rules Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage AutoInvoice Grouping Rules under the Customer Billing functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_AUTOINVOICE_GROUPING_RULES"
task_name: "Manage AutoInvoice Grouping Rules"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-autoinvoice-grouping-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-autoinvoice-grouping-rules/current/"
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

# Manage AutoInvoice Grouping Rules Setup Task Guidance

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::StartDate -->
<!-- fscr-create-fields: AR_AI_GROUPING_RULE::Description, AR_AI_GROUPING_RULE::EndDate, AR_AI_GROUPING_RULE::LineOrderingRuleName, AR_AI_GROUPING_RULE::Name, AR_AI_GROUPING_RULE::StartDate, ORA_AR_AI_GRP_TXN_TYPE::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_TYPE::Class11, ORA_AR_AI_GRP_TXN_REQUEST::AR_AI_GROUPING_RULE.Name, ORA_AR_AI_GRP_TXN_REQUEST::FromColumnName, ORA_AR_AI_GRP_TXN_REQUEST::ORA_AR_AI_GRP_TXN_TYPE.Class11 -->

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage AutoInvoice Grouping Rules` under `Customer Billing`.

## Setup Task Skill Contract

- task_code: `AR_MANAGE_AUTOINVOICE_GROUPING_RULES`
- task_name: `Manage AutoInvoice Grouping Rules`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage AutoInvoice Grouping Rules` under `Customer Billing`.

## Setup Task Metadata

- Task name: `Manage AutoInvoice Grouping Rules`
- Task code: `AR_MANAGE_AUTOINVOICE_GROUPING_RULES`
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
- Setup task name: `Manage AutoInvoice Grouping Rules`
- Setup task code: `AR_MANAGE_AUTOINVOICE_GROUPING_RULES`




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

## Task-Owned Setup Contract

Use the exact `AR_MANAGE_AUTOINVOICE_GROUPING_RULES` FSM package. Its import root is `AR_AI_GROUPING_RULE.csv`; `ORA_AR_AI_GRP_TXN_TYPE.csv` supplies transaction-class children and `ORA_AR_AI_GRP_TXN_REQUEST.csv` supplies optional group-by children. Preserve `ASM_SETUP_CSV_METADATA.xml`, all three exact headers, parent reference columns, and their node paths and sequences. The task's generated [adapter](e2e-adapter.json) is an offline package contract; the active Run Book and `core.data-loader` own any import. The reviewed import hook resolves existing roots by the Name alternate key. Create and positive updates to Description, StartDate, EndDate and LineOrderingRuleName have revision-bound live evidence; the selected maintenance Core handoff also completed a Description update with full fresh-export reconciliation. Keep each campaign's tested revision, approved scope, process results and reconciliation in its project evidence. Source-supported operations do not require a reverse-update test as an ordinary execution prerequisite.

For a create request, require a unique `Name` of at most 40 characters without the reserved `ORA_` prefix and an explicit `StartDate`. `Description` is optional and at most 80 characters. If supplied, `EndDate` must be on or after `StartDate`. `Class11` accepts the seeded package codes `C`, `D`, and `I` for Credit Memo, Debit Memo, and Invoice; do not repeat a class under one rule. Each optional `FromColumnName` must identify an available grouping column for its parent class, with no duplicate characteristic under that class. The import hook resolves line-ordering and grouping-column names internally; no supported public setup GET has been established for these references. See [input validation](ora-resource/ora_input_validation.md), [reference lookups](ora-resource/ora_reference_lookups.md), and [dependency readiness](ora-resource/ora_dependency_readiness.md).

The deployed descriptive flexfield context and segment rules, accepted `ConsBillingUseFlag` codes, and consolidated-billing-specific grouping choices are unresolved. For those fields, retain known constraints and identify the exact missing environment/reference evidence. For eligible update uncertainty, use the exact-field application-validation policy below; do not disable the update operation. Do not infer create defaults from UI prefill. Do not infer rename, physical deletion, or verified end-date retirement. Ordinary updates follow the field-specific source contract and governed application-validation policy below. Follow [defaulting rules](ora-resource/ora_defaulting_rules.md), [design enforcement](ora-resource/ora_design_enforcement.md), and [error handling](ora-resource/ora_error_handling.md). The [rule registry](ora-resource/ora_rule_registry.json) provides the compiled static decision graph.

The generated [test catalog](e2e-test-catalog.json) and [adapter](e2e-adapter.json) define static and offline cases and live campaign requirements. For a live test, obtain a source-backed cleanup or governed retained-state policy and candidate-bound approval for that campaign. Evaluate these requirements from the active campaign's actual authority and evidence; historical test dispositions do not narrow ordinary implementor requests. Route imports through the active Run Book and selected Core Data Loader governance.

## Source-Backed Task Behavior

- The FSM task package contains a grouping-rule root, transaction-class children and optional group-by children. Preserve all three CSV members and exact parent columns; the import root is `AR_AI_GROUPING_RULE`. Sources: `SRC-FSM-PACKAGE`, `SRC-CODE-AMIMPL`, `SRC-CODE-PRIMARY-VO`.
- A new rule requires an explicit unique `Name` of at most 40 characters and an explicit `StartDate`. Customer-created names beginning `ORA_` are reserved. The UI's date prefill does not establish an FSM import default. Sources: `SRC-CODE-PRIMARY-EO`, `SRC-CODE-PRIMARY-VO`, `SRC-CODE-AMIMPL`.
- `Description` is optional and at most 80 characters. If `EndDate` is supplied, it must be on or after `StartDate`. Sources: `SRC-CODE-PRIMARY-EO`, `SRC-CODE-PRIMARY-VO`.
- A transaction-class child uses `Class11` with the system-seeded values `C` (Credit Memo), `D` (Debit Memo) or `I` (Invoice). Reject a repeated class under one rule. Sources: `SRC-CODE-CLASS-SEED`, `SRC-CODE-CLASS-EO`, `SRC-CODE-CLASS-VO`.
- An optional group-by child uses exact `FromColumnName` under its parent rule and class. The import hook resolves the name to a grouping-column ID and reports a missing name; reject repeated characteristics within a class. Confirm available choices in the target environment. Sources: `SRC-CODE-AMIMPL`, `SRC-CODE-GROUPBY-VO`, `SRC-CODE-GROUPBY-EO`, `SRC-CODE-GROUPBY-SEED`.
- An optional `LineOrderingRuleName` resolves to an existing line-ordering rule by exact name inside FSM import. A missing reference removes the affected imported row and reports an error. Sources: `SRC-CODE-AMIMPL`, `SRC-CODE-ORDER-VO`.
- When descriptive flexfield fields or `ConsBillingUseFlag` are requested, verify the deployed context, segments or accepted flag code and applicability; eligible update uncertainty follows the exact-field application-validation policy below. Consolidated-billing-specific grouping choices also require target-environment verification. Sources: `SRC-CODE-PRIMARY-EO`, `SRC-CODE-GROUPBY-CHOICE-VVO`, `SRC-CODE-GROUPBY-SEED`.
- The import hook matches roots through AltKey_Name; the primary VO/EO exposes changeable Description, StartDate, EndDate and the resolved line-ordering reference. Prepare those root-field updates using unchanged Name. Keep remaining field gaps unresolved and eligible for governed application validation; physical deletion and verified end-date retirement remain unestablished. Sources: `SRC-CODE-AMIMPL`, `SRC-CODE-PRIMARY-VO`, `SRC-CODE-PRIMARY-EO`.

## Existing-record update and evidence-gap policy

For an existing-record update, resolve exactly one root by unchanged Name from a fresh same-task export. Description, StartDate, EndDate and LineOrderingRuleName have source-backed root-field update contracts. Description is limited to 80 characters; StartDate remains required, EndDate must not precede StartDate, and a supplied line-ordering name must resolve exactly. Preserve every unrequested root/child value. Other non-key update fields remain evidence_unresolved; apply known validations and offer the exact-operation/exact-field governed application-validation choice when only eligible field-contract or resolver uncertainty remains. Record the accepted uncertainty and warning in the blueprint and candidate-bound preview. Keys, audit fields, malformed packages, unresolved target identity, proven-invalid values, source-proven unsupported operations and missing authorization are not overrideable. Retain normal Run Book/Data Loader routing, candidate-specific approval, one submission, diagnostics and fresh-export reconciliation.

Sources: SRC-CODE-AMIMPL, SRC-CODE-PRIMARY-VO, SRC-CODE-PRIMARY-EO; installed Builder loader-validation policy.

## Core Data Loader handoff

For imports, read and follow `core/data-loader/SKILL.md` and its selected Task Hook workflow in the same repository revision. Delegate validation, preview, approval and submission through those documented entry points; this task does not select the loader's internal storage or approval mechanism. Follow the selected Core workflow whether it uses an interactive session or persisted preflight envelopes, including its artifact handling, integrity verification and recovery requirements. Preserve native FSM ZIP bytes, exact package members, ordered task-rule evaluation, candidate-specific environment and Run Book binding, authorization, one submission, diagnostics and fresh-export reconciliation. Do not mix commands or approval artifacts from different workflows or revisions, reconstruct approvals, or bypass a missing required interface; report a framework gap for architecture review without changing core/shared code. Offline task-adapter normalization, package validation and test evidence do not replace Core Data Loader validation or authorization, and an earlier campaign grant is reusable only to the extent expressly permitted by the active Core contract and user-approved scope. Prior live evidence remains bound to its tested revision.
