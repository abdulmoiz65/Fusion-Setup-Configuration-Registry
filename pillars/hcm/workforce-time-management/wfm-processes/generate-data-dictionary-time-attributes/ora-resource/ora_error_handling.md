# Approval and error handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| LDG scope is not selected | Do not show a preview. Ask whether to apply to all LDGs or a specific LDG. |
| Approval is absent, refused, or stale | Do not submit. Return the current preview and request a new explicit approval when appropriate. |
| ESS request times out | Preserve the request ID, last known status, elapsed wait, and target environment. Resume tracking that ID only; do not resubmit. |
| ESS reports terminal failure | Return the terminal Scheduler outcome and redacted diagnostics. Do not resubmit automatically. |
| Submission response is uncertain | Preserve available diagnostic evidence and do not create a replacement request automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | A required input is missing or Include Payroll Time Type is invalid | Correct the input and generate a new preview. |
| transport or environment | The target environment or read-only LOV request cannot be confirmed | Stop and correct the environment before preview. |
| approval blocker | Exact preview approval is missing, refused, or stale | Do not submit. |
| process timeout | Shared ESS tracking reaches its timeout | Resume tracking the preserved request ID. |
| process failed | ESS returns terminal unsuccessful status | Return redacted diagnostics without resubmission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Pre-submission approval | Target environment, job definition, application, product, immediate schedule, resolved arguments, and redacted request payload |
| Submission and monitoring result | Request ID, current or terminal status, and redacted diagnostics |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Timeout, failure, or uncertain submission result | Do not automatically submit another ESS request. |
| Status check after a request exists | Do not submit a new request; track the preserved request ID through core.fusion-api.ess-job-submitter. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TDL.DDTA.APPROVAL_GATE | decision | 50 | execution_gate | approved->TDL.DDTA.ESS_HANDOFF_READY;not-approved->RETURN_ISSUES | TDL.DDTA.ESS_PREVIEW | stop | Immediately before first live ESS submission |
| TDL.DDTA.ESS_HANDOFF_READY | terminal | 60 | terminal | none | TDL.DDTA.APPROVAL_GATE | stop | The approved request is ready for core.fusion-api.ess-job-submitter |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Any validation, lookup, preview, approval, timeout, failure, or uncertain-response issue |
