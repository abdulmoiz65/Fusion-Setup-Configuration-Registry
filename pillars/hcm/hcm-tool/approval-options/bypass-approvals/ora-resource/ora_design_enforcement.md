# Design Enforcement

## Oracle Documentation Sources

| Source | Documented guidance |
|---|---|
| [Bypass Approvals — How You Manage HCM Approval Transactions](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-you-manage-hcm-approval-transactions.html) | Enabling Bypass Approvals commits the transaction on submission and does not route it for approval. |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate approval process | Require a nonblank approval_process. |
| 2 | Resolve approval process | Confirm one exact Process Name match from the Approval Options REST `findByProcessName` finder. |
| 3 | Scope option configuration | Apply approval options only to the resolved approval process. |
| 4 | Select bypass mode | Enable regular bypass, asynchronous bypass, or neither; never enable both. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every approval-options request | Error | find_approval_process_by_name | approval_process is missing, absent from the finder response, or ambiguous | Provide the exact Process Name to `findByProcessName`. | Yes |
| Bypass Approvals configuration | Error |  | regular Bypass Approvals and Asynchronous Bypass Approvals are both enabled, or the requested mode would leave the other option enabled | Select regular, asynchronous, or disabled. Disable the other bypass option before enabling the requested option. | Yes |
| Enabling Bypass Approvals | Warning |  | None | Confirm that immediate transaction commitment without approval routing is intended. | Yes |
| Bypass Approvals mutation | Error |  | The executor does not use the configured Data Loader business object bypassApprovalsCases | Route the mutation through the configured bypassApprovalsCases Data Loader business object; do not substitute a direct REST route or another business object. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_approval_process_by_name | Before configuring Bypass Approvals | Canonical Process Name and one-result confirmation | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.ENFORCE_SCOPE | decision | 3 | design_enforcement | allowed->BYPASS_OPTION.ENFORCE_EXCLUSIVITY;blocked->APPROVAL_PROCESS.NOT_FOUND | APPROVAL_PROCESS.FIND_BY_PROCESS_NAME | stop | Exact approval process lookup completed |
| BYPASS_OPTION.ENFORCE_EXCLUSIVITY | decision | 4 | design_enforcement | regular->APPROVAL_PROCESS.DONE;asynchronous->APPROVAL_PROCESS.DONE;disabled->APPROVAL_PROCESS.DONE;conflict->BYPASS_OPTION.CONFLICT | APPROVAL_PROCESS.ENFORCE_SCOPE | stop | Exact approval process lookup completed |
