# Position Budgets Dependency Readiness

## Purpose

Defines the conditional profile, Enterprise allocation configuration, and
current Position Budget references used by Position Budgets. The task reads
existing configuration only and never enables or creates missing setup.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Position Budget identity | Resolve one current budget or confirm create availability |
| 2 | Position budgeting profile | Resolve the current position-budgeting profile value for create or edit |
| 3 | Enterprise allocation configuration | Resolve the current Allocate By value for create or edit after the feature profile is enabled |

Invoke each applicable resolver when reached and continue immediately on `ready` or `not_required`; do not pause to report a pending lookup.

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| position_budget_profile | Position budgeting enabled profile | Conditional | Position Budget create or edit | Lookup | Profile option ORA_PER_POSITION_BUDGETING_ENABLED | resolve_position_budget_profile | Permits create or edit only when exactly one current value resolves to Y | Continue only for Y; treat N, no match, ambiguity, or read failure as unresolved | Current profile value |
| enterprise_allocate_by | Enterprise Position Budget configuration | Conditional | Position Budget create or edit and the feature profile resolves to Y | Lookup | Enterprise Position Budget Configuration context | resolve_enterprise_allocate_by | Determines whether Department, Location, or both are required | Require exactly Department, Location, or Department and Location; treat blank or another value as unresolved | Resolved Allocate By value |
| position_budget_identity | Existing Position Budget | Conditional | Read, edit, or delete targets an existing Position Budget | Lookup | Position Budget resource | read_position_budget | Prevents an ambiguous or stale target | Provide one exact Position Budget selector | Resolved Position Budget identity and current values |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.VERIFY_PROFILE | decision | 20 | resolve_dependency | ready->PB.RESOLVE_ALLOCATE_BY;not_required->PB.RESOLVE_ALLOCATE_BY;needs_input->PB.ERROR;unresolved->PB.ERROR | PB.READ_POSITION_BUDGET | stop | Before Position Budget create or edit |
| PB.RESOLVE_ALLOCATE_BY | decision | 30 | resolve_dependency | ready->PB.DEFAULTS;not_required->PB.DEFAULTS;needs_input->PB.ERROR;unresolved->PB.ERROR | PB.VERIFY_PROFILE | stop | After the position-budgeting profile resolves to Y and before create or edit |
