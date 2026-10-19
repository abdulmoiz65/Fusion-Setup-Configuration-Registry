# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Execution intent | Direct request to run or submit geocode generation | Stop before Fusion execution | Ask one short intent question only for advisory, hypothetical, or ambiguous requests |
| New-run scope | All eligible addresses or specific country/other filters | Stop parameter collection | Ask the user-friendly scope question when the request does not resolve it |
| Monitoring behavior | monitoring_choice of request_id_only or monitor_status | Stop before preview | Ask whether to return the request ID only or monitor status here |
| Environment identity | fusion_environment_context or one unambiguous configured Fusion environment | Stop before Fusion execution | Resolve or ask for the exact environment |
| Execution selection | New submission inputs or requestId | Stop when both modes are requested | Choose either submit or track |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| The request explicitly says parameterless | Satisfied | Set execution_mode_selection to parameterless and do not collect ESS parameters |
| One or more supported ESS parameters are supplied | Satisfied | Set execution_mode_selection to parameterized without asking again |
| A direct new run does not state scope and has no supported ESS parameter | Needs input | Ask all eligible addresses or specific country/other filters |
| User chooses all eligible addresses in geocoding-enabled countries | Satisfied | Resolve parameterless and do not ask for individual ESS parameters |
| A new run has no monitoring choice | Needs input | Ask for request ID only or monitor status before preview |
| No optional geocode parameter is supplied | Satisfied | Preview a parameterless all-enabled-country run |
| country is supplied as a documented name, alias, or code | Resolve | Use country_code_reference and retain the canonical name plus uppercase code |
| country is a common misspelling with exactly one high-confidence match | Normalize | Disclose the correction and retain the canonical name plus uppercase code |
| country text has no unique high-confidence match | Needs input | Show close documented candidates and ask the user to choose one |
| Only one of start_date or end_date is supplied | Blocked | Require both dates |
| Both dates are valid after normalization and start_date is later than end_date | Blocked | Correct the date range |
| A date matches M/D/YY or MM/DD/YY and is a real calendar date | Normalize | Interpret YY as 20YY and serialize as YYYY-MM-DD |
| A date matches YYYY-MM-DD and is a real calendar date | Satisfied | Retain the ISO value |
| regenerate_geocode is Y or N after normalization | Satisfied | Continue |
| batch_size is an integer from 1 through 100 | Satisfied | Continue |
| batch_size is above 100 | Normalize | Use 100 and disclose the normalization in preview |
| requestId is supplied without new-submission parameters | Satisfied | Track that request only |

## Field Validation

| Check | What Happens |
|---|---|
| execution_mode_selection is neither parameterless nor parameterized | Reject as input_validation |
| monitoring_choice is neither request_id_only nor monitor_status | Reject as input_validation |
| parameterless is selected together with an ESS parameter | Reject as input_validation and ask the user to choose parameterized or remove the parameters |
| User asks for optional filters but then supplies none | Infer parameterless after the user replies `none` |
| country resolution does not produce exactly one documented two-letter code | Reject as input_validation and ask for an unambiguous country; do not invent a code |
| start_date or end_date is not valid M/D/YY, MM/DD/YY, or YYYY-MM-DD, or is not a real calendar date | Reject as input_validation |
| An ESS date argument still contains `/` after normalization | Reject as input_validation; never submit a slash-formatted date |
| regenerate_geocode is not Y or N | Reject as input_validation |
| batch_size is zero, negative, nonnumeric, or nonintegral | Reject as input_validation |
| wait_seconds is not a positive integer | Reject as input_validation |
| poll_interval is not positive or exceeds wait_seconds | Reject as input_validation |
| request_id_only is selected with polling overrides | Ignore neither silently; explain that polling settings apply only to monitor_status and ask which behavior is intended |
| project_id resolves outside project/{project_id} | Reject as artifact_persistence |
| New-submission inputs and requestId are both supplied | Reject as input_validation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.VALIDATE | step | 2 | validate_input | ok->GEOCODE.DEFAULTS;failure->GEOCODE.FAILED | GEOCODE.COLLECT | stop | Validate environment, mode, optional parameters, polling options, and project path |
