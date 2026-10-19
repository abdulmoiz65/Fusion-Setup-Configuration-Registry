# Input Validation

## Source

- [Oracle Fusion Cloud SCM: Set Up Cost Accounting](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-cost-accounting.html)
- [Oracle Fusion Cloud SCM: Create a Cost Book](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-a-cost-book.html)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Cost book identity | Cost book identifier and, when supplied, description | Block | Provide the identifier to create or update the Cost Book definition | Creating or changing a Cost Book definition | |
| Periodic Average Cost choice | Explicit enabled or disabled choice when periodic average costing is in scope | Block | Confirm whether the Cost Book is periodic-average enabled | Creating or changing a periodic-average Cost Book definition | |
| Excel template REST Action | DELETE for a delete source or PATCH for a patch source | Block | Use the Cost Books Excel template sheet and set REST Action to DELETE for delete cases or PATCH for patch cases | Updating or deleting a Cost Book definition | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Cost Book identifier is present | Continue to the definition-complete terminal | Creating or changing a Cost Book definition | |
| Periodic Average Cost choice is explicit when that feature is requested | Continue to the definition-complete terminal | Creating or changing a periodic-average Cost Book definition | |
| Update or delete source has CostBookId | Continue to the definition-complete terminal | Updating or deleting a Cost Book when CostBookId is absent | resolve_cost_book_id_exact |
| Excel template REST Action is DELETE | Continue to the definition-complete terminal | Deleting a Cost Book | |
| Excel template REST Action is PATCH | Continue to the definition-complete terminal | Patching a Cost Book | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CCB.VALIDATE | decision | 1 | validate_input | valid->CCB.RESOLVE_COST_BOOK_ID;invalid->CCB.HANDLE_ISSUE | none | stop | Creating, changing, or deleting a Cost Book definition |
