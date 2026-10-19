# Manage Set Enabled Lookups Error Handling

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
cross-environment packages, assumed reference groups, or substitution of
another lookup category or task code.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required request mode, route, identity, mutable data, or task identity and persisted Data Loader task context is missing or invalid | Show the exact field or conflict and stop before lookup, export, package review, or preview |
| A lookup parent is missing, ambiguous, identity-mismatched, or returns blank ReferenceGroupName | Stop before set resolution; preserve sanitized evidence and never assume ReferenceGroupName from LookupType |
| A reference set, requested BU assignment, or current code state is missing or ambiguous | Show the sanitized type, returned reference group, set selector, and match count; request a corrected exact identity or return the owning record-set prerequisite |
| SetId/SetCode is malformed, not found in the selected environment, conflicts with another selector or package row, confirmed Common Set resolves to a non-Common set, or a BU/organization assignment resolves elsewhere | Classify as input, lookup-resolution, or catalog/scope mismatch; show sanitized supplied and returned identities and stop before code lookup, package review, or preview |
| A package-only Export or Import is blocked by a missing single selector or code | Correct the validation defect: package scope may cover both owned types and multiple rows, and each changed row is validated independently |
| A baseline is stale, wrong-target, wrong-release, wrong-task, failed, incomplete, or unavailable | Stop package authoring or handoff and obtain a fresh completed FND_MANAGE_SET_ENABLED_LOOKUPS export |
| Package metadata, safe ZIP shape, members, headers, row counts, row delta, hash, task identity and persisted Data Loader task context, or unrelated-row preservation fails | Report every exact mismatch, change no Fusion data, and rebuild from the fresh baseline |
| Any changed package row has an unsupported type or operation, unresolved set, stale state lock, unsupported field, immutable identity change, or missing impact | Block the complete package and report each invalid row; don't submit a partial subset under the reviewed fingerprint |
| Fusion returns 401 or 403 on a read | Refresh a repository-managed cached token at most once; then stop as authentication or privilege failure and don't report absence |
| A read-only call has a transport failure | Preserve sanitized endpoint and elapsed-time evidence; retry only within the bounded core read policy |
| Fusion returns another 4xx, a 5xx, or an identity-mismatched response | Preserve sanitized status, request identifier or ECID, and response summary; stop before preview |
| Core Data Loader preview, Task Hook envelope, archive hash binding, or later standalone approve is missing or stale | Stop before upload or initiation; let Data Loader rebuild its exact immutable lifecycle |
| Core Data Loader returns an accepted initiation | Return that accepted result immediately; don't poll, retrieve ProcessLog, or verify live state in the same request |
| A later explicit FSM status request times out or reports failure | Preserve ProcessId or requestId, last status, elapsed wait, and ProcessLog/status evidence when available; don't submit a replacement automatically |
| A direct REST mutation fails or its result is uncertain | Don't retry or switch to FSM; preserve sanitized HTTP evidence, reconcile once with the disclosed exact GET when safe, and require a new REST preview and approval for any later mutation |
| Delete is requested through FSM | Stop before package preparation; offer Disable or require explicitly selected, separately approved direct REST |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Request mode, operation, route, required field, selector, date, flag, or mutable value is invalid | Correct the request and rerun validation |
| Catalog mismatch | Lookup type, catalog task code, package task identity, or named-task ownership is unsupported | Use one directly owned type with FND_MANAGE_SET_ENABLED_LOOKUPS or route to the exact named adapter |
| Lookup resolution | Parent, returned reference group, set, assignment, or code can't be resolved deterministically | Supply exact identity or restore access, then rerun read-only resolution |
| Record-set prerequisite | A requested business unit isn't assigned to the required set under the parent-returned reference group | Complete the returned Opportunity or Revenue Record Set Values task, then rerun this workflow |
| Package readiness | Freshness, target/task identity and persisted Data Loader task context, ASM metadata, member/header contract, row delta, impact, state lock, or hash evidence fails | Refresh the export and rebuild the complete immutable package |
| Authentication or privilege | Fusion rejects access after the permitted cached-token refresh | Reauthenticate or obtain the exact Common Features or setup-task privilege |
| Transport or environment | Target, DNS, TLS, proxy, connection, or bounded read timeout fails | Restore the target and rerun only the read-only stage |
| Fusion API | Fusion returns a non-authentication error or mismatched response | Correct the endpoint, method, body, identity, or target before a new preview |
| Approval blocker | REST preview/approval is incomplete, or Data Loader Task Hook, hash binding, preview, or later standalone approve is absent or changed | Rebuild the route-specific immutable preview and obtain new approval through its owner |
| Process timeout or failure | A later explicit Data Loader status request times out or reports failure | Preserve status evidence and use the safe next-check path; don't resubmit automatically |
| Unverified REST result | A REST write may have completed but its exact verification GET failed | Report uncertainty and reconcile by read-only GET before considering another mutation |
| Artifact persistence | A package, readiness record, diagnostic, or run artifact can't be saved | Preserve safe diagnostics temporarily and report the intended project path |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read result | Environment, exact lookup parent, returned ReferenceGroupName, set, code scope, sanitized current state, and partial failures |
| Export handoff | Environment, FND_MANAGE_SET_ENABLED_LOOKUPS, target release, full task scope, and owning shared exporter |
| FSM package handoff | Environment, exact FND_MANAGE_SET_ENABLED_LOOKUPS task identity/TaskName, persisted Data Loader task-context fields, fresh baseline, operation/row scope, before/after states, impacts, immutable package path/SHA-256, metadata/member/header receipt, and verification plan |
| Data Loader preview | Data Loader owns the immutable upload preview, Task Hook validation envelope, finalData.archiveSha256 binding, and request for a later standalone approve; this skill must not reconstruct them |
| Accepted FSM initiation | Return only Core Data Loader's accepted-initiation result for this request; state that status, ProcessLog, or live verification needs a later explicit request |
| Direct REST preview | Environment, FND_MANAGE_SET_ENABLED_LOOKUPS, operation, lookup parent, returned reference group, set, before/after state, impact, exact method, returned item link or collection path, exact body or bodyless Delete, Upsert-Mode=false for Create, verification GET, and preview fingerprint |
| Later FSM failure or timeout | Failed stage, sanitized status and identifiers, last status, elapsed wait, ProcessLog/status evidence when available, possible side effects, what wasn't retried, and one safe next action |
| REST failure or uncertainty | Failed stage, sanitized method/path/status/identifier, last known state, possible side effects, verification outcome, what wasn't retried, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Parent ReferenceGroupName is blank or wasn't returned by the exact parent GET | Don't assume it equals LookupType or query BU assignments with a guessed reference group |
| No exact set, current-state lock, impact evidence, route-specific immutable preview, package evidence, or required approval lifecycle exists | Don't submit direct REST or a Core Data Loader FSM import |
| Operation, environment, identity, method, item link, body, package, task identity and persisted Data Loader task context, state lock, impact, or fingerprint changes after preview | Don't reuse approval; rebuild the applicable REST or Data Loader lifecycle |
| A live REST mutation or Data Loader import fails or is uncertain | Don't retry automatically or claim Fusion is unchanged. Unknown/pending/partial writes block route switching; terminal diagnosed wholly unchanged CSV work may use only the documented final fallback with new approval |
| Delete is selected with FSM | Don't prepare or submit a Delete row; use Disable or explicit direct REST |
| Package contains another adapter's lookup type or an invalid changed row | Don't submit the valid subset under the package's fingerprint |
| Data Loader initiation is accepted | Don't poll, fetch ProcessLog, or verify target state until the user makes a later explicit request |
| A request targets a standard, common, or generic lookup | Don't substitute the set-enabled endpoint or infer a reference set |
| A caller supplies credentials, bearer tokens, authorization headers, or protected values | Don't print, reuse, or persist them in diagnostics or artifacts |

## CSV Recovery and Final Fallback Errors

| Situation | What Should Happen |
|---|---|
| Valid full-data export is header-only or omits one/both owned seeded types | Preserve successful process status and apply exact omitted-parent recovery; do not infer live absence or declare fallback |
| Exact export fails/times out or remains unusable after recovery | Retain same-target receipt, actual last status, elapsed timeout, failure classification, recovery outcomes and safe next action; only documented exhaustion returns a candidate |
| Accepted import later fails or has no effect | On a later explicit results request retrieve status/errors/ProcessLog, require all jobs terminal and exact fresh unchanged state before considering fallback. No automatic import retry |
| All requested values applied, or a batch is partially applied | Return verified state without writing if all applied. Partial results stop and need a new remaining-change request |
| REST_FALLBACK eligible but approval missing | Prepare a separate exact immutable REST preview and obtain immediate approval; never reuse export/Data Loader approval |
| Any REST row fails, is uncertain or cannot be verified | Stop immediately; preserve prior successes and unattempted rows without retry, rollback or another fallback |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SET_LOOKUP.GATE | decision | 8 | execution_gate | read_only->OPP.SET_LOOKUP.RETURN_READ;export_ready->OPP.SET_LOOKUP.RETURN_EXPORT_READY;rest_approved->OPP.SET_LOOKUP.RETURN_REST_READY;fsm_handoff_ready->OPP.SET_LOOKUP.RETURN_FSM_READY;accepted_initiation->OPP.SET_LOOKUP.RETURN_ACCEPTED;missing->OPP.SET_LOOKUP.RETURN_MISSING;failed->OPP.SET_LOOKUP.RETURN_FAILED | OPP.SET_LOOKUP.DESIGN | stop | Return read-only results, route full-task Export, hand an immutable FSM package to Data Loader, allow one exact approved REST mutation, or terminate on Data Loader accepted initiation |
| OPP.SET_LOOKUP.RETURN_READ | terminal | 9 | terminal | none | OPP.SET_LOOKUP.GATE | continue | Inventory or Read is complete with exact parent, returned reference group, set, and lookup evidence and no mutation |
| OPP.SET_LOOKUP.RETURN_EXPORT_READY | terminal | 10 | terminal | none | OPP.SET_LOOKUP.GATE | continue | Full-task Package Export is validated for shared.setup-export.task-level-export without requiring one selector or code |
| OPP.SET_LOOKUP.RETURN_REST_READY | terminal | 11 | terminal | none | OPP.SET_LOOKUP.GATE | continue | One exact explicitly selected REST request or eligible ordered REST_FALLBACK batch with separate approval is ready for Apps Common, followed by its disclosed exact GET verification |
| OPP.SET_LOOKUP.RETURN_FSM_READY | terminal | 12 | terminal | none | OPP.SET_LOOKUP.GATE | continue | One exact immutable FND_MANAGE_SET_ENABLED_LOOKUPS package is ready for Core Data Loader Task Hook preview and later standalone approve |
| OPP.SET_LOOKUP.RETURN_ACCEPTED | terminal | 13 | terminal | none | OPP.SET_LOOKUP.GATE | continue | Core Data Loader returned an accepted initiation, which ends this request without polling, ProcessLog retrieval, or live verification |
| OPP.SET_LOOKUP.RETURN_MISSING | terminal | 14 | terminal | none | none | continue | Required input, lookup evidence, prerequisite, package evidence, state lock, impact, or evidence owned by the current preview, Task Hook, hash-binding, or approval stage is missing |
| OPP.SET_LOOKUP.RETURN_FAILED | terminal | 15 | terminal | none | none | continue | Validation, lookup, dependency, design, handoff, REST execution, Data Loader initiation, later status, or verification failed |
| OPP.SET_LOOKUP.RETURN_FALLBACK_REQUIRED | terminal | 16 | terminal | none | OPP.SET_LOOKUP.DEPENDENCY | continue | Applicable CSV recovery is exhausted with a classified same-target receipt and fully reconciled unchanged prior submissions; RestFallbackEligible=false. Router resumes unchanged rows/sets once with fresh reads; no REST approval implied |
| OPP.SET_LOOKUP.RETURN_VERIFIED | terminal | 17 | terminal | none | OPP.SET_LOOKUP.VERIFY_FALLBACK | continue | Fresh complete reconciliation confirms every requested value already applied and no pending/uncertain import; return verified result without another mutation |
