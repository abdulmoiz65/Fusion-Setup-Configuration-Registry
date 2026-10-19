# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | Condition Event Code and Condition Event Type Code | Stop before artifact creation | Provide a unique uppercase alphanumeric code and a valid type code | Create | |
| Update identity | Condition Event Code, Condition Event Type Code, and intended changed field values | Stop before artifact creation | Provide an unambiguous code and type combination | Update or end-date | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Code format | Require an uppercase alphanumeric Condition Event Code; it must be unique within the selected type | Create | |
| Type | Require a valid Condition Event Type Code from the source data or approved lookup | Create or type change | |
| Category | When supplied, require a value accepted by lookup type ORA_MNT_EVENTCODE_CATEGORY | Create or category change | |
| Unsupported field | Reject IotIntegrationFlag | Every request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CEC.VALIDATE_CONDITION_EVENT_INPUT | step | 10 | validate_input | valid->CEC.INPUT_VALID;invalid->CEC.INPUT_INVALID | none | stop | Create, update, or end-date |
