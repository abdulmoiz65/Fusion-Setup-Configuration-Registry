# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| hierarchy_type | CUSTOMER | The user explicitly says use Oracle defaults and does not supply a hierarchy type | No; preserve an explicit user value |  |
| hierarchy_version | null | The user leaves the optional version unset or requests active/current/default behavior | No; preserve and pass an exact supplied Version value otherwise |  |
| flattening_method | INCREMENTAL | The user explicitly says use Oracle defaults and does not supply a flattening method | No; preserve an explicit user value |  |
| hierarchy_name | null | The user does not name a hierarchy | No; show `All hierarchies of the selected type` in the consolidated confirmation and let that one confirmation authorize broad scope and submission |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PHG.APPLY_DEFAULTS | step | 2 | apply_default | applied_or_not_needed->PHG.DEPENDENCY_READINESS;failure->PHG.RETURN_ISSUES | PHG.VALIDATE | stop | Apply only the documented defaults explicitly authorized by the user and retain their provenance in the preview. |
