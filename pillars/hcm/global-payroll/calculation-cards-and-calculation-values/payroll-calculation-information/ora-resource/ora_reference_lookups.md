# Wage Basis Rules Reference Lookups

## Authority and Transport

These are the task-owned read contracts for Payroll Calculation Information
(PAY_MANAGE_PAYROLL_DEDUCTIONS). Wage Basis Rules stays in this skill; it is
not a new sibling skill. Use the existing core REST client and authenticated
environment context. No endpoint in this file authorizes a product REST write.
Honor an existing-session-only instruction; stop on authentication failure and
ask the owner to refresh rather than initiating OAuth.

All paths are relative to the verified target. Use Accept application/json and
REST-Framework-Version 9. URL-encode finder values, escape quotes in ADF q
expressions, and never accept a host or arbitrary URL from business input.
Complete pagination before declaring absence or a complete history. Normalize
every ResultKeyN/ResultValueN pair into named fields, including indices above
15. Conflicting keys, missing fields, inconsistent counts, truncated pages,
or a non-JSON response are errors, not an empty result.

For primary and secondary classification selection, pass effectiveDate as the
explicit operation business date alongside finder, onlyData and pagination.
Use the applicable date established by ora_dependency_readiness.md. If absent
or ambiguous, return NEEDS_INPUT before either classification call. Validate
each distinct applicable date when the request supplies different row dates;
eligibility at one date does not prove eligibility at another.
Do not resolve a January rule against an implicit current-date classification
set. The source chooses DeductionGroupIdFk for the group, ClassificationIdForFk
for primary/secondary, and DeductionTypeIdFk for components. These selected
foreign keys feed dependent binds and persisted identities; the plain view-row
IDs are not interchangeable. Require those aliases rather than guessing a
fallback if they are missing.

The Components finder is scoped by reference definitions (ContextUsageId1..6),
not by jurisdiction values. Preserve that distinction: jurisdiction values
belong in the context LOV cascade and exact rule identity, not pContextId binds.

## Lookup Execution Rules

These presentation rules apply to the selection LOVs below, not to completeness
checks for history or reconciliation. A missing selection does not prevent
retrieving its choices when the resolver's parent binds and core preflight are
ready. Discovery remains inside WBR.RESOLVE_REFERENCES; no input or dependency
node performs a Fusion call.

| Situation | What Happens |
|---|---|
| A selection is missing but its resolver prerequisites are ready | Retrieve the current eligible collection using its declared finder without inventing a selected name, ID or additional bind. Present choices under these rules, then return needs_input if a decision remains. |
| The user explicitly supplied a business name or supported business code | Apply that resolver's exact match rule within the full current scope. A unique eligible exact match validates the supplied selection without a repeat question. A substring search hit is not an exact selection. |
| The complete eligible set contains 1 through 20 choices | Show the eligible business labels, sorted case-insensitively, with business codes or parent labels where needed to distinguish them. Require a selection when none was supplied; a single option is not an automatic default. |
| The complete eligible set contains more than 20 choices | Ask for a business-name or supported business-code search term. Filter case-insensitive contains matches and show at most 20 per conversational page; offer next page or a narrower term when more remain. A supplied exact selection does not need a search question. |
| A search is needed | Use returned business labels and documented business-code fields only, never internal IDs. These resolver contracts declare no server-side text-search parameter: fully paginate the scoped collection, then filter and sort locally. Do not invent a q, finder word or search bind. API page size and the 20-choice display limit are separate. |
| Search returns one match, no matches, or several pages | One match still needs selection unless it validates an explicitly supplied exact choice. No matches means no match for that term within this scope, not no records in Fusion. Offer a revised term or scope choice without broadening scope automatically; complete retrieval is required before any absence claim. |
| Equal labels belong to distinct eligible records | Preserve distinct identities internally and show available business codes, parent hierarchy or other returned business-label distinctions. Do not merge by label, choose the first or expose surrogate IDs. If business distinctions cannot resolve the ambiguity, return AMBIGUOUS. |
| A business code resolves a component whose displayed name is not unique | Retain the selected record and code, but do not assume the code is a supported PayrollComponent native user key. Establish the native value from the current BO contract/mapping evidence; a REST discriminator alone does not prove HDL disambiguation. If no unambiguous native key is established, return CATALOG_MISMATCH for preparation, preserving the completed business selection rather than asking the user for an internal ID. |
| The unfiltered eligible set is empty | Explain which scoped choice has no eligible values. Do not invent a default or reinterpret the empty set as No References, no secondary or all secondary classifications. Apply the explicit secondary-state contract in ora_input_validation.md. |
| Explicit all secondary classifications is selected | Retrieve the complete eligible secondary set for the resolved primary, LDG and applicable date, ignoring conversational text filters and page position. Preserve the membership used for the expected rule count; zero results is not a successful all selection. |
| Explicit no secondary classification is selected | Validate the existing optional-secondary contract for the current scope; no-match or an empty list is not evidence of null-key eligibility. If eligibility is unresolved, report the contract gap rather than requesting an internal key or silently selecting a secondary. |
| No References is selected | Resolve the actual reference-level row and confirm its context definitions are inactive. Skip context-value calls and questions; keep slots empty as declared by metadata. Conflicting active definitions are CATALOG_MISMATCH, not permission to clear them. |
| Active reference contexts are being selected | Use their current business labels and resolve parent values before dependent LOVs, such as State before County before City. Validate a supplied complete hierarchy in order without re-asking resolved values. Do not send a county/city request using unresolved parent values. Preserve inactive gaps in the six slots. |
| A customer-defined value is returned in the eligible scope | Apply the same exact-selection rules as any other value. Do not use a packaged fixture allowlist; unresolved HDL mapping is CONTEXT_MAPPING_UNRESOLVED, not an invalid customer value. |
| Scope changes or a previously displayed page is stale | Apply the invalidation rules in ora_dependency_readiness.md before reusing any choices or selected keys. Page-number selections apply only to the current displayed page and scope; never apply an old ordinal to a refreshed list. |
| Maintenance starts from a selected existing rule | When current operation-local evidence supplies the history resolver's complete identity, read that rule's complete history and verify physical dates before asking for fresh choices. Reuse its resolved business labels and mappings; do not repeat Create LOV selection. A prior operation's keys are not current evidence: re-resolve its supplied business identity through the existing resolvers. |
| Maintenance target is only partly identified | Resolve supplied business values and retrieve choices only through the declared resolvers with their required binds. Ask for the missing discriminator needed for the next lookup, not the full Create questionnaire. These contracts do not declare a global free-text rule search or an ID-only mutation shortcut. |
| History is presented for maintenance | After complete retrieval and ISO date verification, present versions in start-date order with start, end or No end date, and Included/Excluded. Identify the logical rule once by LDG, component, classifications and ordered context business values. Multiple dated versions of that one identity are history, not multiple candidate rules; a stored null secondary is part of its existing identity, not missing Create input. |

## Live Lookups

The named finder contracts below are part of their owning resolver definitions.
In the finder specifications, a double pipe separates values; encode it as
%7C%7C in the query. Do not confuse display labels, view-row IDs, and foreign
key IDs. Preserve all returned aliases until the intended foreign key is proved.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_wbr_ldg | Every fresh operation, LDG change or unresolved LDG choice after core preflight | Verified environment; LDG business name or discovery search term when supplied | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV?onlyData=true&limit=500&offset={offset} | Name, LegislativeDataGroupId, LegislationCode | Fully paginate; present choices under Lookup Execution Rules when unselected; otherwise require exactly one trimmed case-insensitive Name match | Current choices or selected LDG name, internal LDG ID and legislation | NEEDS_INPUT, NOT_FOUND or AMBIGUOUS; never borrow a prior pod ID |
| find_wbr_group | LDG resolves | LDG ID and legislation; group label or discovery search term when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using Group finder below | DeductionGroupId, Name, LegislationCode, LegislativeDataGroupId, DeductionGroupIdFk | Present current choices when unselected; otherwise exact name in current scoped response; preserve distinct group aliases | Current choices or selected group and its reference-level lookup ID | NEEDS_INPUT, NOT_FOUND or AMBIGUOUS |
| find_wbr_reference_level | Group resolves | LDG, legislation and selected group; reference-level label when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using Reference level finder below | SContext, SContextVb, Objecttype, ContextUsageId1..6, Taxabilitycontextname1..6, Taxabilitycontextid1..6, Taxabilitycontext1lookuptype..6lookuptype, Taxabilitycontext1valueset..6valueset, group and legislative scope | Present current choices when unselected; otherwise exact SContextVb selection; star means No References; preserve six ordered context slots rather than compacting gaps | Current choices or selected reference level, ordered context definitions, current lookup/value-set names | NEEDS_INPUT, NOT_FOUND or AMBIGUOUS; missing context definition is CATALOG_MISMATCH |
| find_wbr_context_values | A selected context level is active and its parent values resolve | Current reference definitions and resolved parent context selections; target business value or discovery term when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using Context finders below | Code and Meaning, or LookupCode and Meaning, plus returned context-specific key fields | Present scoped choices when unselected; otherwise resolve each business selection exactly within its parent hierarchy. Keep REST stored value and HDL helper key separately. Do not assume Code, Meaning or a numeric REST value is automatically the HDL key | Current choices or six stored context values, six HDL context keys, labels and mapping evidence | Missing selection is NEEDS_INPUT; ambiguity is AMBIGUOUS; an unestablished HDL key mapping is CONTEXT_MAPPING_UNRESOLVED |
| find_wbr_classifications | LDG and applicable date resolve; secondary lookup additionally requires resolved primary | LDG, legislation, explicit effectiveDate; primary and secondary selections or discovery terms and explicit secondary mode when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using Primary and Secondary finders below | ClassificationId, ClassificationName, BaseClassificationId, BaseClassificationName, ClassificationIdForFk; ParentClassificationId for secondaries | Present scoped choices when unselected; otherwise exact scoped primary and eligible secondary matches. Keep foreign-key identity distinct from view-row identity. Apply the input secondary-state contract and Lookup Execution Rules for all/none; never use a filtered page as all | Current choices or primary and secondary business names, internal foreign keys, explicit selected set with date scope | NEEDS_INPUT, NOT_FOUND or AMBIGUOUS; do not choose a fixture value; missing null-secondary eligibility evidence is CATALOG_MISMATCH |
| find_wbr_components | Classifications and reference level resolve | Group, LDG and ordered context usage IDs; component names/codes or discovery term when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using Components finder below | DeductionTypeId, BaseDeductionTypeId, DeductionTypeIdFk, DeductionCode, BaseName, Name, LegislativeDataGroupId, LegislationCode, DeductionGroupId, ContextMetadata, DisplaySequence | Present scoped choices when unselected; otherwise exact eligible component selection. Resolve the persisted foreign key from returned aliases and current rule identity; never silently choose the first alias or row | Current choices or selected component labels and internal deduction type keys | NEEDS_INPUT, NOT_FOUND or AMBIGUOUS; disagreement between aliases and persisted rule is CATALOG_MISMATCH |
| read_wbr_history | Duplicate check, existing target selection, or reconciliation | Exact classification, secondary selection, component and legislative scope, all six stored contexts | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV using History finder below | TaxabilityRulesId, EffectiveStartDate, EffectiveEndDate, ClassificationId, SecondaryClassificationId, DeductionTypeId, LegislationCode, LegislativeDataGroupId, UsageType, ContextValue1..6 | Read all contexts for the selected classification/component family and locally filter exact LDG, secondary and all six contexts. Include blank-context candidates in anomaly detection. One logical target may have several dated slices; do not call those ambiguous records | Complete logical-rule timeline, duplicate count, sibling baseline and operation-local identity | Empty is valid only for fully paginated Create preflight or whole-history-delete readback; otherwise NOT_FOUND. Multiple logical identities or uncertain completeness block |
| read_wbr_physical_rules | Current-state review, precise date validation, or reconciliation | Operation-local target IDs, complete business identity, and explicit ISO effective date | GET /hcmRestApi/resources/11.13.18.05/taxabilityRules?q={escaped_predicate}&effectiveDate={iso_date}&onlyData=true&limit=500&offset={offset} | TaxabilityRulesId, EffectiveStartDate, EffectiveEndDate, ClassificationId, SecondaryClassificationId, DeductionTypeId, LegislativeDataGroupId, LegislationCode, UsageType, ContextValue1..6 | Use the physical query contract below; compare full identity and date range, never just an ID or aggregate table count | ISO four-digit-year slices and stored context values | Missing required read is NOT_FOUND; transport or incomplete evidence is not zero rows |
| verify_wbr_hdl_contract | Core supplied the final normally validated immutable archive for Task Hook | Core validation evidence, current Taxability Rule template and metadata, selected operation and exact archive | GET /hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos&onlyData=true&limit=500&offset={offset}; follow exact matched item, attributes links and template UcmContentId through core/data-loader | BusinessObjectId, UIDescription, BusObjTopDiscriminator, UcmContentId, supported actions, date-effective behavior, attributes and key flags | Require Taxability Rule, TaxabilityRule.dat, root discriminator TaxabilityRule, no child rows and the selected field shape in ora_input_validation.md. Validate the same bytes; do not recursively invoke Task Hook | Schema fingerprint, exact-field validation and immutable-artifact check | Changed/missing contract or disagreement is CATALOG_MISMATCH; no approval handoff |

## Finder Specifications

All generic finders use `findByWord;PayRestName=...` and collection pagination.
The following argument order is source-backed; runtime identifiers come only
from this operation's preceding lookup, never from packaged test values.

| Finder | PayRestName | AdditionalViewCriteria | ParameterKeys | ParameterValues | DisplayAttributes |
|---|---|---|---|---|---|
| Group | DeductionGroupsWithDeductionTypeVO | findByLdgOrLegCode | pLegislationCode, pLegislativeDataGroupId | legislation, LDG ID | DeductionGroupId, Name, LegislationCode, LegislativeDataGroupId, DeductionGroupIdFk |
| Reference level | GroupTaxabilityRuleContextVO | findByLegCodeLdgIdDedGrpId | pLegislativeDataGroupId, pLegislationCode, pDeductionGroupId | LDG ID, legislation, selected group lookup ID | All fields listed in find_wbr_reference_level, including all six definitions |
| Primary | ElementClassificationVVO | excludeGlobalData, findByLegislativeDataGroupIdAndLegislationCode, findPrimaryClassifications | pLegislationCode, pLdgLegCode, pLegislativeDataGroupId | legislation, legislation, LDG ID | ClassificationId, ClassificationName, BaseClassificationId, BaseClassificationName, ClassificationIdForFk |
| Secondary | ElementClassificationVVO | excludeGlobalData, findByLegislativeDataGroupIdAndLegislationCode, findByParentClassificationId, findSecondaryClassifications | pLegislationCode, pLdgLegCode, pLegislativeDataGroupId, pParentClassificationId | legislation, legislation, LDG ID, selected primary classification lookup ID | Primary attributes plus ParentClassificationId |
| Components | DeductionTypeForContextVO | Omitted by the source finder | pDeductionGroupId, pLegislativeDataGroupId, pUsageType, pContextId1..6 | selected group, LDG ID, T, six ContextUsageId slots | All fields listed in find_wbr_components |
| History | TaxabilityRuleAllVO | findByClassificationId, findBySecondaryClassificationId, findByDeductionTypeIds | pClassificationId, pSecondaryClassificationId, pDeductionTypeId | resolved primary foreign key, resolved secondary foreign key, resolved component foreign key | All fields listed in read_wbr_history; SortBy=EffectiveStartDate |

Commas in the table's criteria/keys/values/attributes columns denote ordered
double-pipe-separated members, not literal finder commas. If no secondary is
selected, omit its criterion and bind together and filter the returned rows for
null secondary. The all-context history query intentionally omits context
criteria. Never treat an unfiltered empty-context query as a complete scoped
result without applying LDG and all six context comparisons.

## Context Finder Contract

For a reference definition with a lookup type, use HcmLookupValuePVO,
AdditionalViewCriteria=findByLookupType, ParameterKeys=LookupTypeBindVar,
ParameterValues={lookupType}, DisplayAttributes=LookupCode||Meaning.
For a value set, use the exact returned VO name. With no parent values use
findByWord;PayRestName={voName}. With parent values use
AdditionalViewCriteria=DynamicLOV, ParameterKeys=pCodeLevel1||...||pCodeLevelN,
ParameterValues={ordered parent REST codes}, DisplayAttributes=Code||Meaning.
Accept only current metadata-selected lookup names matching [A-Za-z0-9_]{1,100}
or VO names matching [A-Za-z0-9_.]{1,300}; do not accept an arbitrary user VO.

For the verified US State/County/City hierarchy, native HDL uses the state
abbreviation and county/city business names. REST stores separate jurisdiction
codes. Resolve the state abbreviation from current jurisdiction information;
if the LOV only gives an internal code and an ambiguous meaning, obtain the
business abbreviation and verify its mapping rather than deriving one by
guessing. Other reference hierarchies require an established HDL helper-key
mapping from current metadata or BO evidence. All delivered and customer-defined
eligible values may be selected; a missing mapping is a contract gap, not an
invalid customer value.

## Physical Query and Date Contract

For a known target, query TaxabilityRulesId={id}. Independently query the
complete identity with ClassificationId, SecondaryClassificationId when present,
DeductionTypeId and populated ContextValueN predicates. Filter the response by
LDG and every context slot including nulls. Use the stored REST codes here,
not HDL keys. Reconcile a blank secondary explicitly rather than dropping it
from the comparison. Never manufacture an opaque date-effective item key;
follow a current returned link only when needed.

History may render dates with two-digit years. Never convert 12/31/12 to either
2012 or 4712 by assumption. Obtain ISO dates from the physical collection at a
date inside each candidate slice; if the period cannot be unambiguously
recovered, return DATE_MAPPING_UNRESOLVED. Compare original, boundary and later
dates as prescribed by the selected reconciliation profile.

The VBCS edit/history source marks a rule as predefined when
LegislativeDataGroupId is empty. Existing-rule mutations require a populated
LDG equal to the selected LDG; an absent field is incomplete evidence, not an
editable non-predefined row. A legislation-only predefined row must not be
reused as an LDG target. Preserve these rows separately when reviewing
predefined configuration; this delivery does not create overrides for them.

## Task Nodes

During discovery, resolve already supplied parent values through their declared
resolvers and retrieve only the choices needed for the next missing decision.
Stop before a dependent call when its binds or applicable date are unresolved.
If input remains missing, the needs_input outcome returns via WBR.HANDLE_ERROR
and WBR.RETURN_ISSUES under Intake Return and Resume in ora_error_handling.md.
Do not enter defaulting, archive validation or approval while collecting.
The resolved outcome requires all applicable requested selections and reads
to be complete, including the mutation's full prior-state checks; choices
retrieved or a unique search result alone never satisfy that outcome.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.RESOLVE_REFERENCES | decision | 3 | reference_lookup | resolved->WBR.CHECK_PREPARATION;needs_input->WBR.HANDLE_ERROR;blocked->WBR.HANDLE_ERROR | WBR.RESOLVE_DEPENDENCIES | stop | Apply Lookup Execution Rules, including existing-rule history discovery, through declared resolvers; missing selections return needs_input without advancing beyond discovery; resolved requires complete applicable inputs and reads; reconciliation uses original request identity plus fresh reads |
| WBR.VALIDATE_NATIVE_CONTRACT | decision | 6 | reference_lookup | validated->WBR.ENFORCE_DESIGN;read_only->WBR.EXECUTION_GATE;blocked->WBR.HANDLE_ERROR | WBR.APPLY_DEFAULTS | stop | Supported mutation validates the core-supplied archive; read/reconciliation skips archive validation without creating or submitting one |
