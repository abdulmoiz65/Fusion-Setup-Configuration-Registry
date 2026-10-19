# Inventory Transaction Sources and Types Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Oracle readiness: Redwood Manage Transaction Sources and Types Using a Redwood Page, https://docs.oracle.com/en/cloud/saas/readiness/scm/25b/inv25b/25B-inventory-wn-f36660.htm | Redwood task identity and visible source/type fields |
| Oracle Inventory Management: Transaction Types, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/faims/transaction-types.html | Functional meaning of transaction sources, transaction types, and transaction actions |
| Implementation owner confirmation | Registered Data Loader business object inventoryTransactionSources |
| Implementation owner REST/UI research | Value Set UI label maps to DescriptiveFlexContext; Transaction Action display values and friendly status/location inputs need resolution or normalization |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Backend-owned validations | Do not duplicate required-field, length, uniqueness, date, transaction action, or source/type domain validations handled by the registered business object or Data Loader |
| Local validation ownership | Validate only user-friendly aliases that must be resolved or normalized before Data Loader receives the values |
| REST execution | Do not create direct REST write guidance; Data Loader owns execution for inventoryTransactionSources |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Friendly control values | LocationRequired, EnableStatusControl, AllowProjectTransactions | Continue with blank values | Normalize only supplied values and leave omitted values blank | Before Data Loader validation or import preparation |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Transaction types are requested for an existing transaction source and TransactionSourceTypeName is supplied without TransactionSourceTypeId | Continue only after resolving one exact existing source | Fill TransactionSourceTypeId from the source resolver before Transaction Action resolution | resolve_transaction_source_type |
| A new transaction source and child transaction types are being created in the same request | Do not look up TransactionSourceTypeId before the source exists | Treat the transaction source as a new user-defined source for Transaction Action LOV context | resolve_transaction_action_name |
| Transaction Action or TransactionActionName is supplied instead of TransactionActionId | Continue only after resolving one case-insensitive exact compatible action value | Fill TransactionActionId from the Transaction Action resolver before Data Loader handoff | resolve_transaction_action_name |
| TransactionActionId is supplied directly | Continue with the supplied TransactionActionId and do not also require TransactionActionName | Treat it as the implementation field value for Data Loader handoff |  |
| Value Set is supplied instead of DescriptiveFlexContext | Continue only after resolving one exact active context value | Fill DescriptiveFlexContext from the Value Set resolver before Data Loader handoff | resolve_transaction_source_value_set |
| DescriptiveFlexContext is supplied directly | Continue with the supplied DescriptiveFlexContext and do not also require Value Set | Treat it as the implementation field value for Data Loader handoff |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LocationRequired normalization | Accept blank, Y, N, Yes, or No; normalize Yes or Y to Y, No or N to N, and blank to blank | LocationRequired is supplied |  |
| EnableStatusControl normalization | Accept blank, 1, 2, Y, N, Yes, or No; normalize Yes or Y to 1, No or N to 2, and preserve 1, 2, or blank | EnableStatusControl is supplied |  |
| AllowProjectTransactions normalization | Accept blank, 1, 2, Y, N, Yes, or No; normalize Yes or Y to 1, No or N to 2, and preserve 1, 2, or blank | AllowProjectTransactions is supplied |  |
| Conflicting Transaction Action inputs | Reject when Transaction Action or TransactionActionName and TransactionActionId are both supplied but resolve to different lookup rows | Transaction Action or TransactionActionName and TransactionActionId are both supplied | resolve_transaction_action_name |
| Conflicting Value Set inputs | Reject when Value Set and DescriptiveFlexContext are both supplied with different values | Both Value Set and DescriptiveFlexContext are supplied | resolve_transaction_source_value_set |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TST.VALIDATE_INPUT | step | 10 | validate_input | valid->TST.RESOLVE_TRANSACTION_SOURCE;invalid->TST.HANDLE_ERROR | none | stop | Before Data Loader task validation or import preparation |
