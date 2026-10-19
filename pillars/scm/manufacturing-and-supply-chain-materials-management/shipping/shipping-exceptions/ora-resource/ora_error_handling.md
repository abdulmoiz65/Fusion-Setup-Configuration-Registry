# Shipping Exceptions Error Handling

Source: Shipping Exceptions Redwood page, live Data Loader metadata preflight, and approved task-authoring boundary.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Type or Severity meaning/code pair does not resolve exactly once | Stop before preview and request an exact supported meaning or matching code. |
| Type lookup returns no rows | Stop before preview. The configured target currently returned zero Type lookup rows; do not invent a code or use a different environment's result. |
| ActiveFlag is neither true nor false | Stop before preview and request true or false. |
| Central Data Loader metadata preflight fails | Stop before Data Loader handoff and follow the central Data Loader diagnostic. Do not use direct REST execution. |
| Data Loader rejects a backend-owned attribute | Preserve the server diagnostic, correct the source against fresh current metadata, and restart validation and preview. Do not create a local ExceptionCode, RestAction, audit, ID, PredefinedFlag, or DFF rule by guesswork. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | The affected Type or Severity field, the exact-match outcome, and the safe correction. |
| Central Data Loader preflight failure | The central diagnostic and a next action without credentials or raw authorization data. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is unresolved, ambiguous, or has no rows | Do not fuzzy-match, select the first row, or invent a backend code. |
| Central Data Loader preflight fails | Do not upload, initiate, or retry a Data Loader request, and do not substitute direct REST execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SE.DONE | terminal | 40 | terminal | none | SE.RESOLVE_SEVERITY | stop | Input and approved lookup validation passed; central Data Loader checks govern handoff |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Input or lookup validation failed |
