# Courses Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target contract | Use the matching raw Describe for methods, finders, writable fields, copy, children, defaults, lookup routes, and DFF context |
| 2 | Current course and person state | Resolve exact course and any required owner, instructor, or facilitator identities |
| 3 | New child eligibility | For only rows that add or replace a child, require authoritative eligibility and exclusivity evidence |
| 4 | Lifecycle readiness | Resolve current assignments, live status values, and FDD transitions before activation or retirement |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CRS-DEP-READ-CONTRACT | learningCourses target read schema | Yes | Identity, validation, preview, or reconciliation | Satisfied | Supplied raw target Describe: 15 nodes, 307 attributes, 46 LOV-decorated attributes, 252 queryable attributes | | Exact finders, fields, children, links, defaults, and lookup routes are confirmed for the described target | Refresh after a target or release change | Identity, fields, child resources, lookup routes, defaults, and WLF_LEARNING_ITEM |
| CRS-DEP-WRITE-CONTRACT | learningCourses write and copy contract | Yes | Create, update, copy, activate, or retire | Satisfied | Supplied raw target Describe declares POST, PATCH, and exact copy action | | Supported writes and copy parameters are known; parent/activity DELETE is absent and upsert is not exposed | Select an explicit supported operation | Method/action, writable fields, parameters, and returned item link |
| CRS-DEP-IDENTITY | Existing course identity and duplicate evidence | Conditional | Create collision check or non-create operation | Lookup | Exact target finders and returned item links | resolve_course_identity | Identity must not rely on title or a manufactured opaque hash | Supply an exact number or technical ID | Exact identity, current state, item link, and fingerprint |
| CRS-DEP-OWNER | Owner or coordinator person identity | Conditional | A person label must become a writable identifier | Lookup | Oracle Workers or Public Workers read contract | resolve_course_owner | Display labels may be ambiguous and are not writable technical identities | Prefer person ID/number or exact work email | Person ID, person number, display name, and evidence |
| CRS-DEP-DEFAULT-INSTRUCTORS | Default instructors | Conditional | One or more instructors are supplied or changed | Lookup | Supplied learningInstructors Describe and ORA_WLF_LI_STATUS lookup | resolve_course_default_instructors | Every instructor must resolve exactly and be active | Supply exact instructor numbers and an approved request representation | Instructor identities, status evidence, links, and readback values |
| CRS-DEP-FACILITATOR-TYPE | Default facilitator type | Conditional | Facilitator type or number is supplied | Lookup | Course commonLookupsLOV for ORA_WLF_FACILITATOR_TYPE | resolve_course_facilitator_type | The enabled meaning selects the owning resource | Supply an exact type and number | Enabled code, meaning, and routing category |
| CRS-DEP-FACILITATOR | Default facilitator reference | Conditional | A facilitator number is supplied | Lookup | Supplied learningInstructors or learningTrainingSuppliers Describe selected by facilitator type | resolve_course_default_facilitator | Instructor and Training Supplier identities have different authorities | Resolve the type first and then one exact active number | Facilitator type, ID, number, name/title, status, and link |
| CRS-DEP-MEMBERSHIP | Current activities and assignment impact | Conditional | Existing course validation, update, activation, copy, or retirement | Lookup | Confirmed activities child, metrics, whereUsed, and changeRequests | read_course_memberships | Current impact must be refreshed, but it is not new-child eligibility evidence | Resolve the current course before preview | Membership, assignments, schedule, metrics, usage, and change-request state |
| CRS-DEP-CHILDREN | New child eligibility and course-versus-path exclusivity | Conditional | A row adds or replaces an offering or child | Blocked | No authoritative catalog-item eligibility and exclusivity resolver is available in the approved source set | | Current activities do not establish eligibility or exclusivity | Defer that row or supply an approved resolver contract; unaffected rows may continue | Exact child identity, status, type, eligibility, and exclusivity evidence |
| CRS-DEP-LIFECYCLE | Lifecycle value and transition | Conditional | Activate or retire | Lookup | commonLookupsLOV for ORA_WLF_ELEARNING_STATUS plus FDD transition rules | resolve_course_lifecycle_values | Current enabled values and transition eligibility must be live-validated | Resolve before preview | Current status, target status, enabled evidence, and transition |
| CRS-DEP-EXTENSIBILITY | Target DFF segments | Conditional | DFF values are supplied | Verify | Raw Describe confirms WLF_LEARNING_ITEM; live target metadata supplies segments | | Course-specific contexts and environment-specific segment names are not portable | Resolve exact current segments and values | Context, segment identifier, and value |
| CRS-DEP-DATALOADER | Data Loader BC REST registration and operation | Yes | Any create or update mutation | Lookup | Current core.data-loader business-object registration, template, component, attribute, and operation metadata | resolve_course_loader_registration | Taxonomy mapping and REST availability do not prove a current loader registration or operation | Correct the learningCourses registration or use only an explicitly documented Direct REST exception whose loader operation is proven unsupported | Registration discriminator, exact business object, template, components, attributes, selected operation, and metadata fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All dependencies applicable to the selected rows and operation are exact | Read-only lookups may run; mutation still requires approval |
| Row Blocked | A dependency applies to only some rows | No for those rows; unaffected valid rows may continue |
| Operation Blocked | A required contract, lifecycle, assignment, or approval condition is unresolved | No for that operation |
| Not Required | A conditional dependency does not apply | No lookup needed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CRS.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->CRS.RESOLVE_REFERENCE;not_required->CRS.RESOLVE_REFERENCE;blocked->CRS.HANDLE_ERROR | CRS.VALIDATE_INPUT | stop | Applicable dependencies are evaluated per selected Course row |
