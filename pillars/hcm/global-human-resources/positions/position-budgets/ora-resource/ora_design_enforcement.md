# Position Budgets Design Enforcement

## Purpose

Defines the mandatory Position Budget allocation-design gate evaluated after
the profile and Enterprise allocation dependencies. It does not perform
lookups, apply defaults, or change Enterprise configuration.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm current budget | Read one exact current budget when an existing record is targeted |
| 2 | Confirm Enterprise configuration | Retain one supported Allocate By value for create or edit |
| 3 | Validate allocation attributes | Match the proposed complete allocation attributes to Allocate By |
| 4 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| ALLOCATION_CONFIG | Create or edit | Blocking | resolve_enterprise_allocate_by | Allocate By is blank, unsupported, ambiguous, or unavailable | Resolve one supported Enterprise Allocate By value | Lookup fix |
| CURRENT_BUDGET | Edit or delete | Blocking | read_position_budget | The current Position Budget is missing or ambiguous | Resolve one exact current Position Budget | Lookup fix |
| ALLOCATION_MATCH | Create or edit | Blocking | resolve_enterprise_allocate_by | The complete budget allocation attributes do not match the resolved Allocate By value | Correct the budget attributes to the configured allocation criteria | Input fix |
| DELETE_CONFIRMATION | Delete | Blocking | read_position_budget | The refreshed budget details were not shown and explicitly confirmed | Confirm the selected budget | Input fix |

| BUDGET_PLANNING | Create or edit | Warning |  | Planning horizon, complete allocation values, or alert behavior is not confirmed | Confirm the period and values, then test budget alerts before relying on them | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_enterprise_allocate_by | Create or edit | One supported Allocate By value: Department, Location, or Department and Location | ora_reference_lookups.md |
| read_position_budget | Edit or delete | Exact current budget identity and allocation values | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared completion node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.ENFORCE_ALLOCATION | decision | 40 | design_enforcement | passed->PB.ROUTE;not_required->PB.ROUTE;blocked->PB.ERROR | PB.DEFAULTS | stop | After applicable current-budget, profile, Allocate By, and preservation rules |
