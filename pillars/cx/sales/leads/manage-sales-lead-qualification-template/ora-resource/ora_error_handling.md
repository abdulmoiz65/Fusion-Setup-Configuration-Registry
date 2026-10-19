# Error Handling and Execution Boundary

Source basis: Oracle Fusion Cloud Sales documentation for qualification-template
creation, task-level CSV export/import, and the Assessment Templates read-only
REST endpoint.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required implementation input is missing or invalid | Stop and return only the missing or invalid fields |
| Export create response contains ProcessId in a nested items collection | Read SetupTaskCSVExportProcess.items[0].ProcessId; reject missing, nonnumeric, or multiple unexpected process identities |
| Export remains NOT_STARTED or does not complete before the poll deadline | Stop and report environment, task code, ProcessId, last status, elapsed wait, and the exact next-check path; do not create another export automatically |
| Export process fails | Retrieve and persist the sanitized process log/status payload and stop |
| Export FileContent is not a valid task ZIP | Stop before inventory or package generation and report the failed integrity, member, metadata, environment, release, scope, or header check |
| Create resolves a duplicate exact Lead template name | Stop and require a new name or an explicit Copy operation |
| Exported inventory and live lookup disagree | Stop, classify the evidence as stale or incomplete, and require a fresh export before another create decision |
| Exact-name lookup returns no target for Copy, Review, or Deploy | Stop and ask for the correct template identity |
| Exact-name lookup returns more than one Lead template | Stop and ask for a narrower business-unit context |
| Question weights do not total 100 | Stop before deployment readiness and return the calculated total |
| Deployment-readiness validation finds errors | Preserve the error summary, correct the template design, and rerun read-only validation; do not attempt deployment |
| A deployed template needs a locked attribute changed | Refuse direct-edit guidance and require a copy |
| Read-only REST lookup fails | Classify the failure, disclose safe diagnostics, and stop before retry |
| Import is requested before Data Loader builds and receives standalone approval for its exact immutable preview | Stop before upload and return the Data Loader approval requirement |
| A task FSM ZIP is routed to shared.setup-import.task-level-import, setupTaskCSVImports, UCM, or an initiation endpoint outside core.data-loader | Stop before the call and reroute the unchanged ZIP through core.data-loader |
| Data Loader authentication is unavailable | Stop before upload; let core.data-loader use core.auth.fusion-oauth-authentication and never pass credentials or tokens from this task skill |
| Data Loader accepts an import without a process/request identifier | Treat initiation as unresolved, do not resubmit, and inspect the returned status or adapter result |
| Data Loader upload or initiation fails | Preserve the request identifier and sanitized Data Loader result; do not retry automatically |
| A declared core/shared command rejects documented inputs or returns an undocumented result | Pause side effects, compare the owning skill contract and command `--help`, then inspect only the smallest relevant implementation area if the mismatch remains; avoid broad repository or test-source scans, record the resolved interface, and resume from the same gate |
| Accepted initiation is followed by automatic polling | Stop; successful initiation is terminal for that request and status requires a later explicit user request |
| Post-import exact-name lookup does not find the proposed template | Report verification failure; do not assume rollback or resubmit the package |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields, enumerations, question structure, response mapping, or weight total are invalid | Correct the reported inputs and restart validation |
| Catalog mismatch | The task identity no longer resolves to CX Sales Leads | Stop and rebuild the effective catalog or review the requested hierarchy |
| Auth or authz | The read-only lookup returns 401 or 403 | Refresh an approved cached token once when allowed, otherwise correct privileges |
| Transport or environment | The read-only endpoint cannot be reached or returns an invalid response | Verify environment identity and connectivity; do not retry automatically |
| Fusion API | Oracle returns a documented export, read-only lookup, or Data Loader import failure | Show the sanitized status, external process/request identifier, and corrective action |
| Process timeout | An export, or a later explicitly requested Data Loader status check, does not reach a terminal state within the allowed wait | Stop polling and report the last state and exact resume path; do not start a replacement process |
| Process failed | Fusion reports a failed export or a failed Data Loader data set | On an explicit status request retrieve Data Loader errors and FSM ProcessLog when available, preserve diagnostics, and stop |
| Artifact persistence | A reference ZIP, hash, preview, package, or diagnostics artifact cannot be persisted safely | Stop before relying on incomplete evidence |
| Approval blocker | The exact immutable preview is not approved or the requested action would bypass core.data-loader | Stop before any Fusion mutation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Environment identity, GET path, status or failure class, and one safe corrective action |
| Validation failure | Requested operation, affected template name, failed rule, and corrected input required |
| Export failure or timeout | Environment identity, task code, ProcessId, HTTP/process status, elapsed wait, failed stage, and one safe resume action |
| Package validation failure | Reference ZIP hash, package hash when available, failed file/rule, affected row identity, and required correction |
| Data Loader handoff | Exact task context path/name/sequence, environment, operation, template identity, reference-data set, export ProcessId/hash/release, inventory and duplicate evidence, package path/hash/row counts, finalData.archiveSha256, and validation results |
| Import failure | Environment identity, process/request identifier, last status, failure class, sanitized ProcessLog/status, and a corrective action that does not resubmit |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous template identity | Guessing a template or business-unit context |
| Missing, invalid, stale, or mismatched reference export | Generating a package from guessed headers, another environment, or an unverified user ZIP |
| Unreviewed or changed preview/package | Continuing with stale duplicate evidence or approval |
| Fusion mutation request | Direct POST, PATCH, DELETE, deploy, import, or retry from this task-node registry; the final archive must route only through core.data-loader |
| Unsupported deployment | Browser, assisted Setup and Maintenance, REST, or another fallback mutation when the FSM deployment contract is not established |
| Ad hoc execution path | A new or modified task-local or shared script; direct shared.setup-import, setupTaskCSVImports, UCM, initiation, or browser fallback outside core.data-loader |
| Lookup failure | Automatic retry other than the single approved cached-token refresh rule |
| Export or import timeout/failure | Starting a replacement process or resubmitting the same ZIP without a new explicit user decision and idempotency review |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LQT.EXECUTION_GATE | step | 6 | execution_gate | data_loader_ready->LQT.READY_DATA_LOADER;review_ready->LQT.READY_REVIEW;blocked->LQT.RETURN_ISSUES | LQT.DESIGN | stop | Route a final validated Create or Copy FSM ZIP to Data Loader, return Review or Deploy-readiness as read-only, and route every actual Deploy mutation or non-Data-Loader mutation request to the refusal terminal |
| LQT.READY_DATA_LOADER | terminal | 7 | terminal | none | LQT.EXECUTION_GATE | continue | The unchanged single-template FSM ZIP, task context, and final archive SHA-256 are ready for core.data-loader Task Hook validation and preview generation; no import approval or execution has occurred |
| LQT.READY_REVIEW | terminal | 8 | terminal | none | LQT.EXECUTION_GATE | continue | Review or deployment-readiness evidence is ready as read-only output; no mutation is authorized |
| LQT.RETURN_ISSUES | terminal | 9 | terminal | none | none | continue | Any validation, dependency, export, lookup, design, Data Loader handoff, import, or verification gate fails safely |
