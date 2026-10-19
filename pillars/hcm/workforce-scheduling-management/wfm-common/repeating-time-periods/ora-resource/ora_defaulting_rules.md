# Repeating Time Periods Defaulting Rules

## Source Basis

- Repeating Time Period UI Skeleton, developer-provided text file, used only for the described Start Day population behavior.
- Period Type defaulting examples, user-provided, used only for first-value default behavior.
- Fresh Repeating Time Periods FSM export and user confirmation, used for Sample Start Date CSV representation.
- User-provided direction and successful controlled FSM import, used for the parent CSV PeriodStartDate value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Period Type | The first displayed permitted Period Type value for the selected Period Usage combination | Period Type is blank after Period Usage selection; for example, Time Card plus Overtime defaults Monthly and Accrual Processing plus Overtime defaults Daily | Yes |  |
| Start Day | Populate Start Day from the selected Sample Start Date | Period Type is Weekly and Period Length is Biweekly, More than two weeks, or One week | No |  |
| Sample Start Date CSV field | ReferenceDate | A task-specific FSM package is prepared | No |  |
| Parent CSV PeriodStartDate | blank | Create FSM package for every Period Type | Yes |  |
| Edit parent and translation fields other than Name and Description | Exact values from the matched fresh-export rows | Edit FSM package | No | verify_repeating_time_periods_fsm_export |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RTP.APPLY_DEFAULTS | step | 20 | apply_default | applied->RTP.VERIFY_FSM_EXPORT;not_applicable->RTP.VERIFY_FSM_EXPORT;blocked->RTP.BLOCKED | RTP.VALIDATE_INPUT | stop | Default Period Type when blank and populate Start Day only for the documented weekly period lengths after input validation succeeds |
