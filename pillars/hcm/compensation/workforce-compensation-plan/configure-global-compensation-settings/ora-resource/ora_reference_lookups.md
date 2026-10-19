# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_compensation_global_settings_rest_metadata | Before validating any supplied global-settings field | Business Object: compensationGlobalSettings | /hcmRestApi/resources/latest/compensationGlobalSettings/describe | REST describe metadata for writable fields, required fields, field types, lengths, enumerations, and key fields | REST metadata must identify every supplied field and validate its shape; do not infer a field contract | Validated field contract | Metadata unavailable or incomplete: stop as a REST metadata validation gap; do not prepare an import or mutation |
| find_current_user_compensation_global_settings | A request addresses or creates global settings | None; the signed-in user's business-group context selects the row | /hcmRestApi/resources/latest/compensationGlobalSettings | Global-settings row identity and returned row count | A plain GET on the business object returns the row for the signed-in user's business group. Exactly one row is the update target. Zero means a create is eligible through compensationGlobalSettings. More than one is an integrity error. | Existing row count and create or update identity | Zero: permit create through compensationGlobalSettings after metadata validation and explicit approval. Many: stop as an integrity gap. GET failure: stop and report the read failure. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| User asks to create a global-settings row | Run find_current_user_compensation_global_settings before the create path. |
| Existing row is found | Do not create another row; permit only an update of the existing row after REST metadata validation and the task's normal approval gate. |
| No row is found | Permit creation through compensationGlobalSettings after REST metadata validation and the task's normal approval gate. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CGI.READ_REST_METADATA | step | 10 | reference_lookup | metadata_ready->CGI.VALIDATE_INPUT;metadata_gap->CGI.HANDLE_ISSUE | none | stop | Before validating supplied global-settings values |
| CGI.FIND_EXISTING_ROW | decision | 30 | reference_lookup | one_existing->CGI.ENFORCE_CREATE_OR_UPDATE;none_existing->CGI.ENFORCE_CREATE_OR_UPDATE;many_existing->CGI.HANDLE_ISSUE;read_failed->CGI.HANDLE_ISSUE | CGI.VALIDATE_INPUT | stop | A global-settings request runs in the signed-in user's business-group context |
