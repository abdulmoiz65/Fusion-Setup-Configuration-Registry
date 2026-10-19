# Picking Rule Assignments Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Fusion read-only metadata, `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV` | Confirms the task's verified standard-lookups collection path. The configured target environment supplies the host. |
| Target-environment Data Loader metadata and sample/validation result | Establishes whether the registered BO accepts `RuleName` and records the resulting Picking Rule mapping before preparation. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_item_type | `ItemTypeMeaning`, `ItemType`, or both are supplied | `ItemTypeMeaning`, `ItemType` | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='EGP_ITEM_TYPE'&onlyData=true` | `LookupCode`, `Meaning` | Trim outer whitespace. Match Meaning to `ItemTypeMeaning` and LookupCode to `ItemType` with case-insensitive exact comparison. Both inputs must identify one same row. | `ItemType`: `LookupCode`; preserve returned `Meaning` as diagnostic output. | Block preparation; do not fuzzy-match or choose the first row. |
| resolve_date_type | `DateTypeMeaning`, `DateTypeCode`, or both are supplied | `DateTypeMeaning`, `DateTypeCode` | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='INV_RULES_DATE_TYPE'&onlyData=true` | `LookupCode`, `Meaning` | Trim outer whitespace. Match Meaning to `DateTypeMeaning` and LookupCode to `DateTypeCode` with case-insensitive exact comparison. Both inputs must identify one same row. | `DateTypeCode`: `LookupCode`; preserve returned `Meaning` as diagnostic output. | Block preparation; do not fuzzy-match or choose the first row. |
| resolve_transaction_action | `TransactionActionMeaning`, `TransactionActionId`, or both are supplied | `TransactionActionMeaning`, `TransactionActionId` | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='INV_TRANSACTION_ACTION'&onlyData=true` | `LookupCode`, `Meaning` | Trim outer whitespace. Match Meaning to `TransactionActionMeaning` and LookupCode to `TransactionActionId` with case-insensitive exact comparison. Both inputs must identify one same row. | `TransactionActionId`: `LookupCode`; preserve returned `Meaning` as diagnostic output. | Block preparation; do not fuzzy-match or choose the first row. |

## Lookup Execution Rules

Each resolver delegates the declared read-only GET to `core.fusion-api.rest-api-client`. That core capability owns authentication, target identity, authorization handling, retry boundaries, and redacted response transport. This resource supplies only the task-specific path, query, mapping, and match rule; it must not provide direct REST transport or write guidance.

Only the target-environment registered `inventoryPickingRuleAssignments` BO may resolve `RuleName` to `PickingRuleId`, and resolve `CarrierName`, `CategoryName`, `CustomerName`, `UnitOfMeasure`, and `ABCAssignmentGroupClassName` when those mappings are available. Establish the accepted mappings through the required Data Loader metadata/sample or immutable-source validation before preparation. Do not add task-local resolvers for `PickingRuleId`, `FreightCarrierId`, `CategoryId`, `CustomerId`, `UOMCode`, `AbcClassId`, or `AssignmentGroupId`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PRA.RESOLVE_ITEM_TYPE | decision | 20 | reference_lookup | resolved->PRA.RESOLVE_DATE_TYPE;not_required->PRA.RESOLVE_DATE_TYPE;blocked->PRA.HANDLE_ERROR;failure->PRA.HANDLE_ERROR | PRA.VALIDATE_INPUT | stop | Resolve supplied Item Type input when required. |
| PRA.RESOLVE_DATE_TYPE | decision | 30 | reference_lookup | resolved->PRA.RESOLVE_TRANSACTION_ACTION;not_required->PRA.RESOLVE_TRANSACTION_ACTION;blocked->PRA.HANDLE_ERROR;failure->PRA.HANDLE_ERROR | PRA.RESOLVE_ITEM_TYPE | stop | Resolve supplied Date Type input when required. |
| PRA.RESOLVE_TRANSACTION_ACTION | decision | 40 | reference_lookup | resolved->PRA.CHECK_READINESS;not_required->PRA.CHECK_READINESS;blocked->PRA.HANDLE_ERROR;failure->PRA.HANDLE_ERROR | PRA.RESOLVE_DATE_TYPE | stop | Resolve supplied Transaction Action input when required. |
