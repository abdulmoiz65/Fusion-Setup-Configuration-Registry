# Manage Account Combinations Error Handling

Classify failures without retrying a package import or treating a resolver error as a not-found business value.

## Error Situations

| Situation | What Should Happen |
|---|---|
| CSV or ZIP validation fails | Return row and position evidence, correct locally, and restart at input validation. |
| COA lookup is zero or many matches | Report the exact supplied COA Name and match outcome; request a precise identifier. |
| COA lookup fails with auth, authorization, transport, paging, parsing, or client error | Preserve the failure class and sanitized detail; do not claim the COA is missing. |
| Required source or segment resolver is TBD | Stop at readiness and request the missing authoritative source or documented resolver. |
| Import process reports warning or error | Retrieve the documented process log and output through the selected execution workflow, correct the source artifact, and require a new preview and approval before another import. |
| Load Interface File for Import or Import Account Combinations reports warning or error | Review the returned log and output for affected rows, correct the source spreadsheet or CSV, remove failed interface data through the approved workflow when required, then create a new ZIP, preview, and approval. |
| Import outcome is uncertain | Do not resubmit. Reconcile through the selected read-only execution-status workflow first. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Candidate shape, column, mandatory-value, or package rule fails | Correct the candidate and validate again |
| catalog_or_metadata_mismatch | COA or segment metadata is absent, ambiguous, stale, or inconsistent | Supply exact authoritative metadata |
| auth_authz | A read-only lookup returns 401 or 403 | Refresh allowed authentication once, retry the same GET once, then stop |
| transport_environment | A read-only lookup has timeout, paging, or service failure | Use bounded GET retry only; otherwise stop |
| fusion_api | Fusion returns a semantic API error | Preserve response evidence and stop |
| process_failed | The interface load or account-combination import returns warning or error | Review returned process log/output, correct source rows, and use a fresh approved package |
| approval_blocker | Package, environment, preview, or approval evidence is missing or stale | Create the required exact preview and obtain current approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Row number, FBDI position, expected condition, observed sanitized value, and correction path |
| Lookup failure | Resolver name, exact source field, match count or sanitized failure class, and next action |
| Import handoff | Package hash, one-member inventory, import-group identifier, resolved structure-instance number, target environment, and current approval state |
| Process warning or error | Load or import request ID, returned status, affected rows when available, and the sanitized log/output location |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The task uses catalog CSV export/import flags of N | Do not use FSM import or export as a fallback |
| A package is invalid or an import is uncertain | Do not submit or resubmit an import automatically |
| A resolver is TBD or required source is absent | Do not guess defaults, segment count, identity, or lookup output |
| A request attempts to delete an account combination | Do not offer deletion; account combinations cannot be deleted |
| Approval has not been provided for the exact preview | Do not perform a live import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-060-EXECUTION-GATE | decision | 60 | execution_gate | ready->MAC-080-READY-FOR-HANDOFF;blocked->MAC-070-HANDLE-ERROR | MAC-050-ENFORCE-DESIGN | stop | Before FBDI execution handoff |
| MAC-070-HANDLE-ERROR | terminal | 70 | terminal | none | none | stop | A prior node reports invalid, unresolved, blocked, or failed |
| MAC-080-READY-FOR-HANDOFF | terminal | 80 | terminal | none | MAC-060-EXECUTION-GATE | stop | Verified package and current approval are ready for the selected execution workflow |
