# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing environment, membership, category, type, or code | Stop and request only missing evidence. |
| 401 or 403 | Classify auth/authz; never report absence or try another category. |
| System field other than Meaning, or System create/delete | Refuse before preview. |
| Extensible mutation without proven custom origin or permitted field | Refuse before preview. |
| Stale preview or missing approval | Stop before mutation and rebuild the immutable preview. |
| Uncertain POST, PATCH, or DELETE | Reconcile once with exact GET; never retry automatically. |
| Missing Task Hook/hash approval | Stop before FSM upload. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.ERROR | step | 80 | error_handler | disclosed->DML.RETURN_ISSUES | none | stop | Any blocked gate. |
| DML.READY | terminal | 90 | terminal | none | DML.ENFORCE | continue | Validated and ready for the owning executor. |
| DML.RETURN_ISSUES | terminal | 99 | terminal | none | DML.ERROR | continue | Classified issues returned without side effect. |
