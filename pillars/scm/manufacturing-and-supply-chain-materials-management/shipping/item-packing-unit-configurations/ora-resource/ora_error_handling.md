# Item Packing Unit Configurations Error Handling

Source: approved Default-field contract and current Data Loader architecture.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Default has an unsupported value | Stop before Data Loader handoff and request one of the approved Default values. Do not coerce an unsupported value. |
| A populated FSM PreferredFlag is not Y or N | Stop before FSM import and request Y, N, or a blank value that is preserved from the source export. |
| An FSM source changes the exported header names or order | Stop before FSM import and rebuild the source from the current task export. Preserve ContainerItemNumber, MaxLoadQuantity, PreferredFlag, DFF, JobDefinition, and ObjectVersionNumber columns as the FSM template defines them. |
| Central Data Loader metadata preflight fails | Stop before Data Loader handoff and follow the central Data Loader diagnostic. Do not use direct REST execution. |
| Data Loader rejects a backend-owned attribute | Preserve the server diagnostic, correct the source against fresh current metadata, and restart validation and preview. Do not create a local Item, Packing Unit, Organization, Maximum Quantity, RestAction, audit, ID, or DFF rule by guesswork. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Default validation failure | The supplied Default value and the approved values. |
| FSM PreferredFlag validation failure | The supplied PreferredFlag value and the permitted FSM values Y, N, or blank. |
| FSM template failure | The affected header or column order and the requirement to rebuild from the current task export. |
| Central Data Loader preflight failure | The central diagnostic and a next action without credentials or raw authorization data. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Default has an unsupported value | Do not infer a Boolean value, use a similar value, or pass the value to Data Loader. |
| An FSM PreferredFlag is blank | Do not replace it with the REST/Data Loader true default. |
| An FSM source changes the export contract | Do not rename ContainerItemNumber, MaxLoadQuantity, PreferredFlag, DFF, JobDefinition, or ObjectVersionNumber columns to REST/Data Loader field names. |
| Central Data Loader preflight fails | Do not upload, initiate, retry, or substitute direct REST execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IPUC.HANDLE_ISSUE | step | 30 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior Default validation or defaulting step is invalid or failed |
| IPUC.DONE | terminal | 40 | terminal | none | IPUC.APPLY_DEFAULT | stop | All documented task-local rules have passed |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Error disclosure is complete |
