# Inventory Transaction Sources and Types Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Implementation owner confirmation | Inventory Transaction Sources and Types has no setup dependency beyond optional display-value resolution for this task authoring scope |
| Implementation owner REST/UI research | Existing source name, Value Set, and Transaction Action display names are the only local pre-Data-Loader readiness dependencies retained for this task |
| Prior scm-inv-transaction-setup-tasks implementation | Concrete DFF context lookup path for INV_TRANSACTION_SOURCES Value Set resolution |
| Prior scm-inv-transaction-setup-tasks implementation | Concrete inventory transaction action LOV path and source-specific lookup group mapping |
| Implementation owner testing | New source and child type create flow should use INV_TRANSACTION_ACTION_GRP3 because the source is user-defined before it has a TransactionSourceTypeId |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing transaction source ID | If child transaction types are requested for an existing source by name, resolve TransactionSourceTypeId before Transaction Action lookup |
| 2 | Transaction Action ID | If a Transaction Action display value is supplied, resolve it to exactly one TransactionActionId before Data Loader handoff |
| 3 | Value Set context | If a Value Set is supplied, resolve it to exactly one DescriptiveFlexContext before Data Loader handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_transaction_source_id | Existing transaction source ID | Conditional | Transaction types are requested for an existing transaction source and TransactionSourceTypeName is supplied without TransactionSourceTypeId | Lookup | inventoryTransactionSources exact TransactionSourceTypeName lookup | resolve_transaction_source_type | The Transaction Action LOV group depends on the selected source type for existing-source child type requests | Provide an exact existing Transaction Source Name or provide TransactionSourceTypeId directly | TransactionSourceTypeId, TransactionSourceTypeName |
| transaction_action_id | Transaction Action ID | Conditional | Transaction Action or TransactionActionName is supplied, or Transaction Action display value and TransactionActionId must be compared | Lookup | inventoryTransactionActionsLOV using the resolved source group; use INV_TRANSACTION_ACTION_GRP3 for new source plus child type create flow | resolve_transaction_action_name | Redwood exposes Transaction Action as a display LOV, while Data Loader needs the TransactionActionId code when a display value is supplied | Provide a valid Transaction Action display value for the selected source, provide TransactionActionId directly, or make the request clearly identify existing-source versus new-source create context; display value and ID matching is trim plus case-insensitive exact | TransactionActionId, TransactionActionName |
| value_set_context | Transaction source Value Set context | Conditional | Value Set is supplied or Value Set and DescriptiveFlexContext must be compared | Lookup | FlexFndDffDescriptiveFlexfieldContexts for ApplicationId 401 and DescriptiveFlexfieldCode INV_TRANSACTION_SOURCES | resolve_transaction_source_value_set | The Redwood Value Set label is stored for the transaction source as DescriptiveFlexContext ContextCode | Provide a valid enabled Value Set Name or ContextCode; leave blank when no DFF context is needed | DescriptiveFlexContext |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Friendly display values are omitted, or implementation fields are already supplied without conflict | Continue |
| Lookup | Existing source name must be resolved for action context, Transaction Action must be resolved to TransactionActionId, or Value Set must be resolved or compared to DescriptiveFlexContext | Read-only only |
| Blocked | Existing source, Transaction Action, or Value Set lookup is absent from metadata, ambiguous, inaccessible, inactive where applicable, or conflicts with the implementation field | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TST.CHECK_DEPENDENCIES | decision | 50 | resolve_dependency | ready->TST.DATA_LOADER_HANDOFF;blocked->TST.HANDLE_ERROR | TST.RESOLVE_VALUE_SET | stop | After local normalization and optional existing source, Transaction Action, and Value Set resolution |
