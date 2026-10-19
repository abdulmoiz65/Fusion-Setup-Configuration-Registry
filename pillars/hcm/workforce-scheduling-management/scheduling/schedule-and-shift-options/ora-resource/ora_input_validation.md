# Schedule and Shift Options Input Validation

## Source Basis

- Schedule and Shift Options UI Skeleton, developer-provided
- Schedule and Shift Options Technical Design Document for FSCR, Confluence page 21805560036

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Setup option identity | SetupParamId, ParameterCode, current ParameterValue | Stop | Load and select exactly one current setup-option row | Any update request | resolve_current_schedule_common_setups |
| Required scheduling values | NUMBER_SCHEDULE_PERIOD, RESPONSIBILITY_TYPE, SKILL_TYPE | Stop | Provide valid values for each required parameter | The corresponding parameter is updated | resolve_setup_option_common_lookup |
| Content Type | CONTENT_TYPE | Stop | Provide one or more Content Type values | CONTENT_TYPE is updated | resolve_content_type |
| Shift-change timing | At least one of the relevant hours or minutes values | Stop | Provide a positive hours or minutes value | Cover, Drop, On-call Swap, or Regular Swap timing is updated | |
| Self-scheduling alert | WHEN_TO_SEND_RULES_NOT_MET_ALERT | Stop | Provide a whole number from 1 through 96 | The alert timing is updated | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| NUMBER_SCHEDULE_PERIOD | Accept a whole number from 1 through 20 | NUMBER_SCHEDULE_PERIOD is updated | |
| MAX_EDITABLE_PAST_SCHEDULE_PERIODS | Accept a whole number from 0 through 10 | MAX_EDITABLE_PAST_SCHEDULE_PERIODS is updated | |
| Alert timing | Accept a whole number from 1 through 96 | WHEN_TO_SEND_RULES_NOT_MET_ALERT is updated | |
| Hours | Accept a nonnegative whole number | A shift-change hours field is supplied | |
| Minutes | Accept a whole number from 0 through 59 | A shift-change minutes field is supplied | |
| Shift-change timing pair | Reject when both hours and minutes are null or non-positive | A shift-change timing parameter is updated | |
| Required lookup values | Reject a blank or unresolved Responsibility Type, Skill Type, Partial Shift Swap, or Flexible Duration Shift Swap value | The corresponding parameter is updated | resolve_setup_option_common_lookup |
| Worker Search Fields mandatory state | Allow an empty WORKER_SEARCH_FIELDS selection | WORKER_SEARCH_FIELDS is updated | |
| Worker Search Fields selection limit | Reject more than four selected values | WORKER_SEARCH_FIELDS is updated | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSO.VALIDATE | step | 1 | validate_input | valid->SSO.DEPENDENCIES;invalid->SSO.ERROR | none | stop | Always |
