# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| approval_process is missing or blank | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. Stop before configuring approval options. |
| findByProcessName returns no exact Process Name or resolves to more than one result | Return APPROVAL_PROCESS_NOT_FOUND: The specified approval process isn't returned by the Approval Options REST finder. Stop before configuring approval options. |
| Additional or interested parties are requested without explicit recipient identities | Return ALERT_RECIPIENT_REQUIRED: Provide each additional recipient for the alert template recipient_list, or retain the initiator-only default. Stop before configuring approval options. |
| Data Loader reports success or that an alert mutation was initiated | Perform an exact read check through findByProcessName for the selected Process Name and compare AlertEnabledFlag with the approved requested value before reporting that the change took effect. |
| The post-Data-Loader read check does not match the approved alert value | Treat the load as ineffective. With explicit approval that covers the fallback, send one direct POST to /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions/action/alertInitiatorOnError using the identical approved payload and headers Content-Type: application/vnd.oracle.adf.action+json and REST-Framework-Version: 9; then repeat the exact read check. Do not alter the payload or retry the direct action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval process is missing, absent, or ambiguous | Do not configure an option, guess a process, use a similar Process Name, or create an approval process. |
| Additional alert recipients are undefined | Do not infer interested parties, reuse an unrelated recipient list, or add recipients without explicit identities. |
| Configured Data Loader business object is unavailable or does not match alertInitiatorOnError | Do not substitute another business object. Stop and report the routing gap. |
| A direct fallback has not been explicitly approved for the exact approved payload | Do not call the direct REST action. Report the read-check mismatch and request approval for the one fallback action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.MISSING | step | 5 | error_handler | disclosed->RETURN_ISSUES | none | stop | approval_process is missing or blank |
| APPROVAL_PROCESS.NOT_FOUND | step | 6 | error_handler | disclosed->RETURN_ISSUES | none | stop | Exact Process Name lookup has no single result |
| ALERT_RECIPIENT.MISSING | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | stop | Additional alert recipients were requested but not identified |
| APPROVAL_PROCESS.DONE | terminal | 8 | terminal | none | ALERT_RECIPIENT.ENFORCE_AUDIENCE | stop | Approval process and alert audience gates passed |
| RETURN_ISSUES | terminal | 9 | terminal | none | none | stop | Error disclosure complete |
