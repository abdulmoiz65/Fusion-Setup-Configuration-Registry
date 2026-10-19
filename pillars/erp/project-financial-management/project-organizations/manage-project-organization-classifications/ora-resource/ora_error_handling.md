# Error Handling

**Omitted classification input means preserve existing state.**

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing/failed/incomplete/ambiguous/inactive/conflicting REST result | Stop before artifact generation; never infer a new classification from export |
| New PTO permissions omitted | Default each omitted flag N; no export or existing-value check |
| Unsupported supplied permission | Reject the field; do not silently interpret arbitrary wording |
| Existing PTO permission update | Legacy single request with supplied permissions, or bulk with update_existing_pto_permissions=true and supplied permissions: write only those normalized values and require original identity. Bulk without opt-in preserves existing PTO and bypasses update-key requirements; never compare old flags |
| Existing update identity missing | Report original HDL key blocker; do not fabricate a key or create a duplicate classification |
| No explicit mutation | Return ALREADY_CONFIGURED; no DAT/ZIP or mutation approval |
| Confirmed missing new-component owner | Separately preview/approve creation; existing owner absence never authorizes creation |
| Load failed/timed out/uncertain | Preserve same request ID and redacted diagnostics; no replay |
| Bulk entry fails readiness | Name the organization/index and block all package generation; do not silently omit the failed entry |
| Incompatible PTO update columns | Block before writing; explain compatible explicit fields or separate compatible requests; never fill omitted existing values |
| One bulk ZIP succeeds and another fails | Persist separate checksums/request IDs and verified partial success; no replay of either accepted request; do not claim task completion |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Invalid supplied field or REST state | Correct named input/state |
| Catalog mismatch | Task/schema contract mismatch | Resolve supported target metadata |
| Auth/authz | Declared read/load denied | Core auth policy; no write replay |
| Transport/environment or Fusion API | Read/load fails | Persist safe diagnostics and reconcile |
| Process timeout/failed | Nonterminal timeout or terminal failure | Resume known ID or investigate |
| Artifact persistence | Mapping/receipt/archive unavailable | Stop dependent mutation |
| Approval blocker | Preview absent/changed/declined | No mutation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Target, REST-confirmed classification existence, explicit new rows, supplied/defaulted new values, partial existing changes, original update identity, preserved fields, DAT/ZIP/checksum |
| Result | Request ID, terminal/status evidence, actual changed/preserved state, separate maintenance handoff |
| No-op | No explicit mutation; existing state preserved; no artifact |
| Existing update blocker | Missing authoritative information identity, not a missing old permission value |

## Artifacts, Approvals and Recovery

Keep registered preparation/approval, acceptance ID, immutable checksum and diagnostics through declared core project services. Core Data Loader owns Task Hook and exact-artifact approval. Submit once, persist each accepted request-to-archive binding and return In Progress without polling or post-load reads. A persistence failure retains the known request ID and stops without resubmission. Only a later explicit status/results/verification request may resume the matching saved project, target, task, role, request ID and approved archive checksum through the core status workflow. Missing or mismatched binding blocks that resume. An active status or bounded timeout returns In Progress and waits for another explicit request; terminal failure stops before readback. After terminal success, run requested post-load verification; a fresh governed task export may verify permissions but never supplies pre-import flag values. No mutation uses FSM import.

## Source Owner Creation

Only confirmed missing owners for new components use the existing core Apps Common Lookups route: type/privilege preflight, exact payload preview and separate approval, one POST and re-read. No type creation, silent enablement or repeated write. Existing original update owner absence blocks.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing new PTO permission input | No permission export; default N |
| REST shows existing classification | No duplicate row |
| Existing update | No fabricated identity, permission comparison or unrequested columns |
| No-op | No mutation artifact or loader call |
| Failure/timeout/uncertainty | No automatic replay |
| Maintenance follow-up | No implicit other-task ESS invocation |
| FSM | Read-only post-load verification/optional existing registered identity only; never FSM import |

## Pre-Upload Task Hook Boundary

Core Data Loader's read-only Task Hook evaluates the final immutable role ZIP
and retained request/evidence context before upload approval. Complete applicable
preparation and verified persisted preflight take PORGCLASS.EXECUTION_GATE's
`prepared` outcome to PORGCLASS.RETURN_PREPARED. Do not require approval, acceptance
or post-load evidence, perform a mutation, or mark later lifecycle checks passed.
Incomplete preparation takes the existing failure outcome to issues.

If a source owner is absent during this phase, PORGCLASS.OWNER_CREATION_GATE
returns failure without POST, recheck or approval prompt. The outer workflow's
separately approved missing-owner creation remains available before artifact
preparation; it is never a Task Hook fallback. Original update-owner absence
continues to block.

Return one ordered `ruleResults` entry per planned resource under the existing
Task Hook contract; keep detailed evidence internal and do not manually construct
approval/envelope objects. Data Loader owns subsequent preview, approval, archive
verification and submission. Actual accepted submission and registered per-ZIP
binding alone permit `initiated`; later explicit status/readback routes remain
unchanged. This follows core/data-loader/SKILL.md's final-artifact Task Hook and
approval workflow, without a new execution route or standing approval.

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.OWNER_CREATION_GATE | decision | 8 | execution_gate | submitted->PORGCLASS.RECHECK_SOURCE_OWNER;uncertain->PORGCLASS.RECHECK_SOURCE_OWNER;declined->PORGCLASS.RETURN_REFUSAL;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.VERIFY_SOURCE_OWNER | stop | Outer workflow only: runbook validates and authorizes exact missing-code POST; gate does not itself write. During read-only pre-upload Task Hook, an absent owner returns failure without mutation or approval prompt |
| PORGCLASS.EXECUTION_GATE | decision | 13 | execution_gate | prepared->PORGCLASS.RETURN_PREPARED;initiated->PORGCLASS.RETURN_IN_PROGRESS;persistence_failed->PORGCLASS.RETURN_ISSUES;declined->PORGCLASS.RETURN_REFUSAL;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.ENFORCE_DESIGN | stop | Independently per nonempty PEO/PTO ZIP: read-only Task Hook returns prepared after complete preparation and verified preflight, before approval or submission. Outer workflow retains core immutable approval, submit once and registered role/checksum/request ID; persistence failure preserves known ID without replay; no status reads; no-op has no gate |
| PORGCLASS.STATUS_REQUEST_GATE | decision | 14 | execution_gate | status_requested->PORGCLASS.LOAD_COMPLETION_GATE;invalid->PORGCLASS.RETURN_ISSUES | PORGCLASS.VALIDATE_INPUT | stop | Require a later explicit status/results/verification request and registered acceptance binding matching project, target, task, role, request ID and approved archive checksum; do not prepare, approve or submit again |
| PORGCLASS.LOAD_COMPLETION_GATE | decision | 15 | execution_gate | terminal_success->PORGCLASS.VERIFY_POST_LOAD;terminal_status->PORGCLASS.RETURN_STATUS;in_progress->PORGCLASS.RETURN_IN_PROGRESS;polling_timeout->PORGCLASS.RETURN_IN_PROGRESS;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.STATUS_REQUEST_GATE | stop | Only on the explicit resume request use core status/count/error checks for each saved ID; terminal_status is successful status-only completion without target reads; terminal_success requires requested verification; retain partial success and never replay |
| PORGCLASS.RETURN_CLASSIFIED | terminal | 17 | terminal | none | PORGCLASS.VERIFY_POST_LOAD | continue | Requested post-load verification proves state and preservation; all requested ZIPs verified before task completion; disclose separate maintenance follow-up |
| PORGCLASS.RETURN_ALREADY_CONFIGURED | terminal | 18 | terminal | none | PORGCLASS.ROUTE_OPERATION | continue | No explicit permission update and no requested missing classification; preserve omitted state without mutation artifact or writes; never compare existing flags to claim a matching-value no-op |
| PORGCLASS.RETURN_IN_PROGRESS | terminal | 19 | terminal | none | none | continue | Accepted initiation or requested active/timed-out status; retain receipt and last state; wait for another explicit request without automatic calls |
| PORGCLASS.RETURN_STATUS | terminal | 20 | terminal | none | PORGCLASS.LOAD_COMPLETION_GATE | continue | Return the explicitly requested successful load status/counts/errors; no setup-verification or task-completion claim |
| PORGCLASS.RETURN_ISSUES | terminal | 21 | terminal | none | none | continue | Correctable failure, incomplete evidence or uncertain outcome |
| PORGCLASS.RETURN_REFUSAL | terminal | 22 | terminal | none | none | continue | Unsupported or declined action |
| PORGCLASS.RETURN_PREPARED | terminal | 23 | terminal | none | PORGCLASS.EXECUTION_GATE | continue | Read-only final-ZIP preparation complete before loader approval; no submission, acceptance, readback or task-completion claim |
