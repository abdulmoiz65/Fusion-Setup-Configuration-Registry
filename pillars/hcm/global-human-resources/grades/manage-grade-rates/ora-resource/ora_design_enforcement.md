# Manage Grade Rates Design Enforcement

## Purpose

Defines the blocking Grade Rate gates evaluated before routing.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact target or confirm create availability |
| 2 | Validate dependencies | Resolve the LDG, Grade, lookup, and currency references |
| 3 | Validate source scope | Require the base row and only requested or changed value rows |
| 4 | Decide readiness | Continue only when no blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| TARGET_IDENTITY | Read, edit, or delete requires one target | Blocking | find_manage_grade_rates | The rate identity is absent or ambiguous | Supply one exact identity | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_grade_rates | An exact rate already exists or availability is ambiguous | Supply a unique identity | Input fix |
| PARENT_KEY | Every mutation | Blocking | resolve_grade_rate_ldg | The parent key is incomplete or mixes LDG name and ID | Use one complete Core-selected parent key | Source fix |
| VALUE_ROWS | GradeRateValue is included | Blocking | resolve_grade_rate_grade | A child key differs from the parent or its amount shape is invalid | Correct the child key or amounts | Input fix |
| RATE_OBJECT_ID | GradeRateValue is included | Blocking | resolve_grade_rate_grade | The workflow requests or accepts RateObjectId as end-user input, or neither the resolved GradeCode and SetCode user key nor a freshly resolved internal GradeId is available | Use GradeCode with SetCode by default; if Core Data Loader selects the internal-ID alternative, derive RateObjectId only from the resolved GradeId | Lookup or source fix |
| SOURCE_SCOPE | Every mutation | Blocking |  | The base row is absent or an unchanged GradeRateValue row is included | Keep the base row and only requested or changed value rows | Source fix |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_grade_rate_split_deletion_range | Source uses HDL DELETE, omits `SET PURGE_FUTURE_CHANGES Y`, would remove the logical first split, does not exactly bound future splits to remove, or includes GradeRateValue rows | Use a `Grade Rate` MERGE row with the confirmed retained EffectiveStartDate and inclusive EffectiveEndDate; omit non-key attributes and all GradeRateValue rows | Source fix |

| RATE_ASSOCIATION | Create or edit | Warning |  | Grade rate name is unclear or its grade or ladder association is not confirmed | Use a meaningful name and confirm the intended association | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_grade_rates | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_grade_rate_ldg | create or LDG validation | LDG name, ID, legislation, and default currency | ora_reference_lookups.md |
| resolve_grade_rate_grade | A value row is supplied | One active effective Grade, GradeCode, SetCode, and internal GradeId | ora_reference_lookups.md |
| resolve_grade_rate_split_deletion_range | A future effective split deletion is requested | Confirmed retained start, inclusive deletion end, predecessor values, and future GradeRateValue rows | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every blocking rule is satisfied | Continue to routing |
| not_required | No design rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRAT.ENFORCE | decision | 5 | design_enforcement | passed->GRAT.ROUTE;not_required->GRAT.ROUTE;blocked->GRAT.ERROR | GRAT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting |
