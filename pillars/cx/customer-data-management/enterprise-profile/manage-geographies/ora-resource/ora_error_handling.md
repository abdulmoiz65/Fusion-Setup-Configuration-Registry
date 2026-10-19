# Error Handling

## Native CX Import failures

- Missing, changed, or context-mismatched preflight/Task Hook artifacts block
  before upload and require fresh validation and approval.
- A partial CRM upload blocks initiation. Retain all returned document IDs and
  envelopes for reconciliation; never retry or initiate a partial group.
- Uncertain initiation is an approval blocker; reconcile the returned data set,
  content IDs, and RequestId rather than uploading or initiating again.
- Only core.data-loader's HTTP 400/action 27503 compatibility retry may remove
  Run Book fields while preserving content IDs and CX fields; do not reupload.
- After accepted initiation, return Data Load In Progress and stop. A pending
  structure is not a timeout or failure; hierarchy remains pending until an
  explicitly requested status check confirms completion without errors.
- If structure completed and hierarchy failed, report partial success and retain
  structure; no rollback or automatic hierarchy retry.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Country is blank, multiple, ambiguous, or invalid for the selected source | Stop before Fusion calls, classify as input_validation, explain the issue, and ask for exactly one source-appropriate country name/code; show close Loqate matches when applicable |
| Environment is missing or ambiguous | Stop before side effects, explain the issue, and ask which target environment to use; show safe available choices when known |
| Authentication is required | Start the configured Fusion authentication flow automatically without asking permission; never ask the user to provide credentials or tokens in chat |
| Profile read fails after one cache-managed token refresh | Tell the user which profile lookup failed and provide a safe error summary and recommended action; classify as auth_expired_or_invalid, authorization_or_privilege, transport_or_environment, or fusion_api_error |
| ORA_HZ_ENABLE_DAAS_LOQATE is missing or does not resolve to Y | Show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y` in the single business preview; ask whether the user wants Loqate as the source for geography data and explain that choosing it requires enabling the profile option |
| ORA_HZ_DAAS_GEO_ENDPOINT is missing, null, empty, or whitespace-only | Ask the user to configure the site-level profile value in Fusion; stop before profile writes or import and re-read it on resumption |
| Either profile lookup returns multiple `SITE` records | Stop and classify as fusion_api_error; do not select or mutate an ambiguous record |
| User declines Loqate or chooses manual setup | Make no profile changes, do not submit ESS, explain the manual Manage Geographies path, and classify as approval_blocker |
| Profile create or update fails | Preserve already completed changes, stop without automatic mutation retry, classify the Fusion error, and report the partial change summary |
| Post-change verification fails | Stop before ESS, classify as fusion_api_error, and report the profile that did not retain its approved value |
| Fusion rejects ESS submission or monitoring because access is insufficient | Tell the user which operation failed, include the job ID if already assigned, recommend the required access check, classify as authorization_or_privilege, and do not retry the submission |
| Clear execution intent is absent | Stop and classify as approval_blocker; ask one business-level question only when the request is ambiguous; even clear initial intent authorizes preview only |
| ESS polling times out | State that setup is still running; retain requestId, last status, and elapsed wait internally and continue tracking the same request |
| Submission command returns an empty initial output chunk | Treat it as a running process when a session handle is present; retain and poll that handle, then read the durable checkpoint |
| Submission process output is lost after POST | Inspect `ess-submission-checkpoint.json`; if it contains a requestId, persist and track that request without another POST |
| Submission checkpoint is unavailable | Run one exact, read-only correlation recovery query; zero or multiple matches block execution and must never trigger an automatic resubmission |
| Polling GET receives a cache-managed 401 or 403 | Refresh authentication once and resume tracking the captured requestId; do not rerun submission |
| ESS reaches a terminal unsuccessful status | State that setup did not complete, show the job ID and safe ESS error or status summary, and give the recommended action; retain full status and process diagnostics internally |
| ESS terminal error says geography data already exists or was already imported | Treat this as an informational already-present outcome: say that no new import was performed, include the job ID, preserve the original terminal diagnostic, do not retry or recommend retrying that country, and ask whether to set up another country |
| Durable output cannot be written | Preserve safe redacted diagnostics in a temporary location and classify as artifact_persistence |
| User-data source or scope is missing/ambiguous | Infer standard-versus-custom source and scope from the requested hierarchy; ask only when two different business outcomes remain genuinely possible |
| User-data CSV or canonical model violates structure/hierarchy rules | Return all safe row/field validation errors, classify as input_validation, and perform no upload |
| Task-owned import mapping definition is missing, malformed, or inconsistent with the required object/headers | Stop before Data Loader or Fusion calls as catalog_or_metadata_mismatch; do not infer a replacement definition |
| Data Loader validation or approval does not authorize a core service | Persist the technical diagnostic, stop as approval_blocker, and give a business-level readiness message; never expose UCM or metadata mechanics by default |
| Mapping lookup returns multiple exact name/object matches or one match with column drift | Stop as catalog_or_metadata_mismatch; report that import prerequisites are inconsistent without exposing mapping names or IDs unless requested |
| Mapping POST returns no MappingNumber or has an uncertain outcome | Stop as approval_blocker, then reconcile only through the exact authorized REST-core GET; never repeat the POST automatically |
| Mapping-only preparation succeeds | Report that reusable import preparation is ready and stop; retain MappingNumber and created/reused details internally |
| Import activity rejects the locally resolved country code or normalized geography type | Preserve the activity diagnostic, classify as process_failed or catalog_or_metadata_mismatch as appropriate, and stop without retry or a target preflight API |
| Country Structure import reports that it is already present | Report already present, stop that stage, and do not delete, replace, append, retry, or continue automatically |
| Internal CX object metadata omits a usable destination or adapter validation fails | Stop before confirmation or upload; retain UCM, metadata, account, and adapter details internally and report only that import prerequisites are not ready unless technical detail is requested |
| Mutation adapter receipt or artifact verification fails | Stop before POST as approval_blocker, preserve the latest preview and diagnostics, and rebuild approval for the exact current artifact |
| Mutation POST returns 401 or 403 | Do not refresh and replay the POST; report auth/authz and uncertain outcome when applicable, then reconcile read-only before any newly approved attempt |
| File staging does not resolve an internal document name | Native CRM upload missing dDocName blocks initiation; retain already uploaded document IDs and approved envelopes for reconciliation |
| File staging outcome is uncertain | Stop as approval_blocker and reconcile internally; never upload again automatically |
| Import activity create output lacks a positive ImportActivityId | For full_import, missing or uncertain accepted data set/RequestId blocks continuation; reconcile the same native load and never initiate again automatically |
| User-data polling times out | Persist the stage, ImportActivityId, last status, elapsed wait, and next-check path; do not replay upload or create |
| Structure completes with errors | Preserve its counters and report IDs, classify as process_failed, and do not start hierarchy |
| Hierarchy fails after structure completed | Preserve the successful structure plus hierarchy diagnostics, classify as partial process_failed, include an errors array, and do not roll back |
| CREATE_ONLY is rejected by the import activity | Native helper has no ImportMode control; stop before approval if required additive behavior is unsupported or unverified, with no direct activity fallback |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Invalid country, polling option, environment input, or project path | Correct the exact invalid field and rerun |
| catalog_or_metadata_mismatch | Country list, task metadata, task-owned mapping definition, or existing mapping cannot be matched confidently | Stop and review the current Oracle source, effective catalog, or conflicting Fusion mapping |
| auth_expired_or_invalid | Cache-managed token remains rejected after one automatic refresh | Attempt the configured authentication flow without asking permission; if it still fails, report the safe error and recovery action |
| authorization_or_privilege | Profile read or ESS execution is forbidden | Obtain the required role or privilege |
| transport_or_environment | Fusion/Data Loader endpoint is unavailable, environment identity is wrong, or a command-output session is interrupted | Preserve the preview, checkpoint, MappingNumber, and requestId when known; recover read-only and do not submit again |
| fusion_api_error | Fusion profile or scheduler API returns an error | Always give a safe Fusion error summary, failed business stage, and recommended action; expose endpoint paths, full payload details, and ECID only when technical details are requested |
| process_timeout | ESS remains nonterminal after wait_seconds | Continue tracking the same request without exposing mechanics by default |
| process_failed | ESS reports a terminal unsuccessful status | Review process details internally and require a new direct setup instruction before any new submission; when the error unambiguously says data already exists or was already imported, offer another country and treat the user's country reply as the new instruction |
| artifact_persistence | Project output cannot be written safely | Correct the project path or permissions |
| approval_blocker | The request is advisory or ambiguous about live execution, the single business preview awaits confirmation, an uncertain mutation awaits reconciliation, or the user chooses manual setup | Present only the pending business decision and make no live mutation until it is resolved |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Profile validation | State whether prerequisites are ready; when the endpoint is missing or blank, name `ORA_HZ_DAAS_GEO_ENDPOINT` and ask the user to configure its site-level value; when Loqate enablement is missing or not Y, display `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y` |
| Profile change | State whether `ORA_HZ_ENABLE_DAAS_LOQATE` was enabled and verified; the skill never changes `ORA_HZ_DAAS_GEO_ENDPOINT` |
| Lookup or API failure | Always show the failed business stage, environment when relevant, safe error summary, and recommended action; do not require the user to request error visibility |
| User input needed for recovery | Ask one focused question for the missing country, environment, or recovery decision; never ask the user to paste credentials, access tokens, or secrets |
| Normal execution | Concisely explain the country, selected Fusion environment, business-level prerequisite status, progress, job ID, structure and hierarchy outcome, separate-feature exclusions, and the next-country option |
| Technical details requested | Relevant REST or ESS contract, request identifiers, diagnostics, and retry policy, with secrets and sensitive values redacted |
| Timeout | State that setup is still running and will continue to be tracked; always provide requestId as the job ID and provide other mechanics only when requested or needed for support |
| Process failure | State the failed business action, completed profile changes, job ID, and recommended next step; provide technical status, ECID, and diagnostics only when requested or needed for support |
| Already-present process outcome | State that geography data for the country is already present or previously imported, that no new import was performed, and the job ID; then use the normal next-country prompt |
| User-data preview | Return native Data Loader approval report with country, scope, environment, levels/counts, additive boundary, and its required UCM Account field; hide tokens and extra raw payloads |
| Import-mapping preview | State only that reusable import preparation will be reused or created internally in the selected environment |
| Import-mapping result | State that reusable import preparation is ready; retain stable names, MappingNumber, fingerprint, and created/reused outcome internally |
| User-data failure | Show the failed stage, ImportActivityId when assigned, completed prior stages, safe Fusion status, record counters, report content IDs, and recommended action |
| User-data partial failure | Explicitly state which structure/hierarchy result remains, include an errors array, and do not describe the overall run as successful |
| Durable diagnostic | status, stage, failure_class, message, recommended_action, environment, skill_id, artifact_refs, and external IDs |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Country is unsupported | Do not substitute another country or submit the job |
| ORA_HZ_ENABLE_DAAS_LOQATE is missing or mismatched | Do not create or update it unless eligible prerequisite setup was included in the single approved business preview; show the exact profile option and proposed Y, ask whether the user wants Loqate as the source for geography data, and explain that choosing it requires enabling the profile option; do not submit until post-change verification passes |
| ORA_HZ_DAAS_GEO_ENDPOINT is missing or blank | Ask the user to configure it in Fusion; do not write it or submit the import until a later read verifies a nonblank site-level value |
| ORA_HZ_DAAS_GEO_ENDPOINT has a nonblank value | Do not normalize, replace, clear, patch, or include it in a change plan; preserve the original value exactly |
| Execution intent is absent or ambiguous | Do not submit the ESS request |
| ESS submission outcome is unknown | Do not submit another request automatically |
| A submission process yielded a session handle | Do not discard the handle or interpret its first empty output chunk as a completed empty response |
| Polling authentication fails | Do not rerun the submit phase; retry only GET tracking for the captured requestId after one cache-managed refresh |
| Polling times out | Do not treat timeout as failure or success and do not resubmit |
| Existing geography data may be present | Do not delete, replace, or overwrite it |
| Diagnostics are written | Do not print or persist credentials, bearer tokens, token-cache contents, or full sensitive payloads |
| User data is invalid | Do not upload a partially validated file or ask the core skill to guess column mappings |
| Mapping definition or caller override differs from the reviewed contract | Do not infer, add, drop, reorder, rename, or accept the mapping change at runtime |
| Data Loader does not authorize the REST core service | Do not implement task-local calls to Fusion importMappings or claim that the preview work is blocked on job submission/status |
| Existing mapping is duplicate or drifted | Do not choose an arbitrary MappingNumber, PATCH, DELETE, overwrite, or create another similarly named mapping |
| Mapping create outcome is uncertain | Do not repeat the POST; reconcile only with an exact authorized REST-core read |
| Country Structure exists | Do not follow a delete-and-reimport remediation; deletion and replacement are outside this skill |
| User requests update or deletion | Do not form a payload, change ImportMode, or reinterpret the request as creation |
| Upload or create result is uncertain | Do not repeat the live operation or infer success from missing output |
| Structure stage did not complete cleanly | Do not start hierarchy in a combined run |
| Hierarchy fails after structure success | Do not roll back structure or retry hierarchy without reconciliation and a new approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.BLOCKED | terminal | 37 | terminal | none | none | continue | A source, country, internal preflight, dependency, design, creation-only, structure, post-change verification, or authorization gate blocks execution |
| GEO.REFUSED | terminal | 38 | terminal | none | none | continue | User declines the single business execution preview or chooses manual geography setup |
| GEO.FAILED | terminal | 39 | terminal | none | none | continue | Input, lookup, profile mutation, Data Loader, Import Management, Fusion API, ESS, partial-stage, or persistence processing fails |
