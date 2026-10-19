# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task execution context | Select project, configured target and ESS scheduling/monitoring privilege |
| 2 | Durable receipt | Allocate unused task-local output paths |
| 3 | Execution mode | Resume supplied request ID or prepare fixed payload |
| 4 | Approval | For submission, show exact target and payload and obtain explicit approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MPO.SCOPE | Task and target context | Yes | Every request | Verify | Selected project and target properties | verify_maintain_project_organizations_scope | Bind execution to configured target | Select project and target with ESS privileges | VerifiedProjectId, VerifiedTaskCode, VerifiedTargetEnvironment |
| MPO.RECEIPT | Durable request receipt | Yes | Every request | Verify | Output and acceptance companion | verify_ess_execution | Save ID before polling | Allocate unused task-local paths | EssReceiptPath, AcceptanceReceiptPath |
| MPO.REQUEST | Supplied ESS identity | Conditional | Resume | Lookup | Supplied requestId and Scheduler status | track_existing_ess_request | Resume without another POST | Supply the saved request ID | ExistingRequestId, ExistingStatus |
| MPO.APPROVAL | Exact submission approval | Yes | Submit | Verify | Explicit approval record | verify_ess_approval | Bind one mutation to target and fixed payload | Approve displayed target and complete payload | ApprovalEvidence, ApprovedPayloadSha256 |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Execution context, receipts and explicit approval verified | One approved OrgDenormJob submission |
| Resume existing | Supplied positive request ID | Read-only monitoring only |
| Missing | Target, receipt, privilege or approval absent | No submission |
| Conflict | Supplied request or target identity conflicts | Stop and reconcile |

The framework owns task sequencing. Invocation on demand prepares the same fixed job without inspecting other setup tasks.

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.RESOLVE_DEPENDENCIES | step | 4 | resolve_dependency | ready->MPO.ENFORCE_DESIGN;resume->MPO.ENFORCE_DESIGN;missing->MPO.RETURN_ISSUES;conflict->MPO.RETURN_REFUSAL | MPO.TRACK_EXISTING_REQUEST | stop | Before preview, submission, or resumed polling |
