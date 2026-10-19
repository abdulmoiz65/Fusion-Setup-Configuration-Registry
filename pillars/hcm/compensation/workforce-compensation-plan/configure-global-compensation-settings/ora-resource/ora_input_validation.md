# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Existing global-settings identity | None; the signed-in user context determines the business-group row | Stop | Use the current signed-in user context; do not ask for or resolve BusinessGroupId in this skill | Every request | find_current_user_compensation_global_settings |
| REST-metadata-valid update values | One or more update fields accepted by the registered business object's REST metadata | Stop | Obtain current REST metadata and provide only fields and values it validates | An update is requested | read_compensation_global_settings_rest_metadata |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| REST metadata has not identified every supplied update field's contract | Blocked | Stop before import preparation or mutation | read_compensation_global_settings_rest_metadata |
| The request is a create request | Continue to the current-user existing-row lookup | Allow creation only when no row is returned; otherwise convert the request to an update | find_current_user_compensation_global_settings |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| REST metadata validation | Accept a supplied update field only when current registered-business-object REST metadata identifies it and validates its type, length, requiredness, and allowed values | Before preparing an update | read_compensation_global_settings_rest_metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CGI.VALIDATE_INPUT | step | 20 | validate_input | valid->CGI.FIND_EXISTING_ROW;invalid->CGI.HANDLE_ISSUE | CGI.READ_REST_METADATA | stop | Before a global-settings update or attempted create |
