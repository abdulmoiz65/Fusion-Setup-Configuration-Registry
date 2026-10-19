# Manage Supplier User Roles Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate role configuration | Confirm that the prepared Data Loader artifact explicitly identifies the selected role and includes required assignment-policy flags for added or maintained roles. |
| 2 | Apply initial defaults | Apply documented defaults only when the configuration is empty and the user has not supplied an explicit value. |
| 3 | Approve Data Loader artifact | Continue only with the approved Data Loader artifact. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A CREATE, UPDATE/PATCH, or DELETE request is prepared | Blocking |  | The Data Loader artifact does not identify the selected role. | Correct the role identity in the Data Loader artifact. | Yes |
| An initial empty configuration has no explicit policy value | Blocking |  | A default cannot be determined from the documented initial default set. | Supply explicit policy values or correct the initial-default condition. | Yes |
| A supplier user role configuration change is requested | Blocking |  | The requested change is not represented by an approved Data Loader artifact. | Prepare and approve the Data Loader artifact before processing. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SUR.ENFORCE_ROLE_POLICY | step | 40 | design_enforcement | compliant->POZ.SUR.DATALOADER_GATE;blocked->POZ.SUR.RETURN_ISSUES;failure->POZ.SUR.RETURN_ISSUES | POZ.SUR.APPLY_ROLE_DEFAULTS | stop | A supplier user role configuration change is prepared for Data Loader REST processing. |
