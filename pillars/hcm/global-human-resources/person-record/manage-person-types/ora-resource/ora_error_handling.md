# Manage Person Types Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| PT-01 | The personTypes REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| PT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| PT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| PT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| PT-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise paired business key |
| PT-03 | The Data Loader contract is missing or stale | Catalog mismatch | Stop before source generation and restore the current contract |
| PT-03A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| PT-03B | Approval is recorded but the verified archive has not been submitted | Process failed | Continue immediately with the declared Core Data Loader submission; do not report the mutation as complete |
| PT-04D | A queued operation is returned to the user after initiation, a nonterminal status, or confirmation while later operations remain | Process failed | Continue monitoring or prepare the next queued operation; return control only for approval, a terminal blocker, or completion of the full queue |
| PT-04E | A document-specified operation queue is stopped without an explicit user stop/cancel/replacement instruction while work remains | Process failed | Resume the active queue at its current verification or next-operation stage; do not issue an intermediate final response |
| PT-04F | A document-specified batch contains a row that requires a value created by an earlier row and no stable loader key is available | Input validation | Stop before DAT generation; do not invent an ID, reuse a stale ID, or split the batch |
| PT-04 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| PT-04A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected person types |
| PT-04B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| PT-04C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| PT-05 | Delete targets a fixed System Person Type | Input validation | Block the request because fixed System Person Types cannot be deleted |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A paired target is ambiguous or delete targets a fixed System Person Type | Correct the target or stop the unsupported delete |
| Catalog mismatch | The REST read or Data Loader contract is missing or stale | Restore the current contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile Person Type state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Fixed System Person Type delete | Exact functional target and the immutable-system-type restriction without exposing internal IDs |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified User Person Type rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| Approval was recorded and the archive still matches | Do not pause or report success before the declared upload/initiation and reconciliation complete |
| A later queued operation remains after confirmed success | Start that operation immediately; do not exit the Person Type workflow |
| A document-specified mutation batch is selected | Do not create more than one DAT, ZIP, approval, or upload for that batch |
| A batch row depends on an earlier generated value | Do not build or submit an invalid DAT, infer the value, or split the batch |
| Delete targets a fixed System Person Type | Do not prepare or submit the delete |
| A paired business key is unresolved | Do not infer or invent a target |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.ROUTE | decision | 6 | execution_gate | read->PT.DONE;create_or_edit_or_delete_ready->PT.LOADER_READY;mutation_blocked->PT.ERROR | PT.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| PT.ERROR | step | 7 | error_handler | stopped->PT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| PT.DONE | terminal | 8 | terminal | none | PT.ROUTE | continue | Read completed |
| PT.LOADER_READY | terminal | 9 | terminal | none | PT.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| PT.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
