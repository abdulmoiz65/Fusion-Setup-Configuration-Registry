# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_purchase_agreement_defaults_by_requisitioning_bu | Current purchase agreement defaults are requested for one requisitioning BU | Exact RequisitioningBUName | /fscmRestApi/resources/11.13.18.05/externalPurchasePricesPurchaseAgreementDefaults?q=RequisitioningBUName='{encoded RequisitioningBUName}'&fields=PaDefaultId,RequisitioningBUName,ActiveFlag,ConfirmingOrderFlag,AllowPriceOverrideFlag,RoundingFactor,RetroPriceCommUpdatesFlag,RetroPriceOpenOrderFlag,RetroPriceInitApprovalFlag,RetroPriceApplyUpdatesFlag,AllowMultipleSitesFlag,ApprovalAction,ApprovalActionCode&onlyData=true&limit=500&offset={offset} | PaDefaultId, RequisitioningBUName, ActiveFlag, ConfirmingOrderFlag, AllowPriceOverrideFlag, RoundingFactor, RetroPriceCommUpdatesFlag, RetroPriceOpenOrderFlag, RetroPriceInitApprovalFlag, RetroPriceApplyUpdatesFlag, AllowMultipleSitesFlag, ApprovalAction, ApprovalActionCode | Use core.fusion-api.rest-api-client with GET and REST-Framework-Version 9. URL-encode the supplied value, follow pagination until hasMore=false, and require exactly one returned record whose RequisitioningBUName exactly equals the supplied value. Never fuzzy-match or select the first result. | PaDefaultId and the returned default fields for the exact requisitioning BU | Zero exact matches: return confirmed not-found. Multiple exact matches, incomplete pagination, malformed collection data, authentication or authorization failure, transport failure, or Fusion API failure: stop and report a sanitized diagnostic. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| RequisitioningBUName is blank or ambiguous | Stop before the GET and request one exact requisitioning BU name. |
| The lookup returns one exact match | Return the configured purchase agreement default fields for that BU. |
| The lookup returns no exact match | Return confirmed not-found; do not infer that an All Business Units record applies. |
| The lookup returns multiple exact matches or pagination is incomplete | Stop and report an ambiguous or incomplete read; do not select a record. |
| The REST read fails | Stop and return a sanitized authentication, authorization, transport, or Fusion API diagnostic. Do not fall back to Data Loader. |
