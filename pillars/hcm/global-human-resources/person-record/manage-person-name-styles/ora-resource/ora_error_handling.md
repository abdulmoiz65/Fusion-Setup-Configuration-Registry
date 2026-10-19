# Manage Person Name Styles Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| PNS-01 | The managePersonNameStyles read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| PNS-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| PNS-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| PNS-01C | A required read or FSM import privilege is denied | Authorization | Stop and report the missing access without changing routes |
| PNS-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| PNS-03 | The FSM Data Loader contract is missing or stale | Catalog mismatch | Stop before archive preparation and restore the current contract |
| PNS-03A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| PNS-04 | FSM import reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| PNS-04A | FSM import completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected name styles |
| PNS-04B | FSM import does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| PNS-04C | The import outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| PNS-05 | User requests whole-style deletion or component removal, including removal worded as an update | Input validation | Stop before target reads or submission; explain deletion is unsupported in FSM mode and no records were changed. Do not request approval or offer a REST fallback |
| PNS-06 | Package SourceType is not FSM, or ProcessLog does not identify submitTaskCSVImport | Catalog mismatch | Stop and rebuild from the current task export; do not retry it as an HCM Data Loader business object |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target is ambiguous or delete is requested | Correct the selector or stop the unsupported delete |
| Catalog mismatch | Package or process evidence does not prove the FSM submitTaskCSVImport route | Rebuild from the current task export and marker |
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
| Wrong route | Observed SourceType, whether submitTaskCSVImport appears in ProcessLog, and the required FSM rebuild action |
| Process failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Unsupported deletion | Identify whether the request removes a style or component; state the FSM limitation and that no records were changed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A create or edit fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared FSM route is unavailable | Do not submit the package as an HCM Data Loader business object or switch routes |
| Preview, approval, exported package, or marker changed | Do not reuse the earlier approval |
| Deletion or component removal is requested | Do not build a delete source or payload, request approval, or invoke Fusion mutation through any route |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected runtime details |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNS.ROUTE | decision | 6 | execution_gate | read->PNS.DONE;create_or_edit_ready->PNS.LOADER_READY;mutation_blocked->PNS.ERROR | PNS.ENFORCE | stop | Select read completion or the Core FSM handoff for supported create and ordinary field edit only |
| PNS.ERROR | step | 7 | error_handler | stopped->PNS.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| PNS.DONE | terminal | 8 | terminal | none | PNS.ROUTE | continue | Read completed |
| PNS.LOADER_READY | terminal | 9 | terminal | none | PNS.ROUTE | continue | Create or edit rules passed; invoke Core Data Loader and follow the FSM source through immutable ZIP preview |
| PNS.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
