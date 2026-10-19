# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm impact | Disclose the all-eligible-request scope and the documentation-versus-source status difference. |
| 2 | Confirm identity | Require the fixed parent ESS identity; reject the child job. |
| 3 | Confirm parameters | Require ordered submit.argument1 and submit.argument2 STRING values, including defaults or explicit overrides. |
| 4 | Confirm schedule | Distinguish one on-demand submission from an ongoing recurring schedule. |
| 5 | Confirm approval | Bind approval to the exact target, payload, schedule, and impact. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| New submission | Error |  | Payload differs from RequestDispatchJob / CrmEss / ZCH or selects RequestProcessJob | Restore the fixed parent-job identity | Yes |
| New submission parameters | Error |  | Parameter names/order/type differ from submit.argument1 STRING then submit.argument2 STRING; argument1 is unsupported; or argument2 is not whole-number text | Restore the validated/defaulted two-parameter contract and rebuild the preview | Yes |
| Every submission | Error |  | Preview implies one selected resolution request or omits the all-eligible-request impact and documentation-versus-source status difference | Disclose the scope and both status descriptions | Yes |
| Recurring schedule | Error |  | An exact RRULE, offset-bearing start date/time, later end date/time, IANA/Olson time zone, exact optional inclusion/exclusion, schedule object, union disclosure, or continuing-impact approval is missing | Complete and reapprove the bounded schedule preview | Yes |
| Recurring schedule shape | Error |  | A frequency is outside SECONDLY through YEARLY; no recurrence exists; executePast is not false; scheduleId or top-level startTime/endTime is present; a recurrence is unbounded; timestamps use fractional seconds; or an RRULE violates an Oracle restriction | Restore the supported bounded general Scheduler shape | Yes |
| Submission | Error |  | Preview changed, approval is absent, retries is not zero, or more than one POST is proposed | Rebuild the immutable preview and obtain fresh approval | Yes |
| Setup-data route | Error |  | FSM, CSV export/import, or Core Data Loader is selected | Use only the ESS route | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.ENFORCE | decision | 40 | design_enforcement | pass->RDJ.READY;fail->RDJ.ERROR | RDJ.DEPENDENCIES | stop | Before presenting a submission as execution-ready. |
