# Error Handling

| Failure class | Condition | Required action |
|---|---|---|
| input_validation | Invalid headers, hierarchy, identifier or source path | Correct the source and rerun preparation/preflight |
| catalog_or_metadata_mismatch | Object/account/import support mismatch or unsupported create-only guarantee | Stop before preview; do not substitute a mode, account or route |
| auth_expired_or_invalid | Core authentication remains rejected after its permitted refresh | Restore authentication for the selected environment |
| authorization_or_privilege | Documents upload or native initiation access denied | Obtain the missing business capability; do not use SOAP as fallback |
| transport_or_environment | Network/callback/target access fails | Correct connectivity; retry only declared safe reads |
| artifact_persistence | Archive, preflight or Task Hook evidence cannot be retained | Stop before side effects; restore writable safe storage |
| approval_blocker | Missing/stale approval or uncertain upload/initiation | Preserve evidence and reconcile through a supported workflow |
| process_failed | Explicitly requested status reports failed rows/jobs | Use core Data Loader monitoring and error retrieval |
| process_timeout | A declared status operation times out | Report last known state and core next-check path; never resubmit |

`TG.PREFLIGHT` passes when all read-only task validation has completed against
the final immutable archive/preflight and that evidence can build a Task Hook
preview. It does not require a prior approval. `TG.READY` permits preview and
later approval, not upload. `TG.ISSUES` blocks preview/approval feedback until
findings are resolved or explicitly waived under core's rules.

Only core owns approval, upload, initiation, response reporting and permitted
retries. Never replay a POST or uncertain import, strip profile fields from a
historical preflight, erase a checkpoint, or infer a content reference. Retain
partial-upload evidence and stop before initiation if any member fails. A
legacy SOAP checkpoint requires a supported reconciliation procedure; this
native route does not resume it or authorize reupload.

Return core helper Markdown verbatim. No automatic polling or report download
follows accepted initiation. On an explicit status/results request, use core's
monitoring contract. Redact secrets, tokens, authorization codes, protected
payloads and raw responses from project diagnostics. Persist required pillar
failure/run evidence and token usage under the active project workspace.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TG.PREFLIGHT | decision | 7 | execution_gate | validated->TG.READY;blocked->TG.ISSUES | TG.DESIGN | stop | All read-only checks have passed against the final core archive and preflight; approval is not yet required. |
| TG.ERROR | step | 8 | error_handler | handled->TG.ISSUES | none | continue | Any preparation, task validation or core execution stage fails. |
| TG.READY | terminal | 9 | terminal | none | TG.PREFLIGHT | continue | Validation is complete; Task Hook may build a preview for later core-owned approval. |
| TG.ISSUES | terminal | 10 | terminal | none | none | continue | Unresolved validation or workflow uncertainty blocks preview and submission. |
