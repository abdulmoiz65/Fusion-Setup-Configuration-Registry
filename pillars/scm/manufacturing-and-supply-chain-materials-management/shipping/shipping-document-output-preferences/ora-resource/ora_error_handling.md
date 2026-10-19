# Error Situations

| Situation | What Should Happen |
|---|---|
| Lookup returns no rows or more than one row | Stop before Data Loader handoff and report the supplied value and resolver name. |
| Meaning and code identify different lookup rows | Stop before Data Loader handoff and require a consistent value pair. |
| Data Loader metadata or validation fails | Delegate diagnostics and retry behavior to core.data-loader; do not use a direct REST write fallback. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SDOP.RETURN_ISSUES | terminal | 5 | terminal | none | none | stop | Any rule fails |
| SDOP.DONE | terminal | 4 | terminal | none | none | stop | Input validated and all applicable lookup paths completed |
