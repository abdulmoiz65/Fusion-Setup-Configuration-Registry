# Manage Assignment Status Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| AS-01 | The assignmentStatuses read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| AS-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| AS-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| AS-01C | A required REST or FSM import privilege is denied | Authorization | Stop and report the missing access without changing routes |
| AS-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| AS-03 | A fresh same-task FSM export cannot be obtained or validated | Catalog mismatch | Stop after the fresh export attempt and report the failed stage; do not request a cached archive |
| AS-03A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| AS-04 | FSM import reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| AS-04A | FSM import completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected assignment statuses |
| AS-04B | FSM import does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| AS-04C | The import outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| AS-05 | Import and Load Data shows a SourceType other than FSM, or the process log does not identify submitTaskCSVImport | Catalog mismatch | Stop and rebuild from the exported FSM ZIP; do not retry it as an HCM Data Loader business object |
| AS-06 | Delete is requested | Input validation | Return unsupported without preparing source data or invoking Fusion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target is ambiguous or delete is requested | Correct the selector or stop the unsupported delete |
| Catalog mismatch | The archive or process evidence does not prove the FSM submitTaskCSVImport route | Rebuild from the exported FSM ZIP and marker |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | FSM import is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | FSM import does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Wrong route | Observed SourceType, whether submitTaskCSVImport appears in the process log, and the required FSM rebuild action |
| Process failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Unsupported delete | That delete is unsupported and no source or Fusion operation was prepared |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A create or edit fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared FSM route is unavailable | Do not submit the archive as an HCM Data Loader business object or switch routes |
| Preview, approval, exported ZIP, or marker changed | Do not reuse the earlier approval |
| Delete is requested | Do not prepare source data or invoke Fusion |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected runtime details |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.ROUTE | decision | 6 | execution_gate | read->AS.DONE;create_or_edit_ready->AS.LOADER_READY;create_or_edit_blocked->AS.ERROR;delete->AS.ERROR | AS.ENFORCE | stop | Select read completion or the Core FSM handoff |
| AS.ERROR | step | 7 | error_handler | stopped->AS.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| AS.DONE | terminal | 8 | terminal | none | AS.ROUTE | continue | Read completed |
| AS.LOADER_READY | terminal | 9 | terminal | none | AS.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow the FSM source through immutable ZIP preview |
| AS.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
