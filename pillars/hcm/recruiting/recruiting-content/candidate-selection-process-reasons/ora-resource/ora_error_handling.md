# Candidate Selection Process Reasons Error Handling

## Purpose

Defines package readiness, failure classification, safe disclosure, reconciliation, and stop-before-retry behavior for CSP Reasons authoring and verification.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| CSPRSN-ERR-01 | Required operation, code, name, status, translation, group, pair, or result evidence is missing | Input validation | Stop and request only the exact missing business value or artifact |
| CSPRSN-ERR-02 | Exact code exists for create, is absent for update, or has an unconfirmed case-insensitive lookalike | Intent or identity | Stop, disclose the exact classification and lookalikes, and require corrected intent or exact case |
| CSPRSN-ERR-03 | Requested lifecycle transition is unsupported | Design | Stop and disclose the current and requested statuses plus supported transitions |
| CSPRSN-ERR-04 | Translation parent, installed Language, export-evidenced SourceLang, target base/source language for a new parent, or text is missing or inconsistent | Reference | Stop; require exact target evidence and explicit text. Preserve the exported SourceLang and never attempt to change it through CSV |
| CSPRSN-ERR-05 | Association reason or group is missing, ambiguous, or the reason is not Active | Reference or design | Stop before package generation and identify the unresolved exact key without selecting a substitute |
| CSPRSN-ERR-06 | FSM reports generic JBO-56012 or JBO-26041 for an association or reference failure | Fusion process | Preserve the sanitized ProcessLog, export current state, and reconcile exact rows; do not infer the missing code from generic text |
| CSPRSN-ERR-07 | Export is missing, stale, wrong-target, malformed, or has unusable completion evidence | Catalog or artifact mismatch | Stop and obtain a complete current task-wide export |
| CSPRSN-ERR-08 | Candidate package has wrong members, headers, order, metadata, values, target, release, or fingerprint | Package validation | Stop and rebuild from the validated export; never repair unknown values silently |
| CSPRSN-ERR-09 | Import fails, completes partially, times out, or has uncertain outcome | Process failed or timeout | Preserve sanitized diagnostics and reconcile a current task-wide export before considering another attempt |
| CSPRSN-ERR-10 | CSV rename, CSV deletion, omission-based removal, or any CSV SourceLang change is requested | Unsupported operation | Stop only the unsupported operation; do not generate replacement semantics |
| CSPRSN-ERR-11 | User lacks Recruiting setup or task-flow access | Authorization | Stop and route access review to the Recruiting security owner; do not change execution routes |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, shapes, lengths, enums, or explicit intent are missing or invalid | Correct the request and restart validation |
| Intent or identity | Current exact-code state conflicts with the requested create, update, or replay intent | Confirm corrected intent and exact case-sensitive key |
| Reference | Reason, group, translation context, or association does not resolve exactly | Correct the selector or obtain current target evidence |
| Design | Lifecycle, activity, omission, deletion, scope, or package policy is violated | Correct the request without bypassing the gate |
| Catalog or artifact mismatch | Current export or package differs from the documented task contract | Obtain or rebuild from the current task-wide export |
| Authorization | Required Recruiting access is denied | Restore authorized access; do not substitute another route |
| Fusion process | FSM or Core Data Loader returns a failed, partial, timed-out, or uncertain result | Preserve diagnostics, reconcile, and stop before retry |
| Unsupported operation | Requested behavior is outside the verified contract | Remove or separately evidence the unsupported operation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Authoring package ready | Intended target and release, operation, exact natural keys, requested delta, preserved values, translations, associations, member inventory, source fingerprint, validation result, and reconciliation plan |
| Any validation or design failure | Task code and name, operation, failed Rule ID, exact sanitized issue, affected natural keys, and one safe correction |
| Failed or uncertain import | Process status, sanitized ProcessLog reference, confirmed and unverified objects, last known state, and required task-wide export reconciliation |
| Partial failure | Confirmed successful, failed, and unverified rows separately; never claim rollback or full success |
| Authorization failure | Required task access context without credentials, tokens, or alternative routes |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Package validation has not passed | Do not return the package as ready or invoke core.data-loader |
| A live mutation is requested from this task skill | Do not upload or submit directly; route the validated immutable handoff to core.data-loader |
| An import fails, times out, is partial, or is uncertain | Do not retry automatically or assume rollback; the migration service permits partial failures |
| A reference is absent or ambiguous | Do not select by position, use a case variant, create a dependency, or invent a value |
| CSV deletion or code rename is requested | Do not generate it; Draft deletion remains a separate authorized UI action |
| Translation values are incomplete | Do not invent text, Language, SourceLang, target base-language evidence, or omission semantics |
| Credentials or protected runtime material are present | Do not persist or disclose them in packages, diagnostics, project artifacts, or output |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSPRSN.VALIDATE_PACKAGE | decision | 60 | execution_gate | ready->CSPRSN.DONE_AUTHORING;invalid->CSPRSN.HANDLE_ISSUES;unsupported->CSPRSN.HANDLE_ISSUES | CSPRSN.CHECK_DESIGN | stop | A candidate FSM CSV package has been authored and must pass the immutable handoff gate |
| CSPRSN.HANDLE_ISSUES | step | 80 | error_handler | handled->CSPRSN.RETURN_ISSUES | none | stop | Any validation, identity, lookup, dependency, design, package, authorization, process, or verification issue |
| CSPRSN.RETURN_ISSUES | terminal | 90 | terminal | none | CSPRSN.HANDLE_ISSUES | stop | An issue was safely classified and returned |
| CSPRSN.DONE_AUTHORING | terminal | 100 | terminal | none | CSPRSN.VALIDATE_PACKAGE | stop | A validated immutable authoring package and reconciliation plan are ready for the Core Data Loader handoff |
| CSPRSN.DONE_VERIFIED | terminal | 110 | terminal | none | CSPRSN.VERIFY_RESULT | stop | Supplied post-import evidence was reconciled with the intended delta and preserved baseline |
