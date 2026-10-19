# Events Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Row and operation scope | Keep validation, dependencies, previews, approvals, writes, and results bound to one stable row key |
| 2 | Draft boundary | Permit omitted activation-only details only when the row explicitly remains Draft and every omission is disclosed |
| 3 | Schedule integrity | Validate supplied boundaries, activity order, time zones, and applicable resource evidence |
| 4 | Learner impact | Validate capacity, waitlist, enrollment, visibility, and activity-removal effects |
| 5 | Lifecycle safety | Confirm live values, writable fields, transition eligibility, and history preservation |
| 6 | Execution safety | Require a fresh fingerprint and explicit approval, one submit, and exact readback per row |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create Draft with omitted schedule, capacity, or resource details | Warning | | The row is mislabeled activation-ready or any missing activation requirement is hidden | Keep the row at ORA_DRAFT and show every activation gap | Yes |
| Create Draft with supplied malformed dates, unsupported fields, or invalid references | Blocker | | A supplied value is internally invalid, undocumented, read-only, or contradicted by lookup evidence | Correct or remove the supplied value; Draft permissiveness covers omissions, not invalid data | Yes |
| Create, update, copy, or reschedule with supplied activities | Blocker | | An interval is reversed, lacks required zone context, or lies outside supplied event boundaries | Correct the activity schedule or event boundary | Yes |
| Activation or active-event schedule change | Blocker | resolve_event_identity | Complete schedule, enrollment, capacity, current-state, or activity evidence is absent or stale | Refresh and complete all activation evidence | Yes |
| Course-linked event | Blocker | resolve_event_course_linkage | The course is missing, ambiguous, inactive, or mismatched | Select one exact active course | Yes |
| Supplier-backed activity | Blocker | resolve_event_training_supplier | A supplied supplier is missing, ambiguous, inactive, or mismatched | Select one exact active supplier | Yes |
| Instructor reference is supplied | Blocker | resolve_event_instructor_availability | The instructor is missing, ambiguous, inactive, or mismatched; for activation or active scheduling, it is unavailable or lacks a complete window | Select one exact active instructor and, when required, prove availability or correct the schedule | Yes |
| Classroom reference is supplied | Blocker | resolve_event_classroom_availability | The classroom is missing, ambiguous, inactive, or mismatched; for activation or active scheduling, it is unavailable, incorrectly located, or below planned demand | Select one exact active classroom and, when required, prove availability and capacity | Yes |
| Instructor-provider webinar account is supplied | Blocker | resolve_event_virtual_classroom_account | The account is ambiguous or incompatible; for activation or active scheduling, the approved provider request or success contract is absent or validation is not explicit success | Select one compatible account and supply the approved provider contract when validation is required | Yes |
| Ad hoc resource is requested | Blocker | | No approved global identity, inventory, quantity, or schedule-availability provider exists | Remove the resource or defer the row until the skill has an approved provider contract | Yes |
| Capacity change, activation, reschedule, cancel, close, or activity delete | Blocker | resolve_event_identity | Proposed capacity is below current enrollment, learner impact is unknown, or usage/history safety is unresolved | Correct the plan or use a documented learner-impact workflow | Yes |
| Explicit Draft, activate, reactivate, cancel, reschedule, or close | Blocker | resolve_event_lifecycle_values | A live value, required reason field, writable-field mapping, or FDD transition is absent or ineligible | Choose a documented enabled value and eligible transition | No |
| Copy | Blocker | resolve_event_identity | Source is not exact, target number is not unique, source equals target, or copy values differ from the preview | Correct source or target identity and rebuild the preview | Yes |
| Activity create, update, or delete | Blocker | resolve_event_identity | Parent or activity identity is ambiguous, the activity link was constructed rather than returned, or impact evidence is stale | Resolve exact links and current activity evidence | Yes |
| Finalize, parent-event delete, or exposed upsert | Blocker | | The requested operation is outside the approved supported contract | Select a supported operation; do not infer an alternative route | No |
| Any selected mutation row | Blocker | resolve_event_identity | Target, operation, payload intent, event or activity state, enrollment, resource evidence, or fingerprint differs from the approved preview | Refresh that row and obtain new approval | Yes |
| Multiple selected rows | Blocker | | The implementation assumes atomic batch behavior, one row's approval covers another, or an uncertain write will be retried | Submit once per independently approved row and reconcile before any dependent write | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_event_identity | Duplicate checks, existing-event or activity work, learner impact, stale-state check, and readback | Exact parent and child identity, returned links, lifecycle, schedule, capacity, metrics, usage, last-modified evidence, and fingerprint | ora_reference_lookups.md |
| resolve_event_lifecycle_values | Explicit Draft, activate, reactivate, cancel, reschedule, or close | Enabled target values, reasons, required fields, and FDD transition eligibility | ora_reference_lookups.md |
| resolve_event_course_linkage | Course-linked mode | Exact active course identity, returned link, status, and fingerprint | ora_reference_lookups.md |
| resolve_event_training_supplier | An activity supplies a training supplier | Exact supplier identity, live status, returned link, and active-state evidence | ora_reference_lookups.md |
| resolve_event_instructor_availability | An instructor is supplied | Exact identity and live status; for activation or active scheduling, complete window, affirmative availability, and fingerprint | ora_reference_lookups.md |
| resolve_event_classroom_availability | A classroom is supplied | Exact identity, live status, location, and capacity; for activation or active scheduling, complete window, planned demand, affirmative availability, and fingerprint | ora_reference_lookups.md |
| resolve_event_virtual_classroom_account | An instructor-provider webinar account is supplied | Exact account, compatible states, and provider type; for activation or active scheduling, supplied validation contracts, explicit success evidence, and fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVT.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->EVT.EXECUTION_GATE;blocked->EVT.HANDLE_ERROR | EVT.APPLY_DEFAULTS | stop | After applicable inputs, dependencies, lookups, and defaults are evaluated per row |
