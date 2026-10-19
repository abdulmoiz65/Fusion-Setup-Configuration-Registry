# Error Handling

| Situation | Classification | Response |
|---|---|---|
| Missing/unreadable/empty/non-CSV source, duplicate basename, duplicate mapping, unresolved object code, or missing/ambiguous `ImportMode` | `input_validation` | Stop before side effects and report the exact transport or routing issue. |
| A supplied CSV has unknown, missing, extra, or reordered columns or unfamiliar row values | `not_a_local_error` | Preserve the exact bytes and continue; do not request a waiver. |
| Exact object import support or UCM routing is missing/ambiguous | `catalog_or_metadata_mismatch` | Stop before upload; do not infer a replacement. |
| `importExportObjectMetadata` omits the exact code or does not return `ImportSupport=Y` | `catalog_or_metadata_mismatch` | Do not retry or invent another code. |
| Cached-token 401/403 | `auth_expired_or_invalid` | Refresh once when eligible; stop if still rejected. |
| User reports changed access and the read-only object finder is empty | `auth_expired_or_invalid` | Force one fresh OAuth login and repeat only that read-only finder once. |
| Upload privilege is missing | `authorization_or_privilege` | Stop and report the required access; do not retry the POST. |
| UCM upload returns no usable response or content ID | `fusion_api_error` | Reconcile read-only by exact activity and content identity; do not retry the POST without a new exact-artifact approval. |
| Core CX upload/import outcome is uncertain or its UCM reference is not available yet | `approval_blocker` | Preserve the Core adapter's redacted result, use its read-only status route, and do not upload again without explicit recovery authorization. |
| DNS, VPN, timeout, or unavailable pod | `transport_or_environment` | Retry bounded read-only calls only. |
| Ordered CSV-group digest differs from approval | `approval_blocker` | Stop and rebuild the preview; never substitute archive verification. |
| Pre-approval CX preview is rejected because `--task-routed` requires an approved Task Validator envelope | `input_validation` | Rerun the non-mutating Core Data Loader preview without `--task-routed`. Reconcile its ZIP with the protected CX preview and use the adapter group digest to build the Task Hook preview, then request approval. |
| A pre-approval command attempts to use task routing | `input_validation` | Run the non-mutating Core Data Loader preview without `--task-routed`; do not create a transport wrapper. |
| Direct CSV approval uses a source-file/ZIP digest, or Core/CX file reconciliation fails | `approval_blocker` | Correct the differing files/order/target, rerun Core preflight and `prepare-import`, then use the skill-local reconciliation helper and adapter manifest group digest for Task Hook. Never request a waiver for an integrity mismatch. |
| Core Data Loader preflight and Task Hook approval cover the same unchanged target and digest | `not_an_approval_error` | Continue directly to the approved live rerun; do not ask for a second routine approval. |
| Preview/envelope omits or changes the exact `ImportMode`, activity name, or mode-aware adapter | `approval_blocker` | Invalidate approval and rebuild the complete preview. Never label a generic import as delete. |
| Generic Data Loader initiation is selected for Trading Community data | `catalog_or_metadata_mismatch` | Stop before upload because this route does not bind the documented CX Import Management `ImportMode`; use the mode-aware adapter after Data Loader authorization. |
| Adapter result omits `ImportMode` or reports a mode different from the approved value | `fusion_api_error` | Do not claim the requested operation succeeded. Preserve the activity ID and reconcile the exact activity before retrying or verifying records. |
| Parent import activity omits `Status` or counts | `not_a_status_failure` | Run the task-local status helper so it fetches `child/DataFiles` through the existing core REST client. Use the child status, counts, timestamps, and report content IDs; do not report status as unavailable from the parent-only response. |
| A terminal data-file result reports errors | `process_failed` | Report the exact activity ID, mode, status, read/loaded/error/warning/unprocessed counts, and available report content IDs. Attempt the declared report-retrieval route; if report download is unavailable, keep the failure visible and do not hide the counts or resubmit. |
| Mode-aware adapter cannot preserve the complete approved CSV group | `catalog_or_metadata_mismatch` | Record the workflow gap and stop; do not substitute generic `initiateDataLoad`. |
| Upload/import request is rejected | `fusion_api_error` | Preserve safe status, endpoint summary, ECID when present, and verified side effects; never auto-retry. |
| Fusion rejects CSV data during processing | `process_failed` | Retrieve and report the redacted Fusion business error from the CX Import error log, including when `dataSetErrors` is empty. Treat Fusion—not this skill—as the data validator. Loaded rows alone are not verification. A correction creates new bytes and requires a new preview and approval. |
| `HZ-120871` rejects a hierarchy structure | `process_failed` | Require direct evidence that the tree structure definition exists. If absent, defer Hierarchy, Hierarchy Member, and Party Hierarchy Generation and route `ORA_HZ_MANAGE_TREE_STRUCTURES` before `HZ_MANAGE_HIERARCHY_TYPES`. |
| A Hierarchy or Hierarchy Member `DELETE_RECORD` activity is unavailable or rejected | `catalog_or_metadata_mismatch` or `process_failed` | Preserve Fusion's sanitized metadata or process diagnostic, do not retry, and let the user correct the source or choose a separately authorized workflow. |
| A supplied Hierarchy or Hierarchy Member delete lacks locally verified row identity | `not_a_local_error` | Preserve the CSV bytes unchanged and continue through the approved pass-through route; Fusion Import Management validates the rows. |
| Optional post-import verification still finds the hierarchy or member | `unknown_requires_reconciliation` | Report the activity and remaining exact match, and do not resubmit automatically. |
| An Additional Identifier delete activity loads rows but the exact parent-scoped `PartyIdentifierId` still resolves | `process_failed` | Report the activity and remaining exact match, classify the outcome as `unknown_requires_reconciliation`, and do not resubmit automatically. |
| Import submission outcome is indeterminate | `fusion_api_error` | Reconcile the exact activity and uploaded content by read-only calls before any retry. |
| Polling expires | `process_timeout` | Report environment, object, activity/request ID, last status, elapsed wait, and read-only next-check path. |
| Cannot persist safe output | `artifact_persistence` | Preserve diagnostics in a safe temporary location and report the intended path. |

Never print or persist credentials, tokens, raw customer rows, or full encoded
payloads. Never retry a live upload or initiation without idempotency or fresh
explicit approval. A delayed UCM document-name lookup is a read-only
reconciliation condition; it is never authorization to replay the upload.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.APPROVAL | decision | 6 | execution_gate | ready->TCA.READY;blocked->TCA.RETURN_ISSUES | TCA.DESIGN_GATE | stop | Bind execution approval to the exact target, `ImportMode`, activity, adapter, and ordered CSV-group digest. |
| TCA.READY | terminal | 7 | terminal | none | TCA.APPROVAL | continue | The request is ready for the owning core executor. |
| TCA.RETURN_ISSUES | terminal | 8 | terminal | none |  | continue | Transport, routing, metadata, integrity, or approval is blocked. |
