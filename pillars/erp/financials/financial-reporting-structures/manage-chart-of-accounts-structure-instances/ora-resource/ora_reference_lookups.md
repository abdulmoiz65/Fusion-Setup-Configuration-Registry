# Reference Lookups

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_chart_of_accounts | Before any FSM export, package, or create | COA Name or StructureInstanceCode | GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV?q=Name='{COA Name}' | Name, StructureInstanceId, StructureInstanceCode, StructureInstanceNumber, Description, EnabledFlag | Exactly one Name match | Existing instance identity | Stop on no result or ambiguity; compare a match before continuing |
| get_chart_of_accounts | A unique StructureInstanceId was found | StructureInstanceId | GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV/{StructureInstanceId} | Name, StructureInstanceCode, StructureInstanceNumber, Description, EnabledFlag | Exact ID | Existing instance detail | Stop if the detail response is unavailable |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.LOOKUP | decision | 4 | reference_lookup | absent->COAINS.DEFAULT;match->COAINS.DONE_MATCH | COAINS.READY | stop | Always |
