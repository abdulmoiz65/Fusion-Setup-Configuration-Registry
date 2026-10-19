# Manage Resource Team Descriptive Flexfields Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required DFF configuration information is missing | Stop and request the missing business outcome, segment, context, validation, or sandbox-test information |
| A segment sequence conflicts with an existing sequence | Stop and select a unique sequence number in the applicable global or context-sensitive segment scope |
| A context value set is incompatible | Stop and use an independent or table-validated Character value set that satisfies the documented length and bind restrictions |
| Initial-value SQL returns multiple rows or an incompatible type | Stop and correct the statement before configuration |
| An existing context is requested for deletion | Stop; disable the associated context value by end-dating it instead |
| Sandbox deployment or test evidence is absent | Stop before publication and require sandbox deployment and test completion |
| A direct REST endpoint or payload is requested | Stop; use the existing core.fusion-api.apps-common DFF route rather than inventing task-local REST transport |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required configuration facts are missing or invalid | Collect corrected facts and restart validation |
| design_blocker | A documented DFF design or sandbox-test gate fails | Correct the configuration plan before preview or publication |
| execution_contract_gap | A task-local REST contract is requested but not documented | Route through core.fusion-api.apps-common; do not construct a direct request |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Context retirement block | State that an existing context cannot be deleted and must be disabled through its associated context value |
| Publication block | State that descriptive-flexfield changes require sandbox deployment and testing before publication |
| Route boundary | State that the task uses the existing Apps Common DFF route and has no task-local REST contract |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or failed sandbox test evidence | Do not publish the descriptive-flexfield change |
| Existing context retirement | Do not delete the context |
| No documented task-local REST contract | Do not invent an endpoint, payload, direct transport, or retry behavior |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRTDFF.DONE | terminal | 4 | terminal | none | MRTDFF.DESIGN_GUARD | stop | Documented input and design gates pass; continue through the existing Apps Common DFF route |
| MRTDFF.BLOCKED | terminal | 5 | terminal | none | none | stop | Any validation, design, sandbox-test, or execution-contract blocker occurs |
