# Error Handling

Classify failures without exposing credentials or replaying an uncertain import. Preserve the fixed task code, SHA-256, and every returned ProcessId.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context, target-state verification, or package validation fails | Stop before preview or Fusion side effects and report the exact missing or invalid fact |
| Preview is missing, stale, or mismatched to approval | Classify approval_blocker and require a new immutable preview |
| Profile-definition read fails | Stop before preview; classify the read failure and do not infer a current value or permitted level |
| Fusion rejects an import for revision mismatch | Preserve the rejection, do not resubmit the same archive, and return the evidence to core.data-loader for its supported recovery decision |
| Import POST returns timeout, connection closure, or uncertain response | Stop and reconcile by read-only process lookup; never replay the POST |
| Fusion returns a ProcessId | Persist it immediately and use only that ProcessId for polling and ProcessLog retrieval |
| Polling reaches the deadline | Classify process_timeout, persist last status, and require status-only continuation |
| Import reaches terminal failure | Classify process_failed and retrieve ProcessLog when available |
| Import succeeds | Re-read the configured profile values affected by the approved change plan before reporting verified completion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required operation, task, environment, profile change plan, ZIP/hash, or status input is invalid | Correct input and rebuild preview or status request |
| catalog_or_metadata_mismatch | Catalog, ZIP metadata, or profile definition does not match the fixed task or requested level | Stop and resolve the authoritative identity |
| authorization_or_privilege | Authentication succeeds but a profile read or import is denied | Confirm the required Fusion privileges |
| transport_or_environment | Environment or network state prevents reliable read or import completion | Preserve state and reconcile; do not replay a POST |
| fusion_api_error | Fusion rejects a profile read or import | Preserve HTTP status, endpoint path, response summary, and ECID when available |
| revision_mismatch | Fusion rejects an archive because its revision is not accepted by the target | Let core.data-loader determine the supported recovery; any replacement archive requires a new immutable preview and approval |
| process_timeout | The same ProcessId remains nonterminal at the polling deadline | Resume that ProcessId through status only |
| process_failed | Import reaches terminal failure | Retrieve ProcessLog and correct the reported setup-data issue |
| approval_blocker | Preview approval is missing, stale, changed, or locally reconstructed | Revalidate and obtain fresh exact approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import approval | Target environment, fixed task, ZIP path and SHA-256, exact profile current-to-proposed changes, Task Hook validation result, and whole-task impact |
| Process accepted | Operation, task, environment, ProcessId, intended artifact path, and current status |
| Revision mismatch or uncertain response | TaskCode, prior ProcessId when available, last status, target, and the safe recovery or status-only next action |
| Terminal failure | Failure class, ProcessId when available, ProcessLog path, redacted Fusion summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Core Data Loader approval or Task Hook validation envelope is missing | Do not initiate import through any route |
| Target profile state is missing, non-updatable, or does not match the change plan | Do not build or approve an import preview |
| Package or preview changes after approval | Do not reuse prior approval |
| Revision mismatch, uncertain response, or accepted ProcessId exists | Do not submit another import automatically |
| Pillar-local import route is selected | Do not reconstruct an adapter, endpoint, payload, upload, initiation, status implementation, or retry policy |
| Task-local package-origin, release, or adapter policy is proposed | Do not add it or modify the generic loader; continue through core.data-loader's unchanged contract |
| Sensitive values are present | Do not print or persist tokens, secrets, Authorization headers, token-cache contents, or full base64 ZIP content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DWHP.ERROR | step | 5 | error_handler | handled->DWHP.ISSUES | none | continue | Any validation, lookup, dependency, design, approval, execution, polling, or persistence failure |
| DWHP.VALIDATED | terminal | 6 | terminal | none | DWHP.DESIGN_GATE | continue | The operation-specific contract is ready for immutable preview, approved execution, or status continuation |
| DWHP.ISSUES | terminal | 7 | terminal | none | none | continue | The request has unresolved validation, execution, or verification issues |
