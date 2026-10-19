# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or unsupported StatusType | Show the fixed numbered StatusType catalog and stop until the user selects by status name or selection number (`1` through `5`) |
| New status has an invalid or duplicate identity after export review | Stop before ZIP preparation. For whitespace in a supplied or derived Internal Name, show: `Internal Name cannot contain spaces. Provide an Internal Name without spaces.` For an existing Internal Name or Status Name, show the matching exported row and direct the user to update it or choose a distinct identity. |
| Delete request | Stop and report that Delete is not supported for Manage Change Statuses. Do not prepare or import an artifact. |
| Update target missing or ambiguous | Stop; do not create a status or select a matching row |
| Existing Status-only selector matches multiple rows | Show all matched Internal Names, Statuses, and Status Types, then stop for explicit approval of the full bulk scope. Do not prepare or import the update before that approval. |
| Update asks to change Internal Name, Active, or Status Code | Stop and report that the field is not supported for update. Existing Internal Name is allowed only as the selector. |
| End Date update has no target-template carrier | Stop and report that the current FSM template has no End Date carrier; do not invent a CSV column. |
| Update row omits StatusName or StatusType | Stop and rebuild from the current export with StatusName, StatusType, and ObjectName retained unchanged; FSM rejects a partial row without those mandatory carriers. |
| Fusion rejects one or more Change Status rows | Show one `Change Status import results` table containing every submitted status after Fusion returns its result. Use columns Status, Requested Change, Result, Reason / Backend Error, and a final marker. Mark a Fusion-rejected row `❌`; mark a row with no Fusion row error `✅`, even when the overall batch rolled back, and state `Not applied — batch rolled back` in Result. Use the imported row identifier for Status; state only the reason supplied by Fusion, and do not invent a more specific rule. After the table, say: `The import was unsuccessful because of the errors shown above. Please correct the rows with errors and upload all the data again.` |
| FSM import failure or uncertain result | Preserve safe process evidence; reconcile before another write |
| Changed artifact after preview | Restart validation and approval for the changed bytes |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Exact task, passed path, missing fields, evidence, blockers, and safe resume step |
| Approval | Exact environment, status name, internal code, type, purpose, and validated artifact |
| Backend row failures | Show every submitted status in one consolidated table. Start with `Status Name`, `Internal Name`, `Status Type`, and `Description`; then add `Result`, `Reason / Backend Error`, and the final marker. Use `❌` for a Fusion-rejected row and `✅` for a row with no Fusion row error; make rollback versus applied outcome explicit in the Result column. |
| Secrets | Never disclose OAuth tokens, secrets, or protected runtime material |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Failed validation | Do not present approval or upload the archive |
| Missing standalone import approval | Do not upload or initiate; a successful rule plan is not approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A reached validation rule returns a missing, invalid, or conflicting outcome |
| MCS.RETURN_SUCCESS | terminal | 100 | terminal | none | MCS.DESIGN | stop | All pre-preview task rules pass; return validation evidence to Data Loader without authorizing import |
