# Time Rules Error Handling

Source: Requested Time Rule and prerequisite Time Rule Template matching, proposal, approval, creation, and verification behavior, plus developer-provided failed-import evidence for BOM-prefixed CSV headers and a short input CSV row.

## Error Situations

| Situation | What Should Happen | Next Action |
|---|---|---|
| Required normalized behavior is missing | Stop before lookup | Obtain and validate the missing requirement |
| RuleName or RuleType is omitted but a plain-language creation request contains both a condition and intended outcome | Do not block the baseline lookup | Derive and display a proposed RuleName and provisional RuleType; resolve and confirm them before package generation |
| Neither a normalized identity nor sufficient plain-language creation intent is available | Stop before lookup | Obtain a rule name and rule type, or a condition and intended outcome from which a draft can be derived |
| Current export is missing, stale, unreadable, or internally inconsistent | Stop without creating anything | Refresh all five objects and rerun lookup |
| Multiple exact matches exist | Block automatic selection | Present all candidates and require user selection |
| A derivable same-family predecessor exists | Do not silently update | Use it internally to propose complete business values and defaults, default to Create new, and invite changes; verify the supporting template before package preparation |
| An update to a derivable source candidate is not explicitly requested | Stop before package preparation | Keep the default Create new proposal; require an explicit user request before preparing an update |
| Compatible but non-exact matches exist without one derivable same-family predecessor | Do not require whole-rule selection | Use the candidates as evidence; present only unresolved meaningful business inputs or outputs as focused choices, and block preparation only until those choices are resolved |
| The current Time Rule Templates export is missing, stale, unreadable, or internally inconsistent | Stop without proposing or creating either object | Refresh the complete template export and rerun compatibility matching |
| Multiple fully compatible or partial-only Time Rule Template candidates exist | Block automatic selection and creation | Display every candidate and material difference and require user direction |
| Candidate template evidence is incomplete | Stop before asking the user to select a candidate | Refresh the template baseline or disclose the missing evidence; do not reduce the request to a generic blocker |
| No fully compatible template exists and the joint proposal is incomplete | Do not request approval | Complete and redisplay both proposed objects |
| The joint proposal has not been explicitly approved | Stop before any template or rule import handoff | Ask for approval of the exact displayed proposal |
| The user rejects or changes the joint proposal | Do not create either object | Revise the proposal and request fresh approval if the user wants to continue |
| The approved Time Rule Template has not been created and verified by the separate Time Rule Templates task | Keep Time Rule creation blocked | Complete and verify the prerequisite task, then rerun template lookup |
| Missing rule creation lacks a validated immutable FSM CSV ZIP or explicit import approval | Keep the dependency blocked | Prepare and validate the CSV package, then obtain approval of its immutable preview |
| A Time Rules CSV starts with EF BB BF or the first parsed header is not the file-specific expected header | Stop before import; classify the package as invalid | Rewrite all CSV files as UTF-8 without BOM, validate their first bytes and headers, and create a new ZIP |
| A Time Rules CSV data row has more or fewer parsed fields than its header | Stop before preview or import; classify the package as invalid | Report the file, row number, header field count, and row field count; rebuild the CSV with exactly matching field counts and create a new ZIP |
| A required field is unspecified or a literal `0`, blank, or null value would be dropped, normalized, or substituted | Stop before package creation | Resolve the field or correct the serializer; preserve the supported FSM null representation and trailing blank fields exactly |
| Fusion reports that the first required attribute is missing even though it is visibly present in the CSV | Treat CSV encoding as a primary diagnostic; do not assume the business value is missing | Inspect the raw first three bytes and parsed first header, reconcile whether any rows were created, then correct the package |
| Rule creation fails | Stop dependent preparation | Show the failure and correct it before retrying |
| Newly created rule cannot be verified in a refreshed export | Do not reference the rule | Investigate creation status and verify explicitly |
| Import result is uncertain | Do not resubmit automatically | Reconcile status and verify authoritative state first |
| A generic catalog search selects a same-name task with a code other than ORA_HWM_MANAGE_RULES | Stop before export, import, or creation | Re-resolve the selected nested Time Rules skill and use only ORA_HWM_MANAGE_RULES |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, unavailable, or its bounded polling slice ends without a result | Do not ask the user to retry exports, check again, or approve another export | Continue task-authorized status monitoring with the same accepted ProcessId until a terminal result is available |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, returns no result, has partial or uncertain status, or produces an unusable ZIP | Do not claim the export evidence is ready and do not submit a duplicate export automatically | Preserve the accepted ProcessId, last-known status, ProcessLog when available, and ZIP-validation evidence; provide one safe investigation or resume action |
| An approved Time Rules asynchronous create, update, import, load, or documented dependent submission is In progress or not yet available | Do not ask the user to request status separately and do not report final success | Immediately start and continue the task-authorized status flow using the accepted request ID until a documented terminal status, then read back the authoritative export |
| An approved Time Rules asynchronous submission fails, times out, has partial or uncertain status, or has a read-back mismatch | Do not report final success or retry the submission automatically | Preserve the request identity, last-known status, approved archive identity, and verification evidence; provide one safe investigation or resume action |
| Parent workflow context is multiple, conflicting, stale, incomplete, or undocumented | Do not infer a dependent-workflow handoff | Ask the user to identify the intended workflow before offering a resume path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input | A requirement is invalid or incomplete | Correct it before lookup |
| Package encoding | A CSV contains a BOM or a file-specific first header cannot be parsed exactly | Rebuild the complete package as UTF-8 without BOM and revalidate it before seeking retry authorization |
| Package shape | A CSV data row has a different parsed field count from its header | Rebuild the complete package with exact header-width rows and revalidate it before seeking approval |
| Lookup | A match is missing, ambiguous, or cannot be evaluated | Refresh the source or obtain user selection only for multiple exact matches |
| Decision required | A meaningful business input or output remains unresolved after field-level resolution | Disclose that business setting and its candidate values; obtain a focused user choice |
| Template lookup | A template match is missing, ambiguous, partial, or cannot be evaluated | Refresh the source, obtain user selection, or prepare a complete joint proposal |
| Candidate disclosure | Candidate template evidence is incomplete | Refresh the source or identify the exact missing evidence before requesting a selection |
| Approval required | No compatible template exists and explicit approval for the displayed joint proposal is absent or stale | Do not hand off either object for import |
| Dependency | A required FSM CSV package, approval, or verification is missing | Resolve the dependency through `core.data-loader`; do not invent a direct REST create route |
| Execution | Creation or verification failed | Diagnose and retry only after explicit authorization |
| Reconciliation | Import status is uncertain | Verify authoritative state before any resubmission |
| Task routing | A same-name catalog result is not the selected Time and Labor task | Correct the task code from the selected nested task skill before continuing |
| Export monitoring | A task-authorized read-only export or authoritative refresh is accepted but not yet terminal, downloaded, or ZIP-validated | Continue status checks using the same accepted ProcessId; do not request a retry or submit a duplicate export for the same task and purpose |
| Export failure | A task-authorized read-only export or authoritative refresh fails, times out, has no usable result, or the result ZIP fails validation | Preserve status and process evidence; do not claim readiness or retry automatically |
| Final completion monitoring | An approved Time Rules asynchronous request is accepted but not yet terminal | Continue status checks with the same accepted request ID; submission acceptance is not verified success |
| Final completion failure | The request fails, times out, is partial or uncertain, or read-back does not match the approved configuration | Preserve the last-known status and verification evidence; do not retry automatically |
| Parent context | A parent workflow cannot be identified as exactly one current active documented prerequisite workflow | Stop for user workflow identification; do not infer a handoff |

## Disclosure Rules

| Situation | What Must Be Shown |
|---|---|
| Exact match selected | RuleName, RuleType, normalized matched behavior, and verification source |
| Multiple exact candidates | Every candidate and every material behavioral difference |
| Compatible-rule evidence | Only unresolved meaningful business inputs or outputs and their candidate values; do not ask the user to select an entire existing rule or expose CSV rows, clone mechanics, or internal technical fields |
| Derivable proposal | Proposed business values, applied defaults, and the default Create new operation. State that source provenance is available on request and that an existing rule is changed only after an explicit update request. |
| Multiple fully compatible or partial-only template candidates | Each candidate's match category, supported characteristics, material differences, verification source, and confirmation needed before selection |
| Compatible template selected | TemplateName, formula, matched condition, inputs, outputs, summation, reporting, Time Category, result or payroll time-type and parameter characteristics, verification source, and why it is fully compatible |
| Conditional creation proposed | Complete Time Rule Template proposal, complete Time Rule proposal, their relationship, target environment, immutable CSV archive SHA-256, and approval status |
| Package encoding failure | Affected file, observed first-byte signature, expected first header, parsed first header, whether Fusion created any rows, and the corrected package identity |
| Package shape failure | Affected file, data-row number, expected header field count, observed row field count, whether Fusion created any rows, and the corrected package identity |
| Creation or verification failure | Submitted identity, known result, missing evidence, and safe next action |
| Export monitoring | Accepted export ProcessId, export purpose, last known status, polling stage, persisted ZIP reference when available, ZIP validation result, and confirmation that no duplicate export was submitted |
| Final completion | Submission accepted, terminal request status, verified persisted configuration, explicitly supplied values, applied defaults labeled Default, and verification evidence. For a standalone flow, show only the verified Time Rules result. For exactly one active documented parent prerequisite, state that the prerequisite is verified and ready to resume that parent, ask “Would you like to resume {parent workflow}?”, and state that the parent has not been started or resubmitted. |
| Final completion failure | Submission accepted when applicable, last-known terminal or nonterminal status, partial or uncertain outcome or mismatch evidence, and one safe investigation or resume action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| RuleName matches but behavior does not | Do not reuse the rule by name alone |
| Candidate selection is ambiguous | Do not choose automatically |
| A derivable source candidate is found | Do not silently update it or expose its internal clone mechanics; propose values, default to Create new, and require an explicit update request plus verified template evidence before an update |
| Lookup fails | Do not create or prepare dependent Rule Set members |
| Template compatibility lookup has not completed | Do not propose or create a new Time Rule |
| A template candidate is only partially compatible | Do not silently reuse it |
| No fully compatible template exists and explicit approval is missing, rejected, or stale | Do not create or import the Time Rule Template or the Time Rule |
| The approved template has not been verified in a refreshed authoritative export | Do not create or import the dependent Time Rule |
| Any Time Rules CSV starts with EF BB BF or has the wrong parsed first header | Do not submit the package |
| Any Time Rules CSV data row does not have exactly the header's field count | Do not preview, approve, or submit the package |
| An import fails because of package encoding | Do not resubmit automatically; require a corrected package, authoritative-state reconciliation, and explicit retry authorization |
| No direct REST create endpoint is documented | Do not block the FSM CSV import route or invent a direct REST create action |
| Verification is incomplete | Do not expose the proposed rule as ready |
| Import status is uncertain | Do not automatically resubmit |
| A task code was chosen from a generic task-name match | Do not export, import, create, or claim that the selected Time and Labor task was used |
| An accepted task-authorized read-only export or authoritative refresh is pending, running, In progress, or unavailable | Do not ask the user to retry exports, check again, or approve another export; continue monitoring only the same accepted ProcessId |
| An accepted task-authorized read-only export or authoritative refresh fails, times out, has no result, or produces an invalid ZIP | Do not report export evidence as ready or submit a duplicate export automatically |
| An approved Time Rules asynchronous submission is In progress or not yet available | Do not ask the user to request status separately or submit another create, update, import, or load; continue only the task-authorized monitoring and read-back flow |
| An approved Time Rules asynchronous submission fails, times out, is partial or uncertain, or fails read-back verification | Do not report final success, retry the submission automatically, or offer parent continuation |
| No exactly one current active documented parent workflow establishes this task as a prerequisite | Do not show a dependent-workflow message or resume prompt; end with the verified standalone result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TIMERULE.TEMPLATE_APPROVAL_GATE | decision | 7 | execution_gate | approved->TIMERULE.TEMPLATE_CREATION_HANDOFF_READY;missing->TIMERULE.TEMPLATE_APPROVAL_REQUIRED;rejected->TIMERULE.TEMPLATE_APPROVAL_DECLINED;changed->TIMERULE.TEMPLATE_APPROVAL_STALE | TIMERULE.TEMPLATE_COMPLETE_SUMMARY | stop | The Complete Summary is displayed for a complete joint Time Rule Template and Time Rule proposal |
| TIMERULE.REUSE_READY | terminal | 11 | terminal | none | TIMERULE.FIND_MATCH | stop | Exactly one verified exact Time Rule match exists |
| TIMERULE.SELECTION_REQUIRED | terminal | 12 | terminal | none | none | stop | Multiple exact Time Rule candidates exist |
| TIMERULE.TEMPLATE_SELECTION_REQUIRED | terminal | 13 | terminal | none | none | stop | Multiple fully compatible or partial-only template candidates require user direction |
| TIMERULE.TEMPLATE_CREATION_HANDOFF_READY | terminal | 14 | terminal | none | TIMERULE.TEMPLATE_APPROVAL_GATE | stop | The exact joint proposal is approved; invoke the separate Time Rule Templates task first, verify it, then rerun this Time Rules workflow |
| TIMERULE.CREATION_HANDOFF_READY | terminal | 15 | terminal | none | TIMERULE.RULE_COMPLETE_SUMMARY | stop | The Complete Summary is displayed and the verified template and validated immutable FSM CSV ZIP are ready for the provider-owned Data Loader approval preview and import |
| TIMERULE.INPUT_ERROR | terminal | 16 | terminal | none | TIMERULE.VALIDATE_REQUIREMENTS | stop | Input validation fails |
| TIMERULE.LOOKUP_ERROR | terminal | 17 | terminal | none | TIMERULE.FIND_MATCH | stop | Time Rule export lookup fails |
| TIMERULE.TEMPLATE_LOOKUP_ERROR | terminal | 18 | terminal | none | TIMERULE.FIND_TEMPLATE | stop | Time Rule Template export lookup fails |
| TIMERULE.TEMPLATE_PROPOSAL_ERROR | terminal | 19 | terminal | none | TIMERULE.PREPARE_TEMPLATE_PROPOSAL | stop | The joint proposal is incomplete |
| TIMERULE.TEMPLATE_CANDIDATE_DISCLOSURE_REQUIRED | terminal | 24 | terminal | none | TIMERULE.PRESENT_TEMPLATE_CANDIDATES | stop | Candidate template evidence must be disclosed before user selection |
| TIMERULE.TEMPLATE_APPROVAL_REQUIRED | terminal | 20 | terminal | none | TIMERULE.TEMPLATE_APPROVAL_GATE | stop | Explicit approval for the exact joint proposal is missing |
| TIMERULE.TEMPLATE_APPROVAL_DECLINED | terminal | 21 | terminal | none | TIMERULE.TEMPLATE_APPROVAL_GATE | stop | The user rejected the joint proposal |
| TIMERULE.TEMPLATE_APPROVAL_STALE | terminal | 22 | terminal | none | TIMERULE.TEMPLATE_APPROVAL_GATE | stop | The proposal or target environment changed after approval |
| TIMERULE.DEPENDENCY_ERROR | terminal | 23 | terminal | none | TIMERULE.CREATE_DEPENDENCY | stop | Conditional Time Rule creation cannot proceed |
| TIMERULE.EXPORT_READY | terminal | 26 | terminal | none | TIMERULE.EXPORT_MONITOR | stop | Terminal export success, persisted result ZIP, and ZIP validation all passed |
| TIMERULE.EXPORT_ERROR | terminal | 27 | terminal | none | none | stop | Export monitoring reached failure, timeout, missing result, unusable ZIP, partial status, or uncertainty |
| TIMERULE.FINAL_COMPLETION_ERROR | terminal | 29 | terminal | none | none | stop | Task-authorized status monitoring reached failure, timeout, partial success, uncertainty, or read-back mismatch |
| TIMERULE.FINAL_COMPLETION_SUCCESS | terminal | 30 | terminal | none | TIMERULE.FINAL_COMPLETION | stop | Terminal success status and authoritative read-back verification passed for a standalone Time Rules flow |
| TIMERULE.FINAL_COMPLETION_PARENT_RESUME | terminal | 31 | terminal | none | TIMERULE.FINAL_COMPLETION | stop | The prerequisite is verified and ready to resume exactly one active documented parent workflow; present the resume prompt and do not start the parent |
| TIMERULE.PARENT_CONTEXT_REQUIRED | terminal | 32 | terminal | none | TIMERULE.FINAL_COMPLETION | stop | Parent workflow context is multiple, conflicting, stale, incomplete, or undocumented |
