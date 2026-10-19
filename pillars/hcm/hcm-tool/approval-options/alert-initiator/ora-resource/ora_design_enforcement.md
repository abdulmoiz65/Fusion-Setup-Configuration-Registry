# Design Enforcement

## Oracle Documentation Sources

| Source | Documented guidance |
|---|---|
| [Alert Initiator on Error — Actions for Managing Transactions](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/actions-for-managing-transactions.html) | Alert Initiator on Error notifies the transaction submitter when the transaction ends in error. |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate approval process | Require a nonblank approval_process. |
| 2 | Resolve approval process | Confirm one exact Process Name match from the Approval Options REST `findByProcessName` finder. |
| 3 | Scope option configuration | Apply approval options only to the resolved approval process. |
| 4 | Configure alert audience | Retain the initiator as the default recipient and add non-initiators only as explicit recipient_list entries. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every approval-options request | Error | find_approval_process_by_name | approval_process is missing, absent from the finder response, or ambiguous | Provide the exact Process Name to `findByProcessName`. | Yes |
| Additional alert recipient request | Error |  | A request names interested parties or non-initiators without explicit recipient identities | Provide the identities to configure in recipient_list, or retain the initiator-only default. | Yes |
| Alert Initiator on Error is enabled | Warning |  | None | Confirm that the transaction submitter should receive an alert when the transaction ends in error. | Yes |
| Alert Initiator mutation | Error |  | The executor does not use the configured Data Loader business object alertInitiatorOnError | Route the mutation through the configured alertInitiatorOnError Data Loader business object; do not substitute a direct REST route or another business object. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_approval_process_by_name | Before configuring Alert Initiator | Canonical Process Name and one-result confirmation | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.ENFORCE_SCOPE | decision | 3 | design_enforcement | allowed->ALERT_RECIPIENT.ENFORCE_AUDIENCE;blocked->APPROVAL_PROCESS.NOT_FOUND | APPROVAL_PROCESS.FIND_BY_PROCESS_NAME | stop | Exact approval process lookup completed |
| ALERT_RECIPIENT.ENFORCE_AUDIENCE | decision | 4 | design_enforcement | initiator_only->APPROVAL_PROCESS.DONE;explicit_recipients->APPROVAL_PROCESS.DONE;missing_recipients->ALERT_RECIPIENT.MISSING | APPROVAL_PROCESS.ENFORCE_SCOPE | stop | Exact approval process lookup completed |
