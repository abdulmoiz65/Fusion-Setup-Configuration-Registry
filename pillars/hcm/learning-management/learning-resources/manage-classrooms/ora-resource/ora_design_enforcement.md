# Manage Classrooms Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select creation route | Ask the classroom count-or-bulk question and select REST for one or Data Loader for multiple or bulk |
| 2 | Preserve user input | Keep the user-provided Title; validate loader identity fields only when the user explicitly supplies them |
| 3 | Enforce mandatory references | Require one existing active location with address details per classroom |
| 4 | Complete optional intake | Ask Owner, Capacity, Contact, Training Supplier, applicable Set, supported Status, and optional DFF values; record a value or Skip |
| 5 | Validate conditional and advanced data | Enforce Set, DFF, key-pair, and explicit integration-mapping requirements |
| 6 | Build route-specific proposal | Show every field, provenance, mapped REST property or loader attribute, lookup result, default, Skip, warning, blocker, and exact action |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every classroom creation request | Blocker |  | Classroom count or explicit Bulk intent is missing, zero, negative, fractional, or unclear | Ask how many classrooms the user wants to create or whether the request is bulk | Yes |
| Count is exactly 1 | Blocker | validate_classroom_rest_contract | A bulk REST loop is proposed, the REST create contract is unavailable, or the proposal does not show one exact JSON payload | Use one direct REST POST after contract validation and exact approval, or explicitly select a newly validated Data Loader route | Yes |
| Count is greater than 1 or Bulk is selected | Blocker | validate_classroom_resource_contract | Excel or DAT is not selected, the source is unavailable, or individual REST POST requests are proposed | Select Excel or DAT and route the exact source through core.data-loader | Yes |
| A Data Loader source contains one normalized classroom row | Blocker | validate_classroom_resource_contract | The single-row mismatch has not been disclosed and the user has not selected REST or explicitly continued with Data Loader | Ask whether to use the normal REST route or continue with Data Loader, then rebuild the route-specific preview | Yes |
| Declared count is greater than 1 | Blocker | validate_classroom_resource_contract | The normalized nonblank loader-row count differs from the declared classroom count | Correct the declared count or source rows before approval | Yes |
| Every classroom row | Blocker |  | Title is blank or derived | Require a user-provided Title | Yes |
| Any loader identity field is supplied | Blocker | validate_classroom_resource_contract | The retained optional identity is incomplete or unsupported | Supply ClassroomResourceNumber, supply both SourceSystemOwner and SourceSystemId, or remove all optional identity fields | Yes |
| An explicit ClassroomResourceNumber is retained | Blocker | resolve_existing_classroom_by_number | One exact existing classroom has the same stable number, the result is ambiguous, or findByClassroomNumber cannot run successfully | Use the existing classroom, provide a different supported number, or omit the optional number for an ordinary create | Yes |
| Location is evaluated | Blocker | resolve_classroom_location | Existing location is missing, inaccessible, ambiguous, inactive, or lacks address details | Select one valid existing HCM Location; for no match, complete hcm.global-human-resources.locations.manage-locations and re-run the lookup | Yes |
| Owner is retained | Blocker | resolve_classroom_owner | Owner is inaccessible or ambiguous | Select one existing worker, correct the value, or Skip | Yes |
| Ad hoc address is supplied | Blocker |  | Current learningClassrooms load contract has no mapped address columns | Select an HCM Location or explicitly switch to the separate interactive UI route | Yes |
| Capacity is supplied | Blocker |  | Value is not a whole number | Supply a whole number; never round | Yes |
| Contact is retained | Blocker | resolve_classroom_contact | Contact is unresolved or ambiguous | Select one worker, correct it, or Skip | Yes |
| Supplier is supplied | Blocker | resolve_training_supplier | Supplier identifier is unverified, inaccessible, ambiguous, or inactive | Supply a verified Active supplier ID or number, or remove it | Yes |
| Set is applicable or supplied | Blocker | resolve_classroom_set | Set is unresolved, ambiguous, or inaccessible | Select one accessible Set; never assume COMMON | Yes |
| DFF values are required or supplied | Blocker | validate_classroom_resource_contract | Context or segment is missing, unsupported, or type-invalid | Use current metadata and correct only the affected context or segment | Yes |
| Status is supplied | Blocker | validate_classroom_resource_contract | Accepted create values are not documented by current metadata | Remove Status and use Fusion default, or select a documented value | Yes |
| Optional-field intake is incomplete | Blocker |  | An applicable optional field has neither a value nor explicit Skip | Answer or Skip each optional question | Yes |
| Advanced source-reference field is supplied | Blocker | validate_classroom_resource_contract | No explicit integration mapping justifies the field or related values are incomplete | Remove it or provide the complete documented mapping | Yes |
| Related material is supplied | Warning |  | Material is not a learningClassrooms loader column | Retain it for a separately supported post-create workflow | Yes |
| Same-title candidates are inspected | Warning | resolve_existing_classroom_by_keyword | findByKeyword returns one or more exact same-title candidates | Show candidate identifiers, numbers, statuses, and location IDs; require the user to choose use existing or create another because Title is not unique | Yes |
| Title-collision inspection is unavailable | Warning | resolve_existing_classroom_by_keyword | findByKeyword returns HTTP 400 or an incompatible response | Disclose that same-title candidates were not inspected, do not claim zero matches, and continue without a readiness override | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| validate_classroom_rest_contract | Count is exactly 1 | Supported POST action, writable JSON properties, and item read-back contract | ora_reference_lookups.md |
| resolve_classroom_location | Existing location is selected | Accessible location identifier and display details | ora_reference_lookups.md |
| resolve_classroom_owner | Owner is supplied | Verified owner person | ora_reference_lookups.md |
| resolve_classroom_contact | Contact is supplied | Verified contact person | ora_reference_lookups.md |
| resolve_training_supplier | Supplier is supplied | Verified Active supplier | ora_reference_lookups.md |
| resolve_classroom_set | Set is applicable or supplied | Verified SetCode and display values | ora_reference_lookups.md |
| resolve_existing_classroom_by_number | When an explicit integration or migration ClassroomResourceNumber is retained and mapped to classroomNumber | Existing classroom identity or verified zero-match evidence | ora_reference_lookups.md |
| resolve_existing_classroom_by_keyword | Every ordinary create after Title validation | Same-title candidate evidence or a disclosed lookup warning | ora_reference_lookups.md |
| validate_classroom_resource_contract | Count is greater than 1 or Bulk is selected | Live Data Loader schema, template columns, selected Excel-or-DAT format, and normalized row count | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.ENFORCE_DESIGN | decision | 5 | design_enforcement | passed->CL.APPROVAL_GATE;blocked->CL.BLOCKED;failure->CL.FAILED | CL.APPLY_DEFAULTS | stop | Before displaying the route-specific REST payload or Data Loader artifact proposal |
