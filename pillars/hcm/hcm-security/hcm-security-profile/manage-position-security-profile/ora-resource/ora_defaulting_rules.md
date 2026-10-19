# Position Security Profile Defaulting Rules

Use the supplied Y and N values in the task-template CSV representation.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | Y | No value is supplied | No | resolve_yes_no_from_common_lookup |
| ViewAllFlag | N | No value is supplied | No | |
| IncludeFuturePositionsFlag | N | No value is supplied | No | resolve_yes_no_from_common_lookup |
| IncludeTopPositionFlag | N | No value is supplied | No | resolve_yes_no_from_common_lookup |
| PosHierarchyTreeCode | #null | PosHierarchyTreeStructCode resolves to PER_POS_HRCHY | No | resolve_position_hierarchy_tree_structure_from_common_lookup |
| All other flags | N | No value is supplied for a flag other than EnabledFlag, ViewAllFlag, IncludeFuturePositionsFlag, or IncludeTopPositionFlag | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.APPLY_DEFAULTS | step | 30 | apply_default | applied->POS.ENFORCE_SCOPE;skipped->POS.ENFORCE_SCOPE | POS.RESOLVE_CSV_CONTEXT | stop | Profile defaults are evaluated after configuration lookup and CSV context resolution |
