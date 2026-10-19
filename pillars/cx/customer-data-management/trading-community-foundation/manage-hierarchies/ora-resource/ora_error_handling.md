# Error Handling

Classify failures without exposing credentials, opaque links, encoded source
data, or source rows. CSV inspection, parsing, classification, and validation
by the selected shared/Core Data Loader workflow are expected and must not be
classified as a Manage Hierarchies contract blocker. Never automatically
resubmit a user-supplied hierarchy CSV.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, environment, read identifier, or usable CSV path is missing | Stop before external access and report only the missing routing input |
| Core Data Loader's rendered Markdown omits the canonical digest | Continue with the task-local read-only preflight bridge and consume response.preflight.archiveSha256 from Core Data Loader's structured approval-stop result; do not calculate a substitute |
| The structured Core Data Loader preflight omits or returns an invalid archiveSha256 | Classify preflight_contract and stop before Task Hook approval or upload |
| The selected shared/Core workflow rejects a supplied source during its normal preflight | Return that workflow's classified validation result; do not replace it with a stricter task-specific check or select another file |
| Live metadata does not expose the exact Hierarchy or HierarchyNode object as importable or cannot resolve its UCM account | Classify catalog_or_metadata_mismatch and stop without substituting an object, account, or execution route |
| Authentication returns 401 or 403 during a read-only preflight | Use the routed workflow's single permitted refresh behavior; then classify authorization_or_privilege if unavailable |
| A GET times out, pagination is incomplete, or its response is uncertain | Classify transport_or_environment and stop without switching routes |
| A completed UI-aligned list has no eligible hierarchy | Return an empty successful list with the applied ACTIVE, as-of-date, and NodeCount criteria; do not fall back to raw inventory |
| A UI-aligned list finds multiple eligible versions for one hierarchy, an orphan version, a missing required filter attribute, or a nonnumeric NodeCount | Report ambiguous_match for duplicate eligible versions or catalog_or_metadata_mismatch for an unusable response; stop without selecting a version or weakening the filters |
| An exact `fndTrees` or `fndTreeVersions` lookup uses SQL-style `and` between `TreeStructureCode` and `TreeCode` clauses | Treat it as invalid query construction, rebuild the one `q` value with semicolon-separated equality clauses, and repeat only that GET before reporting `not_found` |
| Exact tree or version lookup returns no or multiple matches | Report not_found or ambiguous_match and stop without selecting a row |
| An exact current-run version omits its FndTreeNode child link | Use the describe-confirmed `fndTreeNodes` fallback with one exact TreeStructureCode, TreeCode, and TreeVersionId query; stop when its readable contract or complete pagination cannot be established. Never issue an unscoped node query. |
| UCM upload outcome is uncertain or pending resolution | Preserve the checkpoint and reconcile only that upload; never upload again |
| CX Import creation outcome is uncertain | Reconcile the existing activity/checkpoint; never repeat the POST |
| Fusion rejects rows or reports import errors | Return Fusion's sanitized activity/data-file diagnostics and stop; do not silently repair, rewrite, or resubmit the CSV |
| A Hierarchy or HierarchyNode DELETE_RECORD activity is unavailable or rejected | Preserve the sanitized Fusion diagnostics, classify the observed metadata or process failure, and stop without retrying or selecting another route |
| Fusion processes an unchanged supplied delete CSV successfully | Report the exact DELETE_RECORD activity mode, terminal data-file status, and counts. Do not claim a specific record is absent unless the user separately requested and supplied identities for verification. |
| Optional record-level verification still finds the hierarchy or member | Report unknown_requires_reconciliation and do not resubmit automatically |
| Party Hierarchy Generation is separately requested | Require its own resolved preview and fresh approval after import success; never reuse import approval |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Operation, environment, read identifier, source preflight, object role, or import mode cannot be routed | Correct the reported routing or shared/Core validation issue; do not add a separate task-specific validation gate |
| preflight_contract | Core Data Loader's structured approval-stop result lacks a valid archiveSha256, exact object code, UCM account, or ordered file list | Stop without hashing locally, building Task Hook approval, uploading, or switching routes |
| not_found | A completed exact read lookup returns no match | Confirm the exact read identifiers |
| ambiguous_match | A completed exact read lookup returns multiple exact matches | Resolve the read identity ambiguity |
| catalog_or_metadata_mismatch | A declared read resource or exact CX Import object/account is unavailable | Confirm the deployed contract and privileges; do not substitute a route |
| authorization_or_privilege | Authentication succeeds but the required read, upload, import, or ESS privilege is denied | Confirm the exact required privilege |
| transport_or_environment | Network or environment state prevents a reliable completed operation | Resume only with the workflow's safe read-only reconciliation path |
| fusion_api_error | Fusion rejects a read request or supplied import data | Preserve sanitized diagnostics and let the user correct the source externally |
| process_timeout | Import or separately approved ESS monitoring reaches its bounded timeout | Report the external ID and resume with status only |
| process_failed | CX Import or separately approved ESS process ends unsuccessfully | Persist available sanitized diagnostics and stop |
| artifact_persistence | Required preview, checkpoint, receipt, or run record cannot be safely persisted | Stop before the next mutation |
| approval_blocker | Core Data Loader approval is missing, stale, or does not match the exact activity | Rebuild the immutable preview; do not add a second task-level approval |
| unsupported_operation | FSM import/export, direct Trees mutation, or another undeclared route is requested | Use only the supported read or create/update/delete CX Import route |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read result | Task, target, operation, sanitized counts, pagination completion, applied list criteria and as-of date when relevant, and confirmation of no changes |
| CX Import approval | Target, exact object, ImportMode, activity name, filename, canonical group digest, UCM account, activation, schedule, and the authoritative source-review result produced by Core Data Loader; clearly identify destructive effect for DELETE_RECORD |
| Import result | Activity ID and name, object, mode, filename, UCM document name, terminal data-file status, counts, sanitized diagnostics, and whether optional record-level verification was performed |
| Failed or uncertain mutation | Failure class, existing checkpoint/activity ID, last known state, and the one safe reconciliation action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A user-supplied hierarchy CSV is present | Do not block because a declared shared/Core dependency reads, inspects, decodes, parses, classifies, validates, hashes, packages, or otherwise processes it |
| Both hierarchy object files are supplied | Do not combine them into one CX Import activity |
| Approval already covers an unchanged activity | Do not ask for a duplicate Manage Hierarchies approval |
| An upload or import POST is uncertain | Do not replay it |
| Fusion rejects supplied data | Do not silently fix or resubmit it |
| Delete is requested | Do not use direct Trees POST, PATCH, DELETE, or an /action/ endpoint; route only the Core Data Loader governed DELETE_RECORD workflow |
| An unchanged supplied delete CSV lacks locally verified identifiers or an exact pre-delete match | Do not block the pass-through submission for that reason; do not claim record-level absence without optional verification |
| FSM import/export is requested | Do not substitute FSM or generic initiateDataLoad |
| Party Hierarchy Generation lacks fresh approval | Do not submit ESS |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MH.ERROR | step | 6 | error_handler | handled->MH.ISSUES | none | continue | Any validation, lookup, routing, privilege, transport, metadata, approval, import, or process failure |
| MH.DONE_READ | terminal | 7 | terminal | none | MH.READ_HIERARCHY | continue | The requested read operation completed with sanitized evidence |
| MH.IMPORT_READY | terminal | 8 | terminal | none | MH.ROUTE_CX_IMPORT | continue | Exact supplied-file object and mode routing is ready for the shared Data Loader governed CX Import workflow |
| MH.ISSUES | terminal | 9 | terminal | none | MH.ERROR | continue | The request has unresolved issues and no further mutation was attempted |
