# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_approval_process_by_name | approval_process passed input validation | approval_process unchanged and URL encoded only for transport | GET /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions?finder=findByProcessName;Name={url_encoded_approval_process} | Name, ProcessId, ApprovalDisabledFlag, AlertEnabledFlag, ArchivePeriod | findByProcessName must return exactly one nonblank Name equal to approval_process; do not use partial, case-normalized, or similar-name matching. | Canonical Process Name, ProcessId, Bypass Approvals setting from ApprovalDisabledFlag, Alert Initiator On Error setting from AlertEnabledFlag, and Archive Period setting from ArchivePeriod | Return APPROVAL_PROCESS_NOT_FOUND when the finder returns zero or more than one result. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| findByProcessName returns one exact Process Name | Continue to the approval-process scope gate. |
| Finder returns no result or more than one result | Stop and return APPROVAL_PROCESS_NOT_FOUND. Do not choose a similar process. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.FIND_BY_PROCESS_NAME | decision | 2 | reference_lookup | found->APPROVAL_PROCESS.ENFORCE_SCOPE;not_found->APPROVAL_PROCESS.NOT_FOUND;ambiguous->APPROVAL_PROCESS.NOT_FOUND | APPROVAL_PROCESS.VALIDATE_INPUT | stop | approval_process is present |
