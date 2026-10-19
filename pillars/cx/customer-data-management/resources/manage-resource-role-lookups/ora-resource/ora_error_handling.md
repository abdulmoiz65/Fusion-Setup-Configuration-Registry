# Manage Resource Role Lookups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Lookup type, operation, or required code information is missing | Stop and request the missing information |
| Standard lookup read returns no exact LookupCode match | Stop the role operation and direct the user to set up or activate the required code, then repeat validation |
| Lookup is secured or inaccessible | State that access is blocked and request the required security policy or authorized role |
| A requested change is not allowed by the configuration level or predefined-data rules | Stop and explain that the change is not supported |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing input | Required request facts are absent | Collect the missing facts |
| Contract gap | A lookup type or code mutation is requested without a documented mutation contract | Obtain the contract before execution; the documented standard-lookup GET remains available for read-only validation |
| Access blocked | REST access is secured or unavailable | Obtain approved access |
| Change blocked | Configuration level or predefined-data restrictions prohibit the request | Select an allowed change |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Execution blocked | Missing or blocked dependency and the safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup type or code mutation contract is not documented | Do not invent a mutation path, payload, or execution sequence |
| A lookup change is blocked | Do not retry or substitute another lookup type or code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRL.RETURN_ISSUES | terminal | 5 | terminal | none | none | stop | Input, lookup, access, or design validation fails |
| MRRL.RETURN_SUCCESS | terminal | 6 | terminal | none | MRRL.ENFORCE_CONFIGURATION | stop | The requested lookup operation passes all documented validation and design checks |
