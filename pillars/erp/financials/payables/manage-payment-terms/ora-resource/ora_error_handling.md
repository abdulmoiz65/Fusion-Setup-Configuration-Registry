# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A resolver contract issue is recorded | Preserve the customer candidate and record the structured finding in preview and candidate evidence. Review and fix or reverify it during implementation review. |
| Payables Calendar Types REST returns HTTP 400 | Preserve the requested Calendar and record `validation_skipped` plus a structured `resolver_contract_issue` containing endpoint, supplied value, HTTP status, query fingerprint, sanitized diagnostic, timestamp, owner, and required action. It is not proof that the Calendar is invalid. Allow only separately approved FSM import; review and fix or reverify the issue during implementation review. |
| Supporting read-only GET is unavailable | Record `validation_skipped` with HTTP 401/403, TLS, network, timeout, rate-limit, or 5xx errors; endpoint; supplied value; and timestamp. Continue to package generation and, if approved, the governed FSM import. Malformed payloads and unexpected HTTP responses instead block as `resolver_failure`. |
| Package hierarchy or validation evidence changes | Re-run validation and evidence preparation; do not retry a load automatically |
| A child-only Payment Terms archive succeeds but the requested line change is absent from a fresh export | Treat the update as skipped, not successful. Preserve the import and export evidence; rebuild a new archive containing the matching `AP_TERM_HEADER` row and obtain a new preview and approval. |
| CSV parser reports a header or row-width error | Stop the load; rebuild from the exact template headers with full-width rows, then create a new preview and approval |
| A due basis, due-date method, percentage total, amount-zero, numeric-range, discount-completeness, or discount-order rule fails | Stop before ZIP generation; identify the operation and exact fields, request corrected values, and require a new preview. Do not silently add an installment, change a due basis, clamp a negative value, or reorder discounts. |
| A date or Rank rule fails | Stop before ZIP generation; identify the exact header and field. Do not repair a malformed date, reorder active dates, renumber Rank, or scope duplicate-Rank comparison by Set Code. |
| Payment-term Type is not `STD` | Stop before ZIP generation; identify the header and require `Type=STD`. Do not preserve or substitute another explicit type value. |
| A readable lookup returns zero rows | Stop as `not_found` before ZIP/import and retain the supplied Calendar or SetCode in the failure evidence. Do not substitute a returned row or proceed to import. |
| A lookup response is malformed or otherwise unexpected | Stop as `resolver_failure`; retain a sanitized diagnostic and do not generate or import a candidate. |
| Preview or import reports an error, or its outcome is uncertain | Preserve sanitized diagnostics and the immutable candidate identity. Do not retry or resubmit automatically; reconcile the original attempt through the central workflow. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input blocked | Package structure, CSV shape, dates, Rank, due terms, or discount rules are invalid | Correct the reported values or package structure and create a new preview. |
| Resolver blocked | A required Calendar or Set Code lookup returns no result or an invalid response | Correct the submitted value or resolver issue before package generation. |
| Execution blocked | Immutable preview or explicit approval is absent | Complete the central preview and approval workflow. |
| Failed | A controlled import returns an error or has an uncertain outcome | Preserve the original attempt and reconcile it without automatic resubmission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any candidate import | Exact task, target scope, immutable preview identity, known blockers, and required approval boundary |
| On failure | Failure class, sanitized diagnostics reference, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Incomplete resolver | Do not invent values, a writable operation, or an import rule |
| Failed or uncertain import | Do not automatically retry or resubmit. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INPUT.VALIDATE | step | 10 | validate_input | success->DEP.CHECK | none | stop | Always |
| DEP.CHECK | step | 20 | resolve_dependency | success->LOOKUP.CALENDAR;advisory-unavailable->LOOKUP.CALENDAR | INPUT.VALIDATE | stop | Always |
| LOOKUP.CALENDAR | step | 30 | reference_lookup | success->LOOKUP.SET;unavailable->LOOKUP.SET | DEP.CHECK | stop | Calendar is supplied |
| LOOKUP.SET | step | 40 | reference_lookup | success->DEFAULT.APPLY;unavailable->DEFAULT.APPLY | LOOKUP.CALENDAR | stop | SetCode is supplied |
| DEFAULT.APPLY | step | 50 | apply_default | success->DESIGN.ENFORCE | LOOKUP.SET | stop | A new payment-term header omits a defaulted field |
| DESIGN.ENFORCE | step | 60 | design_enforcement | success->PAYTERM.EXECUTION_GATE;failure->ERROR.BLOCK | DEFAULT.APPLY | stop | Always |
| PAYTERM.EXECUTION_GATE | step | 65 | execution_gate | approved_preview->SUCCESS.DONE;not_ready->PAYTERM.EXECUTION_BLOCKED | DESIGN.ENFORCE | stop | A governed execution request exists |
| ERROR.BLOCK | terminal | 70 | terminal | none | none | stop | A documented blocker is reached |
| PAYTERM.EXECUTION_BLOCKED | terminal | 75 | terminal | none | none | stop | Execution approval or preview is absent |
| SUCCESS.DONE | terminal | 80 | terminal | none | PAYTERM.EXECUTION_GATE | stop | A governed immutable preview and approval are available |
