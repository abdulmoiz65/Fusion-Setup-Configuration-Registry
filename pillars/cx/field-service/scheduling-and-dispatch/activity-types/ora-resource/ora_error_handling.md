# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required workbook values, current-state checks, or design decisions are incomplete | Stop before preview and identify the exact missing or unresolved item |
| A read-only lookup fails or returns an ambiguous result | Stop before preview, report the safe diagnostic, and do not retry automatically |
| A REST preview is unavailable or differs from the reviewed request | Stop; obtain a new exact preview before approval |
| A live PUT fails | Stop after the failed operation; do not automatically retry or submit a substitute write |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required Activity Type workbook value is missing or invalid | Correct the identified workbook field and restart validation |
| Dependency or lookup | A group, type, or language read cannot be resolved | Resolve the documented lookup contract and restart from validation |
| Approval blocker | An exact preview has not received one approval for the displayed PUT | Obtain approval bound to the exact preview |
| Fusion API | A preview or live PUT fails | Report the operation outcome and stop before retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview approval | The exact preview, affected label, intended operation, and approval status |
| Failed preview or live PUT | Method, endpoint, label, status or safe diagnostic, and the next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No exact approved preview | A live PUT |
| Failed or uncertain PUT | Automatic retry, a substitute write, or assumed success |
| Unassessed optional feature or business-design decision | Inferring its value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AT.PREVIEW_GATE | step | 5 | execution_gate | ready->AT.ALL_GOOD;blocked->AT.RETURN_ISSUES | AT.DESIGN | stop | Before approval or any live Activity Types PUT |
| AT.ALL_GOOD | terminal | 6 | terminal | none | AT.PREVIEW_GATE | continue | An exact preview is recorded and approval is current; live execution remains outside this resource-authoring workflow |
| AT.RETURN_ISSUES | terminal | 7 | terminal | none | none | continue | Validation, lookup, dependency, design, preview, approval, or live execution is blocked or fails |
