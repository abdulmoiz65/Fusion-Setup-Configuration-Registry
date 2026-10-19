# Resource Type Preparation ESS Error Handling

Use this task-local guidance with the enclosing task `SKILL.md`. It applies to
preview, approved ESS submission, and read-only status tracking. It does not
authorize an ESS submission or a retry.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Payload is malformed, missing a required schedule field, or uses an invalid recurrence | Stop before any Fusion call, identify the invalid field, and require a corrected payload preview. |
| Task code, CrmEss application, or job definition is missing or ambiguous | Stop before invoking the submitter and report a catalog or metadata mismatch. |
| Authentication is expired or invalid | Delegate one cached-token refresh attempt to the core ESS submitter; do not expose token material. |
| Authorization or required ESS privilege is missing | Stop and request the required role or privilege; do not retry the submission. |
| Read-only transport or environment check fails | Record the target environment and bounded diagnostic; retry only a read-only check when the enclosing task permits it. |
| ESS submission outcome is failed or indeterminate | Preserve redacted diagnostics and any request ID, then stop. A new submission requires fresh explicit approval. |
| Polling reaches its configured timeout | Preserve the request ID, last status, elapsed wait, and read-only next-check path; do not submit again. |
| A terminal ESS process failure is returned | Preserve the redacted status or process diagnostic and present the recommended recovery action. |
| Project artifact path is unsafe or unwritable | Stop before the Fusion call and report artifact persistence failure. |
| Live submission has no current approval for its exact payload and target | Stop at the approval gate. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required payload fields, timestamps, timezone, recurrence, or polling options are invalid | Correct the input and regenerate the preview. |
| catalog_or_metadata_mismatch | Task identity, application, or job definition cannot be confirmed | Resolve the exact contract before any submitter invocation. |
| auth_expired_or_invalid | Cached authentication is unavailable or rejected | Let the core submitter perform its one permitted refresh attempt. |
| authorization_or_privilege | Refresh is rejected or the account lacks ESS access | Obtain the necessary environment privilege and rerun preflight. |
| transport_or_environment | DNS, VPN, connection, or environment availability prevents a read-only check | Record the environment and use only a bounded read-only retry. |
| fusion_api_error | Fusion returns an API failure | Persist a redacted response summary, external identifiers, and recovery recommendation. |
| process_timeout | Polling ends before a terminal status | Resume with a read-only request-ID status check. |
| process_failed | Fusion returns a terminal unsuccessful status | Retrieve available status or process diagnostics and stop. |
| artifact_persistence | Required project artifact cannot be safely written | Repair the project path before any Fusion call. |
| approval_blocker | A live submission lacks immediate approval | Present the immutable payload and target, then wait for approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview before live submission | Exact target environment, immutable redacted payload, schedule, polling options, and approval requirement. |
| Submission or status failure | Failure classification, redacted diagnostic summary, request ID or ECID when returned, artifact reference, and recommended next action. |
| Polling timeout | Target environment, job definition, request ID, last status, elapsed wait, and read-only next-check path. |
| Authentication failure | Authentication classification and recovery action without tokens, secrets, token-cache contents, or authorization headers. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Catalog identity is ambiguous | Do not guess an application, job definition, or task match. |
| Payload has changed after preview | Do not reuse prior approval; regenerate and approve the immutable payload. |
| A live submission fails or is indeterminate | Do not resubmit without fresh explicit approval. |
| Polling times out | Do not continue polling indefinitely or create another request. |
| Diagnostics contain sensitive material | Do not print or persist credentials, tokens, private keys, full authorization headers, or token-cache contents. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FFS.RTP.ERROR_CLASSIFY | step | 1 | error_handler | classified->FFS.RTP.ERROR_DISCLOSE | none | stop | A preview, submission, polling, or artifact-persistence error occurs. |
| FFS.RTP.ERROR_DISCLOSE | step | 2 | error_handler | disclosed->FFS.RTP.ERROR_STOP | FFS.RTP.ERROR_CLASSIFY | stop | An error classification has been recorded. |
| FFS.RTP.ERROR_STOP | terminal | 3 | terminal | none | FFS.RTP.ERROR_DISCLOSE | stop | The classified error and safe next action have been disclosed. |
