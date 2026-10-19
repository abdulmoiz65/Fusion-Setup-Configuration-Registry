# Learning Paths Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| New-activity eligibility is unavailable | Block only rows that add or replace activities; preserve unaffected valid rows |
| Graph, lifecycle, usage, lookup, or approval evidence is unresolved | Stop the affected grouped path before mutation and identify the exact field or gate |
| A row changes after preview | Invalidate approval for the affected execution set and rebuild the preview |
| A write outcome is uncertain | Do not retry; reconcile through the confirmed read route first |
| A documented change request times out | Return the operation, sanitized process identity, last status, elapsed time, and safe next-check guidance |
| Readback differs from the approved grouped manifest | Report partial or failed verification without claiming success |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, approval, usage, live value, or documented lookup is unavailable | Supply or resolve the named blocker |
| UNSUPPORTED | Copy, user-facing upsert, or an activity mutation without authoritative eligibility is requested | Select a supported operation or defer the affected row |
| FAILED | Validation, graph checking, execution, polling, or verification fails | Review sanitized diagnostics before another attempt |
| ALL_GOOD | Approved rows, path, graph, validity, renewal, and lifecycle results are verified | Return row-specific results and the completed run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before mutation | Exact environment, grouped path identity or create key, operation, selected rows, graph effects, preview fingerprint, and approval status |
| On failure | Failure class, affected row or group, current rule, sanitized evidence, verified side effects, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent or stale | Do not call POST, PATCH, DELETE, lifecycle, section, nested-activity, or Data Loader write routes |
| A live lookup value or target-specific DFF segment is absent | Do not infer it |
| Copy or user-facing upsert is requested | Do not invoke or synthesize that operation |
| A new activity lacks eligibility evidence | Do not use current membership or a submitted label as eligibility proof |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic conditional-write protection |
| A write result is uncertain | Do not automatically replay the write |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->LPT.EVALUATE_RESULT;blocked->LPT.HANDLE_ERROR | LPT.ENFORCE_DESIGN | stop | A validation-only result or exact approved row set is ready for evaluation |
| LPT.HANDLE_ERROR | step | 8 | error_handler | disclosed->LPT.RETURN_ISSUES | none | stop | A row or grouped path is blocked by validation, dependency, lookup, design, approval, execution, timeout, or verification |
| LPT.RETURN_SUCCESS | terminal | 9 | terminal | none | LPT.EVALUATE_RESULT | stop | Every selected valid row is verified and row-specific results are available |
| LPT.RETURN_ISSUES | terminal | 10 | terminal | none | LPT.HANDLE_ERROR | stop | One or more rows or grouped paths cannot safely complete |
