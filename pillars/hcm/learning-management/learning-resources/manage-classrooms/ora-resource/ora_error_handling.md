# Manage Classrooms Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Classroom count or Bulk intent is missing or invalid | Stop before route selection and ask how many classrooms the user wants to create or whether the request is bulk |
| Bulk route has no Excel-or-DAT choice | Ask whether the source will be an Excel workbook or a DAT file; do not prepare or upload an artifact |
| Declared count differs from normalized loader rows | Show the declared and observed counts and block until the count or source is corrected |
| A single-row Excel or DAT source is supplied | Disclose that one classroom normally uses REST and ask whether to use REST or explicitly continue with Data Loader; rebuild the preview after selection |
| Title is missing | Block the affected row and request the Title |
| Required location value is missing | Block the affected row and request a location name, code, or identifier |
| No eligible existing location matches | Preserve the classroom row, route the manual dependency to hcm.global-human-resources.locations.manage-locations, and repeat locationsLov after provider completion |
| Optional owner is invalid | Offer correction or removal; never substitute another person |
| Ad hoc address is supplied | Block this Data Loader route and require an existing HCM Location |
| Description is missing | Ask first; default to exact Title only after explicit one-time acceptance |
| Optional contact is invalid | Offer correction or removal; never substitute another person |
| Supplier is invalid or inactive | Block until corrected or removed |
| Set is unresolved or ambiguous | Show code, name, and ID candidates and require one selection; never default COMMON |
| Optional loader identity is partially supplied or invalid | Complete one supported identity strategy or remove all optional identity fields |
| DFF context or segment is invalid | Report the exact context, segment, expected type or requiredness, and current live metadata source |
| Optional question has no answer | Ask the field once and allow explicit Skip; do not silently omit it |
| Status has no documented accepted create value | Remove it from the payload and disclose Fusion default behavior rather than guessing |
| Related material is supplied | Exclude it from the classroom load and retain it only for a separately supported post-create workflow |
| Lookup pagination is incomplete | Continue read-only paging before declaring no match |
| Unfiltered learningClassrooms GET returns HTTP 400 | Classify the request as an unsupported or incomplete lookup contract; do not retry with guessed query parameters and do not treat the response as zero matches |
| Optional title-collision inspection is unavailable | Continue with a proposal warning that the informational check was not completed; do not require allowReadinessOverride and do not claim title uniqueness |
| Stable-number finder returns an existing classroom | Block creation with that supplied number and show sanitized existing identity, location, and status evidence |
| Supplied ID and code or number resolve differently | Block as conflicting identity evidence |
| Exact proposal approval is absent or stale | Stop before create and request Approve proposal vN |
| REST payload preparation fails locally before dispatch | Disclose that no HTTP request was sent; correct local preparation and retain approval only when the environment, endpoint, method, and exact JSON payload are unchanged |
| REST create returns a known validation or HTTP 4xx failure | Stop and show the sanitized failure; a Data Loader route requires a new artifact and its own approval workflow |
| REST create times out, loses the connection, returns HTTP 5xx, or has another uncertain outcome | Stop without retry or fallback; reconcile through finders or item read-back before another write |
| Data Loader validation, upload, or initiation fails | Follow the authoritative core.data-loader failure report and retry rules; do not substitute direct REST for the failed rows automatically |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| route_selection | Classroom count, Bulk intent, or Excel-or-DAT choice is missing, invalid, or inconsistent with the source | Correct the route input before field mapping |
| input_validation | Required input, optional-field decision, supplied key pair, or field shape is invalid | Correct the affected row |
| selection_required | Location, person, supplier, or Set choice is ambiguous | Select one documented option |
| catalog_mismatch | Proposed field, key, Status, or DFF does not match current learningClassrooms metadata | Refresh metadata and correct or remove the affected field |
| lookup_contract_missing | A required supplier or stable-number lookup has no documented executable request | Remove the optional value or document the required lookup; do not replace it with an unfiltered collection scan |
| informational_lookup_unavailable | The optional title-collision lookup has no documented contract or returns HTTP 400 | Continue with a warning and no assertion that zero same-title classrooms exist |
| approval_blocker | Approval is absent, stale, or for another proposal | Review and approve the exact current version |
| transport_environment | REST outcome is uncertain because of timeout, connection loss, or server failure | Reconcile with read-only evidence before any retry or route change |
| execution_failure | Create or child-data operation fails | Read back, report sanitized details, and request one safe next action |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Intake completion | Count or Bulk intent, selected route, Excel-or-DAT choice when applicable, and every required, conditional, optional, advanced, system-generated, and separate-workflow field with value, Skip, Not Applicable, or Blocked status |
| Proposal | Selected route; Title, Description and provenance; identity handling; Location, Owner, Capacity, Contact, Supplier, Set, Status handling, DFF values, advanced references, related-material disposition, lookup evidence, warnings, validation, and exact REST properties or Data Loader columns |
| REST approval | Exact environment, POST endpoint, HTTP method, and immutable JSON body for one classroom |
| Data Loader approval | Use the authoritative core.data-loader approval report for the exact immutable Excel-or-DAT-derived artifact; do not add a second task approval |
| Post-create | Created, existing, blocked, and failed rows plus submitted keys, Fusion-generated ID or number, status, and any separate child-workflow result |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Count is missing or unclear | Do not infer single or bulk mode from the number of values mentioned casually or from a filename alone |
| More than one classroom is requested | Do not issue individual REST POST requests in a loop; use core.data-loader with Excel or DAT |
| REST execution fails or is uncertain | Do not switch to Data Loader, retry POST, or assume no classroom was created without reconciliation and new route-specific approval |
| Data Loader is selected | Do not bypass core.data-loader by calling UCM upload or initiateDataLoad directly |
| Name or location was not provided | Do not derive it from context |
| The Data Loader object does not exactly match the registered discriminator | Use the exact registered FSCR object `learningClassrooms` |
| Decimal capacity is supplied | Do not round or truncate it |
| Optional field was not answered | Do not interpret silence as Skip |
| Set or Status is absent | Do not assume COMMON or Active |
| Related material is supplied | Do not insert it into the learningClassrooms load artifact |
| An internal ID, GUID, or audit value is absent | Do not ask the user to invent it |
| Proposal changed after approval | Do not reuse the earlier approval |
| Mutation outcome is uncertain | Do not automatically retry |
| A title-only finder is undocumented | Do not invent finder names, q expressions, required arguments, or an unfiltered learningClassrooms scan |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.APPROVAL_GATE | decision | 6 | execution_gate | approved->CL.READY;missing->CL.BLOCKED;changed->CL.BLOCKED;failure->CL.FAILED | CL.ENFORCE_DESIGN | stop | Immediately before one direct REST POST or before handing the exact bulk source to core.data-loader's authoritative approval workflow |
| CL.READY | terminal | 7 | terminal | none | CL.APPROVAL_GATE | continue | The selected route's current proposal or immutable artifact is approved and every selected classroom passes validation |
| CL.BLOCKED | terminal | 8 | terminal | none | none | continue | Input, dependency, lookup, default, design, or approval blocks creation |
| CL.FAILED | terminal | 9 | terminal | none | none | continue | Validation or readiness evaluation fails unexpectedly |
