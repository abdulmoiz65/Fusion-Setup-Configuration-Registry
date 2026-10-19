# Courses Input Validation

Sources: OLC-116681 FDD v5 section OLC-120243, supplied raw target Describes,
and the Oracle Worker read contract reviewed 2026-09-22.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request identity | target environment; requested operation; row identifier | Stop the affected row before preview | Supply one exact environment, supported operation, and row identity | All requests | |
| Course definition | title; optional user-supplied number; visibility; explicit Draft intent; ownership when applicable; validity and renewal values when supplied | Return row-specific missing fields | Complete the minimum parent definition | Create or parent update | |
| Owner or coordinator identity | technical person ID/number, exact work email, or exact person name | Stop only the affected row when a writable technical identifier is required | Resolve exactly one person through the read-only Worker contract | A person label must become a writable identifier | resolve_course_owner |
| Course defaults | capacity, waitlist, facilitator type and number, instructor references, validity, renewal, and assignment defaults that are being changed | Stop default preparation for the affected row | Supply one internally consistent default plan | Defaults are created or changed | |
| Offering or child plan | exact referenced offering or child identity and requested relationship | Stop only the affected relationship row | Supply authoritative eligibility and exclusivity evidence | A child is added or replaced | |
| Existing course identity | exact learningItemNumber or learningItemId and current fingerprint | Stop before non-create mutation | Resolve one exact course and follow its returned item link | Duplicate check, non-create operation, or reconciliation | resolve_course_identity |
| Extensible attributes | WLF_LEARNING_ITEM plus target-confirmed segments | Stop extensibility processing | Refresh target metadata and resolve every supplied segment and value | DFF values are supplied | |
| Approval evidence | immutable row previews and fresh approval for the exact valid-row selection | Stop before mutation | Refresh applicable evidence and obtain exact approval | Any live mutation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A supplied default instructor is unresolved, inactive, or ambiguous | Invalid | Correct the instructor number or defer that row | resolve_course_default_instructors |
| A default facilitator is supplied | Lookup required | Resolve the enabled facilitator type before routing the number to an instructor or training supplier | resolve_course_facilitator_type |
| A row adds or replaces a child without authoritative eligibility or exclusivity evidence | Blocked for that row | Preserve unaffected rows; obtain an approved resolver before the relationship mutation | |
| Existing activities are returned | Current-state evidence only | Read assignment impact; do not infer eligibility for a new child | read_course_memberships |
| Course, defaults, activity, assignment, or resource evidence changed after preview | Stale | Refresh, rebuild the preview, and obtain new approval | resolve_course_identity |
| Activation or retirement is requested | Lookup required | Resolve an enabled status and FDD-valid transition | resolve_course_lifecycle_values |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Course number behavior is explicit | Accept a writable user number; reject an exact-number collision | Create | resolve_course_identity |
| FDD Draft status is explicit | Send ORA_DRAFT and reject silent acceptance of the target ORA_ACTIVE default | Create | resolve_course_lifecycle_values |
| Course defaults are internally consistent | Reject negative capacity, invalid waitlist bounds, unresolved resources, or incompatible validity/renewal values | Defaults are supplied | |
| Default instructor serialization is authoritative | Preserve the approved request representation; do not build it from courseDefaultInstructorDetails | Default instructors are changed | resolve_course_default_instructors |
| Facilitator type is enabled and supported | Reject missing, disabled, expired, ambiguous, or non-routable values | Facilitator type or number is supplied | resolve_course_facilitator_type |
| Copy parameters are exact | Require learningItemNumber, learningItemTitle, and learningItemCatalogProfileNumber; verify the returned copy is Draft | Copy | resolve_course_identity |
| New child evidence is authoritative | Reject zero, multiple, inactive, ineligible, or exclusivity-conflicting references | A child is added or replaced | |
| DFF context is portable | Reject Course-specific contexts and any segment absent from live WLF_LEARNING_ITEM metadata | DFF values are supplied | |
| Operation is supported | Permit create, update, copy, activity create/update, and status PATCH; reject parent delete, activity delete, and user-facing upsert | Any mutation | |
| Approved row selection is unchanged | Invalidate approval when a row is corrected, excluded, added, removed, or reordered | After preview | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CRS.VALIDATE_INPUT | decision | 1 | validate_input | valid->CRS.CHECK_DEPENDENCIES;invalid->CRS.HANDLE_ERROR | none | stop | One or more Courses rows are normalized |
| CRS.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->CRS.RETURN_SUCCESS;issues->CRS.HANDLE_ERROR | CRS.EXECUTION_GATE | stop | Validation or mutation evidence is reconciled with the approved row previews |
