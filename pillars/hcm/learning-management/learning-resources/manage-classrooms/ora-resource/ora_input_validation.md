# Manage Classrooms Input Validation

## Source Basis

- OLC-116674 FDD, latest approved version; Jira OLC-120236 is traceability only.
- Oracle HCM Data Loading Business Objects, Guidelines for Loading a Learning Classroom Resource.
- Oracle HCM Data Loading Business Objects, Guidelines for Loading Training Suppliers to Oracle Learning.
- Oracle Help, Create a Classroom for Your Oracle Learning Catalog Resources.
- Live tenant Data Loader metadata and UCM template for the `learningClassrooms` discriminator and component.
- Live tenant `/hcmRestApi/resources/latest/learningClassrooms/describe` contract and successful single-classroom POST/read-back validation.

## Creation Mode Intake

| Question | Required? | Accepted Answer | Selected Route | If Missing or Invalid |
|---|---|---|---|---|
| How many classrooms do you want to create? | Yes; ask before classroom fields | 1, a whole number greater than 1, or Bulk | 1 selects single-classroom REST; greater than 1 or Bulk selects Data Loader | Block and ask the count-or-bulk question again; reject zero, negative, fractional, and unclear values |
| Do you want to prepare the bulk classrooms in an Excel workbook or a DAT file? | Yes for Data Loader when the format is not already evident | Excel or DAT | Excel accepts .xlsx; DAT accepts .dat or a ZIP containing the validated DAT | Block bulk preparation until one format is selected |

Do not infer bulk intent solely from a filename. Do not implement a multi-classroom request as repeated REST POST requests.

## Route Field Mapping

| Business Field | Single REST Attribute | Data Loader Attribute | Route Rule |
|---|---|---|---|
| Classroom title | classroomTitle | Title | Required for every classroom |
| Description | classroomDescription | Description | Required at submission after any explicitly accepted default |
| Existing location | classroomLocationId | LocationId or LocationCode | Resolve exactly one active location with address details before mapping |
| Seating capacity | classroomCapacity | Capacity | Optional whole number; omit when skipped |
| Other optional or conditional value | Live describe-backed writable attribute | Live Data Loader metadata-backed attribute | Include only when the selected route contract supports the retained user value |

## Field Collection Contract

| Business Field | Data Loader Attribute | Classification | How the User Can Populate It | Lookup or System Population | If Omitted or Invalid |
|---|---|---|---|---|---|
| Classroom title | Title | Required | Enter exact classroom title | None; preserve user text and trim outer whitespace only | Block; never derive or recommend a title |
| Description | Description | Required at submission | Enter description, or explicitly accept exact Title as the one-time default | Local documented default after explicit acceptance | Block until entered or default acceptance is recorded |
| Existing location | LocationId or LocationCode | Required | Enter or select location ID, code, or name | resolve_classroom_location fills one stable key and verified display or address | Block on no match, ambiguity, inactivity, or missing address details |
| Classroom owner | OwnedByPersonId or OwnedByPersonNumber | Optional; always offer | Enter or select person ID, person number, full name, or work email, or choose Skip | resolve_classroom_owner fills one stable person key and display value when retained | Correct, select, or Skip on no match or ambiguity; Skip omits the owner columns |
| Data Loader identity | ClassroomResourceNumber, or SourceSystemOwner plus SourceSystemId | Advanced optional; not required for an ordinary create | Supply only for an explicit integration or migration mapping | validate_classroom_resource_contract confirms any supplied key columns; never manufacture an identifier | Omit all identity columns when unused; if any are supplied, block the retained mapping until one supported strategy is complete |
| Seating capacity | Capacity | Optional; always offer | Enter a whole number, or choose Skip | No lookup | Reject decimals or unreadable values; Skip omits the column |
| Contact person | ContactId or ContactNumber | Optional; always offer | Enter or select person ID, person number, full name, or work email, or choose Skip | resolve_classroom_contact fills one stable person key and display value | Correct, select, or Skip on no match or ambiguity |
| Training supplier | TrainingSupplierResourceId or TrainingSupplierResourceNumber | Optional; always offer | Enter a verified resource ID or number, search by supplier name when a contract is available, or choose Skip | resolve_training_supplier is required for name search or identifier verification | Block the retained value when unverified; Skip omits the columns |
| Set | SetCode | Conditional; offer when Set assignment applies | Enter or select set code, ID, or name | resolve_classroom_set fills SetCode | Block on no match or ambiguity; never default the Set |
| Descriptive flexfield context | FLEX:WLF_RESOURCE_DFF and context discriminator columns | Conditional | Select a configured context or choose no context when permitted | validate_classroom_resource_contract discovers available DFF contexts and columns | Block when a configured mandatory context is missing or invalid |
| Descriptive flexfield segments | fawqaWlfResourceDff, learnDffResChrac, learnDffResDate, learnDffResNum, and tenant-exposed segment columns | Conditional | Enter values for the selected context | validate_classroom_resource_contract supplies live segment names, types, and requiredness | Block only missing or invalid mandatory segments; omit unused optional segments |
| Initial status | Status | Optional only when live metadata defines accepted create values | Select an accepted value or choose Fusion default | validate_classroom_resource_contract must provide the accepted create values | Omit the column when accepted values are not documented; never guess Active or Inactive |
| Advanced source references | SourceType, SourceId, SourceRefTableName, SourceRef001 through SourceRef010 | Advanced conditional | Supply only from an explicit integration or migration mapping | validate_classroom_resource_contract confirms columns; no business-value lookup | Do not prompt in normal interactive creation; reject an incomplete or undocumented mapping |
| System-generated values | ClassroomResourceId, GUID, audit fields, availability, derived display values | System generated or read-only | Not user populated | Fusion generates or returns them | Never request or send them unless live metadata explicitly makes a field writable for this operation |
| Related materials | Not part of the validated learningClassrooms component | Separate workflow | Collect only when a supported post-create material workflow is selected | No classroom-load mapping | Do not include in the learningClassrooms artifact |
| Manually entered location address | Not part of the validated learningClassrooms loader route | Alternate UI route | Use the Oracle Learning classroom UI when that route is explicitly selected | UI performs its own address handling | Block in this Data Loader flow and offer existing-location selection |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Creation scope | 1, a whole number greater than 1, or Bulk | Block before field collection | Ask how many classrooms the user wants to create or whether the request is bulk | Every request |  |
| Bulk source format | Excel or DAT | Block bulk preparation | Ask whether the user will provide an Excel workbook or a DAT file | Count is greater than 1 or Bulk is selected and no source format is evident |  |
| Classroom identity | User-provided Title | Block the row before proposal | Ask for the title; never derive or recommend it | Every row |  |
| Description | User description, or exact Title after explicit one-time default acceptance | Block creation | Ask for a description or explicit acceptance of the documented default | Every row |  |
| Existing location | One accessible active HCM Location with address details | Block the row | Search by location name, code, or ID and require user selection when ambiguous | Every row in this Data Loader route | resolve_classroom_location |
| Optional owner | One existing worker identified by ID, number, name, or work email, or explicit Skip | Block proposal completeness, not the field itself | Search and require one exact worker selection when retained, or record Skip | Before the versioned proposal | resolve_classroom_owner |
| Tenant-required configuration | Required Set and descriptive flexfield values | Block creation | Discover live fields and request only configured mandatory values | Tenant metadata makes the value mandatory | validate_classroom_resource_contract |
| Optional-field decisions | Owner, Capacity, Contact, Training Supplier, Set when optional, Status when supported, and DFF values when optional | Block proposal completeness, not the field itself | Ask each applicable optional question and record a value or explicit Skip | Before the versioned proposal |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Count is exactly 1 | Select the direct Learning Classrooms REST route | Validate the live REST describe contract before mapping the JSON payload | validate_classroom_rest_contract |
| Count is greater than 1 or Bulk is selected | Select the Data Loader route | Require Excel or DAT, then validate the exact `learningClassrooms` metadata and source artifact | validate_classroom_resource_contract |
| Location text, code, or ID is supplied | Require one active accessible location with address details | Fill LocationId or LocationCode, or request correction or selection | resolve_classroom_location |
| Owner is supplied | Resolve exactly one accessible worker for the owner role | Fill OwnedByPersonId or OwnedByPersonNumber | resolve_classroom_owner |
| Contact is supplied | Resolve exactly one accessible worker for the optional contact role | Fill ContactId or ContactNumber; never copy the owner without user intent | resolve_classroom_contact |
| Set is applicable or supplied | Require one accessible set | Fill SetCode or request correction or selection | resolve_classroom_set |
| Supplier is supplied | Require one accessible verified supplier and Active status when the lookup can return status | Fill supplier ID or number, remove the optional value, or remain blocked | resolve_training_supplier |
| DFF, Status, key, or advanced reference fields are supplied | Validate each column, type, requiredness, and accepted value against live metadata | Keep validated fields; request correction or omit optional unsupported fields | validate_classroom_resource_contract |
| Ad hoc address is supplied | Current Data Loader contract has no mapped address columns | Block and offer an existing HCM Location or the separate interactive UI route |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Classroom count or bulk intent | Accept only 1, a whole number greater than 1, or explicit Bulk intent | Every request before route selection |  |
| Route consistency | Use REST for one classroom and Data Loader for multiple or bulk classrooms; require a new preview and approval after any route change | After count normalization and again before approval |  |
| Bulk format | Accept Excel as .xlsx or DAT as .dat or a ZIP containing the validated DAT | Data Loader route | validate_classroom_resource_contract |
| Bulk row count | Require the declared count to equal the normalized nonblank root-row count; a single-row bulk source requires route confirmation | Data Loader route after source parsing | validate_classroom_resource_contract |
| Title | Require a nonblank user-provided value; trim outer whitespace only | Every row |  |
| Description | Require nonblank text after any approved default is applied | Every row before proposal |  |
| Location | Require exactly one LocationId or LocationCode whose location is active and has address details | Every row | resolve_classroom_location |
| Owner | Keep only one uniquely resolved OwnedByPersonId or OwnedByPersonNumber | Owner is retained | resolve_classroom_owner |
| Loader key | When any identity field is supplied, require exactly one complete supported strategy; source-system owner and ID are a pair. Otherwise omit all identity columns. | Any loader identity field is supplied | validate_classroom_resource_contract |
| Capacity | Accept a whole number only; never round or truncate a decimal | Capacity is supplied |  |
| Contact | Keep only a uniquely resolved ContactId or ContactNumber | Contact is retained | resolve_classroom_contact |
| Supplier | Keep only a verified TrainingSupplierResourceId or TrainingSupplierResourceNumber | Supplier is retained | resolve_training_supplier |
| Set | Keep one resolved SetCode | Set is applicable or supplied | resolve_classroom_set |
| Flexfields | Validate context, column, type, and configured requiredness from current metadata | Any DFF value is supplied or required | validate_classroom_resource_contract |
| Status | Include only when current metadata documents an accepted create value | Status is supplied | validate_classroom_resource_contract |
| Advanced references | Require an explicit integration mapping and complete related values | Any SourceType, SourceId, or SourceRef field is supplied | validate_classroom_resource_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.VALIDATE_INPUT | step | 1 | validate_input | valid->CL.RESOLVE_REFERENCES;invalid->CL.BLOCKED;failure->CL.FAILED | none | stop | After count-or-bulk intent and any required Excel-or-DAT choice are known, and after required and applicable optional fields have a value or explicit Skip |
