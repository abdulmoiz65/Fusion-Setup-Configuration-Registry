# Dependency Readiness

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| existing_group_identity | Existing overhead cost element group | Yes | Membership add or update, membership removal, parent-only update, or delete | Lookup | CostElementGroupId, or CostElementGroupCode with optional CostOrganizationId or cost organization qualifier | resolve_existing_cost_element_group | Resolve exactly one existing group and its IDs for a non-create operation | Search the group code case-insensitively; request a cost organization qualifier only if exact code matches remain ambiguous. Honor a supplied group ID only after verifying its returned parent. | CostElementGroupId: CostElementGroupId; CostOrganizationId: CostOrganizationId |
| existing_member_identity | Existing cost element group member | Yes | Membership removal | Lookup | Resolved CostElementGroupId; CostElementGroupDetailId, CostElementId, or CostElementCode with optional ElementTypeCode | resolve_existing_cost_element_group_member | Resolve exactly one existing child member under the resolved parent | Search the element code case-insensitively within the resolved parent. Honor a supplied child-detail ID or element ID only after verifying its returned child row. Request an element type only when the element code is ambiguous within the resolved group. | CostElementGroupDetailId: CostElementGroupDetailId; CostElementId: CostElementId; CostElementCode: CostElementCode; ElementTypeCode: ElementTypeCode |
| cost_organization | Cost organization | Yes | Create or membership add or update when not resolved from the selected existing group | Lookup | User-provided code, name, or search term | resolve_cost_organization | A resolved cost organization is required before cost elements can be searched or selected | Provide a cost organization code, name, or search term | CostOrganizationId: CostOrganizationId |
| cost_elements | Applicable cost elements | Yes | Create or membership add or update | Lookup | Resolved CostOrganizationId; optional user-provided cost element search term and optional cost element type search term | resolve_cost_elements_for_cost_organization | Each child cost element must be applicable to the selected cost organization | Select one or more returned values; optionally provide a cost element term, a cost element type, or both to filter the cost-organization result set | costAccountingOverheadCostElementGroupDetails[].CostElementId: Id |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The operation-specific identity is resolved; create and membership add or update also have one or more applicable selected cost elements; membership removal has one resolved existing child member | Yes, using only the declared resolver |
| Blocked | A required operation-specific identity is absent, unresolved, or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OCEG.CHECK_CREATE_MEMBERSHIP_DEPENDENCIES | step | 20 | resolve_dependency | ready->OCEG.RESOLVE_COST_ORGANIZATION;blocked->OCEG.RETURN_ISSUES | OCEG.CLASSIFY_OPERATION | stop | Create |
| OCEG.CHECK_EXISTING_GROUP_IDENTITY | step | 25 | resolve_dependency | ready->OCEG.RESOLVE_EXISTING_GROUP;blocked->OCEG.RETURN_ISSUES | OCEG.CLASSIFY_OPERATION | stop | Membership add or update, membership removal, parent-only update, or delete |
