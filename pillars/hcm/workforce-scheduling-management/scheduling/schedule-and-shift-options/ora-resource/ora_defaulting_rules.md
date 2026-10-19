# Schedule and Shift Options Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ParameterValueArray | Convert an existing comma-delimited server value to a UI Set; join selected values with commas on update | CONTENT_TYPE or WORKER_SEARCH_FIELDS is displayed or updated | Yes | |
| ParameterValueNumber | Convert the existing server value to a number; copy the supplied normalized number to ParameterValue on update | NUMBER_SCHEDULE_PERIOD, MAX_EDITABLE_PAST_SCHEDULE_PERIODS, or WHEN_TO_SEND_RULES_NOT_MET_ALERT is updated | Yes | |
| Shift-change timing | Derive hours as floor(ParameterValue divided by 60) and minutes as the remainder; recombine to total minutes on update | A shift-change timing parameter is displayed or updated | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSO.DEFAULTS | step | 6 | apply_default | applied->SSO.DESIGN;not_applicable->SSO.DESIGN | SSO.LOOKUP.COMMON | stop | A UI-normalized value is supplied |
