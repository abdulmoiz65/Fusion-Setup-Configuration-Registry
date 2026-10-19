# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Intent | advisory, preview-only, on-demand submission, recurring schedule, or status tracking | Stop on ambiguity | Ask for one execution intent | Every request |  |
| Status tracking | Positive requestId and bounded execution options | Stop without submitting | Use the existing Process ID | Status tracking | read_request_dispatch_status |
| New submission | Exact environment, optional Refresh Metadata selection, optional Dispatch Job Timeout, and schedule choice | Stop before preview | Resolve the target, parameters, and schedule; use the fixed parent-job contract | On-demand submission or recurring schedule |  |
| Recurring schedule | One or more exact Oracle-supported RFC 5445 RRULEs, offset-bearing per-rule start/end values, IANA/Olson time zone, exact optional inclusions/exclusions, union behavior, and continuing-impact acceptance | Stop before preview | Resolve the complete bounded Scheduler schedule in the target task | Recurring schedule |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task identity | Require ZCH_RUN_REQUEST_DISPATCH_JOB and Customer Hub | Every request |  |
| Request ID | Require a positive integer and reject new-submission fields in the same request | Status tracking | read_request_dispatch_status |
| Technical identity | Require the fixed parent jobDefinitionId, CrmEss application, and ZCH product; reject RequestProcessJob or any inferred variant | New submission |  |
| Refresh Metadata | Accept ALWAYS, IF_NEEDED, NEVER, their exact UI labels, or an explicitly requested blank/null; default omitted input to IF_NEEDED and reject other nonblank values | New submission | resolve_refresh_metadata_policy |
| Dispatch Job Timeout | Accept whole-number text; default omitted input to 120; do not invent a minimum or maximum | New submission |  |
| Parameter contract | Require submit.argument1 followed by submit.argument2, both with paramType STRING; reject internal SYS_* or job metadata fields as user parameters | New submission |  |
| Recurrence rules | Require one or more RRULEs using SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY, or YEARLY; enforce Oracle's documented clause restrictions; preserve every approved `icalString` byte-for-byte | Recurring schedule |  |
| Recurrence bounds | Require offset-bearing ISO 8601 start/end values to seconds without fractional seconds for every recurrence, with each end after its start | Recurring schedule |  |
| Schedule envelope | Require one IANA/Olson `schedule.timezone` and top-level `executePast=false`; allow multiple recurrences plus optional ISO 8601 inclusions/exclusions; reject `scheduleId`, top-level `startTime`/`endTime`, unbounded recurrences, fractional seconds, and unsupported RRULE clauses | Recurring schedule |  |
| Authorization | Assume the current user has ZCH_RUN_TRADING_COMMUNITY_REQUEST_DISPATCH_JOB_PRIV; do not ask for confirmation or role evidence | New submission |  |
| Retry contract | Require client retries=0 and exactly one submit attempt | New submission |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.VALIDATE | decision | 10 | validate_input | tracking->RDJ.STATUS_LOOKUP;submission->RDJ.DEFAULTS;invalid->RDJ.ERROR | none | stop | Normalize intent and validate the applicable input group. |
