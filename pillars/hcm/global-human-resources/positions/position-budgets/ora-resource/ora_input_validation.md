# Position Budgets Input Validation

## Purpose

Validates required business input before any lookup or execution.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | missing | Ask for one supported operation | Every request |  |
| Read selector | Name, Code, or bounded search text | missing | Ask for one selector | get | read_position_budget |
| Create identity | Name and Code | missing | Ask for both values | create | read_position_budget |
| Budget period | BudgetPeriodStartYear | missing | Ask for one four-digit allowed year | create |  |
| Allocation value | AllocatedHeadcount, AllocatedFTE, or AllocatedAmount | missing | Ask for at least one value | create |  |
| Current target | Exact Name, Code, or selected search result | missing | Ask for one exact target | edit or delete | read_position_budget |
| Requested changes | At least one explicit supported change | missing | Ask for the intended change | edit |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A create or edit request has not resolved the position-budgeting profile to Y | Blocked | Resolve the current profile value before continuing | resolve_position_budget_profile |
| A create or edit request has no supported resolved Allocate By value | Blocked | Resolve the current Enterprise Position Budget configuration before continuing | resolve_enterprise_allocate_by |
| A read, edit, or delete target is not exactly resolved | Blocked | Provide one exact Position Budget selector | read_position_budget |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| BudgetPeriodStartYear is a four-digit current, prior, or next calendar year | Otherwise invalid | create |  |
| At least one allocation value is supplied | Otherwise invalid | create |  |
| Allocation values use valid numeric input; remove unambiguous thousands separators before handoff | Otherwise invalid | create or edit |  |
| Included Boolean or Flag values use Y or N | Otherwise invalid | create or edit |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.VALIDATE | decision | 5 | validate_input | valid->PB.READ_POSITION_BUDGET;missing->PB.ERROR;invalid->PB.ERROR;unsupported->PB.ERROR | none | stop | Every Position Budgets request |
