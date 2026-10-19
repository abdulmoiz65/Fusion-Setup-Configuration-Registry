# Repeating Time Periods Reference Lookups

## Source Basis

- Generic FSM Baseline, developer-provided text, used for fresh same-task export validation.
- User-provided authoring direction, used for exact Current Name matching during edit.
- User-provided authoring direction, used to identify every exact functional match before a new period is created.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_repeating_time_periods_fsm_export | A create or edit FSM package is prepared; for edit, Current Name is provided | Fresh Repeating Time Periods FSM export archive; for edit, user-provided Current Name | Require a fresh same-task export with exact-case ASM_SETUP_CSV_METADATA.xml, task-scoped object CSV, valid keys, and approved row scope. For edit, require exactly one exported row whose current Name exactly matches Current Name. | Validated fresh export artifact; for edit, exactly one matching exported row and current values | Stop when the fresh export cannot be obtained or validated, or when Current Name matches zero or multiple rows. |
| find_functionally_matching_repeating_periods | Create after the requested UI configuration is validated and defaulted | Fresh validated Repeating Time Periods FSM export and the requested Period Usage, Period Type, applicable Period Length, Number of Days or Number of Weeks, Sample Start Date, and Start Day | Return every exported period whose period-usage and applicable period-definition values exactly match the validated requested configuration. Name and Description do not determine a functional match. | Every matching period, displayed only with populated UI-exposed values | Return no matches when none exist; stop when the fresh export cannot be obtained or validated. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A create or edit FSM package is prepared | Verify the fresh same-task export before task-specific package preparation. |
| An edit is requested | Match Current Name exactly once in the verified fresh export; use that row as the edit target. |
| A create is requested | Find every exact functional match in the verified fresh export before package preparation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RTP.VERIFY_FSM_EXPORT | decision | 30 | reference_lookup | resolved->RTP.CHECK_FUNCTIONAL_MATCHES;blocked->RTP.BLOCKED;lookup_failure->RTP.BLOCKED | RTP.APPLY_DEFAULTS | stop | A Repeating Time Periods create or edit request needs fresh export verification; edit additionally needs exact Current Name matching |
| RTP.CHECK_FUNCTIONAL_MATCHES | decision | 35 | reference_lookup | matches->RTP.CONFIRM_CREATE_AFTER_MATCHES;no_matches->RTP.CHECK_FSM_READINESS;not_applicable->RTP.CHECK_FSM_READINESS;blocked->RTP.BLOCKED | RTP.VERIFY_FSM_EXPORT | stop | Create after validation and defaulting; find every exact functional match in the fresh same-task export |
