# Specify Supplier News Content Reference Lookups

## Live Lookups

| Resolver | Runs When | Request Path or URL | Requested Fields | Match Rule | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_supplier_news_content | Before initialization or a supplier news content update, and after initialization or update verification | `core.fusion-api.rest-api-client` GET `/fscmRestApi/resources/11.13.18.05/supplierNewsContent?onlyData=true&limit=2&fields=SupplierNewsId,SupplierNewsContent` | SupplierNewsId, SupplierNewsContent | Return exactly one supplier news row; no identifier filter is supplied. | Zero rows require the approved `supplierNewsContentInitializeSetup` Data Loader REST POST artifact; multiple rows block. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A row is returned | Retain the resolved `SupplierNewsId` only as current-state evidence and use the sample-confirmed mapping for the `SupplierNewsContent` update artifact. |
| No row is returned | Prepare the approved minimal `supplierNewsContentInitializeSetup` Data Loader REST POST artifact, submit it once after approval, then re-run this lookup. |
| Initialization returns success or row exists | Re-run this lookup and require exactly one row before preparing the content update. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POZ.SNC.LOOKUP_CURRENT_NEWS | step | 30 | reference_lookup | resolved->POZ.SNC.ENFORCE_DATALOADER_ROUTE;not_found->POZ.SNC.INITIALIZE_GATE;ambiguous->POZ.SNC.RETURN_ISSUES;failure->POZ.SNC.RETURN_ISSUES | POZ.SNC.APPLY_NO_CHANGE_DEFAULT | stop | Before initialization or a supplier news content update. |
