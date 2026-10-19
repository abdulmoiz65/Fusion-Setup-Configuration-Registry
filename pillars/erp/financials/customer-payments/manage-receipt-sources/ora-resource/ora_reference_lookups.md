# Manage Receipt Sources Reference Lookups

## Authority boundary

The current task export is authoritative only for task-owned receipt-source rows in its recorded environment and release. Business units, receipt methods/classes, bank accounts, bank-method compatibility, and DFF deployment require the exact documented resolver or target evidence below. Never choose the first, most frequent, fuzzy, or cross-environment value.

## Local Lookups

| Rule ID | Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|
| RS.LOOKUP_PACKAGE | inspect_receipt_source_package | Before every build, validation, or reconciliation | Template and current ZIPs | Exactly one completed AR_MANAGE_RECEIPT_SOURCES task per ZIP; exact metadata, node, CSV header, environment, and release compatibility; the fresh current ZIP has exactly one FUN_BUSINESS_UNIT / ORGANIZATION_ID scope row. The scope is a match when its displayed value equals every requested BUName, or when it is numeric and every populated AR_RECEIPT_SOURCE row independently has the same exact requested BUName. | Validated package contract, exact Business Unit scope, template-owned CSV envelope, current-owned metadata envelope, and hashes | Report every violated package rule, obtain or request a fresh scoped export for missing/multiple/mismatched scope or conflicting populated BU rows, split cross-Business-Unit requests, and resume validation. |
| RS.LOOKUP_TARGET | find_receipt_source_exact | Create collision, update, end-date, verify, mixed/bulk, or reconciliation | BUName and Name plus fresh AR_RECEIPT_SOURCE.csv | Exact trimmed BUName and exact case-preserving Name; no fuzzy or partial substitution | Baseline row or zero-match proof | Zero is valid only for create; one is valid for update, end-date, or verify and blocks create; zero/multiple for a mutation triggers a focused target clarification and no ZIP. |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| RS.LOOKUP_BU | resolve_receivables_business_unit | Every operation after BUName is supplied and the exact-task package does not already prove the BU scope | BUName | /fscmRestApi/resources/11.13.18.05/receivablesBusinessUnitsLOV | BusinessUnitId, BusinessUnitName | Exactly one returned item whose trimmed BusinessUnitName equals BUName | Exact BusinessUnitName to BUName; retain BusinessUnitId as evidence only | Ask for the exact target-valid business unit, show authoritative candidates when available, and retry. An empty security-filtered LOV does not invalidate a BU already proven by the exact-task scope plus unanimous populated BU rows. |
| RS.LOOKUP_METHOD | resolve_receipt_method_class | ReceiptMethodName or ReceiptClassName is supplied, or lockbox is intended | ReceiptMethodName and optional ReceiptClassName | /fscmRestApi/resources/11.13.18.05/receiptMethods | ReceiptMethodName, ReceiptClassName, applicable effective fields returned by the resource | Exactly one method match and, when supplied, exact owning class match | ReceiptMethodName and ReceiptClassName | Ask for the missing or distinguishing method/class value, show authoritative candidates when available, and retry. |
| RS.LOOKUP_BANK | resolve_bank_account_business_unit | BankAccountName is supplied | BankAccountName and BUName | /fscmRestApi/resources/11.13.18.05/cashBankAccountsLOV | BankAccountName and returned ownership/business-unit evidence | Exactly one exact bank-account result associated with the requested BU | Exact BankAccountName and BU association evidence | Ask for the distinguishing bank-account evidence and retry; never choose by name alone or the first match. |

## Unsupported conditional resolver boundaries

- Receipt-source bank compatibility: no supported resolver is registered for the complete receipt-method plus business-unit plus bank-account plus effective-date contract. When a bank account is requested, ask for exact approved target assignment evidence and resume after it is supplied. The documented bank-account lookup proves existence and BU association only.
- Batch Source DFF mapping: generic DFF storage is documented, but no portable resolver is registered for a target environment's deployed context, segment-to-Attribute mapping, and value sets. When DFF values are requested, ask for exact target DFF metadata and resume after it is supplied.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| No fresh current export | Do not assume a create name is unused or that a requested verification target exists. |
| Fresh export is unscoped, has multiple Business Unit scopes, or differs from requested BUName | Obtain or request a fresh exact-task export scoped to the requested Business Unit, then resume. |
| Operations span more than one Business Unit | Split them into separately scoped designs and packages; never combine them under one metadata scope. |
| Multiple exact matches | Show distinguishing business fields and ask one consolidated question. |
| Resolver evidence belongs to another environment or release | Reject it for target resolution. |
| Read-only lookup fails | Explain the failed lookup, ask for the exact value/evidence or retry when available; do not fall through to direct writes, SQL, or guesses. |
| Bank or DFF conditional resolver is incomplete | Ask for the exact missing evidence and resume after it is supplied; do not invent an executable lookup. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RS.LOOKUP_PACKAGE | decision | 30 | evaluate_result | resolved->RS.LOOKUP_BU;needs_input->RS.NEEDS_INPUT;unsafe->RS.SAFETY_HOLD | RS.DEPENDENCIES | stop | Every request. |
| RS.LOOKUP_BU | decision | 31 | reference_lookup | resolved->RS.LOOKUP_TARGET;needs_input->RS.NEEDS_INPUT | RS.LOOKUP_PACKAGE | stop | Every operation; use exact-task package evidence first and the documented live LOV only as a fallback. |
| RS.LOOKUP_TARGET | decision | 32 | evaluate_result | resolved->RS.LOOKUP_METHOD;needs_input->RS.NEEDS_INPUT | RS.LOOKUP_BU | stop | Every request; create requires zero matches while update, end-date, and verify require exactly one. |
| RS.LOOKUP_METHOD | decision | 33 | reference_lookup | resolved->RS.LOOKUP_BANK;needs_input->RS.NEEDS_INPUT | RS.LOOKUP_TARGET | stop | Method/class reference or lockbox design; otherwise explicit no-op pass. |
| RS.LOOKUP_BANK | decision | 34 | reference_lookup | resolved->RS.DEFAULTS;needs_input->RS.NEEDS_INPUT | RS.LOOKUP_METHOD | stop | Bank-account reference; otherwise explicit no-op pass. |
