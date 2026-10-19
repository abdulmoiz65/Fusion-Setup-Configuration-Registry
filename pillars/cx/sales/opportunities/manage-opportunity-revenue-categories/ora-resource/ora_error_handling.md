# Manage Opportunity Revenue Categories Error Handling

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

Stop before any undocumented write, incomplete package handoff, automatic
retry, premature status polling, or interpretation of a runtime opportunity
field as setup metadata.

## Error Situations

| Situation | What Should Happen |
| --- | --- |
| Create finds an existing code, or Update, Disable, or Read finds no exact code | Show the operation, LookupCode, lookup type MOO_REVN_CATEGORY, and sanitized current-state result; require a corrected operation or identity |
| The fixed MOO_REVN_CATEGORY parent lookup type is absent or mismatched | Classify as catalog mismatch or Fusion API failure and stop; do not create or substitute a lookup type |
| The resolved CustomizationLevel or seed-data state disallows the requested mutation | Show sanitized configuration metadata and stop before preview or execution |
| Fusion returns 401 or 403 during the standard-lookup read | Classify as authentication or privilege failure and stop; do not try another lookup category |
| DNS, TLS, connection, or read timeout prevents either standard-lookup request from receiving a valid response | Classify as transport or environment failure, preserve sanitized endpoint and elapsed-time evidence, and stop before preview |
| The parent request returns 404, or the code-item request returns 404 | Treat parent 404 as catalog mismatch; treat code-item 404 as normal not-found evidence for operation-sensitive design evaluation |
| Fusion returns a non-authentication 4xx, a 5xx, or a malformed or identity-mismatched payload | Classify as Fusion API failure, preserve sanitized status and request identifiers, and stop without substituting another resource |
| A reference set, business unit, or MOO_SETID_REVN_CATEGORY is supplied as category scope | Show that this task uses standard lookup MOO_REVN_CATEGORY and stop before preview |
| A direct REST, browser, shared setup import, or other non-Data-Loader write route is proposed | Refuse before the external call; Apps Common is GET-only for this task and supported writes use the exact FSM package |
| Changed child rows are packaged without exactly one matching current MOO_REVN_CATEGORY row in FND_APP_STANDARD_LOOKUP.csv | Block before preview; Fusion skips orphan child rows even when the outer Data Loader status later reports success |
| Fresh export, exact task identity and persisted Data Loader task context, ASM identity, members, headers, parent-child closure, row delta, state lock, impact, preservation, immutable path, or reopened final SHA-256 is missing or inconsistent | Block the complete package before Data Loader handoff; obtain a fresh export and rebuild rather than repairing or partially submitting it |
| A Core Data Loader FSM import fails or its outcome is uncertain | Do not retry or switch to REST; preserve process evidence, reconcile the exact code through one read-only lookup, and require a new package, Data Loader preview, and later standalone approve before any later import |
| Accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, or exact lookup verification | Stop; accepted initiation is terminal and those reads require a later explicit status or results request |
| A later explicit status or results request is received | Use Core Data Loader's status/results path, retrieve and inspect the FSM ProcessLog even when outer counts say Succeeded, require the expected setup-object row count with no warnings or skips, then verify affected MOO_REVN_CATEGORY rows by exact GET; do not resubmit automatically |
| Data Loader reports Succeeded or one loaded row but the FSM ProcessLog says Completed with warnings, Parent row is missing, Row will be skipped, or Total Objects Processed is 0 | Classify the task import as failed or uncertain, disclose the ProcessLog evidence, do not claim the category was created, and reconcile by exact GET before preparing a new package |

## Error Classifications

| Result Category | When Used | Next Action |
| --- | --- | --- |
| Input validation | Required identity, operation, mutable field, field constraint, or date rule is missing or invalid | Correct the supplied revenue-category fields and rerun validation |
| Design validation | The parent customization level, seed-data state, or current code state does not permit the requested operation | Choose a permitted operation or code; never bypass the lookup configuration level |
| Catalog mismatch | Fusion does not expose the fixed MOO_REVN_CATEGORY parent lookup type or returns a different identity | Confirm the target environment and catalog version; do not create or substitute another lookup type |
| Lookup resolution | Current MOO_REVN_CATEGORY state cannot be resolved exactly | Correct the LookupCode or restore read access, then rerun the standard-lookup lookup |
| Authentication or privilege | Fusion rejects the read-only standard-lookup request with 401 or 403 | Reauthenticate or obtain the required Application Common Features access before retrying |
| Transport or environment | DNS, TLS, connection, proxy, or timeout failure prevents a valid read-only Fusion response | Verify the exact environment base URL and network path; rerun only the read-only lookup after connectivity is restored |
| Fusion API | A non-authentication 4xx, 5xx, malformed payload, or response-identity mismatch prevents deterministic lookup evaluation | Preserve sanitized HTTP status and request identifiers, verify the documented endpoint and environment, and do not continue to preview or mutation |
| Package readiness | Export freshness, target/release/task identity, task identity and persisted Data Loader task context, ASM/member/header contract, exact parent-child closure, row delta, state lock, impact, preservation, or final hash fails | Refresh the export and rebuild the complete immutable package with one matching parent carrier row before a new handoff |
| Unsupported execution route | A REST mutation, browser write, shared setup import, or direct import endpoint is proposed | Refuse the route and use core.data-loader with the exact FSM package |
| Approval blocker | A post-handoff Data Loader Task Hook preview, hash binding, or later standalone approval is missing or stale | Let Data Loader rebuild its lifecycle; no Data Loader approval is required before this child hands off a ready package |
| FSM process timeout or failure | Data Loader submission, polling, process execution, result retrieval, or verification did not complete successfully | Preserve ProcessId or requestId, last status, elapsed time, and ProcessLog when available; reconcile once and require a new package, Data Loader preview, and later standalone approve |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| FSM package handoff | Environment, MOO_MANAGE_REVENUE_CATEGORIES, exact TaskName/task identity, persisted Data Loader task-context fields, target release, fresh export receipt, operation scope, affected codes/state locks/deltas/impact/preservation, immutable package path/SHA-256, ASM/member/header receipt, and verification plan; no child-owned approval |
| Accepted FSM initiation | Return only Core Data Loader's accepted initiation result and state that status, ProcessLog, results, and exact GET verification require a later explicit request |
| Later FSM status or results | Environment, task and operation, external IDs, outer loader status and counts, FSM ProcessLog completion state, processed/succeeded/failed/warning/skip counts, ProcessLog artifact reference, and exact GET verification result; outer Succeeded alone is not task success |
| Failure or uncertain result | Selected route, failed stage, failure classification, sanitized status and identifiers, last known state, elapsed wait when applicable, whether configuration may have changed, what was not retried, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
| --- | --- |
| Exact lookup or per-row state evidence, impact, fresh export, task identity and persisted Data Loader task context, package contract, matching parent carrier row, parent-child closure, preservation, or reopened final hash is missing | Do not hand an incomplete package to Data Loader; absence of Data Loader approval before its preview is expected and must not block a complete handoff |
| Outer Data Loader counters report success while the FSM ProcessLog reports warnings, skipped rows, or zero processed objects | Do not report the task as successful or verified; use the ProcessLog and exact lookup read as the authoritative task outcome |
| A Data Loader import fails or has an uncertain outcome | Do not retry automatically; reconcile MOO_REVN_CATEGORY with a read-only lookup before preparing a new package for a new Data Loader preview and later standalone approve |
| Any direct REST mutation or other non-Data-Loader write route is requested | Do not build a REST preview, request REST approval, call POST/PATCH/PUT/DELETE, or substitute another executor |
| Set-enabled lookup input or MOO_SETID_REVN_CATEGORY is supplied | Do not redirect this task to setEnabledLookups or infer a reference set |
| A caller asks to delete a revenue-category code | Do not invoke DELETE; this task supports Disable only as an FSM package row with EnabledFlag=N |
| Data Loader initiation is accepted | Do not poll, retrieve ProcessLog/results, or verify live state until a later explicit request |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.GATE | decision | 7 | execution_gate | fsm_handoff_ready->OPP.REVENUE_CATEGORY.RETURN_FSM_READY;accepted_initiation->OPP.REVENUE_CATEGORY.RETURN_ACCEPTED;missing->OPP.REVENUE_CATEGORY.RETURN_MISSING;failed->OPP.REVENUE_CATEGORY.RETURN_FAILED | OPP.REVENUE_CATEGORY.DESIGN | stop | Hand the validated immutable package to Core Data Loader without child approval, or route Data Loader's accepted initiation to its terminal result |
| OPP.REVENUE_CATEGORY.RETURN_FSM_READY | terminal | 8 | terminal | none | OPP.REVENUE_CATEGORY.GATE | continue | The unchanged immutable MOO_MANAGE_REVENUE_CATEGORIES package, exact task identity and persisted Data Loader task context, reviewed rows, and reopened SHA-256 are ready for Core Data Loader Task Hook validation and preview; no import approval or execution has occurred |
| OPP.REVENUE_CATEGORY.RETURN_ACCEPTED | terminal | 9 | terminal | none | OPP.REVENUE_CATEGORY.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog or result retrieval, or exact GET verification |
| OPP.REVENUE_CATEGORY.RETURN_READ | terminal | 10 | terminal | none | OPP.REVENUE_CATEGORY.DESIGN | continue | A SingleLookup Read resolved one exact code and returns sanitized current state without mutation approval |
| OPP.REVENUE_CATEGORY.RETURN_EXPORT_READY | terminal | 11 | terminal | none | OPP.REVENUE_CATEGORY.DESIGN | continue | The completed full-task MOO_MANAGE_REVENUE_CATEGORIES export baseline is validated for review or package authoring without LookupCode scope |
| OPP.REVENUE_CATEGORY.RETURN_MISSING | terminal | 12 | terminal | none | none | continue | Required input, lookup evidence, package evidence, task identity and persisted Data Loader task context, state lock, impact, preservation, or current-stage Data Loader evidence is missing; approval is not required before FSM handoff |
| OPP.REVENUE_CATEGORY.RETURN_FAILED | terminal | 13 | terminal | none | none | continue | Validation, parent/code lookup, package readiness, design, execution handoff, Data Loader initiation, later status/results, or verification failed |
