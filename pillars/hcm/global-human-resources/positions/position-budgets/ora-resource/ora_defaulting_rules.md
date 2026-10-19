# Position Budgets Defaulting Rules

## Purpose

Declares that Position Budgets has no task-level business-value defaults.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied | Preserve it | preserved |
| 2 | No explicit value is supplied | Apply no default | not_required |

## Standard Defaults

None. Do not default Name, Code, BudgetPeriodStartYear, allocation values,
Department, Location, or Allocate By.

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Explicit valid value | A supported value is supplied | Preserve it after validation | preserved |
| Omitted edit value | An edit omits an existing value | Leave it omitted from the sparse change | not_required |
| Resolved reference | A lookup supplies an ID or Allocate By | Use it as resolved evidence, not a default | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.DEFAULTS | decision | 35 | apply_default | preserved->PB.ENFORCE_ALLOCATION;not_required->PB.ENFORCE_ALLOCATION | PB.RESOLVE_ALLOCATE_BY | stop | After applicable reads and dependencies are complete |
