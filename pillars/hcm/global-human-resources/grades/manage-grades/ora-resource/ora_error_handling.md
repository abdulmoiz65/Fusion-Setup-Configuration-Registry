# Manage Grades Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| GRD-01 | The Grade REST read contract is missing or incompatible | Catalog mismatch | Stop and record the capability gap with owner, task impact, approved fallback, and disposition |
| GRD-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| GRD-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| GRD-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| GRD-02 | Read, edit, inactivate, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| GRD-02D | A Grade parent delete does not distinguish zap from effective-split deletion | Input validation | Stop before authoring and require one explicit delete mode; do not infer purge scope |
| GRD-02E | Effective-split history is incomplete, the selected row is first or ambiguous, or its predecessor and end boundary cannot be derived exactly | Input validation | Stop before authoring; refresh every GradeHistoryDef page and select one exact non-first split |
| GRD-03 | Create finds an exact existing Grade | Input validation | Stop the duplicate create |
| GRD-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| GRD-05 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| GRD-06 | A date-effective split deletion lacks an exact retained start, aligned deletion end, or safe predecessor row | Input validation | Stop; re-read Grade history and rebuild the bounded `MERGE` range with `SET PURGE_FUTURE_CHANGES Y` |
| GRD-06A | The Grade history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |
| GRD-06B | Post-delete history differs from the confirmed split-range removal and preceding-boundary change | Process failed | Stop without retry and report the failed verification |
| GRD-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| GRD-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| GRD-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and errors; after a partial create, read the Grade and prepare an edit with its base row and only failed children; do not replay create |
| GRD-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| GRD-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, or EFF row is invalid or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | The registered loader object does not support the mutation | Restore the loader contract before authoring |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the declared history request | Report the sanitized response and correct the request before retry |
| Artifact persistence | Core Data Loader reports that the reviewed source or immutable artifact cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Capability gap | Owner, affected task, impact, approved fallback when one exists, and disposition |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Grade rows without assuming rollback |
| Delete eligibility | Grade code or name, retained effective start, and inclusive deletion end only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A read or platform capability is unavailable | Do not infer or substitute a capability without a declared approved route |
| The declared Data Loader route is unavailable | Do not substitute a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key or target is unresolved | Do not invent a value |
| A Grade zap is requested | Do not use `MERGE`, include split-range directives, or mix `DELETE` and `MERGE` for that logical Grade in one file |
| A Grade effective-split delete is requested | Do not use `DELETE`, delete the first split, copy the selected row's start as the `MERGE` start, or proceed without complete GradeHistoryDef evidence |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.ROUTE | decision | 7 | execution_gate | read->GRD.DONE;create_or_edit_or_inactivate_or_split_delete_ready->GRD.LOADER_READY;mutation_blocked->GRD.ERROR | GRD.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| GRD.ERROR | step | 8 | error_handler | stopped->GRD.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| GRD.DONE | terminal | 9 | terminal | none | GRD.ROUTE | continue | Read completed |
| GRD.LOADER_READY | terminal | 10 | terminal | none | GRD.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| GRD.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
