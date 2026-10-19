# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing environment, membership, category, type, or code | Stop and request only missing evidence. |
| 401 or 403 | Classify auth/authz; never report lookup absence or try another category. |
| Disallowed field, seeded target, duplicate create, or stale preview | Refuse before mutation; never upsert or retry automatically. |
| Missing Task Hook/hash approval | Stop before upload with `approval_blocker`; rebuild through Core Data Loader. |
| Process timeout/failure | Preserve TaskCode, ProcessId, last status, elapsed time, and ProcessLog/status. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Invalid field/value/identity or unsafe ZIP | Correct and restart validation. |
| catalog_or_metadata_mismatch | Membership, category, level, describe, task, or CSV flag cannot be proven | Reconcile authority. |
| auth_expired_or_invalid | Cached authentication rejected | Refresh once under repository policy. |
| authorization_or_privilege | Access remains denied | Restore exact access; do not retry side effect. |
| transport_or_environment | Environment/VPN/DNS/connection fails | Retry only bounded reads. |
| fusion_api_error | Fusion rejects one approved request | Report status/ECID and stop. |
| process_timeout | Polling expires | Preserve ProcessId; resume by status check only. |
| process_failed | Process completes with errors | Preserve ProcessLog and partial results. |
| artifact_persistence | Artifact cannot be saved | Report intended path and safe diagnostics. |
| approval_blocker | Preview/approval/envelope/hash binding missing or stale | Rebuild immutable preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.ERROR | step | 80 | error_handler | disclosed->CHC.RETURN_ISSUES | none | stop | Any blocked gate. |
| CHC.READY | terminal | 90 | terminal | none | CHC.ENFORCE | continue | Validated and ready for owning executor. |
| CHC.RETURN_ISSUES | terminal | 99 | terminal | none | CHC.ERROR | continue | Classified issues returned without unsafe side effect. |
