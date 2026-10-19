---
task_code: "FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION"
task_name: "Assign Business Unit Business Function"
parent_skill_id: "erp.financials.organization-structures"
pillar: "ERP"
offering: "Financials"
functional_area: "Organization Structures"
functional_area_code: "ORA_ASK_ORGANIZATION_STRUCTURE"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Assign Business Unit Business Function

## Setup Task Metadata

- Task name: `Assign Business Unit Business Function`
- Task code: `FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Acquire a same-task template/spec with `shared.setup-export.task-level-export`. Apply the parent no-full-data-export policy; current values come from declared GETs and verified current-workflow evidence. A populated export is allowed only through a named, authorized, genuinely scoped route; never request, consume or locally filter a full export as a substitute.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Organization Structures`
- Setup task name: `Assign Business Unit Business Function`
- Setup task code: `FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION`


## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Assign Business Unit Business Function` under `Organization Structures`.

## Mandatory Import Gates

1. Resolve an existing BU exactly. For a BU created in the active workflow, first review its successful creation log and verify its saved identity, active state and foundation; do not recreate it.
2. Resolve the controlled function code and derive `ModuleId`. Record the target function's `Enabled`, `GENERATE_FIN_TXN_FLAG`, and `SETUP_API` evidence when available. For a function that generates financial transactions, exactly resolve the named primary ledger and default legal entity and require both resolved IDs to equal the selected BU's `PrimaryLedgerId` and `LegalEntityId`.
3. Select the operation-specific package contract. Apply BUF_FSM_ADD_FUNCTION_V1 in ora_bulk_intake.md for an eligible additive assignment before imposing maintenance requirements. Include its name-linked parent row and documented business fields; this profile permits unknown generated keys/dates to remain blank. Other operations still require their exact supported contract and necessary current values.

`FUN_BU_USAGES.MODULE_ID` resolves to `FUN_BUSINESS_FUNCTIONS_VL.BUSINESS_FUNCTION_ID`. The reviewed UI view exposes `Enabled` as a nonpersistent attribute and does not filter the assignment list by it; never infer an enabled state when the target evidence does not supply one.

## Function-Assignment Design Guidance

Assign only business functions that the BU will operate. A BU does not need every function, and enabling unused functions increases configuration and control surface. Confirm the end-to-end operating model before assignment: subledger transactions are owned and partitioned by the financial BU, and most subledger processing is secured by BU.

- Evaluate dependencies, not just the owning team's preference. Project Accounting must be assigned in the same BU as Payables Invoicing. If Project Billing is in scope, plan the required co-existence of Project Accounting, Payables Invoicing, and Billing and Revenue Management.
- Confirm that Expenses and employee-assignment BU design are compatible: employee assignment drives expense ledger/chart-of-accounts and template derivation. Where multiple employee-assignment BUs use centralized payments, assess the required Expense Management assignments, service-provider relationship, template maintenance, and access model.
- Use Procurement and Requisitioning assignments to support the intended centralized or decentralized purchasing model. A procurement BU may be global because it does not generate accounting, but it must be associated with the finance BU in which purchase orders are created and matched to payables invoices.
- Validate the implications of any Payables Invoicing, Payables Payments, Billing and Revenue Management, Customer Payments, Materials Management, or Receiving assignment for ledger alignment, legal-entity processing, cross-BU settlement, security, and reporting.

## Validation Checkpoints

Verify the function matrix against the approved BU design, service-provider model, and data roles. Execute representative requisition-to-pay, invoice-to-payment, expense, project, and receivables flows for every enabled combination, including exceptions that cross BUs or legal entities.
  <!-- -->

## Saved BU Prerequisite

Resolve an existing BU exactly, or finish and verify its creation first. For a financial function, require its compatible stored primary ledger and legal entity and the complete LedgerFinder association. Read the controlled function-code mapping; never ask for or invent ModuleId. Use the declared ModuleIdFinder presence check and a matching task template for layout; keep presence, ConfigurationStatus and no-op comparison as distinct facts.

Select BUF_FSM_ADD_FUNCTION_V1 first. When eligible, use its bounded name-linked parent row from explicit decisions in the active workflow; missing generated OrganizationCode, effective dates or unexposed ConfigurationStatus do not independently block this additive path. Do not claim that omitted fields were read or independently preserved. For maintenance, an arbitrary pre-existing BU, optional parent changes or strict field-by-field preservation outside the profile, require the relevant permitted current evidence. After submission, apply the mandatory log-review gate, re-query exact BU identity/foundation and module membership, and disclose unexposed saved values. Any later service relationship still applies its own role and policy gates.


## Verification and Outcome Reporting Policy

Apply the parent's endpoint-only policy to this task and all delegates. No Fusion UI, screenshots, browser inspection or user-assisted screen verification is allowed for duplicate checks, validation or saved results. Use declared core-client endpoints and permitted framework evidence; unavailable facts remain explicitly unverified. Only core.auth may hand login to the user, without agent UI inspection.

Before quoting results, apply [mandatory log review](ora-resource/ora_error_handling.md#mandatory-log-review-before-outcome-reporting). Review matching FSM logs for submitted imports, or actual client/evaluated-rule evidence for reads, native actions and unsubmitted validation. Processing success and independently verified saved values are separate outcomes.
