# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact task package, template header, or node path does not match | Stop; rebuild the candidate from the exact task template and create a new immutable preview. |
| The FSM import hook cannot resolve a business-unit or payment-term source value | Preserve the exact dependency diagnostic, correct the named source field, and create a new immutable preview. Do not directly populate the resolved ID. |
| Fusion rejects an approved package | Preserve the process identity and diagnostics, refresh the same-task export, and stop before retry. |
| Candidate input or package changes after preview | Treat the approval as stale; revalidate and obtain a new candidate-bound approval through core.data-loader. |
| The supplied BuName has zero or multiple preflight matches, or a create row has no unambiguous EnterpriseId | Stop before package approval and preserve the diagnostic. Ask the requester which EnterpriseId to use for the blank create rows; do not create a business unit, guess an EnterpriseId, or substitute an OrgId. |
| A create target is already present in the fresh current export | Stop before package approval; require an explicit update request instead of resubmitting a duplicate row. |
| A submitted immutable system lookup code is outside the task-owned allowlist | Stop before package preview and return the named field with its allowed codes. |
| A readable payment-term or currency lookup returns zero or multiple records, or its endpoint is unavailable | Preserve the submitted value with an advisory receipt. A governed FSM import may be submitted; Fusion performs the final context-aware validation. |
| A batch contains multiple independently invalid records | Validate every record, return one aggregated row-by-row diagnostic, and create no candidate ZIP. Resolve every blocking error before a new validation run. |
| A user uploads a structurally valid FSM ZIP with valid and invalid rows | Read the ZIP against a fresh baseline, classify existing keys as updates and absent keys as creates, validate every row, and return valid/invalid row results. Never import automatically; reject the whole upload when any blocking row error exists. |
| A customer-configured lookup code is invalid | Preserve the submitted CSV value and return Fusion's import diagnostic after the governed import. Do not invent a replacement code or retry automatically. |
| A read-only API preflight returns HTTP 400 | Preserve the submitted value. Record `validation_skipped` and a structured `resolver_contract_issue` with endpoint, supplied value, query fingerprint, sanitized diagnostic, timestamp, owner, and required maintenance action. The governed FSM import remains authoritative. A create-time BU/ledger derivation may still need a readable result because it supplies required create context. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Blocked | Missing exact package evidence or unresolved resolver contract | Collect the missing package or validation input, or retain static-only readiness. |
| Execution blocked | Immutable preview or explicit approval is absent | Complete the central preview and approval workflow. |
| Failed | A controlled import returns an error | Preserve the attempt and diagnose without automatic resubmission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any candidate import | Exact task, target scope, immutable preview identity, known blockers, and required approval boundary |
| On failure | Failure class, sanitized diagnostics reference, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unresolved term resolver or package contract | Do not invent a public endpoint, choose a default term, or directly write to Fusion. |
| Failed or uncertain import | Do not retry, overwrite, or submit another package automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INPUT.VALIDATE | step | 10 | validate_input | success->LOOKUP.PREFLIGHT;failure->ERROR.BLOCK | none | stop | Always |
| LOOKUP.PREFLIGHT | step | 15 | reference_lookup | success->DEP.CHECK;failure->ERROR.BLOCK | INPUT.VALIDATE | stop | Any populated field has a supported read-only resolver |
| DEP.CHECK | step | 20 | resolve_dependency | success->DESIGN.ENFORCE;failure->ERROR.BLOCK | LOOKUP.PREFLIGHT | stop | Always |
| DESIGN.ENFORCE | step | 50 | design_enforcement | success->INVOICE.EXECUTION_GATE;failure->ERROR.BLOCK | DEP.CHECK | stop | Always |
| INVOICE.EXECUTION_GATE | step | 60 | execution_gate | approved_preview->SUCCESS.DONE;not_ready->INVOICE.EXECUTION_BLOCKED | DESIGN.ENFORCE | stop | A governed execution request exists |
| ERROR.BLOCK | terminal | 70 | terminal | none | none | stop | A blocking rule is reached |
| INVOICE.EXECUTION_BLOCKED | terminal | 75 | terminal | none | none | stop | Execution approval or preview is absent |
| SUCCESS.DONE | terminal | 80 | terminal | none | INVOICE.EXECUTION_GATE | stop | A governed immutable preview and approval are available |
