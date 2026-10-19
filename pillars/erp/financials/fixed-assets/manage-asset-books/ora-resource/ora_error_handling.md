# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Fresh FSM export or structural metadata is unavailable or contradictory | Stop package generation and obtain a fresh structural contract. |
| Fusion returns `FA_BOOKCTL_INCORRECT_BOOK_NAME` | Correct the Book Name or Asset Book Code, refresh target state, then present the corrected package for approval. |
| Fusion returns `FA_BOOKCTL_INV_FISCALYR` | Preserve the ProcessLog and treat this as an unresolved Asset Books fiscal-year reference/contract failure. Reverify that the exact selected Fiscal Year belongs to the selected Depreciation Calendar and contains the approved current period. Do not retry by blanking Fiscal Year, substituting another same-date fiscal year, or resubmitting the same ZIP. Prepare a new package only after the reference or contract evidence changes and the normal preview and approval gates are repeated. |
| Final ZIP validation finds a missing, blank, duplicated, or invalid defaulted field, or an unresolved Associated Corporate Book | Block the package. Reapply the authoritative rule in ora_defaulting_rules.md, rebuild the affected `asset book data file` row, and rerun final ZIP validation before approval. |
| Import execution fails or is uncertain | Do not retry automatically. Rediscover target state, retain safe diagnostics, and require a new reviewed plan and approval before retrying. |
| Submission is accepted but terminal status, ProcessLog, or fresh Asset Books read-back is unavailable | Report `accepted — pending parent verification`; do not claim completion or start dependent work. |
| Credentials, tokens, headers, or secrets appear in evidence | Do not persist or disclose them. Stop and use the approved authentication route. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FA_BOOK.DESIGN_APPROVAL_GATE | decision | 7 | execution_gate | approved->FA_BOOK.PACKAGE_PREPARED;approval_missing->FA_BOOK.RETURN_ISSUES | FA_BOOK.DESIGN_ENFORCED | stop | The complete business Design Preview requires approval before ZIP creation. |
| FA_BOOK.IMPORT_GATE | decision | 10 | execution_gate | approved->FA_BOOK.HANDED_OFF_TO_PARENT;approval_missing->FA_BOOK.RETURN_ISSUES | FA_BOOK.FINAL_ZIP_VALIDATED | stop | The Final ZIP Preview identifies one validated immutable package for live import. |
| FA_BOOK.HANDED_OFF_TO_PARENT | terminal | 110 | terminal | none | FA_BOOK.IMPORT_GATE | continue | Asset Books import is accepted — pending parent verification. |
| FA_BOOK.EXISTS_IDENTICAL | terminal | 120 | terminal | none | FA_BOOK.EXISTENCE_CHECKED | continue | An existing book exactly matches the requested definition. |
| FA_BOOK.EXISTS_DIFFERENT | terminal | 130 | terminal | none | FA_BOOK.EXISTENCE_CHECKED | continue | An existing book differs from the requested definition. |
| FA_BOOK.RETURN_ISSUES | terminal | 140 | terminal | none | none | continue | Input, dependency, contract, design, artifact, approval, or verification readiness is blocked. |
