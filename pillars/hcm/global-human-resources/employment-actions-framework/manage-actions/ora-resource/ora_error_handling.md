# Manage Actions Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| ACT-01 | The Action REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| ACT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| ACT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| ACT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| ACT-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| ACT-03 | The Data Loader contract is missing or stale | Catalog mismatch | Stop before source generation and restore the current contract |
| ACT-03A | Source validation is missing or stale | Input validation | Stop and revalidate the complete source |
| ACT-03B | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| ACT-04 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| ACT-04A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected actions |
| ACT-04B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| ACT-04C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| ACT-05 | An Action, association, Country, or role reference has zero or multiple compatible matches | Input validation | Stop and request one exact business selector; never select by position |
| ACT-06 | Source contains a generated ID, unsupported field, partial key, or invented mapping shape | Catalog mismatch | Stop and rebuild a registered-object-supported source shape |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target or supplied reference is missing, ambiguous, or incompatible | Correct the selector and restart resolution |
| Catalog mismatch | Source shape or requested fields differ from the registered Actions contract | Correct the source from the current contract |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Action or association rows without assuming rollback |
| Approval blocker | Current source fingerprint and the reason approval is missing or stale |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not substitute a REST write, FSM import, CSV omission, or another route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A target or reference is unresolved | Do not choose a match by position or invent a value |
| Source shape is unsupported | Do not invent a mapping or association row |
| Diagnostics are returned | Do not expose credentials, runtime links, raw payloads, transient IDs, or sensitive values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACT.ROUTE | decision | 7 | execution_gate | read->ACT.DONE;create_or_edit_or_delete_ready->ACT.LOADER_READY;mutation_blocked->ACT.ERROR | ACT.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| ACT.ERROR | step | 8 | error_handler | stopped->ACT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| ACT.DONE | terminal | 9 | terminal | none | ACT.ROUTE | continue | Read completed |
| ACT.LOADER_READY | terminal | 10 | terminal | none | ACT.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| ACT.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
