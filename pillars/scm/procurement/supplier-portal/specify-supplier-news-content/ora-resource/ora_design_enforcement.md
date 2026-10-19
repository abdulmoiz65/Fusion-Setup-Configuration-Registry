# Specify Supplier News Content Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Row discovery | Resolve the supplier news singleton or establish that it is absent. |
| 2 | Data Loader handoff | When absent, use the approved `supplierNewsContentInitializeSetup` Data Loader REST POST artifact; otherwise prepare the supplierNewsContent content-update artifact from the resolved row. |
| 3 | Block unsupported routes | Do not plan or describe initialization or an update through an alternative integration route. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A supplier news content change is requested | Blocking | resolve_supplier_news_content | The change is not represented in the task-scoped supplierNewsContent Data Loader REST artifact | Use the catalog-supported Data Loader REST route through core.data-loader | Yes |
| Missing singleton row | Blocking | resolve_supplier_news_content | The approved `supplierNewsContentInitializeSetup` Data Loader REST POST artifact is not selected | Submit the approved artifact once, re-read, and require exactly one row before preparing the update | Yes |
| Direct create request | Blocking | resolve_supplier_news_content | A `supplierNewsContent` create, `POST`, or direct REST create route is proposed | Reject it; use only `supplierNewsContentInitializeSetup` through core.data-loader when no row exists | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_supplier_news_content | Before deciding whether to initialize or update the singleton | Match count and the resolved SupplierNewsId when exactly one row exists | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Happens |
|---|---|---|---|---|---|---|---|---|
| POZ.SNC.ENFORCE_DATALOADER_ROUTE | step | 40 | design_enforcement | passed->POZ.SNC.DATALOADER_GATE;blocked->POZ.SNC.RETURN_ISSUES | POZ.SNC.LOOKUP_CURRENT_NEWS | stop | Before the task is handed off for import | Block any content-change plan that is not limited to the supplierNewsContent Data Loader REST route |
