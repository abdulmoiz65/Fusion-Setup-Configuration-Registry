---
skill_id: "erp.financials.customer-billing"
name: "Customer Billing Implementation Guidance"
description: "Routes ERP Financials Customer Billing implementation requests, including Transaction Types, Transaction Sources, Receivables Payment Terms, Remit-to Addresses, and AutoAccounting Rules, to the applicable catalog-backed setup-task skill."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.3.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "customer_billing_scope"
  - "customer_billing_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "AR_MANAGE_RECEIVABLES_PAYMENT_TERMS"
  - "AR_MANAGE_TRANSACTION_TYPES"
  - "AR_MANAGE_TRANSACTION_SOURCES"
  - "AR_MANAGE_AUTOINVOICE_GROUPING_RULES"
  - "AR_MANAGE_REMIT_TO_ADDRESSES"
  - "AR_MANAGE_AUTOACCOUNTING_RULES"
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

# Customer Billing Implementation Guidance

## Purpose

Provides ERP Financials implementation guidance for the Customer Billing functional area.

## When to Use

Use this functional-area skill after Financials scope is confirmed and the project needs customer billing setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Financials` (`XLE_FINANCIALS_JUR`)
- Functional area / Setup Object: `Customer Billing` (`ORA_FIN_CUST_BILL`)

## Setup Tasks

1. [Manage Transaction Types](manage-transaction-types/SKILL.md) (`AR_MANAGE_TRANSACTION_TYPES`)
2. [Manage Transaction Sources](manage-transaction-sources/SKILL.md) (`AR_MANAGE_TRANSACTION_SOURCES`)
3. [Manage AutoInvoice Grouping Rules](manage-autoinvoice-grouping-rules/SKILL.md) (`AR_MANAGE_AUTOINVOICE_GROUPING_RULES`)
4. [Manage Receivables Payment Terms](manage-receivables-payment-terms/SKILL.md) (`AR_MANAGE_RECEIVABLES_PAYMENT_TERMS`)
5. [Manage Remit to Addresses](manage-remit-to-addresses/SKILL.md) (`AR_MANAGE_REMIT_TO_ADDRESSES`)
6. [Manage AutoAccounting Rules](manage-autoaccounting-rules/SKILL.md) (`AR_MANAGE_AUTOACCOUNTING_RULES`)

## Customer Natural-Language Routing

Route business-language requests about customer payment terms to the nested
Manage Receivables Payment Terms skill. Route business-language requests about
remittance destinations and their receipt-from coverage to the nested Manage
Remit to Addresses skill. Route business-language requests about Receivables
default account derivation and AutoAccounting segment sources to the nested
Manage AutoAccounting Rules skill. The customer does not need to know FSM task
codes, CSV entity names, Data Loader, setup export/import services, or physical
tables.

Examples include:

- "Create a Net 30 payment term."
- "Make half due in 30 days and half due in 60 days."
- "End-date our legacy immediate payment term."
- "Move these approved payment terms into our test environment."
- "Check whether the payment terms load completed correctly."
- "Create a remit-to address for our California receipts."
- "Add a new receipt-from postal-code range to an existing remit-to address."
- "Derive the receivable account company segment from the transaction type."
- "Use a constant for the unearned revenue account segment."

## Inputs

- `implementation_objective`
- `project_context`
- `customer_billing_scope`
- `customer_billing_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
When a request actively includes Manage Transaction Sources and another setup task, name the separate task scopes and ask the implementor to confirm those scopes and which task to prepare first. Stop before task preparation until that scope decision is answered; field-level details alone do not establish scope confirmation. If the implementor already explicitly limits the request to Manage Transaction Sources, treat other tasks in an attached document as context and do not reopen the excluded scope.
