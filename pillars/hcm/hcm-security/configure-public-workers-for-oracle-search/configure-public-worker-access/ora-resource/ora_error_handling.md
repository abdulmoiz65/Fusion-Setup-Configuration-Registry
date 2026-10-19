# Configure Public Worker Access Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A configuration Name is unavailable, ambiguous, or renamed | Stop before preview, CSV package generation, or import. Use a unique Name for a create or the exact existing Name for an update. A rename requires a separately supported route. |
| Filtering is inactive | Offer an optional profile-option lookup to help diagnose the state; do not treat unavailable effective-profile verification as a package-preparation blocker |
| Conflicting inclusion and exclusion criteria are entered | Stop and revise the design to remove the conflict |
| A required role or function privilege is missing | Stop and request security administration support |
| A required criterion or role identifier is unresolved | Stop before package generation; do not infer it from a display name. Report the requested value and match count and request the documented discriminator |
| The generic Business Unit or Legal Employer LOV route rejects its documented keyword or exact-name query with HTTP 400 | Use the same-environment verified versioned route for that LOV, retain it for the current session, and rerun only the documented request. Do not ask the user to supply a REST URL, hard-code another tenant's route, add an unsupported predicate, or use the versioned-route form for jobsLov. If the verified route is unavailable or also rejects the documented request, stop and report a route/query compatibility failure |
| A role is already assigned to another PWA | Stop before package preview; do not reuse the assignee |
| An advanced filter has no filter or expression, or combines incompatible options | Stop before preview and correct the inputs |
| A Rule Builder rule references an unpublished or invalid DFF attribute | Stop before package generation; deploy and publish the attribute in Manage Search Indexes |
| A Data Loader package lacks the current task template, immutable preview, or explicit approval | Stop before submission. Obtain the current template, prepare and validate the exact package, preview it, and obtain one final approval immediately before that package is submitted |
| An FSM task CSV export reports COMPLETED_WARNINGS in ASM_SETUP_CSV_METADATA.xml | Surface the export status and every warning for review before using the export as a package template. Do not report the export as unconditional success or omit the warnings from the validation result |
| A package preview is prepared | The preview does not require a Run Book, task context, or end-user approval. Validate one exact ZIP from the current template and show the parent, every role, every criterion, child linkage, ZIP members, header and row field counts, operation scope, and SHA-256. Request approval only immediately before submission |
| A Run Book is absent | Do not block package preview, submission, status checking, or optional verification. A Run Book may track testing but is not a PWA execution prerequisite |
| A role-based package is the tenant's first PWA configuration | Do not require an existing PWA configuration. Export the current Fusion task template, use the documented child view-instance names, validate all nested-FSM checks, and present the complete preview before approval. Use a Fusion-exported working package as additional reference when one exists |
| A package role or detail row uses the parent view-instance name or has blank or mismatched ORA_PER_HCM_PUBLIC_WORKER_ACCESS.Name | Stop before upload. Report the affected CSV member and row. Require PublicWorkerAccessAssignmentMigration for roles or PublicWorkerAccessDetailMigration for details, and the exact package parent Name in the fully qualified parent-name column |
| A PWA CSV header or data row has a missing, extra, or shifted field | Stop before preview. Report the CSV member, row, expected and actual field counts, and affected header. Rebuild the row by current-template header name, retain every template column, and emit an empty field only when it is documented as optional and intentionally blank |
| A template supplies GroupingKey values that are not preserved consistently | Stop before upload. Report the affected CSV member and row. Preserve the supplied value on the parent and every child; do not generate a replacement or require an exported parent value |
| FSM source validation passes but the approval preview lacks archive, member, or child-linkage details | Stop before approval. Rebuild the task-level preview for the unchanged ZIP and show its SHA-256, ZIP members, row counts, parent-child structure, each child member and row, parent Name, template-supplied GroupingKey when present, child parent-name value, operation scope, and prerequisite results |
| Approval-envelope construction fails locally | Stop before upload. Correct and validate the local envelope, reverify the ZIP SHA-256, and retain the same approval only when the exact immutable preview and ZIP remain unchanged |
| A failed import requires a corrected ZIP | Diagnose the failure, rebuild from the approved design, and run all local validation and preview steps without requesting approval. Because the corrected ZIP is a new immutable artifact, request one new final approval only immediately before its resubmission |
| A Data Loader import request is accepted | Show a status card with the request or process reference, state Processing, and an explicit Check status action. Do not report success or poll automatically |
| A Data Loader import status is Succeeded | Show the request or process reference, final status, loaded and failed counts when available, and an offered optional Verify configuration action that uses the expanded PWA readback |
| The FSM process log reports childLogicalRows null or child rows are skipped after the parent loads | Stop before retry. Explain that Fusion could not match a nested child to its parent, report the affected member and row, and require the fully qualified parent-name column to match the package parent exactly. When the template supplied GroupingKey, confirm it was preserved consistently before rebuilding the one-package ZIP |
| A Data Loader import fails or has no verifiable process-log outcome | Stop before retry. Preserve sanitized diagnostics, correct the package or configuration, create and validate a new preview without approval, then obtain one fresh final approval immediately before the changed ZIP is submitted |
| Delete is requested for a configuration with associated roles | Stop; remove role assignments through separate approved operations before preparing the delete package |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Criteria duplicate or conflict with the selected scenario | Correct the design |
| CSV schema blocker | A CSV header differs from the current task template or a data row has a different field count from its header | Rebuild the affected row by header name, preserve optional intentional blank cells, validate field counts, and regenerate the preview before any approval |
| Approval blocker | The package lacks a current template, immutable preview, or explicit approval | Prepare and approve the exact package |
| FSM structure blocker | A role or detail row has an invalid child view-instance name, blank or mismatched fully qualified parent-name value, or unsupported nested-member structure | Correct the package from the current task template and exact package parent Name. Rebuild the preview and obtain fresh approval if the ZIP changes |
| Preview completeness blocker | An FSM preview omits its checksum, ZIP member summary, row counts, parent-child structure, child-linkage values, operation scope, or prerequisite results | Rebuild the task-level preview before requesting approval |
| Processing | Data Loader accepted the package but success is not verified | Check import status or process log later |
| Process failed | Data Loader fails or has no verifiable process log | Correct and locally validate a new package, then approve it only immediately before a new submission |
| Route/query compatibility | A documented Business Unit or Legal Employer LOV request is rejected by both its generic and same-environment verified versioned routes | Report the LOV endpoint, operation, sanitized HTTP result, and that no alternate predicate was attempted. Correct the task-owned route contract before rerunning the lookup |
| Design enforcement | Mode, role uniqueness, or advanced-filter compatibility fails | Correct the design and rerun preview |
| Import succeeded | Import status reports Succeeded | Show the final status card and offer optional expanded configuration verification |
| Blocked | A delete target has associated roles | Remove roles through separate approved operations |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Blocked configuration | The failed prerequisite, its classification, and the recommended corrective action |
| Before a Data Loader create, update, or delete | The visible workflow stage Validate, Preview, Approve exact ZIP, Submit, or Verify optional; the affected operation; current-template provenance; the complete exact package preview; and that approval is requested once, immediately before the exact ZIP is submitted |
| Before approval of a package with child rows | Current task-template provenance, package parent Name, role and detail child view-instance names, each child row's parent-name value, template-supplied GroupingKey values when present, ZIP members, header and row field counts, operation scope, SHA-256, and the single Submit exact ZIP action |
| Data Loader accepted the package | A status card with Processing state, available request or process reference, explicit Check status action, and the safe next action |
| Data Loader import succeeded | A final status card with request or process reference and loaded and failed counts when available, plus an offered optional Verify configuration action |
| Data Loader failure | Failure classification, sanitized diagnostic, affected ZIP member when known, available process reference, corrected-preview requirements, and that a new approval is requested only immediately before resubmitting a changed ZIP |
| LOV route/query compatibility failure | The Business Unit or Legal Employer LOV endpoint, whether candidate browse or exact resolution was attempted, sanitized HTTP result, selected route state, and that no alternate predicate was attempted |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A Data Loader package lacks the current template, immutable preview, or explicit approval | Do not submit the package |
| A role or detail row fails nested-FSM structure or parent-linkage validation | Do not upload the package, add a fabricated criterion row, or invent a parent Name. Preserve a template-supplied GroupingKey rather than generating a replacement |
| An FSM preview is incomplete | Do not ask for approval until the complete task-level preview is available |
| Lookups, template export, package generation, local validation, failure diagnosis, rebuild, status checking, or optional verification are performed | Do not request or record end-user approval for these non-mutating stages |
| A Data Loader submission fails or its outcome is uncertain | Do not retry automatically or report acceptance as success |
| A Business Unit or Legal Employer LOV route rejects the documented contract | Do not ask the user to paste a REST URL, generate a cross-tenant route, invent another predicate, or apply the versioned-route fallback to jobsLov |
| Delete is requested while associated roles remain | Do not submit the delete package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWA.DATALOADER_GATE | decision | 7 | execution_gate | ready->PWA.READY_FOR_DATALOADER;blocked->PWA.BLOCKED | PWA.ENFORCE_DESIGN | stop | The package passes nested-FSM structure validation and has a complete exact preview, explicit approval, and import-status plan; expanded configuration verification is optional after successful import status |
| PWA.READY_FOR_DATALOADER | terminal | 8 | terminal | none | PWA.DATALOADER_GATE | stop | The task-local Data Loader package is validated and ready for its separately authorized submission workflow |
| PWA.BLOCKED | terminal | 9 | terminal | none | none | stop | A required input, dependency, lookup, design rule, Data Loader gate, or delete prerequisite is blocked |
