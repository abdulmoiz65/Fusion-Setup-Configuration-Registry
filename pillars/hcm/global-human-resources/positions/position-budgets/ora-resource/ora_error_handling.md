# Position Budgets Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| PB-01 | A successful positionBudgets read returns zero or multiple exact targets | Input validation | Stop and request one documented identifier or search criterion |
| PB-01A | The positionBudgets response contract is missing or incompatible | Catalog mismatch | Stop and restore the declared read contract |
| PB-01B | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| PB-01C | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| PB-01D | A required Position Budget read privilege is denied | Authorization | Stop and report the missing access without changing routes |
| PB-01E | Fusion rejects the declared read or returns an unusable response | Fusion API | Preserve sanitized diagnostics and stop without substituting a mutating call |
| PB-02 | The Position Budgeting profile does not resolve to Y | Input validation | Stop create or edit without bypassing the profile gate |
| PB-03 | Enterprise AllocateBy is blank or unsupported | Catalog mismatch | Stop and resolve Enterprise Position Budget Configuration first |
| PB-04 | Budget allocation attributes do not match Allocate By | Input validation | Stop and correct the budget definition |
| PB-05 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| PB-06 | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| PB-07 | Data Loader fails or completes with errors | Process failed | Preserve diagnostics, reconcile the affected budget, and stop |
| PB-07A | Data Loader does not reach a terminal status in time | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| PB-07B | The submission outcome is uncertain | Process failed | Reconcile through the authorized read and never replay an uncertain mutation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Budget identity, profile readiness, or allocation attributes are unresolved or invalid | Correct the input or prerequisite and restart its owning node |
| Catalog mismatch | A read contract or Enterprise AllocateBy is unavailable or unsupported | Restore the contract or correct Enterprise Position Budget Configuration |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects a declared read or returns an unusable response | Preserve sanitized diagnostics and correct the request or contract |
| Artifact persistence | Core cannot produce or preserve the reviewed source | Follow the Core correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, or uncertain | Preserve diagnostics, reconcile, and stop before retry |
| Process timeout | Loader does not reach a terminal status | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Profile blocker | Profile result and the requirement that Position Budgeting resolve to Y |
| Allocate By blocker | Resolved or missing AllocateBy value and the incompatible budget attributes |
| Target blocker | Supplied business identifier or search criterion and match outcome without exposing internal IDs |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Position Budget data cannot be read | Do not substitute a mutating REST call |
| Position Budgeting does not resolve to Y | Do not bypass the create or edit profile gate |
| AllocateBy is blank or unsupported | Do not infer an allocation method |
| A resolver or authentication step fails | Do not replace its declared shared or core owner or route |
| A mutation fails, times out, or is uncertain | Do not retry automatically or replay the mutation |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.ROUTE | decision | 45 | execution_gate | read->PB.DONE;create_or_edit_or_delete_ready->PB.LOADER_READY;mutation_blocked->PB.ERROR | PB.ENFORCE_ALLOCATION | stop | Select read completion or the Core Data Loader handoff |
| PB.ERROR | step | 50 | error_handler | stopped->PB.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unsupported |
| PB.DONE | terminal | 60 | terminal | none | PB.ROUTE | continue | Read completed |
| PB.LOADER_READY | terminal | 65 | terminal | none | PB.ROUTE | continue | Mutation rules passed; return PB.LOADER_READY to the task skill |
| PB.BLOCKED | terminal | 70 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
