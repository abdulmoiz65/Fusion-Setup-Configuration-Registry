# Manage External Integrations Dependency Readiness

Only the export path has a workflow dependency. Status is a read-only GET, and setting changes return public Oracle documentation without changing Fusion.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task identity | Use ORA_IRC_EMP_EXT_INTEGRATIONS / Manage External Integrations |
| 2 | FSM export route | Route through shared.setup-export.task-level-export, which uses the FSM setup-task CSV export flow |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| MEI-FSM-EXPORT | FSM Data Loader export route | Yes | Export is requested | Satisfied | Task SKILL.md and setup-task catalog | | Keeps export on the supported FSM task-level workflow | Use shared.setup-export.task-level-export; core.data-loader remains the import route, not the export command | TaskCode ORA_IRC_EMP_EXT_INTEGRATIONS and TaskName Manage External Integrations |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The task identity and FSM export route are available | Yes, run the routed export |
| Blocked | The task cannot be resolved or the export workflow is unavailable | No; report the missing route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEI.ROUTE_EXPORT | decision | 5 | resolve_dependency | ready->MEI.RETURN_EXPORT_ROUTE;blocked->MEI.HANDLE_ERROR | MEI.VALIDATE_INPUT | stop | An FSM export is requested |
