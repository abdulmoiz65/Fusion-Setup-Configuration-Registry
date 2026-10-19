# Performance Library Goal Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| `PriorityCode` | `MEDIUM` (Medium) | REST and HDL create, only when omitted | No; preserve explicit values, validate against current `HRG_PRIORITY`, include in the approved payload/DAT and verify the stored code. Explicit null/blank is not omission. No update default. |
| `StatusCode` | `I` | Create when omitted | No; materialize it in the exact payload. Active creation requires an explicit create-active contract; otherwise activation remains separate. |
| `Visible` | `ALL` | Create when omitted | No; materialize it in the exact payload and verify returned `AvailableTo` is “HR specialist, manager, and worker” |
| omitted parent fields | Preserve fresh stored values | Update | No |
| omitted child collections | Preserve complete fresh collections | Update | No |
| variant | No default | Every request | Never infer performance |
| external ID | Server-derived from `GoalId` only when current metadata exposes default expressions for both `GoalId` and `GoalExternalId` | Create | Preserve a supplied value. If omitted under that verified metadata contract, omit both IDs, disclose the derivation, use exact name within Performance duplicate controls, and verify the returned values match. |
| performance category field | No default | Create or update | Optional unless current tenant metadata marks `PerfCategoryCode` input-required; validate it when supplied. |
| TypeCode | `PERFORMANCE` | Create and update | No; reject a mismatched caller value |

`StatusCode`, `Visible`, `TypeCode`, and `GoalName` are non-null create
invariants. A default shown in a preview but absent from its JSON payload has
not been applied and must block the preview.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.DEFAULTS | step | 50 | apply_default | complete->GOAL_LIBRARY.DESIGN | GOAL_LIBRARY.LOOKUPS | stop | Lookups are resolved |
