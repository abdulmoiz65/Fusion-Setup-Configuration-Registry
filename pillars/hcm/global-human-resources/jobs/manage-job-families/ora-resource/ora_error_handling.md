# Manage Job Families Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| JF-01 | The jobFamiliesV2 REST response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| JF-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| JF-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| JF-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| JF-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| JF-03 | Create finds an exact existing Job Family | Input validation | Stop the duplicate create |
| JF-04 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| JF-05 | XLSX or DAT includes an unmodified JobSubFamilyAssociation object | Input validation | Remove its worksheet and Data Loader Map row, then regenerate the DAT internally |
| JF-06 | A multi-record Job Family delete does not distinguish effective-split from zap | Input validation | Stop before authoring and require one explicit delete mode; a resolved single date-effective record routes to zap |
| JF-06A | Job reference evidence is incomplete, unsupported, or finds one or more references | Input validation | Stop before authoring; resolve complete zero-reference evidence |
| JF-06B | Effective-split evidence is incomplete, the selected row is first, nonfinal, nonfuture, or ambiguous, or its retained boundary cannot be derived exactly | Input validation | Stop before authoring; refresh the Job Family finder evidence and select one final future split |
| JF-07 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| JF-07A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| JF-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| JF-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected job families |
| JF-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| JF-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, or modified-object scope is invalid | Correct the input or source scope and restart resolution |
| Catalog mismatch | A required REST response is missing or Core Data Loader reports unavailable or stale metadata | Correct the reported contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | Core Data Loader reports that the reviewed source cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Modified-object scope | The unmodified JobSubFamilyAssociation worksheet and Data Loader Map row that must be removed |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Job Family rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key or target is unresolved | Do not infer or invent a value |
| JobSubFamilyAssociation was not modified | Do not retain its worksheet or Data Loader Map row |
| A Job Family zap is requested | Do not add `RestAction` to the XLSX, use `MERGE`, include child rows or a split directive, mix `DELETE` and `MERGE`, or bypass failed current live Data Loader validation of the native DAT |
| A Job Family effective-split delete is requested | Do not use `DELETE`, remove the first or a nonfinal/nonfuture split, copy the selected row's start as the `MERGE` start, or proceed without complete finder and zero-reference evidence |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JF.ROUTE | decision | 6 | execution_gate | read->JF.DONE;create_or_edit_or_delete_ready->JF.LOADER_READY;mutation_blocked->JF.ERROR | JF.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| JF.ERROR | step | 7 | error_handler | stopped->JF.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| JF.DONE | terminal | 8 | terminal | none | JF.ROUTE | continue | Read completed |
| JF.LOADER_READY | terminal | 9 | terminal | none | JF.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| JF.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
