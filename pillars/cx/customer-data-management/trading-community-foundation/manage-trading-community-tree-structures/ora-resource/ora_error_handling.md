# Error Handling

Source: Oracle Fusion Cloud Financials, Guidelines for Managing Tree Structures — https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/guidelines-for-managing-tree-structures.html#s20030940

## Error Situations

| Situation | What Should Happen |
|---|---|
| Requested lifecycle action or affected tree structure is missing | Stop before preview and request the missing identity or action. |
| Requested status is not Draft, Active, or Inactive | Stop before preview and request one documented status. |
| Edit of an Active tree structure omits its Draft-status impact | Stop before preview and disclose the effect on the structure, associated trees, and tree versions. |
| Delete request omits the associated-tree and version impact | Stop before preview and disclose that the associated trees and tree versions are automatically deleted. |
| Approved archive, target environment, or Task Hook envelope does not match | Stop before POST and rebuild the immutable approval preview. |
| Fusion rejects the task CSV import process creation request | Preserve a redacted response and stop without automatically retrying the POST. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Lifecycle action, identity, or documented status is missing or invalid | Correct the request and revalidate. |
| design_blocker | Required active-edit, delete, or copy impact has not been included in the preview | Correct the preview scope and rerun design enforcement. |
| fusion_api_error | Fusion rejects the native setup-task CSV import request | Preserve redacted diagnostics and stop without retrying. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Active edit preview | That the tree structure and all associated trees and tree versions change to Draft. |
| Delete preview | That the tree structure's associated trees and tree versions are automatically deleted. |
| Copy preview | That only the tree structure is copied; associated trees and tree versions are not copied. |
| Execution readiness | The immutable path/hash, target environment, approval envelope, and task-local native FSM adapter. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.EXECUTION_GATE | decision | 3 | execution_gate | ready->TCS.READY;blocked->TCS.RETURN_ISSUES | TCS.DESIGN_REVIEW | stop | Before execution; approved path/hash/envelope and the native FSM adapter must match. |
| TCS.READY | terminal | 4 | terminal | none | TCS.EXECUTION_GATE | continue | The native FSM adapter and all applicable preview gates are ready. |
| TCS.RETURN_ISSUES | terminal | 5 | terminal | none | none | continue | Input, design, or execution-contract readiness is blocked. |
