# Shifts and Schedules Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_work_schedule_by_label | ora_rest_execution is selected after workbook validation | Work Schedule Label | /api/field-service/configuration/v1/workSchedules/{label} | label, name, active | Retain the current parent baseline; a 404 is the conditional-create baseline | Current parent values | Multiple or malformed resolutions block preview |
| find_shift_by_label | After the work-schedule lookup | Shift Label | /api/field-service/configuration/v1/shifts/{label} | label, name, active, type, points, workTimeStart, workTimeEnd | Retain the current parent baseline; a 404 is the conditional-create baseline | Current parent values | Multiple or malformed resolutions block preview |
| find_work_schedule_items_by_label | After parent lookups | Work Schedule Label | /api/field-service/configuration/v1/workSchedules/{label}/items | itemId, type, shiftLabel, nonWorkingReasonLabel, startDate, endDate, repeatType, repeatDays | Retain the item collection as an immutable preview baseline | Current item values | A missing item collection blocks item planning after parent creation fails or is unverified |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| data_loader_execution is selected | The REST baseline lookup is not run; Core Data Loader selects its own documented read-only metadata checks. |
| ora_rest_execution is selected | GET parents first, then GET the work-schedule item collection; do not use stale workbook values as a substitute for a current baseline. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SS.LOOKUP_CURRENT_SHIFT_ITEMS | step | 40 | reference_lookup | found->SS.READY;not_applicable->SS.READY;blocked->SS.HANDLE_ERROR | SS.ENFORCE_DESIGN | stop | Before preview; resolve/create candidates for work schedules and shifts before work-schedule item baselines |
