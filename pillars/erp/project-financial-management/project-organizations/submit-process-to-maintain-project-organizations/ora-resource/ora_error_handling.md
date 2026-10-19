# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Invalid payload or supplied request parameters | Input validation failure; stop before authentication or POST |
| Approval absent, declined or mismatched | Approval blocker; show exact target and payload for explicit approval |
| Authentication or authorization fails | Stop without refreshed-token submission replay; preserve ID if known |
| POST fails or returns no positive request ID | Record uncertain submission; never automatically replay; reconcile through active workflow |
| Acceptance receipt cannot be saved or verified | Artifact persistence failure; stop before GET; retain known ID in failure output |
| Final result cannot be saved | Preserve independent acceptance receipt; resume its ID with a fresh output path |
| Polling fails | Preserve saved ID and redacted Fusion API or transport diagnostics; no POST |
| Polling times out | Report ID, last status and elapsed wait; resume same ID, never resubmit |
| Terminal unsuccessful | Report same ID, state, phase, cause, ECID and errors; stop without replay |
| Returned request/job identity differs | Stop and preserve original ID; investigate through read-only tracking |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Invalid execution inputs or fixed payload | Correct input before preview |
| Approval blocker | Missing or mismatched approval | Obtain exact explicit approval |
| Auth/authz | Credentials or privileges rejected | Renew through selected core workflow; resume known ID |
| Transport/environment or Fusion API | POST or status request fails | Preserve diagnostics and reconcile; no automatic replay |
| Process timeout | Nonterminal after wait budget | Resume saved ID |
| Process failed | Terminal unsuccessful | Investigate preserved result |
| Artifact persistence | Receipt write/read-back fails | Preserve known ID; repair persistence before resume |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Submission approval | Configured environment/restBaseUrl, exact three-field payload and canonical payload_sha256 |
| Acceptance | Request ID, fixed job identity, target and persisted receipt path; acceptance is not completion |
| Tracking | Same request ID, state, phase, cause, completion time, elapsed wait, ECID and errors |
| Failure or timeout | Saved ID when known, sanitized diagnostics and safe resume/reconciliation action; no automatic replay |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| User parameters or alternate job supplied | Do not forward them |
| Approval missing or stale | Do not submit |
| Existing request supplied | Do not submit another request |
| Failure, timeout or uncertainty | Do not automatically replay |
| Submission accepted | Do not claim terminal completion |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.EXECUTION_GATE | decision | 6 | execution_gate | ready_to_submit->MPO.RETURN_READY_TO_SUBMIT;ready_to_resume->MPO.RETURN_READY_TO_RESUME;not_ready->MPO.RETURN_ISSUES;declined->MPO.RETURN_REFUSAL | MPO.ENFORCE_DESIGN | stop | Return a validated action or block mutation |
| MPO.RETURN_READY_TO_SUBMIT | terminal | 7 | terminal | none | MPO.EXECUTION_GATE | continue | The fixed OrgDenormJob payload and exact target are explicitly approved |
| MPO.RETURN_READY_TO_RESUME | terminal | 8 | terminal | none | MPO.EXECUTION_GATE | continue | Existing request is validated for read-only status tracking |
| MPO.RETURN_ISSUES | terminal | 9 | terminal | none | none | continue | A correctable input, dependency, lookup, or runtime issue blocks progress |
| MPO.RETURN_REFUSAL | terminal | 10 | terminal | none | none | continue | Unsupported route, concurrency conflict, or declined approval blocks progress |
