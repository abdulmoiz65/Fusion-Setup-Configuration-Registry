# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_workday_pattern_by_name | PatternName is supplied for a schedule workday pattern | PatternName | TBD: backend resolver contract is not documented | PatternId and PatternName | Resolve exactly one backend workday pattern using the supplied PatternName | PatternId: backend-resolved PatternId; PatternName: supplied PatternName | Stop preview, retain the name-based lookup failure, and ask for a corrected pattern name; do not ask the user for an ID |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A workday pattern name is supplied | Send the exact PatternName through the backend name resolver and allow the backend to populate PatternId internally. |
| The resolver returns no match or many matches | Stop before preview and request a corrected or more specific pattern name. |
| The backend resolver contract is unavailable | Treat the lookup contract as TBD and do not replace it with a direct ID request or a guessed REST path. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FAC_SCH.RESOLVE_WORKDAY_PATTERN | decision | 2 | reference_lookup | resolved->FAC_SCH.ENFORCE_NAME_INPUT;unresolved->FAC_SCH.HANDLE_ISSUE;ambiguous->FAC_SCH.HANDLE_ISSUE;failed->FAC_SCH.HANDLE_ISSUE | FAC_SCH.VALIDATE_INPUT | stop | Create schedule with a workday pattern |
