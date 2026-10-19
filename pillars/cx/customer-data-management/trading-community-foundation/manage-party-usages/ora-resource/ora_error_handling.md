# Error Handling

Preserve the fixed task identity and every server-issued identifier. Never
replay an uncertain export or import submission.

## Classifications

| Classification | Use when | Next action |
|---|---|---|
| input_validation | Required context, scope, path, ZIP, hash, or route is invalid | Correct input and rebuild preview |
| catalog_or_metadata_mismatch | Live task identity/support, nonblank live hierarchy evidence, catalog context, or FSM metadata conflicts with the fixed task | Resolve the conflicting evidence or use the matching whole-task package |
| adapter_capability_gap | The task-local adapter or shared FSM engine is unavailable, Task Hook cannot release the approved payload, or required live `setupTaskCSVImports` metadata is absent | Restore the Data Loader-authorized adapter or required live capability; stop before POST |
| auth_expired_or_invalid | Cache-managed authentication is rejected before submission | Refresh once only when the workflow permits |
| authorization_or_privilege | Identity lacks setup export/import privileges | Correct privileges and rerun preflight |
| transport_or_environment | Host is unavailable or response is uncertain | Reconcile read-only; do not replay POST |
| fusion_api_error | Fusion rejects a read, export, upload, or initiation | Persist the redacted response summary and stop |
| process_timeout | The known export process remains nonterminal at deadline | Resume only that ProcessId on a later status request |
| process_failed | Export or import reaches terminal error | Retrieve supported diagnostics and correct the issue |
| artifact_persistence | Required result or audit evidence cannot be stored safely | Persist a safe diagnostic and do not resubmit |
| approval_blocker | Approval is absent, stale, mismatched, or arrived before a ready preview | Finish or rebuild preparation, present the complete immutable preview, and request its single approval |

## Retry and Disclosure Rules

- Never retry a live POST automatically.
- Create an import process only through
  `setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess`. Read the
  documented root-level `ProcessId`; accept the legacy nested
  `SetupTaskCSVImportProcess` list only for compatibility. Persist a redacted
  create-response artifact before treating a missing or invalid identifier as
  uncertain. Never persist echoed `FileContent`.
- Do not classify omitted or blank `OfferingName`, `OfferingCode`,
  `FunctionalAreaName`, or `FunctionalAreaCode` values from the live
  `setupTasks` representation as a catalog mismatch. Use the fixed task
  manifest and effective catalog as hierarchy authority. A contradictory
  nonblank value remains blocking.
- Treat a command-runner yield, live session identifier, or temporarily empty
  output buffer as an orchestration continuation signal, not as export
  completion or `process_timeout`. Resume the same command session until the
  exporter exits.
- Classify `process_timeout` only when the exporter itself exits after its
  declared 300-second polling window. Do not classify a tool or wrapper yield
  as timeout and do not give a final pending result while the exporter session
  is still live.
- Never upload or initiate outside `core.data-loader` validation and its Task
  Hook approval envelope. After Data Loader selects the task-local native FSM
  adapter and releases the approved payload, that adapter may create the one
  setup-task CSV import process and reuse the shared FSM engine for polling and
  log retrieval.
- The task-local adapter always enables source-target revision tolerance for
  cross-environment migration. Do not add a revision-policy option, preflight
  comparison, fail-first request, override preview, or extra approval gate.
- Never send this package through `uploadDataLoaderFile` or
  `dataLoaderDataSets/action/initiateDataLoad`. If that generic action returns
  HTTP 400 / `27503`, classify adapter selection as invalid and stop; do not
  remove `runID`, retain `sourceType`, or retry the generic action.
- Never ask again at a downstream boundary for an unchanged approved preview.
- Automatically select the sole active configured Fusion environment. Ask the
  user only when no environment is configured or multiple active environments
  remain ambiguous; include safe choices when known.
- Treat authentication, browser sign-in, token refresh, task lookup, and other
  read-only checks as uninterrupted preparation. Do not request `ready`,
  `continue`, or approval for those steps.
- An early `approve` does not authorize a POST. Complete preparation, persist a
  ready fingerprint-bound preview, show it, and request the operation's one
  approval. After approval of that preview, execute immediately without another
  conversational gate.
- Never reuse approval after environment, task, scope, archive bytes, hash,
  path, or options change.
- Report the environment, operation, task code, ProcessId or request ID, last
  status, elapsed time, diagnostic path, and safe next action when applicable.
- Never print or persist secrets, tokens, authorization headers, token-cache
  contents, full Base64 payloads, or sensitive customer data.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.ERROR | step | 4 | error_handler | handled->PU.ISSUES | none | continue | Any lookup, validation, approval, authentication, submission, polling, process, or persistence failure |
| PU.VALIDATED | terminal | 5 | terminal | none | PU.VALIDATE_OPERATION | continue | The operation contract is ready for its preview |
| PU.ISSUES | terminal | 6 | terminal | none | none | continue | Unresolved issues remain |
