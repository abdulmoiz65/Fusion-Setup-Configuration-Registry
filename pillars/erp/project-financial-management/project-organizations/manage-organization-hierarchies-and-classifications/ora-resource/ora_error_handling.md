# Manage Organization Hierarchies and Classifications Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Target access, owner approval, current state, or requested design is missing | Stop and return the exact missing business fact |
| Hierarchy type or classification value is invalid or ambiguous | Stop; resolve one exact target-supported value |
| Explicit classification-reference audit fails preflight or returns an authorization, service, transport, empty, partial, malformed, or ambiguous result | Follow failure->OHCL.HANDLE_ERROR, disclose the sanitized audit failure, and stop before preview or import; preserve static validation and do not retry or switch routes |
| Desired classification selection is empty | Stop the proposal and retain the prior approved state |
| Non-None hierarchy lacks a valid tree, active version, or starting organization | Stop before preview or save |
| FSM import conflicts with an existing hierarchy type | Stop only the replacement operation and return it as unsupported unless fresh target evidence proves a non-UI contract |
| Classification removal is requested through FSM import | Stop only the removal operation unless the exact target template proves supported removal behavior |
| Exact FSM template or package contract is unavailable | Continue assisted planning; block package generation and import |
| Preview changes after approval | Invalidate approval and generate a new preview |
| Import is accepted but no successful process log is available | Report Processing with the request reference and safe next action; do not claim success or retry |
| Import fails, times out, or has an uncertain result | Preserve sanitized evidence; do not retry or switch routes; reconcile target state first |
| Import process log or fresh target export differs from the approved preview | Report the mismatch and stop further execution |
| Target reports the maintenance-process follow-up | Record the requirement and hand off to the separately scoped task |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required scope, access, approval, baseline, target value, default hierarchy, template, or metadata is absent | Supply or export the missing fact |
| UNSUPPORTED | Direct REST, internal service, browser automation, hand-built package, unproven import replacement/removal, or implicit maintenance-process submission is requested | Use the proven template-gated route or return only the unsupported operation |
| PROCESSING | Accepted initiation, or a later requested status remains active or timed out | Retain the receipt and last state; wait for a later explicit status/results/verification request without resubmitting |
| FAILED | Validation, warning, requested classification-reference audit, approval, import, process log, or target-state verification fails | Resolve the disclosed issue before a fresh preview |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview and approval | Target, route, current and desired hierarchy state, classifications added/removed/preserved, default hierarchy when applicable, business-unit impact, member and row counts, warnings, checksum |
| Import result | Request reference, sanitized process status, row result, and whether target-state verification is complete |
| Failure | Task code and name, target, failure category, affected business value or package area, verified target state, and one safe next action |
| Classification-reference audit failure | Resolver, verified target when available, failure class (input validation, auth/authz, transport/environment, Fusion API, or artifact persistence), collection completeness, sanitized evidence reference, and one safe corrective action; never expose credentials or treat missing audit results as a changed classification set |
| Follow-up | Whether Maintain Project Organizations is required and that it remains separately scoped |
| UI hierarchy warning lifecycle | A prior posted hierarchy, an actual change, and existing BUs cause a warning. No or dialog cancellation restores the prior type; Yes selects the new structure and opens default-tree selection except for None. Cancelling default-tree selection also restores the prior type. Never treat a warning as an omitted-value default or implicit FSCR approval. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No exact target template or mapping | Do not invent columns, archive names, manifests, translations, keys, or package assembly |
| Internal source behavior is known | Do not expose it as a supported REST, internal-service, or direct Data Loader row contract |
| Execution result is uncertain | Do not retry, replay, or switch mechanisms without fresh reconciliation, preview, and approval |
| Maintenance follow-up is indicated | Do not submit the process from this task without its own scope and approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.EXECUTION_GATE | decision | 9 | execution_gate | accepted_processing->OHCL.PROCESSING;persistence_failed->OHCL.HANDLE_ERROR;missing->OHCL.HANDLE_ERROR;declined->OHCL.REFUSED | OHCL.ENFORCE_DESIGN | stop | Require core preflight, Task Hook and exact-archive approval; submit once and register acceptance before returning without status or export calls; persistence failure retains a known ID and never resubmits |
| OHCL.STATUS_REQUEST_GATE | decision | 10 | execution_gate | status_requested->OHCL.LOAD_COMPLETION_GATE;invalid->OHCL.HANDLE_ERROR | OHCL.VALIDATE_INPUT | stop | Require a later explicit status/results/verification request and registered matching project, target, task, request ID and approved archive checksum; resume without preparation, approval or submission |
| OHCL.LOAD_COMPLETION_GATE | decision | 11 | execution_gate | terminal_success->OHCL.VERIFY_TARGET_STATE;terminal_status->OHCL.RETURN_STATUS;processing->OHCL.PROCESSING;polling_timeout->OHCL.PROCESSING;failure->OHCL.HANDLE_ERROR | OHCL.STATUS_REQUEST_GATE | stop | Only on an explicit resume use core status/count/error checks; terminal_success requires requested setup verification, terminal_status is successful status-only completion; active or timed-out status stops without polling again |
| OHCL.HANDLE_ERROR | step | 13 | error_handler | disclosed->OHCL.FAILED | none | stop | A validation, readiness, reference lookup, approval, execution, resume or verification issue occurs |
| OHCL.READY | terminal | 14 | terminal | none | OHCL.VERIFY_TARGET_STATE | continue | Requested setup verification proves approved changes and preservation after terminal load success |
| OHCL.PROCESSING | terminal | 15 | terminal | none | none | continue | Accepted initiation or requested active/timed-out status; retain receipt and wait for another explicit request; task is not complete |
| OHCL.RETURN_STATUS | terminal | 16 | terminal | none | OHCL.LOAD_COMPLETION_GATE | continue | Return the requested successful load status/count/error result without setup-verification or task-completion claim |
| OHCL.FAILED | terminal | 17 | terminal | none | OHCL.HANDLE_ERROR | continue | A disclosed issue prevents readiness or completion |
| OHCL.REFUSED | terminal | 18 | terminal | none | none | continue | Requested route or action is unsupported or declined |
