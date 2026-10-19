# Manage Receipt Sources Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact task artifacts | Validate the genuine task template and fresh current export where state evidence is required. |
| 2 | Receivables business unit | Resolve one exact BUName from the single-BU exact-task export when its scope and populated rows agree; otherwise use the documented live LOV. |
| 3 | Existing receipt source | Require zero exact BUName plus Name matches for create and exactly one for update, end-date, or verify. |
| 4 | Receipt class and method | Resolve one exact method/class relationship when referenced or required by lockbox use. |
| 5 | Bank account and compatibility | Resolve the exact BU-associated account and prove its method/date compatibility when a bank is referenced. |
| 6 | DFF deployment | Resolve context and segment mapping only when the customer requests DFF values. |
| 7 | Runtime route | Keep import behind Run Book and Core Data Loader preview and approval gates. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RS.DEP.PACKAGE | Exact task template and current evidence | Yes | Every build; current export additionally for state-sensitive work | Local lookup | Supplied task ZIPs | inspect_receipt_source_package | Prevents cross-task, stale, malformed, or incompatible packages. | Supply successful exact-task exports from the target. | Task, environment, release, members, headers, row counts, hashes |
| RS.DEP.BU | Receivables business unit | Yes | Every operation | Local lookup, then live fallback | Fresh exact-task scope and populated `AR_RECEIPT_SOURCE` rows; Receivables Business Units LOV only when local evidence is insufficient | resolve_receivables_business_unit | BUName owns the receipt source and is part of its portable key. A single numeric organization scope plus unanimous populated BU rows is stronger task-specific evidence than an empty security-filtered LOV. | Provide the exact target business-unit name and a correctly scoped export; use the LOV fallback only when the export cannot prove the relationship. | BUName and scope identifier evidence; BusinessUnitId evidence when the LOV fallback is used |
| RS.DEP.TARGET | Existing receipt source | Yes | Create collision check, update, end-date, verify, mixed/bulk, or reconciliation | Local lookup | Fresh current task export | find_receipt_source_exact | Create requires zero matches; update, end-date, and verify require exactly one baseline row. | Provide exact BU and source name or refresh the current export. | Baseline row or zero-match proof |
| RS.DEP.METHOD | Receipt method and class | Conditional | Method/class is supplied or lockbox is intended | Live lookup | Receipt Methods REST resource | resolve_receipt_method_class | The method must belong to the selected class. | Provide an exact method or class when multiple matches remain. | ReceiptMethodName and ReceiptClassName |
| RS.DEP.BANK | Bank account existence and BU association | Conditional | BankAccountName is supplied | Live lookup | Cash Bank Accounts LOV | resolve_bank_account_business_unit | Bank accounts are target-specific references. | Provide the exact bank account and BU. | BankAccountName and association evidence |
| RS.DEP.COMPAT | Bank-method-date compatibility | Conditional | BankAccountName is supplied | Needs input until proven | Exact target receipt-method bank assignment evidence |  | Bank existence alone does not prove the receipt source combination is valid. | Ask for approved target evidence for method, BU, bank account, and effective dates; resume after it is supplied. | Compatibility decision |
| RS.DEP.DFF | Batch Source DFF context and segment map | Conditional | Any DFF value is requested | Needs input until proven | Target DFF deployment metadata |  | Generic storage does not identify deployed context or segment mapping. | Ask for the context, segment names, and target metadata; resume after it is supplied. | AttributeCategory and exact AttributeN values |
| RS.DEP.RUNTIME | Controlled FSM import route | Yes | Any live execution | Awaiting governed approval | Run Book and Core Data Loader |  | The task skill prepares and validates; it does not write Fusion directly. | Present the complete preview and request the current confirmation/approval at its governed gate. | Candidate hash, approval, process and verification evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every applicable dependency is exact, current, and target-valid. | Yes for documented read-only lookups; create remains approval-gated. |
| Needs business input | A material choice is missing or ambiguous. | Ask one consolidated question. |
| Needs target evidence | A BU, method/class, bank compatibility, or DFF mapping is unproven. | Run the documented read-only lookup; otherwise ask for the exact evidence and resume when supplied. |
| Needs operation alternative | The exact requested mutation lacks an evidenced CSV implementation. | Ask whether end-date, replacement create, verify, or the named separate product workflow meets the intent. |
| Unsafe external condition | Credentials, package safety, environment classification, or a product service prevents safe continuation. | Explain the concrete recovery action; retain the design and resume after the condition is corrected. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.DEPENDENCIES | decision | 20 | resolve_dependency | ready->RS.LOOKUP_PACKAGE;needs_input->RS.NEEDS_INPUT;unsafe->RS.SAFETY_HOLD | RS.VALIDATE | stop | Input validation completed for a Manage Receipt Sources request. |
