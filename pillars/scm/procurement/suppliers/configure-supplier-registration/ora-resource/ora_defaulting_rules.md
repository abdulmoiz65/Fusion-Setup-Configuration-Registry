# Configure Supplier Registration Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Autocreate site assignments for spend authorized suppliers | Enabled | The setting is explicitly in scope, no explicit value or Preserve decision is supplied, and the user requests the documented default | No |  |

Oracle documents that site assignments for new supplier sites are automatically created after approval or promotion to spend authorized. Deselecting this option requires manual site-assignment creation.

Never override a supplied Yes/No value or Preserve decision. Omit out-of-scope
settings and blank FSM export cells defined as Preserve. An unanswered in-scope
question is not permission to default; collect only that missing decision.
Show any requested default in the existing preview, without adding an approval
gate separate from Core Data Loader's workflow.

## Golden Scenarios

These are synthetic review cases, not approved execution payloads.

| Scenario | Supplied Decision | Expected Result |
|---|---|---|
| Explicit automatic handling | Yes | Keep Enabled; do not override |
| Explicit manual handling | No | Keep Disabled; do not override |
| Preserve existing setting | Preserve | Omit the attribute; keep the current value |
| Unrelated partial update | Site-assignment setting outside scope | Omit the attribute |
| Blank FSM export cell | Blank EnableAutoCreateSiteAssign | Preserve; omit the attribute |
| Missing in-scope answer | No decision supplied | Ask only for the missing decision; do not default |
| Requested default | In-scope setting; user requests its documented default | Use Enabled and disclose it in the preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SR.APPLY_DEFAULTS | step | 20 | apply_default | applied->POZ.SR.READ_SHARED_SUPPLIER_OPTIONS;blocked->POZ.SR.HANDLE_ERROR | POZ.SR.VALIDATE_INPUT | stop | After input validation |
