# Complete Primary to Secondary Ledger Mapping Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required or conditional intake missing | Name the exact field, trigger, primary and secondary scope, and affected path; block only that path |
| Successful resolver returns zero | Report unknown or ineligible with raw value, endpoint or export source, exact filter/key, and match count zero |
| Resolver returns many | Report ambiguity with candidate business keys and require a precise selection |
| HTTP, auth, authorization, client, timeout, or malformed response | Report the actual failure class and diagnostics; never convert it to value not found |
| GL-781805 same-COA warning | Show the exact warning consequence, require an accountable accept or cancel decision, and keep Name4 blank on accept |
| GL-781342 different-currency failure | Show source currency, target currency, missing or invalid rate type, and the exact corrective choice needed |
| Cross-field mismatch | Show every compared value, relationship key, and violated rule, including direction, currency, conversion level, and parent OrgId |
| Package member, header, alias, scope, release, or manifest mismatch | Reject before ZIP authoring or import and list every mismatch |
| FSM validation or import failure | Capture request/process identity, business object, row semantic key, exact message, stage, timestamps, error file availability, and partial successes; retrieve ProcessLog/status payload when available |
| Process timeout | Stop and report environment, operation, task or job, ProcessId or requestId, last status, elapsed wait, and next-check path |
| Re-export mismatch | Keep Review readiness blocked and show missing relationship/rule/BSV changes, alias asymmetry, wrong parent state, unrelated mutation, or only-metadata change |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing, invalid, overlength, ambiguous, or conditionally required business input | Correct input and revalidate |
| catalog mismatch | Task, member, header, field, code, mapping, or role does not match current authoritative evidence | Refresh the exact export or catalog evidence and rebuild |
| auth or authz | Final 401/403 or insufficient endpoint, export, UI, or import privilege | Refresh cached token once when eligible, then obtain correct access or use the named UI handoff |
| transport or environment | Timeout, 429, 5xx, client, network, malformed response, or wrong environment | Retry only eligible read-only GET with bounds or correct environment; never submit a write blindly |
| Fusion API | Fusion rejects a lookup, validation, or process request | Preserve code/message/correlation evidence and correct the contract or input |
| process timeout | Process has no known terminal state within the polling budget | Do not resubmit; continue checking the same identity |
| process failed | Terminal import or validation failure | Retrieve object errors/logs, preserve partial successes, correct cause, and obtain a new preview approval before retry |
| artifact persistence | ZIP, receipt, preview, error file, or re-export could not be persisted safely | Stop and repair the project artifact path without exposing credentials |
| approval blocker | Preview changed, approval absent, UI handoff incomplete, warning undecided, or Review boundary reached | Stop before live import or Review and Submit |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import | Exact environment/release/task/scope; baseline provenance/checksum; resolver receipts; every member checksum; row-level add/update/delete and parent-key changes; alias/header/manifest checks; warnings; handoffs; exclusions; approval identity |
| During import | Process name and request identity; submitter; timestamps; total/completed/error object counts; per-object status; error-file availability; current terminal stage |
| After import | Fresh identical-scope export receipt and checksum; semantic before/after and raw comparison; service-generated IDs/defaults; relationship/rule signatures; status; unrelated-row changes |
| Resolver failure | Raw and normalized value, endpoint or export source, filter/key, requested fields, match count when available, HTTP/client/correlation details, and safe remediation |
| Timeout or unknown status | Original process identity, last known state, elapsed wait, next-check path, and explicit no-resubmit warning |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No exact current package | Do not author a ZIP from memory, an unrelated export, a sample inventory, or a previous-release manifest |
| Ambiguous or failed resolver | Do not select the first/fuzzy result or relabel transport/auth failure as not found |
| Optional feature lacks exact safe contract | Do not block the baseline unnecessarily or synthesize fields; preserve/disable it and record the exact UI handoff plus required re-export |
| Live side effect lacks checksum-bound approval | Do not import, activate, enable conversion, open periods, or invoke Review and Submit |
| Import request was submitted | Do not auto-retry POST/import or resubmit until its identity and terminal state are known; require idempotency or a new explicit approval |
| Credentials or sensitive data are present | Do not persist tokens, secrets, private keys, customer data, or sensitive payloads in resources, diagnostics, packages, or project artifacts |

## Re-export Verification

| Check | Pass Condition |
|---|---|
| Scope | Fresh export matches the same environment, release, task, and accounting-configuration scope |
| Relationship | Expected Name4/rate/OrgId/flags are present and lifecycle enablement remains unchanged |
| Rules | Every preserved semantic row remains; any controlled catch-all is exact; child parent aliases match the relationship; no synthesized Subledger row |
| BSV conversion | Only approved exact effective rows exist with SourceSegmentValue and Meaning; header-only remains header-only when feature was not selected |
| Package closure | Both aliases, headers, unchanged rows, header-only members, and manifest graph remain intact |
| Noise handling | Audit values, generated IDs, process metadata, timestamps, and request IDs are classified as expected service noise, not authored defaults |
| Proof threshold | A metadata-only change is not evidence of business persistence; any unexplained unrelated delta fails verification |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLMAP.ERROR_POLICY | step | 60 | error_handler | handled->GLMAP.PREVIEW_GATE | GLMAP.ENFORCE | stop | Preview and execution errors must use the classified policy |
| GLMAP.PREVIEW_GATE | decision | 70 | execution_gate | approved->GLMAP.READY;issues->GLMAP.RETURN_ISSUES | GLMAP.ERROR_POLICY | stop | Exact preview is complete |
| GLMAP.READY | terminal | 80 | terminal | none | GLMAP.PREVIEW_GATE | continue | Import and re-export workflow may proceed under separate approved shared/core execution |
| GLMAP.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Validation, dependency, lookup, design, preview, or approval issues remain |
