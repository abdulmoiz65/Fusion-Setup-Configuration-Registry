# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate business inputs | Validate the schedule name and both effective dates before preview. |
| 2 | Resolve the workday pattern | Resolve the supplied PatternName through the backend resolver. |
| 3 | Enforce business-name intake | Keep PatternId internal; user interactions collect and correct names only. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A schedule workday pattern is supplied | Blocking | resolve_workday_pattern_by_name | PatternName cannot be resolved to exactly one backend pattern | Ask for a corrected or more specific workday pattern name; do not ask for PatternId | Yes |
| Any schedule create request | Blocking |  | EffectiveFromDate or EffectiveToDate is not YYYY-MM-DD | Correct the date values before creating a new preview | Yes |
| Any schedule create request | Blocking | resolve_workday_pattern_by_name | A workflow asks the user for PatternId | Remove the ID request and collect PatternName instead | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_workday_pattern_by_name | Before preview when PatternName is supplied | Backend-resolved PatternId associated with the exact PatternName | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FAC_SCH.ENFORCE_NAME_INPUT | decision | 3 | design_enforcement | compliant->FAC_SCH.DONE;blocked->FAC_SCH.HANDLE_ISSUE | FAC_SCH.RESOLVE_WORKDAY_PATTERN | stop | Create schedule after workday pattern resolution |
