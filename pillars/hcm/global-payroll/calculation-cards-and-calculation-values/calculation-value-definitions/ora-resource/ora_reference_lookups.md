# Calculation Value Definitions Reference Lookups

## Read-Only Lookup Boundary

Use Fusion reads only for business-value selection, inspection, and
reconciliation. A resolved ID, link, child record, or metadata result does not
authorize a mutation. Keep internal identifiers and transport details out of
user-facing results. Unavailable child writes stop before mutation-specific
lookup preparation.

## Large Choice Sets

When an omitted required choice has 20 or fewer eligible values, present the
complete sorted business-label list. When it has more than 20 values, report
the total and ask the user for a business-name or business-code search term.
Do not show an arbitrary sample and then require an exact value that was not
shown.

Match the search term using case-insensitive contains semantics. Use a
server-side filter only when that exact filter is declared for the resolver in
this contract. Otherwise complete source pagination and filter the authorized
result set locally. Present at most 20 sorted matches per page, state when more
matches remain, and let the user refine the term or request the next page.

Zero filtered matches keeps the operation in `collecting` and invites a new
term; it is not a global `NOT_FOUND` unless the complete source-backed lookup
was searched. One filtered match is still a choice to confirm unless the user
had already supplied that exact unique business value. Never present internal
IDs as search-page choices or discriminators.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| extract_active_resource_links | A parent or child response will be used for GET navigation, reconciliation, or future native HDL investigation | Current response body, resource name, effectiveAsOfDate | Select links by exact rel, name, and expected resource path; never compose an opaque item key | parentItemKey, childItemKey, selfLink, childCollectionLinks, retrievedAt | Missing link blocks the read/evidence step; duplicate conflicting links are a contract mismatch |
| resolve_parent_calculation_type_semantics | A CVD-HDL04 or CVD-HDL10 CalculationTypeVO selection needs a semantic code | Selected row's Code, Meaning, CalculationTypeId, and CalculationTypeName | Require the numeric ID fields to agree and Meaning/CalculationTypeName to agree when both are present. Use a returned nonnumeric semantic Code when recognized; when Code repeats the numeric ID, use the exact normalized guidance map below. An exact live customer-defined label absent from the map remains valid but has unresolved semantics until resolve_parent_payload_shape establishes them from current evidence. | CalculationTypeId, CalculationTypeCode when resolved, CalculationTypeName, calculationTypeResolution | A conflicting live row is CATALOG_MISMATCH. A map omission is not invalid; CVD-HDL04 remains shape-unresolved and CVD-HDL10 remains outside its fixed Flat Amount profile. Do not call this resolver for CVD-HDL11. |
| resolve_parent_payload_shape | Standalone CVD-HDL04 has one exact current CalculationTypeVO selection | The exact selected CalculationTypeVO row, resolved semantic code when available, current create-field semantics, live ValueDefinition attributes and ValueDefinition.dat template, declared field resolvers, the exact selected PAY_UNITS row only when the preliminary field-state result makes UOM applicable, and readable payrollCalculationValueDefinitions attributes | Resolve in two phases. Phase 1 uses the exact Calculation Type and current field-state evidence to establish its semantic type and classify UOM and every other conditional candidate as required, optional, or forbidden. If UOM is applicable, resolve an explicit exact PAY_UNITS selection. Phase 2 finalizes every field classification and requires live-template membership, resolver lineage where applicable, and an exact read-back mapping for every authored conditional field. Fixed fields are BaseName, EffectiveStartDate, ValueGroupName, CalculationTypeName, LegislativeDataGroupName, and ValueDefinitionName. Conditional candidates are CurrencyCode, Uom, DateMode, Periodicity, DatabaseItemName, and ValueIdentifier. A customer-defined label may reuse a known semantic shape when its exact live row supplies that semantic code. | preliminaryParentFieldState, parentPayloadShape, authoredParentFields, parentReadbackMappings | If the preliminary UOM applicability decision or any final required/optional/forbidden classification, template field, resolver, or read-back mapping is unresolved, return PAYLOAD_SHAPE_UNRESOLVED before DAT authoring. Do not request UOM until Phase 1 makes it applicable; do not call the Calculation Type or Unit of Measure invalid and do not guess or silently drop a field. |

## Parent Calculation Type Semantic Map

This map supplies known semantic-shape guidance when the live Calculation Type
LOV repeats the numeric ID in `Code`. Matching is case-insensitive after
trimming and collapsing whitespace; no partial, fuzzy, translated, or
similarity match is allowed.

The map is not a business-value or customer-extension allowlist. Standalone
CVD-HDL04 accepts every exact current CalculationTypeVO row and applicable
PAY_UNITS row, including a customer-defined label or non-Money unit, when
`resolve_parent_payload_shape` can prove its complete parent field shape.
CVD-HDL10, CVD-HDL05, and CVD-HDL07A/CVD-HDL07B retain their explicit Flat
Amount/Money restrictions. CVD-HDL11 uses the exact values on the freshly
resolved existing parent. Absence from this map never makes a CVD-HDL04 or
CVD-HDL11 tenant value invalid; an unresolved payload shape blocks authoring
without changing the lookup result.

| Exact Calculation Type Name | Semantic Code |
|---|---|
| Text | X |
| Flat Rate | T |
| Rate Definition | RD |
| Flat Amount | F |
| Flat Amount Multiplier | FM |
| Flat Amount Times Multiplier | FM |
| Node | NO |
| Number | N |
| Identifier | VC |
| Value Identifier | VC |
| Standard Formula 1 | S1 |
| Standard Formula 2 | S2 |
| Flat Rate Derived | FP |
| Flat Rate By Derived Base | RDB |
| Incremental Calculation | GC |
| Date | D |
| Incremental Rate | G |

## Live Lookups

For the supported native HDL operations, the user-facing interface accepts and
returns business labels only. Numeric IDs listed in this table are resolver
inputs or outputs for operation-local machine state; they are never prompt
values or user-visible disambiguators. If duplicate labels remain, use scope,
effective dates, or other business attributes to disambiguate.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_legislative_data_group | The task starts or LDG changes | LDG name or an internally retained ID | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV?onlyData=true&orderBy=Name&limit=1000 | LegislativeDataGroupId, Name, LegislationCode | Exact internal ID or case-insensitive exact Name within the authorized result set | LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode, Country | Zero is NOT_FOUND; many is AMBIGUOUS; never select the first row silently and never request an ID from the user |
| find_calculation_type | Parent create, CVD-HDL11 parent-type validation, or calculation-type validation | LegislativeDataGroupId, LegislationCode, and either the current-operation parent-create selection or the fresh CVD-HDL11 parent's CalculationTypeId, CalculationTypeName, and Type | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=CalculationTypeVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLegislationCode,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;CalculationTypeId&#124;&#124;CalculationTypeName,SortBy=Meaning&onlyData=true&fields=Code,Meaning,ResultKey1,ResultValue1,ResultKey2,ResultValue2,ResultKey3,ResultValue3,ResultKey4,ResultValue4&limit=100 | Code, Meaning, CalculationTypeId, CalculationTypeName | Complete pagination. For parent create, require the current-operation selection and retain the exact returned row. Standalone CVD-HDL04 accepts every exact current row, including a customer-defined label, then calls resolve_parent_payload_shape; use resolve_parent_calculation_type_semantics only to obtain semantic guidance when needed. CVD-HDL10 still requires Flat Amount. For CVD-HDL11, require one exact returned row agreeing with the fresh parent's internal CalculationTypeId and exact case-insensitive CalculationTypeName. If a selection is omitted, return the complete eligible list without selecting a row. | Candidate choices for parent create; after selection, CalculationTypeId, CalculationTypeCode when returned/resolved, CalculationTypeName, calculationTypeResolution | Zero or empty active list is NOT_FOUND. An omitted selection remains NEEDS_INPUT even for one candidate. Multiple exact matches or disagreement with a fresh parent are AMBIGUOUS or CATALOG_MISMATCH. A packaged-map omission is not an invalid CVD-HDL04 or CVD-HDL11 value; unresolved CVD-HDL04 semantics proceed to PAYLOAD_SHAPE_UNRESOLVED, while a non-Flat-Amount CVD-HDL10 remains frozen. |
| find_value_definition_group | Parent create with existing group | LegislativeDataGroupId, LegislationCode, and the current-operation group selection when supplied | GET /hcmRestApi/resources/11.13.18.05/payrollValueDefinitionGroups?finder=findByLegislativeDataGroupId;LegislativeDataGroupId={LDG_ID},LegislationCode={LEG_CODE}&fields=ValueGroupId,Name&onlyData=true&orderBy=Name&limit=25 | ValueGroupId, Name | Complete pagination. If a current-operation selection exists, require exact numeric ID or case-insensitive exact Name in the selected LDG. If omitted, return the complete scoped list without selecting a row. | Candidate choices; after user selection, ValueGroupId, ValueGroupName | Zero is NOT_FOUND. An omitted selection remains NEEDS_INPUT even for one candidate; present the choices. Multiple exact matches to a supplied value are AMBIGUOUS. Do not create a group in this resource contract. |
| find_parent_definition | Parent detail; CVD-HDL04 or CVD-HDL10 duplicate check and reconciliation; CVD-HDL05 or CVD-HDL11 baseline/duplicate check; CVD-HDL07A/CVD-HDL07B/CVD-HDL07C target validation; lifecycle reconciliation; or exact read | ValueDefnId or Name, LegislativeDataGroupId, LegislationCode, effectiveAsOfDate | When starting with Name, first GET /hcmRestApi/resources/11.13.18.05/payrollCalculationValueDefinitions?finder=findByFilterAttributes;SearchItem="{PARENT_NAME}",FilterAttributes="LegislativeDataGroupScope:{LDG_ID}&#124;{LEG_CODE}"&effectiveDate={AS_OF_DATE}&fields=ValueDefnId,Name,BaseName,EffectiveStartDate,EffectiveEndDate,LegislativeDataGroupId,LegislationCode,LegislationDiscriminator,ValueGroupId,ValueGroupName,CalculationTypeId,CalculationTypeName,Type,UnitOfMeasure,Uom,CurrencyCode,DateMode,Periodicity,DatabaseItemId,DBItemBaseUserName,ValueIdentifier&onlyData=true&orderBy=Name&limit=500; after resolving one exact candidate, GET /hcmRestApi/resources/11.13.18.05/payrollCalculationValueDefinitions?finder=findByWord;ValueDefnId={VALUE_DEFN_ID}&effectiveDate={AS_OF_DATE}&expand=RangeItems,AllowedOverrides.OverrideUsages,ValueUsages,RelatedElements, omitting onlyData=true and any restrictive fields projection so current item, conditional parent attributes, and child links are retained. When ValueDefnId is supplied, skip directly to the exact read. Never follow or reconstruct the advertised /child/RangeItems link for verification; it returned HTTP 404. | ValueDefnId, Name, BaseName, ValueGroupName, CalculationTypeId, CalculationTypeName, Type, UnitOfMeasure, Uom, CurrencyCode, DateMode, Periodicity, DatabaseItemId, DBItemBaseUserName, ValueIdentifier, LegislativeDataGroupId, EffectiveStartDate, EffectiveEndDate, complete child rows/counts, links | Complete discovery pagination, then require exact case-insensitive Name or BaseName and exact LegislativeDataGroupId; require exact ValueDefnId, SysEffectiveDate={AS_OF_DATE}, and the selected effective slice in the expanded read. For CVD-HDL04 or CVD-HDL10 preflight, require zero exact parent matches. CVD-HDL04 reconciliation requires every fixed and conditional authored field to match through parentReadbackMappings. CVD-HDL10 reconciliation requires the exact parent and one exact same-start Range Item in the same expanded response, with zero other children. For CVD-HDL05 require Flat Amount, Money, open-ended parent state, zero Range Items, and no child with the proposed lower bound. For CVD-HDL11 require nonproduction, open-ended parent state, an exact current Calculation Type LOV match, an exact applicable Unit of Measure lookup match when the parent has one, exactly one baseline Range Item, zero other child families, and no existing row with the proposed lower bound or a type-comparable overlapping interval. Its calculation type may be delivered or customer-defined and its unit need not be Money. For CVD-HDL07A require the operation-bound selected target, Flat Amount, Money, open-ended state, zero children, and exact current Currency. For CVD-HDL07B require that same profile, no existing future slice, and complete current/new Currency evidence. For CVD-HDL07C require zero children and complete evidence of exactly one physical slice. | Parent record, effective slice, business profile, internal ID/link evidence, child counts, CVD-HDL04 duplicate/read-back result, CVD-HDL10 duplicate/reconciliation result, CVD-HDL05 or CVD-HDL11 lower-bound/baseline result, or CVD-HDL07A/CVD-HDL07B/CVD-HDL07C target binding | Zero exact discovery matches is READY only for CVD-HDL04 or CVD-HDL10 duplicate preflight and is otherwise NOT_FOUND; many exact matches is AMBIGUOUS; a missing self link, mismatched SysEffectiveDate, or unavailable authored-field read-back is CATALOG_MISMATCH or CONTRACT_INCOMPLETE as applicable; a direct RangeItems-child read is non-authoritative; IDs remain internal and native HDL uses only operation-specific business-key fields |
| find_retrieval_date_code | DateMode is supplied as display text | Display value | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=HcmLookupValuePVO,AdditionalViewCriteria=findByLookupType,ParameterKeys=LookupTypeBindVar,ParameterValues=PAY_DED_DATE_MODE,DisplayAttributes=LookupCode&#124;&#124;Meaning&#124;&#124;Description,SortBy=Meaning&onlyData=true&limit=200 | LookupCode, Meaning, Description | Exact LookupCode or case-insensitive exact Meaning | DateMode, DateModeMeaning | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_unit_of_measure_code | CVD-HDL04 preliminaryParentFieldState makes UnitOfMeasure applicable, UnitOfMeasure is supplied for a fixed parent-create profile, or a CVD-HDL11 parent has a UnitOfMeasure | Selected calculation type and either the current-operation unit selection or the fresh CVD-HDL11 parent's UnitOfMeasure | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=HcmLookupValuePVO,AdditionalViewCriteria=findByLookupType,ParameterKeys=LookupTypeBindVar,ParameterValues=PAY_UNITS,DisplayAttributes=LookupCode&#124;&#124;Meaning&#124;&#124;Description,SortBy=Meaning&onlyData=true&limit=200 | LookupCode, Meaning, Description | Complete pagination. Require exact LookupCode or case-insensitive exact Meaning for the current-operation selection. Standalone CVD-HDL04 accepts every exact value that preliminaryParentFieldState marks applicable, including non-Money units; the exact selection is then used to finalize parentPayloadShape. CVD-HDL10 remains Money-only. For CVD-HDL11, require one exact row agreeing with the existing parent value and do not author Uom in the RangeItemOverride DAT. If a parent-create selection is omitted, return the complete PAY_UNITS list without selecting a row. | Candidate choices for parent create; after selection, UnitOfMeasure and UnitOfMeasureMeaning from the exact live match | Zero is NOT_FOUND. An omitted parent-create selection remains NEEDS_INPUT even for one candidate. Multiple exact matches are AMBIGUOUS. A valid non-Money unit is eligible for CVD-HDL04 and CVD-HDL11 when applicable; it remains outside CVD-HDL10. |
| find_currency | CurrencyCode is supplied or changed | Currency code/name | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=ValueDefinitionCurrencyLOVVO,DisplayAttributes=CurrencyCode&#124;&#124;Name,SortBy=Name&fields=ResultValue1,ResultValue2&onlyData=true&limit=1000 | CurrencyCode, Name | Exact CurrencyCode or case-insensitive exact Name | CurrencyCode, CurrencyName | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_default_currency | A resolved CVD-HDL04 parentPayloadShape makes CurrencyCode applicable and it is blank, or the fixed CVD-HDL10 Flat Amount parent omits it | LegislationCode | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=oracle.apps.hcm.legconfig.setup.restModel.view.DefaultCurrencyVO,ParameterKeys=pLegCode,ParameterValues={LEG_CODE},DisplayAttributes=CurrencyCode&#124;&#124;Name&onlyData=true&limit=1 | CurrencyCode, Name | Use the single configured row only | CurrencyCode, CurrencyName | Zero leaves an optional field blank; if the resolved shape requires CurrencyCode, remain in collecting. Many is a catalog mismatch. |
| find_periodicity_code | Periodicity is supplied as display text | Display value | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=HcmLookupValuePVO,AdditionalViewCriteria=findByLookupType,ParameterKeys=LookupTypeBindVar,ParameterValues=PAY_TMPLT_ET_TIME_DEFINITION,DisplayAttributes=LookupCode&#124;&#124;Meaning&#124;&#124;Description,SortBy=Meaning&onlyData=true&limit=200 | LookupCode, Meaning, Description | Exact LookupCode or case-insensitive exact Meaning | Periodicity, PeriodicityMeaning | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_database_item | CVD-HDL04 parentPayloadShape requires a database item, including FM | LegislativeDataGroupId, LegislationCode, and current-operation business item selection | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=RangeDatabaseItemLOVVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLdgLegCode&#124;&#124;pLegislationCode,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE}&#124;&#124;{LEG_CODE},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;Description&fields=ResultValue1,ResultValue2&onlyData=true&limit=10000 | Code, Meaning, Description | Exact numeric Code retained internally or case-insensitive exact Meaning selected by the user | DatabaseItemId, DatabaseItemName | Zero is NOT_FOUND; many is AMBIGUOUS. Native HDL authors only DatabaseItemName, never DatabaseItemId. |
| find_override_type | Override-type read or future controlled Allowed Override BO proof | Parent calculation type code, supplied override code/meaning | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=OverrideTypeLOVVO,DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;LookupType,ParameterKeys=pCalculationType,ParameterValues={CALC_TYPE_CODE}&fields=Code,Meaning,ResultKey3,ResultValue3&onlyData=true&limit=100 | Code, Meaning, LookupType | Exact Code or case-insensitive exact Meaning in the returned eligible set | OverrideType, OverrideTypeMeaning | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_calculation_value_definition | Parent type GC, RDB, or FP needs a referenced definition | LDG, legislation, current ValueDefnId, supplied definition name/ID | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=CalculationValueDefinitionLOVVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLegislationCode&#124;&#124;pValueDefnId,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE}&#124;&#124;{CURRENT_VALUE_DEFN_ID},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;ValueDefinitionId&#124;&#124;CalculationTypeName&#124;&#124;CalculationType,SortBy=Meaning&fields=Code,Meaning,ResultKey3,ResultValue3,ResultKey4,ResultValue4,ResultKey5,ResultValue5&onlyData=true&limit=10000 | Code, Meaning, ValueDefinitionId, CalculationTypeName, CalculationType | Exact numeric ID or case-insensitive exact Meaning; current parent must be excluded | ReferencedValueDefnId, ReferencedValueDefnName, ReferencedCalculationType | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_rate_definition | Parent type RD needs a rate definition calculation value | LDG, legislation, effective date, supplied name/ID | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=RateDefinitionLOVVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLegislationCode&#124;&#124;pLdgLegCode&#124;&#124;pEffectiveDate,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE}&#124;&#124;{LEG_CODE}&#124;&#124;{AS_OF_DATE},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;BaseName,FilterAttributes=Meaning&#124;&#124;BaseName,SortBy=Meaning&fields=Code,Meaning,ResultKey1,ResultValue1,ResultKey2,ResultValue2,ResultKey3,ResultValue3&onlyData=true&limit=10000 | Code, Meaning, BaseName | Exact numeric Code or case-insensitive exact Meaning/BaseName | RateDefinitionId, RateDefinitionName | Zero is NOT_FOUND; many is AMBIGUOUS |
| find_range_item | A Range Item is checked for CVD-HDL05 or CVD-HDL11 uniqueness, selected through CVD-HDL09S, read, or reconciled for CVD-HDL05, CVD-HDL10, CVD-HDL11, CVD-HDL09A, CVD-HDL09B, or CVD-HDL09D | Active expanded parent resolved by find_parent_definition, business range bounds, item start date when selecting an existing item, and as-of date | Use the parent response's RangeItems collection or expanded rows and complete pagination | RangeDefId, LowValue, HighValue, LowValueText, RangeValueA, RangeValueB, RangeValueC, ValueIdentifier, every additional result attribute returned by the current expanded row, EffectiveStartDate, EffectiveEndDate, links | Before HDL05, compare lower bounds numerically and require zero matches. Before HDL11, require exactly one baseline row and zero exact lower-bound matches; apply interval ordering and overlap checks only when the resolved bound type is comparable. Use the parent's Type and the baseline's populated RangeValueA/B/C fields, plus current live metadata when available, to establish the required CVD-HDL11 result signature. Declare Value1/Value2/Value3 to RangeValueA/RangeValueB/RangeValueC; every additional authored result field requires an exact current expanded-row attribute mapping before preview. A customer-defined label is eligible when its live semantic shape resolves; absence from the packaged map is not a conflict. For CVD-HDL09S, first require exact parent name, LDG, and as-of date, then match the user-facing From value and item start date; use To value and Flat Amount only as optional refiners. Require explicit selection when multiple rows remain. During CVD-HDL11 reconciliation, require Range Item count 1 -> 2, the unchanged baseline, and exactly one new row with the requested bounds, start date, open-ended result, every authored Value slot mapped to its corresponding RangeValue attribute, and every additional authored result field matched through its predeclared expanded-row attribute. Retain IDs only as read evidence. | Duplicate/overlap count, resolved result-slot shape, resultReadbackMappings, or exact Range Item record and physical range | A preflight duplicate or applicable overlap is CONFLICT; an unresolved result-slot shape or missing read-back mapping remains unresolved without declaring the LOV value invalid; target or reconciliation zero is NOT_FOUND and many is AMBIGUOUS; never ask the user for RangeDefId |
| find_allowed_override | An Allowed Override is read, reconciled, or inspected for future controlled BO proof | Active parent record, Prompt, OverrideType, and as-of date | Use the active parent record's AllowedOverrides collection link and complete the collection read | AllowOverridesId, OverrideType, Prompt, EffectiveStartDate, EffectiveEndDate, links | Exact business Prompt plus OverrideType in the active slice; a previously resolved internal ID may confirm but never replace business selection | AllowOverridesId, allowedOverrideItemKey, allowedOverrideSelfLink, overrideUsagesCollectionLink, physical range | Zero is NOT_FOUND; many is AMBIGUOUS; never ask the user for AllowOverridesId |
| find_override_usage_receipt | An Override Usage is read or reconciled, or a nested read through reconstructed readable ancestor keys returns 404 | Business card/component/value-set selection, internally retained DirOverrideUsageId, and effectiveAsOfDate | Select through the saved nested collection response; reconcile with GET /hcmRestApi/resources/11.13.18.05/payrollOverrideUsageRules?finder=findByDirOverrideUsageId;DirOverrideUsageId={DIR_OVERRIDE_USAGE_ID}&effectiveDate={AS_OF_DATE}&onlyData=true | DirOverrideUsageId, EffectiveStartDate, EffectiveEndDate, AllowOverridesId, DirCardComponentDefId, DCCDDirCardComponentDefId, ComponentName, DirCardDefinitionId, LegislativeDataGroupId, LegislationDiscriminator, LegislationCode, ValueSetCode | Require exactly one business selection in the nested collection, then exactly one root read with the retained usage ID, effective slice, owning Allowed Override, and expected historical values | Override Usage target/receipt, nested self link, physical range, and current joined display values | Zero is NOT_FOUND only after the exact-ID root read; many or mismatched values are AMBIGUOUS/OUTCOME_UNKNOWN. This resolver is read-only and never authorizes a nested CVD write |
| find_calculation_card | Calculation Card choices are read or future native HDL Usage Rule investigation is requested | LDG, legislation, effective date, supplied card name or an internally retained ID | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=CalculationCardLOVVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLegislationCode&#124;&#124;pEffectiveDate,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE}&#124;&#124;{AS_OF_DATE},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;DirCardDefinitionId&#124;&#124;BaseDisplayName&#124;&#124;Description,SortBy=Meaning&fields=Code,Meaning,ResultKey3,ResultValue3,ResultKey4,ResultValue4,ResultKey5,ResultValue5&onlyData=true&limit=10000 | Code, Meaning, DirCardDefinitionId, BaseDisplayName, Description | Exact internal DirCardDefinitionId or case-insensitive exact Meaning/BaseDisplayName | DirCardDefinitionId, CalculationCardName | Zero is NOT_FOUND; many is AMBIGUOUS; never request the ID from the user |
| find_calculation_component | Calculation Component choices are read or future native HDL Usage Rule investigation is requested | LDG, legislation, internally retained DirCardDefinitionId, effective date, supplied component name or an internally retained ID | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=CalculationComponentLOVVO,ParameterKeys=pLegislativeDataGroupId&#124;&#124;pLegislationCode&#124;&#124;pDirCardDefinitionId&#124;&#124;pEffectiveDate,ParameterValues={LDG_ID}&#124;&#124;{LEG_CODE}&#124;&#124;{CARD_ID}&#124;&#124;{AS_OF_DATE},DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;DirCardCompDefId&#124;&#124;DirCardDefinitionId&#124;&#124;ElementTypeId&#124;&#124;BaseComponentName,SortBy=Meaning&onlyData=true&limit=10000 | Code, Meaning, DirCardCompDefId, DirCardDefinitionId, ElementTypeId, BaseComponentName | Exact internal component ID or case-insensitive exact Meaning/BaseComponentName, and returned DirCardDefinitionId equals selected card | DirCardCompDefId, CalculationComponentName | Zero is NOT_FOUND; many is AMBIGUOUS; mismatched card ID is CATALOG_MISMATCH; never request an ID from the user |
| find_table_value_set | Value Set choices are read, a future controlled Usage Rule BO proof is requested, or a CVD-HDL11 result shape requires ValueSetName | Value set code/meaning | GET /hcmRestApi/resources/11.13.18.05/payrollGenericLOV?finder=findByWord;PayRestName=TableValueSetLOVVO,DisplayAttributes=Code&#124;&#124;Meaning&#124;&#124;ValueSetId&#124;&#124;Description&#124;&#124;ValidationType&#124;&#124;ValueDataType,SortBy=Meaning&fields=Code,Meaning,ResultKey3,ResultValue3,ResultKey4,ResultValue4,ResultKey5,ResultValue5,ResultKey6,ResultValue6&onlyData=true&limit=10000 | Code, Meaning, ValueSetId, Description, ValidationType, ValueDataType | Exact Code or case-insensitive exact Meaning and ValidationType equals TABLE. For CVD-HDL11, the exact Code may supply ValueSetName only when the resolved shape and live template require that field; this resolver does not validate ValueSetValue. | ValueSetCode, ValueSetMeaning, ValueSetId, ValueDataType | Zero is NOT_FOUND; many is AMBIGUOUS; a non-TABLE row is invalid. A CVD-HDL11 shape requiring ValueSetValue remains unresolved unless a separate declared resolver proves the exact member. |

For CVD-HDL04 and CVD-HDL10 parent-create duplicate preflight, zero exact
`find_parent_definition` matches is the required uniqueness result and is
`READY`, not `NOT_FOUND`. One or more exact matches is `CONFLICT`. This
operation-specific rule takes precedence over the resolver's generic target
lookup zero-match behavior.

## CVD-HDL04 Parent Read-Back Contract

After a terminal CVD-HDL04 load, `find_parent_definition` must perform the
complete exact expanded parent GET without a restrictive `fields` projection.
It must match the fixed business identity and every conditional field listed in
the operation-bound `parentReadbackMappings`. A successful loader result without
this read-back is not completion.

| Authored HDL field | Exact read-back evidence |
|---|---|
| BaseName | BaseName |
| EffectiveStartDate | EffectiveStartDate for the selected physical slice |
| ValueGroupName | ValueGroupName |
| CalculationTypeName | CalculationTypeName, with Type agreeing with the resolved semantic code when one was available |
| LegislativeDataGroupName | LegislativeDataGroupId agrees with the selected LDG receipt; never expose the ID |
| ValueDefinitionName | Name |
| CurrencyCode | CurrencyCode |
| Uom | UnitOfMeasure or Uom |
| DateMode | DateMode |
| Periodicity | Periodicity |
| DatabaseItemName | DBItemBaseUserName, with DatabaseItemId agreeing with the internally retained find_database_item receipt |
| ValueIdentifier | ValueIdentifier |

If an authored conditional field is absent from the current response, cannot be
mapped exactly, or differs from the request, classify the result as
`CONTRACT_INCOMPLETE` or `OUTCOME_UNKNOWN` and never replay the write.

## Parent Lifecycle Target Selection

For a parent Correct, Update, or Delete request, run
`find_parent_definition`. The first GET produces a complete label-only
candidate page from LDG, effective as-of date, and Name or Base Name search
text. Value Definition Group, Calculation Type, and Unit of Measure are local
refiners, not additional server finder claims. Currency and child counts come
only from the fresh exact expanded GET after explicit selection. CVD-HDL07A,
CVD-HDL07B, and CVD-HDL07C may consume that operation-bound receipt for their
released Parent Correct, Parent Update, and restricted Parent Delete profiles.

Keep the selected Value Definition ID, item key, and self link in technical
state. Never display them. The technical receipt also retains the selected
target's group, calculation type, unit, current Currency, physical range, and
child counts for HDL07A/HDL07B/HDL07C fingerprinting. CVD-HDL07B additionally requires
complete source-backed evidence that no future slice already exists. One active
slice is not proof of one physical slice; CVD-HDL07C remains ineligible without
complete operation-local creation or source-backed timeline evidence.

## Range Item Lifecycle Target Selection

For a Range Item Correct, Update, or Delete request, resolve one parent first
using its business name, LDG, and effective as-of date. Read the complete
`RangeItems` collection only through the expanded parent response. Filter by
the user-facing From value and item start date; To value and Flat Amount may
refine an ambiguous set. Require one explicit selection when more than one row
remains. Keep `RangeDefId` and links only in technical state and bind the plan
to the selected business values, physical range, and fresh parent response
fingerprint.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup returns hasMore=true | Continue using the returned limit/offset until complete before evaluating zero, one, or many matches. |
| A lookup name returns zero exact matches | Return NOT_FOUND with the field and sanitized value; do not pass the display text as an ID/code. |
| A lookup name returns multiple exact matches | Return AMBIGUOUS and present concise distinguishing fields; do not choose automatically. |
| A new parent request omits Value Definition Group, Calculation Type, or applicable Unit of Measure | Run the corresponding complete read-only lookup and remain in collecting until the user selects one. Present all options only when there are 20 or fewer; otherwise apply the large-choice search-term and bounded-page contract above. A prior value or a sole candidate is not a selection. |
| A selected Calculation Type or applicable Unit of Measure resolves exactly but differs from Flat Amount (F) or Money (M) | For standalone CVD-HDL04, accept the exact live value, including a customer-defined Calculation Type name or non-Money unit, and continue to resolve_parent_payload_shape. For CVD-HDL10 and its ordinary Range Item, preserve the value as evidence and return CVD_HDL_ROUTE_FROZEN. For CVD-HDL11, accept the exact existing-parent value and continue to result-shape validation. |
| An internally retained ID/code is validated by one exact returned row | Reuse it in operation-local technical state and do not repeat the lookup unless a dependency changes; never request it from the user. |
| A dependency changes | Invalidate all downstream lookup values listed in ora_dependency_readiness.md. |
| A lookup request is unauthorized | Refresh the configured authorized session once for a read-only lookup; never request or log raw credentials. |
| A lookup transport or server failure occurs | Preserve sanitized status and message, classify it, and leave downstream values unresolved. |
| A Generic LOV result exposes named ResultKey/ResultValue pairs | Map by ResultKey name, not by positional assumption, when both are available. |
| CalculationTypeVO returns a numeric value in Code equal to CalculationTypeId | For CVD-HDL04 or CVD-HDL10, use resolve_parent_calculation_type_semantics as guidance, then require the operation-specific payload-shape gate. An exact CVD-HDL04 customer-defined label absent from the packaged map remains valid but shape-unresolved until current evidence establishes its semantics. For CVD-HDL11, an exact ID/name match to the fresh parent is sufficient. Preserve IDs internally; never expose or author CalculationTypeId/CalcTypeId. |
| An opaque parent or child key is needed | Extract it from the current response link; never concatenate dates and IDs even if a returned key resembles that shape. |
| A lookup completes | Store source resolver, resolved ID/code, display value, scope, effective date, and retrieval time, but no secret material. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.RESOLVE_REFERENCES | decision | 3 | reference_lookup | resolved->CVD.APPLY_DEFAULTS;not_required->CVD.APPLY_DEFAULTS;blocked->CVD.HANDLE_ERROR | CVD.RESOLVE_DEPENDENCIES | stop | Dependencies are classified and one or more exact references are required |
