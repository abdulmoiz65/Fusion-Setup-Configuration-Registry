# Error Handling

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Fusion Cloud SCM 26c | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/cost-profiles-default-cost-profiles-and-item-cost-profiles.html | Item Cost Profile assignment eligibility and profile-type selection errors |

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required or supplied optional resolver returns zero or multiple exact matches | Stop and ask for a valid unique complete user-friendly value. Do not select a partial or first result. |
| Cost Book is not valid for the resolved Cost Organization | Stop and request a Cost Book Code valid for that Cost Organization. |
| Item is not Costing Enabled for the resolved Cost Organization | Stop and request a valid Costing Enabled Item Number. |
| Expense or Asset profile is Periodic Average | Stop and request a non-Periodic Average Cost Profile Code. |
| The Cost Book lookup finds no exact non-Periodic Average Cost Book | Stop and request a valid Cost Book Code with PeriodicAverageFlag=false for the resolved Cost Organization. |
| The generic Costing Items LOV route rejects the documented request with HTTP 400 | Resolve a same-environment verified versioned route from approved environment metadata or configuration, retain it only for the current session, and rerun the same documented request. Do not ask the user for a raw URL, add a predicate, or use another tenant's route. |
| Neither the generic nor same-environment verified Costing Items LOV route accepts the documented request | Stop and report a fusion_api_error. Do not select an item or upload the Data Loader archive. |
| The deletion Cost Book lookup finds no exact Cost Book for the resolved Cost Organization | Stop before Item Cost Profile identification and request a valid unique Cost Book Code. The deletion lookup must not substitute a partial or arbitrary book. |
| A Cost Profile Code is supplied under the wrong profile type | Stop and ask the user to confirm the intended Expense, Asset, or Consigned type; do not resolve the code through another profile-type finder without confirmation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | A required Item Cost Profile value is incomplete | Request the missing complete value. |
| catalog mismatch | An exact Cost Organization, Cost Book, Item, or Cost Profile match cannot be resolved | Request a valid unique value. |
| fusion_api_error | The documented Costing Items lookup is rejected by both the generic and same-environment verified routes | Correct the environment route contract before rerunning validation. |
| business-rule conflict | A profile is Periodic Average where Item Cost Profile assignment does not permit it, or a profile code is supplied under the wrong type | Select an eligible profile for the intended type. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Item Cost Profile validation is blocked | The resolver, supplied business value, exact-match result, and the required correction. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Exact-match lookup fails | Do not select an arbitrary, partial, or first lookup result. |
| A Cost Profile Code is supplied under the wrong profile type | Do not resolve it through a different profile-type finder without confirmation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICP.READY_FOR_REST_IMPORT | decision | 10 | execution_gate | ready->ICP.RETURN_SUCCESS;blocked->ICP.HANDLE_ISSUE | ICP.ENFORCE_LOADER_PAYLOAD_CONTRACT | stop | Before core.data-loader import |
| ICP.HANDLE_ISSUE | terminal | 11 | terminal | none | none | stop | Any blocked, invalid, or failed prior step |
| ICP.RETURN_SUCCESS | terminal | 12 | terminal | none | ICP.READY_FOR_REST_IMPORT | stop | The Item Cost Profile Data Loader import handoff is ready for core.data-loader |
| ICP.DELETE_LOADER_SOURCE | decision | 13 | execution_gate | validated->ICP.DELETE_APPROVAL_GATE;blocked->ICP.DELETE_HANDLE_ISSUE | ICP.VALIDATE_INPUT | stop | Validate the delete-oriented source through core.data-loader |
| ICP.DELETE_APPROVAL_GATE | decision | 14 | execution_gate | approved->ICP.RETURN_DELETE_READY;missing_approval->ICP.DELETE_HANDLE_ISSUE | ICP.DELETE_LOADER_SOURCE | stop | Before delete-oriented core.data-loader submission |
| ICP.RETURN_DELETE_READY | terminal | 15 | terminal | none | ICP.DELETE_APPROVAL_GATE | stop | The Item Cost Profile deletion handoff is ready for core.data-loader |
| ICP.DELETE_HANDLE_ISSUE | terminal | 16 | terminal | none | none | stop | Any blocked Item Cost Profile deletion step |
