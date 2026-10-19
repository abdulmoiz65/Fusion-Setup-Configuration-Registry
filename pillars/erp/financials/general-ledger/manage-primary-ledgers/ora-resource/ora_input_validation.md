# Manage Primary Ledgers Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Primary ledger identity | Name | Block before lookup or package preview and request the primary-ledger name | The user supplies the exact intended name; it is not generated or copied from another ledger | Always |  |
| Core accounting dimensions | ChartOfAccountsName, AccountingCalendarName, CurrencyCode | Block and request every missing business choice | The user selects the chart of accounts, accounting calendar, and ledger currency; none is guessed | Always |  |
| Physical ledger period | FirstLedgerPeriodName for the create shell, distinct from any later options-task opening-period handoff | Block before template export and request the exact physical period unless independently authoritative same-role export evidence already supplies it | Validate the value against one EnteredPeriodName in the fully paged PeriodSetNameId result after local PeriodType filtering; never select from response order | Always | list_eligible_accounting_periods |
| Accounting method policy | Optional AccountingMethodName as a desired-state receipt; physical method fields are not user intake | Never block creation because the method was omitted. Author Standard Accrual as STANDARD_ACCRUAL, type S, and blank language | When AccountingMethodName is omitted or names Standard Accrual, apply the controlled tuple. When it names another method, preserve that exact requested name only for a post-create Specify Ledger Options UI handoff while still creating the ledger with Standard Accrual | Always | resolve_accounting_method_evidence |

## User Intake Classification

| Business Input | Intake Class | Applies When | Contract |
|---|---|---|---|
| Name | Definitely mandatory user input | Always | Exact intended primary-ledger name, maximum 30 characters, unique across the broader ledger namespace |
| Chart of accounts | Definitely mandatory user input | Always | Exact existing chart-of-accounts name selected by the user |
| Accounting calendar | Definitely mandatory user input | Always | Exact existing ACCOUNTING calendar selected by UserPeriodSetName; the LOV exposes no EnabledFlag |
| Currency | Definitely mandatory user input | Always | Exact existing active monetary currency selected by the user |
| Description | Optional user input | User wants a description | Maximum 240 characters; blank is intentional when omitted |
| Accounting method | Controlled default with optional desired-state input | Always for a new FSCR-authored primary ledger | User input is not required. FSCR authors Standard Accrual as STANDARD_ACCRUAL, S, and blank language. A different explicit AccountingMethodName becomes a post-create manual-change handoff and never changes the create tuple |
| Physical FirstLedgerPeriodName | Exact explicit create input or independently authoritative same-role export evidence | New primary-ledger shell requires its physical period identity | Validate the exact value against EnteredPeriodName within the resolved PeriodSetName and PeriodType. The LOV response order and label sorting cannot derive it; separately hand the complete eligible set to Specify Ledger Options for any user opening decision |
| Downstream First Opened Period | Not intake for this task | A user supplies a period for primary or secondary Specify Ledger Options in the same lifecycle | Preserve it only for the owning options-task handoff. Never copy, substitute, or leak that user-selected period into the Manage Primary Ledgers physical FirstLedgerPeriodName field |
| Retained earnings account | Dependent-task receipt, not intake for this task | The ledger request also supplies a retained-earnings account | Preserve the exact user statement outside the CSV package for the primary-ledger Specify Ledger Options handoff. Do not resolve the account, create a combination, or populate RetEarnCcidSegments during Manage Primary Ledgers |
| Other ledger-option families | Dependent-task receipt, not intake for this task | Any optional option family is requested | Preserve the requested business choice for Specify Ledger Options in the primary-ledger context; do not collect or author its physical fields here |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A package candidate is supplied or acquired | Continue only when the artifact matches the selected environment, release, task code, scope, required members, headers, aliases, and metadata | Validate the package before deriving or editing rows | select_validated_general_ledger_package |
| Name passes local shape validation | Continue only when a fully paginated ledgersLOV read returns zero exact matches | Resolve uniqueness before any CoA export or Manage Primary Ledgers template export is submitted | find_primary_ledger_name_conflict |
| Chart-of-accounts name passes local shape validation | Continue only after one exact chart of accounts identity and a current populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export for its exact StructureInstanceCode are resolved | Reuse one qualifying current export or route exactly one new populated task export. Derive the role SegmentCode from the qualified-label member, ColumnName from the structure-segment member, and instance ValueSetCode from the structure-instance-segment member using the full flexfield, application, structure, instance, and segment keys | derive_chart_of_accounts_roles |
| Accounting-calendar name passes local shape validation | Continue only after one exact ACCOUNTING calendar by UserPeriodSetName and its complete eligible-period set are resolved | Map returned PeriodType to AccountedPeriodType. Validate explicit or independently authoritative physical FirstLedgerPeriodName against EnteredPeriodName; never select from response order. Retain the complete set for the options-task handoff | resolve_accounting_calendar_exact |
| Currency code passes local shape validation | Continue only after one active monetary currency is resolved | Populate the authoritative currency code | resolve_monetary_currency_exact |
| AccountingMethodName is omitted or names Standard Accrual | Continue without asking for a method or technical tuple | Populate STANDARD_ACCRUAL, S, and blank SlaDescriptionLanguage in both PRIMARY aliases | resolve_accounting_method_evidence |
| AccountingMethodName explicitly names another method | Continue primary-ledger creation with the controlled Standard Accrual tuple and retain the exact requested display name as desired-state evidence | Add a post-create Specify Ledger Options UI handoff, require same-scope re-export after the user changes the method manually, and block Review and Submit readiness until that verification succeeds | resolve_accounting_method_evidence |
| Every identity and CoA role dependency is satisfied | Continue only with a fresh current-attempt template-only GL_MANAGE_PRIMARY_LEDGERS package whose ten CSV members are header-only and whose metadata proves the exact task and release | Route one template-only export, or reconcile the already accepted current-attempt result; never use a populated ledger export as the carrier | select_validated_general_ledger_package |
| A retained-earnings account or another option was supplied with the ledger request | The primary-shell request remains valid and the option stays outside this package | Persist a non-CSV handoff receipt and release it only after this task imports and verifies successfully |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Missing-value normalization | Preserve the raw supplied value for review; treat null and whitespace-only text as missing; do not silently trim or rewrite a value | Every text input |  |
| Exact-text normalization | Reject leading or trailing whitespace for a nonblank value; preserve internal whitespace, punctuation, and case; never case-fold, fuzzy-match, or substitute a similar label | Name, Description, ChartOfAccountsName, AccountingCalendarName, AccountingMethodName |  |
| Primary-ledger name length | Reject a Name longer than 30 characters before lookup or package authoring | Name is supplied |  |
| Description length | Reject a Description longer than 240 characters; do not manufacture a description when omitted | Description is supplied |  |
| Query-safe exact text | Use an encoded or bound exact query value; inability to encode punctuation safely is a client or transport error, not a no-match result | A live exact-name lookup runs |  |
| Accounting-method omission | Treat an omitted or whitespace-only AccountingMethodName as acceptance of the controlled Standard Accrual create policy; do not ask a baseline method question | No explicit method name is supplied | resolve_accounting_method_evidence |
| Standard Accrual tuple | Author only SlaAccountingMethodCode STANDARD_ACCRUAL, SlaAccountingMethodType S, and blank SlaDescriptionLanguage for a new FSCR-created primary ledger | Always for create, including when another desired method was stated | resolve_accounting_method_evidence |
| Alternative accounting-method request | Preserve the exact nonblank AccountingMethodName as a desired-state receipt, reject user-supplied physical method fields as unsupported direct authoring, and create the ledger with Standard Accrual | AccountingMethodName is neither Standard Accrual nor STANDARD_ACCRUAL | resolve_accounting_method_evidence |
| Unknown or service-owned fields | Reject user attempts to set identifiers, short name, audit columns, process identifiers, lifecycle status, or another undocumented field | User supplies technical fields outside the documented intake |  |
| Invocation cardinality | Author one requested primary ledger per task run while preserving every unrelated package row | Always |  |
| Export request cardinality | Reject a second export submission while a prior same-task request may have been accepted, is still polling, or already produced an unvalidated artifact | Either the CoA populated export or Primary Ledger template export is being acquired |  |

The whitespace and case rules above are conservative FSCR intake guards, not a claim that Oracle normalizes names the same way. They prevent silent mutation before the product's exact display-name and uniqueness checks.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.VALIDATE_INPUT | step | 10 | validate_input | valid->MPL.RESOLVE_REFERENCES;invalid->MPL.HANDLE_ERROR | none | stop | Before any authoritative lookup, package derivation, preview, or import. |
