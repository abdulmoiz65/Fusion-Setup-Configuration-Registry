# Manage Grade Ladders Design Enforcement

## Purpose

Defines the blocking Grade Ladder gates evaluated before routing.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact target or confirm create availability |
| 2 | Validate dependencies | Resolve the Grade Set, Grades, Steps, and requested Rate references |
| 3 | Validate source scope | Require the base row and only requested or changed child rows |
| 4 | Decide readiness | Continue only when no blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| TARGET_IDENTITY | Read, edit, or delete requires one target | Blocking | find_manage_grade_ladders | The ladder identity is absent or ambiguous | Supply one exact identity | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_grade_ladders | An exact ladder already exists or availability is ambiguous | Supply a unique identity | Input fix |
| GRADE_SET | create | Blocking | resolve_grade_ladder_grade | GradeSetCode is unresolved or conflicts with a Grade | Resolve one compatible Grade Set | Lookup fix |
| STEP_MATRIX | Grades and Rates are supplied | Blocking | resolve_grade_ladder_steps | Steps are unordered or the Rate by Grade Step matrix is incomplete or duplicated | Correct the Steps or matrix | Input fix |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_grade_ladder_split_deletion_range | Source uses HDL `DELETE`, omits `SET PURGE_FUTURE_CHANGES Y`, would remove the logical first split, does not exactly bound future splits to remove, or the current generated Grade Ladder loader contract cannot preserve the directive | Use a `GradeLadder` `MERGE` row with the confirmed retained EffectiveStartDate and inclusive EffectiveEndDate; omit non-key attributes and stop when the live contract cannot represent the directive | Source rebuild |
| SOURCE_SCOPE | Every mutation | Blocking |  | The base row is absent or unchanged child rows are included | Keep the base row and only requested or changed children | Source fix |

| LADDER_CONFIGURATION | Create or edit | Warning |  | Referenced grades, sequence, ladder type, or activation settings are incompatible | Confirm existing grades, compatible type, and configuration before activation | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_grade_ladders | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_grade_ladder_grade | A Grade is supplied | Compatible Grade and Grade Set | ora_reference_lookups.md |
| resolve_grade_ladder_steps | A Grade is supplied | Ordered Steps, Step count, and ceiling Step | ora_reference_lookups.md |
| resolve_grade_ladder_split_deletion_range | delete-effective-split | Confirmed retained start, inclusive deletion end, and preserved predecessor values | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every blocking rule is satisfied | Continue to routing |
| not_required | No design rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLAD.ENFORCE | decision | 5 | design_enforcement | passed->GLAD.ROUTE;not_required->GLAD.ROUTE;blocked->GLAD.ERROR | GLAD.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting |
