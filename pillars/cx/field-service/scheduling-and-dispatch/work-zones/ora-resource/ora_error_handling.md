# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Workbook does not contain a readable Work Zones worksheet | Stop and identify the missing workbook source. |
| Candidate row lacks required Work Zone values or contains a duplicate key | Stop the affected candidate set and show the exact row and field. |
| A design rule blocks preview | Show the WZ rule ID, blocking condition, and permitted correction. |
| REST setup-data write is requested with an unsupported execution direction or undocumented payload field | Stop. Use only the documented Work Zones POST-create or PUT-replace contract; do not substitute a Data Loader route or another endpoint family. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Workbook sheet, affected row, affected field, and failed rule. |
| Design blocker | WZ rule ID, blocking condition, recommendation, and Fix Allowed value. |
| REST write blocker | Unsupported execution direction or an undocumented endpoint, payload field, preview, approval binding, or read-back contract. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Data Loader is requested | Do not run a Data Loader command or start an import. |
| REST contract is incomplete | Do not infer a REST endpoint, method, payload, or duplicate behavior. |
| Live write has not received approval bound to an immutable preview | Do not call a mutating endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WZ.RETURN_ISSUES | terminal | 3 | terminal | none | none | stop | Workbook validation or design enforcement fails. |
| WZ.RETURN_SUCCESS | terminal | 4 | terminal | none | WZ.ENFORCE_DESIGN | stop | Workbook validation and applicable design enforcement pass. |
