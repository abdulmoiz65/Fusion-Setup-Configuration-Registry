# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| validate_payables_calendar | AP_TERM_LINE.Calendar is supplied | Calendar | /fscmRestApi/resources/11.13.18.05/payablesCalendarTypes?onlyData=true&fields=calendarName,calendarType&q=calendarName='{Calendar}' and calendarType='PAYMENT TERMS' | calendarName, calendarType | One or more rows corroborate the supplied value only; do not select a row or claim uniqueness. | Submitted Calendar; returned values are corroborating evidence only. | Zero rows are `not_found` and block ZIP/import. Malformed or unexpected responses are `resolver_failure` and block. HTTP 400 is advisory; 401/403/network/timeout/5xx are unavailable/skipped. |
| validate_set_code | AP_TERM_SUBSCRIPTION.SetCode key is supplied | SetCode from the subscription alternate key | /fscmRestApi/resources/11.13.18.05/setIdSetsLOV?onlyData=true&fields=SetCode,SetName,Description&q=SetCode='{SetCode}' | SetCode, SetName, Description | One or more rows corroborate the supplied value only; do not select a row or claim uniqueness. | Submitted SetCode; returned values are corroborating evidence only. | Zero rows are `not_found` and block ZIP/import. Malformed or unexpected responses are `resolver_failure` and block. HTTP 400 is advisory; 401/403/network/timeout/5xx are unavailable/skipped. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| validate_payables_calendar returns no matching item | Stop as `not_found` before ZIP/import; preserve the supplied Calendar in failure evidence. |
| validate_payables_calendar returns HTTP 400 | Preserve the Calendar and record `validation_skipped` plus a `resolver_contract_issue` finding. Do not call the Calendar invalid or the endpoint unavailable. FSM import remains separately approved and authoritative; review the finding during implementation review. |
| validate_payables_calendar returns HTTP 401/403 or another availability error | Record `validation_skipped` with the error, endpoint, supplied Calendar, and time; continue to package generation and, if approved, the governed FSM import through `core.data-loader`. Do not substitute a proxy, UI value, or write operation. |
| validate_set_code returns no matching item | Stop as `not_found` before ZIP/import; preserve the supplied SetCode in failure evidence. |
| A response has no `items` array, a non-object item, or omits requested fields | Stop as `resolver_failure`; do not generate or import a candidate. |
| Any supporting read-only GET is unavailable | Record `validation_skipped` with the error, endpoint, supplied value, and time; continue to package generation and, if approved, the governed FSM import through `core.data-loader`. Do not use this rule when the GET derives a required package value, resolves a required key, or selects an update target. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOOKUP.CALENDAR | step | 30 | reference_lookup | success->LOOKUP.SET;unavailable->LOOKUP.SET | DEP.CHECK | stop | Calendar is supplied |
| LOOKUP.SET | step | 40 | reference_lookup | success->DEFAULT.APPLY;unavailable->DEFAULT.APPLY | LOOKUP.CALENDAR | stop | SetCode is supplied |
