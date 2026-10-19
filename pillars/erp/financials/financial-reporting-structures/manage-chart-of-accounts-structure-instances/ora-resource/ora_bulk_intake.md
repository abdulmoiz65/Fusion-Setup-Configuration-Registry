# Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| Complete same-task FSM CSV export and metadata XML | Every required exported file and column; template-only files only when needed to clarify shape | Validate, default, lookup, then preview each row |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| First-go import readiness | List files, XML, columns, generated/defaulted values, source evidence, unresolved values, and approval state |
| Unresolved technical value | Do not generate or submit package |
| UI label in technical field | Block unless export or metadata proves acceptance |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.BULK | step | 6 | process_bulk | ready->COAINS.GATE | COAINS.DEFAULT | stop | Object absent |
