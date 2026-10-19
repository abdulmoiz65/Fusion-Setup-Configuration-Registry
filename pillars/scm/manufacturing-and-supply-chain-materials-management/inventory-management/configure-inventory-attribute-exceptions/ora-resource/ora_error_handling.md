# Configure Inventory Attribute Exceptions Completion

## Completion Behavior

| Condition | What Should Happen | Next Action | What Must Not Happen |
|---|---|---|---|
| The approved task-local rules complete | Return the prepared rule results to the invoking Data Loader Task Hook. | Continue with Core Data Loader preview, approval, upload, and initiation. | Do not issue a direct REST write from this task resource. |
| Scope is ambiguous, incomplete, or missing while the type is omitted | Stop preparation and request clarification. | Ask the user to choose either item-level or category-level scope. | Do not choose a scope automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IAE.DONE | terminal | 30 | terminal | none | IAE.DERIVE_EXCEPTION_TYPE | continue | The approved task-local rules are ready for the invoking Data Loader Task Hook; Core Data Loader owns preview, approval, upload, and initiation. |
| IAE.REQUEST_SCOPE_CLARITY | terminal | 40 | terminal | none | IAE.DERIVE_EXCEPTION_TYPE | stop | The request needs clarification because its type is omitted and item-level/category-level scope is ambiguous, incomplete, or missing. |
