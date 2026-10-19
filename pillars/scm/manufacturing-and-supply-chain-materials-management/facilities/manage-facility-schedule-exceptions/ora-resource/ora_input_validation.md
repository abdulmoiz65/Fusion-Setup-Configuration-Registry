# Manage Facility Schedule Exceptions Input Validation

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Schedule exception name | Require Name. Ask only for the business name; do not ask the user for ExceptionId or any other technical identifier. | Always |  |
| Full-day off-period lookup value combination | For a full-day off period, require PeriodTypeCode=OFF_PERIOD, PeriodType=Off Period, and AllDayFlag=Y. | A full-day off-period exception is requested |  |
| Exception timestamp format | Require ExceptionStartDate and ExceptionEndDate as literal timestamp strings in YYYY-MM-DDTHH:MI:SS.sss+hh:mm format. | A start or end date is supplied |  |
| Full-day UTC timestamp value | For a full-day exception on 1 September 2026 using UTC, require 2026-09-01T00:00:00.000+00:00 for both ExceptionStartDate and ExceptionEndDate. | The requested exception date is 1 September 2026 and the user selects +00:00 |  |
| Excel serial date rejection | Reject Excel serial values such as 46266 in either exception timestamp field. Preserve literal ISO-8601 timestamp text in the DAT payload. | A DAT payload is prepared |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCHED_EXC.VALIDATE_INPUT | step | 10 | validate_input | valid->SCHED_EXC.VALIDATE_VALUES;invalid->SCHED_EXC.HANDLE_ERROR | none | stop | Before creating a schedule exception through Data Loader |
| SCHED_EXC.VALIDATE_VALUES | step | 20 | validate_input | valid->SCHED_EXC.READY;invalid->SCHED_EXC.HANDLE_ERROR | SCHED_EXC.VALIDATE_INPUT | stop | A full-day off-period schedule exception is requested |
