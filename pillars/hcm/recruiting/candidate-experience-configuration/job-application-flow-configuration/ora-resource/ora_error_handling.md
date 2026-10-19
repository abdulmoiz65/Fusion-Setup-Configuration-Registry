# Error Handling and Handoff Gates

## Error Situations

| Situation | What Should Happen |
|---|---|
| Every validation, lookup, design, generation or import error | AF.HANDLE_ISSUES identifies failed stage/rule, relevant input value, accepted values or candidate code/name/version/status, actionable correction, environment/task and safe resume point. Explicitly state whether generation and import occurred; preserve confirmed partial results and errors. |
| Missing or ambiguous source/parent/version | Stop before candidate construction; ask for exact missing identity or candidate choice. Never infer latest or arbitrarily select. |
| Conflict or unsupported field/type/operation | Return exact conflict/value and supported correction; do not overwrite, merge, truncate, silently drop, reuse or auto-rename. |
| Configure block-specific properties for the selected Apply Flow Version | AF.REFUSE_PROPERTIES -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and configure the selected version's block-specific properties manually. |
| Activate or deactivate an Apply Flow | AF.REFUSE_FLOW_LIFECYCLE -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and activate or deactivate the apply flow manually. |
| Delete an existing Apply Flow | AF.REFUSE_FLOW_DELETE -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and delete the apply flow manually. |
| Edit an existing Apply Flow | AF.REFUSE_FLOW_EDIT -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and edit the apply flow manually. |
| Add, edit, or remove blocks in an existing Apply Flow | AF.REFUSE_EXISTING_BLOCK_EDIT -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and add, edit, or remove blocks in the existing apply flow's version manually. |
| Activate a version of an existing Apply Flow | AF.REFUSE_VERSION_ACTIVATE -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and activate the apply flow version manually. |
| Delete an existing Apply Flow Version | AF.REFUSE_VERSION_DELETE -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and delete the apply flow version manually. |
| Edit an existing draft Apply Flow Version | AF.REFUSE_VERSION_EDIT -> AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Apply the Unsupported operation manual handoff: explain that this action is not currently supported through the skill and ask the user to log in to the Oracle Fusion UI and edit the existing draft apply flow version manually. |
| Export failure | Surface the owning export workflow's safe diagnostics, process/log references when available and next-check path; do not claim root retrieval succeeded. |
| Artifact persistence failure | Report safe destination/stage, preserve completed evidence and stop before treating an artifact as ready. |
| Import initiation accepted | Lead with affected flow/version and evidenced accepted-initiation outcome, not creation/completion. Keep identifiers and logs secondary; immediately return Data Set Name, Content ID, Request ID, environment, ORA_IRC_APPLY_FLOW_CONFIGURATION and exact submitted ZIP SHA-256; distinguish accepted initiation from completion. |
| Import failure or uncertain outcome | Preserve known IDs and safe errors; stop before retry, re-upload or resubmission. Do not invent completion from acceptance. |
| Every later handoff failure or refusal | Re-enter AF.HANDLE_ISSUES -> AF.RETURN_ISSUES with the original operation, preview checksum and known request identity. A preview terminal does not erase diagnostics or authorize another submission. |
| Later successful import verification | Only after a later explicitly requested status continuation confirms successful import, use the declared task-level export workflow to retrieve fresh target evidence. Compare requested, imported and retrieved identities, statuses, options, layout, blocks, translations and in-scope associations; retain discrepancies and distinguish imported from verified. Do not execute this during authoring or start an automatic status loop. |
| Later explicit status request | This is a continuation stage of the existing creation operation, not a fifth Operation. Reuse the same Request ID or Content ID through the owning Data Loader workflow; return observed status and safe terminal logs when available. Do not automatically poll to completion. |

## Default Corrections

These field-specific outcomes use AF.HANDLE_ISSUES -> AF.RETURN_ISSUES;
they supplement the common error record, not the owning input/design rules.

| Situation | What Should Happen |
|---|---|
| Status or Description default fails | Show operation, field and invalid value or missing source evidence. Explain Draft-only target status or the supported Description input/translation; request correction without resetting copied text or changing the CreateVersion parent. |
| VersionName cannot be resolved or conflicts | Show exact parent, supplied/chosen name, conflicting names or missing complete parent evidence. Ask for a valid unique name or the missing parent evidence; do not replace an explicit blank/conflicting name, truncate it or regenerate a previewed name. |
| Option value, applicability or provenance fails | Show business option, technical field, resolved type, supplied/source value and applicable Y/N choices; explain inapplicability where relevant. Request corrected input or source evidence, never silently default an invalid explicit value or fabricate copied/defaulted provenance. |
| Layout or page-block default fails | Show the affected section/page/block instance and baseline or text/flag mismatch. Explain the fixed-layout and supported block/text boundary; request the specific supported correction, not an invented layout or activation-time property. |
| Required PageBlockTitle fails | Identify the block and Language, blank value or missing display-name evidence. Resolve omitted titles through resolve_apply_flow_block and the PageBlockTitle default, preserve valid custom text, and require nonblank base/TL values before a new preview. Explicit blank titles require corrected input. If Fusion rejected a submitted version, preserve any successfully created root and do not replay the new-flow package; reconcile target state through the declared workflow before a separately requested and approved new-version recovery. |
| Initial version missing from a create-flow package | Treat the package as incomplete, not successful flow creation. Include the initial Draft version and required descendants under the new root using the supported creation contract, then rerun package validation and preview. A skill edit or earlier failed import approval is not approval for corrected bytes. |
| Availability default fails | Show the affected target/association and identifier, linkage, duplicate or forced-value mismatch without secrets. Correct the candidate before a fresh verified preview; do not reuse source IDs or regenerate approved identifiers silently. |
| Translation source/default fails | Show the exact entity/Language/field and available codes or missing required US text. Ask for the supported language/base-text correction; preserve valid copied rows and intentional empty optional text. |
| Default evidence is absent | Name the field, operation/type and missing prerequisite/source/CSV representation. Stop before readiness until evidence is available; state whether generation or import actually occurred. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing/invalid field, unsupported intent or identity conflict | Show affected value and supported correction; rerun applicable validation after user correction. |
| Catalog mismatch | Wrong/ambiguous task or unsupported CSV flag | Resolve exact catalog task/support through the declared route. |
| Auth/authz | Routed login or privilege check fails | Use owning Auth/export/Data Loader workflow; never disclose tokens or secrets. |
| Transport/environment | Connectivity failure, wrong environment/release | Correct selected connection/evidence and resume safe owning workflow step. |
| Fusion API | Export or approved submission returns a Fusion error | Report safe error and owning workflow's next action without automatic replay. |
| Process timeout | Owning export/status workflow reports its timeout | Report environment, task/job, ProcessId or request ID, last status and elapsed wait from owning workflow; do not define a task-local import poll timeout. |
| Process failed | Owning workflow confirms failed process | Surface safe status/ProcessLog when available and retain partial results. |
| Artifact persistence | Candidate/export/checksum/destination failure | Correct artifact issue before preview or submission. |
| Approval blocker | Exact environment/artifact approval missing or stale | Hold configuration-changing submission and report the exact missing gate. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| AF.RETRIEVE_READY | Selected environment, task name/code, export evidence/timestamp, filter or all-roots scope, root rows with AfCode/ApplyFlowName/AfTypeCode/AfStatusCode, count including zero, completed path and retrieval result. No configuration mutation occurred. |
| AF.NEW_FLOW_PREVIEW_READY, AF.TEMPLATE_PREVIEW_READY, AF.VERSION_PREVIEW_READY | Render the complete Business-first Preview Contract below from exact final CSVs and verified source/parent evidence; return all fields and layout inline before separately labeled Technical details. Never replace the business preview with a loader validation report. |
| Preview-ready terminals | Return operation-specific validated package evidence, the complete business-preview output contract and submission eligibility to the owning runtime for rendering. No import has occurred merely because a preview terminal was reached. |
| Later approval and import handoff | Accept a later clear contextual affirmative for the displayed environment and unchanged ZIP bytes, such as approve, approved, confirm, confirmed, ok, okay, yes, go ahead, proceed, or equivalent relevant wording. These are examples, not a fixed allowlist or exact-string check. Use core.data-loader in FSM mode and its authoritative approval workflow; do not ask again merely to obtain a particular word or spelling. Any material change requires a new preview and approval. |
| Approval interpretation | Evaluate the user's meaning in response to the pending import preview, not keyword presence. Capitalization, surrounding whitespace, punctuation, Markdown formatting, or an obvious typo such as apporved do not invalidate a clear affirmative. A refusal, question, unmet condition, requested package change, quoted example, unrelated acknowledgment, or ambiguous response is not approval. Ask a concise clarification only when intent or the approved target is unclear; never broaden approval to another artifact, environment, operation, or retry. |
| Immediately before submission | The owning core.data-loader FSM workflow rechecks selected environment/release, authorization, task/catalog support, package validation and unchanged ZIP SHA-256 against the exact approved preview. Any failed check blocks import; a preview or approval never overrides missing authorization or invalid artifact evidence. |
| Approved eligible submission | Submit exactly once through core.data-loader; return accepted IDs immediately. No resource-local import execution or direct REST write. |
| Later status continuation | Lead with affected flow/version and evidenced outcome; keep the same request identity and safe logs secondary, and state whether terminal. Never substitute a new upload/submission. |
| Unsupported operation manual handoff | For all eight use cases in Error Situations, use a concise response: This action is not currently supported through this skill. Please log in to the Oracle Fusion UI and perform the requested action manually. I have not made any changes for this request. Replace this action and requested action with the specific operation the user asked for; distinguish activate from deactivate and add from edit or remove. For multiple unsupported requests, name each requested action in one compact response. Preserve supplied names as context, not verified identities. Explain the skill limitation, not that the action is impossible in Fusion. Do not ask for execution approval, credentials or details needed only for execution; offer skill extension or new-flow/new-version creation as a substitute; or invent UI navigation steps. |

## Preview Handoff Record

| Value | Required handoff behavior |
|---|---|
| Task and branch | Preserve ORA_IRC_APPLY_FLOW_CONFIGURATION, Job Application Flow Configuration, the selected operation and its distinct preview-ready terminal. |
| Immutable approval binding | Preserve environment/release, source or parent, frozen target identity and generated association IDs, immutable ZIP path, SHA-256, full preview and validation result; verify the same checksum immediately before submission. |
| Request state | Before acceptance, record that import has not occurred. After acceptance, retain Data Set Name, Content ID and Request ID with the original environment, task and checksum; accepted initiation is not completion. |
| Resume | A later contextual approval resumes only the owning Data Loader handoff after its environment, authorization, catalog, package and approval-binding checks. A later explicit status request resumes the same accepted request; no new upload or submission. |
| Errors | Report the failed value/candidates, correction and actual generation/import state through AF.HANDLE_ISSUES -> AF.RETURN_ISSUES. Preserve partial successes and safe logs without credentials or sensitive payloads. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or stale preview approval | No import. A request to design, create a ZIP, look up data or approve a different artifact is not contextual approval to import these bytes into the displayed environment. |
| Accepted import or pending status | No automatic polling, task-local poll timeout, retry, re-upload or resubmission; acceptance is not completion. |
| Activation or existing-record changes | Never activate/deactivate/delete flows, activate/delete/edit versions, or change blocks in an existing version. |
| Unsupported operation manual handoff | Do not launch a browser, log in for the user, call an API, export, generate an import package or execute any of these eight actions as a fallback. The user performs login and the requested action manually in the UI; do not claim either occurred. Preserve supported Retrieve, DesignNew, CreateFromTemplate and CreateVersion behavior when separately requested, but never silently replace an unsupported existing-object operation with creation. |
| Authoring this guidance | No authentication, Fusion API call, live export, ZIP generation/import, polling or activation. Runtime instructions describe the later invoking workflow; authoring does not execute them. |


## Business-first Preview Contract

These are mandatory output fields and ordering for all three creation
preview-ready terminals. The owning runtime renders them; this resource
does not create another route, renderer, processor or import operation.

| Gate | What Must Be Shown |
|---|---|
| Evidence before wording | Derive every displayed value from the final prepared CSV package and verified source/parent export evidence, not intended inputs, assumed factory defaults, screenshots or another ZIP. Reconcile names, counts, order, options and translations against the exact final bytes; stop and correct any disagreement before approval |
| Opening sentence | Explain in plain language what will be created and that it has not yet been created in Fusion. DesignNew/CreateFromTemplate: one new Draft Apply Flow and one Draft version. CreateVersion: one new Draft version under the existing parent, not a new Apply Flow |
| Setting / Value summary | Show target environment and release, operation, Apply Flow Name, Apply Flow Code, Application Flow Type business label, Version Name, applicable root/version status, actual Description or Not provided, and activation: Will not be activated. Template: identify exact source flow/version. Version: identify existing parent; clearly label parent name/Description/root status as unchanged evidence, not imported fields |
| Complete configured layout | Show an inline Section / Page / Blocks in order table or nested numbered list in actual configured sequence. Include every section and page, even empty pages, and every repeated block instance. Use canonical business block names and display populated custom title/instructions. Derive totals from the same data; counts alone or a link to another preview cannot replace the complete layout |
| Recruiting Types | Show selected business Meanings, Not selected for an eligible External flow without associations, or Not applicable for other types. For CreateVersion distinguish inherited unchanged parent associations from imported version data; never imply an association was added |
| Applicable options | Show every applicable option with its business label and Enabled for Y / Disabled for N, using final CSV values. Identify copied/defaulted/explicitly overridden provenance accurately from retained evidence; an empty inapplicable field must not be described as Disabled |
| Selection and value provenance | State whether blocks were explicitly selected or inherited from omitted-input defaults/source. Reconcile each instance to that selection and each checkbox to its supplied Y/N or omitted-field fallback. Never describe unrequested extra blocks or overwritten checkbox values as defaults; correct the candidate before approval |
| Text and languages | Include actual Description and all populated supported block titles/instructions, available Language codes and a compact Language / Field / Resulting value table for explicit overrides, identifying the target entity when needed. State whether remaining translations copy US text or preserve existing template translations. Keep a complete field-level listing with entity keys, Language, values and SourceLang in the detailed preview if lengthy |
| Changes and warnings | Template: show selected source and actual target differences from verified source evidence, including required target identity/Draft status, omitted property-child rows and supported explicit overrides. Version: state parent is unchanged. Explain deduplicated requests and material warnings without implying silent edits |
| Design versus submission | Separate Prepared/Validated design status from Not submitted/Submitted/Failed/Succeeded submission status, each based on evidence. Show the complete configuration even if submission is blocked. Explain the prerequisite and next action in plain language; do not put internal router quotes or state-property names in the main business summary |
| Technical details second | After the business summary, provide a separately labeled Technical details section or linked immutable detailed-preview artifact with ZIP filename/link, SHA-256, generated identifiers, per-file row counts, header-only members, schema/archive validation actually performed and safe logs. Keep technical evidence available for audit and exact-package binding, never as a substitute for the business layout. Keep usage/audit reporting separate |
| Approval only when eligible | After business and technical details, identify the exact target environment and immutable package link/checksum and ask whether to upload and initiate that load only when the owning workflow permits submission approval. Accept contextual approval as defined in Disclosure Rules; do not prescribe a required reply word. If a prerequisite is unmet, show the blocker and next action instead; approval cannot bypass it. Revalidate environment, authorization, task/catalog support, package and approval binding immediately before Data Loader |
| Approval binding and changes | Bind the user's contextual approval to the exact environment, task, immutable package and SHA-256. Any input/environment/release/row/byte/checksum change requires a fresh reconciled preview and approval. Do not ask twice for the same unchanged task action |
| Result language | On accepted initiation or a later explicit result request, lead with affected flow/version and evidenced outcome; request IDs and logs follow. Accepted initiation is neither creation nor completion. Do not say created before successful import evidence; distinguish imported from subsequently verified |
| No implicit follow-up | Submission is once through core.data-loader FSM. No automatic polling, status request, retry, re-upload, resubmission or activation. Later explicit status reuses the same request; a preview terminal is not a new execution route |

## Preview Acceptance Specifications

| Check | Required outcome | Status |
|---|---|---|
| Defaults and design gate coverage | All twelve coverage areas have applicable node/handoff evidence; missing defaults, source evidence or gates block readiness instead of silently passing | Documented |
| DesignNew business preview | New Draft root/version opening, package-backed settings/options/text, all actual layout rows and every block instance, translations and technical evidence; not yet created | Documented |
| Explicit blocks for every supported type | ORA_EXTERNAL, ORA_PADC, ORA_TALENT and ORA_EVENT use exactly the explicitly selected valid blocks; no factory extras. External Contact Information plus Review excludes Profile Import, Address and other defaults; PADC Questionnaire alone excludes other blocks; Talent Community Contact Information alone excludes Profile Import; Event Contact Information alone excludes Profile Import. Required-block conflicts stop without silently adding anything | Documented |
| Omitted blocks for every supported type | With no block information, DesignNew/CreateVersion uses that AfTypeCode's factory block membership: External 10, PADC 0, Talent Community 2, Event 2. Preserve fixed sections/pages. Checkbox input alone does not suppress this block fallback | Documented |
| Explicit checkbox values | For any applicable option on any supported AfTypeCode, explicit Y stays Y and explicit N stays N, even when opposite to the default or copied value. For example Event Legal=N and SingleClick=Y remain N/Y; omitted Event options yield Y/N. Inapplicable or invalid supplied values block rather than default | Documented |
| Partial checkbox input | Resolve options independently: Event Legal=N with SingleClick omitted yields N/N; Event SingleClick=Y with Legal omitted yields Y/Y. Block selection does not suppress option defaults and supplied options do not introduce unrequested blocks | Documented |
| Candidate revision and templates | Before import, adding block information replaces default/copied membership and removes excluded block translations; changing an option preserves its exact supplied Y/N. Retained source text remains unchanged. Changed candidate bytes require a new preview and approval; already created flows/versions are never edited by this policy | Documented |
| Create-flow wording without a version request | Create apply flow, create applyflow or createapply flow selects the new-flow branch with one Draft root and one initial Draft version; omitted VersionName becomes Version 1. The preview and final version CSV include it without a separate version question; missing identity/type still follows existing input gates | Documented |
| Default display-name titles | Every omitted newly constructed title uses exact BlockName from its unique BlockCode match, including repeated instances. ORA_NAME_CONTACT_INFO yields Contact Information, ORA_DQ_QUESTIONS yields Job Application Questions and ORA_SUMMARY yields Review; base and US titles agree and all required TL titles are nonblank | Documented |
| Custom and copied titles | Valid explicit custom title wins; otherwise preserve nonblank copied template titles/translations. Default only missing/blank copied titles, seed required TL values from final US text, and preserve unrelated text and valid translated overrides | Documented |
| Title blockers | Explicit null/empty/whitespace title, blank language override, unresolved/duplicate BlockCode or blank inventory BlockName fails before preview; empty optional PageBlockInstructions remains valid | Documented |
| Version and title byte gates | Reject a root-only package, a header-only version member, multiple versions, wrong parent linkage, missing required descendants or any blank base/TL block title. Reject the earlier empty-title shape even if archive structure and headers pass | Documented |
| CreateFromTemplate business preview | Source flow/version and actual differences; copied non-factory layout and supported translations preserved; explicit changes accurately displayed | Documented |
| CreateVersion business preview | One new Draft version under exact parent; parent fields and associations labeled unchanged, root/root-TL/availability excluded from import | Documented |
| Layout and totals reconciliation | Every final CSV section/page/block instance appears in configured order, including empty pages and reusable repeats; totals match the same package | Documented |
| Translation reconciliation | US defaults versus preserved template values accurately identified; explicit overrides list exact Language/entity/field/result and do not alter other rows | Documented |
| Blocked submission | Full prepared configuration still appears; plain-language prerequisite/next action replaces approval solicitation, while technical evidence remains available | Documented |
| Outcome accuracy | Design/submission/verification distinguished; accepted initiation is not completed creation; no polling/retry/activation introduced | Documented |
| Contextual affirmative | After an eligible import preview, approved, confirm, ok, an affirmative sentence, or equivalent wording authorizes only that displayed load; capitalization, Markdown, whitespace and an obvious typo do not force another approval prompt | Documented |
| Non-affirmative response | Do not approve, not yet, confirm what?, a quoted approval example, an unrelated ok, or an unmet condition does not authorize submission; interpret context rather than matching an affirmative substring | Documented |
| Approval with a requested change | Ok, but change the name or use another environment requires the requested change, fresh validation and a new preview before approval of the changed load | Documented |
| All eight unsupported operation requests | Block properties; flow activation/deactivation, deletion or editing; adding/editing/removing existing blocks; version activation, deletion or Draft editing each follows its existing refusal path to the same manual UI message. No approval prompt, skill-extension offer, automated login, external call or substitute creation; supported new construction remains unchanged | Documented |

Documented is a specification, not runtime evidence. Tested—Pass requires an
actually executed check with date, local or environment context, and evidence.
Compilation and graph checks alone do not prove package rendering or import.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AF.RETRIEVE_READY | terminal | 70 | terminal | none | AF.FILTER_RETRIEVE | stop | Retrieve. Return retrieved roots and export evidence. |
| AF.NEW_FLOW_PREVIEW_READY | terminal | 320 | terminal | none | AF.VALIDATE_NEW_FLOW_PACKAGE | stop | DesignNew. Return new-flow guidance; not import permission. Return the complete Business-first Preview Contract and Preview Handoff Record from this file for the owning runtime; show prepared configuration even if submission is blocked; no import permission. |
| AF.TEMPLATE_PREVIEW_READY | terminal | 340 | terminal | none | AF.VALIDATE_TEMPLATE_PACKAGE | stop | CreateFromTemplate. Return template guidance; not import permission. Return the complete Business-first Preview Contract and Preview Handoff Record from this file for the owning runtime; show prepared configuration even if submission is blocked; no import permission. |
| AF.VERSION_PREVIEW_READY | terminal | 370 | terminal | none | AF.VALIDATE_VERSION_PACKAGE | stop | CreateVersion. Return new-version guidance; not import permission. Return the complete Business-first Preview Contract and Preview Handoff Record from this file for the owning runtime; show prepared configuration even if submission is blocked; no import permission. |
| AF.HANDLE_ISSUES | step | 490 | error_handler | success->AF.RETURN_ISSUES;failure->AF.RETURN_ISSUES | none | stop | Any failure/refusal. Return a friendly correction with field/value/candidates and operation stage; retain safe evidence. For any of the eight unsupported operation cases in Error Situations, apply the Unsupported operation manual handoff in Disclosure Rules; explain the current skill limitation and direct the user to log in to the Fusion UI and perform the specific requested action manually. |
| AF.RETURN_ISSUES | terminal | 500 | terminal | none | AF.HANDLE_ISSUES | stop | Any failure/refusal. Stop current attempt and request only the missing input or correction. For any of the eight unsupported operation cases, return the manual UI handoff without an execution-approval question, skill-extension offer or substitute creation. |
