# Error Handling

Classify failures without exposing credentials or replaying an uncertain export
or import submission. Preserve the fixed task identity and any server-issued
ProcessId or request ID.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context, export contract, or ZIP validation fails | Stop before preview or Fusion side effects and report the exact invalid field, contract value, or package check |
| Preview is missing, stale, or does not match approval | Classify approval_blocker and require a new immutable preview |
| Authentication fails before submission | Refresh a cache-managed token once when the selected workflow permits it; otherwise stop |
| Export POST returns 401, 403, timeout, connection closure, or an uncertain response | Stop and reconcile with read-only export-process lookup; do not replay the POST |
| Data Loader upload or initiation returns timeout, connection closure, or an uncertain response | Stop and reconcile through the Data Loader status route when requested; do not replay either POST |
| Fusion returns a ProcessId or request ID | Persist it immediately and use only that identifier for later status or ProcessLog retrieval |
| Polling reaches the configured export deadline | Classify process_timeout, persist the last status, and require a later status-only request |
| An export or import process completes with errors | Classify process_failed and retrieve the applicable ProcessLog or Data Loader diagnostics when requested |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, task context, export contract, ZIP, metadata member, hash, environment, or route input is missing or invalid | Correct the input and rebuild the preview |
| catalog_or_metadata_mismatch | The fixed task identity or FSM metadata does not match the selected setup task | Correct the task context or use the matching whole-task export ZIP |
| auth_expired_or_invalid | A cache-managed token is rejected before submission | Refresh once only when the selected workflow permits it |
| authorization_or_privilege | Authentication succeeds but setup-task export or import access is denied | Confirm the account has the required setup-task and Data Loader privileges |
| transport_or_environment | The configured host is unavailable or the response is uncertain | Preserve the identifier when known and reconcile read-only before any retry |
| fusion_api_error | Fusion rejects a read, export, upload, or initiation request | Preserve the stage, HTTP result, response summary, and ECID when available; stop |
| process_timeout | The same ProcessId remains nonterminal at the export polling deadline | Resume that ProcessId only after a later status request |
| process_failed | The export or import reaches a terminal error state | Retrieve the supported diagnostic and correct the reported setup-data issue before seeking fresh approval |
| approval_blocker | Preview approval is absent or mismatched, or a retry or new submission is requested | Obtain a fresh exact preview and approval |
| artifact_persistence | ProcessId, result, log, or project record cannot be written safely | Preserve a redacted diagnostic at a safe project path and do not resubmit |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before export approval | Source environment, fixed task name and code, unfiltered non-template scope, output and result paths, polling options, and one-process impact |
| Before import approval | Target environment, fixed task name and code, ZIP path, SHA-256, executionRoute=data-loader, sourceType=FSM, and whole-task impact |
| Export accepted | Task name and code, source, ProcessId, output path, and current status |
| Import accepted | The complete core.data-loader success report with its permitted request identifiers |
| Timeout | Task code, ProcessId or request ID, last status, elapsed wait when applicable, and status-only continuation path |
| Terminal failure | Failure class, permitted identifier, diagnostic path when available, Fusion message summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Required approval is missing | Do not invoke a Fusion POST |
| Import does not route through core.data-loader and its Task Hook | Do not upload or initiate the FSM ZIP through a direct endpoint, shared import script, or task-local adapter |
| Export response is uncertain or its process is still running | Do not submit another POST or report an empty output buffer as failure |
| Import response is uncertain | Do not upload the archive again or initiate another load automatically |
| Package or preview changes after approval | Do not reuse the prior approval |
| Individual source-system change is requested | Do not inspect, create, edit, delete, reorder, or filter individual source systems |
| Sensitive values are present | Do not print or persist tokens, secrets, Authorization headers, token-cache contents, or full base64 ZIP content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCSS.ERROR | step | 3 | error_handler | handled->TCSS.ISSUES | none | continue | Any validation, approval, authentication, submission, polling, process, or persistence stage fails |
| TCSS.VALIDATED | terminal | 4 | terminal | none | TCSS.VALIDATE_OPERATION | continue | The whole-task operation contract is ready for its operation-specific preview |
| TCSS.ISSUES | terminal | 5 | terminal | none | none | continue | The request has unresolved validation, approval, execution, or persistence issues |
