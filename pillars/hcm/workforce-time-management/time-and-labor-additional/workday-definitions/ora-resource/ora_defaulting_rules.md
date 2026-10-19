# WorkDay Definitions Defaulting Rules

## Source Basis

- Developer-provided Workday Definition Skeleton.
- Confluence page 22040252607, WorkDay Definitions UI defaulting and payload normalization behavior.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| DayStartTime | Derived internally as 1970-01-01T&lt;supplied-time&gt;:00.000+00:00 | A non-midnight workday or overtime boundary applies | Yes | |
| EarnedBreakThreshold | 0 minutes | EarnedDayBreakRule is ORA_HWM_START_DAY or ORA_HWM_STOP_DAY and the threshold is omitted | Yes | |
| EarnedBreakThreshold | Clear the value | EarnedDayBreakRule is ORA_HWM_SPLIT_START_TIME | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WDD.APPLY_CREATE_DEFAULTS | step | 20 | apply_default | defaulted->WDD.CHECK_CREATE_DEPENDENCIES;not_applicable->WDD.CHECK_CREATE_DEPENDENCIES | WDD.RESOLVE_CREATE_EARNED_RULE | stop | A valid create request is prepared |
| WDD.APPLY_CHANGE_DEFAULTS | step | 21 | apply_default | defaulted->WDD.CHECK_CHANGE_DEPENDENCIES;not_applicable->WDD.CHECK_CHANGE_DEPENDENCIES | WDD.RESOLVE_CHANGE_EARNED_RULE | stop | A mutable existing definition is prepared for update |
