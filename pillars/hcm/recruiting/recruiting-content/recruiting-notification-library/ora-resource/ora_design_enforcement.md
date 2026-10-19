# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Route request | Redirect every Recruiting Notification Library request to Recruiting Content Library Setup Task Guidance. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Blocker |  | Any attempt to process Recruiting Notification Library in this task | Continue with Recruiting Content Library Setup Task Guidance. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RNL.REDIRECT | step | 1 | design_enforcement | redirected->RNL.REDIRECTED | none | stop | Always |
