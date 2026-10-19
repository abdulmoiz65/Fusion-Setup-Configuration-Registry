# Reference Lookups

## Source

| Source | Location | Used For |
|---|---|---|
| Developer-provided Cost Books REST contract | `/fscmRestApi/resources/11.13.18.05/costAccountingCostBooks?q=CostBookCode='<specified cost book code>'` | Resolve the local `CostBookId` for an update or delete source when it is not supplied. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_cost_book_id_exact | A Cost Book update or delete is requested and `CostBookId` is absent | One exact `CostBookCode` | `/fscmRestApi/resources/11.13.18.05/costAccountingCostBooks?q=CostBookCode='<specified cost book code>'` | `CostBookId`, `CostBookCode` | Require exactly one returned item whose `CostBookCode` exactly matches the supplied code. | `CostBookId` | Zero matches, multiple matches, malformed responses, authentication, authorization, or transport failures block the update or delete. |

## Lookup Execution Rules

1. Use this REST path only through `core/fusion-api/rest-api-client` as a read-only `GET`.
2. Use the active Fusion environment from the shared authentication configuration. Do not provide or override a host.
3. Preserve the supplied Cost Book Code exactly for the match. Do not select a partial or first match.
4. Use the resolved `CostBookId` only to rebuild and revalidate the update or delete source. For an update, the Data Loader uses the resolved key with the selected PATCH operation. The lookup itself must not create, update, delete, upload, or initiate data.
5. A source or lookup change invalidates any prior Data Loader validation archive and approval preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CCB.RESOLVE_COST_BOOK_ID | step | 2 | reference_lookup | resolved->CCB.DONE;not_applicable->CCB.DONE;blocked->CCB.HANDLE_ISSUE;failure->CCB.HANDLE_ISSUE | CCB.VALIDATE | stop | Updating or deleting a Cost Book when `CostBookId` is not supplied. |
