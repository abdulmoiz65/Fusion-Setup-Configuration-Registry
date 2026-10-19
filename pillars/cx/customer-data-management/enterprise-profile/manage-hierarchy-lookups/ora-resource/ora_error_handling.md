# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or ambiguous environment or target | Stop before the Fusion call and ask only for the missing identity. |
| 401 or 403 | Classify auth or authorization failure; do not report lookup absence. |
| 404 on exact code | Report absent code and stop before update or delete. |
| Duplicate exact code on create | Show current state and stop; never silently upsert. |
| Prohibited HZ_TREE_STATUS mutation | Stop before preview and explain the System restriction. |
| Hierarchy type authority is unavailable | Stop before create preview; report the missing authoritative evidence. |
| Mutation or import fails or is uncertain | Report the exact classified outcome and never automatically retry or replace it. |
| Task-local import route was selected | Stop before POST with `approval_blocker`; restart through Core Data Loader. |
| Task Hook validation envelope is absent, stale, or locally reconstructed | Stop before Core Data Loader upload or initiation with `approval_blocker`; rebuild validation and approval for the exact archive. |
| Core Data Loader or Task Hook is unavailable | Fail closed before upload or initiation; do not choose a task-local replacement route. |
| Cached-token authentication fails | Refresh once only when repository-managed cache policy applies; otherwise stop. |
| Export or import polling times out | Stop and report TaskCode, ProcessId, last status, elapsed time, and the safe next-check path; never submit a replacement automatically. |
| Registry or source anchor is stale | Stop and recompile or re-author; don't repair the graph at runtime. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required value, date, flag, code format, or ZIP identity is invalid | Correct locally and restart validation. |
| catalog_or_metadata_mismatch | Task, type, configuration level, describe, or CSV flag cannot be matched safely | Stop and review exact authoritative scope. |
| approval_blocker | Task Hook validation, exact archive SHA-256 binding, immutable preview, or separate approval is missing, stale, changed, or declined | Stop before Core Data Loader upload or initiation and restart validation and approval. |
| auth_expired_or_invalid | Fusion returns 401 or 403 for a cached session | Refresh cached authentication once when policy permits; otherwise stop. |
| authorization_or_privilege | Access remains denied or task-specific privilege is absent | Restore exact access; do not retry the operation. |
| transport_or_environment | Target, DNS, VPN, connection, or bounded read timeout fails | Retry only a read under shared policy; never retry a mutation. |
| fusion_api_error | Fusion rejects one approved request | Report the response summary and ECID when available, then stop. |
| process_timeout | Export or import exceeds the owning service wait window | Preserve ProcessId and resume by status check only. |
| process_failed | Export or import finishes with errors | Preserve ProcessLog or status payload and partial business-object results. |
| artifact_persistence | Required ZIP, validation, diagnostic, or run artifact can't be written | Preserve safe diagnostics temporarily and report the intended path. |
| approval_blocker | Immutable preview is not explicitly approved or is stale | Do not submit. |
| unverified_success | A write may have completed but verification failed | Reconcile with read-only GET; never repeat blindly. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read result | Environment, exact type or code, configuration level, values, and partial failures. |
| Mutation preview | Environment, method, exact target, before and after values, supported executor, impact, and approval request. |
| Import preview | Environment, exact task code, immutable archive SHA-256, metadata task identity, task-rule results, Task Hook envelope reference, expected impact, and separate approval fingerprint. |
| Failure | Environment, operation, target, failure class, redacted status, and one safe next action. |
| Timeout | TaskCode, ProcessId, last status, elapsed time, completed checks, and next-check guidance. |
| Durable diagnostic | Status, stage, failure class, message, recommended action, environment, artifact references, external IDs, and verified side effects. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unapproved mutation or import | Do not dispatch a write or data load. |
| Failed or uncertain mutation or import | Do not automatically retry it. |
| Unsupported hierarchy action | Do not create hierarchy definitions, versions, nodes, or hierarchy data through lookup maintenance. |
| Missing authoritative dependency or writable contract | Do not invent an endpoint, payload, source authority, or success claim. |
| Task-scoped FSM ZIP | Do not select an endpoint, adapter, routing field, or retry policy in this task skill. |
| Core Data Loader handoff | Require the current Task Hook validation envelope bound to the unchanged archive; never reconstruct it from preflight data. |
| Stale or changed preview | Do not reuse approval; regenerate the preview and request fresh approval. |
| Uncertain prior mutation | Do not submit compensation or replacement until a separate GET reconciles current state. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.EXECUTION_GATE | decision | 6 | execution_gate | ready->HL.READY;blocked->HL.RETURN_ISSUES | HL.DESIGN_GATE | stop | Confirm supported routing, validation, immutable preview, and approval requirements before handing off a read result, mutation, export, or import. |
| HL.READY | terminal | 7 | terminal | none | HL.EXECUTION_GATE | continue | The requested read or routed operation is validated and ready for its owning executor. |
| HL.RETURN_ISSUES | terminal | 8 | terminal | none | none | continue | Validation, lookup, dependency, design, routing, approval, or execution readiness is blocked. |
