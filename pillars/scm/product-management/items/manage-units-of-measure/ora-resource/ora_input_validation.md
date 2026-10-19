# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Unit of measure identity | UOMClass or UOMClassName, UOMCode, UOM | Stop before lookup | Provide the class, code, and name for the unit of measure | Operation is Create or Update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| UOM class Title Case | Warn when UOMClass is not Title Case; continue to the class lookup | UOMClass is supplied | |
| UOM code length | Reject when UOMCode exceeds 3 characters | UOMCode is supplied | |
| UOM name length | Reject when UOM exceeds 25 characters | UOM is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOM.VALIDATE-INPUT | step | 10 | validate_input | valid->UOM.LOOKUP-CLASS;warning->UOM.LOOKUP-CLASS;invalid->UOM.HANDLE-INPUT-ERROR | none | stop | Always |
