# Local Outcome Terminals

These terminals report only local validation and defaulting outcomes. They do not diagnose Fusion responses, retry operations, or call a server.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | MDS.VALIDATE_INPUT identifies missing, invalid, or inconsistent local input |
| MDS.COMPLETE | terminal | 40 | terminal | none | MDS.APPLY_DEFAULTS | stop | Local validation and defaulting complete without a server-side call |
