# Design Enforcement

## Source Material

- Developer-supplied exported Word document: HCM Config Task UI screenshots and REST calls for BPM based flows.
- [How You Define Approvals for Human Capital Management](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-define-approvals-for-human-capital-management.html#Managing-Approval-Transactions)
- [Define When to Send Workflow Notifications](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/define-when-to-send-workflow-notifications.html#Set-Up-Notification-Scenarios)
- [Aggregate Tasks to Minimize the Number of Notifications to Send](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/aggregate-tasks-to-minimize-the-number-of-notifications-to-send.html#Set-Up-Notification-Scenarios)
- [Show Approve and Reject Options in Notifications](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/show-approve-and-reject-options-in-notifications.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve the approval process | Use the process finder and require one exact Process Name result. |
| 2 | Read the current task configuration | Use the documented readTaskConfiguration action with the resolved processId. |
| 3 | Review the documented defaults | Identify which HCM family defaults will remain and which will be changed. |
| 4 | Apply task-design controls | Confirm the requested notification, aggregation, and participant-action settings meet the documented configuration rules. |
| 5 | Gate registered write adapter | Prepare an immutable preview for the registered businessProcessApprovalRulesTasks writeTaskConfiguration adapter with the resolved processId, complete Json, commitNeededFlag, target environment, and expected effect; obtain explicit approval immediately before dispatch. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Approval policies are configured for HCM tasks | Error | find_approval_process_by_name | The request attempts to use a task configuration without one exact approval-process result. | Use Manage Approval Transactions for Human Capital Management where applicable; BPM Worklist remains necessary for changes to rules created in Advanced Mode. | Yes |
| Notification scenarios are changed | Error |  | The requested task status, recipient, or channel outcome is not explicit. | Define the status and recipient before configuring the Notifications subtab; include reminder settings when reminders are requested. | Yes |
| Task aggregation is changed | Error |  | The aggregation choice is not explicit. | Select None, Once per task, or Once per stage according to the required notification behavior. | Yes |
| Approve or reject actions must appear in notifications | Error |  | Signature Policy is not No Signature Required, either approval pre-condition is not Optional, or Perform update outcome only from task form is selected. | Configure all documented conditions before committing the task. | Yes |
| Registered task-configuration write is requested | Error | read_task_configuration | Current task configuration was not read for the exact resolved processId before changes are prepared. | Start from the readTaskConfiguration result and preserve the complete reviewed configuration in Json. | Yes |
| writeTaskConfiguration mutation is requested | Error |  | The preview does not identify POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRulesTasks/action/writeTaskConfiguration, processId, complete Json, commitNeededFlag, target environment, expected response, and side effects; or fresh explicit approval is absent. | Use the registered businessProcessApprovalRulesTasks Data Loader business object through core.data-loader.task-rest and its approved task REST workflow. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_approval_process_by_name | Before every task-configuration read, preview, or write | One exact Process Name and processId | ora_reference_lookups.md |
| read_task_configuration | Before preparing a changed configuration | Current task configuration result for the resolved processId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TASK_CONFIG.ENFORCE_DESIGN | decision | 6 | design_enforcement | passed->TASK_CONFIG.PREVIEW_APPROVAL_REQUIRED;blocked->TASK_CONFIG.MISSING_INPUT | TASK_CONFIG.APPLY_DOCUMENTED_DEFAULTS | stop | A configuration request passed input validation and current configuration read |
