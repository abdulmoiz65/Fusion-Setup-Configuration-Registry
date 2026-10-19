# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_refresh_metadata_policy | A new submission supplies Refresh Metadata | Refresh metadata on every schedule: ALWAYS; Refresh metadata when needed: IF_NEEDED; Never refresh metadata: NEVER; explicit blank or null: empty string | Match one exact UI label or case-insensitive internal code; treat explicit blank/null as empty, but treat omitted input as the IF_NEEDED default | submit.argument1 STRING value | Reject unsupported or ambiguous nonblank input before preview |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| RDJ.STATUS_LOOKUP | read_request_dispatch_status | User requests status for an existing Process ID | requestId | /ess/rest/scheduler/v1/requests/{requestId} | id, description, jobDefinitionId, application, product, requestParameters, state, phase, cause, completionTime, elapsedTime, ecid, errorWarningDetail | Exact positive requestId in the selected environment | requestId, returned job identity, last-known or terminal state, cause, timing, ECID, diagnostics | Stop with input_validation, auth_or_authorization, transport_or_environment, or Fusion_API; never submit a replacement |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Existing request found | Return the current state for the same requestId and stop without submitting. |
| Request not found or access denied | Preserve the target and requestId, classify the failure, and stop. |
| Status is nonterminal | Return the last-known state and a safe same-request resume path. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.STATUS_LOOKUP | decision | 20 | reference_lookup | found->RDJ.STATUS_DONE;not_found_or_failed->RDJ.ERROR | RDJ.VALIDATE | stop | Read status for an explicitly supplied existing requestId. |
