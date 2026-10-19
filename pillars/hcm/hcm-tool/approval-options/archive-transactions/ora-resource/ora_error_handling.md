# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| approval_process is missing or blank | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. Stop before configuring approval options. |
| findByProcessName returns no exact Process Name or resolves to more than one result | Return APPROVAL_PROCESS_NOT_FOUND: The specified approval process isn't returned by the Approval Options REST finder. Stop before configuring approval options. |
| Data Loader reports success or that an archive-period mutation was initiated | Perform an exact read check through findByProcessName for the selected Process Name and compare ArchivePeriod with the approved requested value before reporting that the change took effect. |
| The post-Data-Loader read check does not match the approved archive period | Treat the load as ineffective. With explicit approval that covers the fallback, send one direct POST to /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions/action/archiveTransactions using the identical approved payload and headers Content-Type: application/vnd.oracle.adf.action+json and REST-Framework-Version: 9; then repeat the exact read check. Do not alter the payload or retry the direct action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval process is missing, absent, or ambiguous | Do not configure an option, guess a process, use a similar Process Name, or create an approval process. |
| Configured Data Loader business object is unavailable or does not match archiveTransactions | Do not substitute another business object. Stop and report the routing gap. |
| A direct fallback has not been explicitly approved for the exact approved payload | Do not call the direct REST action. Report the read-check mismatch and request approval for the one fallback action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.MISSING | step | 4 | error_handler | disclosed->RETURN_ISSUES | none | stop | approval_process is missing or blank |
| APPROVAL_PROCESS.NOT_FOUND | step | 5 | error_handler | disclosed->RETURN_ISSUES | none | stop | Exact Process Name lookup has no single result |
| APPROVAL_PROCESS.DONE | terminal | 6 | terminal | none | APPROVAL_PROCESS.ENFORCE_SCOPE | stop | Approval process scope gate passed |
| RETURN_ISSUES | terminal | 7 | terminal | none | none | stop | Error disclosure complete |
