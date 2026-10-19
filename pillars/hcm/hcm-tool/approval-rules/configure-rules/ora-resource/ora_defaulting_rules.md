# Approval Rules Defaulting Rules

Apply these defaults only when the user explicitly chooses the corresponding participant type and has not supplied an override.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Management hierarchy action type | Approval required | A management hierarchy rule is added and no action is selected | Yes | |
| Conditional rule priority | High | A new rule is created with a primitive or payload-attribute condition and no priority is selected | Yes | |
| Always-valid rule priority | Medium | A new default always-valid rule, including a Self Auto Approve rule, is created and no priority is selected | Yes | |
| Management hierarchy route using | Line Manager | A management hierarchy rule is added and no manager type is selected | Yes | |
| Management hierarchy approval chain of | Task.payload.transactionApprovalRequest.Requestor | A management hierarchy rule is added and no approval-chain value is selected | Yes | |
| Management hierarchy user approver | Task.payload.transactionApprovalRequest.Requestor | A management hierarchy rule is added and no user-approver value is selected | Yes | |
| Management hierarchy up to approver | Task.payload.transactionApprovalRequest.Requestor | A management hierarchy rule is added and no up-to-approver value is selected | Yes | |
| Management hierarchy user tree | Task.payload.transactionApprovalRequest.Requestor | A management hierarchy rule is added and no user-tree value is selected | Yes | |
| Management hierarchy start with for Employee | User | A management hierarchy rule starts with Employee | Yes | |
| Management hierarchy start with for Manager | Requestor's Manager | A management hierarchy rule starts with Manager | Yes | |
| Management hierarchy start with for Second level Manager | Second level Manager | A management hierarchy rule starts with Second level Manager | Yes | |
| Management hierarchy number of levels | 1 | A management hierarchy rule is added and no level count is selected | Yes | |
| Job-based line manager approval chain of | Task.payload.transactionApprovalRequest.Requestor | A JobListBuilder participant is added and no chain subject is selected | Yes | |
| Job-based line manager up to approver | Task.payload.transactionApprovalRequest.Requestor | A JobListBuilder participant is added and no upper-bound subject is selected | Yes | |
| Job-based line manager user tree | Task.payload.transactionApprovalRequest.Requestor | A JobListBuilder participant is added and no user tree is selected | Yes | |
| Job-based line manager top approver | Manager | A JobListBuilder participant is added and no top approver is selected | Yes | |
| Position hierarchy action type | Approval required | A position hierarchy rule is added and no action is selected | Yes | |
| Position hierarchy include | All Approvers | A position hierarchy rule is added and no inclusion option is selected | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_RULES.APPLY_DEFAULTS | step | 3 | apply_default | reviewed->APPROVAL_RULES.ENFORCE_DESIGN | APPROVAL_RULES.RESOLVE_PROCESS | stop | A hierarchy participant type is selected without an explicit override |

## Sources

- [Management Hierarchy Approval Rule Attributes](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/management-hierarchy-approval-rule-attributes.html)
- [Position Hierarchy Approval Rule Attributes](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/position-hierarchy-approval-rule-attributes.html)
