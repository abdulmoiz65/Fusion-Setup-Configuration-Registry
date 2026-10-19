# Absence Certification Error Handling and Execution Gate

The task graph evaluates source readiness before core creates its preview.
`source_ready_for_preview` means applicable validation passed; it is not
approval, submission, or Fusion completion. Core Data Loader obtains approval
after presenting its immutable preview and checks it immediately before the
mutation. Missing approval does not prevent source validation or preview
construction; it prevents execution.

## Error Situations

| Situation | What Should Happen |
|---|---|
| An exact certificate search returns no effective record | State that no certificate matched the supplied Certificate Name, optional Legislation, and As-of Date; request corrected business-facing values without showing the identifier, stored codes, resolver name, or endpoint. |
| An exact certificate search returns multiple effective records | State that the Certificate Name is ambiguous and request Legislation or a more precise As-of Date; do not select the first row or expose technical identities. |
| A search result code cannot be mapped to a display meaning | Classify it as a lookup-contract failure and stop before presenting a partial result; do not expose the stored classification, status, or territory code as a fallback. |
| A non-create request has no exact resolved certificate identity | Stop before Data Loader preparation and request Certificate Name, Legislation when needed, and an As-of Date using business-facing labels. Keep the lookup date separate from the explicit mutation effective date. |
| Certification Type has no documented Trigger lookup mapping | Stop before querying or suggesting Trigger values and request a supported Certification Type; do not invent a lookup type. |
| Create needs Trigger and omitted business intent clearly identifies exactly one available option | Present that option by its business-facing meaning as a suggestion and request explicit confirmation. Do not populate the loader value yet. |
| Create needs Trigger and omitted business intent is unclear or ambiguous | Present every available business-facing option for the resolved Certification Type and ask the requester to select one; do not choose the first option. |
| View or unrelated maintenance uses a saved Trigger | Resolve its saved display meaning under the saved Classification; preserve before-state context without requesting a new selection or populating TriggerCode in Update. A missing display match is unavailable evidence, not a new Trigger choice. |
| A supplied Trigger has no exact match or multiple exact matches | State that the Trigger could not be resolved uniquely, present the available business-facing options, and ask the requester to select one. Keep lookup codes internal. |
| A suggested Trigger is not confirmed | Stop before preview and retain it only as an uncommitted suggestion. |
| A supplied coded value or conditional default candidate has no exact LOV match | Identify the business field and safe supplied business value; classify it as a catalog mismatch and stop before committing the value. Keep resolver and lookup type in technical diagnostics unless technical details were requested. |
| A lookup returns multiple exact matches or supplied code and meaning conflict | Identify the business field and conflicting business identity; classify it as input validation or lookup-contract failure and request one precise value. Keep technical resolver details in diagnostics and never select the first row. |
| An initial LOV page has no match while hasMore is true | Continue the same read-only GET with offset increased by the number of returned rows; classify no match only after all pages have been checked. |
| A lookup response omits LookupCode, Meaning, territory fields, DFF binding, or another documented field | Classify it as a Fusion API lookup-contract failure and stop; do not infer the missing mapping. |
| New or changed DFF values are omitted from a mutation | Do not resolve or default __FLEX_Context or include a DFF mutation section. Full View still reads requested existing children through its current metadata contract. |
| DFF values are supplied but current context metadata is unavailable or ambiguous | Classify it as a metadata-validation gap and stop; do not hard-code US or reuse a captured context. |
| EffectiveStartDate and RangeStartDate are both omitted for create | Default the normalized business effective start date to the current system date in YYYY-MM-DD format, derive effectiveOf, and disclose the applied default. |
| EffectiveStartDate and RangeStartDate differ | Classify as input validation and require one matching business date; do not choose one silently. |
| A maintenance date is unresolved | Classify as input validation. Request only an omitted Update operation date. For Correct, retrieve the selected stored row date without asking for a new date. For End Date, retain the supplied date or disclose the UI current-date candidate in core preview. Whole-object ZAP is date-free; Delete Record derives the selected stored row date and stops if selected configuration, complete History, protection or adapter evidence is missing. |
| Whole-object ZAP supplies a mutation range date | Stop as input validation; ZAP has no range date. Retain lookup as-of dates solely as target-selection context and require correction of the explicit mutation intent. |
| A create source supplies or synthesizes EffectiveEndDate | Reject the create end date because the Redwood Create form does not expose it. Retain an explicit End Date request for the separate supported action. |
| EffectiveStartDate exists only in DAT METADATA | Continue; header presence is not a populated physical date and requires no workbook-column removal. Validate the corresponding data-record value separately. |
| Physical EffectiveStartDate is populated and effectiveOf is absent | Classify it as a source-shape failure. Update always rejects the nonblank physical value. Correct the resolved intent, derive controls from the verified operation and applicable date, regenerate and revalidate; any prior approval becomes invalid. |
| Physical EffectiveStartDate and RangeStartDate inside effectiveOf are both populated with equal normalized dates | Update always rejects the nonblank physical value, including unchanged copied dates; no dual-population exception applies. For another applicable operation, block unless explicit current task-, operation-, and section-specific evidence proves support. Correct and regenerate the reviewed source where needed, revalidate, and invalidate any prior approval. |
| Physical EffectiveStartDate and RangeStartDate inside effectiveOf conflict | Classify it as input validation and source-shape failure and stop. Never choose one value, infer precedence, or permit an override; correct the business date, regenerate the artifact, and require new approval. |
| Fusion rejects effectiveOf or the selected RangeMode | Stop as a source-shape or metadata mismatch. Refresh the registered Data Loader template; do not retry using an inferred mapping. |
| Data Loader validation fails | Classify the validation issue, correct the reviewed source artifact, and create a new preview. |
| Fusion returns authentication or authorization failure | Report the redacted auth/authz failure. At a declared read-only GET, refresh a rejected cached token once where the authentication workflow permits it; otherwise stop and request access. Never expose tokens or automatically retry a mutation. |
| Fusion returns an uncertain create, update, or delete outcome | Stop and reconcile with a permitted read-only verification before any new mutation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Successful certificate search | Certificate Name, Certification Type, Legislation, Status, Effective Start Date, and Effective End Date using display values only. Do not show the certificate identifier, stored codes, resolver name, endpoint, or raw REST/Data Loader attribute names. |
| Certificate search failure | Supplied business-facing search values, zero or multiple match classification, and one corrective action. Keep technical lookup details internal. |
| Trigger choice required | Resolved Certification Type, available Trigger meanings, any single suggested meaning, and whether requester confirmation is pending. Do not show lookup types or stored codes unless technical details were explicitly requested. |
| Mutation preview | Target environment, operation, business object absenceCertifications, immutable reviewed artifact, and Data Loader REST mode. |
| Date-effective handoff | Applicable business date, whether supplied or create-defaulted, affected sections, and contract-validation result; ZAP has no mutation range date. Keep derived technical controls in the source artifact. |
| Non-search lookup failure | Business field, safe requested identity, zero/multiple/conflict/missing-field classification, and one corrective action. Resolver, lookup type and endpoint belong in technical diagnostics unless requested. |
| Applied default | Certification type, business field, matched business-facing candidate, and confirmation that an explicit value was preserved. Keep mapped codes and resolver details in technical artifacts. |
| Immediately before mutation | Current explicit approval bound to the exact preview and artifact. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A read-only certificate search is requested | Do not default omitted Legislation to US, use a fuzzy name match, stop before reading all pages, select the first row, or expose identifiers, stored codes, resolver names, endpoints, or raw attribute names. |
| A search as-of date is omitted | Do not reuse the current-date search default as the effective date for a mutation. |
| Any mutation | Do not invoke a direct REST client POST, PATCH, or DELETE call. |
| Missing approval, incomplete lookup, or changed artifact | Do not submit, retry, or infer an execution path. |
| Opaque parent or child key required | Do not construct or reverse-engineer the key. |
| A common-lookup-backed LOV is requested | Do not use an endpoint other than /fscmRestApi/resources/11.13.18.05/commonLookupsLOV. |
| Create needs a missing Trigger | Do not treat an inferred option as a default, silently select a value, or populate TriggerCode before the requester confirms or selects an available business-facing option. Saved Trigger context for View or unrelated maintenance does not require a new selection. |
| Trigger options are resolved | Do not query them before Certification Type resolves, use a lookup type belonging to another certification type, expose stored codes in ordinary interaction, or stop after only the first result page. |
| LegislationCode is resolved | Do not use an endpoint other than /fscmRestApi/resources/11.13.18.05/territoriesLOV. |
| New or changed DFF values are omitted from a mutation | Do not query or default a new flexfield context or infer a DFF mutation child from legislation US. This does not suppress requested existing-child reads in a full View. |
| DFF values are supplied | Do not hard-code a captured context or segment; use only the current absenceCertifications describe and its returned polymorphic or valid-values bindings. |
| effectiveOf is supplied directly by a caller | Do not pass it through; derive it from the validated operation and normalized business date. |
| EffectiveStartDate appears only as a DAT METADATA attribute | Do not treat header presence alone as a populated value or require removal of the template column. |
| Physical EffectiveStartDate is populated | Update always rejects the nonblank value. For other applicable operations, do not preview or submit unless derived effectiveOf is present, both normalized dates are equal, and explicit current task-, operation-, and section-specific evidence proves support. A conflicting date can never be overridden. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ANC_CERT.EXECUTION_GATE | step | 70 | execution_gate | source_ready_for_preview->ANC_CERT.DONE;not_ready->ANC_CERT.STOP_EXECUTION | ANC_CERT.ENFORCE_DESIGN | stop | Applicable source validation, operation capability, dependencies, defaults and source integrity passed; return readiness for core's immutable preview. Approval is checked by core after preview and immediately before mutation, not as a prerequisite to this validation pass |
| ANC_CERT.DONE | terminal | 80 | terminal | none | ANC_CERT.EXECUTION_GATE | continue | Return source_ready_for_preview and rule evidence to core.data-loader; nothing is approved or submitted by this terminal. Core owns preview, final approval, execution and reconciliation |
| ANC_CERT.STOP_EXECUTION | terminal | 99 | terminal | none | none | stop | An applicable input, operation/date contract, lookup, source integrity or Data Loader prerequisite is missing; preserve the draft and exact blocker. Missing mutation approval stops core execution after preview, not this source-validation phase |
