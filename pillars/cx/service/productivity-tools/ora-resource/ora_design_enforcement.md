# Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | 1 | Confirm Site-level Global Search profile option | FUSION_APPS_SEARCH_ENABLED must be confirmed before Global Search visibility is validated |
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | 2 | Refresh user session | Users must sign out and sign back in before checking Global Search visibility |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | Global Search is being enabled | Error | resolve_global_search_profile_value | FUSION_APPS_SEARCH_ENABLED is not confirmed as Yes at the Site profile level | Set FUSION_APPS_SEARCH_ENABLED to Yes at the Site profile level | Yes |
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | Global Search visibility is being validated after a profile update | Error |  | The user session has not been refreshed | Sign out and sign back in before checking whether Global Search is visible | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | resolve_global_search_profile_value | Before enabling Global Search | Current FUSION_APPS_SEARCH_ENABLED value and profile level | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | GSEARCH.DESIGN | step | 40 | design_enforcement | passed->GSEARCH.DONE;issues->RETURN_ISSUES | GSEARCH.DEFAULT | stop | Global Search is being enabled or validated |
