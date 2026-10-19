# Error Handling

## Error Situations
| Situation | What Should Happen |
|---|---|
| Missing environment, exact parent, code, level, seed, or describe | Stop and request missing evidence. |
| 401 or 403 | Classify auth/authz; never infer absence. |
| Seeded target, unsupported field, duplicate create, stale preview, or missing approval | Refuse before mutation. |
| Uncertain mutation | Reconcile with exact GET; never retry automatically. |
| Missing Task Hook/hash approval | Stop before FSM upload. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.ERROR | step | 80 | error_handler | disclosed->NT.RETURN_ISSUES | none | stop | Any blocked gate. |
| NT.READY | terminal | 90 | terminal | none | NT.ENFORCE | continue | Validated and ready. |
| NT.RETURN_ISSUES | terminal | 99 | terminal | none | NT.ERROR | continue | Classified issues returned without side effect. |
