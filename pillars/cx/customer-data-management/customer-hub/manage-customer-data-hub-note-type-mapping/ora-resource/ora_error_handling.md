# Error Handling

## Error Situations
| Situation | What Should Happen |
|---|---|
| Missing environment, unsupported source object, or ambiguous object/code | Stop and request missing evidence; use NOTE only when SourceObjectCode is omitted. |
| 401 or 403 | Classify auth/authz; never report no mappings. |
| Empty successful GET | Report no effective rows for that exact request; do not infer global absence. |
| Mutation requested | Refuse before any HTTP request. |
| Missing Task Hook/hash approval | Stop before FSM upload. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.ERROR | step | 80 | error_handler | disclosed->NTM.RETURN_ISSUES | none | stop | Any blocked gate. |
| NTM.READY | terminal | 90 | terminal | none | NTM.ENFORCE | continue | Validated and ready. |
| NTM.RETURN_ISSUES | terminal | 99 | terminal | none | NTM.ERROR | continue | Classified issues returned without side effect. |
