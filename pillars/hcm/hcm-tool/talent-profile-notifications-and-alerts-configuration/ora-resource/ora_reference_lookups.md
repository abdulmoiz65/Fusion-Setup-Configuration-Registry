# Talent Notifications Reference Lookups

Guidance-only, blank-template, and draft-questionnaire modes perform no live
lookup. On the explicit implementation path, the preflight capability lookup
is the only live REST lookup. All notification resolution and readback lookups remain local to
`HRT_MANAGE_TALENT_NOTIFICATIONS` and use a fresh target-environment task
export stored in the durable run context.

## Source Basis

- Oracle REST API version and URL path guidance:
  `https://docs.oracle.com/en/cloud/saas/human-resources/farws/URL_Paths_for_REST_Services.html`
- Oracle collection `limit` and `onlyData` parameter contract:
  `https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-publicworkers-get.html`
- Oracle Talent Notifications GET-capability evidence:
  `https://docs.oracle.com/cd/F13257_01/tutorial/cloud/r13/wn/talent/releases/23D/23D-talent-mgmt-wn.htm`

These sources establish the resource name, GET capability, API resource
version, and bounded collection parameters only. Their release labels never
identify the selected environment's quarterly release.

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | verify_talent_notifications_rest_capability | After explicit implementation classification and authenticated environment validation, before any FSM export | environment and restBaseUrl from the active core.auth.fusion-oauth-authentication context; API resource version 11.13.18.05 | Through core.fusion-api.rest-api-client, GET /hcmRestApi/resources/11.13.18.05/talentNotifications with onlyData=true, limit=1, and timeout=60 seconds against the authenticated restBaseUrl | No fields projection; validate HTTP status and the JSON collection items array only | Require HTTP 200, the requested relative path on the authenticated target, and a JSON object whose items value is an array containing at most one item. Zero items is a successful capability result. Do not inspect or map item fields into notification runtime data. | capability_status=available; capability_failure_reason when blocked; environment; restBaseUrl; api_version=11.13.18.05; method=GET; relative_path; only_data=true; limit=1; timeout_seconds=60; checked_at; http_status; returned_item_count | After the core client's one permitted authentication refresh, classify final 401 as rest_capability_unauthenticated and final 403 as rest_capability_forbidden. Classify 404 as rest_capability_unavailable, timeout as rest_capability_timeout, transport as rest_capability_transport_failure, any other non-200 response as rest_capability_http_failure, and invalid JSON or collection shape as rest_capability_malformed_response. Stop before FSM export and never substitute another host, endpoint, browser, or direct client. |

## Local Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | resolve_talent_notification_targets | After input and dependency validation and before comparison or packaging | Original identity, label, or business intent; explicit proposed enabled value; validated current export and fingerprint; ordered eight-column schema; prior clarification evidence | First partition every export row by exact ProductCode: HRT is eligible, another nonblank value is out of scope, and missing or ambiguous selected scope is invalid. Run exact, case/whitespace, and semantic resolution only on eligible rows. Resolve one unique exact case-sensitive NotifId, NotifName, or NotifLabel automatically. A unique case/whitespace-only eligible correction returns mapping_confirmation_required. Otherwise search only eligible rows and their NotifLabel, NotifName, Description, GroupingKey, ViewInstanceName, and ProductCode for meaningful candidates; every semantic result requires confirmation. If no eligible target resolves, inspect the unfiltered export only for exact-identity diagnostics: an identity found solely under another product code returns out_of_scope_notification; no identity returns unsupported_by_current_fsm_provider. Never infer scope or expose a non-HRT candidate. After confirmation, prefer unique nonblank NotifId; if blank, require unique nonblank NotifName and mark provisional_notifname. Clone the selected complete HRT row, normalize the explicit enabled state to Y or N, and compare only NotifEnabled. | original_supplied_value; source_kind; eligible_rows; out_of_scope_rows; invalid_scope_rows; scope_disposition; scope_reason; semantic_candidates; match_rationale; resolved_notif_label; provider_identifier; provider_identifier_field; provider_key_status; confirmation_evidence; original_eight_column_row; current_enabled; proposed_enabled; changed_row; unchanged_row; export_reference | Any unsupported, out-of-scope, blank-scope, conflicting-scope, or ambiguous row fails the complete set before preview. Multiple direct matches, unconfirmed correction or candidate, rejected candidates without refinement, missing or duplicate provider key, changed export, schema drift, or unpreservable row also fails closed. |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | resolve_talent_notification_readback | After successful load completion and a new validated export | Approved provider identifiers and key fields; approved HRT scope; approved preview fingerprint; post-import rows; target environment; export timestamp | Partition the new export again and resolve exactly one eligible ProductCode HRT row using the same provider identifier field, then compare saved NotifEnabled with the approved Y or N. Do not fall back to another identity field after approval. | actual_enabled; expected_enabled; actual_product_scope; row_readback_result; match_count; mismatch_count; post_import_export_reference | Missing, multiple, non-HRT, blank-scope, changed provider identity, or different enabled value returns readback_failed with business comparison and exact internal evidence. |

## Lookup Outcomes

| Task Code | Task Name | Condition | Expected Result |
|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Fresh validated export is partitioned | Treat every exact ProductCode HRT row as eligible dynamically; retain other rows only as diagnostic evidence and do not use a name or count allowlist |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET returns HTTP 200 with an empty items array | Record the sanitized available receipt and continue; data presence is not required for capability validation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET returns HTTP 200 with one item | Record only the sanitized capability receipt; never use the item as a target, candidate, current-state, package, or readback source |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Capability GET fails authentication, authorization, availability, transport, timeout, HTTP, or response-shape validation | Return validation_failed under the owning failure class and retain the corresponding distinct `rest_capability_*` reason before any FSM export or persistence |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | One exact case-sensitive NotifId, NotifName, or NotifLabel match in the eligible HRT partition | Resolve automatically and preserve the exact exported row |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | One eligible direct match only after case/whitespace normalization | Return mapping_confirmation_required and preserve the exact delivered value |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | One or more meaningful semantic matches among eligible HRT rows | Return candidate_selection_required with up to five candidates; even one strong candidate requires confirmation |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | User selects multiple candidates | Resolve every selected candidate independently and retain one explicit enabled value per input row |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | User rejects or refines candidates | Preserve the original intent and evidence; rerun discovery only against the same or a refreshed validated export |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Exact identity exists only under an exported non-HRT product code | Return validation_failed with reason out_of_scope_notification; never expose the row as a candidate or package it |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Identity is absent from the current FSM export | Return validation_failed with reason unsupported_by_current_fsm_provider |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | No meaningful eligible semantic candidate | Request more event or recipient context with unsupported_by_current_fsm_provider; do not search non-HRT rows semantically |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Selected identity has blank, conflicting, or ambiguous product scope | Return validation_failed for the complete set and require fresh valid FSM evidence |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Nonblank unique NotifId exists | Use NotifId as the provider identifier and record confirmed_notifid |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | NotifId is blank and NotifName is nonblank and unique | Use NotifName provisionally and record provisional_notifname |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Provider identifier is missing, duplicated, or changes | Fail closed before preview or return readback_failed after execution |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Duplicate inputs resolve to the same row and same state | Consolidate one normalized row and retain all source references |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Duplicate inputs resolve to the same row with conflicting states | Block the complete set until one state is supplied |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Selected eligible HRT row is prepared for import | Preserve all eight serialized fields, retain ProductCode HRT, and replace only NotifEnabled with Y or N |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | All selected values match | Return exact_match_no_change without package, approval, or import |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Some values differ | Package only approved changed rows; retain exact-match rows in preview and omit unrelated rows |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Load remains active or post-import export is unavailable | Keep pending_readback; do not claim success or submit again |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | Post-import provider identity resolves without exact ProductCode HRT | Return readback_failed; never accept another product scope |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.CHECK_REST_CAPABILITY | step | 3 | reference_lookup | available->TPN.CHECK_DEPENDENCIES;blocked->TPN.RETURN_VALIDATION_FAILED | TPN.VALIDATE_INPUT | stop | For explicit implementation only, use the authenticated FDOS environment to run the one source-backed bounded Talent Notifications GET; retain only a sanitized capability receipt and no notification data |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RESOLVE_TARGETS | decision | 5 | evaluate_result | resolved->TPN.APPLY_TRACE_DEFAULTS;mapping_confirmation_required->TPN.RETURN_MAPPING_CONFIRMATION_REQUIRED;candidate_selection_required->TPN.RETURN_CANDIDATE_SELECTION_REQUIRED;blocked->TPN.RETURN_VALIDATION_FAILED | TPN.CHECK_DEPENDENCIES | stop | Partition the fresh export by exact ProductCode, resolve direct or semantic targets only within eligible HRT rows, diagnose unsupported or out-of-scope identities, require confirmation, select a stable provider key, preserve complete rows, and compare only NotifEnabled |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.RESOLVE_READBACK | decision | 9 | evaluate_result | match->TPN.RETURN_VERIFIED;mismatch->TPN.RETURN_READBACK_FAILED;blocked->TPN.RETURN_READBACK_FAILED | TPN.EXECUTION_GATE | stop | Verify approved provider identifiers, exact ProductCode HRT scope, and NotifEnabled values using a fresh post-import export |
