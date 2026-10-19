# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve scope | Ask all eligible addresses or specific country/other filters when unresolved; any supported filter selects parameterized and existing requestId selects tracking |
| 2 | Resolve monitoring | Ask request ID only or monitor status before preview unless the request already resolves it |
| 3 | Resolve environment | Bind the request to exactly one Fusion environment |
| 4 | Validate parameters | Normalize optional values and preserve ESS argument order |
| 5 | Verify readiness | Resolve the target environment; treat country setup and address eligibility as Fusion selection criteria, and disclose required ESS privilege |
| 6 | Summarize impact | Briefly state the target, filter scope, monitoring behavior, defaults, and regeneration impact without pausing for confirmation |
| 7 | Enforce execution intent | Treat a direct run request as authorization for exactly one POST; after scope and monitoring are resolved, submit without an Approve or Confirm prompt |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| GEOCODE.MODE.REQUIRED | Every new run | Blocker | none | Business scope is unstated and no supported filter is supplied | Ask all eligible addresses or specific country/other filters | Yes |
| GEOCODE.MONITORING.REQUIRED | Every new run | Blocker | none | Neither request ID only nor monitor status behavior can be resolved | Ask the monitoring question before preview | Yes |
| GEOCODE.MODE.EXCLUSIVE | Every run | Blocker | none | New-submission fields and requestId are combined | Choose submit or track | Yes |
| GEOCODE.ENVIRONMENT.REQUIRED | Every run | Blocker | none | Target environment is missing or ambiguous | Confirm one exact environment | Yes |
| GEOCODE.DATE.PAIR | Either date is supplied | Blocker | none | One date is missing, either value is not a real accepted date, or normalized start_date is later than normalized end_date | Supply a valid inclusive date range | Yes |
| GEOCODE.DATE.SERIALIZATION | A date range is supplied | Blocker | none | submit.argument2 or submit.argument3 is not normalized as YYYY-MM-DD | Convert UI-style dates to ISO before preview and submission | Yes |
| GEOCODE.REGENERATE.WARNING | regenerate_geocode is Y | Warning | none | Execution summary does not disclose that existing coordinates may be processed again | Add the warning before submission | Yes |
| GEOCODE.BATCH.LIMIT | batch_size is supplied | Blocker | none | Value cannot normalize to an integer from 1 through 100 | Correct or cap the value and preview again | Yes |
| GEOCODE.ONE.POST | Every new submission | Blocker | none | The execution plan contains retries or more than one POST | Submit once and retain requestId | Yes |
| GEOCODE.NO.SECOND.APPROVAL | A direct imperative authorized the run | Blocker | none | The flow pauses after preview to ask for approval or confirmation | Treat the original imperative as authorization and continue to one POST | Yes |
| GEOCODE.TRANSIENT.RUN | project_id is absent and durable output was not requested | Blocker | none | The flow creates or seeks approval for a project or audit workspace | Run without project persistence | Yes |
