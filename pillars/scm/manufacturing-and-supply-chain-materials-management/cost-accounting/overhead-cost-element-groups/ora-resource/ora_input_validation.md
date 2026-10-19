# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | Mandatory | Applies When | If Missing | How to Resolve |
|---|---|---|---|---|---|
| Operation | Create, membership add or update, membership removal, parent-only update, or delete | Yes | Always | Stop | State the intended operation before validation begins |
| Create identity | CostElementGroupCode | Yes | Create | Stop | Provide a non-empty new overhead cost element group code |
| Existing-group identity | CostElementGroupCode with optional cost organization qualifier, or CostElementGroupId | Yes | Membership add or update, membership removal, parent-only update, or delete | Stop | Resolve the group code; provide a cost organization qualifier only when the group code has multiple matches. Honor a supplied ID as an alternate identity. |
| Cost organization selection | CostOrganizationSearchTerm, CostOrganizationCode, or CostOrganizationName | Yes | Create or membership add or update when CostOrganizationId is not resolved from the selected existing group | Stop | Provide one cost organization search value for exact selection |
| Cost element filters | CostElementSearchTerm or CostElementTypeSearchTerm | No | Create or membership add or update, when supplied | Continue without a filter | Apply every supplied filter; when neither is supplied, list the applicable cost elements for the resolved cost organization |
| Group members | costAccountingOverheadCostElementGroupDetails with one or more selected CostElementId values | Yes | Create or membership add or update | Stop | Resolve and select at least one applicable cost element |
| Member-removal identity | CostElementCode with optional ElementTypeCode qualifier, CostElementId, or CostElementGroupDetailId | Yes | Membership removal | Stop | Resolve the exact element code within the group; provide a type qualifier only when the code has multiple member matches. Honor a supplied ID as an alternate identity. |

## Field Validation

| Field | Mandatory | Applies When | Accepted Values or Fields | If Missing or Invalid | Send in Request Body? |
|---|---|---|---|---|---|
| CostElementGroupId | No | When supplied for membership add or update, membership removal, parent-only update, or delete | Exact existing group ID | Stop only when the supplied ID does not identify one group | Alternate identity |
| CostElementGroupCode | Yes | Create; membership add or update, membership removal, parent-only update, or delete unless an ID is supplied | Non-empty user-provided text | Stop only when neither an ID nor a group code is supplied | Create value or natural-key parent identity |
| CostOrganizationId | Yes | Create or membership add or update when not resolved from the selected existing group | ID returned by resolve_cost_organization or resolve_existing_cost_element_group | Stop; do not use a user-supplied search term as an ID | Yes when required by the selected operation |
| CostElementGroupDescription | No | When supplied | User-provided text | Keep blank when omitted | Yes |
| InactiveFlag | No | When supplied | Boolean, Y, N, active instruction, or inactive instruction | Reject explicit null or ambiguous status | Yes |
| costAccountingOverheadCostElementGroupDetails | Yes | Create or membership add or update | Non-empty array of selected cost elements | Stop; do not create or add or update memberships with an empty collection. Parent-only updates and group deletes omit this collection and preserve existing memberships. | Yes when adding or updating memberships |
| costAccountingOverheadCostElementGroupDetails[].CostElementId | Yes | For every child in a create or membership add or update | ID returned by resolve_cost_elements_for_cost_organization | Stop; do not construct a child from an unresolved cost element | Yes when adding or updating memberships |
| CostElementGroupDetailId | No | Membership removal when supplied | Exact existing child-detail ID under the resolved group | Stop if it is not an existing member of the resolved group | Alternate child identity |
| CostElementId | No | Membership removal when supplied | Exact existing member CostElementId under the resolved group | Stop if it is not an existing member of the resolved group | Alternate child identity |
| CostElementCode | Yes | Membership removal when child IDs are absent | Exact existing member code under the resolved group | Stop only when no child ID, element ID, or element code is supplied; request ElementTypeCode only when the code is ambiguous | Natural-key child identity |
| ElementTypeCode | No | Membership removal when CostElementCode is ambiguous | Exact type of an existing member with the supplied code | Stop if the code remains ambiguous after the qualifier | Ambiguity qualifier only |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OCEG.VALIDATE_INPUT | step | 10 | validate_input | valid->OCEG.CLASSIFY_OPERATION;invalid->OCEG.RETURN_ISSUES | none | stop | Always |
| OCEG.CLASSIFY_OPERATION | decision | 15 | evaluate_result | create->OCEG.CHECK_CREATE_MEMBERSHIP_DEPENDENCIES;membership_add_or_update->OCEG.CHECK_EXISTING_GROUP_IDENTITY;membership_removal->OCEG.CHECK_EXISTING_GROUP_IDENTITY;parent_only_update->OCEG.CHECK_EXISTING_GROUP_IDENTITY;delete->OCEG.CHECK_EXISTING_GROUP_IDENTITY;invalid->OCEG.RETURN_ISSUES | OCEG.VALIDATE_INPUT | stop | Always |
