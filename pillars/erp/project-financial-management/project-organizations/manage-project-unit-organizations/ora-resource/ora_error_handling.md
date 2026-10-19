# Error Handling

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing name, externally selected action, invalid length or date, ambiguous selection, ineligible organization, or malformed HDL | Report the exact field or conflicting candidates and correct before generation |
| Catalog mismatch | Task, business object, metadata or loader mode differs | Correct routing; no substitution |
| Auth/authz | Lookup or loader authentication/privileges fail | Routed core policy may refresh cached token once; never expose credentials |
| Transport/environment | Target or read-only lookup unavailable | Retry only known recoverable read-only failure through core policy |
| Fusion API | Fusion rejects organization, classification or EFF | Preserve redacted Oracle message and correct input; no automatic write retry |
| Process timeout | An explicitly requested status check times out before terminal status | Return In Progress with target, task, request ID, last status, elapsed wait and next-check path under core reporting rules; wait for another explicit status request, never resubmit or automatically continue polling |
| Process failed | HDL load reaches a terminal failed or partial-success state | Persist status, counts and Data Loader diagnostics when available; stop without post-load verification or automatic resubmission |
| Tracking failure | Accepted initiation lacks a usable request ID or requested status cannot be authoritatively resolved | Treat the write as indeterminate and report the available server identity; require a later explicit recovery/status request through the declared route, never infer success or submit again |
| Post-load verification | Terminal load success is proven but classification or Project Unit attributes cannot be confirmed | Preserve the receipt and verification evidence, report the missing or mismatched state, and do not resubmit |
| Artifact persistence | Preparation, acceptance binding/registration, status evidence, run record, token usage or verification deliverable cannot be persisted | Stop with known server ID and saved partial evidence; repair the local handoff through declared project services without re-upload or resubmission; do not claim the accepted load failed |
| Approval blocker | Immutable preview missing, changed or declined; required route absent | Stop before external execution |
| Bulk validation | One or more rows invalid, missing a chosen code, lacking evidence, or duplicating names/codes within the request | Show all row outcomes and name-derived suggestions together; ask whether to accept each suggestion or enter a code; generate and import no archive until the whole batch passes |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, action, name, code, selected ID and exact existing classification when applicable, dates, eligibility evidence and conflicts |
| Bulk validation | Target and stable row numbers with each row's derived action, name, resolved code, evidence reference, and every encountered row issue; identify all blocked rows in one report |
| Import preview | Exact target, Organization business object, DAT contents, component counts, checksum, warnings and eligibility evidence |
| Import result | On accepted initiation, return only core's Data Load In Progress report with exact Data Set Name and Content ID(Request ID); on a later explicit status request use core's status, counts and actionable-error report |
| Post-load result | Exact organization identity, effective date, active PRJ_PROJECT_UNIT result, sequence-1 PRJ_PU_ATTRIBUTES result, exact requested code and verification evidence reference |
| Diagnostics | Persist minimal acceptance/status bindings, available redacted diagnostics, run records and token usage through declared core project services under the selected project. Preserve core's concise response and restrictions on unsolicited user-facing reports; follow ora_dependency_readiness.md#execution-persistence-and-resume-contract |

## Acceptance Persistence and Status Recovery

If receipt writing, registration, state update or run/token recording fails,
take persistence_failed to PUORG.RETURN_ISSUES. Preserve any saved partial
record and the known server ID, return the ID with an artifact-persistence issue,
and stop. Repair only the missing local handoff from retained acceptance and
approval evidence; do not re-upload, resubmit or claim the load failed merely
because local recording failed. Unknown acceptance requires read-only recovery
only on a later explicit request through the declared route. Binding prerequisites
remain in ora_dependency_readiness.md#execution-persistence-and-resume-contract.

On a later explicit status request, nonterminal status or timeout returns
In Progress and waits for another explicit request. Terminal failure stops
without post-load verification or resubmission. Terminal success permits the
declared classification/EFF verification using the durable receipt and original
row mapping.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous evidence | Do not generate DAT or silently select the first organization, classification, organizationClassificationsLOV label, or location match |
| User-selected action | Do not let an input action override the action derived from the exact-name organization search |
| Existing-organization action | Do not use the required Organization MERGE anchor to create or alter identity; emit only the exact selected REST start date, name and classification code plus the exact LOV label. OrganizationId remains lookup evidence only |
| Import fails or receipt is missing | Do not retry POST, loader or import without idempotency or explicit new approval; recover target state read-only through declared route |
| Initiation is accepted | Persist and register the local acceptance binding and record run/token usage, then return In Progress; do not query status, counts or errors, add user-facing reports, call it load completion, mark the task complete, or start post-load verification |
| Local acceptance persistence fails | Preserve the known request ID and partial records; do not return a normal initiated outcome, re-upload or resubmit. Repair local state before a later explicitly requested status check |
| Requested status is nonterminal or times out | Do not ask for another submission, change request ID, automatically continue polling, or convert a nonterminal/unknown result into success; resume the same request ID only on another explicit status request |
| Post-load verification fails | Do not report success or resubmit the archive; retain the receipt and investigate the observed state |
| Archive changes | Invalidate approval and return to exact preview through core.data-loader |
| Invalid bulk row | Do not silently exclude it, write an archive for valid rows, or begin a loader operation |

## Pre-Upload Task Hook Boundary

When Core Data Loader invokes its read-only Task Hook for the final immutable
Organization HDL archive, evaluate the applicable preparation rules against that
archive and its retained input/evidence context. At PUORG.EXECUTION_GATE, a
complete package with verified persisted preflight takes `prepared` to
PUORG.RETURN_PREPARED. Do not require upload approval, an accepted Request ID,
status or post-load evidence in this phase; do not initiate a load or mark those
later checks passed. Incomplete preparation still takes `not_initiated` to issues.

Return one ordered `ruleResults` entry per planned resource using the existing
Task Hook result contract; keep detailed evidence internal and do not construct
approval/envelope objects manually. Core Data Loader owns its subsequent preview,
approval, archive verification and submission. The outer task's submission stage
uses `initiated` only after actual acceptance and successful local persistence.
The existing explicit-status and post-load routes remain unchanged. This boundary
follows core/data-loader/SKILL.md's final-artifact Task Hook and approval workflow;
it supplies no standing approval or new execution route.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.EXECUTION_GATE | decision | 8 | execution_gate | prepared->PUORG.RETURN_PREPARED;initiated->PUORG.RETURN_IN_PROGRESS;persistence_failed->PUORG.RETURN_ISSUES;not_initiated->PUORG.RETURN_ISSUES;declined->PUORG.RETURN_REFUSAL | PUORG.ENFORCE_DESIGN | stop | Read-only pre-upload Task Hook: complete preparation and verified preflight return prepared without approval or submission. Outer submission: require immutable preview, core.data-loader approval, one accepted initiation with a nonblank request ID, and persisted/registered acceptance binding plus run/token records; persistence failure preserves the known ID and stops without resubmission. No status reads; never entered on status resume |
| PUORG.STATUS_REQUEST_GATE | decision | 9 | execution_gate | status_requested->PUORG.LOAD_COMPLETION_GATE;invalid->PUORG.RETURN_ISSUES | PUORG.VALIDATE_INPUT | stop | Require a later explicit status request and registered durable acceptance binding matching project, target, task, request ID, approved archive hash and approval reference; missing, unregistered or mismatched evidence blocks, and this route never prepares or submits a load |
| PUORG.LOAD_COMPLETION_GATE | decision | 10 | execution_gate | terminal_success->PUORG.VERIFY_POST_LOAD;terminal_failure->PUORG.RETURN_ISSUES;nonterminal->PUORG.RETURN_IN_PROGRESS;polling_timeout->PUORG.RETURN_IN_PROGRESS;indeterminate->PUORG.RETURN_ISSUES | PUORG.STATUS_REQUEST_GATE | stop | Only on a later explicit status request obtain authoritative status/count/diagnostic evidence through core.data-loader for the retained same-target request ID; nonterminal status or timeout returns In Progress and waits for another explicit request |
| PUORG.RETURN_CREATED | terminal | 12 | terminal | none | PUORG.VERIFY_POST_LOAD | continue | CREATE_NEW completed only after terminal load success and both post-load checks passed |
| PUORG.RETURN_EXISTING_DEFINED | terminal | 13 | terminal | none | PUORG.VERIFY_POST_LOAD | continue | USE_EXISTING_ORGANIZATION completed only after terminal load success and both post-load checks passed |
| PUORG.RETURN_ALREADY_PROJECT_UNIT | terminal | 14 | terminal | none | none | continue | Matching active organization is already a Project Unit; report it and generate no HDL |
| PUORG.RETURN_ISSUES | terminal | 15 | terminal | none | none | continue | Correctable blocker, terminal load failure, indeterminate tracking, or failed post-load verification |
| PUORG.RETURN_IN_PROGRESS | terminal | 16 | terminal | none | none | continue | Accepted initiation with registered local acceptance/run/token evidence ends the submission request without status reads; a requested nonterminal status or timeout also returns here after local status evidence recording. Task is not complete; resume the same request ID only on a later explicit status request |
| PUORG.RETURN_REFUSAL | terminal | 17 | terminal | none | none | continue | Unsupported operation or declined approval |
| PUORG.RETURN_PREPARED | terminal | 18 | terminal | none | PUORG.EXECUTION_GATE | continue | Read-only Task Hook preparation complete before loader approval; no submission, acceptance or post-load success is implied |
