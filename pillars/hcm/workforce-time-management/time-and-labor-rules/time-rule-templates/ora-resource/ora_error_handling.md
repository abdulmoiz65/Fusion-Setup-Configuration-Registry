# Time Rule Templates Error Handling

Source: User-provided compatibility, proposal, approval, FSM CSV import through core.data-loader, and verification requirements, the supplied Time Rule Templates CSV reports, and the demonstrated Fusion failure mode for BOM-prefixed first headers.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required normalized behavior is missing | Stop before lookup and obtain the missing requirement |
| Current template export is missing, stale, unreadable, or internally inconsistent | Stop without selecting, proposing, or creating a template; refresh the complete export |
| One or more fully compatible candidates exist | Display every verified candidate and ask whether the user still wants a new template; do not create until they explicitly confirm |
| A create package is derived by copying an existing template record, metadata differs from the fresh export, or a literal blank, `0`, or `#null` changes during preparation | Stop before preview or import; reprepare from normalized intent and the fresh export contract, then repeat package and Data Loader validation |
| The exact validated FSM ZIP is not linked before approval | Stop before requesting approval; display the clickable link to that ZIP, then request approval |
| The Complete Summary or Defaults Applied section is absent, incomplete, or contains technical package data | Stop before linking the package or requesting approval; regenerate the business-only summary from verified values and defaults actually applied |
| Partial-only candidates exist | Block automatic reuse, disclose every material difference, and require user direction |
| An update target is missing or ambiguous | Stop before proposal and package preparation; require one exact current TemplateName match from the authoritative export |
| The proposal is incomplete | Do not request approval or prepare an import; complete and redisplay it |
| A create or update has no immutable FSM CSV ZIP validated through core.data-loader | Stop before approval or import and build the task-scoped package and Data Loader preview |
| Explicit import approval is missing | Stop before import handoff and ask for approval of the exact core.data-loader preview and archive SHA-256 |
| The user rejects or modifies the proposal | Do not import; revise and request fresh approval if the user wants to continue |
| A CSV starts with EF BB BF or its parsed first header is not the exact file-specific header | Reject the complete package and rebuild every CSV as UTF-8 without BOM |
| Fusion reports that the first required attribute is missing even though it is visibly present | Inspect the raw first three bytes and parsed first header before changing business data |
| core.data-loader validation, upload, initiation, monitoring, or import fails | Stop before retry, show the Data Loader stage, process result, and affected objects, and correct the cause |
| Import result is uncertain | Do not resubmit automatically; reconcile process status and authoritative state first |
| Created template cannot be reproduced in a refreshed authoritative export | Do not release it for Time Rule use; investigate and verify explicitly |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, unavailable, or its bounded polling slice ends without a result | Do not ask the user to retry exports, check again, or approve another export; continue task-authorized status monitoring with the same accepted ProcessId until a terminal result is available |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, returns no result, has partial or uncertain status, or produces an unusable ZIP | Do not claim the export evidence is ready or submit a duplicate export automatically; preserve the accepted ProcessId, last-known status, ProcessLog when available, and ZIP-validation evidence, then provide one safe investigation or resume action |
| An approved Time Rule Templates asynchronous create, update, import, load, or documented dependent submission is In progress or not yet available | Do not ask the user to request status separately or report final success; immediately start and continue the task-authorized status flow using the accepted request ID until a documented terminal status, then read back the authoritative export |
| An approved Time Rule Templates asynchronous submission fails, times out, has partial or uncertain status, or has a read-back mismatch | Do not report final success or retry the submission automatically; preserve the request identity, last-known status, approved archive identity, and verification evidence, then provide one safe investigation or resume action |
| Parent workflow context is multiple, conflicting, stale, incomplete, or undocumented | Do not infer a dependent-workflow handoff; ask the user to identify the intended workflow before offering a resume path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input | A required behavior or proposal field is missing or invalid | Correct it before lookup or approval |
| Lookup | A match is ambiguous, partial, missing, or cannot be evaluated | Refresh the source, obtain user direction, or complete a proposal |
| Update identity | The requested existing TemplateName does not resolve to exactly one current parent and child graph | Correct the target identity and refresh the complete export before preparing the update package |
| Approval | Approval is absent, rejected, stale, or bound to different proposal content | Stop and request approval of the current exact proposal |
| Approval summary | Complete Summary or Defaults Applied is missing, incomplete, or contains blank, null, unused, metadata-only, or technical package values | Regenerate the business-only summary from the validated configuration before package linking or approval |
| Package encoding | A CSV contains a BOM or its first header cannot be parsed exactly | Rebuild and fully revalidate the package |
| Package contract | The package does not use the fresh headers and metadata contract or does not preserve explicit literal values | Reprepare from verified structured values and repeat package and Data Loader validation |
| Execution | Import or verification fails | Diagnose and retry only after explicit authorization |
| Reconciliation | Import status is uncertain | Verify authoritative state before any resubmission |
| Route | A create or update is being blocked for lack of a direct REST endpoint, or an import bypasses core.data-loader | Select the supported FSM CSV route through core.data-loader and stop any direct REST or direct-adapter write |
| Export monitoring | A task-authorized read-only export or authoritative refresh is accepted but not yet terminal, downloaded, or ZIP-validated | Continue status checks using the same accepted ProcessId; do not request a retry or submit a duplicate export for the same task and purpose |
| Export failure | A task-authorized read-only export or authoritative refresh fails, times out, has no usable result, or the result ZIP fails validation | Preserve status and process evidence; do not claim readiness or retry automatically |
| Final completion monitoring | An approved Time Rule Templates asynchronous request is accepted but not yet terminal | Continue status checks with the same accepted request ID; submission acceptance is not verified success |
| Final completion failure | The request fails, times out, is partial or uncertain, or read-back does not match the approved configuration | Preserve the last-known status and verification evidence; do not retry automatically |
| Parent context | A parent workflow cannot be identified as exactly one current active documented prerequisite workflow | Stop for user workflow identification; do not infer a handoff |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Exact-match disclosure | Every matching template, its formula, template type, matched condition, inputs, outputs, summation, reporting, Time Category, result or payroll time-type characteristics, and the user choice to reuse or create |
| Confirmed create | Requested name, normalized parent/input/usage/translation values, validated ZIP identity, and approval status |
| Partial candidates | Every candidate and every material functional difference |
| Missing-template proposal | Complete template details, dependent Time Rule relationship, target environment, intended operation, proposal fingerprint, unresolved fields, and approval status |
| Approval request | Show the business-only Complete Summary and Defaults Applied details, then separately show the target environment, TaskCode ORA_HWM_MANAGE_RULE_TEMPLATES, create or update operation, clickable immutable archive link and SHA-256, core.data-loader validation result and preview, and state that neither the Time Rule Template nor the dependent Time Rule will be imported before explicit approval |
| Package encoding failure | Affected file, first-byte signature, expected and parsed first headers, whether Fusion created rows, and corrected package identity |
| Import or verification failure | Submitted identity, process result, failures, warnings, known side effects, missing evidence, and safe next action |
| Export monitoring | Accepted export ProcessId, export purpose, last known status, polling stage, persisted ZIP reference when available, ZIP validation result, and confirmation that no duplicate export was submitted |
| Final completion | Submission accepted, terminal request status, verified persisted configuration, explicitly supplied values, applied defaults labeled Default, and verification evidence. For a standalone flow, show only the verified Time Rule Templates result. For exactly one active documented parent prerequisite, state that the prerequisite is verified and ready to resume that parent, ask “Would you like to resume {parent workflow}?”, and state that the parent has not been started or resubmitted. |
| Final completion failure | Submission accepted when applicable, last-known terminal or nonterminal status, partial or uncertain outcome or mismatch evidence, and one safe investigation or resume action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| TemplateName matches but functional configuration does not | Do not reuse the template by name alone |
| Candidate selection is ambiguous or partial | Do not choose automatically |
| The user has not confirmed creation after exact-match disclosure | Do not prepare a package |
| A package is derived by copying a source record or its exact validated ZIP is not linked before approval | Do not request approval or submit the package |
| Current target-environment export lookup fails | Do not propose or create a template |
| Explicit approval for the exact proposal is missing, rejected, or stale | Do not create or import the template or dependent Time Rule |
| No direct REST create or update endpoint is documented | Do not block the supported FSM CSV import route and do not invent a direct REST write |
| A live import would bypass core.data-loader or call the FSM import adapter directly | Do not submit it; route the validated approved archive through core.data-loader |
| Any CSV starts with EF BB BF or has the wrong parsed first header | Do not submit the package |
| An import fails because of encoding | Do not resubmit automatically; require a corrected package, authoritative-state reconciliation, and explicit retry authorization |
| Verification is incomplete | Do not expose the template as ready for Time Rule use |
| Import status is uncertain | Do not automatically resubmit |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, or unavailable | Do not ask the user to retry exports, check again, or approve another export; continue monitoring only the same accepted ProcessId |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, has no result, or produces an invalid ZIP | Do not report export evidence as ready or submit a duplicate export automatically |
| An approved Time Rule Templates asynchronous submission is In progress or not yet available | Do not ask the user to request status separately or submit another create, update, import, or load; continue only the task-authorized monitoring and read-back flow |
| An approved Time Rule Templates asynchronous submission fails, times out, is partial or uncertain, or fails read-back verification | Do not report final success, retry the submission automatically, or offer parent continuation |
| No exactly one current active documented parent workflow establishes this task as a prerequisite | Do not show a dependent-workflow message or resume prompt; end with the verified standalone result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMETMPLT.APPROVAL_GATE | decision | 7 | execution_gate | approved->TIMETMPLT.IMPORT_HANDOFF_READY;missing->TIMETMPLT.APPROVAL_REQUIRED;rejected->TIMETMPLT.APPROVAL_DECLINED;changed->TIMETMPLT.APPROVAL_STALE | TIMETMPLT.PRESENT_VALIDATED_PACKAGE | stop | The complete proposal, business-only Complete Summary and Defaults Applied details, and immutable core.data-loader preview, including archive SHA-256 and create or update operation, have been displayed |
| TIMETMPLT.EXISTING_READY | terminal | 24 | terminal | none | TIMETMPLT.FIND_MATCH | stop | Exact matches were disclosed and the user selected reuse or has not confirmed a create |
| TIMETMPLT.SELECTION_REQUIRED | terminal | 25 | terminal | none | none | stop | Multiple exact matches need a reuse decision, or partial-only candidates require user direction |
| TIMETMPLT.IMPORT_HANDOFF_READY | terminal | 8 | terminal | none | TIMETMPLT.APPROVAL_GATE | stop | The exact core.data-loader preview is approved; invoke core.data-loader to upload, initiate, monitor, retrieve the terminal result, and then refresh the authoritative export for verification |
| TIMETMPLT.INPUT_ERROR | terminal | 9 | terminal | none | TIMETMPLT.VALIDATE_REQUIREMENTS | stop | Input validation fails |
| TIMETMPLT.LOOKUP_ERROR | terminal | 10 | terminal | none | TIMETMPLT.FIND_MATCH | stop | Current export lookup fails |
| TIMETMPLT.PROPOSAL_ERROR | terminal | 11 | terminal | none | TIMETMPLT.PROPOSAL_GATE | stop | The template proposal or dependent Time Rule relationship is incomplete |
| TIMETMPLT.APPROVAL_REQUIRED | terminal | 12 | terminal | none | TIMETMPLT.APPROVAL_GATE | stop | Explicit approval for the exact proposal is missing |
| TIMETMPLT.APPROVAL_DECLINED | terminal | 13 | terminal | none | TIMETMPLT.APPROVAL_GATE | stop | The user rejected the proposal |
| TIMETMPLT.APPROVAL_STALE | terminal | 14 | terminal | none | TIMETMPLT.APPROVAL_GATE | stop | The proposal or target environment changed after approval |
| TIMETMPLT.DEPENDENCY_ERROR | terminal | 15 | terminal | none | TIMETMPLT.CREATE_DEPENDENCY | stop | Package, import handoff, process result, or verification readiness is blocked |
| TIMETMPLT.EXPORT_READY | terminal | 17 | terminal | none | TIMETMPLT.EXPORT_MONITOR | stop | Terminal export success, persisted result ZIP, and ZIP validation all passed |
| TIMETMPLT.EXPORT_ERROR | terminal | 18 | terminal | none | none | stop | Export monitoring reached failure, timeout, missing result, unusable ZIP, partial status, or uncertainty |
| TIMETMPLT.FINAL_COMPLETION_ERROR | terminal | 20 | terminal | none | none | stop | Task-authorized status monitoring reached failure, timeout, partial success, uncertainty, or read-back mismatch |
| TIMETMPLT.FINAL_COMPLETION_SUCCESS | terminal | 21 | terminal | none | TIMETMPLT.FINAL_COMPLETION | stop | Terminal success status and authoritative read-back verification passed for a standalone Time Rule Templates flow |
| TIMETMPLT.FINAL_COMPLETION_PARENT_RESUME | terminal | 22 | terminal | none | TIMETMPLT.FINAL_COMPLETION | stop | The prerequisite is verified and ready to resume exactly one active documented parent workflow; present the resume prompt and do not start the parent |
| TIMETMPLT.PARENT_CONTEXT_REQUIRED | terminal | 23 | terminal | none | TIMETMPLT.FINAL_COMPLETION | stop | Parent workflow context is multiple, conflicting, stale, incomplete, or undocumented |
