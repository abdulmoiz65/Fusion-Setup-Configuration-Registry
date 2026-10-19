# Design Enforcement

## Oracle Documentation Sources

| Source | Documented guidance |
|---|---|
| [Archive period — Configure Approval Transactions for Archiving](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/configure-approval-transactions-for-archiving.html) | Archive period options are 3 months, 6 months, 9 months, or Don't archive. The Archive Transaction Console Completed Transactions process archives completed transactions according to the selected period. |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate approval process | Require a nonblank approval_process. |
| 2 | Resolve approval process | Confirm one exact Process Name match from the Approval Options REST `findByProcessName` finder. |
| 3 | Scope option configuration | Apply approval options only to the resolved approval process. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every approval-options request | Error | find_approval_process_by_name | approval_process is missing, absent from the finder response, or ambiguous | Provide the exact Process Name to `findByProcessName`. | Yes |
| Archive-period configuration | Warning |  | None | Select a documented archive period that aligns with the organization's retention policy and the Archive Transaction Console Completed Transactions process. | Yes |
| Archive Transactions mutation | Error |  | The executor does not use the configured Data Loader business object archiveTransactions | Route the mutation through the configured archiveTransactions Data Loader business object; do not substitute a direct REST route or another business object. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_approval_process_by_name | Before configuring Archive Transactions | Canonical Process Name and one-result confirmation | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.ENFORCE_SCOPE | decision | 3 | design_enforcement | allowed->APPROVAL_PROCESS.DONE;blocked->APPROVAL_PROCESS.NOT_FOUND | APPROVAL_PROCESS.FIND_BY_PROCESS_NAME | stop | Exact approval process lookup completed |
