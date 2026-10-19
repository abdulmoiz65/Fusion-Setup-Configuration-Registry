# Events Dependency Readiness

Dependency readiness is evaluated per event row. A conditional blocker affects
only a row that requests that dependency; it does not make the Events task or
unrelated Draft rows unavailable.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Target capability | Use only confirmed learningEvents GET, POST, PATCH, copy, and activity contracts; reject parent deletion, finalization, and exposed upsert |
| 2 | Current event state | Resolve exact identity and applicable lifecycle, schedule, capacity, activity, metric, usage, and last-modified evidence |
| 3 | Lifecycle values | Resolve enabled values from exact commonLookupsLOV routes and apply FDD transition rules before lifecycle PATCH |
| 4 | Course linkage | Resolve one exact active course when course-linked mode is selected |
| 5 | Supplier and instructor | Resolve exact active supplier and instructor identities and schedule-aware instructor availability when requested |
| 6 | Classroom | Resolve exact active classroom identity, location, availability, and sufficient capacity when requested |
| 7 | Virtual classroom | Resolve a compatible provider account and use the validation action only with an approved provider-specific contract |
| 8 | Ad hoc resources | Stop only a row requesting an ad hoc resource until an authoritative identity and availability provider is supplied |
| 9 | Extensibility | Use only WLF_LEARNING_ITEM and exact segments from current target metadata |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| EVT-DEP-DATALOADER | Data Loader BC REST registration and operation | Yes | Any create or update mutation | Lookup | Current core.data-loader business-object registration, template, component, attribute, and operation metadata | resolve_event_loader_registration | Taxonomy mapping and REST Describe do not prove a current loader registration or operation | Correct the learningEvents registration or use only an explicitly documented Direct REST exception whose loader operation is proven unsupported | Registration discriminator, exact business object, template, components, attributes, selected operation, and metadata fingerprint |
| EVT-DEP-ROUTE | learningEvents capability | Yes | Every row | Satisfied | Public Oracle REST guidance plus sanitized raw target Describe with 21 nodes, 365 attributes, 56 LOV-decorated attributes, and 283 queryable attributes | | Supported methods, exact finders, copy, activity CRUD, required/defaulted fields, and LOV routes are confirmed | Select only a documented operation | Selected route and supported operation |
| EVT-DEP-STATE | Current event state | Conditional | Duplicate checking, a non-create operation, learner-impact validation, stale-state recheck, or readback is required | Lookup | learningEvents parent, activities, metrics, userActionHints, whereUsed, and server-returned links | resolve_event_identity | Preview and reconciliation require one exact current snapshot | Supply a number or ID and retain the normalized fingerprint | Identity, lifecycle, schedule, capacity, learner impact, usage, activities, links, and fingerprint |
| EVT-DEP-LIFECYCLE | Lifecycle value and transition contract | Conditional | Activate, reactivate, cancel, reschedule, close, or explicit Draft status is requested | Lookup | Exact commonLookupsLOV routes exposed by current raw metadata plus FDD version 5 transition rules | resolve_event_lifecycle_values | Writable fields and lookup routes do not alone prove enabled values or an eligible transition | Resolve exact live values and FDD eligibility before preview | Current status, target status, reason values, required fields, and transition eligibility |
| EVT-DEP-COURSE | Exact course linkage | Conditional | Course-linked mode is selected | Lookup | Raw target learningCourses read contract | resolve_event_course_linkage | A linked event must reference one exact active course | Supply the exact course number or ID | Course identity, returned link, status, and current-state evidence |
| EVT-DEP-SUPPLIER | Training supplier | Conditional | An activity references a training supplier | Lookup | Raw target learningTrainingSuppliers Describe with 3 nodes, 64 attributes, 3 LOV-decorated attributes, and 49 queryable attributes | resolve_event_training_supplier | A supplied training resource must be exact and active | Supply the exact supplier number | Supplier ID, number, title, status, link, and active-state evidence |
| EVT-DEP-INSTRUCTOR | Instructor identity and availability | Conditional | An activity supplies an instructor | Lookup | Raw target learningInstructors Describe with 5 nodes, 96 attributes, 9 LOV-decorated attributes, and 80 queryable attributes | resolve_event_instructor_availability | Every supplied instructor must be exact and active; activation or active scheduling also requires availability for the complete window | Supply the instructor number and, when availability is required, complete schedule inputs | Instructor identity, status, conditional availability, supplier, provider summary, link, and schedule evidence |
| EVT-DEP-CLASSROOM | Classroom identity, capacity, and availability | Conditional | An activity supplies a classroom | Lookup | Raw target learningClassrooms Describe with 5 nodes, 142 attributes, 4 LOV-decorated attributes, and 99 queryable attributes | resolve_event_classroom_availability | Every supplied classroom must be exact and active; activation or active scheduling also requires availability and sufficient capacity | Supply the classroom number and, when availability is required, complete schedule and planned demand | Classroom identity, status, conditional availability, capacity, location, supplier, link, and schedule evidence |
| EVT-DEP-VIRTUAL | Virtual-classroom provider account | Conditional | Instructor-provider webinar delivery or account details are supplied | Lookup | Raw target learningInstructors learningVirtualClassrooms child and validateProviderUser action | resolve_event_virtual_classroom_account | Every supplied account must be exact and compatible; activation or active scheduling also requires the caller-supplied provider request and success rule | Supply the provider account and, when validation is required, the approved provider validation contract | Account identity, provider type, account states, conditional validation evidence, and meeting-template evidence |
| EVT-DEP-ADHOC | Ad hoc activity resource | Conditional | An activity requests an ad hoc resource | Blocked | Event assignment rows confirm assigned values but no approved global identity, inventory, or schedule-availability provider exists | | Assignment evidence cannot prove that a resource is globally valid or conflict-free | Remove the ad hoc resource or supply an approved provider contract in a future skill revision | Resource identity, status, quantity, availability, and conflict evidence |
| EVT-DEP-SECURITY | HCM security profile | Conditional | Visibility requires security-controlled access | Lookup | Approved HCM security-profile evidence already returned to the task context | resolve_event_security_profile | Visibility must not exceed established security | Resolve the applicable profile before preview | Exact security profile identity and evidence fingerprint |
| EVT-DEP-EXTENSIBILITY | Descriptive flexfield metadata | Conditional | A row supplies extensible attributes | Blocked | Current raw metadata confirms only the WLF_LEARNING_ITEM context, not portable target segment definitions | | Custom segments from another target are not portable | Defer the DFF change until exact live target segments and write support are supplied | Context, segment identifier, datatype, allowed value, and write support |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The row's documented route and every dependency applicable to the requested operation are exact | Yes for read-only checks; mutation still needs preview and approval |
| Draft With Activation Gaps | A create-Draft row omits activation-only schedule, capacity, or resource evidence | Yes for Draft create only; no activation |
| Blocked | A required identity, contract, conflict check, provider, value, or transition is unresolved for that row | No for that row |
| Not Required | A conditional dependency does not apply to the row | No lookup needed |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVT.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->EVT.RESOLVE_REFERENCE;draft_gaps->EVT.RESOLVE_REFERENCE;not_required->EVT.RESOLVE_REFERENCE;blocked->EVT.HANDLE_ERROR | EVT.VALIDATE_INPUT | stop | After row inputs and the selected operation are validated |
