# Manage Supplier User Roles Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplier user role for create | Role Name or Role Code | Stop preparation | Include the explicit role identity in the Data Loader artifact. | A CREATE request is prepared |  |
| Existing supplier user role for update or delete | Role Name or Role Code | Stop preparation | Include the explicit role identity in the Data Loader artifact. | An UPDATE/PATCH or DELETE request is prepared |  |
| Role assignment policy | Allow supplier provision flag, default for Supplier Portal flag, and default for Sourcing flag | Stop preparation | Supply an explicit value for each role assignment policy flag in the Data Loader artifact. | A supplier user role is added or maintained |  |
| Data Loader route | Data Loader artifact for the selected setup task | Stop preparation | Use the approved Data Loader workflow. | A supplier user role configuration change is requested |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Assignment-policy flags | Require explicit true or false values for Allow supplier provision, Default for Supplier Portal, and Default for Sourcing. | A supplier user role is added or maintained |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SUR.VALIDATE_CHANGE_PACKAGE | step | 10 | validate_input | valid->POZ.SUR.CHECK_DEPENDENCIES;missing->POZ.SUR.RETURN_ISSUES;invalid->POZ.SUR.RETURN_ISSUES | none | stop | A supplier user role configuration change is requested |
