# Shipping Cost Types Reference Lookups

Source: Shipping Cost Types Redwood page, approved resolver selection, and read-only target-environment verification.

These are advisory lookup contracts. They do not authorize or execute Fusion REST calls. The routed core.data-loader workflow owns every live lookup request, including authentication, transport, diagnostics, redaction, and exact-match enforcement.

## Live Lookups

All live lookup requests include the header `REST-Framework-Version: 9`.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_shipping_cost_type_category | A Shipping Cost Type Category Meaning or LookupCode is supplied | Category Meaning or LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_FREIGHT_COST_TYPE'&fields=LookupCode,Meaning&onlyData=true | LookupCode, Meaning | Trim and case-insensitive exact match on Meaning or LookupCode, scoped to LookupType WSH_FREIGHT_COST_TYPE. Require exactly one returned row. When both Meaning and LookupCode are supplied, require them to identify the same row. | ShippingCostTypeCategoryCode: LookupCode | Zero or multiple matches, or conflicting supplied meaning and code, blocks Data Loader handoff. Do not fuzzy-match or select the first record. |
| resolve_currency | A Currency Name or CurrencyCode is supplied | Currency Name or CurrencyCode | /fscmRestApi/resources/11.13.18.05/currenciesLOV?q=UPPER(Name) LIKE UPPER('%<Currency Name>%')&fields=CurrencyCode,Name&onlyData=true | CurrencyCode, Name | For a supplied Currency Name, filter with UPPER(Name) LIKE UPPER('%<Currency Name>%'), then trim and case-insensitive exact match on Name. For a supplied CurrencyCode, match CurrencyCode exactly after trim and case folding. Require exactly one returned row. When both Name and CurrencyCode are supplied, require them to identify the same row. | CurrencyCode: CurrencyCode | Zero or multiple matches, or conflicting supplied name and code, blocks Data Loader handoff. Do not fuzzy-match or select the first record. |
