# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Delegated index action | Rebuild only, subject to the child's seeded-repair checks; retain the complete named profile | Every selected profile identity is already indexed, name resolution succeeded and attributes_to_remove is empty. | No | verify_index_attribute_profile |
| target_fusion_environment | Currently authenticated Fusion environment | The request does not explicitly name a target environment. | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.APPLY-REBUILD-DEFAULT | step | 40 | apply_default | rebuild_prepared->SALES_INDEX.DONE-REBUILD-HANDOFF;failure->RETURN_ISSUES | SALES_INDEX.VERIFY-INDEX-PROFILE | stop | The selected index already contains the complete requested profile |
