# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied attribute maps to more than one group and Group Name is absent | Stop with Provide Group Name as there are more than 1 for given attribute name |
| Lookup has no exact result or display-value mismatch | Disclose the mismatch and stop before preview or update |
| Approval is missing, stale, or bound to a changed target or request | Stop and obtain a new exact approval preview |
| Fusion rejects the update or returns an uncertain result | Do not retry the update automatically; retrieve the exact record to reconcile the outcome |
| An item-level request returns HTTP 404 | Do not retry the PATCH. Re-resolve the record using `REST-Framework-Version: 9`, validate the Fusion-issued composite-key item link with a read-only GET, then prepare a new approval preview before any further PATCH |
| Post-update verification differs from the approved change | Report verification failure and stop; do not issue another update automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Approval preview | Target environment, resolved business identity, current value, requested change, and exact approved request |
| Verification | Resolved identity and returned value of each approved changed field |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Target is not uniquely resolved | Do not construct a target URL or perform an update |
| Approval is not current | Do not perform an update |
| Update result is uncertain or failed | Do not retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OAC.APPROVAL_GATE | decision | 60 | execution_gate | approved->OAC.READY_FOR_EXECUTION;missing_or_stale->OAC.RETURN_ISSUES | OAC.ENFORCE_PREVIEW_GATES | stop | A preview is ready for a mutable update |
| OAC.READY_FOR_EXECUTION | terminal | 70 | terminal | none | OAC.APPROVAL_GATE | stop | Current approval is bound to the exact preview |
| OAC.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Any validation, lookup, readiness, design, or approval gate fails |
