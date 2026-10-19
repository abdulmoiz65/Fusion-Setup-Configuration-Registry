# Manage Win/Loss Reasons Error Handling

## FSM Task Identity Policy

Preserve the catalog identity `MOO_MANAGE_WIN/LOSS_REASONS` / `Manage Win/Loss
Reasons` for task selection and task-local validation. Use the FSM execution
identity `FND_MANAGE_SET_ENABLED_LOOKUPS` / `Manage Set Enabled Lookups` for
export/import requests and archive metadata. Bind both identities, the selected
task `SKILL.md`, target environment, and immutable archive SHA-256 throughout
review, export, package preparation, and validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  catalog `TaskCode`, `TaskName`, offering, and functional area. Do not rewrite
  task context to the execution task.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Stop before undocumented writes, automatic mutation retries, stale approvals,
or substitution of another lookup type, catalog task code, or FSM execution
task code.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity or mutable data is missing or invalid | Show the exact field or conflict and stop before lookup or preview |
| The reference set, requested assignment, or code state is missing or ambiguous | Show sanitized identity and match evidence; request a corrected exact value or return ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES |
| SetId/SetCode is malformed, absent in the selected environment, conflicts with another selector or package row, confirmed Common Set resolves elsewhere, or a BU/organization assignment resolves to another reference group/set | Classify as input, lookup, or catalog/scope mismatch; disclose sanitized supplied and returned identities and stop before code lookup, package review, or preview |
| Fusion returns 401 or 403 | Refresh a cache-managed token at most once, then stop as authentication or privilege failure |
| A read-only call fails | Preserve sanitized endpoint and request evidence; retry only within the bounded core read policy |
| A core.data-loader FSM import fails or is uncertain | Do not replay; reconcile once by exact read and require a new package, preview, and later standalone approve |
| A direct REST mutation fails or is uncertain | Stop the ordered request list immediately. Do not retry, continue, roll back successful rows, or switch routes; reconcile every attempted row by exact read and require a new combined preview and approval before resuming |
| Delete is requested through FSM | Stop before package preparation; offer Disable or the documented direct REST exception |
| Create, Update, or Disable requests direct REST without verified same-target FND export unavailability evidence | Stop before preview until a classified receipt proves an unavailable/unusable exact-target export attempt; then continue through fresh direct REST reads and separate exact-preview approval, never from readability alone |
| A valid completed same-target full-task data export omits the fixed lookup parent and all its codes during FSM mutation preparation | Preserve COMPLETED status, baseline path/hash and catalog_mismatch evidence; return fallback_required before submission, then continue once through direct Apps Common REST with fresh parent/set/nonempty inventory and requested-row reads plus independent preview/approval unless constrained to FSM-only or Data Loader-only |
| The verified same-target export attempt fails before ProcessId, its process fails/times out, or its result is missing, malformed, narrowed, template-only, or returns wrong task/release metadata | Preserve the actual request/process status and classify the exact defect as EXPORT_REQUEST_FAILED, PROCESS_FAILED, PROCESS_TIMEOUT, COMPLETED_LOOKUP_OMISSION, or COMPLETED_UNUSABLE_EXPORT as applicable; return fallback_required for Create/Update/Disable and continue once through direct REST fresh-read validation. Do not use an unusable result as omission proof, parse unsafe ZIP content, or require a final FSM ZIP/task context. An old/cross-environment receipt or failed REST confirmation remains blocked |
| Package REST fallback has one invalid row | Block the entire combined preview; do not submit only the valid rows under a different or partial scope |
| One row in an approved REST fallback batch fails or becomes uncertain | Preserve verified prior successes, identify the failed/uncertain row and all unattempted rows, stop immediately, and require fresh reads plus a new preview and approval to resume |
| Export or import is constructed from MOO_MANAGE_WIN/LOSS_REASONS, including a URL-encoded slash workaround | Stop before the external call; retain this value only as the catalog/task-context identity and use FND_MANAGE_SET_ENABLED_LOOKUPS as the FSM execution task |
| A coordinator-task package changes a lookup type other than MOO_SETID_WIN_LOSS_REASON | Reject the package as scope-expanded; rebuild from the fresh export and preserve every unrelated member and row unchanged |
| An accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, or live lookup verification | Stop; accepted initiation is terminal and those reads require a later explicit status or results request |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field, operation, set selector, date, or mutable value is invalid | Correct the request and rerun validation |
| Catalog mismatch | LookupType is not MOO_SETID_WIN_LOSS_REASON or the catalog task identity is not MOO_MANAGE_WIN/LOSS_REASONS | Use this adapter's fixed catalog and lookup identities |
| Execution task mismatch | Requested export/import identity is wrong or a supplied final mutation package changes identity/unrelated content | Stop and correct the request or final package; do not infer export unavailability from invalid input. When a verified exact-target FND export returns mismatched task/release metadata, classify that returned result as COMPLETED_UNUSABLE_EXPORT and continue Create/Update/Disable through fresh direct REST validation before separate preview/approval |
| Completed lookup omission | A valid completed same-target full-task data-export baseline omits the fixed parent and codes | Record catalog_mismatch and fallback_required for Create/Update/Disable before submission; fresh exact parent/set/nonempty inventory and requested-row reads precede direct REST eligibility and separate approval; Export/Import stay FSM-only |
| REST fallback blocker | The unavailable/unusable receipt lacks exact-target attempt evidence or applicable fresh REST confirmation, is stale/cross-environment, or is being used for Export, Import, Delete, an explicit incompatible-route constraint, or after submission/uncertainty | Complete the exact receipt/fresh reads or correct the route; never invent eligibility or relabel an actual COMPLETED process as failed |
| Record-set prerequisite | A requested assignment is absent or incorrect | Complete ORA_MOO_MANAGE_OPPORTUNITY_RECORD_SET_VALUES, then rerun read-only resolution |
| Authentication or privilege | Fusion rejects access after the permitted token refresh | Reauthenticate or obtain required privileges |
| Transport or Fusion API | Connectivity or Fusion response prevents deterministic resolution | Correct the environment or request before a new preview |
| Approval blocker | A direct REST mutation lacks approval bound to its exact immutable preview, or the native FSM Data Loader lifecycle is incomplete | For REST fallback or Delete, approve the exact preview immediately before submission; changes/reordering invalidate approval. For usable native FSM, approval is not required before handoff; Data Loader owns its later preview and approval |
| Process timeout or failure | An FSM process times out or fails | Preserve process evidence, reconcile target state, and do not retry automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| FSM handoff | Environment, catalog identity MOO_MANAGE_WIN/LOSS_REASONS, execution identity FND_MANAGE_SET_ENABLED_LOOKUPS, operation, MOO_SETID_WIN_LOSS_REASON, SingleLookup set/state or every changed Win/Loss Reason row's set/state lock, unrelated-content preservation receipt, immutable package path, SHA-256, member summary, proposed rows, impact, and verification plan |
| Direct REST preview | Environment, catalog identity, operation, REST_FALLBACK or REST_DELETE, fixed lookup, classified export-unavailability reason and exact attempt/process/defect receipt when applicable, available baseline path/hash, applicable fresh-read confirmation, ordered row count, per-row set/state/method/endpoint/body/impact/verification GET, partial-success and stop-on-first-failure/no-rollback disclosure, and combined fingerprint |
| Failure or uncertainty | Failed stage and row, classification, sanitized status and identifiers, last known state, verified successful rows, failed/uncertain row, unattempted rows, possible side effects, what was not retried or rolled back, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Exact SingleLookup/per-row evidence is missing, REST fallback eligibility is unproven, or a REST mutation lacks its exact preview and approval | Do not submit direct REST or hand an incomplete native FSM package to Data Loader. REST fallback needs its own preview/approval, but no Data Loader task context, final FSM ZIP, loader-support check or Data Loader approval |
| The approved operation, identity, endpoint, body, package, or fingerprint changed | Do not reuse approval |
| A mutation or import failed or is uncertain | Do not retry automatically or claim Fusion is unchanged |
| A REST batch partially succeeds | Do not continue past the failed/uncertain row, automatically reverse prior successes, claim atomicity, or hide unattempted rows |
| Delete is selected with FSM | Do not prepare or submit an FSM delete row |
| Another lookup type, catalog task code, or execution task code is supplied | Do not substitute it into this adapter; do not use the slash-containing catalog code for FSM transport |
| Set identity is wrong, conflicting, or cross-environment | Do not substitute Common Set, choose a close match, rewrite a package row, or continue under a different set scope |
| Credentials, bearer tokens, or protected values are supplied | Do not print or persist them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.WIN_LOSS.GATE | decision | 8 | execution_gate | read_only->OPP.WIN_LOSS.RETURN_READ;rest_approved->OPP.WIN_LOSS.RETURN_REST_READY;fsm_handoff_ready->OPP.WIN_LOSS.RETURN_FSM_READY;accepted_initiation->OPP.WIN_LOSS.RETURN_ACCEPTED;export_ready->OPP.WIN_LOSS.RETURN_EXPORT_READY;missing->OPP.WIN_LOSS.RETURN_MISSING;failed->OPP.WIN_LOSS.RETURN_FAILED | OPP.WIN_LOSS.DESIGN | stop | Return read-only or validated export results, native FSM Data Loader handoff, or direct Apps Common REST readiness after exact-preview approval. Any unavailable/unusable exact-target FSM export selects direct REST fallback after applicable fresh reads; no registered loader capability/context/session is used for fallback. Never reuse another route approval |
| OPP.WIN_LOSS.RETURN_READ | terminal | 9 | terminal | none | OPP.WIN_LOSS.GATE | continue | Inventory or Read completed with exact parent, reference-group, pagination, set, assignment when requested, and lookup evidence |
| OPP.WIN_LOSS.RETURN_REST_READY | terminal | 10 | terminal | none | OPP.WIN_LOSS.GATE | continue | One exact REST Delete or ordered REST_FALLBACK Create/Update/Disable list has its separately approved immutable preview and is ready for Apps Common submission once per request with immediate per-row verification; stop on first failure/uncertainty, report partial outcomes and do not roll back automatically. No Data Loader capability, context, session, ZIP or approval is involved |
| OPP.WIN_LOSS.RETURN_FSM_READY | terminal | 11 | terminal | none | OPP.WIN_LOSS.GATE | continue | One unchanged FND_MANAGE_SET_ENABLED_LOOKUPS Create, Update, Disable, or Import ZIP with only reviewed MOO_SETID_WIN_LOSS_REASON changes, preserved unrelated content, exact catalog/execution identities, and resolved persisted catalog task context is ready for core.data-loader Task Hook validation and preview; no upload approval or execution has occurred |
| OPP.WIN_LOSS.RETURN_ACCEPTED | terminal | 12 | terminal | none | OPP.WIN_LOSS.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result retrieval, or live verification until a later explicit request |
| OPP.WIN_LOSS.RETURN_EXPORT_READY | terminal | 13 | terminal | none | OPP.WIN_LOSS.GATE | continue | The fresh complete FND_MANAGE_SET_ENABLED_LOOKUPS export baseline and its MOO_SETID_WIN_LOSS_REASON inventory are validated for review or package preparation under the Manage Win/Loss Reasons catalog context; no mutation package or upload approval is implied |
| OPP.WIN_LOSS.RETURN_MISSING | terminal | 14 | terminal | none | none | continue | Required input, exact parent/set/code state, impact, native FSM package/context evidence, fallback receipt/fresh reads or route-owned approval is missing. REST_FALLBACK always uses direct REST preview/approval and requires no Data Loader context/ZIP. Native FSM Data Loader approval belongs to its later session and is not required before handoff |
| OPP.WIN_LOSS.RETURN_FAILED | terminal | 15 | terminal | none | none | continue | Validation, parent/set/code lookup, package/fallback verification, handoff, execution, import, or later verification failed; for REST return successful, failed/uncertain, and unattempted row groups without retry or rollback |
| OPP.WIN_LOSS.RETURN_FALLBACK_REQUIRED | terminal | 16 | terminal | none | OPP.WIN_LOSS.VERIFY_PACKAGE | continue | Return RestFallbackRequired, classified FsmExportUnavailableReason for EXPORT_REQUEST_FAILED, PROCESS_FAILED, PROCESS_TIMEOUT, COMPLETED_LOOKUP_OMISSION, or COMPLETED_UNUSABLE_EXPORT, actual attempt/process status, sanitized exact-target receipt/defect and available artifact path/hash, unchanged requested rows/confirmed sets, and RestFallbackEligible=false. This terminal performs no external action. The invoking router continues the same mutation once as REST_FALLBACK for fresh parent/set/requested-row validation and additional nonempty inventory only for completed lookup omission, then direct Apps Common REST preview and separate approval. Do not re-export, query loader capability, require task context/final ZIP, reuse approval, or reroute after submission/uncertainty or an explicit incompatible-route constraint |
