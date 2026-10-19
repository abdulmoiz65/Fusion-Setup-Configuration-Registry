# Error Handling

Classify failures without exposing sensitive values or replaying an uncertain export, profile update, or FSM import.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required task, environment, option, SITE, package, value, or approval input fails | Stop before preview or mutation and report the exact invalid fact |
| Documented profile is live but absent from the completed task export | Classify export_content_discrepancy; never synthesize an FSM row; offer verified update_one |
| Profile definition, SITE level, or lookup code read fails | Stop before preview and do not infer the target or value |
| Exported and live application id, level, current value, or validation contract disagree | Classify catalog_mismatch and stop |
| FSM copy changes an identity, audit column, unrelated row, member name, metadata file, or encoding | Reject the package and return to the immutable baseline |
| Preview is missing, stale, or mismatched to approval | Classify approval_blocker and require a fresh exact preview |
| Direct profile write or import returns timeout, connection closure, or uncertain response | Stop and reconcile by read-only status or value read; never replay automatically |
| Fusion returns a ProcessId | Persist it immediately and continue only that process |
| Polling reaches its deadline | Classify process_timeout, preserve last status, and require status-only continuation |
| Import reaches terminal failure | Retrieve and persist ProcessLog when available |
| Import or direct update succeeds | Re-export or re-read all changed SITE values before verified completion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, environment, code, SITE scope, stored value, ZIP, hash, or row is invalid | Correct input and rebuild preview |
| export_content_discrepancy | Live supported definition is omitted from a successful exact-task export | Use view or update_one after live verification; do not synthesize a CSV row |
| catalog_mismatch | Task inventory, definition, lookup, application id, or metadata conflicts | Resolve the authoritative identity before continuing |
| auth_authz | Authentication fails or required export/import/profile privilege is absent | Refresh an expired cache once when routed; otherwise correct privileges |
| transport_environment | Environment or network state prevents a reliable result | Preserve state and reconcile; do not replay a mutation |
| fusion_api | Fusion rejects a read, export, profile update, or import | Preserve status, safe endpoint path, response summary, and ECID when available |
| approval_blocker | Approval is missing, stale, or not bound to the exact preview | Revalidate and obtain fresh executor-owned approval |
| process_timeout | The same ProcessId remains nonterminal at the deadline | Continue status for that ProcessId only |
| process_failed | Export or import reaches terminal failure | Retrieve ProcessLog and correct the reported issue |
| artifact_persistence | Required export, ZIP copy, hash, diagnostic, or run record cannot be saved | Retry persistence without repeating Fusion execution |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before FSM import approval | Environment, fixed task, original and modified ZIP paths and hashes, exact changed codes, current and proposed stored values, lookup meanings, and Task Hook result |
| Before update_one approval | Environment, fixed task, profile code, SITE key, current and proposed stored values, lookup meaning, eligibility, and design checks |
| Process accepted | Operation, task, environment, sanitized request identifier or ProcessId, and current status |
| Terminal failure | Failure class, affected codes, ProcessId or request ID, ProcessLog path when available, redacted summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Code is outside the closed inventory | Do not read by approximation, change it, or add it to the package |
| UI label is not the exact stored token | Do not write the label into ProfileOptionValue |
| SITE is disabled or non-updatable | Do not choose another level or proceed with mutation |
| Expected row is absent from the task export | Do not synthesize an FND_APP_PROFILE_VALUE row |
| Required cross-option rule fails | Do not weaken or omit the design gate |
| Exact Core Data Loader or Apps Common approval is missing | Do not submit import, POST, or PATCH |
| Target state, package, or preview changes after approval | Do not reuse prior approval |
| Mutation result is uncertain | Do not automatically retry or start another mutation |
| Sensitive values are present | Do not print or persist credentials, tokens, headers, token-cache contents, client secrets, or full base64 ZIP data |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.ERROR | step | 7 | error_handler | handled->CDMO.ISSUES | none | continue | Any validation, lookup, dependency, design, approval, execution, polling, or persistence failure |
| CDMO.VALIDATED | terminal | 8 | terminal | none | CDMO.DESIGN_GATE | continue | The operation-specific contract is ready for exact preview, approved execution, or status continuation |
| CDMO.ISSUES | terminal | 9 | terminal | none | none | continue | The request has unresolved validation, execution, or verification issues |
