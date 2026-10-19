# Development Library Goal Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| `PriorityCode` | `MEDIUM` (Medium) | REST and HDL create, only when omitted | No; preserve explicit values, validate against current `HRG_PRIORITY`, include in the approved payload/DAT and verify the stored code. Explicit null/blank is not omission. No update default. |
| `StatusCode` | `I` | Create when omitted | No; materialize it in the exact payload. Active creation requires an explicit create-active contract; otherwise activation remains separate. |
| `Visible` | `ALL` | Create when omitted | No; materialize it in the exact payload and verify returned `AvailableTo` is “HR specialist, manager, and worker” |
| omitted parent fields | Preserve fresh stored values | Update | No |
| omitted child collections | Preserve complete fresh collections | Update | No |
| variant | No default | Every request | Never infer development |
| `GoalExternalId` and `GoalId` | Omit both only when `GoalExternalId` is omitted and current metadata has `hasDefaultValueExpression=true` for both fields | Create | No; Fusion derives `GoalExternalId` from generated `GoalId`, then the response must prove equality |
| external ID without both server defaults | No default | Create | Never invent an ID; use exact `GoalName` within `TypeCode=DEVELOPMENT` duplicate controls and require duplicate-risk acknowledgement |
| development category field | Omit unless supplied or current metadata requires `DevCategoryCode` | Every create or update | No; do not invent a category code |
| TypeCode | `DEVELOPMENT` | Create and update | No; reject a mismatched caller value |

`StatusCode`, `Visible`, `TypeCode`, and `GoalName` are non-null create
invariants. A default shown in a preview but absent from its JSON payload has
not been applied and must block the preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.DEFAULTS | step | 50 | apply_default | complete->GOAL_LIBRARY.DESIGN | GOAL_LIBRARY.LOOKUPS | stop | Lookups are resolved |
