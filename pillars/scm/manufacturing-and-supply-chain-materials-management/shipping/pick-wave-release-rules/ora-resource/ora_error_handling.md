# Pick Wave Release Rules Error Handling

Source: Redwood Pick Wave Release Rules dynamic layout and approved task-authoring boundary.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required UI field is missing | Stop before preview and request the missing field. |
| A checkbox flag is not a recognized friendly value | Stop before preview and request Y, Yes, True, Checked, N, No, False, Unchecked, or a blank value. |
| A UI-only processing dependency is violated | Stop before preview and present the dependent controls that require correction. |
| A display value requires an unverified lookup | Stop before preview and request a backend code or ID, or an approved complete lookup contract. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or dependency failure | The affected field or processing-option combination and the safe correction. |
| Lookup contract gap | That no local or REST resolver is authorized yet; do not claim a matched value. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No complete lookup contract is approved | Do not guess a code or ID, fuzzy-match a display value, or select the first result. |
| Validation or dependency readiness fails | Do not create a preview, archive, upload, or Data Loader request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWR.DONE | terminal | 70 | terminal | none | PWR.VALIDATE_DEPENDENCIES | stop | Input, approved display-value lookup, and UI-only dependency validation passed |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Input, display-value lookup, or UI-only dependency validation failed |
