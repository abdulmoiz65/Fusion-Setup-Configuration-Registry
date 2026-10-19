# Attachment Category Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact Category Name already exists in Fusion | Return a duplicate-category error identifying Category Name and stop before checking Entity Name or preparing an update. |
| Entity Name is missing | Default to ITEM_ENTITY, ask the user to approve that entity, and stop before preview until approval is received. |
| Entity Name is not one of ITEM_ENTITY, ITEM_REVISION_ENTITY, EGO_ENGINEERING_CHANGES_B, or ITEMCLASS_ENTITY | Ask the user to provide one of the allowed Entity Name values and stop before preview. |
| The skill's baseline export or duplicate preflight is incomplete or fails | Stop before the local validation graph or preview and preserve the sanitized baseline-export diagnostic; do not assume the name is available. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Category Name or User Name is missing, or supplied Entity Name is not an allowed value | Obtain the missing or allowed value. |
| duplicate | The skill's preflight finds one or more exact Category Name rows in the complete baseline | Stop the create request and report the duplicate Category Name. |
| approval_blocker | The user has not approved the default ITEM_ENTITY or rejects it | Wait for approval or obtain an allowed Entity Name and rerun validation. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Entity Name was defaulted but is unapproved, or a supplied Entity Name is invalid | Do not create, update, preview, or import an attachment category. |
| Exact Category Name already exists | Do not create a duplicate or silently switch to update. |
| The skill's baseline export or duplicate preflight is incomplete or fails | Do not create, update, preview, or import an attachment category. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_SUCCESS | terminal | 80 | terminal | none | APPLY_PRODUCT_MODEL_DEFAULTS | stop | All checks pass, including approval when Entity Name was defaulted |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Local input validation or approval fails after the skill's preflight |
