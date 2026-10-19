# Manage Facility Schedule Exceptions Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Name is missing | Stop and ask only for the schedule exception name. Do not ask for ExceptionId or another technical identifier. |
| Period type, meaning, or all-day flag is invalid | Stop and correct the full-day off-period values to OFF_PERIOD, Off Period, and Y before preview. |
| Oracle rejects an exception date | Stop and replace the affected date with a literal YYYY-MM-DDTHH:MI:SS.sss+hh:mm timestamp. |
| The DAT payload contains an Excel serial date such as 46266 | Stop, rebuild the DAT with literal ISO-8601 timestamp text, validate the new archive, and obtain a new approval before submission. |
| Oracle returns a validation, authorization, transport, or process error | Preserve the redacted response and external identifier when available; stop before retry or a different execution route. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Name, full-day off-period values, or timestamp text is missing or invalid | Correct the source and revalidate |
| Fusion API | Oracle rejects the submitted schedule exception | Preserve the diagnostic and stop before retry |
| Approval blocker | A corrected archive differs from the approved archive | Generate a fresh immutable preview and obtain explicit approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCHED_EXC.HANDLE_ERROR | terminal | 30 | terminal | none | none | stop | Any input or Fusion validation failure |
| SCHED_EXC.READY | terminal | 40 | terminal | none | SCHED_EXC.VALIDATE_VALUES | stop | All documented input checks pass and the request is ready for its separately approved execution workflow |
