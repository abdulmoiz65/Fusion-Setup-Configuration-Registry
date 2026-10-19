# Default Cost Profiles Error Handling

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Default Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-default-cost-profile.html).

## Error Situations

| Situation | What Should Happen |
|---|---|
| No Asset Cost Profile Code, Expense Cost Profile Code, or Consigned Cost Profile Code is supplied | Stop before reference lookup and request at least one type-specific default cost profile. |
| An assignment scope is absent | Stop and request the missing setup information before preview. |
| New Item Profile Creation does not return one exact standard-lookup result | Stop and correct the value or the approved lookup contract before preview. |
| Any resolved Asset, Expense, or Consigned Cost Profile has `CostMethodCode = PERIODIC_AVERAGE` and no cost book was resolved or its `PeriodicAverageFlag` is not `Y` | Stop before preview. Provide a resolved periodic-average cost book or replace the incompatible cost profile. |
| A documented lookup returns zero or multiple results, hasMore is true, or the read request fails | Stop and report the resolver result; do not select a partial result or substitute another lookup. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required default-profile association, at least one type-specific default cost profile, or new-item profile behavior is incomplete or invalid | Supply or correct the indicated information. |
| Lookup failure | A documented resolver cannot return one exact result | Correct the supplied value or resolve the read failure before retrying. |
| Design enforcement | A periodic-average cost profile is paired with no resolved cost book or with a cost book whose `PeriodicAverageFlag` is not `Y` | Provide a cost book with `PeriodicAverageFlag = Y` or choose a non-periodic-average profile. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| A lookup cannot resolve one exact value | State the resolver, sanitized supplied value, result count, and that no substitute lookup was used. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A documented lookup cannot return one exact value | Do not select a result by position or partial match, and do not issue an undocumented substitute lookup. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.HANDLE_ERROR | step | 40 | error_handler | handled->DCP.RETURN_ISSUES | none | stop | Any validation, dependency, or design result blocks progress |
| DCP.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | A blocking issue was classified |
| DCP.DONE | terminal | 60 | terminal | none | DCP.ENFORCE_IMPORT_RECOMMENDATION | stop | All documented checks passed |
