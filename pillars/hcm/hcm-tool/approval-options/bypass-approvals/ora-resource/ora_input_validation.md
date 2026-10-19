# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Approval process | approval_process | Return APPROVAL_PROCESS_REQUIRED: Specify an approval process name. | Supply the exact Process Name, then rerun validation. | Every request |  |
| Bypass mode | bypass_mode: regular, asynchronous, or disabled | Return BYPASS_OPTION_CONFLICT: Specify one bypass mode only. Regular and asynchronous bypass approvals can't both be enabled. | Supply one supported bypass_mode. | Every request |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| approval_process is present and nonblank | Continue to the `findByProcessName` REST lookup. | Every request | find_approval_process_by_name |
| bypass_mode is regular, asynchronous, or disabled | Continue to the mutual-exclusivity gate. | Every request |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPROVAL_PROCESS.VALIDATE_INPUT | decision | 1 | validate_input | valid->APPROVAL_PROCESS.FIND_BY_PROCESS_NAME;missing_process->APPROVAL_PROCESS.MISSING;invalid_bypass_mode->BYPASS_OPTION.CONFLICT | none | stop | Every request |
