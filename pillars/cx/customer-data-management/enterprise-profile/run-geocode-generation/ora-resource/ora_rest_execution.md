# REST Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| core.fusion-api.ess-job-submitter | Validate, submit, poll, and resume the ESS request without duplicating transport or authentication |
| Oracle Scheduler REST requests resource | Submit and retrieve ESS request status |
| Populate Location Latitude and Longitude Information documentation | Define supported business parameters and process behavior |
| HZ-HZGEOCODER ESS metadata | Define the fixed job identifier and ordinal request-parameter mapping |

## Execution Contract

| Situation | What Happens |
|---|---|
| Parameterless execution is requested | Submit the fixed job definition without requestParameters |
| Parameterized execution is requested | Map supplied fields to submit.argument1 through submit.argument5, include empty earlier placeholders when needed, and omit unused trailing parameters |
| Direct execution intent is missing | Stop before POST |
| Request ID only execution | Invoke core.fusion-api.ess-job-submitter once in submit-only mode, return requestId, and do not poll |
| Monitor status execution | Invoke core.fusion-api.ess-job-submitter once, return requestId, and poll that same request |
| Existing requestId is supplied | Invoke the core tracking path and do not POST |
| Polling times out | Preserve the requestId and last status as nonterminal; resume later without resubmission |
| ESS completes successfully | Report terminal status and the requestId; state that the process completed without claiming every address received coordinates |
| ESS completes unsuccessfully | Persist available status, error, and ECID diagnostics and stop before retry |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Submit Populate Location Latitude and Longitude Information | POST | /ess/rest/scheduler/v1/requests |
| Track the submitted process | GET | /ess/rest/scheduler/v1/requests/{requestId} |

## ESS Request Fields

| Field | Value Source | Required Behavior |
|---|---|---|
| jobDefinitionId | Fixed task contract | Use JobDefinition://oracle/apps/ess/cdm/foundation/geographies/HZ-HZGEOCODER |
| application | Fixed task contract | Use CrmEss |
| requestParameters | Parameter mapping contract | Omit for a parameterless run; otherwise use ordered STRING arguments |
| retries | Fixed safety policy | Use zero or omit; never introduce an automatic retry |
| description | Skill execution context | Use a non-sensitive description identifying the purpose without customer data |

## Parameter Mapping

| Business Parameter | Technical Name | Type | Runtime Value |
|---|---|---|---|
| Country Code | submit.argument1 | STRING | Uppercase country_code or empty placeholder |
| Start Date | submit.argument2 | STRING | normalized start_date in YYYY-MM-DD or empty placeholder; never send the UI slash format |
| End Date | submit.argument3 | STRING | normalized end_date in YYYY-MM-DD or empty placeholder; never send the UI slash format |
| Regenerate Geocode | submit.argument4 | STRING | Y, N, or empty placeholder |
| Batch Size | submit.argument5 | STRING | Integer from 1 through 100 represented as text |

## User-Facing Execution Summary

| Step | Requirement |
|---|---|
| Environment | Show the exact target Fusion host |
| Mode | Show parameterless, parameterized, or track-existing-request |
| Monitoring | Show request ID only or monitor status, including polling options when monitoring is selected |
| Parameters | Show business parameter names, normalized values, omissions, and any Batch Size cap |
| Date normalization | When dates are supplied, show the effective YYYY-MM-DD start and end values that will be sent to ESS |
| Impact | State that the process updates latitude and longitude for eligible HZ_LOCATIONS records and can spawn child jobs |
| Regeneration warning | When Regenerate Geocode is Y, state that already populated coordinates may be processed again |
| Authorization | Treat the direct run request as authorization for one submission; do not ask for technical approval again |
| Preview behavior | Present the summary as an informational update and continue immediately; never ask for `Approve submission` after a direct run request |

## Live Pattern

| Step | Requirement |
|---|---|
| Submission | Invoke core.fusion-api.ess-job-submitter with the fixed job definition, application `CrmEss`, validated ordered parameters, and submit-only behavior when request_id_only is selected |
| Polling | Poll through the core skill using bounded wait_seconds and poll_interval only when monitor_status is selected |
| Audit | When project_id is explicitly supplied, capture environment, job definition, requestId, parameter mode, terminal or last status, and ECID; otherwise do not create a project or audit workspace |
| Timeout | Resume the same requestId; never create a replacement request because polling expired |
| Failure | Retrieve available full status through the core skill and require a new direct run request before any new submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.PREVIEW | step | 5 | preview_gate | ok->GEOCODE.AUTHORIZED;failure->GEOCODE.FAILED | GEOCODE.READINESS | stop | Emit an informational summary and continue without pausing; a direct run request plus resolved scope and monitoring must not trigger another prompt |
| GEOCODE.AUTHORIZED | decision | 6 | approval_gate | approved->GEOCODE.EXECUTE;declined->GEOCODE.REFUSED | GEOCODE.PREVIEW | stop | Internally resolve the original direct imperative as authorization for one POST; never emit an Approve or Confirm prompt; tracking is read-only |
| GEOCODE.EXECUTE | step | 7 | execution_gate | success->GEOCODE.DONE;timeout->GEOCODE.TIMEOUT;failure->GEOCODE.FAILED | GEOCODE.AUTHORIZED | stop | Submit once or track the selected existing request through core.fusion-api.ess-job-submitter |
| GEOCODE.DONE | terminal | 8 | terminal | none | GEOCODE.EXECUTE | continue | The ESS request reaches a terminal successful or warning status |
| GEOCODE.TIMEOUT | terminal | 9 | terminal | none | GEOCODE.EXECUTE | continue | The polling window ends while the request remains nonterminal |
