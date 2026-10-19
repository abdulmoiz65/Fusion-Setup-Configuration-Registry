# Specify Supplier News Content Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplier news content change | SupplierNewsContent and a supplierNewsContent Data Loader REST artifact scoped to Specify Supplier News Content | Block preparation | Supply the intended content in the task-scoped artifact | A content change is requested | resolve_supplier_news_content |
| No-change confirmation | Confirmation that the supplied content is unchanged | Retain the existing content | Do not prepare an update when no content change is intended | No content change is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supplier news content | Accept SupplierNewsContent as the task value to be changed. Treat an unchanged value as no change. | Always | |
| Setup-data route | Require the change to be represented in the task-scoped supplierNewsContent Data Loader REST artifact. | A content change is requested | resolve_supplier_news_content |
| Singleton readiness | Accept exactly one resolved row for an update. When no row exists, accept only the approved `supplierNewsContentInitializeSetup` Data Loader REST POST artifact followed by a fresh lookup. | Before an update handoff | resolve_supplier_news_content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Happens |
|---|---|---|---|---|---|---|---|---|
| POZ.SNC.VALIDATE_INPUT | step | 10 | validate_input | valid->POZ.SNC.APPLY_NO_CHANGE_DEFAULT;invalid->POZ.SNC.RETURN_ISSUES | none | stop | Before Data Loader REST preparation | Validate the intended supplier news content and require a task-scoped REST artifact for a requested change |
