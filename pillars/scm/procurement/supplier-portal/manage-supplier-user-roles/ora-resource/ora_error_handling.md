# Manage Supplier User Roles Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required change-package information is absent or invalid | Stop and return the missing or invalid information; do not prepare a Data Loader artifact. |
| The Data Loader artifact does not identify the requested role | Stop and request an explicit Role Name or Role Code in the artifact. |
| An initial default cannot be determined for an empty configuration | Stop and require explicit assignment-policy values. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing input | The Role Name or Role Code required for CREATE, UPDATE/PATCH, or DELETE, intended configuration, or Data Loader artifact is absent. | Supply the missing information and restart validation. |
| Role validation failure | The requested role is absent from the Data Loader artifact. | Supply the Role Name or Role Code and restart validation. |
| Initial-default failure | An empty configuration cannot resolve a documented default and has no explicit policy value. | Supply explicit policy values and restart validation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before Data Loader processing | The explicit role identity, assignment-policy flags when applicable, and approval for the Data Loader artifact. |
| On a validation stop | The failed validation and required next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Supplier user role configuration change | Do not process configuration outside the Data Loader workflow. |
| Validation failure or initial-default failure | Do not submit or retry a Data Loader configuration update until the issue is resolved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SUR.DATALOADER_GATE | step | 50 | execution_gate | ready->POZ.SUR.RETURN_READY;blocked->POZ.SUR.RETURN_ISSUES;failure->POZ.SUR.RETURN_ISSUES | POZ.SUR.ENFORCE_ROLE_POLICY | stop | The approved supplier user role configuration is ready for Data Loader REST processing. |
| POZ.SUR.RETURN_READY | terminal | 60 | terminal | none | POZ.SUR.DATALOADER_GATE | stop | The approved configuration is ready for Data Loader REST processing. |
| POZ.SUR.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Input validation or policy enforcement cannot proceed. |
