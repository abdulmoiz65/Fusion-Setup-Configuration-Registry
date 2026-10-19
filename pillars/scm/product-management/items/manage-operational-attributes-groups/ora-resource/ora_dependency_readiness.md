# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Attribute group | Resolve the group names from the supplied attribute name or display name |
| 2 | Target operational attribute control | Resolve exactly one current Fusion record using the resolved technical composite key |
| 3 | Requested-value confirmation | Confirm the resolved identity and retain current ControlLevel and optional MaximumDecimalDigits for the approval preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| resolved_attribute_group | Attribute group for the supplied attribute | Yes | Any update request | Lookup | Fusion REST collection | resolve_attribute_group_by_attribute | The technical group is required to form the exact control-record identity | Provide Group Name when more than one group is returned for the attribute | AttrGroupName, AttrGroupDispName, AttrName, AttrDispName |
| resolved_operational_attribute_control | Existing operational attribute control | Yes | Attribute group is resolved | Lookup | Fusion REST collection | resolve_operational_attribute_control | A PATCH must target one Fusion-issued item link | Correct the resolved identity values if no single record is found | Resolved item link, current ControlLevel, current MaximumDecimalDigits |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | One group and one control record are resolved | Yes |
| Blocked | The attribute has several groups without a supplied Group Name, or the target is not unique | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OAC.CHECK_READINESS | decision | 40 | resolve_dependency | satisfied->OAC.ENFORCE_PREVIEW_GATES;blocked->OAC.RETURN_ISSUES | OAC.RESOLVE_TARGET | stop | Attribute group and target lookups completed |
