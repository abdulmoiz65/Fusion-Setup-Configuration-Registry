# Error Handling

Classify failures without exposing sensitive values or replaying an uncertain profile update or import. Preserve the fixed task code and every returned request or process identifier.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context, task membership, SITE eligibility, target-state verification, or package validation fails | Stop before preview or Fusion side effects and report the exact missing or invalid fact |
| Current target inventory disagrees with the documented option inventory | Classify catalog_or_metadata_mismatch, identify disputed codes, and do not write them |
| Preview is missing, stale, or mismatched to approval | Classify approval_blocker and require a new exact preview |
| Profile-definition or SITE-value read fails | Stop before preview; classify the read failure and do not infer the current value or allowed value |
| A guarded-option prerequisite is missing | Stop before preview and show the exact warning or evidence required |
| Direct profile-value write returns timeout, connection closure, or uncertain response | Stop and re-read the exact SITE value; never replay the POST or PATCH automatically |
| Import POST returns timeout, connection closure, or uncertain response | Stop and reconcile by read-only process lookup; never replay the POST |
| Fusion returns a ProcessId | Persist it immediately and use only that ProcessId for polling and ProcessLog retrieval |
| Polling reaches the deadline | Classify process_timeout, persist last status, and require status-only continuation |
| Import reaches terminal failure | Classify process_failed and retrieve ProcessLog when available |
| Direct update or import succeeds | Re-read every affected SITE value before reporting verified completion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, environment, profile code, SITE level, proposed value, ZIP/hash, or status input is invalid | Correct the input and rebuild preview or status request |
| catalog_or_metadata_mismatch | Task inventory, profile definition, or FSM metadata conflicts with the fixed task contract | Stop and resolve the authoritative identity |
| auth_expired_or_invalid | A cache-managed authentication token is rejected | Refresh once through the selected core route, then stop if rejection repeats |
| authorization_or_privilege | Authentication succeeds but the required profile-view, update, export, or import privilege is absent | Stop and correct the required role or privilege |
| transport_or_environment | Environment or network state prevents a reliable read or execution result | Preserve state and reconcile; do not replay a write |
| fusion_api_error | Fusion rejects a profile read, update, or import | Preserve HTTP status, endpoint path, response summary, and ECID when available |
| approval_blocker | Approval is missing, stale, changed, or not bound to the exact preview | Revalidate and obtain fresh exact approval |
| process_timeout | The same ProcessId remains nonterminal at the polling deadline | Resume that ProcessId through status only |
| process_failed | Import reaches terminal failure | Retrieve ProcessLog and correct the reported setup-data issue |
| artifact_persistence | Required blueprint, validation result, diagnostic, or run record cannot be saved | Preserve external identifiers and retry persistence without repeating Fusion execution |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before direct-update approval | Target environment, fixed task, exact profile code, SITE key, current and proposed values, definition eligibility, and every applicable guardrail |
| Before import approval | Target environment, fixed task, ZIP path and SHA-256, exact profile changes, Task Hook validation result, and whole-task impact |
| Write or process accepted | Operation, task, environment, sanitized request identifier or ProcessId, and current status |
| Uncertain response | TaskCode, option code or artifact hash, request or ProcessId when available, last known state, and read-only reconciliation action |
| Terminal failure | Failure class, request or ProcessId, ProcessLog path when available, redacted Fusion summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Requested code is outside the supported inventory or is disputed by target evidence | Do not read by approximation, write, or synthesize an FSM row |
| Profile level is not SITE or the SITE definition is disabled/non-updatable | Do not choose product/user level or proceed with mutation |
| Required guarded-option evidence is missing | Do not weaken, omit, or silently accept the guardrail |
| Exact direct-update or Core Data Loader approval is missing | Do not initiate a write or import through any route |
| Target profile state, package, or preview changes after approval | Do not reuse prior approval |
| A direct write, import response, or accepted ProcessId is uncertain | Do not submit another mutation automatically |
| Pillar-local execution route is proposed | Do not reconstruct an endpoint, adapter, payload, upload, initiation, polling, or retry implementation |
| Sensitive values are present | Do not print or persist credentials, tokens, Authorization headers, token-cache contents, full base64 ZIP content, or sensitive configuration values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.ERROR | step | 6 | error_handler | handled->CHP.ISSUES | none | continue | Any validation, lookup, dependency, design, approval, execution, polling, or persistence failure |
| CHP.VALIDATED | terminal | 7 | terminal | none | CHP.DESIGN_GATE | continue | The operation-specific contract is ready for exact preview, approved execution, or status continuation |
| CHP.ISSUES | terminal | 8 | terminal | none | none | continue | The request has unresolved validation, execution, or verification issues |
