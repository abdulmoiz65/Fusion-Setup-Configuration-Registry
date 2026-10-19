# Event Group Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EventGroupCode | Copy the exact supplied EventGroupName | EventGroupCode is omitted | No; preserve an explicitly supplied code | |

The resulting code must still pass target-release attribute validation. This default does not establish permitted length or characters.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVENT_GROUP.DEFAULT_CODE | step | 2 | apply_default | applied->EVENT_GROUP.RESOLVE_REFERENCES;preserved->EVENT_GROUP.RESOLVE_REFERENCES;blocked->EVENT_GROUP.RETURN_ISSUES | EVENT_GROUP.VALIDATE_INPUT | stop | Copy EventGroupName only when EventGroupCode was omitted; otherwise preserve the user code. |

## Source

- User clarification on 2026-10-01: EventGroupCode is optional and may default to the name.
