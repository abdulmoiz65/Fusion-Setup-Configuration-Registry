# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| track_existing_ess_request | Resume with supplied requestId; execution polling uses the saved returned ID | Configured TargetEnvironment, restBaseUrl, requestId | /ess/rest/scheduler/v1/requests/{requestId} through core.fusion-api.ess-job-submitter | requestId, jobDefinitionId, state, processPhase, cause, completedTime, elapsedTime, ecid, errorWarningMessage | Read only the exact request; when returned, requestId must match and jobDefinitionId must equal JobDefinition://oracle/apps/ess/projects/foundation/setup/system/OrgDenormJob | ExistingRequestId, ExistingState, ExistingStatus, ExistingErrors, TargetEnvironment, RequestProvenance | Stop on missing/inaccessible result, mismatched identity or REST failure; preserve request ID and diagnostics, never submit a replacement |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_maintain_project_organizations_scope | Before execution | Selected project, exact task identity and configured target | Require selected project and exact task code; environment and restBaseUrl must be configured | VerifiedProjectId, VerifiedTaskCode, VerifiedTargetEnvironment | Block missing or conflicting target; framework owns sequencing decisions |
| verify_ess_execution | Before execution and before polling | Distinct output path, acceptance companion and returned request ID | Both paths must be unused; persist and read back the accepted receipt before any polling | EssReceiptPath, AcceptanceReceiptPath, ReceiptRequestId | Stop on persistence failure; preserve any known ID and never resubmit |
| verify_ess_approval | Before submission | Explicit approval receipt and displayed fixed payload | approved=true, operation=submit, exact configured environment/restBaseUrl and canonical JSON payload_sha256 match | ApprovalEvidence, ApprovedPayload, ApprovedPayloadSha256 | Block missing, declined or mismatched approval; request fresh approval for any changed target or payload |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| New submission has no request ID | No live prerequisite lookup; prepare fixed payload and approval |
| Existing request is supplied | Read-only tracking of that ID; retain target and status provenance |
| Status reports another request or job | Stop; preserve saved identity and diagnose mismatch |
| Polling fails or times out | Preserve last known result, saved ID and safe resume instructions |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.TRACK_EXISTING_REQUEST | step | 3 | reference_lookup | resolved->MPO.RESOLVE_DEPENDENCIES;not_required->MPO.RESOLVE_DEPENDENCIES;failure->MPO.RETURN_ISSUES | MPO.APPLY_DEFAULTS | stop | Resume when requestId is supplied; otherwise continue without a lookup |
