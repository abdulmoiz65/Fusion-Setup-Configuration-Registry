# Error Handling and Execution Gate

## Failure Handling

| Failure Class | Detection | What Happens | Retry Rule | User Guidance |
|---|---|---|---|---|
| Input validation | Unsupported operation, unsafe identity, invalid flags/dates/sequence, unsupported fields, or incomplete preview | Stop before side effect and return field-level issues | Retry after corrected input and fresh validation | Correct named fields |
| Scope mismatch | Set ID type, non-standard lookup category, or lookup-type mutation | Stop this task | Do not retry in this graph | Use the correct owning task |
| Authentication/authorization | 401/403 or missing management privilege | Stop; never classify as not_found | Allow only shared cached-token behavior; never task-level write retry | Restore access |
| Transport/environment | DNS, TLS, timeout, wrong host, or environment mismatch | Stop with sanitized context | Retry reads only after recoverable condition is established | Verify target/connectivity |
| Fusion API read | Non-success GET, malformed response, cardinality, or pagination failure | Stop the affected graph | No speculative retry | Correct request or privileges |
| Export omission/failure | Inventory/Review export lacks a type or fails | Disclose and continue exact live reads | Not a mutation blocker or retry trigger | Use live Apps Common evidence |
| Duplicate code | AddCode finds an exact code | Stop before preview | Choose a different code or Review existing item | Review duplicate |
| Ambiguous result | Multiple exact items or inconsistent identity | Stop before preview | Never choose automatically | Resolve canonical item |
| Stale state | Immediate pre-write read differs from approved expected state | Invalidate preview/approval | Re-read and build a new preview | Review changed state |
| Delivered/custom uncertainty | RemoveCode cannot positively prove customer-created ownership | Refuse DELETE and offer DisableCode | Do not retry without new positive evidence | Use non-destructive alternative |
| Approval blocker | Approval is missing or not bound to complete digest | Return immutable preview without execution | Require a new exact approval | Approve exact preview |
| Apps Common write | POST/PATCH/DELETE returns error | Preserve method, sanitized path, HTTP outcome, request ID/ECID, and message; stop | Never retry automatically | Correct request/state before new preview |
| Indeterminate write | Transport fails after possible submission | Re-read exact code before any further action | Never replay automatically | Reconcile current state |
| Verification mismatch | Exact post-write read differs from approved change | Report mismatch and stop | No automatic compensation | Investigate current result |
| Partial bulk completion | A row fails after earlier verified successes | Stop and report successful, failed, and unattempted rows | No rollback or continuation | Submit a new request for remaining rows |
| Route bypass | FSM, Data Loader, setup import, browser, curl, or task-local HTTP is proposed | Stop before call | No fallback | Use core.fusion-api.apps-common |
| Artifact persistence | Required durable artifact cannot be written | Stop dependent side effects | Retry after path/storage correction | Restore project path |

## Disclosure Rules

Every mutation preview/result identifies environment, task code, exact type and
code, source classification, operation, method, relative endpoint, current
state or absence, proposed delta, availability/translation/delete impact,
minimal body or bodyless delete, preview digest, approval state, HTTP outcome,
and exact verification. Redact credentials, tokens, secret headers, and
unneeded protected identifiers.

Inventory discloses documented/export-only candidate lists, attempted/resolved/
not-found/error counts, and one status plus complete code pagination per
candidate. Review discloses exact type/code, export attempt, live attributes,
translations when requested, and timestamps.

## Refusal Rules

- Do not create or modify task-local, core, or shared scripts.
- Do not return export rows as the complete environment inventory.
- Do not mutate lookup type definitions or translation resources.
- Do not fuzzy-match type/code identity or treat 401/403 as absence.
- Do not send audit, module, ownership, immutable key, BOSS, or unsupported
  fields.
- Do not DELETE without positive customer-created evidence and impact review.
- Do not POST/PATCH/DELETE without a complete digest-bound approval and
  immediate stale-state read.
- Do not use FSM, Data Loader, setup import, browser automation, direct curl, or
  task-local HTTP for code mutations.
- Do not retry or compensate automatically.

## Execution Routing

| Condition | Outcome | Terminal |
|---|---|---|
| Inventory or Review passes completeness gates | Return verified read-only result | SLL.READY_READ_ONLY |
| AddCode, UpdateCode, DisableCode, safe RemoveCode, or BulkSet has exact live state and complete preview | Return Apps Common CRUD preview for standalone approval and execution | SLL.READY_APPS_COMMON |
| Translation/type mutation, unsafe RemoveCode, or any gate failure | Return classified issues with no write | SLL.RETURN_ISSUES |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLL.EXECUTION_GATE | step | 6 | execution_gate | read_only_ready->SLL.READY_READ_ONLY;apps_common_ready->SLL.READY_APPS_COMMON;blocked->SLL.RETURN_ISSUES | SLL.DESIGN | stop | Route Inventory/Review to read-only output or validated lookup-code mutations to an exact Apps Common preview; block unsafe delete, translation/type mutation, stale state, missing approval, or any FSM/Data Loader route |
| SLL.READY_READ_ONLY | terminal | 7 | terminal | none | SLL.EXECUTION_GATE | continue | Inventory or Review is complete with live reconciliation and no side effect |
| SLL.READY_APPS_COMMON | terminal | 8 | terminal | none | SLL.EXECUTION_GATE | continue | Exact lookup-code CRUD preview is ready for standalone digest-bound approval and one non-retried Apps Common call followed by exact verification |
| SLL.RETURN_ISSUES | terminal | 9 | terminal | none | none | continue | Any validation, dependency, scope, lookup, design, approval, execution, persistence, or verification gate fails safely |
