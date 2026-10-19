# Design Enforcement

Enforce whole-task FSM migration and prevent stale or unreviewed profile-value changes. This resource does not itself edit profile values, construct an import adapter, or submit a Fusion request.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fix task and scope | Use only Manage Customer Center Profile Options and its complete task-level FSM package |
| 2 | Bind export route | Export only through shared.setup-export.task-level-export after exact preview approval |
| 3 | Verify changed profile state | Read target definition and level value for every changed profile row before preview |
| 4 | Bind import route | Route exclusively through core.data-loader and retain its Task Hook validation envelope |
| 5 | Preserve immutable package | Bind approval to the exact ZIP SHA-256; any rebase or package change requires a new preview and approval |
| 6 | Reconcile outcome | After an accepted import, use the returned ProcessId and ProcessLog; do not submit another import automatically |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every run | Error |  | Task name or code differs from Manage Customer Center Profile Options and ZCM_MANAGE_CUSTOMER_CENTER_PROFILE_OPTIONS | Restore the catalog-backed task identity | Yes |
| Export | Error |  | Template, export criteria, filter, partial selection, or nonshared executor is requested | Use a complete, unfiltered, non-template shared FSM export | Yes |
| Import with changed profile rows | Error | read_profile_option_definition | A changed row lacks an exact profile code, level, current target value, proposed value, or enabled/updatable target-level evidence | Read the target state and rebuild the preview with the exact change plan | Yes |
| Import | Error |  | ZIP bytes, hash, task metadata, target, or Task Hook validation envelope differs from the approved preview | Restart Core Data Loader validation and obtain fresh approval | Yes |
| Import | Error |  | This pillar skill selects or invokes an adapter, endpoint, payload builder, upload method, initiation method, status implementation, or retry policy | Hand the immutable task context to core.data-loader and let it choose and execute the registered route | Yes |
| Import | Error |  | This pillar skill adds a package-origin or release-compatibility policy, modifies the generic loader, or independently selects an adapter or source-target-difference option | Remove the task-local policy and hand the immutable task context to core.data-loader under its unchanged contract | Yes |
| Revision mismatch | Error |  | The same rejected archive is proposed again, or this pillar skill selects its own recovery | Preserve the rejection and let core.data-loader prescribe the supported recovery; any new package requires a new preview and approval | Yes |
| Any process acceptance or uncertain response | Error |  | Another import is proposed before the prior ProcessId is reconciled | Poll or retrieve the existing process and ProcessLog; do not resubmit | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_profile_option_definition | Before preview for each changed profile-value row | Current configured value, enabled/updatable flag, level key | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CUCP.DESIGN_GATE | decision | 4 | design_enforcement | pass->CUCP.VALIDATED;fail->CUCP.ERROR | CUCP.DEPENDENCY_READINESS | stop | Before operation-specific preview, adapter release, or import outcome reporting |
