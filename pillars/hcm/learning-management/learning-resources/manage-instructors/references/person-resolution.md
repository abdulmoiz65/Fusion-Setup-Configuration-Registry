# Person resolution

## Source contract and limits

Source inspected 2026-09-23, not deployed-target verification:

- Redwood root: `/scratch/learning-administration-ui/extension1/sources/`.
  `ui/self/applications/learning-resources/flows/main/pages/instructor-details-page.js:31-47`
  constructs `workersLov` `findByWord` with `AssignmentType=E C N`,
  `PrimaryAssignmentOnly=true`, `AssignmentStatusType=ACTIVE SUSPENDED`,
  `DataSecurityPrivilege=PublicPerson`,
  `FilterAttributes=DisplayName PersonNumber DepartmentName`, and `SearchTerms`.
- The same pages directory's `instructor-details-page-chains/fetchWorkerLOVActionChain.js:22-43`
  requests PersonId, DisplayName, PersonNumber, DepartmentName, LocationName,
  JobName, BusinessUnitName and AssignmentStatusType. Its person-ID lookup uses q.
- `instructor-details-page-chains/selectPersonActionChain.json:45` checks
  `learningInstructors` with `q=personId=<selected ID>` before creation.
- `services/self/catalog.json` maps these to HCM REST 11.13.18.05 and framework 9.

Use `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` only, following
its skill/reference and the independent read-only readiness below. Fixed relative routes in
`scripts/instructor_workflow.py` retain shared authentication and host/redirect
policy. No private transport, broadened security, caller URLs or direct POST.
The CLI pins the expected origin to the current configured restBaseUrl before
starting the shared client. A target change blocks; never edit configuration to
make a check pass. Let shared authentication handle login; if interactive login
cannot finish within the read bound, use the routed shared authentication workflow
first, then restart the read. Do not scrape browser credentials.

## Independent read-only readiness

An explicit person lookup or duplicate-check request selects `lookup` or
`check-existing`. Supply both --expected-environment and --expected-origin.
The command verifies these against the current properties, applies shared HTTPS
target policy, checks the shared client exists, validates the identifier before
the first GET, and retains the fixed query, pagination and person-selection rules.
The GET enforces the current account's person/data access; denial is not no-match.
No Set/DFF creation check, active Run Book or usable upload template is needed for
discovery. Those remain mandatory where applicable for creation. The read result
is not a Task Hook envelope or write approval; read_readiness always returns
createReady=false and refuses creation/readback/other operations. Post-create
readback retains its separate existing gate. Never call the shared client directly
to evade a failed read check. Do not broaden PublicPerson scope on empty results.

## Intake and selection

Use the local request schema and normalize_request. Preserve person numbers and
IDs as strings, including leading zeros. Chat and structured rows are supported;
CSV/file intake must first be read with an installed supported reader and mapped
explicitly to the same schema. No claim of universal file-format support.

Person number, full name and partial-name discovery use the source finder. Exact
mode filters complete results by literal equality; no undocumented case-folding,
wildcards or fuzzy identity choice. ID mode uses the same PublicPerson finder and
numeric `q=PersonId=...`. A comma/semicolon/equal sign or other finder syntax is
blocked until escaping is verified; ask for an ID, not a guessed escape sequence.
Email has no enabled contract. Do not infer people from job/department/context.

Partial-name results are candidates, not verified name matches: the source finder
also searches numbers and departments. Present name, number, department, location
and assignment status where accessible. Require an explicit C1/C2/etc selection
even for one candidate. select_candidate binds the label to the result fingerprint
and target context; then resolve that ID afresh and check for an existing instructor.
Never carry a label across a changed search/result/target. Identity confirmation
does not approve the load. Match semantics, accents and minimum search length still
need target verification; do not introduce an arbitrary product minimum.

The local bounds are 100 rows/page, 20 pages and 120 seconds. Repeated pages,
unexpected offsets, missing identities, malformed pagination, empty nonterminal
pages, errors and limits produce incomplete results. Do not claim absence or
uniqueness from them. Narrow the search rather than selecting from a partial set.
Only complete zero results mean no accessible match under this security/filter/date
context. An authorization failure is never an empty result.

Only ACTIVE assignment creation is enabled. SUSPENDED occurs in the UI finder but
is not equivalent to active; inactive/terminated FDD acceptance conflicts with UI
create filtering. Do not broaden the finder or accept a warning as contract proof.
Deduplicate by verified PersonId, never name. Conflicting rows for one PersonId
require a narrower lookup. After exact resolution, `ensure_no_existing` requires
complete `learningInstructors?q=personId=...` results with zero matches.

## Backend evidence

Under `/scratch/jkaribee/view_storage/jkaribee_v2/fusionapps/`:
`hcm/components/hcmEngagement/learn/core/model/hcmEngmtLearnCoreModel/src/oracle/apps/hcm/engagement/learn/core/model/items/courses/`

- `entity/InstructorResourceDEOImpl.java:29-39`: beforeCommit duplicate check raises
  `WLF_LEARNTOP_DUP_INSTRUCTOR`. A prior GET cannot eliminate a concurrent race.
- `view/InstructorPersonSearchVO.xml:10`: inherits EnrollPersonSearchVO; excludes
  existing WLF_INSTRUCTOR_RESOURCES person IDs and applies public-person security.

Source presence does not establish current DL_ENV deployment, account eligibility,
or successful Data Loader writes. No person records belong in project diagnostics.
