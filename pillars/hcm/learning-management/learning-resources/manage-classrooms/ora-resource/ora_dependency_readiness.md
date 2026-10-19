# Manage Classrooms Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Creation route | Ask how many classrooms the user wants to create or whether the request is bulk; select REST for one and Data Loader for multiple or bulk |
| 2 | Route-specific live contract | For REST, discover writable learningClassrooms properties from describe; for Data Loader, discover registered learningClassrooms columns, keys, requiredness, DFF definitions, and accepted values |
| 3 | Bulk source format | For Data Loader, require Excel or DAT and validate the exact source before approval |
| 4 | Location | Resolve exactly one active HCM Location with address details per row; if none exists, route the blocked row to hcm.global-human-resources.locations.manage-locations, then re-query locationsLov before resuming |
| 5 | Optional and conditional references | Resolve retained Owner, Contact, Training Supplier, and applicable Set; record explicit Skip for omitted optional values |
| 6 | Existing classroom identity | When an explicit integration or migration classroom number is retained, require a zero-match findByClassroomNumber collision check; for every ordinary create, collect same-title candidates through findByKeyword and treat them as informational |
| 7 | Payload or artifact readiness | Map only attributes supported by the selected route; validate a Data Loader identity strategy only when the user explicitly supplied one |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CL.ROUTE | Classroom creation route | Yes | Every request | Verify or Blocked | User-provided count or explicit Bulk intent |  | Prevents unsafe bulk REST loops and accidental Data Loader selection for a single classroom | Enter 1, a whole number greater than 1, or Bulk | Normalized count or bulk intent plus REST or Data Loader route |
| CL.BULK_FORMAT | Bulk source format | Conditional | Count is greater than 1 or Bulk is selected | Verify or Blocked | User choice or supplied file extension |  | Establishes the source contract before Data Loader processing | Select Excel or DAT and provide or generate the matching source | Excel .xlsx or DAT .dat or validated ZIP |
| CL.REST_CONTRACT | Live Learning Classrooms REST schema | Conditional | Count is exactly 1 | Lookup or Blocked | Fusion REST describe metadata | validate_classroom_rest_contract | Prevents an unsupported property or method from being sent in the direct create request | Correct the JSON fields to the current REST contract or explicitly choose a newly previewed Data Loader route | Validated POST endpoint, writable properties, and item read-back contract |
| CL.LOCATION | Classroom location | Yes | Every row | Lookup, Provider Handoff, or Blocked | User-selected existing location or validated Manage Locations output | resolve_classroom_location | learningClassrooms requires a location with address details | Select one accessible existing HCM Location; if none exists, complete hcm.global-human-resources.locations.manage-locations and re-run the lookup | LocationId or LocationCode |
| CL.OWNER | Optional classroom owner | No | Owner is supplied | Lookup or Blocked | User-provided owner identity | resolve_classroom_owner | Prevents an incorrect retained owner reference | Select one accessible worker, correct the value, or remove the owner | OwnedByPersonId or OwnedByPersonNumber |
| CL.CONTACT | Optional contact | No | Contact is supplied | Lookup or Blocked | User-provided contact identity | resolve_classroom_contact | Prevents an incorrect person reference | Select, correct, or remove the contact | ContactId or ContactNumber |
| CL.SUPPLIER | Optional training supplier | No | Supplier is supplied | Lookup or Blocked | User-provided verified supplier identifier | resolve_training_supplier | Prevents an unverified supplier reference | Supply a verified ID or number, or remove the supplier | TrainingSupplierResourceId or TrainingSupplierResourceNumber |
| CL.SET | Accessible reference-data set | Conditional | Set is applicable or supplied | Lookup or Blocked | User-provided set code, ID, or name | resolve_classroom_set | SetCode must identify one accessible set and must not be guessed | Select one set or remove it only when the tenant does not require it | SetCode and proposal display values |
| CL.KEY | Optional Data Loader identity | No | Any loader identity field is supplied | Verify or Blocked | Explicit integration or migration mapping | validate_classroom_resource_contract | A retained optional identity must use one complete supported strategy | Supply an exact resource number, supply both SourceSystemOwner and SourceSystemId, or remove all identity fields | Validated key columns and values, or confirmed omission |
| CL.EXISTING_NUMBER | Existing classroom with the supplied stable number | Conditional | ClassroomResourceNumber is retained | Lookup or Blocked | Explicit integration or migration classroom number | resolve_existing_classroom_by_number | Prevents creating another classroom with the same stable business number | Use the existing classroom, provide a different supported number, or omit the optional number for an ordinary create | Existing classroom identity or verified zero-match evidence |
| CL.EXISTING_TITLE | Accessible classrooms with the supplied Title | No | Every ordinary create after Title validation | Lookup or Warning | User-provided Title | resolve_existing_classroom_by_keyword | Surfaces likely duplicates without treating Title as a unique key | Review same-title candidates and choose use existing or create another; an unavailable informational lookup is a warning, not a readiness override | Same-title candidate evidence or a disclosed lookup warning |
| CL.DFF | Classroom descriptive flexfields | Conditional | A DFF context is configured, required, or supplied | Verify or Blocked | Live metadata plus user values | validate_classroom_resource_contract | Tenant-specific mandatory segments must be present and type-correct | Select a context and supply required segments; omit optional unused segments | Context and validated segment columns |
| CL.CONTRACT | Live Data Loader schema | Conditional | Count is greater than 1 or Bulk is selected | Lookup or Blocked | Fusion Data Loader metadata and UCM template | validate_classroom_resource_contract | Prevents use of a stale or unregistered discriminator | Correct fields and keys to the live learningClassrooms contract | Validated field catalog and loader source schema |
| CL.OPTIONAL_DECISIONS | Optional-field completion | Yes | Before proposal | Verify or Blocked | User values or explicit Skip decisions |  | Prevents silent omission of relevant create options | Answer or Skip Owner, Capacity, Contact, Training Supplier, and any supported initial Status | Complete optional-field decision record |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every mandatory or conditional dependency is resolved; an unavailable optional title-collision inspection is disclosed as a warning | Yes |
| Route input required | Classroom count or Bulk intent is missing or invalid, or a Data Loader source format is not selected | No |
| Selection required | Multiple location, person, supplier, or Set choices remain | Lookup yes; create no |
| Optional decision required | An applicable optional field has neither a value nor explicit Skip | Lookup yes; create no |
| Blocked | A mandatory dependency, key, configured DFF, retained optional value, or contract is missing or invalid | Lookup yes; create no |

## Locations Setup Provider Handoff

The published Learning baseline marks Locations Setup as a manual dependency. A zero-match location lookup must preserve the classroom row and route location setup to `hcm.global-human-resources.locations.manage-locations`; it must not create a location through the Classroom skill. Provider completion must return the location identifier or code, name, address, and Active status. The Classroom skill then repeats `resolve_classroom_location`. Only that independent read-back can change `CL.LOCATION` to Satisfied.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->CL.APPLY_DEFAULTS;selection_required->CL.BLOCKED;blocked->CL.BLOCKED;failure->CL.FAILED | CL.RESOLVE_REFERENCES | stop | After route selection and all applicable route-contract, location, duplicate, and optional-reference lookups complete |
