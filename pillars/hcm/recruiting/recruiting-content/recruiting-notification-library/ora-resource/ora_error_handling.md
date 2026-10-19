# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Recruiting Notification Library request is received | Redirect to Recruiting Content Library Setup Task Guidance; do not process the request in this task. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Redirected | Every request for this setup task | Continue with Recruiting Content Library Setup Task Guidance. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Request routing | This task always redirects to Recruiting Content Library Setup Task Guidance. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A request is redirected | Do not call Fusion APIs, import or export data, activate a flow, or infer implementation behavior. |
| A request is redirected | Do not retry, substitute another route, or guess a value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RNL.REDIRECTED | terminal | 2 | terminal | none | RNL.REDIRECT | stop | Always |
