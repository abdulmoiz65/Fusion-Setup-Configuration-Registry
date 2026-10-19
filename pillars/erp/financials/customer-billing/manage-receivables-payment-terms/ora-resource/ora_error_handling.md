# Payment Terms Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required business value has no current match | State the supplied value, explain why it is required, show bounded current choices when available, ask one business-first question, and stop before package preparation. |
| Required business value has multiple current matches | Show the distinct display names and codes, ask the customer to choose, and never select the first, COMMON, ENTERPRISE, or a fuzzy match. |
| Create request exactly matches an existing term | Report the exact Name and SetCode match and ask whether the intended action is update; do not create a duplicate package. |
| Update or end-date request has zero or multiple exact matches | Report the exact match count and ask for the payment-term name and business set needed to identify one record. |
| Update requests a rename, reference-set move, or child deletion | Explain that this task CSV workflow treats Name+set as immutable and omission as preserve, not delete. Stop and offer a separately reviewed create/end-date or supported product workflow. |
| Current task template, metadata, or required baseline export is missing | Stop before archive preparation and request a current target export through the routed workflow. |
| Create request lacks one exact base language | Show current evidence-backed language choices, ask which business language to use, and create no ZIP. |
| Split term lacks Print Lead Days or the tax/freight installment option | Ask one consolidated business question for the missing values and stop before preview; never select values from a similar term. |
| Discount rows lack a discount basis | Ask which invoice amounts the discount should apply to, show the supported business choices, and stop before preview. |
| A candidate header lacks CalcDiscountOnLinesFlag | Block local validation. For a create without discounts apply and disclose Invoice Amount (`I`); with discounts require the customer-selected basis. Do not upload a blank value. |
| A candidate header lacks FirstInstallmentCode, CreditCheckFlag, InUse, PartialDiscountFlag, PrepaymentFlag, or DiscountBasisDateType | Block local validation. For a one-line create apply and disclose `INCLUDE` and the supported flag/date defaults; for a split term ask for the tax/freight choice. Do not upload a blank entity-required value. |
| Base Description is changed only in the header or conflicts with the base translation | Block before ZIP handoff. Resolve exactly one base row where Language equals SourceLang, put the same requested Description in both locations, and preserve non-base translations. |
| Update child patch omits a stable identity or repeats it | Report the affected entity and require line SequenceNum, translation Language, or discount line-sequence plus DiscountPercent. Do not guess which current child to replace. |
| A text value exceeds current entity precision | Report entity, row, field, value length, and supported maximum; ask for a shorter business value and never truncate silently. |
| Discount SequenceNum differs from its line or DiscountPercent repeats on a line | Report the affected parent/line/percentage and block before ZIP handoff; align child SequenceNum with the parent line and keep each percentage unique on that line. |
| Final normalized design is not confirmed | Show action, name, set, dates, amount, installments, discounts, language, and conditional behavior; ask for the orchestration-owned design confirmation and create no ZIP. |
| Request, evidence, target, or normalized value changes after confirmation | Invalidate the design confirmation, generate a new preview/design SHA-256, and request confirmation again. |
| Mixed or batch request contains an invalid, unresolved, duplicate-ID, duplicate-targeted, unsupported, or 101st operation | Identify the operation number and business identity, block the whole package, and create no partial ZIP. Require a complete design with no more than 100 distinct operation IDs and Name/set targets. This local gate does not assert Fusion transaction atomicity. |
| A requested term count has no explicit list or deterministic business pattern | Ask for the names and business values or an attached approved list; never invent terms merely to satisfy the count. |
| An invalid value and a missing choice coexist | Report every already-known invalid field/range value before asking for business choices; do not ask a choice that cannot make the design valid. |
| Build input is a functional-area, offering, multi-task, failed, or error-status export | Classify the package scope and status, permit read-only reporting when safe, and refuse to generate or present it as a task-level Payment Terms import. |
| Offline evidence is missing or stale | Request the exact local artifact and state that no authentication or environment call was made. |
| CSV or ZIP validation fails | Preserve safe validation evidence and affected entity, row, and field; do not upload. |
| A candidate contains exported audit values | Classify `nonblank_service_owned_audit_field`, identify each affected entity, row, and field, clear those service-owned values in a newly generated candidate, and require new confirmation and approval. Never retry the rejected archive. |
| JBO-25009 or JBO-25027 reports a date conversion/load failure | Classify the affected metadata date field, check partial persistence with a fresh export, reject the candidate, canonicalize every emitted date/date-time to its ISO import-safe representation, add a regression, and rebuild from fresh current evidence plus a fresh template. |
| ZIP is structurally valid but differs from the normalized blueprint plus baseline | Classify `candidate_blueprint_mismatch`, report each affected entity, reject the handoff, and rebuild from current inputs. |
| Core Data Loader Task Hook envelope is missing, stale, reconstructed, or bound to different bytes | Stop before upload with approval_blocker; rebuild the immutable preview and obtain new standalone approval. |
| A task-local import route, direct REST write, UI automation, SQL, or RA_TERMS table update is proposed | Refuse before any mutation and restart through Core Data Loader. |
| Manual uploader is on an offering-level or functional-area-level import page | Stop before upload and direct them to the exact Manage Receivables Payment Terms task's Import from CSV File action; bind the handoff to filename and SHA-256. |
| Fusion accepts an import request | Report accepted initiation separately; do not claim process completion or persisted-state verification. |
| Status check times out | Preserve task code, request or process ID, last status, elapsed time, and one status-only next action; do not resubmit. |
| Import completes with errors or warnings | Retrieve available status, counts, errors, ProcessLog, and result reports through the owning workflow; do not retry automatically. |
| Persisted-state export disagrees with the approved preview | Classify verification failure, preserve the exact comparison, and stop without another import. |
| Current CodeSearch cannot be reached for a requested refresh | Use the registered FPHDEV ownership and exception baseline only as labeled fallback; do not claim current-series completeness. |

## CodeSearch-Verified Business Exceptions

These findings were refreshed on 2026-08-12 against
`FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64`. They came from PaymentTerm entity/view
implementations, the TransactionPaymentTermsService WSDL, and service
implementations. Refresh the accessible current series whenever the product
series or release changes. Treat this table as known-message coverage, not as a
promise that Fusion can never return another validation or framework error.

| Message or exception | Affected area | Required handling |
|---|---|---|
| FND:::FND_CMN_TO_ERLY_EQ_FRM_DATE | Effective dates | Show supplied start/end dates and block until their sequence is valid; do not invent a replacement date. |
| AR:::AR_SU_UNIQUE_PAY_TERMS | Header identity | Report the duplicate/conflicting term in the resolved set and require create/update clarification. |
| AR:::AR_SU_INVALID_PRINT_LEAD_DAYS | PrintingLeadDays | Before preview, require a positive whole-number value whenever the term has more than one payment line; report any rejected value without inventing one. |
| AR:::AR_CONS_BILL_CLEAR_INSTALL | Consolidated or balance-forward term | Report the incompatible installment state and require an evidence-backed cycle/installment correction. |
| AR:::AR_SU_TOT_RELAMOUNT_EQ_BASE_AM | Header and payment lines | Show BaseAmount, computed line total, and variance; block until reconciled. |
| AR:::AR_SU_TERM_ENTER_LINE | Payment schedule | Report that at least one valid schedule line is required for the selected design. |
| AR:::AR_SU_COMPLETE_DISCOUNT_INFO | Discount schedule | Identify the incomplete row and missing or conflicting discount fields. |
| AR:::AR_SU_BASE_AMT_POSITIVE | BaseAmount | Report the rejected amount and require a valid value under current product validation. |
| AR:::AR_API_INVALID_LOOKUP | Lookup-backed field | Report field, supplied value, resolver, and zero/multiple-match state; require exact resolution. |
| AR:::AR_SU_DISCOUNT_PERCENT_RANGE | DiscountPercent | Require the refreshed entity range of 0 through 100, report the rejected percentage, and block until corrected. |
| FND:::FND_CMN_REC_COMB_VALS_EXST | Discount business key | Report the duplicate discount combination and its parent/sequence identity. |
| AR:::AR_SU_TERM_FULLY_ALLOCATED | Schedule allocation | Show the current allocation total and stop adding lines until the schedule is corrected. |
| JBO-27014: Attribute CalcDiscountOnLinesFlag in PaymentTermEO is required | Required header discount basis | Require a supported nonblank value on every header. For create without discount rows use and disclose Invoice Amount (`I`); with discount rows require the customer-selected basis. |
| JBO-27014: Attribute FirstInstallmentCode in PaymentTermEO is required | Required header installment option | Require a supported value on every header. Use and disclose `INCLUDE` only for a one-line create; for split terms require the customer's tax/freight choice. |
| JBO-27014: Attribute InUse or PartialDiscountFlag in PaymentTermEO is required | Required header flags | Require a nonblank supported Y/N value and use only the documented create default; preserve export-backed values on update. |
| Any unlisted AR or FND message ID | Product validation | Preserve the exact safe message ID, entity, row, field, and supplied value when available; classify it as an unknown product validation, stop, and require current CodeSearch or Oracle documentation review before changing the package. |

## Executable Product-Constraint Coverage

Known-message coverage is complete only when the bundled validator has a
negative test for the condition. The 2026-08-12 audit maps the component's
current validators as follows:

| Product validation | Executable preflight |
|---|---|
| Effective-date compare | Require StartDateActive and EndDateActive strictly later when supplied. |
| Unique payment term | Exact Name + SetCode duplicate/create and single-match update/end-date checks. |
| Print lead days | Require positive whole-number PrintingLeadDays for more than one payment line. |
| Consolidated billing | Reject a billing cycle combined with more than one payment line. |
| Relative amount total | Require positive BaseAmount/RelativeAmount and exact child total equality. |
| Required term line and due-by method | Require at least one line, unique positive sequence, exactly one due method, and complete day-of-month/months-forward pairing. |
| Complete discount | Require percent, exactly one complete date method, valid parent line, child SequenceNum equal to the line sequence, unique DiscountPercent on that line, and supported basis/date basis. |
| Base amount positive | Reject missing, zero, or negative BaseAmount. |
| Lookup validity | Validate Y/N flags plus current seeded installment option, discount basis, and date-basis codes. |
| Discount percent range | Require 0 through 100. |
| Discount combination uniqueness | Reject a child SequenceNum that differs from its referenced line, duplicate line/DiscountPercent combinations, and more than three discounts per line. |
| Fully allocated schedule | Require final RelativeAmount total to equal BaseAmount. |
| Required discount-basis header | Require supported nonblank CalcDiscountOnLinesFlag on every header; apply Invoice Amount (`I`) only for create without discount rows and verify it with a negative regression test. |
| Required installment-option/flag header | Require supported nonblank FirstInstallmentCode, InUse, and PartialDiscountFlag; apply and disclose `INCLUDE` only for a one-line create and cover blank values with negative tests. |
| Full required header state | Require supported nonblank CreditCheckFlag, PrepaymentFlag, and DiscountBasisDateType in addition to the existing required header checks; preserve export-backed update values. |
| Base-description translation | When Description is requested, require exact header/base-row equality and one base row; preserve every non-base translation unless explicitly patched. |
| Baseline-backed update patch | Merge child patches by stable identity, preserve unspecified fields/rows, reject missing/duplicate keys, and forbid end-date child changes. |
| Semantic candidate intent | With baseline and blueprint, independently reconstruct and compare all four candidate entities; reject structurally valid omissions or unintended clears. |
| Persisted-state reconciliation | Compare every candidate parent with a fresh successful export by stable parent/child identity, ignoring audit fields and reporting only extra system translation languages as nonblocking. |
| Entity string precision | Enforce current source-backed limits for header/translation identity, descriptions, language codes, lookup/flag values, and DFF context/segments. |

Do not add an exception to this file without also adding its executable check
and negative test, unless the condition provably cannot be evaluated offline;
in that case label it explicitly as an environment-only residual risk.

## CodeSearch-Verified Framework Exceptions

| Exception or fault | Evidence boundary | Required handling |
|---|---|---|
| oracle.jbo.RowValException | Explicitly thrown by CreatePaymentTermLineUIVOImpl in the refreshed baseline | Extract a nested message ID when present and use the business table; otherwise report the object, field, and sanitized message. |
| oracle.jbo.service.errors.ServiceException | Declared as the fault for TransactionPaymentTermsService WSDL operations in the refreshed baseline | Classify the attempted operation, preserve the correlation/process identifier, and stop; never retry automatically. |
| Generic Exception | Caught by PaymentTermServiceAMImpl in the refreshed baseline | Keep sanitized restricted diagnostics and show only a stable summary/correlation; never expose stack traces or credentials. |
| Generic Throwable | Caught by TransactionPaymentTermsServiceImpl in the refreshed baseline | Treat as an unexpected service failure, stop, and require investigation before retry. |
| Unknown exception class or message | Not proven by the current known-message table | Preserve only safe class, message ID, entity/row/field, correlation, and stage; classify as unknown, make no retry, and require evidence refresh. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required business value, schedule, field, date, task identity, or ZIP shape is invalid | Correct the blueprint or artifact and restart validation. |
| ambiguity_blocker | A required identity or business decision has zero or multiple exact matches, or request and evidence conflict | Ask one consolidated business-first clarification and rerun affected rules after the answer. |
| catalog_or_metadata_mismatch | Catalog flag, task identity, release, template contract, set, or resolver evidence conflicts | Refresh authoritative evidence and reconcile before preview. |
| auth_expired_or_invalid | Cached authentication is rejected | Refresh once only through the owning authentication workflow. |
| authorization_or_privilege | Required setup, export/import, or reference-set access remains denied | Restore exact access; do not retry a side effect. |
| transport_or_environment | Environment, VPN, DNS, or connection fails | Retry only a bounded read; never repeat a mutation automatically. |
| fusion_api_error | Fusion rejects the one approved request | Report safe status, message, and ECID when available, then stop. |
| process_timeout | Status does not reach terminal state in the allowed wait | Preserve identifiers and resume only with a status check. |
| process_failed | Import completes with errors | Preserve counts, logs, partial results, and corrected-package next action. |
| artifact_persistence | Required archive, hash, preview, log, or comparison cannot be saved | Stop before approval or completion and report the intended path. |
| approval_blocker | Preview, exact SHA-256 binding, Task Hook envelope, or standalone approval is missing, changed, stale, or declined | Rebuild the immutable preview; do not upload or reconstruct the envelope. |
| unverified_success | Fusion may have accepted or completed work but persisted-state comparison is absent or failed | Perform read-only reconciliation; never repeat the import blindly. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation result | Exact task name/code, target, validated facts, blocked facts, current rule node, and one next action. |
| Clarification | Known business facts, the one unresolved decision, bounded current choices with display names and codes, why the choice matters, and one direct question. |
| Offline package result | Exact task name/code, package scope, metadata/process status, archive members, Payment Terms row counts, rule results, SHA-256, no-external-call statement, and one next action; omit approval language. |
| Immutable preview | Environment, business effect, affected entities/rows, archive SHA-256, validation result, no-mutation statement, and exact approval instruction. |
| Accepted initiation | Data Set Name, Content ID, Request ID, and accepted status in the Core Data Loader response shape; do not claim completion. |
| Status | Exact returned data-set status plus total, loaded, and failed counts, then every user-friendly diagnostic supplied by Core Data Loader. |
| Failure or timeout | Failure class, safe message, task code, request/process ID, last status, elapsed time, verified side effects, artifact links when produced, and one safe next action. |
| Persisted-state verification | Approved versus exported header, lines, translations, and discounts, including every mismatch and whether the setup is verified. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing current template evidence | Do not invent columns, codes, keys, hierarchy, or ZIP order. |
| Missing or ambiguous reference data set | Do not default to COMMON, ENTERPRISE, the first exported value, a fuzzy match, or a set from another environment. |
| Functional-area or offering package supplied to the task skill | Do not strip members, rewrite metadata, or call the result a task-level Payment Terms package. |
| Update omits current children or fields | Do not interpret omission as deletion or blanking; preserve current state. |
| Rename, reference-set move, or child deletion is requested | Do not emulate the mutation through a partial CSV package. |
| Offline prepare or review | Do not authenticate, call Fusion, export, upload, import, initiate, poll, or request approval. |
| Missing or stale Core Data Loader validation envelope | Do not upload, initiate, choose an adapter, or reconstruct an envelope. |
| Approval appears in the original request or a longer message | Do not treat it as the required standalone approve response. |
| Failed, timed-out, or uncertain prior import | Do not retry or submit a replacement until status is reconciled. |
| Process status is successful but persisted comparison is missing | Do not mark the setup task complete. |
| Raw diagnostic contains a stack trace, credential, token, signed URL, or sensitive payload | Do not expose or persist the unsafe value. |

## Completion Decision

An import is verified only when the approved archive hash matches the submitted
bytes, terminal process status is successful, failed rows are zero, warnings
are accepted, required evidence is retained, and bundled `reconcile` reports
that a fresh read-only export matches the approved header, lines, translations,
and discounts. Otherwise
return the last confirmed state as blocked or unverified and do not resubmit.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.EXECUTION_GATE | decision | 60 | execution_gate | ready->PT.READY;blocked->PT.BLOCKED | PT.ENFORCE | stop | Confirm supported scope, semantic candidate match, complete task-rule evidence, standalone local-design confirmation when generating a ZIP, Core Data Loader ownership, reconciliation, and stop-before-retry boundaries before handoff |
| PT.READY | terminal | 70 | terminal | none | PT.EXECUTION_GATE | continue | Request is validated and ready for its owning read-only workflow or Core Data Loader preview; this terminal does not authorize a write or claim setup completion |
| PT.BLOCKED | terminal | 999 | terminal | none | none | continue | Validation, dependency, lookup, design, routing, approval, process, or persisted-state evidence is blocked |
