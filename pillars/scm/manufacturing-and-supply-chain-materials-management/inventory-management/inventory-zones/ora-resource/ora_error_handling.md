# Inventory Zones Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Status or activity type lookup returns no match, multiple matches, or conflicting code and meaning | Stop Data Loader handoff and request an exact approved value. |
| StartDate or EndDate is not in YYYY-MM-DD format | Stop Data Loader handoff and request a valid calendar date in YYYY-MM-DD format. |
| A user supplies a system-managed Activity Usages or Default Delivery Cart field | Stop Data Loader handoff. Remove the user-supplied field; the task rule will populate its fixed value. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A selected lookup value does not resolve exactly. | Correct the supplied code or meaning. |
| Input validation | StartDate or EndDate is malformed or is not a valid calendar date. | Supply the date in YYYY-MM-DD format. |
| Input validation | A user supplies TasksEnabled, TaskGroupingLevel, or a Default Delivery Cart ActivityTypeCode or ConfigurationLevel. | Remove the user-provided field and rerun task validation. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup result is absent, ambiguous, or conflicting | Do not guess, fuzzy-match, or select the first result. |
| A system-managed field is supplied by the user | Do not accept, preserve, or present it as a user-overridable value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INV-ZONES.DONE | terminal | 70 | terminal | none | INV-ZONES.ENFORCE-DELIVERY-CART-CONFIGURATION-LEVEL | continue | Task-local validation, lookup, and defaulting rules have completed. |
| INV-ZONES.RETURN-ISSUES | terminal | 90 | terminal | none | none | stop | A task-local validation or lookup blocker occurs. |
