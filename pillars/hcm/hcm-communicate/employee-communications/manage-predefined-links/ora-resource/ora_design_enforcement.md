# Manage Predefined Links Design Enforcement

Sources: Confluence page 21736675148, Manage Predefined Links — ORA_IRC_EMP_CAMP_DEEP_LINKS; user-requested FSM export-and-inspect query route.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce task scope | Use the exact Manage Predefined Links task code and its catalog-supported CSV export route |
| 2 | Enforce operation scope | Use the export route for queries; use the core Data Loader FSM import route only for an approved Draft-link activation or rename |
| 3 | Enforce archive evidence | Count only after inspecting the downloaded task CSV metadata, headers, and rows |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A current Active-link count is requested | Blocker | | The task code, offering, or functional area does not resolve to Manage Predefined Links | Use ORA_IRC_EMP_CAMP_DEEP_LINKS under HCM Communicate / Employee Communications | Yes |
| An FSM export is prepared | Blocker | | The operation includes import, mutation, or an unrelated task | Use shared.setup-export.task-level-export for a read-only task export only | Yes |
| Exported rows are counted | Blocker | | The archive metadata and CSV headers were not inspected | Inspect the current downloaded content before selecting the status field and Active representation | Yes |
| An internal UI or ADF service is proposed as the query path | Blocker | | The route bypasses the task export workflow | Use the routed FSM export-and-inspect path | No |
| A Draft link is activated | Blocker | | The current export does not contain exactly one matching ORA_DRAFT row | Refresh the export and resolve DisplayName, ObjectType, and Action exactly once | No |
| A Draft link is renamed | Blocker | | New DisplayName is blank or the current export does not contain exactly one matching ORA_DRAFT row | Supply a nonblank name and refresh the exact baseline row | No |
| A mutation archive is prepared | Blocker | | The archive changes any row other than the approved target or changes fields beyond StatusCode for activation or DisplayName for rename | Rebuild from the current export with only the approved field change | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.ENFORCE_EXPORT_SCOPE | decision | 4 | design_enforcement | passed->MPL.EXPORT_GATE;blocked->MPL.HANDLE_ERROR | MPL.CHECK_REQUEST_READINESS | stop | A current active-link count is prepared through FSM export |
| MPL.ENFORCE_MUTATION_SCOPE | decision | 9 | design_enforcement | passed->MPL.MUTATION_GATE;blocked->MPL.HANDLE_ERROR | MPL.CHECK_MUTATION_BASELINE | stop | A Draft-link activation or rename archive is prepared |
