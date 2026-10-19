# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| approval_process is missing or blank | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. Stop before configuring approval options. |
| findByProcessName returns no exact Process Name or resolves to more than one result | Return APPROVAL_PROCESS_NOT_FOUND: The specified approval process isn't returned by the Approval Options REST finder. Stop before configuring approval options. |
| regular and asynchronous bypass are both enabled, or the requested mode leaves the other option enabled | Return BYPASS_OPTION_CONFLICT: Regular Bypass Approvals and Asynchronous Bypass Approvals are mutually exclusive. Disable one before enabling the other. Stop before configuring approval options. |
| Data Loader reports success or that a bypass mutation was initiated | Perform an exact read check through findByProcessName for the selected Process Name and compare ApprovalDisabledFlag and AsyncBypassEnabledFlag with the approved requested values before reporting that the change took effect. |
| The post-Data-Loader read check does not match the approved bypass values | Treat the load as ineffective. With explicit approval that covers the fallback, send one direct POST to /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions/action/bypassApprovalsCases using the identical approved payload and headers Content-Type: application/vnd.oracle.adf.action+json and REST-Framework-Version: 9; then repeat the exact read check. Do not alter the payload or retry the direct action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval process is missing, absent, or ambiguous | Do not configure an option, guess a process, use a similar Process Name, or create an approval process. |
| Bypass mode is conflicting or unspecified | Do not enable regular and asynchronous bypass approvals together or infer the requested bypass mode. |
| Configured Data Loader business object is unavailable or does not match bypassApprovalsCases | Do not substitute another business object. Stop and report the routing gap. |
| A direct fallback has not been explicitly approved for the exact approved payload | Do not call the direct REST action. Report the read-check mismatch and request approval for the one fallback action. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.MISSING | step | 5 | error_handler | disclosed->RETURN_ISSUES | none | stop | approval_process is missing or blank |
| APPROVAL_PROCESS.NOT_FOUND | step | 6 | error_handler | disclosed->RETURN_ISSUES | none | stop | Exact Process Name lookup has no single result |
| BYPASS_OPTION.CONFLICT | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | stop | Regular and asynchronous bypass options conflict |
| APPROVAL_PROCESS.DONE | terminal | 8 | terminal | none | BYPASS_OPTION.ENFORCE_EXCLUSIVITY | stop | Approval process and bypass mode gates passed |
| RETURN_ISSUES | terminal | 9 | terminal | none | none | stop | Error disclosure complete |
