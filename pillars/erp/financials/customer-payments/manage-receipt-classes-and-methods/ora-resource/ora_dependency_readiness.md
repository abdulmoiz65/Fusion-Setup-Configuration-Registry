# Manage Receipt Classes and Methods Dependency Readiness

## Required dependency order

| Sequence | Dependency | Requirement |
|---|---|---|
| 1 | Exact task artifacts | Validate a successful task-level template; require a fresh current export for duplicate detection, update, end-date, mixed, or reconciliation work. Reuse a successful reconciliation export as the next ordered phase's current baseline. |
| 2 | Receipt class hierarchy | Resolve every child to exactly one receipt class and every account or card-error mapping to exactly one receipt method. |
| 3 | Processing prerequisites | Prove the payment channel, funds-capture behavior, automatic-receipt prerequisites, or bills-receivable prerequisites selected by the design. |
| 4 | Remittance bank account | Resolve target-valid business unit, bank, branch, bank account, currency, effective dates, and required accounting combinations. |
| 5 | Runtime route | Keep import behind the shared Run Book or Data Loader preview, confirmation, approval, process-monitoring, and reconciliation gates. |

## Dependency rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RCM.DEP.PACKAGE | Exact task template and current evidence | Yes | Every candidate; current export additionally for state-sensitive operations | Local lookup | Supplied task ZIPs | inspect_receipt_setup_package | Prevents cross-task, cross-release, stale, and malformed packages. | Supply the exact successful task exports from the target environment. | Environment, release, task code, process status, member inventory, hashes |
| RCM.DEP.CLASS | Receipt class | Yes | Every receipt method, account, or error mapping | Local lookup | Candidate hierarchy and fresh current export | find_receipt_class_exact | Child rows cannot exist without one exact parent class. | Provide the exact class name or include its create operation in the same request. | Receipt class identity and processing design |
| RCM.DEP.METHOD | Receipt method | Yes | Every method account or error mapping | Local lookup | Candidate hierarchy and fresh current export | find_receipt_method_exact | Account and card-error rows require one exact parent method. | Provide the exact method name and parent class. | Receipt method identity and effective design |
| RCM.DEP.AUTOMATIC | Automatic receipt prerequisites | Conditional | Automatic creation or automatic payment processing | Verify | Target-valid setup evidence |  | Automatic processing depends on compatible payment channel, payment system/profile, and remittance setup. | Provide or export the target-valid prerequisite setup; do not infer it from an existing unrelated method. | Payment type, payment channel, automatic rules, funds-capture prerequisites |
| RCM.DEP.BANK | Remittance bank account | Conditional | A receipt method is assigned remittance accounts | Verify | Target-valid bank and BU evidence |  | Bank accounts and business units are environment-specific references. | Supply exact BU, bank account, currency, dates, and applicable accounting combinations. | BuName, BankName, BankBranchName, BankAccountName, CurrencyCode, StartDate, GL accounts |
| RCM.DEP.ACCOUNTING | Valid accounting combinations | Conditional | The class/method behavior requires cash, remittance, clearing, factoring, or risk accounts | Verify | Approved target accounting evidence |  | Invalid combinations cause import or downstream accounting failure. | Provide approved combinations; never generate or copy unrelated account segments. | Applicable account segment columns |
| RCM.DEP.RUNTIME | Controlled FSM import route | Yes | Any live execution | Blocked until approved | Shared Run Book or core Data Loader |  | The task skill prepares and validates data; it does not directly write Fusion or database tables. | Complete design confirmation and separate import approval in the controlled execution flow. | Candidate SHA-256, approval, process ID, logs, verification export |

## Dependency outcomes

| Outcome | Meaning | Next action |
|---|---|---|
| Ready | Every applicable dependency is exact, current, and target-valid. | Continue to package and hierarchy lookups. |
| Needs business input | A required business choice is absent or ambiguous. | Ask one consolidated business-language question. |
| Needs target evidence | A referenced BU, bank account, account combination, payment system, or channel has not been proven. | Stop and request the smallest authoritative target artifact. |
| Blocked | Task evidence is invalid, a parent cannot be resolved, the operation is unsupported, or runtime approval is absent. | Do not generate or import a ZIP. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCM.DEPENDENCIES | decision | 20 | resolve_dependency | ready->RCM.LOOKUP_PACKAGE;blocked->RCM.BLOCKED | RCM.VALIDATE | stop | Input validation has completed for a Manage Receipt Classes and Methods request. |
