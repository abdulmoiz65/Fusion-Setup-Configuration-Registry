# Job Costing Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity, date, account value, KFF value, or accepted loader handoff reference is missing; a Create/effective-dated Update supplied account SourceType is not JOB; Create explicitly supplies SourceSubType other than COST or an ambiguous user date; a clear is requested through #NULL, JSON null, or an empty value; a Correct MERGE SubTypeSequence is missing, nonpositive, inferred, or conflicts with REST state; a Correct child DELETE supplies caller account facts, lacks sealed bound current-state evidence, selects no/ambiguous/orphaning child, or has null/blank/#NULL SourceSubType; an End Date lacks sealed complete history/detail state and a valid date range; or a Zap lacks sealed complete parent/history/child evidence or destructive JSON boolean true confirmation. | Classify as input_validation. For Create, request date clarification or reject the explicit non-COST subtype before HDL; never silently convert it. When REST omitted Correct SubTypeSequence, ask the user for the exact positive HDL value; otherwise stop before package generation or status verification. |
| LDG bounded Name LIKE discovery returns no candidates, unresolved selection, eleven rows or hasMore=true without an exact candidate, malformed paging, or the exact row lacks a positive CostAllocationIdFlexNumber. | Classify as catalog_or_metadata_mismatch or input_validation and stop before KFF, HDL, or Data Loader. Use only the validated plain Name LIKE q expression; never derive an ID or flex number. Request narrower LDG text when too broad. |
| resolve_runtime_costing_kff, resolve_costing_job_segment_qualifiers, or validate_costing_segment_value fails because the runtime discriminator differs, required KFF/LOV metadata is missing, a Job qualifier cannot be reconciled, Value Set paging is incomplete, or an exact supplied Value is absent or conflicting. | Classify a missing or invalid supplied value as input_validation, a metadata or identity conflict as catalog_or_metadata_mismatch, and an HTTP failure as auth_authz, transport_environment, or fusion_api_error according to the response. Stop before HDL rendering, approval, or Data Loader; preserve only a redacted diagnostic. Never guess an index or copy runtime `SEGMENTn` spelling into HDL; derive and template-validate each canonical `Segment<N>` attribute. |
| The Job search SetCode derived from that request's DisplayAttributes differs from jobsLov.SetCode, a separately returned SetName differs from jobsLov.SetName, an exact Job, jobsLov, or LDG response has hasMore=true or lacks explicit hasMore=false, jobsLov is ambiguous, or its SetCode is blank. Never compare SetCode with SetName. | Classify as catalog_or_metadata_mismatch and stop on a like-typed mismatch. Do not infer a SetCode from the display value or SetId. |
| A documented GET or governed read-only decision-action result is malformed, incomplete, unauthorized, or ambiguous. | Classify as catalog_or_metadata_mismatch, auth_authz, or transport_environment and stop; refresh a cached token once only for a read. |
| Create findExistingRecord returns a string "true"/"false", null, a missing result, or any value outside the documented JSON booleans true and false; futureRecordExists returns an empty HTTP 200 body, a missing result, string "null", another unsupported JSON shape or type, or an unsuccessful status. | Classify as catalog_or_metadata_mismatch for a response-contract difference, auth_authz for authorization failure, transport_environment for transport failure, or fusion_api_error for an API failure. Stop before the next action, Create KFF, or HDL; never coerce a string to a JSON boolean or null, and never treat an empty or missing result as absence. |
| A documented read-only Fusion endpoint returns a recognized Fusion API error after the permitted token refresh. | Classify as fusion_api_error; preserve a redacted diagnostic and do not substitute a write route. |
| Data Loader source/schema or Task Hook validation fails, including a runtime KFF column rendered with a noncanonical HDL segment name. | Classify as catalog_or_metadata_mismatch or process_failed; preserve redacted diagnostics and do not substitute a route. |
| A final Job Costing DAT omits an operation-applicable mandatory attribute, omits SetCode from either Job MERGE component, leaves a required value blank, or differs from the DAT that was validated before ZIP creation. | Classify as input_validation and stop before approval, upload, or initiation. Rebuild the exact ZIP with the complete jobsLov-derived Job key and all applicable mandatory values, then repeat source/schema and Task Hook validation; an earlier generic validation result does not certify the corrected archive. |
| A terminal loader status is failed or a verification GET after terminal success does not match the requested effect. | Classify as process_failed; stop without retry and require a new preview and approval. |
| The user explicitly asks for a status check and the loader remains initiated, in progress, or exceeds the requested observation window. | Classify as pending or process_timeout; return the pending handoff with a safe next-check option and do not retry or poll automatically. |
| A direct REST mutation or unsupported operation is requested. | Classify as approval_blocker or input_validation and state that only Create, Update, Correct, End Date, or Zap HDL is in scope; Delete (ED Split) remains blocked. |
| A Correct stage fails, does not verify, or has an unsafe intermediate total. | Stop before any later sibling stage and require a fresh plan from observed read-only state. |
| Required redacted archive, registry, run, or diagnostic persistence fails. | Classify as artifact_persistence and stop before approval or handoff. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required source key, sealed context/history/details evidence, account value, date, approval, accepted handoff reference, positive Correct MERGE SubTypeSequence, sealed Correct child DELETE selection, Correct SourceSubType, JSON boolean destructive confirmation, or Zap parent/history/child evidence is missing; a clear is requested without an explicit-clear contract; or a Create/Update serial is not positive and consecutive from 1. | Ask the user for Correct SubTypeSequence when REST omits it; generate serials from supplied account-row order only for Create/Update. Never infer a Correct sequence. |
| catalog_or_metadata_mismatch | Official key shape, jobsLov SetCode evidence, KFF metadata, or loader schema differs. | Stop and correct the source contract; never substitute a display SetName or SetId for SetCode. |
| auth_authz | A read cannot authenticate or authorize after one refresh. | Request the required read privilege. |
| transport_environment | Read transport fails. | Preserve redacted diagnostics and retry only the documented read when safe. |
| fusion_api_error | A documented read-only Fusion endpoint returns a recognized API error after the permitted token refresh. | Preserve a redacted diagnostic and stop; do not substitute a write route. |
| process_timeout | An explicitly requested status observation window ends before a terminal result. | Return pending with the safe next-check path; do not poll or retry automatically. |
| process_failed | A terminal loader result or subsequent verification is unsuccessful. | Do not retry without a new preview and approval. |
| artifact_persistence | Required redacted archive, registry, run, or diagnostic persistence fails. | Stop before approval or handoff and restore the durable artifact path. |
| approval_blocker | Archive approval is absent, stale, or mismatched. | Present the exact immutable archive again. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| HDL preview | Sanitized environment, operation, official identity fingerprint, archive fingerprint, expected effect, and fresh approval requirement. |
| Accepted loader handoff | Sanitized environment, Content ID, Request ID, initiated or pending state, and the message that the load can take several minutes with an offered status check. |
| User-requested loader status | Sanitized environment, Content ID, Request ID, current status, elapsed wait when applicable, and safe next-check path. |
| Verification | Requested scope, redacted expected-versus-actual state, and safe next action. |
| Failure | Failure class, stage, redacted artifact reference, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mutation route | Do not use arbitrary REST POST, PATCH, PUT, DELETE, genericCosting Data Loader business objects, raw UCM/import endpoints, browser replay, or FSM. The exact findExistingRecord and futureRecordExists POST actions are read-only decisions, not mutation routes. |
| Approval | Do not hand off an archive without current approval bound to its exact immutable fingerprint. |
| Loader status | Do not poll automatically after initial handoff. Do not verify or retry until an explicit user status or verification request confirms terminal success for the exact Content ID and Request ID. |
| Retry | Do not automatically retry an import or replay an uncertain mutation. |
| Diagnostics | Do not persist or disclose credentials, tokens, hosts, raw payloads, account values, or technical identifiers. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JCP.HDL_GATE_CREATE | decision | 80 | execution_gate | submitted->JCP.SUBMITTED_CREATE;blocked->JCP.HANDLE_ERROR;failed->JCP.HANDLE_ERROR | JCP.ENFORCE_DESIGN | stop | The immutable Create archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| JCP.SUBMITTED_CREATE | terminal | 85 | terminal | none | JCP.HDL_GATE_CREATE | continue | The Create handoff was accepted. Report initiated or pending, explain that it can take several minutes, and offer a later status check. |
| JCP.PENDING_CREATE | terminal | 95 | terminal | none | JCP.RESULT_CREATE | continue | The explicitly checked Create handoff is still pending or its observation window ended. Report a safe next-check path without polling. |
| JCP.DONE_QUERY | terminal | 70 | terminal | none | JCP.VERIFY_QUERY | continue | The read-only query result is persisted with redacted facts. |
| JCP.DONE_CREATE | terminal | 110 | terminal | none | JCP.VERIFY_CREATE | continue | The verified Create effect is persisted with redacted facts. |
| JCP.HDL_GATE_UPDATE | decision | 120 | execution_gate | submitted->JCP.SUBMITTED_UPDATE;blocked->JCP.HANDLE_ERROR;failed->JCP.HANDLE_ERROR | JCP.ENFORCE_DESIGN | stop | The immutable Update archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| JCP.SUBMITTED_UPDATE | terminal | 125 | terminal | none | JCP.HDL_GATE_UPDATE | continue | The Update handoff was accepted. Report initiated or pending, explain that it can take several minutes, and offer a later status check. |
| JCP.PENDING_UPDATE | terminal | 135 | terminal | none | JCP.RESULT_UPDATE | continue | The explicitly checked Update handoff is still pending or its observation window ended. Report a safe next-check path without polling. |
| JCP.DONE_UPDATE | terminal | 150 | terminal | none | JCP.VERIFY_UPDATE | continue | The verified Update effect is persisted with redacted facts. |
| JCP.HDL_GATE_CORRECT | decision | 160 | execution_gate | submitted->JCP.SUBMITTED_CORRECT;blocked->JCP.HANDLE_ERROR;failed->JCP.HANDLE_ERROR | JCP.ENFORCE_DESIGN | stop | The immutable one-action Correct MERGE or child DELETE archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. A MERGE has an explicit positive SubTypeSequence; a DELETE remains sealed to current state. |
| JCP.SUBMITTED_CORRECT | terminal | 165 | terminal | none | JCP.HDL_GATE_CORRECT | continue | The Correct handoff was accepted. Report initiated or pending, explain that it can take several minutes, and offer a later status check. |
| JCP.PENDING_CORRECT | terminal | 175 | terminal | none | JCP.RESULT_CORRECT | continue | The explicitly checked Correct handoff is still pending or its observation window ended. Report a safe next-check path without polling. |
| JCP.DONE_CORRECT | terminal | 190 | terminal | none | JCP.VERIFY_CORRECT | continue | The verified Correct account effect is persisted with redacted facts. |
| JCP.HDL_GATE_END_DATE | decision | 200 | execution_gate | submitted->JCP.SUBMITTED_END_DATE;blocked->JCP.HANDLE_ERROR;failed->JCP.HANDLE_ERROR | JCP.ENFORCE_DESIGN | stop | The immutable End Date archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| JCP.SUBMITTED_END_DATE | terminal | 205 | terminal | none | JCP.HDL_GATE_END_DATE | continue | The End Date handoff was accepted. Report initiated or pending, explain that it can take several minutes, and offer a later status check. |
| JCP.PENDING_END_DATE | terminal | 215 | terminal | none | JCP.RESULT_END_DATE | continue | The explicitly checked End Date handoff is still pending or its observation window ended. Report a safe next-check path without polling. |
| JCP.DONE_END_DATE | terminal | 230 | terminal | none | JCP.VERIFY_END_DATE | continue | The verified End Date effect is persisted with redacted facts. |
| JCP.HDL_GATE_ZAP | decision | 240 | execution_gate | submitted->JCP.SUBMITTED_ZAP;blocked->JCP.HANDLE_ERROR;failed->JCP.HANDLE_ERROR | JCP.ENFORCE_DESIGN | stop | The immutable Zap archive contains every resolved child DELETE and the logical parent DELETE, passed source/schema and Task Hook validation, has fresh destructive approval, and is handed once to core.data-loader. |
| JCP.SUBMITTED_ZAP | terminal | 245 | terminal | none | JCP.HDL_GATE_ZAP | continue | The Zap handoff was accepted. Report initiated or pending, explain that it can take several minutes, and offer a later status check. |
| JCP.PENDING_ZAP | terminal | 255 | terminal | none | JCP.RESULT_ZAP | continue | The explicitly checked Zap handoff is still pending or its observation window ended. Report a safe next-check path without polling. |
| JCP.DONE_ZAP | terminal | 270 | terminal | none | JCP.VERIFY_ZAP | continue | The verified complete logical-history Zap effect is persisted with redacted facts. |
| JCP.HANDLE_ERROR | step | 280 | error_handler | disclosed->JCP.FAILED | none | stop | Any validation, lookup, package, loader, verification, or persistence failure. |
| JCP.FAILED | terminal | 290 | terminal | none | JCP.HANDLE_ERROR | continue | The request stopped with a classified diagnostic and safe next action. |
