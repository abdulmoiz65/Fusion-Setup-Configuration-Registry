# Position Costing Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| An End Date request is missing a Position identity clue, an LDG clue, an allocation effective date that identifies the target interval, or the separate requested EffectiveEndDate. | Stop locally as input_validation before authentication, token refresh, lookup, REST or Data Loader calls, template or metadata checks, or history, future-record, account, or interval validation. Acknowledge the Position, LDG, and dates already supplied, then ask one natural conversational question for only the missing value or values. Do not use a numbered list, checklist, or field form, and do not infer the requested EffectiveEndDate from the allocation effective date. |
| Position discovery is terminal-empty or has multiple candidates for exact detail. | Report actual filter/date scope. Empty lists are valid; exact detail needs selection. Never infer global absence or change the date. |
| A found Position has blank allocation/LDG fields consistent with no costing. | Continue with confirmed LDG and date-specific preflight; this is not a malformed Position or auth error. |
| Stage 1 positionsLov returns multiple distinct Position rows, multiple BusinessUnitIds or conflicting projected repeats after complete paging. | Stop HDL at resolve_position_business_unit as input_validation and report an ambiguous or malformed Position-bound Business Unit result. Do not select by row order, ask for a second Position choice, continue stage 2 or render HDL. Query remains available. |
| The Position is found but stage 1 positionsLov yields zero exact rows, a Position identity/date mismatch or a missing/nonpositive BusinessUnitId. | Stop HDL at resolve_position_business_unit as input_validation and report Position found but Business Unit unresolved. Do not report Main Search Position absence, use unobserved fields or another route, change dates or substitute caller values. Query remains available. |
| Search/expanded collections are truncated or a paged LOV is incomplete. | Never claim uniqueness, completeness or value absence. Continue declared paging; otherwise narrow criteria or stop with sanitized incomplete-response evidence. |
| Finder separators are double-encoded or runtime KFF x became a fragment. | Stop as input_validation before dispatch when detectable. Rebuild logical parameters and let the client encode once; never replay captured authenticated traffic. |
| A runtime LOV has null optional Description. | Preserve the valid code and display it without an invented meaning; this does not invalidate the segment. |
| Stage 2 finBusinessUnitsLOV returns zero, ambiguous/conflicting, ID-mismatched or blank-name rows, incomplete pagination or a different environment. | Stop HDL at resolve_business_unit and report this actual failing stage. Classify missing, ambiguous or mismatched business identity as input_validation, malformed/incomplete response as fusion_api_error and environment disagreement as transport_or_environment. Never invent BusinessUnitName, query by caller name, bypass stage-1 evidence or return a partial HDL context. |
| A BU stage cannot establish a required historical name or the environment does not support its documented route, finder or effective-date contract. | Record the actual resolver, sanitized GET resource, status and stage as catalog_or_metadata_mismatch; an HTTP/API error remains fusion_api_error. Stop HDL; do not serialize object-typed SysEffectiveDate without a contract, infer past names from current names/ActiveFlag, change the selected date or substitute another route. |
| Either BU stage receives an authorization, transport, endpoint or metadata failure. | Report resolve_position_business_unit for stage 1 or resolve_business_unit for stage 2. Apply the existing auth_expired_or_invalid, authorization_or_privilege, transport_or_environment, fusion_api_error or catalog_or_metadata_mismatch classification to the actual failure. Never treat a failure as an empty collection, replay a mutation, refresh repeatedly, use copied sessions or perform a browser mutation. |
| Required identity, BusinessUnitName, or KFF is missing, or a Create/effective-dated Update generated SubTypeSequence is invalid. | Stop and report the missing value or invalid sequence; generate 1 through N from supplied account-row order rather than request it from the user. A complete ambiguous Position candidate set follows its selection terminal instead of this error path. For Correct MERGE, ask the user for the exact positive HDL SubTypeSequence when REST omits it; physical DELETE operations do not require or invent one. |
| A Correct MERGE SubTypeSequence is missing, nonpositive, inferred, or conflicts with REST state. | Stop before rendering. Ask the user for the exact positive HDL value when REST omitted it; never derive it from response order, identifiers, percentages, or a fixed value. |
| LDG LIKE discovery returns multiple terminal candidates. | List the returned LegislativeDataGroupName values and request user selection; do not treat candidate multiplicity as an error or render a package before exact confirmation. |
| Create/Add confirms exactly one LDG, but that item's CostAllocationIdFlexNumber is null, empty, or whitespace-only. | Stop at LDG confirmation before Main Search or any KFF, DAT, archive, preview, or loader work. Show exactly "The {LDG_NAME} legislative data group has no associated cost structure", replacing {LDG_NAME} with the confirmed returned Name. Explain that costing cannot be created for this LDG. Do not ask the user for the internal flex number, infer one, switch LDGs, or continue on the generic missing-KFF path. Classify as catalog_or_metadata_mismatch. |
| A requested Delete (ED Split) has no documented standard HDL contract. | Stop as input validation; do not construct REST or generic-business-object mutation material. |
| Current template or package row shape is invalid. | Stop as catalog or metadata mismatch and correct members, keys, dates, or row arity. |
| A governed read-only REST request, loader upload, initiation, status, or verification response is invalid or returns a Fusion API error. | Classify as fusion_api_error, stop before another state change, preserve redacted diagnostics, and do not replay the archive or retry a mutation. |
| A loader initiation is accepted. | Return pending, explain that the load can take several minutes, and invite the user to request a status check. Do not poll automatically. |
| A user-requested loader status fails, times out, or verifies differently than expected. | Preserve redacted status and error detail, perform only the matching read-only verification when terminal evidence permits it, and stop. |
| Fresh approval or required preview, audit, or diagnostic artifact persistence is missing. | Classify as artifact_persistence when persistence failed; keep the immutable preview only and do not upload or initiate. |
| A multi-account Correct stage fails or has an unsafe total. | Stop before any later stage and require a fresh plan from observed read-only state. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Identity, effective date, KFF, operation, current state, or Correct SubTypeSequence is missing or invalid, or a generated sequence is invalid. | Supply or resolve the exact required value. A complete ambiguous Position candidate set requests selection and restarts source validation; regenerate 1 through N only for Create or Update, and ask the user for Correct SubTypeSequence when REST omits it. |
| catalog_or_metadata_mismatch | HDL template, package shape, runtime KFF contract or required resolver metadata is unsupported. | Correct the source/metadata mismatch before dependent validation or preview. |
| auth_expired_or_invalid | A read-only credential receives 401 or 403. | Refresh once only for a read, then stop if it fails. |
| authorization_or_privilege | A declared read or Data Loader operation lacks required access. | Obtain access; never treat permission denial as an empty result or refresh repeatedly. |
| transport_or_environment | A governed read or loader transport cannot reach the selected environment. | Record sanitized environment evidence and stop. |
| fusion_api_error | A governed read-only REST request, loader upload, initiation, status, or verification receives an invalid or HTTP error response. | Preserve redacted response and stop; do not replay a mutation. |
| process_timeout | A user-requested loader status check does not reach a terminal result. | Report the user-supplied request reference, last status, elapsed wait, and next-check path; do not poll again automatically. |
| process_failed | A loader result or post-load verification fails. | Preserve redacted diagnostics and stop. |
| artifact_persistence | Required preview, audit, or redacted diagnostic artifact cannot be persisted. | Stop before loader handoff and report the safe persistence failure. |
| approval_blocker | Fresh approval is absent or no longer matches the archive. | Obtain approval for the exact immutable preview. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read-only REST failure | Resolver/stage, sanitized environment, method, normalized resource path, status and safe error summary, completeness state and next action. Never show HAR headers/cookies, bearer values, token caches or raw sensitive bodies. |
| Pre-handoff approval | Sanitized environment, operation, expected effect, immutable ZIP SHA-256, and loader handoff scope. |
| Loader timeout | Sanitized environment, operation, Request ID, last status, elapsed wait, and next-check path. |
| Pending initiation | Sanitized environment, operation, accepted initiation result, and a message that status can be checked later on explicit user request. |
| Verification mismatch | Requested effect, observed read-only result category, redacted diagnostic, and safe resume stage. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any mutation | Do not invoke a mutating REST POST, PATCH, PUT, DELETE, raw UCM, FSM, CX, browser automation, or an ungoverned loader adapter. |
| Failed or ambiguous import | Do not retry, compensate, or replay automatically. |
| Multi-account Correct | Do not combine sibling account actions into one archive or rely on row order. |
| Delete (ED Split) | Do not substitute direct REST or a generic REST-backed business object. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCP.WAIT_LDG_SELECTION | terminal | 13 | terminal | none | PCP.SEARCH_LDG | continue | Show returned LDG Names and request one choice. Resume through validation with that candidate, not downstream without selection. |
| PCP.WAIT_POSITION_SELECTION | terminal | 19 | terminal | none | PCP.SEARCH_POSITION | continue | Show Position names, types, statuses and LDG names when returned; retain codes and IDs internally. Request one choice and resume through validation with the selected returned identity. |
| PCP.HDL_GATE_CREATE | decision | 80 | execution_gate | initiated->PCP.RESULT_CREATE;blocked->PCP.HANDLE_ERROR;failed->PCP.HANDLE_ERROR | PCP.ENFORCE_DESIGN | stop | The immutable Create archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| PCP.PENDING_CREATE | terminal | 95 | terminal | none | PCP.RESULT_CREATE | continue | Create initiation was accepted. Return pending and resume at PCP.RESULT_CREATE only when the user explicitly requests status. |
| PCP.DONE_QUERY | terminal | 70 | terminal | none | PCP.VERIFY_QUERY | continue | The read-only query result is persisted with redacted facts. |
| PCP.DONE_CREATE | terminal | 110 | terminal | none | PCP.VERIFY_CREATE | continue | The verified Create effect is persisted with redacted facts. |
| PCP.HDL_GATE_UPDATE | decision | 120 | execution_gate | initiated->PCP.RESULT_UPDATE;blocked->PCP.HANDLE_ERROR;failed->PCP.HANDLE_ERROR | PCP.ENFORCE_DESIGN | stop | The immutable Update archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| PCP.PENDING_UPDATE | terminal | 135 | terminal | none | PCP.RESULT_UPDATE | continue | Update initiation was accepted. Return pending and resume at PCP.RESULT_UPDATE only when the user explicitly requests status. |
| PCP.DONE_UPDATE | terminal | 150 | terminal | none | PCP.VERIFY_UPDATE | continue | The verified Update effect is persisted with redacted facts. |
| PCP.HDL_GATE_CORRECT_DELETE | decision | 160 | execution_gate | initiated->PCP.RESULT_CORRECT_DELETE;blocked->PCP.HANDLE_ERROR;failed->PCP.HANDLE_ERROR | PCP.ENFORCE_DESIGN | stop | The immutable one-action Correct MERGE or child DELETE archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. A MERGE has an explicit positive SubTypeSequence; a DELETE remains sealed to current state. |
| PCP.PENDING_CORRECT_DELETE | terminal | 175 | terminal | none | PCP.RESULT_CORRECT_DELETE | continue | Correct initiation was accepted. Return pending and resume at PCP.RESULT_CORRECT_DELETE only when the user explicitly requests status. |
| PCP.DONE_CORRECT_DELETE | terminal | 190 | terminal | none | PCP.VERIFY_CORRECT_DELETE | continue | The verified Correct child action is persisted with redacted facts. |
| PCP.HDL_GATE_END_DATE | decision | 200 | execution_gate | initiated->PCP.RESULT_END_DATE;blocked->PCP.HANDLE_ERROR;failed->PCP.HANDLE_ERROR | PCP.ENFORCE_DESIGN | stop | The immutable End Date archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| PCP.PENDING_END_DATE | terminal | 215 | terminal | none | PCP.RESULT_END_DATE | continue | End Date initiation was accepted. Return pending and resume at PCP.RESULT_END_DATE only when the user explicitly requests status. |
| PCP.DONE_END_DATE | terminal | 230 | terminal | none | PCP.VERIFY_END_DATE | continue | The verified End Date effect is persisted with redacted facts. |
| PCP.HDL_GATE_ZAP | decision | 240 | execution_gate | initiated->PCP.RESULT_ZAP;blocked->PCP.HANDLE_ERROR;failed->PCP.HANDLE_ERROR | PCP.ENFORCE_DESIGN | stop | The immutable Zap archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| PCP.PENDING_ZAP | terminal | 255 | terminal | none | PCP.RESULT_ZAP | continue | Zap initiation was accepted. Return pending and resume at PCP.RESULT_ZAP only when the user explicitly requests status. |
| PCP.DONE_ZAP | terminal | 270 | terminal | none | PCP.VERIFY_ZAP | continue | The verified Zap effect is persisted with redacted facts. |
| PCP.HANDLE_ERROR | step | 280 | error_handler | disclosed->PCP.FAILED | none | stop | Any lookup, validation, package, loader, verification, or persistence failure. |
| PCP.FAILED | terminal | 290 | terminal | none | PCP.HANDLE_ERROR | continue | The request stopped with a classified redacted diagnostic and safe next action. |
