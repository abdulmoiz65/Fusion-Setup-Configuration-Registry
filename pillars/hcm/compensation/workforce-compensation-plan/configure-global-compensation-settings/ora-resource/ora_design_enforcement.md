# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate with REST metadata | Verify the key and every supplied update value against the registered business object's current REST metadata. |
| 2 | Read existing global settings | GET the business object in the signed-in user's business-group context before any create request or update preparation. |
| 3 | Enforce create-or-update model | Permit an update only when exactly one existing row is found. Permit a create through compensationGlobalSettings only when GET returns no rows. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A request asks to create a global-settings entry | Blocker | find_current_user_compensation_global_settings | An existing row is found for the signed-in user's business group | Do not create a duplicate; change the request to update the existing row | Yes |
| A request asks to create a global-settings entry | Permitted | find_current_user_compensation_global_settings | No existing row is found | Create one row through compensationGlobalSettings after REST metadata validation and explicit approval | Yes |
| An update is requested | Blocker | find_current_user_compensation_global_settings | Zero or more than one matching row, or unavailable GET contract | Stop until exactly one existing row and a usable GET contract are available | Yes |
| Any global-settings field is supplied | Blocker | read_compensation_global_settings_rest_metadata | REST metadata does not validate the key or a supplied field | Stop and obtain current REST metadata; do not infer field rules | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_compensation_global_settings_rest_metadata | Before every update validation | Supplied field contract | ora_reference_lookups.md |
| find_current_user_compensation_global_settings | Before every create attempt or update | Existing row count and update identity | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CGI.ENFORCE_CREATE_OR_UPDATE | decision | 40 | design_enforcement | update_allowed->CGI.ROUTE;create_allowed->CGI.ROUTE;blocked->CGI.HANDLE_ISSUE | CGI.FIND_EXISTING_ROW | stop | After existing global-settings rows are read |
