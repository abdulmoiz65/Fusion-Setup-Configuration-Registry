# Manage Email Profiles Input Validation

Source: Confluence page 21768014830 and current FSM export evidence.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Required sender identity | ConfigName; SenderDisplayName; SenderEmail | Stop before archive preparation | Supply all live-UI mandatory values | A profile is created | |
| Optional reply identity | ReplyToDisplayName; ReplyToEmail | Continue blank | Supply only when needed | A profile is created | |
| Delete target | ConfigName and current exported row | Stop before archive preparation | Resolve exactly one current profile row | A profile is deleted | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Unique profile name | Require no exact ConfigName match in the current export | A profile is created | |
| FSM creation row | Use ObjectStatus ORA_ACTIVE and omit ConfigId under the supplied create contract | A profile archive is prepared | |
| FSM deletion row | Change only ObjectStatus to ORA_DELETED for the exact exported target row | A profile archive is prepared | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEP.VALIDATE_INPUT | decision | 1 | validate_input | valid->MEP.CHECK_DEPENDENCIES;invalid->MEP.HANDLE_ERROR | none | stop | A sender-profile FSM create request is evaluated |
