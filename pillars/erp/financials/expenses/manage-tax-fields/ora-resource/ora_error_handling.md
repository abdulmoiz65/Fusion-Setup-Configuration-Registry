# Manage Tax Fields error handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| BU not found | Report unresolved BuName in target enterprise; never silently switch to global setup |
| Invalid territory or behavior, duplicate BU/territory | Return input validation issues with field and source; no import |
| Authentication or transport failure | Use active core client diagnostics and bounded recovery; never expose credentials |
| Process failed or timeout | Capture process ID, last status, elapsed time and sanitized process log; stop before retry |
| Partial success | Retain successful outcomes and errors separately; reconcile a fresh export before another decision |
| Candidate violates single-member contract | Reject missing members, changed headers, populated cash-advance rows, unrelated options or scope, and duplicate requested keys before Data Loader preview |
| Live result not yet verified | Report candidate-ready or submitted status accurately; require terminal import success and fresh-export reconciliation before claiming setup completion |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Data Loader approval | Exact environment, task, business scope, intended operation and immutable candidate diff |
| Completion | Verified persisted changes, unresolved errors and artifact references; job submission alone is not success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAX.EXECUTION | step | 6 | execution_gate | success->TAX.DONE;failure->TAX.ISSUES | TAX.DESIGN | stop | create or update |
| TAX.ISSUES | terminal | 8 | terminal | none | none | stop | failure |
| TAX.DONE | terminal | 7 | terminal | none | TAX.EXECUTION | stop | completed validation gates |
