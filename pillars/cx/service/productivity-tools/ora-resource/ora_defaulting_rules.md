# Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | FUSION_APPS_SEARCH_ENABLED | Yes | Global Search is being enabled and the Site-level value is explicitly approved | No | resolve_global_search_profile_value |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_SEARCH_OPTIONS | Manage Global Search Profile Options | GSEARCH.DEFAULT | step | 30 | apply_default | applied->GSEARCH.DESIGN;issues->RETURN_ISSUES | GSEARCH.LOOKUP | stop | Global Search is being enabled |
