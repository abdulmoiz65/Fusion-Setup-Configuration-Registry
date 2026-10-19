# Shifts and Schedules Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Workbook completeness | Confirm the workbook identifies the requested schedules, shifts, absences, holidays, assignments, and exceptions needed for the requested change. |
| 2 | Hierarchy and pattern design | Enforce inherited common schedules and standard repeatable shifts before allowing lower-level variations. |
| 3 | Availability and routing design | Enforce current availability, routing-versus-on-call intent, internal-work handling, absence model, and holiday precedence. |
| 4 | Capacity and lifecycle design | Enforce usable labels, active future shifts, and capacity alignment before preview. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| SS.HIERARCHY_AND_INHERITANCE | A schedule or calendar is created | Error | | A common schedule is configured independently on individual resources or low-level nodes without a true exception | Define schedules at the highest practical organization-unit or bucket level and inherit them to children; manage only genuine exceptions lower down | Yes, before preview |
| SS.AVAILABILITY_ACCURACY | A working schedule, shift, absence, or holiday is changed | Error | | Calendar availability is stale or unverified | Keep calendars accurate and current: schedule availability is a hard routing constraint alongside skills and zones | Yes, before preview |
| SS.STANDARD_SHIFT | A regular shift model is introduced | Error | | A standard repeatable pattern is duplicated across lower hierarchy levels | Establish a standard regular shift high in the hierarchy for consistent coverage and simpler maintenance | Yes, before preview |
| SS.SCHEDULE_VARIATION | Separate schedules are proposed | Error | | The variation is not a genuinely different repeatable pattern | Create separate schedules only for real differences such as rotations, regions, seasons, weekends, or materially different operating hours | Yes, before preview |
| SS.NAMING_AND_STATUS | A work schedule or shift is created or deactivated | Error | | Labels are ambiguous, non-sortable, or needed future shifts are inactive | Use clear, API-friendly labels with a consistent convention, such as WS_ prefixes. Keep required future shifts active; deactivation does not remove existing assignments | Yes, before preview |
| SS.ROUTING_VS_ON_CALL | An on-call or regular shift is proposed | Error | | On-call shifts are expected to behave as normal automatic-routing availability | Use regular shifts for normal automatic routing. Use on-call shifts for deliberate manual assignment beyond normal hours and explicitly configure their coverage | Yes, before preview |
| SS.RECURRING_INTERNAL_WORK | Lunches, breaks, meetings, or other recurring internal activities are planned | Error | | The activity is manually recreated for every resource despite applying to every assigned route | Associate recurring internal activities with the relevant shifts when they should appear automatically on every assigned resource route | Yes, before preview |
| SS.ABSENCE_MODEL | Full-day or partial-day absence is configured | Error | | Full-day absence, partial-day leave, mid-day time off, or split-shift handling is conflated | Use non-working reasons for full-day absences. Use dedicated calendar approaches for partial-day absences, mid-day time off, and split shifts | Yes, before preview |
| SS.HOLIDAY_PRECEDENCE | Holidays or inherited calendar changes are configured | Error | | Child overrides have not been reviewed | Apply holidays centrally at the parent level where appropriate, then verify child overrides because they take precedence | Yes, before preview |
| SS.CAPACITY_ALIGNMENT | Capacity display units or Points Support are configured | Error | | Capacity units do not match planning practice, or point limits permit routing beyond intended workload | Select hours, points, scheduled resources, or FTE based on the operating model. Set sensible shift-level limits when using Points Support | Yes, before preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SS.ENFORCE_DESIGN | decision | 30 | design_enforcement | passed->SS.LOOKUP_CURRENT_SHIFT_ITEMS;blocked->SS.HANDLE_ERROR | SS.VALIDATE_INPUT | stop | Before any REST lookup or preview |
