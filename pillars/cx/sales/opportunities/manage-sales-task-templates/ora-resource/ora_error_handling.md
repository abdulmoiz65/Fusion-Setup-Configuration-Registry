# Error Handling

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Stop safely on missing template context, incorrect operation ordering, ambiguous setup-page selections, an invalid or pending CSV package, an incomplete Core Data Loader lifecycle, or an unselected execution route. The reviewed Oracle sources document the setup UI and Functional Setup Manager CSV flow, but not a task-specific Sales Task Template REST write contract.

Sources: [Shared task-template fields and defaults](https://docs.oracle.com/cd/G55130_01/trans/F77858-09/getting-started-with-your-partner-relationship-management-implementation.pdf#page=112), [Add Task Templates to Sales Stages](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-task-templates-to-sales-stages.html), [Setup Task CSV Template Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html), [Setup Task CSV Imports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html), [Create an activity](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activities-post.html), and the current target-environment task export and import validation for ZBS_MANAGE_SALES_TASK_TEMPLATE on 2026-08-10.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required template, task, set, sales-stage, or CSV input is missing | Stop and request only the missing value. |
| SetId/SetCode is malformed, conflicts with another selector or package row, confirmed Common Set resolves elsewhere, or the candidate uses a different target's set | Classify as input or package identity validation, show the sanitized conflict, and stop before guided setup or handoff. |
| An existing template requested for review, update, task addition, or stage association can't be selected uniquely | Stop; don't create or choose a different template unless the requester explicitly changes scope. |
| An individual task is requested before its template header exists | Stop and complete or select the header first. |
| Automatic opportunity visibility is requested without Automatically generated | Block the association plan and require the documented generation type. |
| A CSV template-export process is incomplete or has no result | Stop before package preparation and handoff; retain the process identifier and wait for that process rather than starting another automatically. |
| A supplied CSV ZIP isn't for ZBS_MANAGE_SALES_TASK_TEMPLATE or changes the exported member structure | Block the import and request a current exact-task export or template. |
| An ORA_ACTIVITY.csv row has a missing, overlength, or repeated ActivityNumber | Block the candidate before handoff, assign a reviewed unique identifier no longer than 64 characters, rebuild the ZIP, and rerun task-local validation. |
| FSM returns JBO-27014 for ActivityPEO.ActivityNumber on a later explicit results request | Treat the import as failed, report whether any template object succeeded, correct every child identifier, and require a new immutable package and Core Data Loader preview lifecycle. |
| CSV import handoff is requested without a verified immutable ZIP, exact task identity and persisted Data Loader task context, reopened SHA-256, and completed package validation | Block the handoff and report the missing package gate; approval is not a child-skill prerequisite. |
| This child skill requests package approval or constructs a Task Hook preview before handoff | Stop that flow; hand the validated immutable package to Core Data Loader, which owns Task Hook preview and later contextual approval. |
| A direct Sales Task Template create or update REST request is made | Block the direct mutation; use the documented setup task UI or approved FSM CSV route. |
| A supported mutation request has no manual-UI preference | Default to the current task-specific CSV/FSM package and core Data Loader preview-and-approval workflow; do not initialize browser control. |
| The requester explicitly selects Data Loader, FSM, CSV import, or bulk maintenance | Use the current task-specific package and core Data Loader preview-and-approval workflow; do not initialize browser control. |
| A CSV import reports a revision mismatch | Stop with SourceTargetDiffOkFlag at its documented default N; don't bypass the mismatch merely to continue. |
| Core Data Loader returns accepted initiation | End the request immediately; status, ProcessLog, result retrieval, and verification require a later explicit request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required setup value, predecessor, or authorized access is absent | Obtain the missing value, predecessor, or access. |
| PENDING | A selected template-export process hasn't produced a completed result | Wait for the existing process result. |
| BLOCKED | A design gate, ambiguous template selection, invalid immutable ZIP, unsupported direct write, missing handoff evidence, or incomplete Data Loader-owned preview/approval prevents progress | Correct the setup context or continue through the owning Data Loader lifecycle. |
| FAILED | A documented template-export status call, local package validation, Data Loader initiation, or later explicitly requested FSM result fails | Report safe diagnostic context, confirm whether any object succeeded when evidence is available, and stop before retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or dependency block | The missing or conflicting business value and the safe next action. |
| Template-export failure | Task code, process identifier, status when available, and the no-automatic-resubmission instruction. |
| CSV automation block | Source/final-package status, structural or hash mismatch, missing handoff gate, and the no-upload instruction. |
| CSV activity-number failure | The affected task rows, ActivityNumber requirement, process result when later requested, whether any object succeeded, and the requirement for a corrected package plus a new Core Data Loader preview lifecycle. |
| Data Loader handoff | Exact target, task identity and persisted Data Loader task context, immutable ZIP path and SHA-256, ASM task identity, member/header receipt, reviewed row delta, and task-local validation result; no child approval is requested. |
| Accepted initiation | Return Core Data Loader's accepted result and state that status, ProcessLog, results, or verification requires a later explicit request. |
| Direct-write block | The exact task name, documented guided UI route, and approved FSM CSV alternative. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No public task-specific Sales Task Template write contract is documented | Don't invent a REST endpoint, method, or payload. |
| An existing template selection is absent or ambiguous | Don't choose another template or claim that a task was added. |
| Template set identity is wrong, conflicting, or cross-environment | Don't substitute Common Set, choose a close match, invent a set REST lookup, or rewrite a package row to continue. |
| The template export is pending or failed and no valid task data-export ZIP was supplied | Don't submit a CSV import or automatically create another export process. |
| The task CSV package is incomplete, belongs to another task, or has altered member names or headers | Don't edit, repackage, or import it. |
| The child package is valid but hasn't been handed to Core Data Loader | Don't request approval or upload; hand off the unchanged package and validation evidence. |
| Core Data Loader's current persisted-envelope approval contract has not authorized submission | Don't upload or initiate, and don't let this child manufacture, replace or add a separate approval requirement. |
| The import reports a source-target revision mismatch | Don't set SourceTargetDiffOkFlag to Y merely to continue. |
| Core Data Loader initiation is accepted | Don't poll, retrieve ProcessLog, inspect results, or verify in the same request. |

## Documented Guided Setup — Explicit Manual UI Only

1. Sign in as a sales administrator or setup user and open the exact Manage Sales Task Templates setup task.
2. In Task Template, add the template, enter its name and optional description, confirm Active, Opportunity, subtype intent, and the intended template set, then save the dialog.
3. In Details, add each individual task, supply the required subject, and review optional description, lead time, type, template duration, and priority values.
4. When stage-specific automatic tasks are required, open Manage Sales Methods and Sales Stages, edit the intended stage, add the template in Activity Templates, select Automatically generated, and save.
5. This guidance doesn't claim that any Fusion side effect has been performed or verified.

## Documented CSV Automation Route

| Sequence | Required Gate | What Must Happen |
|---|---|---|
| 1 | Source package | Use a current completed task data-export ZIP or CSV-template-export ZIP for ZBS_MANAGE_SALES_TASK_TEMPLATE. |
| 2 | Package preparation | Populate or edit only the reviewed data while retaining the exact exported member names and headers, then produce a new ZIP. |
| 3 | Child package validation | Validate the exact final ZIP, task identity and persisted Data Loader task context, reopened SHA-256, ASM identity, members, headers, template inputs, task inputs, and reviewed row delta. Do not request approval here. |
| 4 | Core Data Loader handoff | Hand the unchanged immutable package and validation evidence to Core Data Loader; it persists the immutable upload artifact, preflight envelope and Task Hook-bound preview, then follows its approval contract. |
| 5 | Core approval | Follow current core.data-loader authorization: its preview normally awaits a later contextual affirmative for the exact saved artifact and approval context. Core owns its persisted preflight and approved Task Hook envelope. This child does not require a literal user keyword, prescribe a same-process command or redefine core-owned explicit approval exceptions. Requested material changes require fresh core validation, preview and approval. |
| 6 | Upload and initiation | Core Data Loader submits the exact saved artifact through its approved-preflight workflow after verifying artifact integrity, selected environment, Run Book context and the approved Task Hook envelope. It does not reopen the original source, rebuild the artifact, refresh live metadata or rerun Task Hook rules. This child does not revalidate, reconstruct or submit the approved load. Accepted initiation ends the request; partial or uncertain failures retain the approved artifact and envelopes for reconciliation without automatic replay. |
| 7 | Later explicit status or results request | Only after a new explicit request, retrieve the import result or ProcessLog once and verify the template through the documented setup task UI. Do not poll automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.EXECUTION_GATE | decision | 6 | execution_gate | package_validated->SALES_TASK_TEMPLATE.IMPORT_READY;default_data_loader->SALES_TASK_TEMPLATE.IMPORT_READY;accepted_initiation->SALES_TASK_TEMPLATE.ACCEPTED;ui_guidance->SALES_TASK_TEMPLATE.UI_GUIDANCE_READY;export_request->SALES_TASK_TEMPLATE.EXPORT_READY;direct_rest_requested->SALES_TASK_TEMPLATE.BLOCKED | SALES_TASK_TEMPLATE.ENFORCE | stop | A validated immutable package is handed to Data Loader without child approval; accepted initiation is terminal; manual UI, export, review, or sales-stage guidance remain explicitly selectable. |
| SALES_TASK_TEMPLATE.IMPORT_READY | terminal | 7 | terminal | none | SALES_TASK_TEMPLATE.EXECUTION_GATE | continue | The final immutable task package passed local validation and is ready for Core Data Loader to create the Task Hook-bound preview and later request contextual approval. |
| SALES_TASK_TEMPLATE.ACCEPTED | terminal | 8 | terminal | none | SALES_TASK_TEMPLATE.EXECUTION_GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result inspection, or verification. |
| SALES_TASK_TEMPLATE.UI_GUIDANCE_READY | terminal | 9 | terminal | none | SALES_TASK_TEMPLATE.EXECUTION_GATE | continue | The requester explicitly selected manual UI and the documented template or downstream sales-stage procedure is ready for an authorized user; no Fusion side effect has been performed. |
| SALES_TASK_TEMPLATE.EXPORT_READY | terminal | 10 | terminal | none | SALES_TASK_TEMPLATE.EXECUTION_GATE | continue | The exact task metadata is ready for shared.setup-export.task-level-export; no export has been started by this rule set. |
| SALES_TASK_TEMPLATE.BLOCKED | terminal | 11 | terminal | none | none | continue | Input, access, dependency, selection, design, immutable-package, handoff, Data Loader-owned approval, or direct-write gates block the requested work. |
| SALES_TASK_TEMPLATE.FAILED | terminal | 12 | terminal | none | none | continue | A documented read-only export-status lookup, local package validation, Data Loader initiation, or later explicitly requested result/verification fails. |
