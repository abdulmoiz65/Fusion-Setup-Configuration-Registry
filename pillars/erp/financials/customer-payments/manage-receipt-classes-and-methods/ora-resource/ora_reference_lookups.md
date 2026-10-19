# Manage Receipt Classes and Methods Reference Lookups

## Authority boundary

The supplied current task export is authoritative only for the four task-owned business objects and for its recorded environment and release. Cross-task references such as business units, bank accounts, payment systems, payment channels, currencies, and account combinations require separate target-valid evidence. A first match, similar name, database row, or unrelated existing setup is never an allowed substitute.

## Local Lookups

| Rule ID | Resolver | Runs When | Source Values | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| RCM.LOOKUP_PACKAGE | inspect_receipt_setup_package | Before every build or reconciliation | Template and current ZIP paths | Environment, release, task code, process status, metadata, members, headers, row counts, hashes | Exactly one completed AR_MANAGE_RECEIPT_CLASSES_AND_METHODS task; only the four registered CSVs; compatible template/current metadata | Validated package contract | Stop; report every violated package rule. |
| RCM.LOOKUP_CLASS | find_receipt_class_exact | Class collision check or child-parent resolution | Receipt class Name | Class row and immutable identity evidence | Exact Name match after preserving significant characters; no fuzzy, contains, or case-folded substitution | Exact baseline class or zero-match proof | Zero blocks child/update operations; one blocks create as a duplicate; many is corrupt or ambiguous and blocks. |
| RCM.LOOKUP_METHOD | find_receipt_method_exact | Method collision check or account/error parent resolution | Parent class Name and method Name | Method row plus effective dates and parent evidence | Exact class hierarchy and method Name | Exact baseline method or zero-match proof | Zero blocks child/update operations; one blocks create as a duplicate; many blocks. |
| RCM.LOOKUP_ACCOUNT | find_method_account_exact | Method-account create/update/end-date | Parent class, method, BuName, BankAccountName, CurrencyCode, StartDate | Full account row and sibling account evidence | Exact hierarchy plus all supplied business-key values | Exact baseline account or zero-match proof | Ask for missing key values; zero blocks update; one blocks create as duplicate; many blocks. |
| RCM.LOOKUP_ERROR | find_cc_error_mapping_exact | Card-error mapping create/update | Parent class, method, CcTrxCategory, CcErrorCode | Full mapping row and parent evidence | Exact hierarchy, category, and error code | Exact mapping or zero-match proof | Zero blocks update; one blocks create as duplicate; many blocks. |

## Cross-task reference rules

| Reference | Accepted evidence | Match rule | Failure handling |
|---|---|---|---|
| Business unit | Target export, approved setup artifact, or controlled read-only resolver with environment identity | One exact active business unit name | Stop and ask for the exact target-valid BU. |
| Bank, branch, and bank account | Target bank-account evidence including ownership, currency, and effective status | One exact applicable bank account | Stop; never use the first account or copy an unrelated account ID. |
| Currency | Target-supported ISO code or explicit ANY where the selected design supports it | One exact code | Stop on blank, unsupported, or ambiguous values. |
| Accounting combinations | Approved target chart/ledger validation evidence | One valid combination for each applicable account role | Stop before preview; do not synthesize segments. |
| Payment channel and payment system | Target payment setup evidence compatible with the method design | One exact active compatible reference | Stop and request evidence; observed CSV codes are candidates only. |

## Lookup execution rules

| Situation | Required behavior |
|---|---|
| No current export for create | Creation may proceed only after the user supplies a fresh export for duplicate proof; do not assume the name is unused. |
| Multiple matches | Show the distinguishing business fields and ask one consolidated question; never choose automatically. |
| Business label maps to multiple observed codes | Ask for the exact business behavior rather than exposing an arbitrary code. |
| Parent is created in the same request | Resolve against an earlier parent create in the normalized candidate dependency order, then verify no baseline collision. |
| Lookup evidence has a different environment or release | Reject it for target resolution. |
| Read-only lookup fails | Stop before preview; do not fall through to database writes, direct REST writes, or guessed values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCM.LOOKUP_PACKAGE | decision | 30 | evaluate_result | resolved->RCM.LOOKUP_CLASS;unresolved->RCM.BLOCKED | RCM.DEPENDENCIES | stop | Every request. |
| RCM.LOOKUP_CLASS | decision | 31 | evaluate_result | resolved->RCM.LOOKUP_METHOD;unresolved->RCM.BLOCKED | RCM.LOOKUP_PACKAGE | stop | Every class create/update or child operation; no-op pass when class resolution is not needed. |
| RCM.LOOKUP_METHOD | decision | 32 | evaluate_result | resolved->RCM.LOOKUP_ACCOUNT;unresolved->RCM.BLOCKED | RCM.LOOKUP_CLASS | stop | Every method create/update or account/error operation; no-op pass when method resolution is not needed. |
| RCM.LOOKUP_ACCOUNT | decision | 33 | evaluate_result | resolved->RCM.LOOKUP_ERROR;unresolved->RCM.BLOCKED | RCM.LOOKUP_METHOD | stop | Every method-account operation; no-op pass otherwise. |
| RCM.LOOKUP_ERROR | decision | 34 | evaluate_result | resolved->RCM.DEFAULTS;unresolved->RCM.BLOCKED | RCM.LOOKUP_ACCOUNT | stop | Every card-error mapping operation; no-op pass otherwise. |
