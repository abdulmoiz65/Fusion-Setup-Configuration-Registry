# External Purchase Prices Requisitioning BU Mapping Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Source organization input is missing or invalid | Stop and request only the missing or invalid value; never invent an identifier |
| Existing-target lookup returns zero or ambiguous identities | Stop for PATCH or DELETE and disclose the exact missing or ambiguous target; never select the first row. A zero-match read returns not-found and a zero-match new-parent check is not an error by itself |
| Active-membership lookup returns zero, many or incomplete evidence | Zero after complete enumeration is not a BU-eligibility result. Retain all same-identity membership matches for design evaluation; block ambiguous identities, restricted visibility, failed pages or incomplete pagination |
| An existing active mapping conflicts | Stop before Data Loader REST preparation; present the conflicting mapping and require an approved design decision |
| REST import fails or its outcome is uncertain | Preserve redacted status evidence and reconcile using a read-only GET before any retry; do not replay a POST, PATCH, or DELETE automatically |
| A pure record GET fails or is incomplete | Classify and disclose the read issue; no Data Loader fallback, sample generation, mutation approval or load initiation. Never label a partial or unauthorized read not-found |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | The required SourceOrganization value fails validation | Correct the exact supplied input |
| Dependency blocker | Procurement readiness or access evidence is unavailable | Complete the prerequisite and revalidate |
| Lookup blocker | A required existing target is missing, identity is ambiguous, or membership evidence is incomplete | Correct the exact keys or complete the read scope; do not turn incomplete evidence into no conflicts |
| Design conflict | A requisitioning BU has another active source-organization mapping | Make an approved reuse, update, or retirement decision |
| Auth or authz | Required privileges are unavailable | Correct access and retry only a read if appropriate |
| Transport or environment | A read-only service request fails before a side effect | Retry only a known idempotent read with bounds |
| Fusion API | A direct GET or REST import returns an HTTP 4xx or 5xx error; handle authentication/authorization failures under Auth or authz | Record fusion_api_error with the sanitized HTTP diagnostics below. A failed GET remains incomplete, never not-found; use only the core client's permitted bounded idempotent-read recovery within the selected read budget, otherwise RETURN_ISSUES with no Data Loader fallback. Do not automatically replay a write |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Readiness handoff | Supplied business-unit identities, source organization, defaulted activation state, and mapping-conflict result |
| Failure | Task code, stage, failure class, redacted evidence, affected business-unit identities, and recommended next action |
| HTTP failure diagnostics | For GET and import failures, include operation, HTTP status, sanitized endpoint path, Oracle error code and redacted message/body summary when supplied, ECID when supplied, and recommended next action. Redact query values, opaque resource keys, business values and secrets; never retain full URLs, raw response bodies, authorization headers, tokens or cookies. Mark unavailable fields as unavailable rather than inventing them. A transport failure without an HTTP response remains Transport or environment |
| Data Loader handoff | State that resource validation is complete only when no readiness blocker remains; core.data-loader owns sample generation, preview, approval, import, and verification |
| Read-only completion | Return the requested current parent/child details or confirmed not-found after complete direct GET evidence. EPPBU.RETURN_READ_RESULT completes the request without a loader handoff; do not claim mutation readiness or execution |
| Supported execution route | Parent and child POST, PATCH, and DELETE requests are delegated to core.data-loader using its live registered schema, child sections, immutable artifact and approval workflow. This v3 resource set defines no direct task-rest write operation; do not invoke core.data-loader.task-rest or construct a direct Fusion write from these rules |
| Representation boundary | Preserve the parent and child sections selected by core.data-loader. Nested REST examples are not Data Loader row/linkage requirements; never flatten or nest records contrary to the live loader contract |
| Validation versus execution | EPPBU.READY_FOR_DATA_LOADER_REST means mutation validation is ready for the loader approval workflow, not that a mapping was changed. EPPBU.RETURN_READ_RESULT means only that a pure read completed; these outcomes are not interchangeable |
| Conditional evidence | Record every applicable rule as passed or blocked and every excluded rule as not applicable with its operation reason; never report name-only exclusivity as passed solely because an ID was omitted |

## Verification Evidence

core.data-loader retains ownership of loader-job status and its mutation
lifecycle. Do not poll or query after initiation unless the active workflow and
user request permit that check. Requested record reads and authorized final-state
verification use the direct core REST GET contract, not a Data Loader read flow.
Distinguish loader success from separately observed final state; a GET result
does not authorize retrying any write.

| Operation | Expected Read Evidence | If Not Confirmed |
|---|---|---|
| Parent POST | Exactly one intended parent and its intended child memberships | Report not verified; do not replay the create |
| Parent PATCH | Exact parent remains, requested activation state matches, and omitted child memberships remain | Report mismatch or incomplete evidence; ask before another mutation |
| Child POST | Exactly one intended child under the exact parent; unrelated children remain | Report not verified or ambiguous; do not replay POST |
| Child DELETE | Requested child absent under the exact parent; retained children remain | Report mismatch or incomplete evidence; do not replay DELETE |
| Parent DELETE | Exact parent no longer found after a complete read | Report not verified if read scope is incomplete; absence alone does not describe recoverability |

## Golden Scenarios

| Scenario | Evidence | Expected Result |
|---|---|---|
| loader-handoff | Requested mutation and all applicable task rules complete | Return readiness to core.data-loader; no direct task-rest invocation |
| uncertain-post | Submission outcome unknown | Reconcile through an authorized read; no automatic retry |
| mutation-unapproved | Validation passed but exact artifact has no approval | No upload or initiation |
| partial-read | A needed parent or child page is unavailable | Incomplete validation; no approval preview claiming success |
| read-only-request | User asks only for parent and child details; no loader file or write privileges | After read preflight, direct core REST GET to RETURN_READ_RESULT; no loader, sample generation, defaults, upload or initiation |
| read-not-found | Complete authorized record GET finds no exact parent | RETURN_READ_RESULT with not-found; do not offer or initiate an implicit create |
| read-auth-failure | Direct GET cannot authenticate or read the requested scope after the core client's bounded recovery | RETURN_ISSUES with redacted auth/access diagnostics; no loader fallback |
| read-api-error | A required direct GET returns HTTP 400 with an Oracle error message and ECID | fusion_api_error and RETURN_ISSUES with HTTP status, sanitized endpoint path, redacted error summary and ECID; incomplete, not not-found; no automatic retry for invalid input and no loader fallback |
| read-api-recovery-exhausted | A required direct GET still returns HTTP 503 after permitted bounded recovery or the finite read budget is exhausted | Stop with incomplete evidence and sanitized HTTP diagnostics; RETURN_ISSUES, no further retry or loader fallback |
| read-child-http-not-found | Exact parent resolved but the returned child collection GET returns HTTP 404 | Report failed/incomplete child lookup with HTTP diagnostics, not an empty child set or confirmed parent-not-found |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.HANDLE_ERROR | step | 60 | error_handler | handled->EPPBU.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, defaulting, or design failure |
| EPPBU.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| EPPBU.READY_FOR_DATA_LOADER_REST | terminal | 80 | terminal | none | EPPBU.ENFORCE_DESIGN | stop | Requested mutation validation is satisfied and core.data-loader is the next workflow owner; never for pure record GET |
| EPPBU.RETURN_READ_RESULT | terminal | 90 | terminal | none | EPPBU.RESOLVE_REFERENCES | stop | Pure record GET selected read_complete with complete authorized parent/child evidence or confirmed not-found; return details without Data Loader |
