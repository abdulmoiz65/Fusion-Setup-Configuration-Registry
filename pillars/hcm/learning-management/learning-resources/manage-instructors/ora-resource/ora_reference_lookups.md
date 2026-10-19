# Manage Instructors Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_instructor_person | A supported identifier or partial-name search is supplied | Explicit user name/number/ID or version-bound selected PersonId | GET /hcmRestApi/resources/11.13.18.05/workersLov using the finder contract below through core.fusion-api.rest-api-client | PersonId, DisplayName, PersonNumber, DepartmentName, LocationName, JobName, BusinessUnitName, AssignmentStatusType | Complete exact literal match on supplied field; partial search requires explicit selection then fresh ID resolution | personId and accessible verified identity/assignment fields | Zero means no accessible match; many or partial blocks; never auto-select even one partial-name candidate |
| inspect_existing_instructor | Person resolves uniquely or explicit later readback is requested | Resolved PersonId | GET /hcmRestApi/resources/11.13.18.05/learningInstructors with q=personId=<digit-string>, onlyData=true through core.fusion-api.rest-api-client | Root response including personId, instructorId, instructorNumber, instructorStatus and trainingSupplierId when present | Complete collection; zero matches required before create, exactly one matching person required for readback | Existing/generated instructor identity and observed values; missing fields stay unknown | Existing blocks create; incomplete cannot prove absence; readback zero/many stays unverified |
| validate_required_instructor_configuration | Before every root-only create | Explicit user Set scope deferral with recorded decision reference; no supplied DFF values | GET /hcmRestApi/resources/11.13.18.05/learningInstructors/describe through core.fusion-api.rest-api-client using instructor_workflow.py validate-configuration | Complete resourcesDFF attributes, properties, global flags, mandatory flags, context and default-expression metadata | Require configuration_validated from the executable pillar checker; verify decision reference against the actual user decision; reject required fields, unknown flags, custom defaults, non-global segments or incomplete global count | Current target and scope fingerprints; dffInputRequired=false for the supported root-only case | Any missing, denied, malformed or unsupported contract blocks; Set not explicitly deferred or any supplied DFF input requires supported extension, not a waiver |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A create-graph lookup path is TBD | Stop before presenting creation as executable; independent discovery still requires its own declared read readiness |
| A lookup returns 401 or 403 | Classify as authentication or authorization failure, not no-match |
| A person match is ambiguous | Show distinguishing person values and require user selection |

## Source-backed person query

Redwood instructor-details-page.js:31-47 and fetchWorkerLOVActionChain.js:22-43
under the Learning Administration UI (full paths in ../references/person-resolution.md)
declare findByWord;AssignmentType=E C N,PrimaryAssignmentOnly=true,
AssignmentStatusType=ACTIVE SUSPENDED,DataSecurityPrivilege=PublicPerson,
FilterAttributes=DisplayName PersonNumber DepartmentName. Append SearchTerms for
names/numbers; selected exact IDs use q=PersonId=<digit-string> with the same finder.
Use fields listed above, onlyData=true and REST-Framework-Version=9. No email
contract is enabled. GET workersLov/describe and learningInstructors/describe are
metadata-only checks through the same shared client. The separately requested
instructor prerequisite-inspection route in ../references/prerequisite-inspection.md
has its own metadata-only readiness. Explicit person discovery and duplicate checks
use the independent read readiness in ../references/person-resolution.md; they do
not evaluate or satisfy the create Task Nodes. Post-create readback retains graph readiness.
Source-backed declarations are not proof of deployed metadata or target behavior.

Bound pagination to 100/page, 20 pages, 120 seconds; loops/errors/limits remain
partial. Do not follow response URLs. Exact matching is literal. Finder searches
department and number too, so partial results are candidates, not name matches.
Only ACTIVE resolves for this increment. Supplier input is rejected by intake;
no supplier resolver is executed. Configuration validation is limited to explicit
Set deferral and optional global DFF fields without an advertised context default.
See ../references/prerequisite-inspection.md. A planned graph is not a successful
configuration check; execute the resolver for the current target and proposal.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IN.RESOLVE_REFERENCES | decision | 2 | reference_lookup | resolved->IN.CHECK_DEPENDENCIES;selection_required->IN.BLOCKED;duplicate->IN.BLOCKED;blocked->IN.BLOCKED;failure->IN.FAILED | IN.VALIDATE_INPUT | stop | Resolve person, duplicate instructor, optional supplier, Set, and flexfields before proposal |
