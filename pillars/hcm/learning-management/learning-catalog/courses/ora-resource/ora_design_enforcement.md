# Courses Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Definition integrity | Validate identity, explicit Draft status, ownership, visibility, validity, and renewal |
| 2 | Default-resource integrity | Resolve instructors, facilitator type, facilitator identity, and approved serialization |
| 3 | Membership and relationship integrity | Refresh current assignments and block only unresolved new-child rows |
| 4 | Lifecycle safety | Validate activation, copy readback, retirement, stale-state, and approval gates |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create | Blocker | resolve_course_identity | A supplied number collides or the request does not explicitly send validated ORA_DRAFT | Choose a unique number and an enabled Draft value | Yes |
| Owner or coordinator label | Blocker | resolve_course_owner | The label does not resolve to exactly one target-visible person | Supply a technical person ID/number or exact work email | Yes |
| Default instructors | Blocker | resolve_course_default_instructors | Any instructor is missing, ambiguous, inactive, or the write lacks authoritative serialization | Select exact active instructors and preserve the approved representation | Yes |
| Default facilitator type | Blocker | resolve_course_facilitator_type | Type is missing, ambiguous, disabled, expired, or unsupported | Select one current enabled Instructor or Training Supplier type | Yes |
| Default facilitator | Blocker | resolve_course_default_facilitator | The number does not resolve to one active resource of the validated type | Supply one exact active reference | Yes |
| A row adds or replaces a child | Blocker | | Eligibility or course-versus-path exclusivity evidence is unavailable | Defer the row or provide an approved resolver | Yes |
| Activate | Blocker | resolve_course_lifecycle_values | No valid learning option exists, current assignment impact is unresolved, or target status/transition is invalid | Complete readiness and refresh current membership before approval | Yes |
| Copy | Blocker | resolve_course_identity | Required action parameters are incomplete or Draft readback is not verified | Correct the parameters and reconcile the returned copy | Yes |
| Retire | Blocker | resolve_course_lifecycle_values | Assignment impact or enabled transition evidence is unresolved | Refresh impact and resolve the live transition | Yes |
| Parent or activity delete | Blocker | | DELETE is absent from the corresponding raw contract | Do not execute deletion | No |
| DFF attributes | Blocker | | Context is not WLF_LEARNING_ITEM or a segment is absent from live target metadata | Use only target-confirmed portable metadata | Yes |
| Any approved row | Blocker | | Environment, row selection, course, resource, membership, assignment, or lifecycle fingerprint changed | Rebuild the preview and obtain new approval | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_course_identity | Duplicate check, existing course, copy readback, or reconciliation | Exact identity, item link, Draft readback, last-modified evidence, and fingerprint | ora_reference_lookups.md |
| resolve_course_owner | A person label must become a writable identity | Exact person ID/number, display evidence, and match count | ora_reference_lookups.md |
| resolve_course_default_instructors | Default instructors are supplied or changed | Exact identities, enabled statuses, links, and approved serialization evidence | ora_reference_lookups.md |
| resolve_course_facilitator_type | Facilitator type or number is supplied | Enabled code, meaning, and routing category | ora_reference_lookups.md |
| resolve_course_default_facilitator | Facilitator number is supplied | Type-routed identity, active status, and returned link | ora_reference_lookups.md |
| resolve_course_lifecycle_values | Draft create, activation, or retirement | Current status, enabled target status, and transition evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CRS.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->CRS.EXECUTION_GATE;blocked->CRS.HANDLE_ERROR | CRS.APPLY_DEFAULTS | stop | Validated rows have completed applicable dependencies, lookups, and defaults |
