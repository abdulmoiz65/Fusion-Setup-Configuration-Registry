# Landed Cost Charges Reference Lookups

Every referenced lookup must use the exact header
`REST-Framework-Version: 9`.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_procurement_bu_set | Before creating a charge | searchText | /fscmRestApi/resources/11.13.18.05/costingSetsLOV?finder=IntentFinder;Intent=CML_MANAGE_LANDED_COST_CHARGE_DATA&onlyData=true&q=UPPER(SetName) LIKE UPPER('%{searchText}%')&fields=Description,SetCode,SetId,SetName&limit=25&offset=0 | Description, SetCode, SetId, SetName | Require exactly one user-selected result. | SetId | Stop on no match or ambiguous selection. |
| resolve_charge_currency | Before creating a charge | searchText | /fscmRestApi/resources/11.13.18.05/currenciesLOV?fields=CurrencyCode&onlyData=true&q=UPPER(CurrencyCode) LIKE UPPER('%{searchText}%')&limit=25&offset=0 | CurrencyCode | Require exactly one user-selected result. | EnteredCurrencyCode | Stop on no match or ambiguous selection. |
| resolve_currency_conversion_type | Before creating a charge | searchText | /fscmRestApi/resources/11.13.18.05/currencyConversionTypesLOV?onlyData=true&q=UPPER(UserConversionType) LIKE UPPER('%{searchText}%')&fields=ConversionTypeId,Description,UserConversionType&limit=25&offset=0 | ConversionTypeId, Description, UserConversionType | Require exactly one user-selected result. | CurrencyConversionType | Stop on no match or ambiguous selection. |
| resolve_charge_basis | Before creating a charge | searchText | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?onlyData=true&q=LookupType='CML_CHARGE_BASIS' AND UPPER(Meaning) LIKE UPPER('%{searchText}%')&fields=Description,LookupCode,LookupType,Meaning,Tag&limit=25&offset=0 | Description, LookupCode, LookupType, Meaning, Tag | Require exactly one CML_CHARGE_BASIS result. | ChargeBasisCode | Stop on no match or ambiguous selection. |
| resolve_charge_basis_uom | ChargeBasisCode is PER_UNIT | searchText | /fscmRestApi/resources/11.13.18.05/unitsOfMeasure?fields=UOM,UOMId,UOMCode&onlyData=true&q=UPPER(UOM) LIKE UPPER('%{searchText}%')&limit=25&offset=0 | UOM, UOMId, UOMCode | Require exactly one user-selected result. | ChargeBasisUOMCode | Stop on no match or ambiguous selection. |
| resolve_allocation_basis | Before creating a charge | searchText | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?onlyData=true&q=LookupType='CML_CHARGE_ALLOC_BASIS' AND UPPER(Meaning) LIKE UPPER('%{searchText}%')&fields=Description,LookupCode,LookupType,Meaning,Tag&limit=25&offset=0 | Description, LookupCode, LookupType, Meaning, Tag | Require exactly one CML_CHARGE_ALLOC_BASIS result. | DefaultAllocBasisCode | Stop on no match or ambiguous selection. |
| resolve_allocation_basis_uom | An allocation UOM is applicable | searchText | /fscmRestApi/resources/11.13.18.05/unitsOfMeasure?fields=UOM,UOMId,UOMCode&onlyData=true&q=UPPER(UOM) LIKE UPPER('%{searchText}%')&limit=25&offset=0 | UOM, UOMId, UOMCode | Require exactly one user-selected result. | DefaultAllocBasisUOMCode | Stop on no match or ambiguous selection. |
| resolve_default_charge_reference_type | A user elects a default charge reference type | SetId, searchText | /fscmRestApi/resources/11.13.18.05/landedCostReferenceTypes?fields=ChargeReferenceTypeId,Name,Description&onlyData=true&q=(SetId='0' OR SetId='{SetId}') AND UPPER(Name) LIKE UPPER('%{searchText}%')&limit=25&offset=0 | ChargeReferenceTypeId, Name, Description | Require exactly one selected global or selected-set result. | ChargeReferenceTypeId | Stop only the optional child association on no match or ambiguity. |
| resolve_cost_analysis_group | A user elects an analysis association | none | /fscmRestApi/resources/11.13.18.05/costAccountingCostAnalysisGroups?fields=AnalysisGroupId,AnalysisGroupCode,AnalysisGroupDescription&onlyData=true&limit=25&offset=0 | AnalysisGroupId, AnalysisGroupCode, AnalysisGroupDescription | Require exactly one user-selected group. | AnalysisGroupId | Stop only the optional child association on no match or ambiguity. |
| resolve_cost_analysis_code | A group is selected for an analysis association | AnalysisGroupId, searchText | /fscmRestApi/resources/11.13.18.05/costAccountingCostAnalysisGroups/{AnalysisGroupId}/child/costAccountingCostAnalysisCodes?fields=AnalysisId,AnalysisCode,AnalysisDescription&onlyData=true&q=UPPER(AnalysisCode) LIKE UPPER('%{searchText}%')&limit=25&offset=0 | AnalysisId, AnalysisCode, AnalysisDescription | Require exactly one user-selected code under the selected group. | AnalysisCodeId | Stop only the optional child association on no match or ambiguity. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup returns more pages | Follow pagination before applying the match rule. |
| Lookup scope | All resolvers above are read-only Fusion REST lookups. They must not create, update, delete, upload, or initiate setup data. |
| Environment identity | The orchestration workflow joins each documented path to the active, approved Fusion REST base URL. Do not ask the user for, hardcode, or override a host. |
| REST client and query encoding | Every referenced lookup must use the exact header `REST-Framework-Version: 9`. Invoke lookups through core.fusion-api.rest-api-client; retain the readable query syntax in this file and let the client encode query values for transport. |
| Lookup result safety | A LIKE predicate narrows results only; derive a value only after the documented exact selection rule is met. |
| A primary LOV lookup is unresolved | Stop before preview or import preparation. |
| An optional-child lookup is unresolved | Keep the primary charge eligible; report the child association as unresolved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCC.RESOLVE_SET | step | 20 | reference_lookup | resolved->LCC.RESOLVE_CURRENCY;unresolved->RETURN_ISSUES | LCC.VALIDATE_INPUT | stop | A valid primary charge request is supplied. |
| LCC.RESOLVE_CURRENCY | step | 30 | reference_lookup | resolved->LCC.RESOLVE_CONVERSION_TYPE;unresolved->RETURN_ISSUES | LCC.RESOLVE_SET | stop | A Procurement BU Set is resolved. |
| LCC.RESOLVE_CONVERSION_TYPE | step | 40 | reference_lookup | resolved->LCC.RESOLVE_CHARGE_BASIS;unresolved->RETURN_ISSUES | LCC.RESOLVE_CURRENCY | stop | A charge currency is resolved. |
| LCC.RESOLVE_CHARGE_BASIS | step | 50 | reference_lookup | per-unit->LCC.RESOLVE_CHARGE_BASIS_UOM;not-per-unit->LCC.RESOLVE_ALLOCATION_BASIS;unresolved->RETURN_ISSUES | LCC.RESOLVE_CONVERSION_TYPE | stop | A conversion type is resolved. |
| LCC.RESOLVE_CHARGE_BASIS_UOM | step | 60 | reference_lookup | resolved->LCC.RESOLVE_ALLOCATION_BASIS;unresolved->RETURN_ISSUES | LCC.RESOLVE_CHARGE_BASIS | stop | ChargeBasisCode is PER_UNIT. |
| LCC.RESOLVE_ALLOCATION_BASIS | step | 70 | reference_lookup | uom-applicable->LCC.RESOLVE_ALLOCATION_UOM;uom-not-applicable->LCC.CHECK_OPTIONAL_NO_ALLOCATION_UOM;unresolved->RETURN_ISSUES | LCC.RESOLVE_CHARGE_BASIS | stop | A charge basis is resolved. |
| LCC.RESOLVE_ALLOCATION_UOM | step | 80 | reference_lookup | resolved->LCC.CHECK_OPTIONAL_CHILDREN;unresolved->RETURN_ISSUES | LCC.RESOLVE_ALLOCATION_BASIS | stop | An allocation UOM is applicable. |
