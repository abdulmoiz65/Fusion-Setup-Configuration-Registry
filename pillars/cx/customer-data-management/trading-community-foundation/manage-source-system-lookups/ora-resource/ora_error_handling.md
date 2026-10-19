# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or ambiguous environment, task membership, category, type, or code | Stop before Fusion execution and request only the missing evidence. |
| 401 or 403 | Classify auth/authz; never report lookup absence or try another category. |
| Duplicate code on create | Show current state and stop; never upsert. |
| Unsupported System, Extensible, seeded, identity, module, tag, or field mutation | Refuse before preview. |
| Mutation or import fails or is uncertain | Report classified outcome; never automatically retry, compensate, or replace. |
| Core Data Loader Task Hook validation envelope is absent, stale, or locally reconstructed | Stop before Core Data Loader upload and initiation with approval_blocker; rebuild the immutable Data Loader preview and approval. |
| FSM ZIP would use task-local import route | Stop before POST with `approval_blocker`; restart through Core Data Loader. |
| Missing Core Data Loader Task Hook or validation envelope | Stop before POST with `approval_blocker`; do not choose a task-local route or reconstruct the envelope. |
| Export/import timeout or failure | Preserve TaskCode, ProcessId, last status, elapsed time, and ProcessLog/status evidence. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Invalid field, date, flag, code, task identity, or unsafe ZIP | Correct locally and restart validation. |
| catalog_or_metadata_mismatch | Task scope, category, level, describe, CSV flag, or metadata cannot be matched | Stop and reconcile authority. |
| approval_blocker | Task Hook validation or immutable-archive binding is missing, stale, ambiguous, or mismatched | Stop before submission and restart Core Data Loader validation; do not select a task-local fallback. |
| auth_expired_or_invalid | Cached session rejected | Refresh once only under repository cache policy. |
| authorization_or_privilege | Access remains denied | Restore exact access; do not retry side effect. |
| transport_or_environment | Environment/VPN/DNS/connection fails | Retry only bounded reads. |
| fusion_api_error | Fusion rejects the one approved request | Report status, response summary, and ECID, then stop. |
| process_timeout | Export/import wait expires | Preserve ProcessId and resume by status check only. |
| process_failed | Process completes with errors | Preserve ProcessLog/status and partial results. |
| artifact_persistence | Required artifact cannot be saved | Preserve safe temporary diagnostics and report intended path. |
| approval_blocker | Core Data Loader Task Hook validation envelope or exact archive SHA-256 binding is absent, or the immutable preview is missing, stale, changed, reconstructed, or declined | Stop before Core Data Loader upload and initiation and rebuild the exact Data Loader preview. |
| unverified_success | Write may have completed but separate GET failed | Reconcile with read-only GET; never repeat blindly. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read | Environment, exact task/type/code, category, level, values, evidence boundary, and partial failures. |
| Mutation preview | Environment, method, target, before/after, payload, impact, fingerprint, and approval request. |
| Import preview | Environment, HZ_MANAGE_SOURCE_SYSTEM_LOOKUPS, immutable ZIP hash, metadata identity, validation results, exact archive SHA-256 binding, Task Hook envelope reference, expected impact, and approval fingerprint. |
| Failure or timeout | Failure class, redacted status, safe next action, TaskCode, ProcessId/ECID, last status, elapsed time, and verified side effects as applicable. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSL.EXECUTION_GATE | decision | 6 | execution_gate | ready->SSL.READY;blocked->SSL.RETURN_ISSUES | SSL.DESIGN_GATE | stop | Confirm supported routing, immutable preview, approval, and retry restrictions. |
| SSL.READY | terminal | 7 | terminal | none | SSL.EXECUTION_GATE | continue | Request is validated and ready for its owning executor. |
| SSL.RETURN_ISSUES | terminal | 8 | terminal | none | none | continue | Validation, membership, dependency, design, Task Hook, approval, or execution readiness is blocked. |
