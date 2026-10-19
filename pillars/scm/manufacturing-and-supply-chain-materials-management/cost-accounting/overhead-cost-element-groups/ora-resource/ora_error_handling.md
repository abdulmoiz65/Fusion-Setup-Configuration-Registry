# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A create or membership add or update lacks its required group, cost organization, or cost element selection | Identify the exact missing value and stop |
| A membership removal, parent-only update, or delete lacks CostElementGroupCode and CostElementGroupId | Request one existing-group identity; do not require a cost organization qualifier unless the group code is ambiguous |
| A supplied group code matches several groups without a cost organization qualifier | Request the cost organization qualifier and resolve the exact group |
| A membership removal lacks a child cost-element code, child-detail ID, and element ID | Request one member identity; prefer the user-facing element code |
| A supplied membership-removal element code matches several existing members in the resolved group | Request ElementTypeCode and resolve the exact member; do not request a type before the code is ambiguous |
| A supplied child-detail ID or element ID is not an existing member of the resolved group | Stop and request a member identity for that group; do not remove a different child |
| Cost organization lookup has no match, or a supplied cost element filter returns no selectable results | Explain the failed lookup and request a corrected cost organization value or optional filter |
| The resolved cost organization has no applicable cost elements | Explain that no cost elements are available for selection and stop |
| A lookup returns several selectable matches | Present the matches and request a user selection |
| A selected cost element is not applicable to the resolved cost organization | Reject the selection and stop before payload construction |
| A deletion is requested for a group used in overhead accounting rules | Refuse the deletion; explain that history is retained and that deactivation requires all referencing rules to be deactivated |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input or selection is absent | Request the exact missing value |
| FAILED | Lookup has no exact selectable result or a selected element is invalid | Preserve the search context and request a corrected value |
| UNSUPPORTED | The request is to delete a group used in an overhead accounting rule | Explain the lifecycle restriction and offer deactivation guidance only |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any preview | The operation, resolved existing-group identity when applicable, resolved cost organization and selected cost elements for create or membership add or update, or the resolved group-and-element identity plus explicit child DELETE record for membership removal, normalized inactive status, and any design warning |
| On a blocked request | Failure category, affected business value, sanitized lookup outcome, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A required value is unresolved or ambiguous | Do not construct a payload, preview a mutation, or execute a write |
| Membership removal is requested | Do not remove a member by omitting child rows or by treating a partial collection as replacement semantics |
| A live error or uncertain write result occurs | Do not retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OCEG.RETURN_READY_CREATE | terminal | 70 | terminal | none | OCEG.ENFORCE_CREATE_DESIGN | stop | Create checks passed; this terminal does not authorize a write |
| OCEG.RETURN_READY_PARENT_ONLY | terminal | 71 | terminal | none | OCEG.ENFORCE_PARENT_ONLY_DESIGN | stop | Parent-only update checks passed; this terminal does not authorize a write |
| OCEG.RETURN_READY_DELETE | terminal | 72 | terminal | none | OCEG.ENFORCE_DELETE_DESIGN | stop | Delete checks passed; this terminal does not authorize a write |
| OCEG.RETURN_READY_MEMBERSHIP | terminal | 73 | terminal | none | OCEG.ENFORCE_MEMBERSHIP_DESIGN | stop | Membership-update checks passed; this terminal does not authorize a write |
| OCEG.RETURN_READY_MEMBERSHIP_REMOVAL | terminal | 74 | terminal | none | OCEG.ENFORCE_MEMBERSHIP_REMOVAL_DESIGN | stop | Membership-removal checks passed with one explicit child DELETE record; this terminal does not authorize a write |
| OCEG.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Any declared missing, failed, ambiguous, blocked, or unsupported outcome |
