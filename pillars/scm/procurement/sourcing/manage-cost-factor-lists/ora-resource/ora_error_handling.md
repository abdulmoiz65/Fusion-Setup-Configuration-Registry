# Manage Cost Factor Lists Error Handling

Sources: Oracle Fusion Cloud Procurement 26C, Cost Factors and Cost Factor Lists, accessed 2026-09-23; user direction on 2026-09-24 for Data Loader parent updates.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A new Cost Factor List source has no Cost Factor child row | Reject the source before preview. Create the list parent and one or more Cost Factor children in the same Data Loader source. |
| A new Cost Factor List source supplies ListId | Reject the source before preview. Remove ListId; Data Loader generates and uses the shared parent-child ListId. |
| An existing-list Cost Factor add includes a parent PATCH | Reject the source before preview. Omit the parent row and submit only the child Cost Factor POST rows with the existing ListId. |
| An existing-list Cost Factor update omits ListId or ListCostFactorId | Reject the source before preview. Retrieve the existing child row identity and supply both identifiers in the child PATCH row. |
| An existing-list Cost Factor update includes a parent row | Reject the source before preview. Omit the parent row and submit only the child Cost Factor PATCH rows with the existing ListId and ListCostFactorId. |
| An existing-list Cost Factor delete omits ListId or ListCostFactorId | Reject the source before preview. Retrieve the child row identity and supply both existing identifiers in the child DELETE row. |
| An existing-list Cost Factor delete includes a parent row | Reject the source before preview. Omit the parent row and submit only the child Cost Factor DELETE rows with the existing ListId and ListCostFactorId. |
| An existing Cost Factor List update omits ListId, a PATCH action, or all mutable fields | Reject the source before preview. Include the existing ListId, RestAction PATCH, and at least one of ListName, Description, ListStatus, or ListStatusCode. |
| An existing Cost Factor List update includes Cost Factor child rows or unsupported parent fields | Reject the source before preview. Submit only the parent row and restrict mutable fields to ListName, Description, ListStatus, and ListStatusCode. |
| A Cost Factor List deletion omits one or more current child Cost Factors | Reject the source before preview. Retrieve all current children and include a child DELETE row for each before deleting the parent list. |
| A Cost Factor List deletion omits the parent DELETE row | Reject the source before preview. Include the existing parent ListId with RestAction DELETE and the complete child DELETE set. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Data Loader source validation failure | The parent, child, generated ListId, existing-list child POST, existing-list child PATCH, existing-list parent PATCH, existing-list child DELETE, or list cascade-delete contract is invalid. | Correct the source and restart validation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Data Loader source validation failure | The missing parent or child row, a supplied ListId for a new list, an unsupported parent PATCH for a child-only add, missing child identifiers for a child-only PATCH or DELETE, a malformed parent PATCH, or incomplete list cascade-delete set. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A parent-child Data Loader source is invalid | Do not preview, approve, or submit it. |
| A child-only add includes a parent PATCH | Do not preview, approve, or submit it. |
| A child-only update lacks its existing identifiers or includes a parent row | Do not preview, approve, or submit it. |
| A child-only delete lacks its existing identifiers or includes a parent row | Do not preview, approve, or submit it. |
| A parent update omits its identity or mutable field, includes a child row, or changes an unsupported parent field | Do not preview, approve, or submit it. |
| A list delete omits the parent or any current child DELETE row | Do not preview, approve, or submit it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COST_FACTOR_LIST.RETURN_VALIDATED_CREATE_SOURCE | terminal | 25 | terminal | none | COST_FACTOR_LIST.VALIDATE_LIST_CONTEXT | stop | A Cost Factor List Data Loader source is valid for the core Data Loader preview and approval workflow. |
| RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | Validation, dependency, or lookup reports a blocking issue. |
