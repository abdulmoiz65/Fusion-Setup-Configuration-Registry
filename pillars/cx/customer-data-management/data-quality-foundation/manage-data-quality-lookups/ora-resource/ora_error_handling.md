# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing environment, membership, category, type, or code | Stop before Fusion execution and request only missing evidence. |
| 401 or 403 | Classify auth or authorization; never report absence or try another category. |
| Disallowed field, seeded target, duplicate create, or stale preview | Refuse before mutation; never upsert or automatically retry. |
| Missing or stale Task Hook/hash approval | Stop before upload with `approval_blocker`; rebuild through Core Data Loader. |
| Export/import timeout or failure | Preserve TaskCode, ProcessId, last status, elapsed time, and ProcessLog/status evidence. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Invalid field, value, identity, or unsafe ZIP | Correct locally and restart validation. |
| catalog_or_metadata_mismatch | Membership, category, level, describe, task identity, or CSV flag cannot be proven | Stop and reconcile authority. |
| auth_expired_or_invalid | Cached authentication is rejected | Refresh once under repository policy. |
| authorization_or_privilege | Access remains denied | Restore exact access; do not retry side effect. |
| transport_or_environment | Environment, VPN, DNS, or connection fails | Retry only bounded reads. |
| fusion_api_error | Fusion rejects one approved request | Report status and ECID, then stop. |
| process_timeout | Export/import wait expires | Preserve ProcessId and resume by status check only. |
| process_failed | Process completes with errors | Preserve ProcessLog/status and partial results. |
| artifact_persistence | Required artifact cannot be saved | Report intended path and preserve safe diagnostics. |
| approval_blocker | Preview, approval, Task Hook envelope, or archive-hash binding is missing/stale | Rebuild the immutable preview before execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.ERROR | step | 80 | error_handler | disclosed->DQL.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, design, approval, or execution-readiness failure. |
| DQL.READY | terminal | 90 | terminal | none | DQL.ENFORCE | continue | Request is validated and ready for its owning executor. |
| DQL.RETURN_ISSUES | terminal | 99 | terminal | none | DQL.ERROR | continue | Classified issues are returned with no unsafe side effect. |
