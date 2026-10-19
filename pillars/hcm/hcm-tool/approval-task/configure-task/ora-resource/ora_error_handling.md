# Error Handling

## Source Material

- Developer-supplied exported Word document: HCM Config Task UI screenshots and REST calls for BPM based flows.
- [How You Define Approvals for Human Capital Management](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-define-approvals-for-human-capital-management.html#Managing-Approval-Transactions)

## Error Situations

| Situation | What Should Happen |
|---|---|
| Approval process or requested configuration scope is missing | Return APPROVAL_PROCESS_REQUIRED or CONFIGURATION_SCOPE_REQUIRED and stop before configuration. |
| The approval-process finder returns no exact result or multiple results | Return APPROVAL_PROCESS_NOT_FOUND or APPROVAL_PROCESS_AMBIGUOUS and stop; never choose a similar process. |
| readTaskConfiguration does not return the current configuration for the resolved processId | Persist redacted read diagnostics and stop before preparing Json. |
| A requested setting changes a documented HCM default without a stated intended outcome | Return CONFIGURATION_SCOPE_REQUIRED and request the intended business outcome. |
| A write request lacks a current immutable preview or explicit approval | Return APPROVAL_REQUIRED and stop before the registered businessProcessApprovalRulesTasks writeTaskConfiguration adapter. |
| A writeTaskConfiguration call fails or its result cannot be verified | Classify the failure, persist redacted diagnostics, and do not retry without idempotency or new explicit approval. |
| A task rule created in BPM Worklist Advanced Mode is changed through the simplified UI | Stop and use BPM Worklist for the change. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Required task identity or requested setting is missing. | Obtain the missing configuration detail. |
| approval blocker | A write preview or fresh explicit approval is absent. | Obtain approval bound to the exact preview before dispatch. |
| Fusion API | The documented finder, read action, or write action fails or returns an unusable result. | Preserve redacted diagnostics and stop. |
| process failed | The requested UI cannot modify an Advanced Mode rule. | Continue the rule change in BPM Worklist. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval process is not exact | Do not choose a similar process name or use an unconfirmed processId. |
| Write action fails or is uncertain | Do not replay writeTaskConfiguration without documented idempotency or new explicit approval. |
| A configuration request is incomplete | Do not choose notification recipients, aggregation behavior, or participant actions by inference. |
| Internal source content is inaccessible | Do not represent the internal source as verified or derive implementation details from its title. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TASK_CONFIG.MISSING_INPUT | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required approval process or configuration scope is missing |
| TASK_CONFIG.APPROVAL_PROCESS_NOT_FOUND | step | 8 | error_handler | disclosed->RETURN_ISSUES | none | stop | Approval-process finder returned no exact result |
| TASK_CONFIG.APPROVAL_PROCESS_AMBIGUOUS | step | 9 | error_handler | disclosed->RETURN_ISSUES | none | stop | Approval-process finder returned multiple results |
| TASK_CONFIG.READ_CONFIGURATION_FAILED | step | 10 | error_handler | disclosed->RETURN_ISSUES | none | stop | readTaskConfiguration did not return a usable result |
| TASK_CONFIG.PREVIEW_APPROVAL_REQUIRED | terminal | 11 | terminal | none | TASK_CONFIG.ENFORCE_DESIGN | stop | Preview and explicit approval are required before the separately routed write action |
| RETURN_ISSUES | terminal | 12 | terminal | none | none | stop | Error disclosure complete |
