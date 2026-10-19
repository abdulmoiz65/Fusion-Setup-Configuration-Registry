# Events Input Validation

Sources: OLC-116681 FDD version 5 section OLC-120242, Oracle Learning Events
REST documentation, and the sanitized raw target Describe reviewed 2026-09-22.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Row identity | local row key; target environment; requested operation | Reject only the affected row | Assign a stable row key and obtain one exact environment and supported operation | Every row | |
| Event business identity | learningItemNumber; learningItemTitle; learningItemVisibility | Reject only the affected row | Supply the event number, title, and visibility; number and visibility are REST create requirements | Create Draft, create and activate, or copy target | |
| Existing event identity | learningItemNumber or learningItemId; current fingerprint for a mutation | Stop the affected row before preview | Resolve exactly one current event and follow its returned item link | Readback, update, copy source, lifecycle change, or activity mutation | resolve_event_identity |
| Draft intent | explicit Draft lifecycle intent; supplied parent and child fields | Default to Draft only for create | Preserve incomplete activation details as named gaps; still validate every field actually supplied | Create Draft | |
| Activation schedule | event boundary; one or more activities; activity numbers and statuses; exact dates, start and end times, time zones, and delivery modes | Block activation for the affected row | Supply a complete internally consistent activation schedule | Create and activate, activate, reactivate, or active-event reschedule | |
| Enrollment controls | event and classroom capacities; planned demand; waitlist and enrollment behavior; current enrollment evidence | Block the learner-impacting operation | Supply applicable controls and fresh metrics | Activate, reactivate, reschedule, cancel, close, capacity change, or activity delete | resolve_event_identity |
| Activity payload | activityNumber; status; operation-specific schedule and resource fields | Reject the affected activity | Supply the raw-contract mandatory fields and the fields required by the selected activity operation | Activity create or update | |
| Copy target | source event identity; new unique learningItemNumber; learningItemTitle; optional learningItemCatalogProfileNumber | Block copy | Supply the source and exact target values required by the approved copy plan | Copy | resolve_event_identity |
| Extensible attributes | WLF_LEARNING_ITEM context and exact segments returned by current target metadata | Stop extensibility processing for the affected row | Refresh live target DFF metadata and resolve each supplied segment and value | A row includes learningItemDFF values | |
| Approval evidence | immutable selected-row preview fingerprint; fresh explicit approval | Stop before mutation | Regenerate the preview and obtain approval for the exact row set | Any live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Course-linked mode is selected | Require one exact active course | Resolve the exact course before preview | resolve_event_course_linkage |
| Capacity is lower than confirmed enrollment or classroom capacity is lower than planned demand | Invalid for activation or an impact operation | Increase capacity, reduce planned demand, or use a documented learner-impact workflow | resolve_event_identity |
| An activity uses a training supplier | Require one exact active supplier | Resolve the supplier number and live status before preview | resolve_event_training_supplier |
| An activity uses an instructor | Require one exact active and available instructor | Resolve identity and the exact schedule window before activation preview | resolve_event_instructor_availability |
| An activity uses a classroom | Require one exact active and available classroom with sufficient capacity | Resolve identity, schedule window, location, and planned demand before activation preview | resolve_event_classroom_availability |
| Instructor-provider webinar delivery is selected | Require one compatible account and explicit provider-user success evidence | Resolve the account; run validation only with an approved provider request and result contract | resolve_event_virtual_classroom_account |
| An activity requests an ad hoc resource | Unsupported until an approved provider contract is supplied | Stop only that row or remove the ad hoc resource | |
| Draft omits schedule, capacity, instructor, classroom, or webinar data | Draft with activation gaps | List the gaps and keep learningItemStatus at ORA_DRAFT | |
| Event, activity, enrollment, or resource state changed after preview | Stale | Refresh the affected row and obtain new approval | resolve_event_identity |
| Lifecycle PATCH is requested | Require exact current status, live target values, required reason fields, and FDD transition eligibility | Resolve target values and the transition rule before preview | resolve_event_lifecycle_values |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is supported | Reject finalize, parent-event delete, exposed upsert, or any inferred action | Every row | |
| Event identity is present and unique | Reject a missing identity, a duplicate input number, one existing create target, or ambiguous matches | Create, copy, update, or lifecycle operation | resolve_event_identity |
| Supplied fields exist and are writable for the operation | Reject Redwood-only objective or ideal-learner fields and every undocumented or read-only write field | Any mutation | |
| Activity lies within event boundaries | Block activation or an active-event schedule change; record a Draft activation gap when the incomplete activity is retained only in Draft | Create, update, copy, activate, or reschedule | |
| Activity ordering and time zone are coherent | Reject reversed or unzoned intervals for execution; preserve only a valid incomplete Draft representation | Any supplied activity schedule | |
| Instructor is active and available | Block activation or active scheduling on an inactive instructor or non-affirmative result for the exact window | An instructor is scheduled | resolve_event_instructor_availability |
| Classroom is active, available, and large enough | Block activation or active scheduling on an inactive, unavailable, or undersized classroom | A classroom is scheduled | resolve_event_classroom_availability |
| Training supplier is active | Reject a missing, ambiguous, or inactive supplied supplier | A supplier is referenced | resolve_event_training_supplier |
| Provider account is compatible | Block provider-backed delivery when the account or provider is ambiguous or incompatible, or validation is absent, failed, or indeterminate | Instructor-provider webinar delivery is selected | resolve_event_virtual_classroom_account |
| Draft and activation are separate | A create or update never implies activation; ORA_DRAFT is explicit for Draft | Create, update, or activate | resolve_event_lifecycle_values |
| Copy has a unique target | Reject source-equals-target and any existing or ambiguous target number | Copy | resolve_event_identity |
| Preview is current | Invalidate only the stale row approval when its event, child, resource, enrollment, target, or operation fingerprint changes | Any approved mutation | resolve_event_identity |

## Multi-Row Processing Rules

| Situation | What Happens |
|---|---|
| Input contains multiple rows | Assign stable row keys and validate, resolve, preview, execute, and reconcile each row independently |
| One row is invalid or blocked | Retain its exact issues and continue read-only evaluation of unrelated rows |
| Input contains duplicate target numbers | Block every colliding row until the intended single row is identified |
| Valid and invalid rows are mixed | Preview only explicitly selected valid rows and display excluded rows with reasons |
| More than one row is approved | Submit once per row in deterministic preview order; do not claim a cross-row transaction |
| A prior row write is uncertain | Stop further writes that depend on it, refresh state, and do not replay the uncertain write |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVT.VALIDATE_INPUT | decision | 1 | validate_input | valid->EVT.CHECK_DEPENDENCIES;invalid->EVT.HANDLE_ERROR | none | stop | One or more event rows are normalized |
| EVT.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->EVT.RETURN_SUCCESS;issues->EVT.HANDLE_ERROR | EVT.EXECUTION_GATE | stop | Row-scoped validation-only evidence or mutation readback is reconciled with the approved preview |
