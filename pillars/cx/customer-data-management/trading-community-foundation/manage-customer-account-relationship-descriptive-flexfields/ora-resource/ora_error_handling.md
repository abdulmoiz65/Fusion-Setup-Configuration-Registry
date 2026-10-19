# Error Handling

Classify failures without exposing credentials or replaying an uncertain export
or import. Preserve the fixed task code and every returned ProcessId.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context, operation contract, or import ZIP validation fails | Stop before preview or Fusion side effects and report the exact invalid or missing fact |
| Preview is missing, stale, or mismatched to approval | Classify approval_blocker and require a new immutable preview |
| Authentication fails during read-only preflight | Refresh a cache-managed token once and repeat only the GET; otherwise stop |
| Export or import POST returns 401, 403, timeout, connection closure, or uncertain response | Stop and reconcile by read-only process lookup; never replay the POST |
| Fusion returns a ProcessId | Persist it immediately and use only that ProcessId for polling and artifact retrieval |
| Polling reaches the deadline | Classify process_timeout, persist last status, and require status-only continuation |
| Export or import completes with errors | Classify process_failed and retrieve ProcessLog when available |
| Import succeeds but target deployment or functional evidence is incomplete | Return import_succeeded_deployment_pending and report the exact manual verification or deployment action |
| Import succeeds and target status and functional evidence pass | Return import_succeeded_deployment_verified |
| Deployment status is Error | Keep import success separate, classify deployment_verification, and require manual diagnosis; do not resubmit the import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required operation, task, environment, import ZIP/hash, or status input is invalid | Correct input and rebuild preview or status request |
| catalog_or_metadata_mismatch | Catalog, live task, or ZIP metadata does not match the fixed task | Stop and resolve the authoritative identity |
| auth_expired_or_invalid | Cached authentication is rejected during preflight | Refresh once before any authorized POST |
| authorization_or_privilege | Authentication succeeds but the operation is denied | Confirm the required Fusion privileges |
| transport_or_environment | Environment, network, or callback state prevents reliable execution | Preserve state and reconcile; do not replay a POST |
| fusion_api_error | Fusion rejects a request | Preserve HTTP status, endpoint path, response summary, and ECID when available |
| process_timeout | The same ProcessId remains nonterminal at the polling deadline | Resume that ProcessId through status only |
| process_failed | Export or import reaches terminal failure | Retrieve ProcessLog and correct the reported setup-data issue |
| artifact_persistence | ProcessId, ZIP, hash, log, diagnostic, or run state cannot be safely written | Preserve redacted evidence and do not resubmit |
| approval_blocker | Preview approval is missing, stale, changed, or locally reconstructed | Revalidate and obtain fresh exact approval |
| deployment_verification | Import succeeded but target deployment or functional verification is pending or failed | Complete the manual DFF deployment/test lifecycle; do not retry import |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before export approval | Source environment, fixed task, whole-task non-template scope, output path, adapter, options, and one-process impact; do not request deployment evidence or a pre-existing ZIP/hash |
| Before import approval | Target environment, fixed task, ZIP path and SHA-256, unchanged-package statement, Core Data Loader Task Hook validation envelope, and whole-task impact |
| Process accepted | Operation, task, environment, ProcessId, intended artifact path, and current status |
| Timeout or uncertain response | TaskCode, ProcessId or reconciliation window, last status, elapsed wait, and status-only next action |
| Import terminal success | Import process result plus separate target deployment-verification status |
| Terminal failure | Failure class, ProcessId when available, ProcessLog path, redacted Fusion summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Export approval is missing or the shared export adapter is not selected | Do not invoke the shared exporter or any export POST |
| Core Data Loader approval or Task Hook validation envelope is missing | Do not initiate import through any route |
| Pillar-local import route is selected | Do not invoke or reconstruct an adapter, endpoint, routing field, payload, upload, initiation, status implementation, or retry policy; Core Data Loader owns them |
| Export or import response is uncertain | Do not submit another POST or assume no process was created |
| Package or preview changes after approval | Do not reuse prior approval |
| Template, filter, partial package, loose CSV, task override, or direct DFF CRUD is requested | Refuse without a Fusion call |
| Import succeeded but deployment verification is incomplete | Do not claim complete migration and do not resubmit import |
| Sensitive values are present | Do not print or persist tokens, secrets, Authorization headers, token-cache contents, full base64 ZIP content, or sensitive environment values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CARDFF.ERROR | step | 5 | error_handler | handled->CARDFF.ISSUES | none | continue | Any validation, dependency, design, approval, execution, polling, persistence, or deployment-verification failure |
| CARDFF.VALIDATED | terminal | 6 | terminal | none | CARDFF.DESIGN_GATE | continue | The operation-specific contract is ready for immutable preview, approved execution, or status continuation |
| CARDFF.ISSUES | terminal | 7 | terminal | none | none | continue | The request has unresolved validation, execution, or deployment-verification issues |
