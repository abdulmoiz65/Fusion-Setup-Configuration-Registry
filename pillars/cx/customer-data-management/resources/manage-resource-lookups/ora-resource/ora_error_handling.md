# Manage Resource Lookups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Lookup type, operation, or required code information is missing | Stop and request the missing information |
| Lookup REST contract is TBD | Stop and identify the missing task-specific endpoint and request contract |
| Lookup is secured or inaccessible | State that access is blocked and request the required security policy or authorized role |
| A requested change is not allowed by the configuration level or predefined-data rules | Stop and explain that the change is not supported |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing input | Required request facts are absent | Collect the missing facts |
| Contract gap | A task-specific endpoint or mutation contract is not documented | Obtain the contract before execution |
| Access blocked | REST access is secured or unavailable | Obtain approved access |
| Change blocked | Configuration level or predefined-data restrictions prohibit the request | Select an allowed change |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Execution blocked | Missing or blocked dependency and the safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Task-specific REST contract is TBD | Do not invent a request path, payload, or mutation sequence |
| A lookup change is blocked | Do not retry or substitute another lookup type or code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRL.RETURN_ISSUES | terminal | 5 | terminal | none | none | stop | Input, lookup, access, or design validation fails |
| MRL.RETURN_SUCCESS | terminal | 6 | terminal | none | MRL.ENFORCE_CONFIGURATION | stop | The requested lookup operation passes all documented validation and design checks |
