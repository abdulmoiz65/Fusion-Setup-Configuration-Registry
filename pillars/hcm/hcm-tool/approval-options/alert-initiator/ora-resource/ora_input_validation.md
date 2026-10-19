# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Approval process | approval_process | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. | Supply the exact Process Name, then rerun validation. | Every request |  |
| Additional alert recipients | additional_alert_recipients, when non-initiators or interested parties are requested | Return ALERT_RECIPIENT_REQUIRED: Provide the explicit recipient identities to configure in recipient_list. | Supply one or more recipient identities, or omit the request to alert additional parties. | Additional recipients requested |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| approval_process is present and nonblank | Continue to the `findByProcessName` REST lookup. | Every request | find_approval_process_by_name |
| additional_alert_recipients is omitted or contains explicit recipient identities | Continue to alert-audience enforcement. | Every request |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.VALIDATE_INPUT | decision | 1 | validate_input | valid->APPROVAL_PROCESS.FIND_BY_PROCESS_NAME;missing_process->APPROVAL_PROCESS.MISSING;missing_recipients->ALERT_RECIPIENT.MISSING | none | stop | Every request |
