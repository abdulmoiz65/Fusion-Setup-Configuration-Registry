# Financial Orchestration Flows design enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Evaluate supported operation and flexfield restrictions |
| 2 | Identity and design | Evaluate applicable dated target, route topology and child impact rules; Fusion validates Agreement name and priority conflicts during create/correction |
| 3 | Artifact boundary | Require validated fields and Data Loader handoff |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error |  | A status change is requested outside the current-version Agreement correction path; standalone end-date changes, rename, bulk, Agreement-header deletion, standalone FTR deletion or an Insert outside parent-only DRAFT description change is requested | Route an explicitly requested status change through current-version Agreement correction and resolve it from FOS_AGREEMENT_STATUS; report other unsupported operations without silently dropping them | No |
| Explicit flexfield request | Error |  | PTR/FTR context/global/segment value requested; no supported context/value-set and loader mapping | Block the request. PrimaryTradeRelationToPrimaryTradeRelationDFFVA and FinancialTradeRelationToFinancialTradeRelationDFFVA are separate resources; never infer context codes or omit requested values | No |
| Agreement correction | Error | resolve_flow_agreement | No uniquely selected current version or unsupported dated transport | Resolve current target and preserve unrelated values | No |
| Agreement Status correction | Error | resolve_flow_status | Requested Status is not an exact, unique FOS_AGREEMENT_STATUS Meaning or LookupCode, or Status is not exposed by the current correction template | Use the current-version Agreement Correction path and resolved LookupCode. Let Fusion validate whether the requested transition is allowed; do not substitute another status after rejection | No |
| Agreement Insert | Error | resolve_flow_agreement_version | Target not DRAFT or not parent-only; new start <= existing start, earlier than today, after existing end or at an existing version boundary; Description unchanged; other changed fields requested | Require an explicit new date and changed Description; preserve Priority/status/end and identity | No |
| PTR/FTR topology | Error | resolve_flow_child_target | New PTR has no FTR; first FTR FromBUId differs from PTR FromBUId; next FromBUId differs from previous ToBUId; last ToBUId differs from PTR ToBUId | Require complete ordered chain and PTR-date inheritance for initial FTRs; a different date split requires supported transport | No |
| FTR trade organization chain | Error | resolve_flow_trade_org | Nonshippable Sales FTR contains a trade organization; the first Internal Transfer FTR has a selling organization, a later Internal Transfer FTR lacks its selling organization, an Internal Transfer FTR before the last lacks its buying organization, or its last FTR has a buying organization; any PROCUREMENT FTR lacks an eligible selling-BU organization, or the last PROCUREMENT FTR has a buying organization; another applicable omitted buying organization has no valid buying BU default; or a later omitted selling organization outside Internal Transfer and Procurement cannot inherit the preceding buying organization in its selling BU | Leave both FTR trade organizations blank for Nonshippable Sales. For Internal Transfer leave first selling and last buying organizations blank; populate selling on every later FTR and buying on every FTR before the last. For Procurement populate every FTR selling side from its own selling BU, and populate a buying side on every FTR except the last. Apply Shipment and other chain defaults only in their contexts | No |
| FTR charge account | Error | resolve_flow_charge_account | A supplied ChargeAccount has not resolved to exactly one eligible buying-ledger ChargeAccountCodeCombinationId, or the DAT sends the display value in ChargeAccount | Resolve the account in the buying ledger and send only ChargeAccountCodeCombinationId | No |
| Shipment PTR trade organization | Error |  | A SHIPMENT PrimaryTradeRelation contains Selling Trade Organization, FromTradeOrganizationId or ToTradeOrganizationId, or invokes trade-organization resolution | Rebuild the source without PTR trade-organization attributes; resolve and default applicable trade organizations only on FTR rows | No |
| Child linkage | Error | resolve_flow_child_registration | Keys mismatch, derivation unscoped, generated identity invented, or independently dated URL substitutions unverified | Use deployed parent-child linkage and exact resolved identity. File order or a root PATCH cannot substitute for nesting | No |
| FTR correction parent-date helpers | Error | resolve_flow_child_registration | An existing FTR correction populates ParentEffectiveStartDate or ParentEffectiveEndDate, adds a helper column absent from the fresh template, uses FTR dates as parent URL dates, or lacks a verified AgreementId foreign-key derivation for a required parent-date URL placeholder | When a helper column is present in the fresh FTR template, leave its DAT value blank. When absent, do not add it. In both cases require both deployed foreign-key derivations and nested URL mapping; otherwise stop before archive creation | No |
| Standalone FTR correction artifact | Error | resolve_flow_child_registration | A standalone FTR correction DAT contains a PrimaryTradeRelation or financialOrchestrationTradeAgreements section, more than one business-object section, or no FinancialTradeRelation section | Rebuild from the fresh FTR template with exactly one FinancialTradeRelation METADATA section and one selected FTR row. Use Agreement/PTR data only as resolved identity and URL-routing context | No |
| PTR deletion impact | Error | resolve_flow_ftr_target | Target/descendant inventory missing or scope includes header/sibling/child-first deletion | Preview exact PTR and descendants. Verified cascade may remove listed descendants; unknown behavior must be disclosed and approval cover that impact. Never add FTR deletes to bypass rejection | No |
| Document-price rule | Error | resolve_flow_document_price_profile | INTERNAL_TRANSFER DocumentPriceBasis=Y without verified eligible profile/feature result | Reject disabled or unresolved conditional candidate; transaction-cost rules do not require this feature | No |
| Artifact scope | Error |  | Values differ from resolved/requested fields, audit/custom fields are populated, or loader-only surrogate values would become business attributes | Require operation-specific fields from live template and verified surrogate handling; no guessed IDs or unexpected rows | No |
| Environment configuration | Error |  | Operation would republish registration, change keys or refresh attributes without a separate request | Report deployment mismatch; setup mutation does not authorize configuration changes | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_flow_agreement | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_status | When an Agreement Status correction is requested | Exactly one matching status Meaning/LookupCode and the returned LookupCode for the correction payload | ora_reference_lookups.md |
| resolve_flow_agreement_version | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_child_registration | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_child_target | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_document_price_profile | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_ftr_target | When referenced by applicable Design Rules | Resolved result from the named lookup | ora_reference_lookups.md |
| resolve_flow_trade_org | When referenced by applicable Design Rules | Resolved FTR trade organization for each applicable side BU | ora_reference_lookups.md |
| resolve_flow_charge_account | When an FTR ChargeAccount is supplied | One eligible buying-ledger code-combination ID | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOF.CHECK_SCOPE | step | 5 | design_enforcement | success->FOF.CHECK_INPUT;failure->FOF.RETURN_ISSUES | none | stop | Evaluate only Every request and Explicit flexfield request scope rules before lookups; other design rules run at FOF.CHECK_DESIGN |
| FOF.CHECK_DESIGN | step | 380 | design_enforcement | success->FOF.CHECK_HANDOFF;failure->FOF.RETURN_ISSUES | FOF.CHECK_RESOLVED_INPUT | stop | Apply scope, effective-version, route topology, deletion-impact and artifact design gates |
