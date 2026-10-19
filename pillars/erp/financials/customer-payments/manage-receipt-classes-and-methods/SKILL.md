---
skill_id: "erp.financials.customer-payments.manage-receipt-classes-and-methods"
name: "Manage Receipt Classes and Methods Setup Task Guidance"
description: "Handles business-language Oracle Receivables receipt-class and receipt-method setup requests, including their remittance bank accounts and credit-card error mappings. Resolves the exact catalog-backed FSM task, validates and deterministically prepares its four-entity CSV package, asks only for material business ambiguity, delegates every import to Core Data Loader, and verifies persisted state without requiring customers to know task codes, CSV files, services, or database tables."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Payments"
functional_area_code: "ORA_FIN_CUSTOMER_PAYMENTS"
task_code: "AR_MANAGE_RECEIPT_CLASSES_AND_METHODS"
task_name: "Manage Receipt Classes and Methods"
parent_skill_id: "erp.financials.customer-payments"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.10.2"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "business_flow_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "offline_package_review"
  - "candidate_handoff"
  - "reconciliation_report"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-payments/manage-receipt-classes-and-methods/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-payments/manage-receipt-classes-and-methods/current/"
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
side_effects:
  - "After Core Data Loader creates an immutable preview and the customer supplies the required standalone approval, the authorized FSM adapter may create or change receipt-class and receipt-method setup in the approved Fusion environment."
required_privileges: []
---

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields:
AR_CC_ERROR_MAPPINGS::AR_RECEIPT_CLASS.Name, AR_CC_ERROR_MAPPINGS::AR_RECEIPT_METHOD.Name, AR_CC_ERROR_MAPPINGS::CcActionCode, AR_CC_ERROR_MAPPINGS::CcErrorCode, AR_CC_ERROR_MAPPINGS::CcErrorText, AR_CC_ERROR_MAPPINGS::CcTrxCategory, AR_CC_ERROR_MAPPINGS::ErrorNotes, AR_CC_ERROR_MAPPINGS::NoDays, AR_CC_ERROR_MAPPINGS::SubsequentActionCode, AR_RECEIPT_CLASS::Attribute1, AR_RECEIPT_CLASS::Attribute10, AR_RECEIPT_CLASS::Attribute11, AR_RECEIPT_CLASS::Attribute12, AR_RECEIPT_CLASS::Attribute13, AR_RECEIPT_CLASS::Attribute14, AR_RECEIPT_CLASS::Attribute15, AR_RECEIPT_CLASS::Attribute2, AR_RECEIPT_CLASS::Attribute3, AR_RECEIPT_CLASS::Attribute4, AR_RECEIPT_CLASS::Attribute5, AR_RECEIPT_CLASS::Attribute6, AR_RECEIPT_CLASS::Attribute7, AR_RECEIPT_CLASS::Attribute8, AR_RECEIPT_CLASS::Attribute9, AR_RECEIPT_CLASS::AttributeCategory, AR_RECEIPT_CLASS::BillOfExchangeFlag, AR_RECEIPT_CLASS::ClearFlag, AR_RECEIPT_CLASS::ConfirmFlag, AR_RECEIPT_CLASS::CreationMethodCode, AR_RECEIPT_CLASS::CreationStatus, AR_RECEIPT_CLASS::GlobalAttribute1, AR_RECEIPT_CLASS::GlobalAttribute10, AR_RECEIPT_CLASS::GlobalAttribute11, AR_RECEIPT_CLASS::GlobalAttribute12, AR_RECEIPT_CLASS::GlobalAttribute13, AR_RECEIPT_CLASS::GlobalAttribute14, AR_RECEIPT_CLASS::GlobalAttribute15, AR_RECEIPT_CLASS::GlobalAttribute16, AR_RECEIPT_CLASS::GlobalAttribute17, AR_RECEIPT_CLASS::GlobalAttribute18, AR_RECEIPT_CLASS::GlobalAttribute19, AR_RECEIPT_CLASS::GlobalAttribute2, AR_RECEIPT_CLASS::GlobalAttribute20, AR_RECEIPT_CLASS::GlobalAttribute3, AR_RECEIPT_CLASS::GlobalAttribute4, AR_RECEIPT_CLASS::GlobalAttribute5, AR_RECEIPT_CLASS::GlobalAttribute6, AR_RECEIPT_CLASS::GlobalAttribute7, AR_RECEIPT_CLASS::GlobalAttribute8, AR_RECEIPT_CLASS::GlobalAttribute9, AR_RECEIPT_CLASS::GlobalAttributeCategory, AR_RECEIPT_CLASS::Name, AR_RECEIPT_CLASS::NotesReceivable, AR_RECEIPT_CLASS::RemitFlag, AR_RECEIPT_CLASS::RemitMethodCode, AR_RECEIPT_METHOD_ACCOUNT::AR_RECEIPT_CLASS.Name, AR_RECEIPT_METHOD_ACCOUNT::AR_RECEIPT_METHOD.Name, AR_RECEIPT_METHOD_ACCOUNT::Attribute1, AR_RECEIPT_METHOD_ACCOUNT::Attribute10, AR_RECEIPT_METHOD_ACCOUNT::Attribute11, AR_RECEIPT_METHOD_ACCOUNT::Attribute12, AR_RECEIPT_METHOD_ACCOUNT::Attribute13, AR_RECEIPT_METHOD_ACCOUNT::Attribute14, AR_RECEIPT_METHOD_ACCOUNT::Attribute15, AR_RECEIPT_METHOD_ACCOUNT::Attribute2, AR_RECEIPT_METHOD_ACCOUNT::Attribute3, AR_RECEIPT_METHOD_ACCOUNT::Attribute4, AR_RECEIPT_METHOD_ACCOUNT::Attribute5, AR_RECEIPT_METHOD_ACCOUNT::Attribute6, AR_RECEIPT_METHOD_ACCOUNT::Attribute7, AR_RECEIPT_METHOD_ACCOUNT::Attribute8, AR_RECEIPT_METHOD_ACCOUNT::Attribute9, AR_RECEIPT_METHOD_ACCOUNT::AttributeCategory, AR_RECEIPT_METHOD_ACCOUNT::BankAccountName, AR_RECEIPT_METHOD_ACCOUNT::BankChargesCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BankName, AR_RECEIPT_METHOD_ACCOUNT::BrCollectionDays, AR_RECEIPT_METHOD_ACCOUNT::BrFactorCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BrRemittanceCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BrStdRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::BrStdRxTrxOrgId, AR_RECEIPT_METHOD_ACCOUNT::BuName, AR_RECEIPT_METHOD_ACCOUNT::CashCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::ClaimBuName, AR_RECEIPT_METHOD_ACCOUNT::ClaimRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::ClearingDays, AR_RECEIPT_METHOD_ACCOUNT::CurrencyCode, AR_RECEIPT_METHOD_ACCOUNT::EarnedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::EdiscBuName, AR_RECEIPT_METHOD_ACCOUNT::EdiscRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::EndDate, AR_RECEIPT_METHOD_ACCOUNT::FactorCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute1, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute10, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute11, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute12, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute13, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute14, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute15, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute16, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute17, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute18, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute19, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute2, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute20, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute3, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute4, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute5, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute6, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute7, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute8, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute9, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttributeCategory, AR_RECEIPT_METHOD_ACCOUNT::MinReceiptAmount, AR_RECEIPT_METHOD_ACCOUNT::Name, AR_RECEIPT_METHOD_ACCOUNT::OnAccountCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::OverrideRemitAccountFlag, AR_RECEIPT_METHOD_ACCOUNT::PrimaryFlag, AR_RECEIPT_METHOD_ACCOUNT::ReceiptClearingCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::RemittanceCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::RiskEliminationDays, AR_RECEIPT_METHOD_ACCOUNT::ShortTermDebtCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::StartDate, AR_RECEIPT_METHOD_ACCOUNT::UnappliedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::UnearnedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::UnEdiscBuName, AR_RECEIPT_METHOD_ACCOUNT::UnediscRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::UnidentifiedCcidSegments, AR_RECEIPT_METHOD::AR_RECEIPT_CLASS.Name, AR_RECEIPT_METHOD::Attribute1, AR_RECEIPT_METHOD::Attribute10, AR_RECEIPT_METHOD::Attribute11, AR_RECEIPT_METHOD::Attribute12, AR_RECEIPT_METHOD::Attribute13, AR_RECEIPT_METHOD::Attribute14, AR_RECEIPT_METHOD::Attribute15, AR_RECEIPT_METHOD::Attribute2, AR_RECEIPT_METHOD::Attribute3, AR_RECEIPT_METHOD::Attribute4, AR_RECEIPT_METHOD::Attribute5, AR_RECEIPT_METHOD::Attribute6, AR_RECEIPT_METHOD::Attribute7, AR_RECEIPT_METHOD::Attribute8, AR_RECEIPT_METHOD::Attribute9, AR_RECEIPT_METHOD::AttributeCategory, AR_RECEIPT_METHOD::BrCustTrxTypeName, AR_RECEIPT_METHOD::BrInheritInvNumFlag, AR_RECEIPT_METHOD::BrMaxAcctdAmount, AR_RECEIPT_METHOD::BrMinAcctdAmount, AR_RECEIPT_METHOD::DmInheritReceiptNumFlag, AR_RECEIPT_METHOD::EndDate, AR_RECEIPT_METHOD::GlobalAttribute1, AR_RECEIPT_METHOD::GlobalAttribute10, AR_RECEIPT_METHOD::GlobalAttribute11, AR_RECEIPT_METHOD::GlobalAttribute12, AR_RECEIPT_METHOD::GlobalAttribute13, AR_RECEIPT_METHOD::GlobalAttribute14, AR_RECEIPT_METHOD::GlobalAttribute15, AR_RECEIPT_METHOD::GlobalAttribute16, AR_RECEIPT_METHOD::GlobalAttribute17, AR_RECEIPT_METHOD::GlobalAttribute18, AR_RECEIPT_METHOD::GlobalAttribute19, AR_RECEIPT_METHOD::GlobalAttribute2, AR_RECEIPT_METHOD::GlobalAttribute20, AR_RECEIPT_METHOD::GlobalAttribute3, AR_RECEIPT_METHOD::GlobalAttribute4, AR_RECEIPT_METHOD::GlobalAttribute5, AR_RECEIPT_METHOD::GlobalAttribute6, AR_RECEIPT_METHOD::GlobalAttribute7, AR_RECEIPT_METHOD::GlobalAttribute8, AR_RECEIPT_METHOD::GlobalAttribute9, AR_RECEIPT_METHOD::GlobalAttributeCategory, AR_RECEIPT_METHOD::ISO20022DirectDebitFlag, AR_RECEIPT_METHOD::LeadDays, AR_RECEIPT_METHOD::MaturityDateRuleCode, AR_RECEIPT_METHOD::MerchantRef, AR_RECEIPT_METHOD::Name, AR_RECEIPT_METHOD::PaymentChannelCode, AR_RECEIPT_METHOD::PaymentTypeCode, AR_RECEIPT_METHOD::PrintedName, AR_RECEIPT_METHOD::ReceiptCreationRuleCode, AR_RECEIPT_METHOD::ReceiptInheritInvNumFlag, AR_RECEIPT_METHOD::StartDate
 -->
<!-- fscr-update-fields:
AR_CC_ERROR_MAPPINGS::CcActionCode, AR_CC_ERROR_MAPPINGS::CcErrorText, AR_CC_ERROR_MAPPINGS::ErrorNotes, AR_CC_ERROR_MAPPINGS::NoDays, AR_CC_ERROR_MAPPINGS::SubsequentActionCode, AR_RECEIPT_CLASS::Attribute1, AR_RECEIPT_CLASS::Attribute10, AR_RECEIPT_CLASS::Attribute11, AR_RECEIPT_CLASS::Attribute12, AR_RECEIPT_CLASS::Attribute13, AR_RECEIPT_CLASS::Attribute14, AR_RECEIPT_CLASS::Attribute15, AR_RECEIPT_CLASS::Attribute2, AR_RECEIPT_CLASS::Attribute3, AR_RECEIPT_CLASS::Attribute4, AR_RECEIPT_CLASS::Attribute5, AR_RECEIPT_CLASS::Attribute6, AR_RECEIPT_CLASS::Attribute7, AR_RECEIPT_CLASS::Attribute8, AR_RECEIPT_CLASS::Attribute9, AR_RECEIPT_CLASS::AttributeCategory, AR_RECEIPT_CLASS::BillOfExchangeFlag, AR_RECEIPT_CLASS::ClearFlag, AR_RECEIPT_CLASS::ConfirmFlag, AR_RECEIPT_CLASS::GlobalAttribute1, AR_RECEIPT_CLASS::GlobalAttribute10, AR_RECEIPT_CLASS::GlobalAttribute11, AR_RECEIPT_CLASS::GlobalAttribute12, AR_RECEIPT_CLASS::GlobalAttribute13, AR_RECEIPT_CLASS::GlobalAttribute14, AR_RECEIPT_CLASS::GlobalAttribute15, AR_RECEIPT_CLASS::GlobalAttribute16, AR_RECEIPT_CLASS::GlobalAttribute17, AR_RECEIPT_CLASS::GlobalAttribute18, AR_RECEIPT_CLASS::GlobalAttribute19, AR_RECEIPT_CLASS::GlobalAttribute2, AR_RECEIPT_CLASS::GlobalAttribute20, AR_RECEIPT_CLASS::GlobalAttribute3, AR_RECEIPT_CLASS::GlobalAttribute4, AR_RECEIPT_CLASS::GlobalAttribute5, AR_RECEIPT_CLASS::GlobalAttribute6, AR_RECEIPT_CLASS::GlobalAttribute7, AR_RECEIPT_CLASS::GlobalAttribute8, AR_RECEIPT_CLASS::GlobalAttribute9, AR_RECEIPT_CLASS::GlobalAttributeCategory, AR_RECEIPT_CLASS::NotesReceivable, AR_RECEIPT_CLASS::RemitFlag, AR_RECEIPT_CLASS::RemitMethodCode, AR_RECEIPT_METHOD_ACCOUNT::Attribute1, AR_RECEIPT_METHOD_ACCOUNT::Attribute10, AR_RECEIPT_METHOD_ACCOUNT::Attribute11, AR_RECEIPT_METHOD_ACCOUNT::Attribute12, AR_RECEIPT_METHOD_ACCOUNT::Attribute13, AR_RECEIPT_METHOD_ACCOUNT::Attribute14, AR_RECEIPT_METHOD_ACCOUNT::Attribute15, AR_RECEIPT_METHOD_ACCOUNT::Attribute2, AR_RECEIPT_METHOD_ACCOUNT::Attribute3, AR_RECEIPT_METHOD_ACCOUNT::Attribute4, AR_RECEIPT_METHOD_ACCOUNT::Attribute5, AR_RECEIPT_METHOD_ACCOUNT::Attribute6, AR_RECEIPT_METHOD_ACCOUNT::Attribute7, AR_RECEIPT_METHOD_ACCOUNT::Attribute8, AR_RECEIPT_METHOD_ACCOUNT::Attribute9, AR_RECEIPT_METHOD_ACCOUNT::AttributeCategory, AR_RECEIPT_METHOD_ACCOUNT::BankChargesCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BrCollectionDays, AR_RECEIPT_METHOD_ACCOUNT::BrFactorCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BrRemittanceCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::BrStdRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::BrStdRxTrxOrgId, AR_RECEIPT_METHOD_ACCOUNT::CashCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::ClaimBuName, AR_RECEIPT_METHOD_ACCOUNT::ClaimRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::ClearingDays, AR_RECEIPT_METHOD_ACCOUNT::EarnedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::EdiscBuName, AR_RECEIPT_METHOD_ACCOUNT::EdiscRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::EndDate, AR_RECEIPT_METHOD_ACCOUNT::FactorCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute1, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute10, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute11, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute12, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute13, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute14, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute15, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute16, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute17, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute18, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute19, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute2, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute20, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute3, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute4, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute5, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute6, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute7, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute8, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttribute9, AR_RECEIPT_METHOD_ACCOUNT::GlobalAttributeCategory, AR_RECEIPT_METHOD_ACCOUNT::MinReceiptAmount, AR_RECEIPT_METHOD_ACCOUNT::OnAccountCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::OverrideRemitAccountFlag, AR_RECEIPT_METHOD_ACCOUNT::PrimaryFlag, AR_RECEIPT_METHOD_ACCOUNT::ReceiptClearingCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::RemittanceCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::RiskEliminationDays, AR_RECEIPT_METHOD_ACCOUNT::ShortTermDebtCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::UnappliedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::UnearnedCcidSegments, AR_RECEIPT_METHOD_ACCOUNT::UnEdiscBuName, AR_RECEIPT_METHOD_ACCOUNT::UnediscRxTrxName, AR_RECEIPT_METHOD_ACCOUNT::UnidentifiedCcidSegments, AR_RECEIPT_METHOD::Attribute1, AR_RECEIPT_METHOD::Attribute10, AR_RECEIPT_METHOD::Attribute11, AR_RECEIPT_METHOD::Attribute12, AR_RECEIPT_METHOD::Attribute13, AR_RECEIPT_METHOD::Attribute14, AR_RECEIPT_METHOD::Attribute15, AR_RECEIPT_METHOD::Attribute2, AR_RECEIPT_METHOD::Attribute3, AR_RECEIPT_METHOD::Attribute4, AR_RECEIPT_METHOD::Attribute5, AR_RECEIPT_METHOD::Attribute6, AR_RECEIPT_METHOD::Attribute7, AR_RECEIPT_METHOD::Attribute8, AR_RECEIPT_METHOD::Attribute9, AR_RECEIPT_METHOD::AttributeCategory, AR_RECEIPT_METHOD::BrCustTrxTypeName, AR_RECEIPT_METHOD::BrInheritInvNumFlag, AR_RECEIPT_METHOD::BrMaxAcctdAmount, AR_RECEIPT_METHOD::BrMinAcctdAmount, AR_RECEIPT_METHOD::DmInheritReceiptNumFlag, AR_RECEIPT_METHOD::EndDate, AR_RECEIPT_METHOD::GlobalAttribute1, AR_RECEIPT_METHOD::GlobalAttribute10, AR_RECEIPT_METHOD::GlobalAttribute11, AR_RECEIPT_METHOD::GlobalAttribute12, AR_RECEIPT_METHOD::GlobalAttribute13, AR_RECEIPT_METHOD::GlobalAttribute14, AR_RECEIPT_METHOD::GlobalAttribute15, AR_RECEIPT_METHOD::GlobalAttribute16, AR_RECEIPT_METHOD::GlobalAttribute17, AR_RECEIPT_METHOD::GlobalAttribute18, AR_RECEIPT_METHOD::GlobalAttribute19, AR_RECEIPT_METHOD::GlobalAttribute2, AR_RECEIPT_METHOD::GlobalAttribute20, AR_RECEIPT_METHOD::GlobalAttribute3, AR_RECEIPT_METHOD::GlobalAttribute4, AR_RECEIPT_METHOD::GlobalAttribute5, AR_RECEIPT_METHOD::GlobalAttribute6, AR_RECEIPT_METHOD::GlobalAttribute7, AR_RECEIPT_METHOD::GlobalAttribute8, AR_RECEIPT_METHOD::GlobalAttribute9, AR_RECEIPT_METHOD::GlobalAttributeCategory, AR_RECEIPT_METHOD::ISO20022DirectDebitFlag, AR_RECEIPT_METHOD::LeadDays, AR_RECEIPT_METHOD::MaturityDateRuleCode, AR_RECEIPT_METHOD::MerchantRef, AR_RECEIPT_METHOD::PaymentChannelCode, AR_RECEIPT_METHOD::PaymentTypeCode, AR_RECEIPT_METHOD::PrintedName, AR_RECEIPT_METHOD::ReceiptCreationRuleCode, AR_RECEIPT_METHOD::ReceiptInheritInvNumFlag
 -->

# Manage Receipt Classes and Methods

## Purpose

Plan, clarify, validate, package, route, monitor, and verify the exact
`Manage Receipt Classes and Methods` FSM task. Treat receipt classes, their
receipt methods, remittance bank accounts, and credit-card error mappings as
one governed hierarchy. Fail closed instead of inventing business choices or
target references.

## Source-Backed Task Behavior

- Treat `AR_RECEIPT_CLASS` as the parent, `AR_RECEIPT_METHOD` as its child,
  and `AR_RECEIPT_METHOD_ACCOUNT` plus `AR_CC_ERROR_MAPPINGS` as children of
  an exact receipt method. Emit existing ancestor rows as unchanged import
  context for child operations. Evidence: `SRC-FSM-PACKAGE`,
  `SRC-CODE-FSM-REGISTRATION`, `SRC-CODE-RECEIPT-CLASS-EO`,
  `SRC-CODE-RECEIPT-METHOD-EO`, `SRC-CODE-METHOD-ACCOUNT-EO`,
  `SRC-CODE-CC-ERROR-EO`.
- Match receipt classes by exact `Name`; methods by exact parent class plus
  method `Name`; method accounts by exact parent class/method, business unit,
  bank account, currency, and start date; and card-error mappings by exact
  parent class/method, transaction category, and error code. Preserve case and
  significant characters. Evidence: `SRC-FSM-PACKAGE`,
  `SRC-CODE-RECEIPT-CLASS-EO`, `SRC-CODE-RECEIPT-METHOD-EO`,
  `SRC-CODE-METHOD-ACCOUNT-EO`, `SRC-CODE-CC-ERROR-EO`.
- Support source-backed create and exact existing-row update preparation.
  Implement method and method-account retirement as a narrow `EndDate` update.
  Physical delete, rename, and reparent remain unsupported. Evidence:
  `SRC-FSM-PACKAGE`, `SRC-HELP-RECEIPT-CLASSES-26C`, and controlled
  nonproduction regression evidence recorded in this skill.
- For every class create, require an exact name, creation method, confirmation
  behavior, remittance behavior, and clearance behavior. Require only the
  additional automatic, factoring, bills-receivable, or clearing choices made
  applicable by that design. Never infer a business meaning from an observed
  code alone. Evidence: `SRC-HELP-RECEIPT-CLASSES-26C`,
  `SRC-HELP-TASK-26B-FALLBACK`, `SRC-CODE-RECEIPT-CLASS-EO`.
- For every method create, require an exact parent class, method name,
  effective start date, and intended receipt use/payment type. Require payment
  channel, creation and maturity rules, direct-debit, funds-capture, lead-day,
  or bills-receivable choices only when applicable. Evidence:
  `SRC-HELP-RECEIPT-CLASSES-26C`, `SRC-HELP-TASK-26B-FALLBACK`,
  `SRC-CODE-RECEIPT-METHOD-EO`.
- For every remittance-account create, require one exact active target business
  unit, eligible bank account, currency, start date, primary choice, override
  behavior, and every applicable accounting, clearing, and risk value. A bank
  account name alone is not eligibility evidence. Evidence:
  `SRC-HELP-RECEIPT-CLASSES-26C`, `SRC-CODE-METHOD-ACCOUNT-EO`.
- Resolve every populated accounting display value to one exact target-native
  30-slot LF-delimited vector before ZIP creation. Never write a hyphenated
  display string directly into a `*CcidSegments` field. Evidence:
  `SRC-FSM-PACKAGE`, `SRC-CODE-METHOD-ACCOUNT-EO`, and controlled import
  regression evidence recorded in the canonical noship suite.
- For a card error mapping, require one compatible automatic credit-card
  method, transaction category, error code, primary action, and any applicable
  subsequent action and delay. Observed action codes are candidates, not
  permission to map ambiguous prose. Evidence: `SRC-FSM-PACKAGE`,
  `SRC-CODE-CC-ERROR-EO`, `SRC-HELP-RECEIPT-CLASSES-26C`.
- Ask one consolidated business-language clarification covering all unresolved
  class, method, and remittance-account choices already knowable from the
  complete request. Ambiguous or unparseable customer dates require an exact
  `YYYY-MM-DD` answer; never infer locale order. Evidence:
  `SRC-HELP-RECEIPT-CLASSES-26C`, compiled task validation rules, and canonical
  clarification regressions.
- Reject duplicate creates, missing or ambiguous update targets, orphan child
  creates, incompatible hierarchy choices, unsupported operations, and any
  mixed or bulk request containing a blocked row before package creation.
  Evidence: `SRC-FSM-PACKAGE`, task entity contracts, and canonical noship
  collision/hierarchy regressions.
- Preserve every unspecified field, sibling, child, and unrelated row during
  update, end-date, mixed, and bulk work. Omission means preserve; clearing
  requires explicit intent and field support. Evidence: `SRC-FSM-PACKAGE` and
  controlled update, end-date, mixed, and bulk reconciliation evidence
  recorded in this skill.
- Normalize every populated package date to strict `YYYY-MM-DD`, including
  requested, preserved, key, and ancestor-context dates. Accept slash-formatted
  dates only as current-export evidence and reject an end date earlier than its
  start date. Evidence: `SRC-FSM-PACKAGE` and canonical date regressions.
- Treat `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, and
  `LastUpdateLogin` as service-owned. Keep them as read-only baseline evidence
  and emit them blank in every candidate row. Evidence: `SRC-FSM-PACKAGE` and
  all four task entity implementations.
- Build only from a successful exact-task template plus compatible fresh
  current evidence. Preserve template `ASM_SETUP_CSV_METADATA.xml` byte for
  byte, ordered headers, explicit trailing blanks, and the four-object package
  hierarchy. Evidence: `SRC-FSM-PACKAGE`, `SRC-CODE-FSM-REGISTRATION`.
- Route live import only through `core.data-loader` in `FSM` mode after the
  active workflow's design confirmation and Data Loader's immutable-candidate
  approval. Verify success only through a fresh exact-task export and complete
  requirement/preservation reconciliation. Evidence: repository runtime
  contracts and `SRC-FSM-PACKAGE`.
- Treat developer fixtures, campaign policies, and test approvals as noship
  controls. They never restrict ordinary customer row counts or replace the
  source-backed behavior in this skill and its active `ora-resource` files.

## Customer interaction contract

A business-language request is sufficient. Do not ask the customer for the FSM
task code, CSV filenames, service names, database tables, IDs, or a normalized
JSON file. Examples include:

- "Create a manual receipt class with a standard remittance method."
- "Add a receipt method to our existing lockbox receipt class."
- "Assign our USD remittance bank account to the receipt method."
- "Configure how this credit-card error should be handled."
- "Update this method and prepare an offline package for review."

Normalize the request into class, method, method-account, and error-mapping
operations. Ask one consolidated question containing only unresolved material
business choices. Never answer ambiguity from test convenience, the first
exported row, a similar name, or another environment.

For every identity or reference, apply this exact contract:

| Evidence result | Behavior |
|---|---|
| One exact candidate | Use it, disclose the resolved business value and evidence, and continue. |
| No candidate | Stop and ask one business-language question; show valid target choices when authoritative evidence supplies them. |
| Multiple candidates | Show distinguishing business fields and ask the customer to choose; never choose the first or a fuzzy match. |
| Missing or stale evidence | Request or route a fresh exact-task/current reference artifact; make no write. |
| Request conflicts with evidence | Explain the conflict and ask which outcome is intended; never silently turn create into update. |

## Task and package contract

- Offering: `Financials`
- Functional area: `Customer Payments`
- Task: `Manage Receipt Classes and Methods`
- Task code: `AR_MANAGE_RECEIPT_CLASSES_AND_METHODS`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`
- Execution surface: repository CLI services only. Use
  `shared.setup-export.task-level-export` for exact-task exports and
  `core.data-loader` for validation, upload, submission, monitoring, logs, and
  diagnostics. Never use the Fusion browser/UI to create, poll, or download an
  export, or to upload, submit, poll, or verify an import.
- Import archive identity: the exact `ASM_SETUP_CSV_METADATA.xml`
  `ObjectShortName`; `businessObject` remains empty.
- Preserve `ASM_SETUP_CSV_METADATA.xml` byte-for-byte from the successful
  template-only export. Use the fresh current-data export only for state,
  duplicate, preservation, and reconciliation evidence; never substitute its
  process metadata into an import candidate.
- Treat business-object `NodeSequence` values in a successful current-data
  export as runtime ordering evidence, not a fixed schema fingerprint. Require
  positive unique values and exact object paths, headers, and types. The
  template-only export must retain the canonical parent-before-child sequence
  because its metadata is copied into the candidate.

The task package contains exactly these business objects in the metadata-owned
hierarchy and order:

| Role | CSV entity | Portable identity |
|---|---|---|
| Receipt class | `AR_RECEIPT_CLASS` | Exact `Name` (maximum 30 characters) |
| Receipt method | `AR_RECEIPT_METHOD` | Exact parent class plus method `Name` (each maximum 30 characters) |
| Remittance bank account | `AR_RECEIPT_METHOD_ACCOUNT` | Exact parent class/method, BU, bank account, currency, and effective start |
| Card error mapping | `AR_CC_ERROR_MAPPINGS` | Exact parent class/method, transaction category, and error code |

Require a successful exact task-level template for every build and a fresh
current-data export for duplicate detection, update, end-date, mixed/bulk, or
reconciliation work. Reject broader, mixed-task, failed, unsafe, mixed-release,
mixed-environment, schema-mismatched, or hand-built source packages.

Before emitting a blueprint or preview, the adapter rejects a create when the
same exact business key already exists for any of the four task business
objects. These keys preserve case and significant characters; this task does
not case-fold names or substitute a similar spelling. A child create must
resolve its immediate parent either in the fresh current export or in an
earlier parent create in the same candidate graph. Keep dependency order as
class, method, then method account or card error mapping.

For every child candidate row, emit every existing ancestor as an import-
context row in its parent CSV. Copy non-audit values exactly from the fresh
current export and blank the service-owned audit columns. Do not count these
context rows as customer-requested mutations. Independently fail validation if
an ancestor row is absent or differs from the fresh baseline. Fusion process
207394 proved that a child-only package is accepted for upload but the child is
then skipped with a parent-row-missing warning.

## Business design contract

For a new receipt class, require its exact name and creation method plus
explicit confirmation, remittance, and clearance behavior. Do not guess the
meaning of an observed enum code. `No Remittance` is only for a compatible
manual-receipt design. Automatic clearing, factoring, bills receivable, and
automatic receipt processing each require their applicable product and target
prerequisites.

For a new receipt method, require one exact parent class, method name, and
effective start date. Require payment type/channel, creation/maturity rules,
direct-debit, funds-capture, lead-day, or bills-receivable choices only when the
selected design uses them. Do not synthesize them from neighboring methods.

For a remittance bank account, require exact target-valid business unit, bank
account, currency, effective start, primary choice, override behavior, and every
applicable accounting combination. Require one applicable primary account per
currency/effective period and the required currency coverage. Never invent a
bank account, business unit, currency, ledger segment, or account combination.
Before opening the candidate ZIP, resolve every populated `*CcidSegments`
business display value to the exact target-native 30-slot LF-delimited vector
from the fresh current export. Require exactly 30 LF terminators, including the
terminal LF. A hyphenated display string must never be written directly to the
task CSV; zero or multiple native matches stop before ZIP creation.

### Enforced follow-up question contract

Before `normalize`, `build`, or any approval preview, evaluate the
entire requested hierarchy and collect every unresolved material choice. Ask
one consolidated business-language question grouped as `Receipt class`,
`Receipt method`, and `Remittance bank account`; omit a group only when the
request contains no operation at that level or all of its applicable choices
are already explicit and validated. Never ask one level per turn when the
remaining groups are already knowable.

Treat an ambiguous or unparseable customer-supplied date as an unresolved
material choice. Include it in that consolidated follow-up question, identify
the affected object and date field, and ask for an unambiguous calendar date in
`YYYY-MM-DD` form. Never infer month/day order from locale, nearby records, the
current date, or test convenience. Do not normalize, preview, confirm, or build
until the customer resolves it.

- Receipt class create: require the operation, exact class name, creation
  method, confirmation behavior, remittance behavior, and clearance behavior.
  Include automatic clearing, factoring, bills-receivable, or other
  prerequisites in the same question when the selected class design makes them
  applicable.
- Receipt method create: require the operation, exact parent class, exact
  method name, effective start date, and intended receipt use/payment type.
  In the same question, ask only the applicable payment channel,
  creation/maturity rules, direct-debit, funds-capture, lead-day, or
  bills-receivable choices revealed by that intended use.
- Remittance bank-account create: require the operation, exact parent class and
  method, target-valid active BU, eligible bank/branch/account, supported
  currency, effective start, primary choice, override behavior, and every
  applicable accounting, clearing, and risk value. A supplied bank-account
  name is not eligibility evidence by itself.

For updates, ask only for the exact complete target key and explicit changed
fields; omitted values remain preserved. When authoritative lookup evidence
contains multiple eligible values, show all distinguishing business fields in
the consolidated question. When no executable cross-task resolver or target
evidence exists, ask for that evidence instead of presenting an export-derived
or first-match option list.

The adapter's contract-driven clarification preflight is a fail-closed backstop:
an incomplete create raises `FOLLOW_UP_REQUIRED` with all affected groups and
must produce no blueprint, candidate, or approval prompt. Do not bypass or
waive this result as a convenience default.

For a card error mapping, require one compatible automatic credit-card method,
transaction category, error code, primary recovery action, and any applicable
subsequent action and delay. Observed action codes are evidence candidates, not
permission to map ambiguous prose.

## Operation and preservation contract

| Request | Static handling | Live readiness |
|---|---|---|
| Create class/method/account/error mapping | Normalize, validate, preview, and deterministically prepare only after all parents and prerequisites resolve. | Requires controlled nonproduction import evidence. |
| Update | Patch exactly one fresh-export baseline row and preserve every unspecified field, sibling, and child. | Ready only for exact single-row updates under the controlled import, zero-warning, and fresh-export reconciliation gates below. |
| End-date | Require one exact method or method-account target and an end date on or after its start date; implement it as a narrow baseline-preserving update to `EndDate`. | Ready as an exact update under the controlled import, zero-warning, and fresh-export reconciliation gates below. |
| Mixed or bulk | Validate all operations and hierarchy keys as one all-or-nothing design; never drop a blocked row. | Create and update operations may share one candidate across any number of receipt classes and parent branches. The adapter imposes no operation-count or shared-parent limit; actual Fusion ZIP/service limits and the normal validation gates still apply. |
| Hard delete, rename, or reparent | Do not generate a candidate. | Unsupported. |

## Single-go business flow contract

When one request contains multiple test scenarios or asks to run everything in
one go, produce one consolidated design and one consolidated clarification
question. Do not turn each scenario or package into a separate business-design
conversation.

This task skill is self-contained and must not depend on a developer-only E2E
harness. Normalize the consolidated design before candidate generation and
bind its `businessDesignSha256` to the reviewed business design. Plan the
fewest ordered phases required by real lifecycle
dependencies, then execute them without another business-design conversation.

Combine all valid create and update operations into one candidate regardless
of operation count, entity mix, or parent-class grouping. Split only when the
requested lifecycle cannot be represented unambiguously in one package, such
as creating and then updating the same exact target, or when Fusion reports an
actual package/service limit. Keep expected-rejection scenarios offline with
no candidate. Continue with unrelated ready phases after a failed phase while
leaving the failed scenario `In Progress` with its process and recovery
evidence. Do not ask for another design decision unless fresh target evidence
invalidates a confirmed business value.

Run only one live mutation at a time. After each successful phase, reuse its
fresh reconciliation export as the next phase's current baseline. Reuse a
validated template while the task, target environment, release, schema
fingerprint, headers, and member inventory remain identical. Re-run local
build, validation, and determinism only when their complete input hashes
change. Static negative cases and other independent offline checks may run
while Fusion processes are being monitored, but live mutations must remain
serialized.

Omitted means preserve. Blank means clear only when the customer explicitly
requests it and the exact field/operation contract supports clearing. Preserve
the current hierarchy during updates; omission is never deletion.

Normalize every populated `date` field to `YYYY-MM-DD` before candidate ZIP
creation, including requested values, preserved update values, business-key
dates, and baseline ancestor-context dates. Accept `YYYY/MM/DD` only as a
source-export representation and convert it. For customer-supplied ambiguous
or unparseable dates, stop and ask the consolidated follow-up question required
above; reject the value before opening the output archive. Independent
candidate validation must reject any populated date that is not already in
canonical `YYYY-MM-DD` form.

Treat `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, and
`LastUpdateLogin` as service-owned. Retain them in read-only baseline evidence
and emit them blank in generated candidate rows. Do not ask for or copy
generated IDs, object versions, request IDs, onboarding IDs, or opaque keys as
portable business input unless the exact template requires an established
parent reference.

## Preview and confirmation contract

Before generating the first candidate ZIP, show one complete normalized flow
preview:

- task, target environment/release evidence, and requested operation count;
- every class, method, account, and error-mapping hierarchy key;
- dates, processing choices, payment/channel choices, bank/currency/BU and
  applicable accounting references;
- exact create/update/end-date intent, before/after values, preserved state,
  defaults, prerequisites, warnings, and row counts; and
- phase grouping, template/current evidence hashes, the stable business-design
  SHA-256, and the evidence-bound phase design SHA-256 values.

Obtain the design confirmation required by the active implementation workflow,
bound to the target environment, task, and stable business-design SHA-256. A
changed requested operation, target key,
business value, default, preservation instruction, environment, task, release,
or incompatible schema invalidates confirmation. A refreshed current export,
new process ID, changed source/evidence hash, or regenerated candidate does not
invalidate business-design confirmation when the stable business-design hash
is unchanged; it still requires the normal phase validation and immutable-
candidate approval checks. Design confirmation never authorizes a Fusion
import. Core Data Loader remains the sole owner of any mandatory live import
approval.

## Routed workflow

1. Enter through `router/implementation-router/SKILL.md`, then the Customer
   Payments skill, and select this exact task by catalog metadata.
2. Normalize the unchanged business prompt and apply the six task resources
   plus the compiled rule plan in the read order below.
3. Obtain/validate the exact task template and fresh current data only through
   the repository CLI route owned by `shared.setup-export.task-level-export`
   when they were not supplied. Do not substitute a browser/UI export flow.
4. Run shared setup/reference validation and the task adapter's `manifest` and
   semantic checks. Cross-task references require target-valid evidence.
5. Normalize the complete consolidated design, produce its preview, and obtain
   the design confirmation required by the active implementation workflow.
6. Build each ready phase from the genuine template and then-current export,
   independently validate the candidate, rebuild to prove identical SHA-256,
   and report it as locally validated only.
7. For live work, hand the exact immutable candidate to `core.data-loader`
   through its repository CLI workflow only.
   Core Data Loader owns the final preview and approval, the supported FSM
   adapter, upload, one-time submission, process monitoring, logs, and
   diagnostics. Never use a direct REST write, SQL, or a task-local importer.
8. After each successful terminal process, obtain a fresh exact-task export,
   run `reconcile` against every confirmed phase requirement, and use that
   verified export as the next phase baseline. Continue automatically through
   every unblocked phase. Completion requires zero unresolved mismatches;
   submission or process initiation is not success.

## Portable task adapter

The generated task adapter is standard-library Python and uses repository-
relative files. Discover the repository root and Python runtime at execution;
do not hardcode a laptop path, browser profile, environment, credential, or
token. Its commands are:

| Command | Purpose |
|---|---|
| `manifest` | Normalize and fingerprint an exact task template/current export. |
| `normalize` | Convert the unchanged prompt plus agent-resolved design into blueprint, preview, and stable requirements. |
| `build` | Apply the confirmed complete blueprint to the genuine template/current evidence, add baseline-preserving ancestor context rows for every child, canonicalize all populated dates before opening the ZIP, and emit a candidate handoff. |
| `validate` | Independently compare task/schema, blueprint, baseline, candidate, audit fields, keys, hierarchy, required ancestor context, requirements, and canonical candidate date serialization. |
| `determinism` | Rebuild from identical inputs and require identical SHA-256. |
| `rollback` | Build only a narrow evidence-backed update reversal; this does not authorize live rollback. |
| `reconcile` | Compare each requirement and preservation assertion with a fresh post-process export. Treat source-equivalent date/numeric formatting as equal. For creates, require unrequested candidate fields to remain unset while allowing Fusion-owned persisted defaults; for updates, require non-requested values to match the baseline. |

The adapter's generated-generic normalizer accepts only an explicit
schema-constrained design produced after this skill's business rules run. It is
not a substitute for business clarification or cross-task reference
resolution. It independently enforces task-owned create collisions and the
descriptor-declared parent graph before writing a blueprint or preview. A valid
ZIP structure does not make an unresolved design safe.

## Completion and failure contract

Keep these states separate: locally generated, locally validated, approved,
submitted, process-completed, and persisted-state verified. Mark the setup
verified only when submitted bytes match the approved SHA-256, the process
completes successfully with zero failed rows and no unresolved warnings, logs
and diagnostics are retained, and fresh-export reconciliation passes every
requirement and preservation assertion.

Never retry or resubmit automatically after rejection, timeout, unknown result,
or failed processing. Preserve the failed candidate and evidence, obtain a
fresh current export to detect partial persistence, repair the owning layer,
add a regression test, then create a new candidate requiring a new design
confirmation and a new candidate-bound Data Loader approval.

## Controlled runtime evidence

Runtime evidence is an authoring qualification, never a target-environment
default or a substitute for the current run's validation and approvals:

- parent and child create paths completed successfully in controlled
  nonproduction runs, including fresh-export reconciliation of the complete
  class/method hierarchy; and
- an exact single-class update completed as process `207503` and reconciled
  from fresh export `207508`, proving baseline preservation, blank generated
  audit columns, and persisted-state verification for that guarded path; and
- an exact receipt-method end-date completed as process `207556` and
  reconciled from fresh export `207559`, proving the lifecycle date rule,
  unchanged parent context, and preservation of all other method values; and
- an atomic receipt-class create plus exact receipt-class update completed as
  process `207601` and reconciled from fresh export `207603`, proving that both
  operations persist together without silent row loss or unrelated changes;
  and
- a homogeneous ten-class create completed as process `207629` and reconciled
  from fresh export `207639`, proving all 90 requirements and all ten requested
  rows persisted with zero warnings, failures, or unrelated changes; and
- a homogeneous three-method create under one exact existing class completed
  as process `207658` and reconciled from fresh export `207659`, proving one
  preserved parent context row, all three child rows, and all 18 requirements.

These runs are regression evidence, not adapter-imposed batch qualifications.
The adapter does not cap operation counts, require methods to share a parent,
or restrict valid mixes of create and update operations. It validates the
complete graph atomically and emits one candidate whenever every key, parent,
reference, field, and preservation rule succeeds. Split only for a genuine
same-target lifecycle conflict or an actual Fusion ZIP/service constraint.
Every live run must still use fresh target evidence and satisfy the normal
preview, design-confirmation, candidate-approval, process, diagnostic, and
reconciliation gates.

## Current Oracle documentation

Use the newest documentation matching the target release. This authoring
baseline used:

- [Implementing Receivables Credit to Cash 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/fairp/implementing-receivables-credit-to-cash.pdf)
- [Manage Receipt Classes and Methods task guidance](https://docs.oracle.com/en/cloud/saas/financials/26b/faufa/manage-receipt-classes-and-methods.html)
- [Automatic Clearing of Receipts](https://docs.oracle.com/en/cloud/saas/financials/26c/faofc/automatic-clearing-of-receipts.html)
- [Considerations for Remitting Receipts](https://docs.oracle.com/en/cloud/saas/financials/26c/faofc/considerations-for-remitting-receipts.html)
- [Export and Import of CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/export-and-import-of-csv-file-packages.html)

## Registered implementation evidence

The reviewed implementation establishes this ownership chain:

`AR_MANAGE_RECEIPT_CLASSES_AND_METHODS` -> `ReceiptClassManageFlow` ->
receipt-class create/manage pages -> receipt-class application modules and view
objects -> `ReceiptClassEO`, `ReceiptMethodEO`, `ReceiptMethodAccountEO`, and
`CreditCardErrorMappingEO` -> the corresponding `AR_RECEIPT_*` and
`AR_CC_ERROR_MAPPINGS` tables.

The FSM registration maps the exact four business objects listed above. This
evidence is authoring provenance, not a runtime dependency and not permission
to write database tables.

## Resource read order

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
3. [Reference lookups](ora-resource/ora_reference_lookups.md)
4. [Defaulting rules](ora-resource/ora_defaulting_rules.md)
5. [Design enforcement](ora-resource/ora_design_enforcement.md)
6. [Error handling](ora-resource/ora_error_handling.md)
7. Generated [rule registry](ora-resource/ora_rule_registry.json)
8. Generated [E2E adapter](e2e-adapter.json). Developer-only catalogs and
   regression fixtures are discovered from the task's functional-area
   `noship/tests` bundle and are never required by the customer skill.

## Refusal rules

- Do not invent or default a class/method behavior, bank account, BU, currency,
  payment system/channel, accounting combination, recovery action, flexfield,
  date, task package member, or enum mapping.
- Do not transform a create collision into update or choose among zero/multiple
  matches without the customer's business decision.
- Do not build a partial mixed/bulk package, silently drop a row, or mutate an
  unrelated hierarchy.
- Do not build from a stale, failed, wrong-task, broader-scope, mixed-pod,
  mixed-release, unsafe, schema-mismatched, or hand-edited template.
- Do not hand off populated service-owned audit columns or unsupported IDs.
- Do not treat update as replacement or omission as child deletion.
- Do not hard-delete, rename, or reparent through this generic CSV workflow.
- Do not treat design confirmation as import approval or reuse either gate
  after a bound input changes.
- Do not use direct REST, SQL, browser/UI export or import actions, UI data
  entry automation, or database-table updates as substitutes for the governed
  repository CLI task CSV and Core Data Loader routes.
- Do not claim success from candidate creation, upload acceptance, request ID,
  or process completion without fresh-export reconciliation.

## Portability

Resolve repository, project, target environment, release, exports, references,
process IDs, and current CodeSearch series at runtime. Recorded source sandbox,
absolute paths, credentials, request IDs, and source revisions are provenance
only. No generated skill/runtime file depends on this laptop or stores
provided credentials.
