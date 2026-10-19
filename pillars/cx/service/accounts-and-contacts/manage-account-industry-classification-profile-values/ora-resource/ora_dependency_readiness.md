# Dependency Readiness

Preserve the shared whole-task FSM export route, Core Data Loader-owned import route, and explicit target-state verification for changed profile values.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact target and task | Resolve one configured target environment and the fixed task identity |
| 2 | Target profile state | Verify the persisted task-owned profile-value row with a fresh task export; read the effective value only when MOT_INDUSTRY_CLASS_CATEGORY is REST exposed |
| 3 | Immutable authorization | Consume the unchanged Core Data Loader contract to build a Task Hook-validated preview and obtain approval for its exact ZIP and impact |
| 4 | FSM execution and verification | Let Core Data Loader submit once, then reconcile the returned ProcessId and ProcessLog without resubmission |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| AICP.ENV | Exact Fusion target | Yes | Live export, import, update, or status | Satisfied | One configured target environment selected by the runbook |  | Bind the live operation to the intended target | Select one named target; do not add task-local package-origin or release policy | Target environment identity and role |
| AICP.TARGET_PROFILE_STATE | Current task-owned profile-value row and effective value when REST exposed | Yes | Import with changed profile-value rows, view, or update | Verify | Fresh task export and read-only Apps Common Profile Values response when REST exposed | read_industry_classification_profile_value | Prevent stale revision imports and unsupported level/value changes | Show each current-to-proposed value before preview; do not infer a configured value from an absent effective-value response | ProfileOptionName, level, persisted value, and effective value when available |
| AICP.DATA_LOADER | Immutable Data Loader authorization | Yes | Live import | Blocked until approved | Core Data Loader import preview and Task Hook validation envelope |  | Bind the exact ZIP, environment, task, and validated impact before import | Complete validation and approve the exact immutable preview; do not select an adapter or endpoint locally | Approved import artifact, validation envelope, and fingerprint |
| AICP.PROCESS_RECONCILIATION | Accepted process or failed submission evidence | Yes | After import submission attempt | Verify | Returned ProcessId, status, and ProcessLog when available |  | Avoid duplicate imports after an uncertain or failed attempt | Poll or retrieve the existing process; never submit another archive automatically | ProcessId, last status, ProcessLog reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact target and fixed task identity are present | Continue only to the declared read, generic Data Loader preview, or status step |
| Verify | Target profile state or an accepted process must be read and reconciled | Read-only verification only; no replacement submission |
| Blocked until approved | Immutable preview approval has not been released | No live POST |
| Blocked | A mandatory dependency is missing, stale, ambiguous, ineligible, or rejected | Stop and report the required correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AICP.DEPENDENCY_READINESS | decision | 3 | resolve_dependency | satisfied->AICP.DESIGN_GATE;blocked->AICP.ERROR | AICP.READ_PROFILE_OPTION | stop | Before immutable preview, approved execution, or status continuation |
