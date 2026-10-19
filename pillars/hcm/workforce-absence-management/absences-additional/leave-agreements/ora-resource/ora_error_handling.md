# Leave Agreements Error Handling

Use business-facing labels and display values in requester-visible errors and corrective actions. Keep raw Data Loader or REST attribute names, stored codes, surrogate identifiers, resolver names, lookup types, and endpoints internal unless the requester explicitly asks for technical details or the diagnostic requires implementation-owner action.

For an AC1 list, zero or multiple matches are valid. Do not report ambiguity
merely because several agreements match the requested Legislation and As-of
Date. If any page or child section fails, show the verified rows and name the
incomplete portion; do not claim a complete list or a blank child collection.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A dated Update, Correction, End date, Delete changes, or caller-selected ZAP operation is requested | Explain that this Redwood template has one current version and the requested operation is unavailable. Present applicable View, Create, Edit, or Delete choices without performing a substitute action or marking the supported task unavailable. Internal date-free ZAP remains the loader mapping for current whole-object Delete |
| An applicable create field, exact existing identity, or changed-field dependency is missing | Name only the missing applicable business value and stop the affected preparation. Create may need Name, Pattern, Legislation, Start Date and plan mappings; plain parent Edit/Delete require exact current identity and full before state rather than a new operation date or replacement child plan IDs |
| Full before state or an affected child cannot be retrieved for Edit/Delete | Report the unavailable parent field or child section and block only that execution; do not substitute an identity-only result or an empty collection for missing evidence |
| A selected Edit/Delete action or changed field lacks current adapter support | Report the supported business operation and the specific missing action/field mapping. Preserve the draft and obtain the current contract through its declared metadata path; do not invent date controls or declare Edit/Delete functionally unavailable |
| Fusion reports ANC-3405183 or says valid plan information is required | Compare the action and source with the full configuration and current section contract. For Create or new/changed entitlements, collect the missing Target Plan or Conversion mapping. For a plain parent Edit, inspect lost parent/child binding or an unsupported source shape before asking for replacement plan IDs; rebuild and revalidate before a new preview |
| An exact Target Plan search returns no match after applying the Agreement plan type, active status, legislation, and effective-date filters | Report the requested Target Plan, Legislation, and effective business date; request a corrected exact Target Plan name and stop before Data Loader preparation. Do not broaden or remove any resolver filter |
| An exact Target Plan search returns multiple matches | Report the ambiguity without choosing the first row; request corrected business context or a plan identifier using business-facing wording and stop before Data Loader preparation |
| A Target Plan resolves with a non-Agreement plan type, inactive status, different legislation, or incompatible effective date | Classify a lookup-resolution failure and request a compatible active Agreement Target Plan; do not reuse a plan found under another type, status, legislation, or date |
| A supplied plan identifier conflicts with the identifier resolved from Target Plan name | Classify input validation and request correction of the Target Plan name or identifier; do not choose one value as authoritative |
| An exact Source Absence Type search returns no match after applying the maternity-pattern and legislation filters | Report the requested Source Absence Type and Legislation; request a corrected exact name and stop before Data Loader preparation. Do not broaden or remove either resolver filter |
| An exact Source Absence Type search returns multiple matches | Report the ambiguity without choosing the first row; request a more precise Source Absence Type or its identifier and stop before Data Loader preparation |
| A resolved Source Absence Type does not return exactly one plans child link when SourcePlanName is supplied | Classify lookup resolution and stop before Source Plan or Data Loader preparation; do not construct the child URL from numeric SourceAbsenceTypeId |
| An exact Source Plan search through the returned plans child link returns no match | Report the requested Source Plan and Source Absence Type; request a corrected exact Source Plan name and stop before Data Loader preparation |
| An exact Source Plan search returns multiple matches | Report the ambiguity without choosing the first row; request a more precise Source Plan or its identifier and stop before Data Loader preparation |
| A supplied Source Plan identifier conflicts with the identifier resolved from Source Plan name | Classify input validation and request correction of the Source Plan name or identifier; do not choose one value as authoritative |
| A lookup returns no match or multiple matches | Show the supplied safe value and resolver classification, then request one precise value |
| Legislative Grouping does not resolve in the selected legislation | Report the requested grouping and Legislation, clear the unresolved technical value, and request one exact compatible grouping; do not remove the legislation-tag scope |
| A formula or Eligibility Profile name returns zero or multiple exact matches | Report the requested business name and kind, stop before source preparation, and request one exact name or an identifier only if needed to disambiguate; never select the first row |
| A Denial Reasons or Withdrawal Reasons list contains an unresolved, ambiguous, or duplicate item | Reject the complete list, preserve its requester order for correction, and do not serialize a partial comma-separated code value |
| Event Type is supplied for Conversion | Classify input validation, remove the incompatible value, and explain that Event Type applies only to Agreement |
| Eligibility Formula and Eligibility Profile are both supplied or conflict with Eligibility Rule | Classify input validation, clear stale incompatible values, and request only the dependency selected by the rule |
| Override Allowed is supplied without a Payment Percentage Display Formula in the same plan item | Classify dependency mismatch and request the formula first; do not default Yes or No |
| A Certification Name or identifier does not resolve as active documentation in the selected legislation | Report the requested Certification Name and Legislation, stop before child preparation, and request one exact compatible name; do not broaden classification, status, or legislation filters |
| A Certification is not effective on the leave agreement Effective Start Date | Report the Certification Name, its effective start and end dates, and the agreement Effective Start Date using business-facing labels. Explain that the Certification must be effective on the agreement start date, then request a compatible Certification or a corrected agreement date and stop before Data Loader preparation |
| Legislation or the leave agreement Effective Start Date changes after Legislative Grouping or Certifications were resolved | Invalidate and clear the prior grouping after a legislation change and invalidate every prior certification identity after either context value changes; require re-resolution before source preparation |
| Current lookup values differ from the captured defaults | Use the current read-only lookup result and stop before applying an unsupported default |
| An existing agreement cannot be resolved exactly | Stop the affected view or maintenance preparation and request Name, Legislation, or Status using business-facing labels; request an identifier only to resolve remaining ambiguity. Do not request a new operation date or assume date-slice selection |
| The registered Data Loader business object or UCM template is unavailable or mismatched | Classify a metadata or catalog mismatch and stop before source preparation |
| A loader source contains a direct REST request header, action payload, audit field, response-only meaning, or unknown section | Classify input validation, identify the field or section, and rebuild from the current template |
| EffectiveStartDate and RangeStartDate are both omitted for a new parent Create | Default the normalized parent Start Date to the current system date in YYYY-MM-DD format, derive native Create RangeStartDate context where required, and disclose the applied default |
| Create EffectiveStartDate and RangeStartDate differ | Classify as input validation and require one matching parent business Start Date; do not choose one silently |
| Edit or Delete omits a new operation date | Continue when exact current identity, before state and applicable gates pass; derive Edit's internal RangeStartDate from verified stored Start Date and date-free RangeMode=ZAP for whole-object Delete |
| Child Create under an existing parent requires native date context but the stored parent Start Date is unavailable | Stop that child preparation and retrieve the stored parent context through the declared full-detail lookup. Do not replace it with the current date or ask for a new parent operation date |
| Edit or Delete contains caller-authored effectiveOf, a new range date, or a mode other than internal CORRECTION for Edit or date-free ZAP for whole-object Delete | Classify input validation and source shape. Derive Edit's internal `RangeMode=CORRECTION;RangeStartDate=<verified stored Start Date>` or whole-object Delete's `RangeMode=ZAP`, rebuild and invalidate any prior approval |
| Edit or Delete proposes physical stored-date changes | Compare with the full before state and current UI field permissions. Exclude those date changes unless the UI explicitly permits them and current adapter evidence supports the exact field; otherwise explain the unavailable change and preserve the supported edits |
| A create source client-defaults EffectiveEndDate to 4712-12-31 | Remove the unsupported default unless the current Data Loader template requires the field |
| EffectiveStartDate exists only in DAT METADATA | Continue; header presence is not a populated physical date. Validate the corresponding data-record value separately |
| Native Create populates physical EffectiveStartDate while its required effectiveOf context is absent | Classify a create source-shape failure. Leave the physical data value blank by default, derive required RangeStartDate from the new parent business Start Date or known stored parent context, and revalidate; source changes invalidate prior approval |
| Native Create populates physical EffectiveStartDate and RangeStartDate inside effectiveOf with equal normalized dates | Block unless explicit current create-section evidence proves dual-population support; template presence alone is insufficient. Otherwise blank the physical value, revalidate and invalidate prior approval |
| Native Create physical EffectiveStartDate and RangeStartDate inside effectiveOf conflict | Classify input validation and source shape and stop. Never infer precedence or permit a mismatching-date override |
| Fusion rejects native Create effectiveOf or Edit/Delete action controls | Stop as a source-shape or metadata mismatch and refresh the selected action contract. A returned requirement for an Effective-Of header on whole-object DELETION must be reconciled against the documented date-free ZAP mapping before a new source and approval; never replay the failed load automatically |
| Fusion returns HTTP 401 or 403 for a read-only lookup | Classify authentication or authorization; refresh a rejected cached token at most once for the read-only operation |
| Data Loader validation or initiation fails | Preserve the exact task, stage, request ID when available, and redacted Fusion diagnostic; stop and follow core.data-loader recovery guidance |
| A mutation has an uncertain result | Reconcile through safe Data Loader status or read-only lookup evidence; never replay automatically |
| Delete scope or known protection review is missing | Resolve the exact current parent and full known child inventory before preview; disclose unknown downstream references. Fusion enforces dependency restrictions at load. Never infer cascade behavior or absence of references; a known protection constraint blocks preparation |
| A prepared Delete lacks immutable approval | Present the exact reviewed environment, current object/child, deletion scope and applicable impact through core.data-loader's approval gate; stop before submission, with no extra approval prompt |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields, pattern shape, date format, length, or source-field rules fail | Correct the identified input and rerun validation |
| Lookup resolution | A pattern, legislation, grouping, formula, reason, event type, eligibility profile, plan, source type, certification, plans child link, code, or existing template does not resolve exactly once or is not valid in the required effective-date context | Supply one precise supported business value that is valid in the required context or restore the required returned child link |
| Dependency mismatch | An applicable create or changed-field dependency, full before state, or affected-child context is incomplete | Correct only the affected dependency or retrieve missing state and rerun validation; do not demand new plan IDs for unrelated parent edits |
| Catalog mismatch | BusinessObject absenceLeaveAgreementTemplates is not registered or resolves ambiguously | Correct the registration or exact business-object selection |
| Metadata validation | The current UCM template is missing, stale, or incompatible with the source | Refresh metadata and rebuild the source |
| Source shape | Native Create context is absent or invalid, Edit/Delete has unsupported range controls, or physical date values violate the action-specific rule | Correct the selected action's source shape, regenerate the artifact, and invalidate prior approval |
| Authentication or authorization | A read-only metadata or lookup call returns 401 or 403 | Correct access or refresh an eligible cached token once; do not retry a mutation |
| Fusion API | Fusion rejects a lookup contract or business value | Preserve the redacted diagnostic and correct the contract or value |
| Approval blocker | A mutation lacks an immutable core.data-loader preview and explicit approval | Complete the Data Loader approval workflow |
| Process failed | An approved Data Loader request is rejected or completes with errors | Retrieve available status and errors through the declared core workflow, persist redacted diagnostics, and prepare a corrected source with fresh approval; never replay automatically |
| Unsupported operation | Dated Update, Correction, End date, Delete changes, or caller-selected ZAP conflicts with the current-version Redwood scope | Explain the unavailable intent and offer applicable View/Create/Edit/Delete choices; do not report all supported flows blocked. Internal ZAP is reserved for whole-object Delete |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Business-facing field or section, safe supplied value, violated rule, and one corrective action; do not expose the raw attribute name unless technical details were requested |
| Lookup failure | Safe requested business value, zero or multiple match classification, and requested correction; keep resolver, lookup type, endpoint, stored code, and identifier internal unless implementation-owner action requires them |
| Successful agreement search | Current Name, Pattern, Legislation, Status and available Start Date using display values. Distinguish discovery from a full configuration view; an available stored End Date does not establish date-effective maintenance. Keep identifiers, codes and endpoints internal |
| Target Plan lookup | Requested Target Plan, resolved Legislation, normalized agreement business date, active Agreement-plan filter, match count, and resolved plan name, status, and effective dates. Keep the mapped plan identifier internal unless technical details were requested |
| Certification lookup | Requested Certification Name, resolved Legislation, leave agreement Effective Start Date, match count, and the resolved Certification name, status, Effective Start Date, and Effective End Date. Keep the mapped certification identifier internal unless technical details were requested |
| Source Absence Type lookup | Requested Source Absence Type, resolved Legislation, maternity-pattern filter, match count, and resolved name, status, and effective dates. Keep the mapped identifier and legislative data group internal unless technical details were requested |
| Source Plan lookup | Requested Source Plan, resolved Source Absence Type, match count, and resolved Source Plan name. Keep the returned child link and mapped plan identifier internal unless technical details were requested |
| New LOV lookup | Requested business label and value, applicable Agreement Type or Legislation context, match count, and resolved business name or meaning. Keep lookup types, endpoints, codes, and identifiers internal unless technical details were requested |
| Multi-select reason lookup | Ordered requested and resolved Denial Reasons or Withdrawal Reasons and any failing item; do not expose or partially persist the comma-separated technical code representation |
| Dependency failure | Selected pattern, missing source or target dependency, and correction needed |
| Metadata failure | Target environment name, BusinessObject absenceLeaveAgreementTemplates, failed metadata stage, and safe next action |
| Data Loader handoff | Exact task, REST mode, BusinessObject absenceLeaveAgreementTemplates, validated values, unresolved items, target environment, and approval state |
| Operation-specific loader handoff | Create: normalized parent Start Date and native control. Edit: exact current identity and verified stored Start Date mapped to internal RangeStartDate. Whole-object Delete: exact identity and date-free RangeMode=ZAP. Include changed fields/children and applicable impact. Keep raw controls in technical artifacts and show the business effect in final review |
| Applied create-date default | Exact current system date used in YYYY-MM-DD form and confirmation that neither EffectiveStartDate nor RangeStartDate was supplied |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct POST, PATCH, DELETE, upsert, child write, custom action, or batch request is proposed | Do not invoke or author a direct REST mutation; route exclusively through core.data-loader in REST mode with BusinessObject absenceLeaveAgreementTemplates |
| The POST-based findByAdvancedSearch action is proposed as a lookup | Do not use it; use documented GET finders and local exact matching |
| A lookup is ambiguous | Do not choose the first row or infer a code |
| An ordinary requester interaction is presented | Do not expose raw REST or Data Loader attribute names, stored lookup codes, surrogate identifiers, resolver names, lookup types, or endpoints unless the requester explicitly asked for technical details |
| A technical field has a documented business-name resolver | Do not ask for the raw field or identifier first; ask for its business-facing name or meaning and resolve the technical value internally |
| TargetPlanName is supplied | Do not send the name as TargetPlanId, use a partial-name match, substitute absencePlansLOV, remove the Agreement plan type, active status, legislation, or date filter, or prepare a child until the GET absencePlans lookup resolves exactly once |
| A source absence type name is supplied | Do not send the name as SourceAbsenceTypeId, use a partial-name match, remove the maternity-pattern or legislation filter, or prepare the parent until the GET absenceTypes lookup resolves exactly once |
| SourcePlanName is supplied | Do not send the name as SourcePlanId, construct the child URL from numeric SourceAbsenceTypeId, use a partial-name match, or prepare the child until the returned plans child link resolves the plan exactly once |
| A newly supported LOV business value is supplied | Do not copy its name or meaning into a code or identifier field, use partial matching, select the first row, or bypass the documented read-only resolver |
| Legislation or the leave agreement Effective Start Date changes | Do not retain a prior Certification identifier without resolving it again in the new context; also re-resolve Legislative Grouping when Legislation changes |
| A Certification is outside the leave agreement start-date context | Do not prepare, preview, or submit the certification child, even when the Certification's status is Active |
| Eligibility Rule changes | Do not retain an incompatible Eligibility Formula or Eligibility Profile, and never populate both |
| Override Allowed is supplied without a payment formula | Do not resolve or default the value and do not populate absenceAgreementPlans.OverideFlag |
| A captured identifier or template name appears in source evidence | Do not persist or reuse it as project or runtime data |
| EffectiveEndDate is absent on create | Do not default 4712-12-31 solely from an observed response |
| effectiveOf is supplied directly by a caller | Do not pass it through. Derive Create from new Start Date, Edit from verified stored Start Date, and whole-object Delete from date-free ZAP |
| EffectiveStartDate appears only as a DAT METADATA attribute | Do not treat header presence alone as a populated value or require removal of the template column |
| Native Create physical EffectiveStartDate is populated | Do not preview or submit without explicit current create-section support; when dual populated, require equal normalized dates. A conflicting create date cannot be overridden |
| Edit/Delete date controls or stored-date changes are proposed | Do not derive a new range or require an operation date. Do not change physical stored dates without explicit current UI and adapter support |
| A retired dated operation is requested | Do not expose UPDATE, CORRECTION, END_DATE, DELETE_CHANGES or ZAP as separate business actions or silently replace the request with Edit/Delete; internal CORRECTION for current Edit is tied only to the stored Start Date and internal date-free ZAP maps current whole-object Delete |
| Current Data Loader metadata is missing | Do not substitute REST describe as authority for loader sections or fields |
| A prior mutation result is uncertain | Do not retry automatically or claim success |
| Exact Delete intent or applicable impact evidence is absent | Do not prepare an ambiguous or unverified deletion |
| Immutable Delete approval is absent | Do not submit; complete the concrete source, review and preview before core.data-loader requests final approval |
| Credentials, bearer tokens, cookies, ETags, or session identifiers appear in evidence | Do not persist or disclose them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LA.READINESS_GATE | decision | 160 | execution_gate | ready->LA.DONE_VALIDATED;blocked->LA.HANDLE_ISSUE | LA.ENFORCE_DESIGN | stop | Before handing a supported-operation, current-contract-valid source to core.data-loader; Create has new-date context, Edit uses internal CORRECTION with verified stored Start Date, whole-object Delete uses date-free ZAP, and applicable dependencies/impact are met |
| LA.HANDLE_ISSUE | step | 170 | error_handler | handled->LA.RETURN_ISSUES | none | stop | Classify an applicable input, lookup, dependency, metadata, approval, transport, Fusion, process or persistence failure, or disclose a retired intent as unsupported with available choices |
| LA.RETURN_ISSUES | terminal | 180 | terminal | none | LA.HANDLE_ISSUE | stop | The specific execution issue or unavailable intent was disclosed without marking unrelated supported operations blocked |
| LA.DONE_VALIDATED | terminal | 190 | terminal | none | LA.READINESS_GATE | stop | Leave Agreements source is validated for the separate core.data-loader workflow |
