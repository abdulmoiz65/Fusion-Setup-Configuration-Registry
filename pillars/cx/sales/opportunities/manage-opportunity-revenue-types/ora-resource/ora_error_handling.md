# Manage Opportunity Revenue Types Error Handling

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Stop before undocumented writes, automatic mutation retries, stale approvals,
or substitution of another lookup type or FSM task code.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity or mutable data is missing or invalid | Show the exact field or conflict and stop before lookup or preview |
| The reference set, requested assignment, or code state is missing or ambiguous | Show sanitized identity and match evidence; request a corrected exact value or return ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES |
| SetId/SetCode is malformed, absent in the selected environment, conflicts with another selector or package row, confirmed Common Set resolves elsewhere, or a BU/organization assignment resolves to another reference group/set | Classify as input, lookup, or catalog/scope mismatch; disclose sanitized supplied and returned identities and stop before code lookup, package review, or preview |
| Fusion returns 401 or 403 | Refresh a cache-managed token at most once, then stop as authentication or privilege failure |
| A read-only call fails | Preserve sanitized endpoint and request evidence; retry only within the bounded core read policy |
| A successful exact-task data export has header-only CSVs | Do not relabel the process as failed or infer an empty live lookup. Validate the archive contract, then prepare Create using the task skill's Header-Only FSM Baselines and Parent Linkage procedure and fresh parent/set/code evidence |
| The final package has a child code without its matching parent row | Stop before Data Loader handoff as input validation; include the unchanged existing-parent linkage row. Fusion may otherwise skip the child even when that parent exists live |
| The parent cannot be resolved exactly or its required exported fields are missing or conflicting | Stop as input validation or catalog mismatch; do not invent parent fields, substitute another task's export, change seeded parent configuration, or switch execution routes |
| A core.data-loader FSM import fails, has no effect, or is uncertain | Do not replay. On a later explicit results request, retrieve prescribed status/errors/ProcessLog and reconcile every requested row. Only terminal, fully diagnosed, wholly unchanged work with documented CSV exhaustion may enter the final Apps Common fallback; pending/uncertain/partial results block it. A new FSM attempt needs a new package, preview and approval |
| A direct REST mutation fails or is uncertain | Do not retry or switch routes; reconcile once by exact read and require a new REST preview and approval |
| Delete is requested through FSM | Stop before package preparation; offer Disable or the documented direct REST exception |
| Create, Update, or Disable requests direct REST without final CSV exhaustion | Stop before preview; use exact-task FSM and applicable header-only/parent recovery first |
| The approved exact-task export fails, exceeds its polling window, or cannot provide a safe usable baseline | Preserve actual failure/timeout, request fingerprint, same-target receipt and applicable recovery outcomes. Only documented CSV exhaustion may return fallback_required; input/catalog/auth/approval/context gaps remain blockers |
| A valid header-only baseline or repairable missing parent is treated as fallback eligibility | Reject fallback and complete the CSV procedure; zero rows and an invalid child-only package do not exhaust FSM |
| Final fallback has complete exhaustion evidence and fresh unchanged state | Route once to core.fusion-api.apps-common then Lookups with a separate immutable REST preview and immediate approval; never reuse export/Data Loader approval |
| Reconciliation shows all requested values already applied or some rows applied | Return a verified result without writing if all are applied. For partial results stop, retain successes and require a new reviewed request for remaining changes; do not replay the original batch |
| An accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, or live lookup verification | Stop; accepted initiation is terminal and those reads require a later explicit status or results request |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field, operation, set selector, date, or mutable value is invalid | Correct the request and rerun validation |
| Catalog mismatch | LookupType is not MOO_SETID_REVENUE_TYPE or the package task code is not MOO_MANAGE_REVENUE_TYPES | Use this adapter's fixed identities |
| Record-set prerequisite | A requested assignment is absent or incorrect | Complete ORA_MOO_MANAGE_REVENUE_RECORD_SET_VALUES, then rerun read-only resolution |
| Authentication or privilege | Fusion rejects access after the permitted token refresh | Reauthenticate or obtain required privileges |
| Transport or Fusion API | Connectivity or Fusion response prevents deterministic resolution | Correct the environment or request before a new preview |
| Approval blocker | A REST mutation lacks separate immediate exact-preview approval, or a post-handoff Data Loader preview/approval lifecycle is incomplete | Approve the exact REST preview before its submission; missing or declined approval cannot trigger fallback. FSM pre-preview handoff does not require Data Loader approval yet |
| Process timeout or failure | An FSM process times out, fails, or completes without the requested effect | Preserve actual process evidence and reconcile target state without automatic retry. Export timeout may qualify after the polling window; import timeout/uncertainty never qualifies until all jobs are terminal and full reconciliation passes |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| FSM handoff | Environment, MOO_MANAGE_REVENUE_TYPES, operation, MOO_SETID_REVENUE_TYPE, SingleLookup set/state or every package row's set/state lock, immutable package path, SHA-256, member summary, proposed rows, impact, and verification plan |
| REST preview | Final CSV failure/recovery and prior-submission reconciliation evidence when applicable; environment, MOO_MANAGE_REVENUE_TYPES, operation, MOO_SETID_REVENUE_TYPE, each resolved set/code and current/proposed state, ordered row count, method, endpoint, writable body or no-body delete, impact, verification GET, and immutable preview fingerprint |
| Failure or uncertainty | Failed stage, classification, sanitized status and identifiers, last known state, possible side effects, what was not retried, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Exact SingleLookup or per-row evidence is missing, or a REST mutation lacks its exact preview and approval | Do not submit REST or hand an incomplete FSM package to Data Loader; absence of Data Loader approval before its preview is expected and must not block handoff |
| The approved operation, identity, endpoint, body, package, or fingerprint changed | Do not reuse approval |
| A mutation or import failed or is uncertain | Do not retry automatically or claim Fusion is unchanged |
| Delete is selected with FSM | Do not prepare or submit an FSM delete row |
| Another lookup type or task code is supplied | Do not substitute it into this adapter |
| Set identity is wrong, conflicting, or cross-environment | Do not substitute Common Set, choose a close match, rewrite a package row, or continue under a different set scope |
| Credentials, bearer tokens, or protected values are supplied | Do not print or persist them |
| Fallback evidence is missing/stale/cross-target, CSV is repairable, the request requires FSM-only, or prior submissions are pending/uncertain/partial | Do not switch routes, synthesize eligibility, skip CSV recovery, reinterpret Import as REST, or repeat a write to obtain failure evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.REVENUE_TYPE.GATE | decision | 9 | execution_gate | read_only->OPP.REVENUE_TYPE.RETURN_READ;rest_approved->OPP.REVENUE_TYPE.RETURN_REST_READY;fsm_handoff_ready->OPP.REVENUE_TYPE.RETURN_FSM_READY;accepted_initiation->OPP.REVENUE_TYPE.RETURN_ACCEPTED;export_ready->OPP.REVENUE_TYPE.RETURN_EXPORT_READY;missing->OPP.REVENUE_TYPE.RETURN_MISSING;failed->OPP.REVENUE_TYPE.RETURN_FAILED | OPP.REVENUE_TYPE.DESIGN | stop | Return read-only or Export evidence without mutation; validated native FSM packages go to Data Loader and terminate at accepted initiation. REST_FALLBACK needs dedicated eligibility and separate immediate exact-preview approval; REST_DELETE needs its explicit no-body DELETE approval. Both use Apps Common once and exact disclosed verification |
| OPP.REVENUE_TYPE.RETURN_READ | terminal | 10 | terminal | none | OPP.REVENUE_TYPE.GATE | continue | Inventory or Read completed with exact parent, reference-group, pagination, set, assignment when requested, and lookup evidence |
| OPP.REVENUE_TYPE.RETURN_REST_READY | terminal | 11 | terminal | none | OPP.REVENUE_TYPE.GATE | continue | Separately approved eligible REST_FALLBACK Create/Update/Disable requests or explicit REST_DELETE are ready for Apps Common; submit each displayed request once, verify immediately and stop on first failure/uncertainty |
| OPP.REVENUE_TYPE.RETURN_FSM_READY | terminal | 12 | terminal | none | OPP.REVENUE_TYPE.GATE | continue | One unchanged MOO_MANAGE_REVENUE_TYPES Create, Update, Disable, or Import ZIP, exact task identity, and resolved persisted Data Loader task context are ready for core.data-loader Task Hook validation and preview; no upload approval or execution has occurred |
| OPP.REVENUE_TYPE.RETURN_ACCEPTED | terminal | 13 | terminal | none | OPP.REVENUE_TYPE.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result retrieval, or live verification until a later explicit request |
| OPP.REVENUE_TYPE.RETURN_EXPORT_READY | terminal | 14 | terminal | none | OPP.REVENUE_TYPE.GATE | continue | The fresh MOO_MANAGE_REVENUE_TYPES export baseline is validated for review or package preparation; no mutation package or upload approval is implied |
| OPP.REVENUE_TYPE.RETURN_MISSING | terminal | 15 | terminal | none | none | continue | Required input, parent/set/code evidence, prerequisite, impact, FSM package/context, fallback exhaustion/reconciliation, or separate REST approval is missing; Data Loader approval is not required before FSM handoff |
| OPP.REVENUE_TYPE.RETURN_FAILED | terminal | 16 | terminal | none | none | continue | Validation, parent/set/code lookup, package or fallback verification, handoff, execution, import, or later explicit verification failed; no retry or route switch is authorized |
| OPP.REVENUE_TYPE.RETURN_FALLBACK_REQUIRED | terminal | 17 | terminal | none | OPP.REVENUE_TYPE.VERIFY_PACKAGE | continue | Applicable CSV recovery is exhausted for Create/Update/Disable with a classified same-target receipt and reconciled prior submissions; RestFallbackEligible=false. Return unchanged intent/rows/sets for one router resume as REST_FALLBACK with fresh reads and its dedicated verifier; no REST write is approved |
| OPP.REVENUE_TYPE.RETURN_VERIFIED | terminal | 18 | terminal | none | OPP.REVENUE_TYPE.VERIFY_FALLBACK | continue | Complete fresh reconciliation proves every requested value is already applied and no import job or write remains pending/uncertain; return the verified result without another mutation |
