# Reference Lookups

## Source Material

- Developer-supplied exported Word document: HCM Config Task UI screenshots and REST calls for BPM based flows.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_approval_process_by_name | approval_process passed input validation | approval_process unchanged and URL encoded only for transport | GET /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions?finder=findByProcessName;Name={url_encoded_approval_process}&fields=Name,ArchivePeriod,AiCommentConfiguration,PurgePeriod,ProcessId,ApprovalDisabledFlag,AsyncBypassEnabledFlag,AiCommentEnabledFlag,AlertEnabledFlag,SendToUsersFlag,BypassSupportedFlag,AsyncBypassSupportedFlag,ApprovalOverrideSupportedFlag,ApprovalDisabledValue,IsParallelTransactionSupported,IsAICommentsSupported,RuleFileName,IsTaskConfigSupported,IsParallelTransactionEnabled,isOverallParallelTransactionEnabled | Name and ProcessId plus projected approval-options fields | Require exactly one returned Process Name equal to approval_process; do not use partial or similar-name matching. | ProcessId and current approval-options attributes | Return APPROVAL_PROCESS_NOT_FOUND for no result. Return APPROVAL_PROCESS_AMBIGUOUS for multiple results and request an exact selection. |
| read_task_configuration | One exact processId is resolved | processId from find_approval_process_by_name | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalRulesTasks/action/readTaskConfiguration with Content-Type application/vnd.oracle.adf.action+json | processId request field and result | Submit only the resolved processId. | Current task configuration result; retain its complete configuration only in the approved write-preview flow | Return READ_TASK_CONFIGURATION_FAILED when the result is unavailable or unusable. |
| get_approval_users | Approval-user mappings are needed for task configuration review | processId from find_approval_process_by_name | POST /hcmRestApi/resources/11.13.18.05/businessProcessApprovalBuilderRules/action/getApprovalUsers with Content-Type application/vnd.oracle.adf.action+json | processId request field and result | Submit only the resolved processId. | Approval-user mapping results | Stop and report the unavailable lookup result; do not infer user mappings. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The approval-process finder returns one exact result | Continue with its processId. |
| The configuration read returns a result for the resolved processId | Use it as the basis for reviewing the complete configuration. |
| Approval-user mappings are required | Perform get_approval_users only after the exact processId is resolved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| TASK_CONFIG.FIND_APPROVAL_PROCESS | decision | 2 | reference_lookup | found->TASK_CONFIG.READ_CONFIGURATION;not_found->TASK_CONFIG.APPROVAL_PROCESS_NOT_FOUND;ambiguous->TASK_CONFIG.APPROVAL_PROCESS_AMBIGUOUS | TASK_CONFIG.VALIDATE_INPUT | stop | approval_process is present | find_approval_process_by_name |
| TASK_CONFIG.READ_CONFIGURATION | decision | 3 | reference_lookup | read->TASK_CONFIG.GET_APPROVAL_USERS;read_failed->TASK_CONFIG.READ_CONFIGURATION_FAILED | TASK_CONFIG.FIND_APPROVAL_PROCESS | stop | One exact approval process is resolved | read_task_configuration |
| TASK_CONFIG.GET_APPROVAL_USERS | step | 4 | reference_lookup | mapped->TASK_CONFIG.APPLY_DOCUMENTED_DEFAULTS;not_required->TASK_CONFIG.APPLY_DOCUMENTED_DEFAULTS;lookup_failed->TASK_CONFIG.READ_CONFIGURATION_FAILED | TASK_CONFIG.READ_CONFIGURATION | stop | Approval-user mapping review is requested | get_approval_users |
