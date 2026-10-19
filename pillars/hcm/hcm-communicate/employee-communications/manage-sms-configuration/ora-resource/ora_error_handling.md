# Manage SMS Configuration Error Handling

This task-specific error scope reports Data Loader failures without retrying an uncertain import. Successful provider creation ends with an exact manual activation handoff in Manage SMS Configuration; the FSM import does not run or verify activation.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required provider field is missing or invalid | Stop import preparation, report the affected row and field, and return Configure SMS for Campaigns as setup guidance |
| A supplied CommProviderId does not match ProviderCode | Stop and require TWILIO with 1 or SYNIVERSE with 2; do not overwrite an explicit conflicting value |
| The Data Loader process fails | Report the process failure and available sanitized log reference, return Configure SMS for Campaigns, and do not retry automatically |
| The Data Loader process times out or has an uncertain outcome | Report the last status and identifiers, return Configure SMS for Campaigns, then stop before another import attempt |
| Provider creation succeeds and activation was requested | Output: Creation succeeded. Go to Manage SMS Configuration, open the created configuration, deactivate any currently active SMS configuration, activate the created configuration, and verify exactly one SMS configuration is active |
| More than one SMS configuration is active during the manual activation handoff | Do not leave the task in that state; deactivate configurations until exactly one SMS configuration is active |
| The created configuration cannot be activated | Keep provider creation reported as successful, report activation as incomplete, return Configure SMS for Campaigns, and require correction in Manage SMS Configuration; do not retry the import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required field, provider code, provider identifier, message length, or task scope value is invalid | Correct the affected row, return Configure SMS for Campaigns, and generate a new immutable preview |
| Process failed | The Data Loader import reaches a failed terminal status | Review the sanitized process log, return Configure SMS for Campaigns, and correct the documented cause before preparing a new import |
| Process timeout | Polling ends before a terminal process status is available | Report the last status, return Configure SMS for Campaigns, and use the declared status-check route before considering another attempt |
| Process uncertain | Submission or completion cannot be confirmed | Return Configure SMS for Campaigns and reconcile the existing process before any retry |
| Activation handoff incomplete | Provider creation succeeded but the created configuration was not activated or exactly one active configuration was not verified in the task | Return Configure SMS for Campaigns, complete the manual activation handoff in Manage SMS Configuration, and do not rerun provider creation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import | Exact target environment and the immutable ZIP identity required by the core Data Loader approval workflow |
| After failed or uncertain import | Process status, sanitized identifiers, available log reference, and one safe next action |
| After successful creation when activation was requested | Creation succeeded. Go to Manage SMS Configuration, open the created configuration, deactivate any currently active SMS configuration, activate the created configuration, and verify exactly one SMS configuration is active |
| Any failed, timed-out, uncertain, or incomplete activation result | Link Configure SMS for Campaigns and state that it is setup guidance, not evidence that the FSM import or activation completed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A provider identifier conflicts with ProviderCode | Do not overwrite the explicit value or prepare the row for import |
| A live import result is failed, timed out, or uncertain | Do not retry automatically |
| Another SMS configuration is active | Do not activate the created configuration until the currently active configuration is deactivated |
| More than one SMS configuration is active | Do not leave the task in that state; correct it until exactly one SMS configuration is active |
| Provider creation succeeds | Do not claim that active status was automatically set or verified from the supplied CSV |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SMS.EXECUTION_GATE | decision | 5 | execution_gate | approved->SMS.EVALUATE_RESULT;blocked->SMS.HANDLE_ERROR | SMS.ENFORCE_SINGLE_ACTIVE | stop | The core Data Loader workflow evaluates the exact target environment and immutable import artifact |
| SMS.HANDLE_ERROR | step | 7 | error_handler | disclosed->SMS.RETURN_ISSUES | none | stop | Input, dependency, provider-policy, approval, process-failure, timeout, or uncertain-result handling is required |
| SMS.RETURN_SUCCESS | terminal | 8 | terminal | none | SMS.EVALUATE_RESULT | stop | Provider creation succeeds; when activation was requested, return the exact Manage SMS Configuration activation handoff and exactly-one-active requirement |
| SMS.RETURN_ISSUES | terminal | 9 | terminal | none | SMS.HANDLE_ERROR | stop | A blocker or failed, timed-out, or uncertain import prevents successful completion |
