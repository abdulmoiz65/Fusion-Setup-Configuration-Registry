# Position Security Profile Error Handling

The supplied describe response defines no task-specific error payload or retry contract. Stop on validation, lookup, or design-enforcement failure; do not retry a create, update, or delete operation from these resources.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity or conditional configuration is unavailable | Return the issue and request the missing or corrected value |
| A genuine rename has an available new Name | Report `rename CSV identity mapping unverified` and stop before CSV preview or import. Do not infer parent or child update keys from REST IDs or name-based GroupingKeys. |
| A documented lookup cannot retrieve its result | Stop and preserve sanitized lookup evidence; do not infer a profile or enterprise setting |
| A live create or update is requested | Require the current task-template CSV package, immutable ZIP preview, exact approval, one core.data-loader-authorized task-level CSV import, and process-log verification before reporting a result |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any response | Do not display internal IDs, including profile, child-row, lookup, process, request, content, or data-set identifiers; retain them only in sanitized internal evidence when needed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup, validation, or design rule fails | Do not retry a mutation, construct an undocumented request body, or substitute an undocumented configuration value |
| A direct REST create or update is requested | Do not send POST, PATCH, PUT, or DELETE to positionSecurityProfiles; prepare and approve a task-level CSV import instead |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.DONE | terminal | 50 | terminal | none | POS.ENFORCE_SCOPE | stop | Validation, defaults, and design enforcement are complete |
| POS.RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | A task rule returns an issue |
