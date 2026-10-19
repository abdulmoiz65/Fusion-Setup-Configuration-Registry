# Manage Hold Codes Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveStartDate | Current UTC calendar date in YYYY-MM-DD format | A new hold omits the start date | No | |
| ApplyHoldRoleEligibility | A | A new hold omits the value | Yes | |
| ReleaseHoldRoleEligibility | A | A new hold omits the value | Yes | |
| OrchestrationApplicationId | 10008 for Order Management | The requester does not provide an application identifier | Yes | |
| SystemFlag | false | Every new hold | No | |
| HoldCodeId | Backend-generated; omit from the create parent record | Every new hold | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HOLD_CODES.APPLY_DEFAULTS | step | 20 | apply_default | defaulted->HOLD_CODES.RESOLVE_SET;default-failed->RETURN_ISSUES | HOLD_CODES.VALIDATE_INPUT | stop | A new hold has passed input validation. |
