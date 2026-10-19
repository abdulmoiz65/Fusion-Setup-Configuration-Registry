# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| REST metadata is unavailable, incomplete, or does not validate a supplied field | Stop before import preparation or mutation and report the REST metadata validation gap. |
| GET for the signed-in user's business-group context fails | Stop and report the read failure; do not treat it as no existing row. |
| More than one global-settings row is returned for the signed-in user's business-group context | Stop and report an integrity gap; do not choose a row. |
| User requests a create operation when an existing row is found | Refuse the create operation and direct the user to update the existing row. |
| A permitted create or update reaches the handoff gate | Invoke core.data-loader with the validated task context and immutable source; Core owns preview, approval, and submission. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| REST metadata validation gap | Current metadata contract is unavailable or cannot validate the key or supplied field | Provide the exact registered-business-object metadata endpoint and retry validation only. |
| Existing-row read failure | GET cannot determine whether the signed-in user's business group has an existing row | Restore read access; do not create. |
| Global-settings integrity gap | More than one row is returned for the signed-in user's business-group context | Correct the duplicate data condition before an update. |
| Duplicate create | User asks to create a row when one already exists | Change the request to update the existing row. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Metadata validation blocker | Business object name, supplied fields, missing metadata contract, and safe next action; do not disclose credentials. |
| Existing-row lookup blocker | Signed-in user context, resolver name, match count when available, and safe next action. |
| Create decision | Signed-in user context, whether an existing row was found, and the resulting create or update path. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Existing row is found | Do not create another global-settings row. |
| No existing row is found | Do not create until REST metadata validation and explicit approval are complete. |
| REST metadata is missing or incomplete | Do not infer fields, validation rules, or a request shape. |
| GET failure or multiple matches | Do not update or create a row. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CGI.ROUTE | decision | 45 | execution_gate | update_ready->CGI.LOADER_READY_UPDATE;create_ready->CGI.LOADER_READY_CREATE;mutation_blocked->CGI.HANDLE_ISSUE | CGI.ENFORCE_CREATE_OR_UPDATE | stop | Select the permitted Core Data Loader handoff |
| CGI.HANDLE_ISSUE | step | 50 | error_handler | handled->CGI.RETURN_ISSUES | none | stop | Any metadata, read, integrity, or create-policy issue |
| CGI.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| CGI.LOADER_READY_UPDATE | terminal | 70 | terminal | none | CGI.ROUTE | continue | Existing-row update rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| CGI.LOADER_READY_CREATE | terminal | 80 | terminal | none | CGI.ROUTE | continue | Create rules passed with no existing row; invoke core.data-loader and follow it through immutable ZIP preview |
