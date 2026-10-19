# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Create code, type, or category is invalid | Stop; correct the source values and regenerate the artifact. |
| Update identity is missing or ambiguous | Stop; correct the Condition Event Code and Type Code combination before retrying. |
| A description-only artifact changes another field | Stop; regenerate the artifact preserving type, category, active status, and end date. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CEC.INPUT_VALID | terminal | 20 | terminal | none | CEC.VALIDATE_CONDITION_EVENT_INPUT | stop | Condition Event Code input is valid |
| CEC.INPUT_INVALID | terminal | 30 | terminal | none | none | stop | Condition Event Code input is missing or invalid |
