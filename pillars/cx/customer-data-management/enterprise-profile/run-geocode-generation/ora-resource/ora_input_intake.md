# Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Direct run with unstated scope | Target Fusion environment and execution intent | Ask whether to run for all eligible addresses in geocoding-enabled countries or narrow the run |
| Monitoring selection | request_id_only or monitor_status | Required before preview for every new submission |
| Parameterless request | Target Fusion environment and execution intent | Run for eligible addresses in every country where geocoding is enabled |
| Structured request | Target Fusion environment plus any supported optional parameters | Country-scoped, date-scoped, regeneration, or tuned batch execution |
| Existing ESS request | requestId and target Fusion environment | Resume status tracking without submitting another request |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| execution_intent | Yes for a new submission | Authorize one live submission from a direct run request | No | Do not ask for a second technical approval |
| execution_mode_selection | Yes for a new submission | Select all-enabled-country or filtered intake | No | Ask the user-friendly scope question when unresolved; infer parameterized from any supported filter |
| monitoring_choice | Yes for a new submission | Select submit-only or submit-and-monitor behavior | No | Infer only when the request explicitly requests request ID only or monitoring; otherwise ask before preview |
| fusion_environment_context | Yes for submission or tracking | Bind the operation to one Fusion environment | No | Resolve exactly one configured environment |
| country | No | Restrict processing to one country | No; resolve first | Accept a country name, documented alias, common misspelling, or two-letter code and resolve it through ora_reference_lookups.md |
| country_code | No | Restrict processing to one country | Yes after resolution | Send only the resolved uppercase two-letter code |
| start_date | No | Restrict locations by HZ_LOCATIONS last update date | Yes after normalization | Pair with end_date; accept UI-style M/D/YY or MM/DD/YY and ISO YYYY-MM-DD, then serialize as YYYY-MM-DD |
| end_date | No | Restrict locations by HZ_LOCATIONS last update date | Yes after normalization | Pair with start_date; accept UI-style M/D/YY or MM/DD/YY and ISO YYYY-MM-DD, then serialize as YYYY-MM-DD |
| regenerate_geocode | No | Include already geocoded locations when Y | Yes when supplied | Normalize to uppercase Y or N |
| batch_size | No | Set the number of locations handled by each subprocess | Yes when supplied | Normalize to an integer from 1 through 100 |
| requestId | Conditional | Resume tracking of an existing request | No | Mutually exclusive with a new submission |
| wait_seconds | No | Bound status polling | No | Use a positive integer |
| poll_interval | No | Set the polling interval | No | Use a positive integer not greater than wait_seconds |
| project_id | No | Persist redacted execution artifacts only when explicitly supplied or durable output is explicitly requested | No | If absent, run transiently; do not create a draft project or audit workspace |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Direct new run does not state its scope | Ask all eligible addresses or specific country/other filters before continuing |
| User supplies a country name or code in the direct request | Infer parameterized mode and resolve the country without asking the scope question again |
| Country spelling has one uniquely high-confidence documented match | Disclose the normalized country and code, then continue without a correction-confirmation prompt |
| Country spelling is unknown or ambiguous | Ask one short clarification question with close documented candidates |
| User chooses all eligible addresses in geocoding-enabled countries | Resolve parameterless mode and omit requestParameters |
| Parameterless mode is selected | Do not ask for individual ESS parameters and omit requestParameters |
| Parameterized mode is selected | Collect at least one supported optional parameter, then validate and preview it |
| User asks to narrow the run but supplies no filters | Show the friendly optional-parameter prompt and accept `none` as parameterless |
| Monitoring choice is not stated for a new run | Ask whether to return the request ID only or monitor status here before preview and submission |
| request_id_only is selected | Submit once in submit-only mode, return requestId, and end without polling |
| monitor_status is selected | Submit once, return requestId, and poll the same request using the selected monitoring options |
| No optional geocode parameter is supplied | Omit requestParameters and let the ESS job apply its defaults |
| One or more optional parameters are supplied | Build ordered submit.argument parameters through the highest supplied position and use empty STRING placeholders for omitted earlier positions |
| UI-style dates are supplied | Parse them as calendar dates, interpret YY as 20YY, retain the user's input for disclosure, and send only normalized YYYY-MM-DD values to ESS |
| A trailing optional parameter is absent | Omit that trailing request parameter |
| An unknown parameter is supplied | Reject it before preview |
| requestId is supplied | Track the existing request and do not construct or submit a new request |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.COLLECT | step | 1 | collect_input | ok->GEOCODE.VALIDATE;failure->GEOCODE.FAILED | none | stop | Every Run Geocode Generation request |
