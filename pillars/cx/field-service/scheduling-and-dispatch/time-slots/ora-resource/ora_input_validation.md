# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Workbook input | A readable .xlsx workbook with a `Time Slots` worksheet | Stop before design validation | Provide the workbook path and a readable `Time Slots` worksheet | Always | |
| Time-slot identity | Time slot label; Name when it differs from the label | Stop before preview | Extract clear equivalents from a free-format workbook, then request only a missing or ambiguous label or name | Every proposed time slot | |
| Required time-slot configuration | Status, Start Time, End Time | Stop before preview | Extract clear equivalents from the workbook, normalize allowed time formats, then request only a missing or ambiguous value | Every proposed time slot | |
| Design-purpose evidence | Business Purpose | Stop before design enforcement and preview | Provide a specific customer-service, booking, routing, assignment-ordering, capacity, or quota-management purpose for the row | Every proposed time slot | |
| Conditional design evidence | Booking Model, Eligible Activity Types, Change Impact | Stop before preview when the corresponding design rule applies and the evidence is missing or ambiguous | Supply the applicable evidence in the Time Slots worksheet; these fields are not API payload fields | A row declares the applicable use or is an existing required slot being changed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Time Slots worksheet availability | Reject the workbook input when the Time Slots worksheet is absent or unreadable | Workbook input is supplied | |
| Labels are stable identifiers | Require each time-slot label to be unique, nonblank, and stable; reject a row whose label is ambiguous with another row | Every proposed time slot | |
| Status is normalized | Accept only Active or Inactive after normalizing the workbook value | Every proposed time slot | |
| Bounded time values are valid | Require both Start Time and End Time; accept an Excel time, `HH:MM`, or a consistent 12-hour value and reject mixed 24-hour-plus-AM/PM notation | Every proposed time slot | |
| Business purpose is documented | Reject a blank or generic Business Purpose; it must identify the operating purpose for that row | Every proposed time slot | |
| Design evidence is explicit | Preserve supplied Booking Model, Eligible Activity Types, and Change Impact as validation evidence only. Do not default them and do not map them to association APIs or the Time Slots payload | A row provides the field or the corresponding design rule applies | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.VALIDATE_WORKBOOK | step | 1 | validate_input | valid->TS.DEPENDENCIES;invalid->TS.DESIGN_BLOCKED | none | stop | Before dependency checks and design validation for a workbook-supplied Time Slots request. |
