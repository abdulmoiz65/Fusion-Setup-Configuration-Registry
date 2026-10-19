# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Any local, dependency, lookup, or design failure | Stop at first failure and return the correction. |
| Lookup failure | Do not retry automatically; retain redacted diagnostics only. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Multiple candidates, missing evidence, or failed lookup | Do not guess, select an ambiguous organization, substitute a similar name, or continue to a change action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MIO.HANDLE_ISSUE | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | stop | Prior node reports invalid, blocked, rejected, or failed |
| MIO.DONE | terminal | 8 | terminal | none | MIO.ENFORCE | stop | Creation passed all documented gates |
| RETURN_ISSUES | terminal | 9 | terminal | none | none | stop | Error disclosure complete |
