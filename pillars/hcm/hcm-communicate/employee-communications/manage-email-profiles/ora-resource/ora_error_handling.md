# Manage Email Profiles Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact ConfigName exists | Stop before archive preparation |
| Archive hash differs from approved preview | Stop before upload |
| Import outcome is uncertain | Do not resubmit; inspect import result first |
| Delete target is ambiguous | Stop before archive preparation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEP.EXECUTION_GATE | decision | 4 | execution_gate | preview_ready->MEP.RETURN_SUCCESS;blocked->MEP.HANDLE_ERROR | MEP.ENFORCE_DESIGN | stop | An immutable archive has a fresh approval |
| MEP.RETURN_SUCCESS | terminal | 5 | terminal | none | MEP.EXECUTION_GATE | stop | A sender-profile archive is ready for submission |
| MEP.HANDLE_ERROR | step | 6 | error_handler | disclosed->MEP.RETURN_ISSUES | none | stop | Input, baseline, archive, or approval behavior is blocked |
| MEP.RETURN_ISSUES | terminal | 7 | terminal | none | MEP.HANDLE_ERROR | stop | A blocked result is disclosed |
