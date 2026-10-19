# Dependency Readiness

Preserve the direct shared-export route, Data Loader-authorized import route,
and separate target deployment verification after import. These checks do not
deploy a flexfield.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact environment and task | Resolve one configured environment and the fixed trading community organization DFF task identity |
| 2 | Operation-specific authorization | For export, approve the exact task-level preview; for import, approve Core Data Loader's exact immutable preview and Task Hook validation envelope |
| 3 | Shared FSM adapter | Use only the operation-matched shared task-level exporter or importer |
| 4 | Target deployment verification | After successful import, verify target deployment status and functional behavior before claiming complete migration |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TCODFF.ENV | Exact Fusion environment | Yes | Live export, import, or status | Satisfied | One configured environment selected by the runbook |  | Prevent cross-environment execution | Select one named source or target | Environment identity and role |
| TCODFF.EXPORT_APPROVAL | Task-level export authorization | Yes | Live export | Blocked until approved | Exact export preview for the selected environment and fixed task |  | Bind the environment, task, whole-task scope, output path, adapter, and options before one export submission | Approve the task-level export preview; no deployment evidence or pre-existing ZIP/hash is required | Approved export values |
| TCODFF.DATA_LOADER | Immutable Data Loader authorization | Yes | Live import | Blocked until approved | Core Data Loader import preview and Task Hook validation envelope |  | Bind the exact ZIP, environment, task, and validation result before import execution | Complete Core Data Loader validation and approve its immutable import preview; do not select an adapter or endpoint locally | Approved import artifact, validation envelope, and fingerprint |
| TCODFF.TARGET_DEPLOYMENT | Target deployment and functional verification | Yes | After terminally successful import | Verify | Current target task evidence and functional test result |  | Import success does not prove deployment or UI availability | Check target status and test the trading community organization DFF; perform manual sandbox deployment/publication when required | Target status, test result, evidence, next action |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact environment and all operation-specific prerequisites are present | Continue only to the declared preview or status step |
| Verify | Target deployment or functional evidence must be supplied after import | Manual/read-only verification only; no replacement submission |
| Blocked until approved | Required export preview approval or immutable import approval has not been released | No live POST |
| Blocked | A mandatory dependency is missing, stale, ambiguous, or ineligible | Stop and report the required correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCODFF.DEPENDENCY_READINESS | decision | 3 | resolve_dependency | satisfied->TCODFF.DESIGN_GATE;blocked->TCODFF.ERROR | TCODFF.VALIDATE_OPERATION | stop | Before operation-specific preview or status continuation |
