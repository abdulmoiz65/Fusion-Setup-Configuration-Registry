# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required group or attribute detail is missing | Return the missing detail and stop before preparing or importing setup data. |
| Internal Name contains a comma | Return the invalid Internal Name and stop until it is corrected. |
| Attribute group behavior is unsupported | Return the supplied behavior and require Single Row or Multiple Row. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required group or attribute detail is not supplied | Provide the missing detail and restart validation. |
| INVALID | Internal Name contains a comma or behavior is unsupported | Correct the supplied value and restart validation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or design enforcement fails | Affected field or dependency, the applicable rule, sanitized supplied value when available, and corrective action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Input validation fails | Do not continue to prepare task-specific configuration details. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 20 | terminal | none | none | stop | Input validation identifies missing or invalid Items-specific details |
| IAG.READY | terminal | 30 | terminal | none | IAG.VALIDATE_INPUT | stop | All applicable Items-specific input validations pass |
