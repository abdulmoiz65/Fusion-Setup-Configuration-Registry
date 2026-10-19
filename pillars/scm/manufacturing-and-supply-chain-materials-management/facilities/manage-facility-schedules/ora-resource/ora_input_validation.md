# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Schedule identity | Name | Block preview | Ask for the schedule name | Create schedule |  |
| Effective period | EffectiveFromDate and EffectiveToDate in YYYY-MM-DD format | Block preview | Ask for each missing or incorrectly formatted date | Create schedule |  |
| Workday pattern selection | PatternName | Block preview | Ask for the workday pattern name; do not ask for PatternId | Create schedule with a workday pattern | resolve_workday_pattern_by_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| EffectiveFromDate matches YYYY-MM-DD | Reject any other date format before preview | EffectiveFromDate is supplied |  |
| EffectiveToDate matches YYYY-MM-DD | Reject any other date format before preview | EffectiveToDate is supplied |  |
| EffectiveFromDate is on or before EffectiveToDate | Block preview and request corrected dates | Both effective dates are supplied |  |
| PatternName is a nonblank business name | Use the exact supplied name as the lookup value; never require a user-supplied PatternId | A workday pattern is supplied | resolve_workday_pattern_by_name |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FAC_SCH.VALIDATE_INPUT | decision | 1 | validate_input | valid->FAC_SCH.RESOLVE_WORKDAY_PATTERN;invalid->FAC_SCH.HANDLE_ISSUE | none | stop | Create schedule |
