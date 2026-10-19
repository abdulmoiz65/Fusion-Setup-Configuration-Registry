# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | common.security-console.manage-hcm-role-provisioning-rules | Accept the unchanged task identity, request scope, environments, and source artifact. |
| 2 | core.data-loader | Be selected only by the shared workflow for the final immutable import. |

## Delegation Boundary

The shared workflow owns export, archive validation, same-environment restore
confirmation, immutable approval preview, Data Loader import, monitoring, and
diagnostics. Stop if that workflow is unavailable or if a caller asks this
pillar task to substitute a direct export, REST, UCM, FSM, OAuth, or Data Loader
route.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HRPRFS.CHECK_SHARED_WORKFLOW | decision | 2 | resolve_dependency | satisfied->HRPRFS.ENFORCE_DELEGATION;blocked->HRPRFS.BLOCKED | HRPRFS.VALIDATE_DELEGATION | stop | After the pillar task inputs are valid and before a shared-workflow preview. |
