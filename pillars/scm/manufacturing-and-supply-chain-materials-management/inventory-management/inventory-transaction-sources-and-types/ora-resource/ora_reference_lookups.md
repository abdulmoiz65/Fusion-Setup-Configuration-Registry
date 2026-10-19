# Inventory Transaction Sources and Types Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Oracle readiness: Redwood Manage Transaction Sources and Types Using a Redwood Page, https://docs.oracle.com/en/cloud/saas/readiness/scm/25b/inv25b/25B-inventory-wn-f36660.htm | Confirms Value Set appears on the Redwood transaction source create/update flow |
| Implementation owner REST metadata | Confirms the REST/Data Loader implementation field is DescriptiveFlexContext and its UI title is Value Set |
| Implementation owner UI research | Confirms Value Set is a user-facing LOV value resolved through the source DFF context LOV before Data Loader handoff |
| Prior scm-inv-transaction-setup-tasks implementation | Concrete lookup path and matching rule for INV_TRANSACTION_SOURCES DFF contexts |
| Prior scm-inv-transaction-setup-tasks implementation | Concrete Transaction Action LOV path, source-specific lookup groups, and display-name to ID mapping |
| Implementation owner testing | New source and child type create flow has no TransactionSourceTypeId yet and must use the user-defined source action group INV_TRANSACTION_ACTION_GRP3 |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_transaction_source_type | Transaction types are requested for an existing transaction source and TransactionSourceTypeName is supplied without TransactionSourceTypeId | TransactionSourceTypeName | /fscmRestApi/resources/11.13.18.05/inventoryTransactionSources?fields=TransactionSourceTypeId,TransactionSourceTypeName&onlyData=true&q=TransactionSourceTypeName='<TransactionSourceTypeName>' | TransactionSourceTypeId, TransactionSourceTypeName | Trim outer whitespace and require one exact TransactionSourceTypeName match. Do not run this lookup when the request is creating a new transaction source and child transaction types in the same request because the source ID does not exist yet. | TransactionSourceTypeId: TransactionSourceTypeId; TransactionSourceTypeName: TransactionSourceTypeName | Stop and ask for a valid existing Transaction Source Name or TransactionSourceTypeId; do not guess, fuzzy-match, or pick the first source |
| resolve_transaction_action_name | Transaction Action or TransactionActionName is supplied and TransactionActionId is blank, or both display name and ID are supplied and must be compared | Transaction Action display value, TransactionActionName, TransactionActionId, TransactionSourceTypeId when available, and new-source-create context when applicable | /fscmRestApi/resources/11.13.18.05/inventoryTransactionActionsLOV?fields=LookupCode,Meaning,LookupType&onlyData=true&q=<source-specific LookupType filter and optional LookupCode or Meaning filter>&orderBy=Meaning | LookupCode, Meaning, LookupType | Trim outer whitespace and compare case-insensitively for matching while preserving the returned LOV values for output. Select the action lookup group before matching. For an existing source, use the resolved TransactionSourceTypeId: source 3 or 6 uses INV_TRANSACTION_ACTION_GRP1; source 4 uses INV_TRANSACTION_ACTION_GRP2; source 13 or custom source greater than 100 uses INV_TRANSACTION_ACTION_GRP3. For a new transaction source and child transaction types created in the same request, use INV_TRANSACTION_ACTION_GRP3 because the source is user-defined and TransactionSourceTypeId is not available yet. First require case-insensitive exact LookupCode match to TransactionActionId when supplied; otherwise require case-insensitive exact Meaning match to Transaction Action or TransactionActionName. When both display name and ID are supplied, they must identify the same row in the selected group after case-insensitive comparison. If neither source ID nor new-source-create context is known, evaluate all three groups and continue only when exactly one case-insensitive exact match exists. | TransactionActionId: LookupCode; TransactionActionName: Meaning | Stop and ask for a valid Transaction Action display value or TransactionActionId plus the source context needed to select the lookup group; do not guess, fuzzy-match, use contains matching, use an unfiltered ambiguous action, or pick the first candidate |
| resolve_transaction_source_value_set | Value Set is supplied and DescriptiveFlexContext is blank, or both are supplied and must be compared | Value Set display Name or ContextCode; DescriptiveFlexContext when supplied | /fscmRestApi/resources/11.13.18.05/FlexFndDffDescriptiveFlexfieldContexts?fields=ContextCode,Name,EnabledFlag&onlyData=true&q=ApplicationId=401 AND DescriptiveFlexfieldCode='INV_TRANSACTION_SOURCES' | ContextCode, Name, EnabledFlag | Trim outer whitespace. First require exact ContextCode match to the supplied Value Set; if no ContextCode match, require exact Name match. Only EnabledFlag Y contexts are valid. When DescriptiveFlexContext is also supplied, it must equal the resolved ContextCode. | DescriptiveFlexContext: ContextCode | Stop and ask for a valid enabled Value Set Name or ContextCode; do not guess, fuzzy-match, use disabled contexts, or pick the first candidate |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Existing transaction source name supplied for child transaction types | Resolve TransactionSourceTypeId before Transaction Action lookup |
| New transaction source and child transaction types supplied together | Do not look up TransactionSourceTypeId; use INV_TRANSACTION_ACTION_GRP3 for Transaction Action lookup context |
| Transaction Action omitted | No action lookup runs and TransactionActionId remains blank unless supplied directly |
| Transaction Action or TransactionActionName supplied | Resolve one case-insensitive exact inventory transaction action before Data Loader handoff |
| Transaction Action display value and TransactionActionId both supplied | Confirm they identify the same LOV row after case-insensitive comparison; otherwise return a conflicting-input issue |
| Transaction source type is available for action resolution | Apply the Redwood source-specific action lookup group before matching |
| Transaction source type is not available and this is not a new-source create flow | Evaluate the known Redwood action lookup groups and continue only when the action resolves to exactly one row after case-insensitive comparison |
| Value Set omitted | No lookup runs and DescriptiveFlexContext remains blank unless supplied directly |
| Value Set supplied | Resolve one exact enabled INV_TRANSACTION_SOURCES DFF context before Data Loader handoff |
| Value Set and DescriptiveFlexContext both supplied | Confirm they identify the same context; otherwise return a conflicting-input issue |
| Lookup unavailable | Classify as a lookup/readiness issue and stop before Data Loader handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TST.RESOLVE_TRANSACTION_SOURCE | decision | 20 | reference_lookup | resolved->TST.RESOLVE_TRANSACTION_ACTION;not_required->TST.RESOLVE_TRANSACTION_ACTION;blocked->TST.HANDLE_ERROR;failure->TST.HANDLE_ERROR | TST.VALIDATE_INPUT | stop | Resolve existing Transaction Source Name to TransactionSourceTypeId only when needed for child transaction type action context |
| TST.RESOLVE_TRANSACTION_ACTION | decision | 30 | reference_lookup | resolved->TST.RESOLVE_VALUE_SET;not_required->TST.RESOLVE_VALUE_SET;blocked->TST.HANDLE_ERROR;failure->TST.HANDLE_ERROR | TST.RESOLVE_TRANSACTION_SOURCE | stop | Resolve Transaction Action display value only when supplied |
| TST.RESOLVE_VALUE_SET | decision | 40 | reference_lookup | resolved->TST.CHECK_DEPENDENCIES;not_required->TST.CHECK_DEPENDENCIES;blocked->TST.HANDLE_ERROR;failure->TST.HANDLE_ERROR | TST.RESOLVE_TRANSACTION_ACTION | stop | Resolve Value Set only when supplied |
