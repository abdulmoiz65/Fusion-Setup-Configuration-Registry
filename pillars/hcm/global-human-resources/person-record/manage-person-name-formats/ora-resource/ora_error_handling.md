# Manage Person Name Formats Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| PNF-01 | The internal Name Format REST resource or response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the internal resource contract |
| PNF-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| PNF-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| PNF-01C | A required read or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| PNF-02 | Read returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| PNF-03 | The Data Loader contract is missing or stale | Catalog mismatch | Stop before source generation and restore the current contract |
| PNF-03B | Live Data Loader Business Object Validation returns HTTP 500 without a usable diagnostic | Fusion API | Preserve the failed stage and retry the unchanged source only when the user explicitly requests a retry; otherwise stop |
| PNF-03A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| PNF-04 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| PNF-04A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected name formats |
| PNF-04B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| PNF-04C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| PNF-04D | A create is confirmed but its user-facing details have not been returned | Result presentation | Return the created Name Format details using the authoritative read or, for caller UI confirmation, the confirmed submitted values |
| PNF-04E | A delete is confirmed but the successful deletion has not been reported | Result presentation | State that the Name Format was deleted successfully and return its name, scope, and legislation or country |
| PNF-05 | Delete lacks one exact format or component target | Input validation | Stop and request one precise component selector |
| PNF-06 | Fusion rejects FormatMask | Fusion API | Preserve the rejection, rebuild the complete escaped mask, and obtain new preview and approval |
| PNF-06A | A required component token cannot be resolved from the current contract | Catalog mismatch | Stop and restore the token contract before rebuilding the mask |
| PNF-06B | Source validation finds an unescaped pipe in FormatMask | Input validation | Backslash-escape every pipe, rebuild the source, and continue through Core Data Loader |
| PNF-06C | A replacement component is malformed, nested, contains a separator, or has an unresolved preferred or fallback token | Input validation | Rebuild the complete mask with exactly two proven core tokens inside `<...>`, then obtain a new preview and approval |
| PNF-06D | A whitespace separator, comma, or other literal character has no valid current separator-token mapping | Input validation | Map whitespace to `$SPA$`, comma to `$COM$`, and resolve every other literal character before rebuilding the source and obtaining a new preview and approval |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A format or component target is missing or ambiguous, or FormatMask contains an unescaped pipe | Correct the selector or escaped source value and restart validation |
| Catalog mismatch | The internal read, Data Loader, or component-token contract is missing or stale | Restore the current contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects FormatMask | Rebuild the complete escaped mask from the current contract |
| Fusion API | Live Data Loader Business Object Validation returns HTTP 500 | Preserve the stage and server result; retry only on explicit user direction, then stop and report the repeated failure or continue to preview on success |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile format state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| FormatMask rejection | Rejected mask, unresolved component label, current token contract result, and need for a complete rebuilt preview |
| Replacement-component rejection | Preferred and fallback component labels, resolved-token evidence, malformed replacement expression, and need for a complete rebuilt preview |
| Literal-separator rejection | Supplied character, expected mapping, current token contract result, and need for a complete rebuilt preview |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Confirmed create | Format name, scope, legislation or country, and human-readable layout; omit raw mask and runtime identifiers |
| Confirmed delete | State that the Name Format was deleted successfully; include format name, scope, and legislation or country |
| Delete blocker | Exact format and component identity still required |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to another mutation route |
| Preview, approval, contract, token mapping, or source bytes changed | Do not reuse the earlier approval |
| FormatMask or a token is unresolved | Do not try quote prefixes, one-character retries, or guessed tokens |
| Delete target is ambiguous | Do not prepare or submit the delete |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNF.ROUTE | decision | 6 | execution_gate | read->PNF.DONE;create_or_edit_or_delete_ready->PNF.LOADER_READY;mutation_blocked->PNF.ERROR | PNF.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| PNF.ERROR | step | 7 | error_handler | stopped->PNF.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| PNF.DONE | terminal | 8 | terminal | none | PNF.ROUTE | continue | Read completed |
| PNF.LOADER_READY | terminal | 9 | terminal | none | PNF.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| PNF.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
