# Design Enforcement

Source: Oracle Fusion Cloud Financials, Guidelines for Managing Tree Structures — https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/guidelines-for-managing-tree-structures.html#s20030940

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm lifecycle action | Identify whether the request creates, edits, deletes, copies, or changes the status of a tree structure. |
| 2 | Review associated-tree impact | Review the documented effect on associated trees and tree versions before preview. |
| 3 | Verify copy scope | For a reuse request, copy the tree structure without copying associated trees and tree versions. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Edit of an Active tree structure | Error |  | The preview does not disclose that the structure and all associated trees and tree versions change to Draft | Include the Draft-status impact in the preview before any execution | Yes |
| Delete of a tree structure | Error |  | The preview does not disclose that all associated trees and tree versions are automatically deleted | Confirm the deletion scope and impact before any execution | Yes |
| Reuse of a tree structure | Error |  | The request copies associated trees or tree versions with the tree structure | Copy only the tree structure | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.DESIGN_REVIEW | decision | 2 | design_enforcement | pass->TCS.EXECUTION_GATE;fail->TCS.RETURN_ISSUES | TCS.VALIDATE_INPUT | stop | Before any create, edit, delete, copy, or status-change preview. |
