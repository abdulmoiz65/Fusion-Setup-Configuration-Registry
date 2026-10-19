# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Payables calendar | Run the conditional read-only validation for a supplied Calendar before submission when the endpoint is available |
| 2 | Reference data set | Run the conditional read-only validation for a supplied SetCode before submission when the endpoint is available |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DEP-CALENDAR | Payables calendar | Conditional | AP_TERM_LINE.Calendar is supplied | Conditional blocker | Payables Calendar Types REST collection; query uses the supplied Calendar and `PAYMENT TERMS` predicate | validate_payables_calendar | The documented endpoint corroborates an already supplied value | One or more rows corroborate only. Zero rows block as `not_found`; malformed/unexpected responses block as `resolver_failure`. HTTP 400 is advisory; 401/403/network/timeout/5xx are `validation_skipped`. | Calendar |
| DEP-SET-CODE | Payables Payment Terms reference data set | Conditional | AP_TERM_SUBSCRIPTION.SetCode is supplied | Conditional blocker | Set ID Sets LOV REST collection | validate_set_code | The documented endpoint corroborates an already supplied value | One or more rows corroborate only. Zero rows block as `not_found`; malformed/unexpected responses block as `resolver_failure`. HTTP 400 is advisory; 401/403/network/timeout/5xx are `validation_skipped`. | SetCode |

## What These Statuses Mean

| Status | Plain Meaning | What Happens Next |
|---|---|---|
| Conditional blocker | A read-only check is required only when the related value is supplied. A readable zero-result or malformed response blocks the candidate; a documented advisory/unavailable result is retained as evidence for Fusion's later import-time validation. | Correct a blocking value or response issue before candidate generation. For an advisory/unavailable result, preserve the value and evidence; Fusion remains authoritative during approved import. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEP.CHECK | step | 20 | resolve_dependency | success->LOOKUP.CALENDAR;advisory-unavailable->LOOKUP.CALENDAR | INPUT.VALIDATE | stop | Always |
