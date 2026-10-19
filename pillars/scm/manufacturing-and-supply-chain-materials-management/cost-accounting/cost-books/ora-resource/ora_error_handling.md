# Error Handling

## Source

- [Oracle Fusion Cloud SCM: Create a Cost Book](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-book.html)
- [FSCR Data Loader](../../../../../../core/data-loader/SKILL.md)

## Error Situations

| Situation | What Should Happen |
|---|---|
| Cost Book identifier is missing | Stop and request the identifier. |
| Periodic Average Cost is requested but its enabled or disabled choice is not supplied | Stop and request the choice. |
| An update or delete source omits `CostBookId` and the Cost Book Code lookup returns zero or multiple exact matches | Stop; correct the code or resolve the lookup issue before rebuilding the source. |
| A delete or patch Excel template source has a blank or incorrect REST Action | Stop; use the Cost Books Excel template sheet and set REST Action to DELETE for delete cases or PATCH for patch cases, then rebuild and revalidate the source. |
| Data Loader source or Business Object validation fails | Stop before preview, correct the source data, and revalidate it through core.data-loader. |
| Upload or initiation is requested without an immutable Data Loader approval preview and a later standalone approve | Stop before the first POST. |
| Data Loader REST submission is requested | Route the operation through core.data-loader for upload and initiation; do not construct a direct REST request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | The Cost Book identifier or required Periodic Average Cost choice is absent | Collect the missing definition input. |
| Reference lookup | The required `CostBookId` cannot be resolved exactly for an update or delete | Correct the Cost Book Code or resolve the Fusion lookup issue, then rebuild and revalidate the source. |
| Data Loader validation | The source or costAccountingCostBooks Business Object does not pass Data Loader validation | Correct the source data and generate a new immutable approval preview. |
| Approval blocker | Upload or initiation is requested without a current immutable approval preview and later standalone approve | Stop before upload; obtain a new preview and then send approve in a separate message. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Definition-input failure | The missing Cost Book definition input and the corrective action. |
| Data Loader validation failure | The affected source data, validation result, and corrective action. |
| Data Loader approval gate | The immutable preview and the required standalone approve action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Data Loader validation or approval gate is incomplete | Do not upload, initiate, retry, or construct a direct REST request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CCB.HANDLE_ISSUE | step | 3 | error_handler | disclosed->RETURN_ISSUES | none | stop | Cost Book definition input or lookup is invalid or missing |
| CCB.DONE | terminal | 4 | terminal | none | CCB.RESOLVE_COST_BOOK_ID | stop | Cost Book definition input and required delete lookup passed |
| RETURN_ISSUES | terminal | 5 | terminal | none | none | stop | Error disclosure complete |
