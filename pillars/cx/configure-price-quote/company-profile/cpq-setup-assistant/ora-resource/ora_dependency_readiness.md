# Dependency Readiness

## Readiness and Execution

The Task Nodes below evaluate readiness for an approval preview. They may return
`ready` with the current stage's approval pending; this never authorizes a write.
Approval dependencies apply at execution, after the exact preview is presented.
Do not require an approval record, reviewed binding, actor or nonce before their
creation in the guard lifecycle. Prior-stage completion and reconciliation are
readiness prerequisites, not substitutes for current-stage approval.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | CPQ deployment lookup | Make the unauthenticated deployment-version request. A `404` stops setup with the documented not-deployed message; any other HTTP response permits initialization flow. |
| 2 | Pre-initialization status lookup | Read the CPQ Setup Assistant status once. A completed, processing, error, or indeterminate state stops the configuration workflow. |
| 3 | Initialization approval | Only when the pre-initialization status is `SETUP_NOT_DONE`, prepare the immutable initialization archive, complete Task Hook validation and the guard preview, then obtain one explicit approval to initialize CPQ once. |
| 4 | Assistant identity | Initialize CPQ, then resolve the assistant record and child-resource identities through the documented read request. |
| 5 | Change approval | For each later stage, complete discovery/reconciliation, immutable preparation and Task Hook validation; build and present the exact guard preview, then obtain approval before execution. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CPQ_PREINITIALIZATION_STATUS | One read-only CPQ Setup Assistant status result | Yes | Configuration workflow after deployment validation | Lookup | Read-only Setup Assistant status | resolve_cpq_preinitialization_status | Prevents unnecessary initialization | Stop on completed, processing, error, or indeterminate status; proceed only on `SETUP_NOT_DONE` | Pre-initialization status result |
| CPQ_INITIALIZATION_APPROVAL | Separate approval to initialize CPQ | Yes | Initialization execution after preview | Pending | User confirmation | | Prevents an unapproved initialization | Present the initialization effect and request approval | Initialization approval record |
| CPQ_ASSISTANT_STATE | Unambiguous assistant and child records | Yes | Before company profile update, user creation, or submission | Lookup | Read-only setup-assistant response | resolve_cpq_setup_assistant_record | Child IDs must be discovered, not guessed | Resolve the assistant record before any child mutation | Assistant and child-record identities |
| CPQ_APPROVAL | Exact change approval | Yes | Stage execution after preview | Pending | User confirmation | | Prevents an unapproved configuration change | Present the redacted change summary and request approval | Approval record |

## Dependency Classification

| Result Category | When Used | Allowed Action |
|---|---|---|
| Blocked | Required access, input, state, artifact or reconciliation evidence is invalid or missing | Stop the affected preparation or execution step |
| Pending Approval | Readiness passes but current-stage approval is absent | Complete read-only validation and preview; request approval only after the exact preview is ready; no mutation |
| Ready | All applicable preapproval prerequisites pass | Build the approval preview; execution still requires current guard approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPQ.INITIALIZATION_READINESS | decision | 7 | resolve_dependency | ready->CPQ.INITIALIZATION_BINDING_READINESS;blocked->CPQ.RETURN_ISSUES | CPQ.PREINITIALIZATION_STATUS_LOOKUP | stop | Confirm the selected environment, the `SETUP_NOT_DONE` pre-initialization state and validated immutable initialization artifact. Current-stage approval remains pending and does not block preview readiness. Do not check role assignments or authorize execution. |
| CPQ.CONFIGURATION_READINESS | decision | 8 | resolve_dependency | ready->CPQ.CONFIGURATION_BINDING_READINESS;blocked->CPQ.RETURN_ISSUES | CPQ.CONFIGURATION_DISCOVERY_LOOKUP | stop | Confirm the selected environment, current authenticated discovery evidence, state-applicable proposal, validated immutable artifact and required prior-stage completion/reconciliation. Current-stage approval remains pending and does not block preview readiness. Do not check role assignments or authorize execution. |
