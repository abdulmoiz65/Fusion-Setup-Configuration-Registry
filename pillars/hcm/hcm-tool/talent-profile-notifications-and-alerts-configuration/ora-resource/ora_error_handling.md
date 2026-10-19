# Talent Notifications Error Handling and Execution Gates

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Request has no explicit implementation intent | Classify a pure question as guidance_only, a blank-template request as blank_template, and supplied or collected values as draft_questionnaire; do not initialize an implementation run or call Fusion |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Guidance-only, blank-template, or draft-questionnaire mode attempts project, authentication, REST, FSM, Data Loader, or persistence approval | Stop that dependency path and return the applicable side-effect-free result |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Checked-in blank workbook is missing or unreadable | Return validation_failed with reason blank_template_unavailable; do not regenerate, substitute, or call Fusion |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Draft questionnaire contains a value not explicitly supplied by the user or lacks its unvalidated label | Remove the inferred or enriched value, preserve it only as an open question, apply the required label, and return draft_questionnaire_provided |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Authenticated FDOS environment context is missing, malformed, or conflicts with the selected project | Return validation_failed with Fusion login or environment-configuration guidance; do not accept a user-supplied host or ask for a quarterly release |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Quarterly-release metadata is absent | Continue without a release value or source; absence is not a preflight failure |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Trusted authenticated-context and validated FSM quarterly-release values conflict | Return catalog_or_metadata_mismatch and require refreshed trusted evidence; do not ask the user to choose a release |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Bounded Talent Notifications GET returns HTTP 200 with a valid empty or one-item collection | Record only the sanitized capability receipt and continue to FSM dependencies; never retain the item as notification runtime evidence |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET ends in 401 after the core client's one permitted authentication refresh | Return auth_expired_or_invalid with reason rest_capability_unauthenticated and stop before FSM export |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET ends in 403 after the core client's one permitted authentication refresh | Return authorization_or_privilege with reason rest_capability_forbidden and stop before FSM export |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET returns 404 | Return validation_failed with reason rest_capability_unavailable and stop before FSM export; do not try another endpoint |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET reaches its 60-second timeout | Return transport_or_environment with reason rest_capability_timeout and stop before FSM export without automatic retry |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET fails before receiving an HTTP response | Return transport_or_environment with reason rest_capability_transport_failure and stop before FSM export without automatic retry |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET returns a non-200 status other than final 401, 403, or 404 | Return fusion_api_error with reason rest_capability_http_failure and stop before FSM export without automatic retry |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET returns invalid JSON or an invalid collection shape | Return fusion_api_error with reason rest_capability_malformed_response and stop before FSM export without automatic retry |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Target text or enabled state is missing or invalid | Return validation_failed and request the exact missing business value |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Legacy Worklist or Email columns appear | Return validation_failed with migration guidance to one Notification Enabled column; do not merge values |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | One case/whitespace-only correction exists | Return mapping_confirmation_required with the exact delivered identity; do not request persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | One or more semantic candidates exist | Return candidate_selection_required with up to five candidates, rationale, and current state; require selection even for one candidate |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Exact identity exists only under an exported non-HRT product code | Return validation_failed with reason out_of_scope_notification; do not expose the row as a candidate or continue any row in the set |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Requested identity is absent from current FSM evidence | Return validation_failed with reason unsupported_by_current_fsm_provider; do not use REST or another route |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | No meaningful eligible HRT candidate exists | Request more event or recipient context with reason unsupported_by_current_fsm_provider; do not guess, recommend policy, or search non-HRT rows semantically |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Selected row has missing, conflicting, or ambiguous ProductCode evidence | Return validation_failed for the complete set and require a fresh valid export; never infer scope |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | A mixed request contains eligible and unsupported, out-of-scope, or invalid-scope rows | Fail the complete set before preview or package preparation; do not partially process eligible rows |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Candidate set is rejected or refined | Preserve the original intent and prior evidence and resume the same run without losing unrelated confirmations |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Provider key is blank, duplicated, unavailable, changes, or resolves without exact ProductCode HRT | Return validation_failed before submission or readback_failed after execution; never switch keys or scope silently |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Any non-enabled serialized field cannot be copied exactly | Return catalog_or_metadata_mismatch and stop before package preparation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Metadata, required CSV members, header, encoding, BOM, quoting, or native line endings differ | Stop and rebuild the minimal package from fresh export evidence |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | An omitted row is treated as deleted or an unrelated row is included | Reject the package; omission means unchanged and the skill never deletes notifications |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Catalog, task, authenticated environment, trusted release evidence, template, current export, or eight-column schema disagree | Stop; do not infer missing values or substitute another route |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Data Loader preview is unapproved or fingerprint changed | Return approval_required for the latest preview or rebuild it; never reuse approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Data Loader accepted initiation or remains active | Persist pending_readback and end without polling or claiming success |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Load failed, timed out, is uncertain, or readback differs | Persist readback_failed with evidence and one safe next action; never replay |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Reusable workbook cannot be authored or maintained | Report only a template-maintenance limitation; continue valid direct, CSV, DOCX, PDF, text, or existing-XLSX input |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Alerts Composer work is explicit but Alert Foundation is unavailable | Retain a deferred handoff and continue supported notification enablement |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | input_validation | Missing, malformed, ambiguous, unconfirmed, conflicting, unsupported, or out-of-scope business values | Correct the row, confirm mapping, select/refine eligible candidates, or use a supported Profile Management FSM identity |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | catalog_or_metadata_mismatch | Task, environment, schema, product scope, provider identity, serialized row, member, or export evidence differs | Obtain fresh exact-task evidence and repeat scope partition and resolution |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | auth_expired_or_invalid | Delegated authentication, including the capability GET, cannot be refreshed by its owner | Re-authenticate through the owning core service |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | authorization_or_privilege | Capability GET, export, status, upload, or import privilege is absent | Obtain required access; do not bypass |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | transport_or_environment | Target service or environment is unavailable | Preserve evidence and retry only a permitted read after recovery |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | fusion_api_error | A delegated Fusion operation reports an application error | Preserve the sanitized error and owning operation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | process_timeout | Export, import, or status reaches its limit | Record the reference, last status, and continuation path |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | process_failed | Export or import reaches a failed terminal state | Preserve logs or status evidence and stop |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | artifact_persistence | A run artifact cannot be written or registered | Preserve diagnostics safely and do not mutate Fusion |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | approval_blocker | Preview, approval, immutable artifact, or authorized route is missing or stale | Rebuild the preview and obtain one explicit approval |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Request-mode result | Selected request mode and confirmation that guidance_only, blank_template, and draft_questionnaire performed no Fusion lookup or implementation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Blank-template result | Direct reference to the unchanged checked-in requirements workbook; no generated-copy or validation claim |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Draft-questionnaire result | Exact user-supplied values, open questions for missing information, and `UNVALIDATED DRAFT - no Fusion lookup or implementation has been performed` |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Authenticated preflight | Authenticated environment identity, sanitized target origin, GET capability status, API resource version, checked-at time, and failure classification when blocked; show quarterly release only when trusted metadata explicitly supplied it |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Mapping clarification | Original value and one exact delivered case/whitespace correction; state that confirmation is not persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Candidate selection | Original intent; up to five eligible delivered labels and provider identifiers; current state; event/recipient explanation; match rationale; selection, reject, and refine choices; no non-HRT candidate |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Scope validation failure | Original request; plain-language Profile Management FSM boundary; out_of_scope_notification or unsupported_by_current_fsm_provider reason; no candidate, preview, package, or partial processing |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Business preview | Source; original identity or intent; exact eligible label and provider identifier; key status; mapping and candidate confirmations; current/requested state; changed/no-change result; Profile Management FSM eligibility; exclusions; channel boundary; delivery-testing exclusion; package row and member summary; archive fingerprint; Data Loader evidence; Alert Foundation status; one authoritative question |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Pending continuation | pending_readback, execution reference, last known status, and safe continuation instruction; do not claim configured |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Readback result | Original intent, delivered label, provider identifier, expected and actual states, per-row result, discrepancies, execution reference, timestamp, and alert-handoff status |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Request mode is not explicit implementation | Do not initialize an implementation project run, authenticate, call REST, request an FSM export, resolve target state, invoke Data Loader, or ask for persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Blank template is requested | Do not create, copy, rename, populate, or regenerate XLSX; return only the existing checked-in workbook unchanged |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Draft questionnaire is requested | Do not require complete requirements, normalize or enrich business values, infer notification identity or enabled state, claim validation, generate XLSX automatically, or call Fusion |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | A file or row is supplied without a change instruction | Do not treat the source as implementation approval; preserve it as unvalidated draft input and ask whether implementation is wanted |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Environment or release preflight | Do not ask for a quarterly release, accept a user-derived host, or infer release from API version 11.13.18.05, hostname, documentation, date, catalog path, or conversation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | REST capability preflight | Do not call a different endpoint or host, retain returned notification data, run more than the one bounded GET, or treat GET access as FSM write support |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Mapping confirmation or candidate selection completes | Do not interpret clarification as persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Semantic input is supplied | Do not select a candidate without confirmation or recommend which notification policy the business should adopt |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Scope partition or candidate discovery runs | Do not infer scope from a prefix, label, description, intent, or tab; do not show non-HRT rows as candidates or use a fixed notification inventory |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | A row is unsupported, out of scope, or has invalid scope evidence | Do not preview, package, or submit any row in the configuration set and do not fall back to REST or browser automation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Provider key is provisional | Do not hide the fallback or switch to another key after approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Minimal package is built | Do not delete required members, include unrelated or non-HRT rows, normalize native CSV bytes, or encode a deletion for omitted rows |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Preview is ready | Do not ask any persistence question other than: Do you want to proceed with submitting the reviewed archive? |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Approval is absent, negative, ambiguous, or stale | Do not submit; remain approval_required or rebuild the preview |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Submission outcome is uncertain | Do not retry, replay, or create another approval automatically |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Readback differs | Do not auto-correct or import again |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Alerts Composer requirement exists | Do not execute it locally or report it configured; use ready_for_handoff or deferred |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.EXECUTION_GATE | decision | 8 | execution_gate | no_change->TPN.RETURN_EXACT_MATCH;preview_ready->TPN.RETURN_APPROVAL_REQUIRED;approved_and_submitted->TPN.RETURN_PENDING_READBACK;execution_failed->TPN.RETURN_EXECUTION_FAILED;status_active->TPN.RETURN_PENDING_READBACK;status_complete->TPN.RESOLVE_READBACK;status_failed->TPN.RETURN_READBACK_FAILED | TPN.ENFORCE_DESIGN | stop | On the explicit implementation path, delegate immutable preview, the single approval, submission, and continuation status to core.data-loader; never bypass it |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_VALIDATION_FAILED | terminal | 10 | terminal | none | none | stop | Return validation_failed with request-mode, preflight, or row-level causes, including deterministic scope reason codes, whole-set failure, and no Fusion mutation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_MAPPING_CONFIRMATION_REQUIRED | terminal | 11 | terminal | none | TPN.RESOLVE_TARGETS | stop | Persist mapping_confirmation_required and return the exact delivered correction without persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_CANDIDATE_SELECTION_REQUIRED | terminal | 12 | terminal | none | TPN.RESOLVE_TARGETS | stop | Persist candidate_selection_required with original intent, candidates, rationale, state, and export reference |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_EXACT_MATCH | terminal | 13 | terminal | none | TPN.ENFORCE_DESIGN | stop | Return exact_match_no_change without package, approval, or import |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_APPROVAL_REQUIRED | terminal | 14 | terminal | none | TPN.EXECUTION_GATE | stop | Return the immutable business preview and one Data Loader submission question |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_PENDING_READBACK | terminal | 15 | terminal | none | TPN.EXECUTION_GATE | stop | Persist pending_readback after accepted or active execution and stop without claiming success |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_VERIFIED | terminal | 16 | terminal | none | TPN.RESOLVE_READBACK | stop | Return verified only after successful completion and matching fresh-export readback |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_READBACK_FAILED | terminal | 17 | terminal | none | none | stop | Return readback_failed for failed, uncertain, missing, ambiguous, changed-key, or mismatched post-import evidence |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_EXECUTION_FAILED | terminal | 18 | terminal | none | TPN.EXECUTION_GATE | stop | Return a sanitized execution failure without retry or replay |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_GUIDANCE | terminal | 19 | terminal | none | TPN.CLASSIFY_REQUEST | stop | Return guidance_provided from local checked-in guidance without project, authentication, REST, FSM, Data Loader, or persistence approval |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_BLANK_TEMPLATE | terminal | 20 | terminal | none | TPN.CLASSIFY_REQUEST | stop | Return blank_template_provided with the existing checked-in XLSX unchanged and no runtime generation or Fusion-dependent work |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RETURN_DRAFT_QUESTIONNAIRE | terminal | 21 | terminal | none | TPN.CLASSIFY_REQUEST | stop | Return draft_questionnaire_provided containing user-supplied values and open questions only under the required unvalidated label, without XLSX conversion or Fusion-dependent work |
