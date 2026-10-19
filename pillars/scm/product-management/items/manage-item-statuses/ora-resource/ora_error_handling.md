# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Status Code or Status Name is missing | Return the missing field names and stop before the record is used. |
| Derived Status Code is blank | Return the derived code and supplied Status Name, then request an explicit unique Status Code and stop before preview or submission. |
| Derived Status Code collides case-insensitively with an existing Status Code while the supplied Status Name is available | Derive and verify the next numbered candidate with the complete case-insensitive collection scan; show the available candidate for confirmation before preview or submission. |
| Supplied Status Name collides with an existing Status Name | Return the supplied Status Name and stop before preview or submission; never remap a duplicate name. |
| Item-status identity lookup has zero, multiple, conflicting, or unreadable results | Return the supplied Status Code and/or Status Name, request one exact existing identity value, and stop before preview or submission. |
| Confirmed derived or numbered Status Code or Status Name is no longer available, or the code collection cannot be completely read | Return the confirmed pair, identify the collision or unavailable evidence, and stop before preview or submission. |
| Status Code exceeds 10 characters | Return the supplied Status Code and its maximum length, then stop. |
| Status Code contains a space | Return the supplied Status Code and state that spaces are not allowed, then stop. |
| Status Name exceeds 240 characters | Return the supplied Status Name and its maximum length, then stop. |
| Status Description exceeds 240 characters | Return the supplied Status Description and its maximum length, then stop. |
| A status-controlled attribute is not Y or N | Return the affected attribute name and value, then stop. |
| Stocked or Build in WIP is Y while Inventory Item is not evidenced as Y | Return the affected Item Status Code and prerequisite failure, then stop before preview or submission. |
| StatusControl does not exactly resolve to one standard lookup code or meaning | Return the supplied StatusControl value and request an exact LookupCode or Meaning from lookup type EGP_STATUS_CONTROL_CODES, then stop. |
| An AttrDispName operational-attribute lookup has zero, multiple, or unreadable results | Return the requested display name when supplied, require an exact AttrDispName for a specific lookup, and stop before preview or submission. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Status Code or Status Name is blank or absent | Provide the missing required value and restart validation. |
| INVALID | A supplied value exceeds its permitted length, a Status Code contains a space, or a status-controlled attribute is not Y or N | Correct the identified value and restart validation. |
| DEPENDENCY | Stocked or Build in WIP is Y while Inventory Item is absent, N, or not evidenced as Y for the same status | Set Inventory Item to Y, refresh the exported baseline, and restart validation. |
| LOOKUP | A supplied identity cannot resolve exactly, a derived candidate name collides, a confirmed candidate is no longer available, a StatusControl code or meaning cannot resolve exactly, a requested AttrDispName cannot resolve exactly, or a required read fails | Provide a unique Status Name or explicit Status Code, resolve the read failure, or provide an exact StatusControl LookupCode, Meaning, or AttrDispName, then restart validation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation fails | The affected field or attribute, its supplied value when available, the applicable requirement, and the corrective action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Input validation fails | Do not continue to preview, construct a payload, or submit setup data. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IST.RETURN_SUCCESS_NO_OPERATIONAL_ATTRIBUTE | terminal | 50 | terminal | none | IST.DETERMINE_OPERATIONAL_ATTRIBUTE_LOOKUP | stop | All required validation and optional StatusControl handling rules pass, and no operational attributes are provided |
| IST.RETURN_SUCCESS_OPERATIONAL_ATTRIBUTE | terminal | 55 | terminal | none | IST.RESOLVE_ITEM_OPERATIONAL_ATTRIBUTE | stop | All required validation and optional StatusControl handling rules pass, and the requested operational-attribute lookup resolves exactly |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | Manage Item Statuses validation, StatusControl lookup, or operational-attribute lookup identifies a missing or invalid value |
