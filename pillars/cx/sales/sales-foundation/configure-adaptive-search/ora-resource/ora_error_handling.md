# Adaptive Search Publish Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Empty object list | Classify as input_validation and stop before preview |
| Recognized CPQ alias is not returned by Entities | Do not classify it as invalid; resolve it directly to `oraclecpqo_transaction` and `oraclecpqo_transactionLine` because a newly provisioned custom CPQ environment may not expose those entities in its active metamodel. A null or empty Entities response still selects the new-environment OOTB Full Publish path. |
| Requested names absent from the isDocument=true Entities response localizedName set | Classify as object_name_correction, display invalid names and up to three nearest display-name suggestions for each, ask whether a suggestion is required, and compare again; do not POST a partial list or expose the full catalog |
| localizedName maps to multiple entityName values | Classify as object_name_disambiguation, show numbered `Display Name (entityName)` choices, and require an exact selection before continuing |
| Entities GET returns HTTP 400 `Could not find active meta model` | Classify as new_environment_full_publish and display the OOTB Full Publish confirmation; do not attempt object-name validation |
| Entities GET returns HTTP 400 other than `Could not find active meta model`, or any other non-200 status | Classify as fusion_api_error, show HTTP status and a redacted Fusion message, and stop |
| Entities response is null, has null items, or has an empty items array | Classify as new_environment_full_publish; display the OOTB confirmation, then prepare its internal-entity array without `publishType` on Yes or collect a replacement list on No |
| Authentication fails | Classify as auth_expired_or_invalid; refresh a managed cache once only when supported |
| User lacks publish privilege | Classify as authorization_or_privilege and stop |
| Another publish is active, including ZCA-210166 | Classify as approval_blocker or Fusion concurrency conflict and stop without retry |
| publishStatus GET returns HTTP 404 with exactly `{"Error":"Cannot parse null string"}` | Classify as no_prior_publish and continue through payload mapping and the combined confirmation; this is expected when the Entities GET established a new environment. |
| publishStatus GET returns another HTTP error or a malformed 404 body | Classify as fusion_api_error, show the status and redacted message, and stop; do not submit. |
| Publish POST reports that an active sandbox prevents metamodel synchronization | Classify as fusion_api_error, report it, require sandbox resolution, and do not retry automatically |
| Publish POST returns Invalid Preference Parameter | Verify the embedded contract requires `Preference: transient`, invalidate the prior approval if the header binding changed, regenerate the preview, and require explicit approval before one new POST |
| POST response is ambiguous or loses connection | Classify as transport_or_environment; check latest status read-only before any new submission and never retry POST automatically |
| Status becomes ERROR | Classify as process_failed; retain a redacted message, jobId, mmuuid, and recommended action |
| User-requested one-time status check returns CANCELLED | Record and report the terminal cancelled result |
| User-requested current status finds a failed or unsuccessful Data Loader request | Report the Data Loader status and safe error details; do not call Adaptive Search publishStatus, retry the load, or infer a Publish Job ID |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Request shape or entity selection is invalid | Correct input and preview again |
| authorization_or_privilege | Fusion rejects publish authorization | Correct roles or use an approved account |
| transport_or_environment | Network or environment identity prevents a reliable result | Diagnose safely; use read-only status before considering another POST |
| fusion_api_error | Fusion returns a non-process REST error | Record status, endpoint path, safe response summary, and ECID when present |
| process_failed | Job reaches ERROR | Review the redacted message or approved ESS diagnostics |
| approval_blocker | Live execution, retry, or conflict resolution needs approval | Stop and request the missing decision |
| new_environment_full_publish | Entities lookup establishes that the target is new | Preview the full-publish impact and require explicit approval |
| entity_list_revision | User declines the displayed active/requested comparison | Collect a revised nonempty list and repeat the review iteration |
| object_name_correction | One or more requested names are absent from all nonempty localizedName values in the isDocument=true Entities response | Show invalid names and up to three nearest display-name suggestions for each, collect corrections, and compare the complete list again |
| object_name_disambiguation | A display name maps to multiple internal entityName values | Show internal names in parentheses for those duplicate choices and require the user to select one |
| catalog_mismatch | A display label or its internal entityName is missing | Stop and report that the object catalog entry is incomplete |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Environment, publish type, requested objects, object count, internal-object behavior, action, and expected response |
| Object review | Current active objects, requested objects, validation result, and whether confirmation is required |
| Submission | Data Loader Content ID, Data Loader Request ID, an explicit statement that neither is the Adaptive Search Publish Job ID, and that automatic polling is not performed |
| User-requested current status after Data Loader success | Data Loader status followed by Adaptive Search Publish Job ID, mmuuid when useful, initial status, and publish source |
| Failure | Functional stage, failed or blocked result, safe Fusion message, and recommended action |

Apply `ora_user_presentation.md` to normal administrator output. Keep endpoint paths, failure classes, fingerprints, contract identifiers, and artifact references internal unless the user explicitly requests technical diagnostics; always show a safe functional stage, result, message, and recommended action.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Credential or Authorization header is present | Do not print, persist, or commit it |
| Empty object list | Do not submit the publish |
| Some requested names are invalid | Do not discard them silently, publish only the valid subset, or continue without correction |
| Entities GET returns an unexpected status | Do not continue to publishStatus, preview, or POST |
| Existing job is nonterminal | Do not submit a concurrent publish |
| Live approval is missing or stale | Do not submit the POST |
| POST outcome is ambiguous | Do not automatically retry |
| Contract, payload, or mapping report is missing or stale | Do not preview or execute |
| A mapping input changes or prior binding metadata is unverifiable | Do not retain the old body as current; archive it when supported, remove executable-current names, persist an invalidation record, and revoke prior preview/approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.ERROR.HANDLE | decision | 180 | error_handler | failed->AS.END.FAILED | none | stop | Entity discovery, REST submission, or publish job fails |
| AS.END.FAILED | terminal | 190 | terminal | none | AS.ERROR.HANDLE | stop | Failure is terminal and diagnostics are captured |
