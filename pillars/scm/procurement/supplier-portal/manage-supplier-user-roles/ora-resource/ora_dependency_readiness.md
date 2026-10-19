# Manage Supplier User Roles Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplier role identity | Include the supplied Role Name or Role Code in the Data Loader artifact for CREATE, UPDATE/PATCH, or DELETE. |
| 2 | Setup-data artifact | Prepare the supplier user role configuration in the approved Data Loader artifact. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| supplier_role_identity | Supplier role identity | Conditional | A CREATE, UPDATE/PATCH, or DELETE request is prepared | Verify | Approved Data Loader artifact |  | The selected role must be explicitly identified by the prepared change. | Supply a Role Name or Role Code in the Data Loader artifact. | Role Name or Role Code |
| approved_dataloader_artifact | Approved Data Loader artifact | Yes | A supplier user role configuration change is requested | Verify | Approved implementation artifact |  | Supplier user role updates are processed only through Data Loader. | Prepare and approve the Data Loader artifact before processing. | Approved artifact reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The selected role is identified in the Data Loader artifact and the artifact is approved. | No external lookup; proceed to Data Loader validation. |
| Missing dependency | A Role Name or Role Code, or an approved Data Loader artifact, is absent. | Supply the missing value before Data Loader processing. |
| Invalid dependency | The change artifact is malformed or does not identify a role. | Stop before Data Loader processing. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SUR.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->POZ.SUR.APPLY_ROLE_DEFAULTS;missing->POZ.SUR.RETURN_ISSUES;invalid->POZ.SUR.RETURN_ISSUES;failure->POZ.SUR.RETURN_ISSUES | POZ.SUR.VALIDATE_CHANGE_PACKAGE | stop | A supplier user role configuration change is requested. |
