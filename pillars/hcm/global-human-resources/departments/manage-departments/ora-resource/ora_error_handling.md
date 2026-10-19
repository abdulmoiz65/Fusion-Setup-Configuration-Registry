# Manage Departments Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| DEPT-01 | The departments REST response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| DEPT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| DEPT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| DEPT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| DEPT-02 | Read, edit, inactivate, or delete-effective-split returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| DEPT-03 | Create finds an exact existing Department | Input validation | Stop the duplicate create |
| DEPT-03A | A date-effective split deletion lacks a resolved OrganizationId unique reference, operation-required OrgUnitClassification association, exact retained start, aligned deletion end, safe predecessor row, or generated Organization loader directive | Input validation | Stop; re-read the Department and history, then rebuild the Organization and classification MERGE rows with the resolved OrganizationId and `SET PURGE_FUTURE_CHANGES Y` only when the current generated loader contract exposes it |
| DEPT-03B | Post-delete history differs from the confirmed split-range removal and preceding-boundary change | Process failed | Stop without retry and report failed verification |
| DEPT-03C | The history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |
| DEPT-04 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| DEPT-05A | An EFF category, context discriminator, or multirow unique key is incomplete or inconsistent | Input validation | Stop and correct the OrgInformation row |
| DEPT-06 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| DEPT-06A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| DEPT-07 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| DEPT-07A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected departments |
| DEPT-07B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| DEPT-07C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, or EFF row is invalid or ambiguous | Correct the input and restart from target resolution |
| Catalog mismatch | A required REST response is missing or Core Data Loader reports unavailable or stale metadata | Correct the reported contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the declared history request | Report the sanitized response and correct the request before retry |
| Artifact persistence | Core Data Loader reports that the reviewed source cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile Department state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Department rows without assuming rollback |
| Approval blocker | Current source fingerprint and the reason approval is missing or stale |
| Delete eligibility | Department basic details, retained effective start, and inclusive deletion end only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key or target is unresolved | Do not infer or invent a value |
| A date-effective split deletion is requested | Do not use an HDL DELETE instruction or delete the logical Department record; use only a reviewed Organization MERGE range with `SET PURGE_FUTURE_CHANGES Y` when the current generated loader contract exposes it |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPT.ROUTE | decision | 7 | execution_gate | read->DEPT.DONE;create_or_edit_or_inactivate_or_delete_ready->DEPT.LOADER_READY;mutation_blocked->DEPT.ERROR | DEPT.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| DEPT.ERROR | step | 8 | error_handler | stopped->DEPT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| DEPT.DONE | terminal | 9 | terminal | none | DEPT.ROUTE | continue | Read completed |
| DEPT.LOADER_READY | terminal | 10 | terminal | none | DEPT.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| DEPT.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
