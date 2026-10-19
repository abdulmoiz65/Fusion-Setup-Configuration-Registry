# Shifts and Schedules Input Validation

## Required Input Groups

| Input Group | Mandatory | Accepted Fields | If Missing | How to Resolve | Next Action |
|---|---|---|---|---|---|
| Filled workbook template | Yes | A readable end-user-completed XLSX workbook containing the Work Schedules sheet | The workbook or the Work Schedules sheet is absent | Provide the filled workbook template and use its Work Schedules worksheet as the task input | Stop before design validation |
| Execution direction | No | data_loader_execution or ora_rest_execution | An unrecognized direction is supplied | Omit the value for data_loader_execution or explicitly select ora_rest_execution | Stop before route selection |
| Work schedule rows | Yes | Name, Label, Active, and any assignment or exception information needed by the requested change | A proposed schedule cannot be identified or its active state is absent | Complete the applicable Work Schedules row and identify the target organization unit, bucket, resource, or exception | Correct the workbook before preview |
| Shift rows | Conditional | Work Schedule, Name, Label, Active, Type, Start time, End time, and Points when the shift is capacity constrained | A proposed shift omits its schedule, identity, active state, type, or working hours | Complete the corresponding Shifts section row | Correct the workbook before preview |
| Work-schedule item REST payload | Yes for REST preview or execution | `work_schedule_label`, `itemId`, `type`, `shiftLabel` or `nonWorkingReasonLabel`, `startDate`, `endDate` when applicable, and repeat fields | A completed template does not provide documented fields or an item has no positive `itemId` | Correct the filled template; do not infer labels, IDs, or recurrence values | Block REST preview and execution |

## Input Validation Rules

| Rule ID | Applies When | Validation | What Happens | Resolver |
|---|---|---|---|---|
| SS.VALIDATE_WORKBOOK | Every request | Filled workbook template intake and applicable Work Schedules and Shifts rows are present and readable | Missing or incomplete workbook data returns issues before design enforcement | |
| SS.VALIDATE_EXECUTION_DIRECTION | Every request | `execution_direction` is omitted, `data_loader_execution`, or `ora_rest_execution` | Any other value blocks route selection; omission is defaulted by SS.SELECT_EXECUTION_DIRECTION | |
| SS.VALIDATE_REST_PAYLOAD | REST preview or execution is requested | Parent work schedules and shifts plus documented work-schedule item paths, identities, and payload fields are complete and valid | Missing parent labels, conditional item labels, recurrence fields, or `itemId` blocks the request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SS.VALIDATE_INPUT | step | 20 | validate_input | passed->SS.ENFORCE_DESIGN;blocked->SS.HANDLE_ERROR | SS.SELECT_EXECUTION_DIRECTION | stop | Every workbook-backed request |
