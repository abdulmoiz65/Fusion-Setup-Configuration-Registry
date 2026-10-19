# Location Costing Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input or request construction fails before dispatch. | Classify input_validation and report the exact invalid field or logical query rule. Do not claim Fusion returned an HTTP status. |
| DNS, proxy, TLS, connection, or timeout fails without an HTTP response. | Classify transport_or_environment, preserve sanitized endpoint and environment identity, and stop. |
| A governed GET receives 401 or a credential-expiry indication. | Classify auth_expired_or_invalid. The governed client may refresh a managed cached token and retry that GET once. |
| A governed GET receives 403. | Permit the same single managed-token refresh check; if 403 persists or explicitly denotes missing access, classify authorization_or_privilege and stop. |
| Fusion returns a real non-2xx response other than the handled authentication case. | Classify fusion_api_error and preserve the actual status, relative endpoint, sanitized body summary, and ECID when present. Report HTTP 400 only when the client actually received status 400. |
| HTTP 2xx contains invalid JSON, a wrong envelope, wrong types, missing required fields, or wrong cardinality for an identity-fixed or contractually singular response. | Classify catalog_or_metadata_mismatch with diagnostic detail response_contract_mismatch. Never relabel this local parse or normalization failure as HTTP 400 or fusion_api_error. |
| A valid discovery or candidate-search response has zero matches, multiple candidates, or needs a user selection. | Report lookup resolution required with the sanitized candidate or missing-value summary. This is not a transport, fixed-response contract, or Fusion API failure. |
| KFF or current Data Loader template does not support required account fields. | Classify catalog_or_metadata_mismatch and stop before preview. |
| Complete history, Zap fan-out, physical identity, or exact source binding is missing. | Classify input_validation when supplied evidence is invalid, otherwise catalog_or_metadata_mismatch when a valid response lacks the required contract. Stop before handoff. |
| Fresh approval or an authorized import workflow is missing. | Classify approval_blocker and retain only the sanitized immutable preview. |
| A downstream Data Loader process later times out or fails. | The active loader workflow owns process_timeout or process_failed diagnostics, including Request ID and status. This authoring resource does not poll or retry it. |
| A required durable artifact cannot be stored by the active workflow. | Classify artifact_persistence and stop before mutation handoff. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing or invalid operation, identity, date, distribution, sequence, confirmation, or pre-dispatch query value. | Correct the named input and restart from validation. |
| lookup_resolution_required | A valid discovery or candidate-search lookup has zero matches, multiple candidates, or needs one explicit user selection. | Refine the lookup input or select one returned candidate; do not classify it as an HTTP or fixed-response contract failure. |
| catalog_or_metadata_mismatch | A valid response or template does not meet the documented shape or capability. | Preserve response_contract_mismatch detail when applicable, correct the contract or metadata, and rerun the read-only branch. |
| auth_expired_or_invalid | A managed credential is rejected or explicitly expired. | Refresh once for the GET through the governed client, then stop if rejected again. |
| authorization_or_privilege | Access remains denied after the one allowed credential check or Fusion explicitly reports missing privilege. | Obtain the required role or environment access; do not retry. |
| transport_or_environment | No HTTP response exists because connectivity, proxy, TLS, or timeout failed. | Correct the environment path and start a new read-only attempt. |
| fusion_api_error | Fusion actually returned a non-2xx HTTP response. | Report the observed sanitized status and diagnostic; do not invent or replace it. |
| process_timeout | A separately authorized downstream loader status workflow exceeds its polling window. | Report Request ID, last status, elapsed time, and next-check path; do not resubmit. |
| process_failed | A separately authorized downstream loader reaches a failed terminal status or verification mismatch. | Preserve sanitized process diagnostics and stop without replay. |
| artifact_persistence | Required preview, run record, or safe resume state cannot be persisted. | Repair persistence before handoff. |
| approval_blocker | Exact fresh approval or an authorized mutation workflow is absent. | Obtain approval for the same immutable artifact and target. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup stop | Selected operation, relative endpoint, resolver, actual HTTP status when one exists, local diagnostic category, and one safe next action. |
| Response contract mismatch | HTTP 2xx status, expected envelope or cardinality, sanitized observed shape, and response_contract_mismatch detail. |
| Mutation handoff | Target environment, operation, expected business effect, immutable artifact fingerprint, template validation, authorized workflow, and fresh approval fingerprint. |
| Downstream status | Only the active loader workflow may show sanitized Request ID, last status, elapsed time, verification result, and next-check path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Read-only lookup | Do not invoke POST, PATCH, PUT, DELETE, browser mutation, raw UCM, or an ungoverned client. |
| Request serialization | Honor the request-shape and single-encoding contract in ora_reference_lookups.md; do not pass both a pre-encoded full URL and separate logical query values. |
| Local contract error | Do not report a synthetic HTTP 400 or call the result a Fusion API error. |
| Mutation | Do not build or execute DAT, ZIP, upload, import, polling, retry, or verification from these ora-resource files. |
| Retry | Do not automatically retry a live mutation. Do not retry a GET beyond the one managed-token refresh attempt. |
| Sensitive data | Do not print or persist credentials, tokens, cookies, private URLs, or sensitive payloads. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCP.GOVERNED_DATALOADER_HANDOFF | decision | 730 | execution_gate | ready_create->LCP.READY_CREATE;ready_update->LCP.READY_UPDATE;ready_correct->LCP.READY_CORRECT;ready_end_date->LCP.READY_END_DATE;ready_zap->LCP.READY_ZAP;blocked->LCP.HANDLE_ERROR;failed->LCP.HANDLE_ERROR | LCP.ENFORCE_DESIGN | stop | Confirm an independently authorized governed import workflow can receive the selected operation, exact lookup evidence, template validation, immutable artifact, and fresh approval. No mutation occurs in this node. |
| LCP.READY_CREATE | terminal | 740 | terminal | none | LCP.GOVERNED_DATALOADER_HANDOFF | continue | Create preflight is ready for the active governed import workflow; Fusion has not been changed by this resource. |
| LCP.READY_UPDATE | terminal | 741 | terminal | none | LCP.GOVERNED_DATALOADER_HANDOFF | continue | Update preflight is ready for the active governed import workflow; Fusion has not been changed by this resource. |
| LCP.READY_CORRECT | terminal | 742 | terminal | none | LCP.GOVERNED_DATALOADER_HANDOFF | continue | Correct preflight is ready for the active governed import workflow; Fusion has not been changed by this resource. |
| LCP.READY_END_DATE | terminal | 743 | terminal | none | LCP.GOVERNED_DATALOADER_HANDOFF | continue | End Date preflight is ready for the active governed import workflow; Fusion has not been changed by this resource. |
| LCP.READY_ZAP | terminal | 744 | terminal | none | LCP.GOVERNED_DATALOADER_HANDOFF | continue | Zap preflight is ready for the active governed import workflow; Fusion has not been changed by this resource. |
| LCP.NEEDS_OPERATION_SELECTION | terminal | 745 | terminal | none | LCP.RESOLVE_LOCATION_SOURCE | continue | Create found an existing active allocation and requires a new explicit Update or Correct request. |
| LCP.DONE_QUERY | terminal | 746 | terminal | none | LCP.RESOLVE_CURRENT_ALLOCATION | continue | Query returned one normalized read-only state or an explicit empty result with no duplicate GET. |
| LCP.NEEDS_LDG_SELECTION | terminal | 747 | terminal | none | LCP.SEARCH_LDG | continue | Multiple LDG candidates require one explicit returned Name before any later lookup. |
| LCP.HANDLE_ERROR | step | 900 | error_handler | disclosed->LCP.FAILED | none | stop | A validation, lookup, contract, authorization, transport, metadata, approval, or persistence failure must be classified and disclosed without exposing sensitive data. |
| LCP.FAILED | terminal | 910 | terminal | none | LCP.HANDLE_ERROR | continue | The task stopped with a classified sanitized diagnostic and one safe next action. |
