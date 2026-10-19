# Assign Default Process Owners Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The Risk Management search setting is absent or disabled | Before owner coverage, show the business-labelled approval table. On fresh approval, delegate the single setting change and verification to the Profile Options Core skill. |
| The search-setting definition, Site capability, change, or final verification is unavailable or unsuccessful | Stop before owner coverage. State that Risk Management search could not be confirmed, that no owner review or assignment started, and ask an administrator to enable the setting before resuming. Do not expose profile codes, values, endpoints, request identifiers, or privilege mechanics. |
| Approval to enable the search setting is withheld | Make no change and stop before owner coverage. State that no owner review or assignment started and retain only redacted phase evidence. |
| A required process, current-owner, department, department-bounded worker, hierarchy, or BOSS-user read is missing, malformed, incomplete, or ambiguous | Stop the affected stage. Preserve only redacted diagnostics and request the missing customer decision or a corrected Core result. An optional Business Unit lookup does not block functional discovery. |
| Current owner coverage is complete but has not been rendered to the consultant | Render the complete Markdown coverage table in chat before asking for a selection. A persisted artifact, count summary, or bullet list is not a coverage review. |
| A Level 2 coverage row omits one or more catalog members | Do not show or refresh that row. Re-read every unique member in the complete catalog scope, aggregate their owner states, and then render the Level 2 row. A complete one-member scope is valid. |
| A Level 2 catalog scope has duplicate member identities or multiple self-named roots | Do not show, approve, or mutate that Level 2 row. Re-read the complete catalog; if the duplicate or root ambiguity remains, report a catalog mismatch and stop the scope. No self-named root is valid. |
| An optional HCM display-name read is unavailable | Retain the verified Fusion username as the candidate label. Do not block the owner review or infer another person's name. |
| Optional candidate job, department, position, manager, assignment, or person-detail evidence is absent | Retain the verified eligible candidate. Do not infer the missing value; lower confidence and present alternatives when the available evidence is equivalent. |
| Candidate evidence contains an explicit inactive or ineffective result | Exclude that candidate from recommendation ranking. Do not replace it with an inferred person; continue only with other verified eligible candidates or present the no-candidate exception. |
| Multiple candidates share the strongest functional-evidence tier | Present equivalent alternatives and require consultant selection. Stable internal ordering must not be presented as a business preference. |
| A read returns 401 or 403 after the Core client applies its permitted refresh behavior | Classify the result as authentication or authorization failure. Do not treat the requested record as absent. |
| Every requested manager-hierarchy read returns HTTP 200 with an empty final collection | Complete the hierarchy stage. Do not request a manager identity when there is no manager row; retain verified functional-worker identities for ranking. Report that no reporting relationships were returned; do not diagnose an access failure. |
| A process has no unique supported match | Do not select a value automatically. Present supported choices or re-prompt for the process selection. |
| A member has a valid assigned owner tuple but no explicit individually named Level 2 UPDATE or RESET request | Preserve it as informational. Normal CREATE may still fill other unassigned members in that Level 2 scope; do not prepare a replacement or reset for the assigned member. |
| An exact member property has a blank/null owner code | Treat exactly one supported USER/GROUP property as `EMPTY_PROPERTY`, hence unassigned. For CREATE, require one matching `$id`, record `REPLACE_EMPTY_PROPERTY` in the redacted receipt, and use the documented bulk DELETE/CREATE replacement. For UPDATE and RESET, preserve it as already unassigned. An unclassifiable blank-code property is ambiguous and stops the member. |
| A changed existing UPDATE or RESET member lacks one current property whose `$id` equals its valueCode | Mark that member unsupported, preserve its owner, and request a corrected current-owner result. Do not infer a direct item endpoint. |
| Current property state is stale, unavailable, or inconsistent with the reviewed operation | Before approval, cancel the Level 2 scope when its aggregate action plan has changed and require a fresh review. After approval, cancel the stale member and stop remaining requests in that scope. A CREATE member that gained a valid owner type/code, an empty-property CREATE member with a missing/nonmatching `$id`, an UPDATE member whose exact source owner changed, or an ambiguous property is stale. An absent or blank-code RESET member is unchanged. |
| The hidden action plan repeats a member identity | Cancel the Level 2 scope before its first bulk request. Re-read the catalog and rebuild the unique scope; require a fresh review and approval. Never submit two bulk requests for one member. |
| A create, update, or reset fails or has an uncertain outcome | Do not retry the write automatically. Retain redacted status, safe pre-write property state, selected mutation path, endpoint path, and request identifier or ECID when supplied; reconcile with the current-owner read. |
| One create, update, or reset member fails | Stop remaining requests in that Level 2 scope. Do not retry or compensate; retain aggregate counts in the internal diagnostic and report the Level 2 process, operation, safe result, and next action. |
| A post-mutation property read does not match the approved result | Mark that target as verification failure. Do not report it as complete or submit another mutation without a new review and approval. |
| Every planned member change in an operation verifies successfully | Re-read the complete process and current-owner inventories and render the full Level 2 coverage table. If any members remain unassigned, remain in this skill and ask the normal assignment-selection question. If none remain unassigned, record a completed-and-verified result. An explicit consultant deferral while work remains is recorded as deferred, not complete. |
| A project artifact or run record cannot be written safely | Stop before a mutation when possible, preserve a redacted diagnostic in a safe location, and report artifact persistence failure. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required process selection, hierarchy selection, approved decision, or artifact destination is missing or invalid | Correct the missing or invalid input before continuing. |
| catalog_or_metadata_mismatch | A process cannot be uniquely matched, or the expected property result shape is unavailable | Present supported candidates or record the mismatch and stop the affected target. |
| auth_expired_or_invalid | Core reports an unusable OAuth session after its permitted refresh | Re-authenticate through Core, then restart the blocked read. |
| authorization_or_privilege | Core reports 403 or missing BOSS/Fusion privilege after refresh | Stop and request the required read, create, update, or delete privilege for the requested operation. |
| transport_or_environment | Core cannot reach the selected environment or returns an incomplete page set | Stop and repeat only the affected read through Core after the environment is available. |
| fusion_api_error | Core reports a rejected or uncertain create, update, or reset, or post-mutation verification fails | Reconcile with the current-owner lookup; require a new approved plan before another mutation. |
| artifact_persistence | Redacted project artifact or run record cannot be persisted | Stop before live work and correct the safe destination. |
| approval_blocker | The current owner state, exact target set, or explicit approval is missing or changed | Refresh preview and obtain approval for the unchanged request set. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Department or department-bounded worker lookup failure | Business process, safe result category, whether a choice is required, and one next action. Do not request a Business Unit mapping. |
| Apply approval | Exact target environment, one Level 2 row per requested operation, approved owner choice or reset result, and confirmation that the hidden request set is unchanged. |
| Mutation or verification failure | Affected Level 2 process, operation stage, redacted status and error summary, safe property state and selected mutation path, request identifier or ECID when available, and one safe recovery action. |
| Partial outcome | Level 2 process, operation, safe result, and next action. Retain aggregate counts in the internal diagnostic. |

## Consultant-facing exception language

Use the consultant interaction contract before disclosing an error. Present a
compact table with **Item**, **Business impact**, **Current result**, and **Next
action**. Do not show the result category, endpoint, request identifier,
pagination state, or raw diagnostic to the consultant. When completed hierarchy
reads return no rows, say that no reporting relationships were returned and no
owner was proposed or assigned. Offer an exact Fusion username or HCM validation
of reporting relationships and functional worker information. Do not request a
Business Unit or Business Unit-to-process mapping.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any required lookup is incomplete or ambiguous | Do not present the affected process as proposal-ready or apply-ready. |
| A live mutation lacks an unchanged approved scope plan | Do not submit a bulk POST. |
| A create, update, or reset fails or has uncertain outcome | Do not retry a bulk POST automatically, infer success, or compensate another member. |
| Existing owner state is returned without an explicit individually approved operation | Do not replace, overwrite, or reset it. |
| A diagnostic contains credentials, token values, raw authorization headers, or unnecessary identity data | Do not print or persist it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DPO.ENABLE_SEARCH_SETTING | decision | 6 | execution_gate | changed->DPO.REVERIFY_SEARCH_SETTING;not_approved->DPO.RETURN_ISSUES;blocked->DPO.HANDLE_ERROR;failure->DPO.HANDLE_ERROR | DPO.VERIFY_SEARCH_SETTING | stop | A disabled Site search setting requires a fresh approval, current Core preflight, one Core-managed create or update, and final verification. |
| DPO.PREVIEW_READY | terminal | 70 | terminal | none | DPO.LOOKUP_OWNER_PROPERTIES | continue | The complete current owner coverage review is ready to show or refresh for process selection. |
| DPO.CANDIDATE_REVIEW_READY | terminal | 75 | terminal | none | DPO.LOOKUP_DEPARTMENT_WORKERS | continue | Required process, department-bounded worker, and current-owner reads are complete and the workflow may continue to candidate review. |
| DPO.HANDLE_ERROR | step | 80 | error_handler | handled->DPO.RETURN_ISSUES | none | stop | Any required lookup, approval, create, update, reset, verification, or artifact gate is blocked. |
| DPO.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | A blocking issue was disclosed with one safe next action. |
