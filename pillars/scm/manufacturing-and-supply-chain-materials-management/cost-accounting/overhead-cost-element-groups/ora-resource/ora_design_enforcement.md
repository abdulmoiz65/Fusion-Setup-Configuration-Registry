# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Confirm group composition | For create or membership add or update, confirm that the group has a non-empty selected cost element collection for the resolved cost organization |
| 2 | Confirm parent-only preservation | For a parent-only update, omit child details and preserve existing memberships |
| 3 | Confirm membership removal contract | For membership removal, require one resolved existing child member and use the documented child DELETE contract; never infer removal from omitted rows |
| 4 | Confirm future-transaction impact | For a membership add, update, or removal, inform the user that cost-element changes apply only to new transactions cost processed after the change |
| 5 | Confirm lifecycle restriction | Do not plan deletion of a group used in an overhead accounting rule; historical records are retained. Deactivation is permitted only after all referencing rules are deactivated |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create or membership add or update | Error | resolve_cost_elements_for_cost_organization | No child cost element is selected or a selected element is not applicable to the resolved cost organization | Select one or more applicable cost elements before preview | Yes |
| Parent-only update | Error |  | Child details are supplied or existing memberships would be changed | Omit child details and preserve existing memberships | Yes |
| Membership removal | Error | resolve_existing_cost_element_group_member | No exact existing member is resolved, or removal is represented by omitting child rows | Resolve one member under the resolved parent ID using its child ID, cost element ID, or element code; use an optional type qualifier only for ambiguity. Generate one explicit child DELETE record using the resolved identities. | Yes |
| A group is used in an overhead accounting rule and deletion is requested | Error |  | The group has historical rule usage | Retain the group; deactivate all referencing rules first if the group must no longer be used in new rules | No |
| A cost element selection is changed | Warning |  | None | Explain that the change applies only to transactions cost processed after the change | Yes |
| A percentage-based overhead accounting rule needs a cost basis | Warning |  | None | Use a system-defined or user-defined cost element group to identify the cost elements to sum | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_cost_elements_for_cost_organization | Validate selected group members for create or membership add or update | CostOrganizationId, applicable CostElementId values | ora_reference_lookups.md |
| resolve_existing_cost_element_group_member | Validate one membership removal and populate the child DELETE record | CostElementGroupId, CostElementGroupDetailId or CostElementId, CostElementCode, ElementTypeCode when needed | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OCEG.ENFORCE_CREATE_DESIGN | step | 60 | design_enforcement | passed->OCEG.RETURN_READY_CREATE;blocked->OCEG.RETURN_ISSUES | OCEG.DEFAULT_INACTIVE_FLAG | stop | Create |
| OCEG.ENFORCE_PARENT_ONLY_DESIGN | step | 61 | design_enforcement | passed->OCEG.RETURN_READY_PARENT_ONLY;blocked->OCEG.RETURN_ISSUES | OCEG.ROUTE_RESOLVED_EXISTING_GROUP | stop | Parent-only update |
| OCEG.ENFORCE_DELETE_DESIGN | step | 62 | design_enforcement | passed->OCEG.RETURN_READY_DELETE;blocked->OCEG.RETURN_ISSUES | OCEG.ROUTE_RESOLVED_EXISTING_GROUP | stop | Delete |
| OCEG.ENFORCE_MEMBERSHIP_REMOVAL_DESIGN | step | 64 | design_enforcement | passed->OCEG.RETURN_READY_MEMBERSHIP_REMOVAL;blocked->OCEG.RETURN_ISSUES | OCEG.RESOLVE_EXISTING_GROUP_MEMBER_FOR_REMOVAL | stop | Membership removal |
| OCEG.ENFORCE_MEMBERSHIP_DESIGN | step | 65 | design_enforcement | passed->OCEG.RETURN_READY_MEMBERSHIP;blocked->OCEG.RETURN_ISSUES | OCEG.RESOLVE_COST_ELEMENTS_FOR_EXISTING_GROUP | stop | Membership add or update |
