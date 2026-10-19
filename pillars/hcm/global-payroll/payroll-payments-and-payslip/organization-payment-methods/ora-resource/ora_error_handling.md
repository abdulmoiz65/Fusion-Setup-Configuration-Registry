# Error Handling and Execution Gate

## Error Situations

| Situation | What Should Happen |
|---|---|
| Source validation, reference lookup, or task validation fails | Stop before upload and show the affected source and next action |
| OAuth authentication or authorization fails | Stop and report the auth or privilege issue; do not retry an upload or load automatically |
| Upload or load response is uncertain or fails | Preserve the sanitized result and stop; do not retry the POST without explicit approval and reconciliation |
| OPM.VALIDATE_RULE_CONDITIONS fails or lacks condition-level evidence | Stop before populated DAT or upload ZIP generation; classify as input validation and identify the missing or conflicting selections using ora_input_validation.md; invalidate any earlier successful preview and require corrected inputs before regeneration |
| OPM.ENFORCE_HDL_DESIGN rejects an immutable-field change, inherited-field conflict, or override request | Stop before preview, upload, or load; classify as input validation and identify each affected field, parent OPM, and prohibited change; do not silently replace conflicting source values or offer an approval bypass |
| OPM.ENFORCE_HDL_DESIGN lacks authoritative parent values for the immutable-field or inheritance comparison | Stop before preview; classify unresolved or ambiguous parent identity as catalog mismatch, and missing comparison values as input validation; preserve an auth/authz, transport/environment, or Fusion API failure classification when the declared lookup failed; report the missing evidence and the declared resolver as the next action |
| Prenotification processing is requested for AE, BH, CA, GB, KW, OM, QA, or SA | Stop before defaults, populated HDL artifact generation, and preview; return exactly Prenotification processing is not supported for legislation {legislation}.; use the resolved legislation; report this before a Category selection error when both conditions apply |
| Prenotification Required is requested selected when Category is not MT for a legislation outside the explicitly unsupported list | Stop before defaults, populated HDL artifact generation, and preview; return exactly Prenotification Required can be selected only when Category is MT. |
| Category or LDG-derived legislation cannot be established | Stop affected prenotification validation before defaults; classify unresolved or ambiguous Category or legislation as catalog mismatch; identify the missing evidence; use the existing declared resolvers and do not invent a read or execution route |
| A request asks to waive a prenotification enablement, selection, or supplied-value validation failure | Preserve removal intent and the original failed condition; do not build an exception preview or offer approval as a validation bypass; invalidate earlier previews that retain this invalid state and require corrected final inputs |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Approval preview | Target environment, create operation, source file, organization payment method name, LDG, effective start date, currency, payment type, and archive SHA-256 |
| Live result | Accepted data set name and server request identifiers when Fusion returns them |
| Failure | Failure class, stage, affected source, and recommended action without credentials or tokens |
| Prenotification preview | Resolved legislation and Category; flag enablement and selected value separately; each detail field's enablement, original input intent, final value, and value origin; no unsupported selection or invalid supplied value |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No explicit approval bound to the unchanged archive | Do not upload or initiate the Data Loader request |
| Archive SHA-256 differs from the approved preview | Do not upload; rebuild validation and approval preview |
| Duplicate organization payment method is found | Do not create a second record |
| A mutation is proposed through REST, UI automation, or another non-Data-Loader route | Do not execute it; prepare and validate the HDL DAT archive for HCM Data Loader |
| Prenotification enablement, selection, or supplied-value validation fails | Do not generate a populated HDL artifact, request approval, upload, or initiate; an instruction to proceed, generic readiness override, or prior prenotification waiver cannot bypass these mandatory checks |

## HCM Data Loader Failure Handling

| Situation | What Should Happen |
|---|---|
| DAT hierarchy or parent source key fails validation | Stop before upload and show the component, parent reference, and affected source-system key |
| HCM Data Loader import or load process fails | Retrieve the process status and available process log, preserve sanitized diagnostics, and don't resubmit automatically |
| HCM Data Loader status remains incomplete at the polling timeout | Report the environment, process identifier, last status, and elapsed wait; provide the safe status-check path |
| REST LOV lookup fails | Stop reference validation; don't substitute a REST write or bypass the lookup |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.APPROVAL_GATE | decision | 10 | execution_gate | approved->OPM.DONE;missing_approval->OPM.FAILED;changed_archive->OPM.FAILED | OPM.ENFORCE_HDL_DESIGN | stop | Before UCM upload and HCM Data Loader initiation; reject a preview with a prenotification validation waiver or invalid final prenotification state | |
| OPM.DONE | terminal | 11 | terminal | none | OPM.APPROVAL_GATE | stop | Approved archive is submitted through HCM Data Loader and Fusion accepts initiation | |
| OPM.FAILED | terminal | 12 | terminal | none | none | stop | Any stop condition | |

## Reference Resolution Errors

| Situation | What Should Happen |
|---|---|
| A reference or LOV display value returns no match | Stop before DAT generation or archive approval and identify the business field plus invalid supplied value |
| A reference or LOV display value returns multiple matches | Return an ambiguity error with the business field and supplied value; don't select a value automatically |
| A supplied display value conflicts with a supplied validated code or ID | Stop and report both conflicting inputs; don't overwrite either value silently |
| A dependent lookup input is missing | Stop at the missing dependency; for example, don't query legislation-scoped payment types without LegislationCode or bank accounts without the LDG-derived legal-employer names |
| A reference session has expired or isn't active | Obtain a fresh authorized Fusion session before retrying the read-only lookup; don't disable certificate validation or expose credentials or tokens |
| A live resolver fails after some values were cached | Discard unresolved results, retain only sanitized diagnostic context, and don't prepare or submit a partial archive |
| A successful bank-account lookup returns identity without activity evidence | Complete the metadata and exact-account detail reads declared by resolve_bank_account_by_legal_employer before reporting a verification gap; do not infer activity from account existence alone |
| The bank account is not active on the requested effective date or Payroll use is not enabled | Classify as input validation, identify the affected account and eligibility condition, and stop before preview; request an eligible account or prerequisite correction |
| Declared bank-account status reads still lack a required field or return an incompatible date contract | Classify as catalog mismatch and report the missing evidence; preserve auth/authz, transport/environment or Fusion API classification when the read itself failed; do not weaken the active-account prerequisite |

## Supplemental Scoped-Authentication Errors

| Situation | What Should Happen |
|---|---|
| A request for `/api/boss/data/objects/ora/erpCore/bankingSetup/v1/bankAccounts` has only a Fusion-scoped token available | Stop before the BOSS call; obtain a BOSS-scoped token through the BOSS client. Do not invoke the endpoint with the Fusion token. |
| A BOSS-scoped token cannot be obtained or is rejected | Classify the failure as auth/authz, retain only sanitized diagnostics, and stop the dependent bank-account resolution. |
| A Fusion-scoped token cannot be obtained or is rejected | Classify the failure as auth/authz, retain only sanitized diagnostics, and stop the dependent Fusion request. |
| Any scoped access token is refreshed or acquired | Keep it in transient authentication handling only; do not include its value in a resource, DAT, preview, diagnostic, or result. |

## REST Hierarchy Discovery Errors

| Situation | What Should Happen |
|---|---|
| A mandatory finder ID or SysEffectiveDate is missing or invalid | Classify as input validation, don't issue the request, and report the exact parameter plus expected format |
| A hierarchy finder is rejected by Fusion | Classify as auth/authz, transport/environment, or Fusion API as applicable; retain the endpoint class, finder name, and sanitized status without tokens |
| A paged response can't be completed | Retain the pages already read as partial data, mark the collection incomplete, and don't claim complete metadata or hierarchy coverage |
| `additionalDetails` doesn't return documented logical dates | Retain the parent record, mark the logical date metadata as undocumented, and report the missing expanded data without copying ordinary effective dates into logical-date fields |
| An OPM name is absent and fallback detail lookup returns zero or multiple identities | Retain the OPM ID, mark the name unresolved, and return a mapping error |
| A Payment Source name is absent and fallback source lookup returns zero or multiple matching identifiers | Retain the Payment Source ID and rule, mark the name unresolved, and return a mapping error |
| A Payment Source parent ID doesn't resolve to the current OPM | Retain the source and original ParentOrgPayMethodId outside the resolved child group and return a parent-mapping error |
| A Payment Method Rule source identifier doesn't resolve uniquely | Retain the rule and original identifier outside the resolved source groups and return a source-mapping error; don't attach it to a guessed source |
| Returned ID and denormalized name conflict | Retain both returned values in sanitized evidence, mark the relationship unresolved, and don't overwrite either value silently |

## Physical Payment Method Rule Deletion Handling

| Situation | What Should Happen |
|---|---|
| The OPM target isn't uniquely resolved | Stop before DAT generation; report the supplied OPM name and LDG without selecting a similarly named record |
| No active Payment Method Rule is returned | Stop; report that no physical delete target exists as of the selected system-effective date |
| Multiple active Payment Method Rules are returned | Stop; require the user to identify the specific rule before building a DELETE record |
| The resolved rule is the default rule | Show that deleting it removes default routing; don't add, change, or infer a replacement rule |
| Live Data Loader validation rejects the DELETE record or archive | Preserve the validation result and stop; don't substitute a REST delete or retry with changed identifiers |
| The archive changes after the approval preview | Reject the approval and repeat validation plus preview for the changed archive |
| Approval is missing or not bound to the immutable delete archive | Stop before UCM upload and HCM Data Loader initiation |
| Upload or load initiation is uncertain or fails | Preserve sanitized diagnostics and don't resubmit the DELETE archive automatically |

## Physical Payment Method Rule Deletion Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.PHYSICAL_DELETE_APPROVAL_GATE | decision | 124 | execution_gate | approved->OPM.PHYSICAL_DELETE_DONE;missing_approval->OPM.DELETE_FAILED;changed_archive->OPM.DELETE_FAILED | OPM.ENFORCE_PHYSICAL_DELETE | stop | Before UCM upload and HCM Data Loader initiation of a permanent PaymentMethodRule deletion | |
| OPM.PHYSICAL_DELETE_DONE | terminal | 125 | terminal | none | OPM.PHYSICAL_DELETE_APPROVAL_GATE | stop | The approved immutable DELETE archive is accepted for HCM Data Loader initiation | |
| OPM.DELETE_FAILED | terminal | 126 | terminal | none | none | stop | Any permanent PaymentMethodRule deletion stop condition | |

## REST Hierarchy Terminal Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.READ_HIERARCHY_EMPTY | terminal | 105 | terminal | none | OPM.READ_LIST | stop | Read-only hierarchy discovery completed with a valid empty LDG result | |
| OPM.READ_HIERARCHY_DONE | terminal | 106 | terminal | none | OPM.READ_RULES | stop | Read-only hierarchy discovery completed with one or more reconstructed OPM hierarchies | |
| OPM.READ_HIERARCHY_FAILED | terminal | 107 | terminal | none | none | stop | A read-only hierarchy discovery stop condition occurs | |

## Observed Fusion OPM Warnings and Rule Errors

Preserve the following developer-supplied Fusion messages when the corresponding condition is encountered. Warnings permit the user to choose whether to continue; errors block the conflicting rule design.

| Situation | What Should Happen |
|---|---|
| OPM has no default payment source | Show: No default payment source is defined for this organization payment method. (PAY-1636073) If you submit this organization payment method without selecting a default payment source, the prepayment may not be processed for some payees. Continue anyway? Continue only after the user explicitly acknowledges the warning. |
| OPM has no Payment Source | Show: You didn't define a payment source. (PAY-1636071) If you save this organization payment method without a payment source, the method can't be used to create payments in Oracle Fusion Global Payroll. Continue anyway? Continue only after the user explicitly acknowledges the warning. |
| More than one default rule exists for employee payments or more than one default rule exists for third-party payments | Stop and show: You can't set more than one payment rule as the default payment rule. (PAY-1636085) An organization payment method can only have one default payment rule for employee payments and one default payment rule for third-party payments. |
| A third-party payment rule has neither Tax Reporting Unit nor Third-Party Name | Stop and show: You must specify a tax reporting unit or a third-party name for any payment rules used for third-party payments. |
| A nondefault, non-third-party payment rule has no Tax Reporting Unit | Stop and show: You must specify a tax reporting unit for all payment rules that aren't defined for third parties or as the default payment source. |
| The effective-date source-reuse check owned by OPM.ENFORCE_HDL_DESIGN finds another rule overlapping a default rule for the same Payment Source | Stop and show: You can't use a payment source in another payment method rule if it's already used as the default source for the payment method. (PAY-1636090) Identify the conflicting rules and overlap dates. Do not raise this diagnostic solely because the source was default in a disjoint past or future period. |
| The effective-date source-reuse check lacks complete rule identity or date-range evidence | Stop before preview, classify unresolved identity or incomplete existing-rule evidence as catalog mismatch and missing or invalid supplied dates as input validation, and report the missing evidence required by find_payment_source_rule_date_overlap. Do not treat an unresolved overlap check as passed. |
| A default rule supplies Tax Reporting Unit, Third-Party Name, or Payment Criteria | Stop before DAT approval and explain that a default rule permits only the Payment Source selection; don't silently discard the conflicting values. |
