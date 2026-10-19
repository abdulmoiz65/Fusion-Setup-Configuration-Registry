# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Role identity/seeded state invalid | Stop with role identity and cardinality/protection state |
| Enterprise role invalid | Stop with supplied value, match count, role types, and effective state |
| Qualification capability/row invalid | Stop with PM flag and exact conflicting child rows |
| Active-use/access conflict | Stop with operation and affected assignment/request/access counts |
| Package/import fails | Follow core.data-loader's Markdown failure report and identifier-disclosure policy; do not retry or create automatic failure files |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Missing/invalid identity, dates, child fields or required evidence; unsafe paths | Correct exact input or supply missing evidence |
| catalog_or_metadata_mismatch | Task/target/catalog/header/member/wrapper mismatch | Reconcile current target contract before preparation |
| auth_expired_or_invalid | Cached token rejected with 401/403 | Use the delegated client's one authorized refresh; no task-local auth |
| authorization_or_privilege | Missing read privilege or 403 after refresh | Stop and request target privilege/access correction |
| transport_or_environment | Unreachable target, failed/incomplete pages or wrong environment | Report failed read stage; do not infer absence or reuse stale identity evidence |
| fusion_api_error | Oracle business/API error or inconsistent returned identity/model | Report redacted message and recommended correction; revalidate contract |
| process_timeout | Explicitly requested export/status exceeds delegated timeout | Report operation, last status, elapsed wait and next-check path; do not initiate again |
| process_failed | Delegated export/import reports failed/partial processing | Preserve partial-success knowledge, disclose failed stage and reconciliation next action; no replay |
| artifact_persistence | Task-owned planning/validation artifact cannot be saved | Report intended safe destination; do not claim a durable result |
| approval_blocker | Loader preview absent, changed or declined | Stop; use loader's fresh preflight/approval workflow |

## Task-Owned Diagnostic Contract

Outside delegated Data Loader execution, use the declared project validation
and run locations and existing schemas. A validation-result finding contains
severity, message, artifact and recommended_action. Include stage, standard
failure class, target alias, operation and a redacted cause in message; link
sanitized evidence using artifact. A skill-run uses status=failed for failure,
notes for that summary, and artifact_refs for the validation result. Do not add
undeclared failure_class, errors or partial status fields to these schemas.
List partial successes and errors as separate findings; never mark a partially
verified request completed. Keep credentials, tokens, payloads and protected
identifiers out of durable records and disclose only identifiers the delegated
workflow permits.

Delegation takes precedence: core.data-loader forbids automatic result/failure
files, logs and run records and terminates after accepted initiation. Keep its
failure details in the requested Markdown response; save a specific file only
when the user explicitly requests it. Do not create a pillar record as a
workaround. Retrieve status/logs only on an explicit status/results request,
using the loader's client, timeout and redaction rules. Accepted initiation is
in progress; reconciliation against a fresh task export is a separately
requested verification step, never an automatic second import.

## Disclosure Rules

The task graph is a read-only validation/preparation graph, including when
called as the loader's Task Hook. RETURN_SUCCESS must be reachable before
upload approval; it does not test or supply that approval. EXECUTION_GATE
checks completion of task validation and the immutable preparation handoff.
Only core.data-loader checks its pending preview/envelope and authorizes
submission afterward. A task-local approval or this terminal cannot replace
the loader's approval. A changed package requires fresh task validation and
loader preflight. The declined graph outcome is reserved for a declined task
preparation request, not a duplicate loader approval prompt.

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, role, seeded/use state, enterprise-role resolution, PM flag, dates, child findings |
| Preview | Before/after base fields, explicit qualification/translation rows, removals, impact, checksum |
| Result | Exact requested stage: validated/prepared, loader initiation accepted (in progress), or explicitly requested status/verification. Follow delegated disclosure rules; show verification counts only after actual reconciliation |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous/seeded/capability unknown | Do not guess or mutate |
| Unsafe access/use impact | Do not end-date/remove association/child |
| Direct setup REST/delete | Do not infer support |
| Template/approval absent | Do not import |
| Failure | Do not retry/claim success |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.EXECUTION_GATE | decision | 8 | execution_gate | ready->PROLE.RETURN_SUCCESS;not_ready->PROLE.RETURN_ISSUES;declined->PROLE.RETURN_REFUSAL | PROLE.ENFORCE_DESIGN | stop | Return completed validation/preparation; loader owns later submission approval |
| PROLE.RETURN_SUCCESS | terminal | 9 | terminal | none | PROLE.EXECUTION_GATE | continue | Task validation/preparation complete; does not authorize submission or certify import completion |
| PROLE.RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Correctable issue |
| PROLE.RETURN_REFUSAL | terminal | 11 | terminal | none | none | continue | Unsupported/unsafe/declined action |
