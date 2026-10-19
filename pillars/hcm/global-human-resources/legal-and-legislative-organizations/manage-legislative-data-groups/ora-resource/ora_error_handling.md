# Manage Legislative Data Groups Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| LDG-01 | The legislativeDataGroups resource or response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the internal resource contract |
| LDG-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| LDG-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| LDG-01C | A required read or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| LDG-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| LDG-03 | Create returns one or more exact Name matches | Input validation | Stop and require a unique Name |
| LDG-04 | Country or default Currency cannot be resolved, or Currency differs from the default | Input validation | Stop before preview and require one exact Country with its default Currency |
| LDG-05 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| LDG-05A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| LDG-06 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| LDG-06A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected legislative data groups |
| LDG-06B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| LDG-06C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| LDG-07 | Delete does not resolve one exact target | Input validation | Stop and request one precise business selector |
| LDG-07A | A zap-delete source lacks a fresh LegislativeDataGroupId, serializes MERGE instead of DELETE, or includes dates, split directives, country, currency, child, EFF, or source-system-key values | Input validation | Stop before preview; re-read the exact target and rebuild one root-only DELETE row using its returned locator |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, create Name, Country, Currency, or loader key is invalid or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | An internal read is missing or Core Data Loader reports unavailable or stale metadata | Correct the reported contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile LDG state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Country or Currency failure | Supplied Country and Currency, required default relationship, and unresolved field without exposing internal IDs |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Delete blocker | Exact target identity, required root-only DELETE row, preview status, and approval status |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| Country, Currency, or target is unresolved | Do not infer or invent a value |
| Delete gates are incomplete | Do not prepare or submit the delete |
| A delete is requested | Do not ask for source-system keys, effective dates, delete mode, split history, country, currency, child, or EFF data; do not use MERGE or any row beyond the one root DELETE row |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDG.ROUTE | decision | 7 | execution_gate | read->LDG.DONE;create_or_edit_ready->LDG.LOADER_READY;create_or_edit_blocked->LDG.ERROR;delete_ready->LDG.LOADER_READY;delete_blocked->LDG.ERROR | LDG.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| LDG.ERROR | step | 8 | error_handler | stopped->LDG.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| LDG.DONE | terminal | 9 | terminal | none | LDG.ROUTE | continue | Read completed |
| LDG.LOADER_READY | terminal | 10 | terminal | none | LDG.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| LDG.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
