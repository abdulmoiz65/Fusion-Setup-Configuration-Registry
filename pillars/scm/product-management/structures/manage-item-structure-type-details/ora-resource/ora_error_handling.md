# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required structure-name or parent-control details are missing or invalid | Stop before validation and identify the missing identity, effective-date handling, validation setting, selected range character, or an attachment category only when one is supplied or required by the target. |
| The requested range indicator code or meaning is not enabled and effective in ORA_EGP_COMP_REF_DES_RANGE_IND | Stop before validation and request an enabled, effective lookup value. |
| The request would delete, repurpose, or deactivate the seeded parent structure type | Refuse the request. Keep the parent active and add or maintain a child structure name for the business need. |
| A new structure name is created through the UI without an effective start date | Stop the UI runbook and request the date. |
| A new structure name has no documented effective-date representation in the current FSM template | Continue the FSM import without an effective-start-date value in the archive. Do not invent a CSV field, request a UI date, or assume a default date. |
| An FSM archive has a child structure-name row but no matching EGP_STRUCTURE_TYPE parent row | Stop before import and rebuild the archive with the exact matching parent row from the same fresh export. Use the same StructureTypeId; do not generate a parent identifier. |
| The FSM process log says a child row was skipped because its parent row is missing | Treat the import as unsuccessful even if the Data Loader dataset says completed or succeeded. Preserve the diagnostic, obtain a fresh export, rebuild the archive with the matching parent row, and require a new approval before retrying. |
| An attachment category differs only by case from a category in the populated export | Use the exported canonical CategoryName and do not add a duplicate attachment row. |
| No attachment category is supplied and the target does not require one | Continue without an attachment-category row; do not treat the omission as an input-validation error. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | The requested structure-name or parent-control details, or range-indicator lookup value, fail a validation rule | Correct the request and validate it again |
| process failed | The FSM process log reports that a child row was skipped because the parent row is missing | Record the process log evidence, rebuild the source archive with the matching exported parent row, validate again, and obtain approval for the changed archive |
| design enforcement | The request conflicts with retained parent structure type or assigned-name protection policy | Keep the parent unchanged; do not delete or repurpose the assigned structure name |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The requested structure name is already assigned to items | Do not delete or repurpose the structure name |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| STRUCTURE_DETAILS.INVALID_REQUEST | terminal | 50 | terminal | none | none | stop | The requested structure type details fail validation |
| STRUCTURE_DETAILS.DESIGN_BLOCKED | terminal | 60 | terminal | none | none | stop | The request violates structure type design policy |
| STRUCTURE_DETAILS.DONE | terminal | 80 | terminal | none | STRUCTURE_DETAILS.ENFORCE_DESIGN | stop | The request is validated and compliant for handoff to the next authorized implementation step |
