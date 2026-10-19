# Error Handling

## Error Situations
| Situation | What Should Happen |
|---|---|
| Missing environment, membership, category, type, or code | Stop and request missing evidence. |
| 401 or 403 | Classify auth/authz; never infer absence. |
| Non-Meaning field, create/delete, stale preview, or missing approval | Refuse before mutation. |
| Uncertain PATCH | Reconcile with GET; never retry automatically. |
| Missing Task Hook/hash approval | Stop before FSM upload. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.ERROR | step | 80 | error_handler | disclosed->DCL.RETURN_ISSUES | none | stop | Any blocked gate. |
| DCL.READY | terminal | 90 | terminal | none | DCL.ENFORCE | continue | Validated and ready. |
| DCL.RETURN_ISSUES | terminal | 99 | terminal | none | DCL.ERROR | continue | Classified issues returned without side effect. |
