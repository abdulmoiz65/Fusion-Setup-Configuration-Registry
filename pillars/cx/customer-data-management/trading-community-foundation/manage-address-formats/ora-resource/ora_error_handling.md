# Error Handling

Classify failures without exposing credentials or replaying an uncertain export
or import. Preserve the exact task code and `ProcessId` whenever available.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required context or operation contract fails | Stop before the approval summary and report the invalid field |
| Live lookup is ambiguous, unsupported, or contradictory | Classify catalog_or_metadata_mismatch and stop before approval or POST |
| Export preview requests archiveSha256 or Data Loader archive verification | Classify input_validation; rebuild the export request preview using bound request fields |
| Preview is missing, stale, or mismatched | Classify approval_blocker and prepare one new immutable summary |
| Authentication needs interactive sign-in | Keep one callback listener active, inform the user that sign-in is needed without requesting any reply, and continue automatically after the callback |
| Authentication fails during preparation | Refresh a cache-managed token once; otherwise stop without asking for approval or a `ready` response |
| Live generic Data Loader action metadata omits `sourceType` or another proposed payload property | Classify catalog_or_metadata_mismatch, select the native setup-task CSV import adapter before preview, and make no UCM upload or generic initiation request |
| Generic `initiateDataLoad` returns HTTP 400 action error 27503 | Classify fusion_api_error and adapter-contract defect; preserve whether UCM upload succeeded and its content ID when available, then stop without retrying or reuploading |
| Export POST returns an uncertain response | Stop and reconcile through read-only process lookup; never replay the POST |
| Setup-task CSV import POST returns an uncertain response | Stop and reconcile through the shared adapter's process lookup; never replay the POST |
| Fusion rejects the initial import with the explicit HTTP 400 source-target revision-mismatch message and no ProcessId | Continue once under the preview-approved fallback with the same immutable operation and `SourceTargetDiffOkFlag=Y`; do not ask for another approval |
| The HTTP 400 body does not explicitly contain source, target, revision, and mismatch/difference language | Treat it as a different Fusion API error; do not invoke the fallback |
| Authentication expires during the approved fallback sequence | Refresh a cache-managed token once and resume the same N or Y stage; never restart from N after reaching Y |
| Fusion returns a ProcessId | Persist it immediately and use only that ProcessId for polling and result retrieval |
| Polling reaches the deadline | Classify process_timeout, persist last status, and wait for a later status request |
| Process completes with errors | Classify process_failed and persist ProcessLog when available |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required context, export contract, ZIP, metadata, hash, environment, or adapter is invalid | Correct input and rebuild the preview |
| catalog_or_metadata_mismatch | Live task identity/support or nonblank hierarchy data conflicts with the fixed context | Resolve the metadata conflict before approval |
| auth_expired_or_invalid | Cached authentication cannot be refreshed during preparation | Complete authentication and resume unchanged preparation |
| authorization_or_privilege | Authentication succeeds but task lookup/export/import access is denied | Confirm required Fusion privileges |
| transport_or_environment | Configured host is unreachable or environment identity cannot be confirmed | Correct environment connectivity |
| fusion_api_error | Fusion rejects a read, export, or import request, including action error 27503 | Preserve HTTP status, endpoint path, response summary, ECID, and accepted-upload state when available |
| process_timeout | The same ProcessId remains nonterminal at the polling deadline | Resume that ProcessId only after a status request |
| process_failed | The process reaches a terminal error state | Retrieve ProcessLog and correct the reported issue before a new preview |
| approval_blocker | Approval is missing/mismatched or a new POST is requested | Present one fresh exact summary and obtain approval |
| artifact_persistence | Preview, ProcessId, ZIP, log, or run state cannot be written safely | Preserve redacted diagnostics safely and do not submit/resubmit |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before export approval | Source, task name/code, unfiltered non-template scope, output path, adapter, options, and one-process impact |
| Before import approval | Target, task name/code, ZIP path, SHA-256, Data Loader route, selected task-local native FSM adapter, and whole-task impact |
| Export accepted | Task, source, ProcessId, output path, and current status |
| Import accepted | Task, target, immutable ZIP path/hash, request identifier, and current status |
| Timeout | TaskCode, ProcessId/request ID, last status, elapsed wait, and status-only continuation path |
| Terminal failure | Failure class, identifier, ProcessLog path, Fusion message summary, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Export is routed through Data Loader Task Hook | Do not fabricate an archive hash or use import-only archive validation; route through the shared exporter after one export approval |
| Generic Data Loader action omits a proposed property | Do not upload the archive, call `initiateDataLoad`, or rely on post-upload fallback; select the native setup-task CSV import adapter before preview |
| Approval is missing or mismatched | Do not invoke the operation-specific execution adapter |
| POST response is uncertain | Do not submit another POST or assume no process was created |
| Revision mismatch fallback is not preview-bound, the response is uncertain, or a ProcessId exists | Do not change `SourceTargetDiffOkFlag` from `N` to `Y` or submit another POST |
| Preview-bound value changes | Do not reuse prior approval |
| Individual address-style work is requested | Do not inspect, create, edit, delete, reorder, or filter styles |
| Sensitive values are present | Do not print or persist tokens, secrets, headers, token-cache content, or Base64 ZIP content |
| Authentication is pending | Do not ask for `approve`, `ready`, `continue`, confirmation, or permission to log in; wait on the same authentication process |
| Import polling times out | Say the import is still running, preserve the same ProcessId, and do not suggest a new submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.ERROR | step | 4 | error_handler | handled->AF.ISSUES | none | continue | Any validation, lookup, approval, authentication, submission, polling, process, or persistence failure |
| AF.VALIDATED | terminal | 5 | terminal | none | AF.VALIDATE_OPERATION | continue | The operation-specific contract is ready for one execution summary |
| AF.ISSUES | terminal | 6 | terminal | none | none | continue | The request has unresolved issues |
