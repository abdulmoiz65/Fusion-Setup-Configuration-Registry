# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identity gate | Resolve the attribute group and then the exact item link from the live lookup |
| 2 | Change-scope gate | Limit the request to the normalized ControlLevel and optional MaximumDecimalDigits when supplied |
| 3 | Approval gate | Bind approval to the target environment, resolved identity, current values, and requested changes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any operational attribute control update | Error | resolve_attribute_group_by_attribute | The supplied attribute maps to more than one group and Group Name is absent | Provide Group Name as there are more than 1 for given attribute name | Yes |
| Any operational attribute control update | Error | resolve_operational_attribute_control | The record does not resolve exactly once | Correct the technical identity before preview | Yes |
| Any operational attribute control update | Error | resolve_operational_attribute_control | Requested display values differ from the resolved record | Correct the supplied identity values before preview | Yes |
| Any operational attribute control update | Error | | The proposed change includes fields not explicitly requested and approved | Limit the request to approved changed fields | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_attribute_group_by_attribute | Before resolving the target when Group Name is not supplied | AttrGroupName, AttrGroupDispName, AttrName, AttrDispName | ora_reference_lookups.md |
| resolve_operational_attribute_control | Before preview of any update | Resolved item link, current ControlLevel, current MaximumDecimalDigits, technical names, display names | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OAC.ENFORCE_PREVIEW_GATES | decision | 50 | design_enforcement | passed->OAC.APPROVAL_GATE;blocked->OAC.RETURN_ISSUES | OAC.CHECK_READINESS | stop | Target is resolved and ready |
