# Manage Action Reasons Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| AR-01 | The Action Reason REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| AR-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| AR-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| AR-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| AR-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| AR-03 | The Data Loader contract is missing or stale | Catalog mismatch | Stop before source generation and restore the current contract |
| AR-03A | Source validation is missing or stale | Input validation | Stop and revalidate the complete source |
| AR-03B | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| AR-04 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| AR-04A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected action reasons |
| AR-04B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| AR-04C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| AR-05 | An Action Reason, Action, Country, role, or configured reference has zero or multiple compatible matches | Input validation | Stop and request one exact business selector; never select by position |
| AR-06 | Source contains a generated ID, unsupported field, partial key, or invented association shape | Catalog mismatch | Stop and rebuild a registered-object-supported source shape |
| AR-07 | Requested Description is absent from current ActionReasons loader metadata | Catalog mismatch | Disclose the unsupported field and omit it only after explicit confirmation, then regenerate the preview; otherwise stop |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target or supplied reference is missing, ambiguous, or incompatible | Correct the selector and restart resolution |
| Catalog mismatch | Source shape or requested fields differ from the registered ActionReasons contract | Correct the source from current loader metadata |
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
| Unsupported Description | The requested field, current metadata result, omission impact, and need for explicit confirmation |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Action Reason or association rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not substitute a REST write, FSM import, CSV omission, or another route |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| A target or reference is unresolved | Do not choose a match by position or invent a value |
| Description is unsupported | Do not omit it without explicit confirmation |
| Diagnostics are returned | Do not expose credentials, runtime links, raw payloads, transient IDs, or sensitive values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.ROUTE | decision | 7 | execution_gate | read->AR.DONE;create_or_edit_or_delete_ready->AR.LOADER_READY;mutation_blocked->AR.ERROR | AR.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| AR.ERROR | step | 8 | error_handler | stopped->AR.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| AR.DONE | terminal | 9 | terminal | none | AR.ROUTE | continue | Read completed |
| AR.LOADER_READY | terminal | 10 | terminal | none | AR.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| AR.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
