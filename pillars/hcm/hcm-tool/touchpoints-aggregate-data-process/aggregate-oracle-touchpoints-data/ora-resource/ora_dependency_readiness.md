# Aggregate Oracle Touchpoints Data Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Catalog task identity | Match CUSTOM_AGGREGATE_ORACLE_TOUCHPOINTS_DATA under CUSTOM_TOUCHPOINTS_AGGREGATE_DATA_PROCESS and CUSTOM_HCM_TOOL |
| 2 | Active project Run Book | Require runbook_control.status to be active in the selected project workspace |
| 3 | Fusion environment identity | Resolve the configured target environment without exposing credentials or token-cache contents |
| 4 | Durable output path | Resolve a unique execution-result path inside the active project workspace |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| catalog_identity | Effective catalog task | Yes | Every invocation | Satisfied only on an exact hierarchy match | knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json | | Prevents a display name or FSM task code from becoming an ESS job definition | Correct the catalog mapping before continuing when it does not match | task_code, functional_area_code, offering_code |
| active_runbook | Active implementation Run Book | Yes | Every new submission | Satisfied only when status is active | project/{project_id}/state/project-state.json | | Binds the mutation and durable evidence to the governed implementation workflow | Activate or repair the project Run Book before submission | project_id, runbook_status |
| target_environment | Configured Fusion environment | Yes | Every Fusion operation | Verify | core/auth/fusionEnv.properties through the selected core workflow | | Prevents submission to an unintended environment | Review the resolved environment in the immutable preview | environment |
| audit_destination | Unique project execution artifact | Yes | Every new submission | Verify | Declared project workspace output | | Preserves the request ID and terminal or last status for later recovery | Correct an unsafe or unwritable output path before submission | output_path |
| implementation_readiness | Parent workflow handoff | Conditional | Full or daily scheduling within implementation scope | Blocked until current parent readiness and synchronized task bindings are supplied | Parent implementation workflow state and evaluator result | | Prevents bypassing implementation configuration gates through the ESS task | Resume the parent workflow; cross-task orchestration remains there | project_id, environment, configuration_revision, readiness_confirmation, evidence_refs |
| successful_full_handoff | Verified Full result | Yes | Daily Incremental scheduling | Blocked until same-context Full success evidence is supplied | Parent workflow handoff from core ESS result and approved Full payload | | Submission or manual task completion cannot unlock scheduling | Resume the parent workflow to reconcile the existing Full request; never resubmit automatically | request_id, job_definition_id, run_type, cause, completed_at, verification_reference |

Selected-task scope requires its selected bindings and the owning operation's
preflight only. Daily-only requests still require successful_full_handoff;
they do not create an implementation readiness row or unrelated setup tasks.

Fusion enforces ESS authorization when the approved request is submitted or
monitored. Do not add a separate submit-privilege dependency, evidence field,
role/UI permission probe, or recent-request lookup before submission. A lookup
result cannot establish submission rights. Actual 401/403 responses follow the
owning error-handling contract without automatically repeating a POST.

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every mandatory dependency is confirmed | Continue to defaults and design enforcement |
| Verify | Environment or output destination still needs confirmation | Read-only verification only; no submission |
| Blocked | Catalog identity, active Run Book, environment, or safe output is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPA.RESOLVE_DEPENDENCIES | decision | 20 | resolve_dependency | ready->TPA.APPLY_DEFAULTS;blocked->TPA.ERROR_HANDLER | TPA.VALIDATE_INPUT | stop | Input validation succeeded |
