# Error Handling

Source: the generated Import Price Lists setup-task skill and its declared
FBDI Data Loader workflow.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Data Loader source review or Task Hook validation fails | Stop before approval or upload and return the redacted validation result |
| The ZIP changes after validation or preview | Invalidate the preview and validate the changed artifact again |
| Upload, import, or status is failed, timed out, or uncertain | Preserve the available request identity and diagnostics, stop, and use the recovery path defined by core.data-loader |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required task, artifact, or environment input is missing or inconsistent | Correct the input and rerun validation |
| Approval blocker | The exact immutable preview has not been approved | Obtain approval through the core.data-loader workflow |
| Loader failure | Data Loader reports a failed, timed-out, or uncertain operation | Return redacted diagnostics and stop before retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Data Loader preview | Exact target environment, operation, and immutable ZIP identity |
| Failure | Last known status, available external request identity, redacted diagnostics, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Source review or Task Hook validation has not passed | Do not request approval or upload the ZIP |
| The artifact differs from the approved preview | Do not reuse the earlier approval |
| A prior upload or import failed, timed out, or has an uncertain result | Do not retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLB_RETURN_READY | terminal | 2 | terminal | none | PLB_VALIDATE_INPUT | stop | Task validation passed and Data Loader may continue to preview and approval |
| PLB_RETURN_ISSUES | terminal | 3 | terminal | none | none | stop | Any task validation requirement is missing or invalid |
