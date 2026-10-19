# Configure Item Transaction Defaults Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Oracle Fusion Cloud Applications REST API, Standard Lookups List of Values REST Endpoints, 26b, https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-standard-lookups-list-values.html | Confirms the standard-lookups list-of-values collection supports a read-only GET route |
| Oracle Fusion Cloud SCM REST API, Create One Item Transaction Default, 26c, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/op-itemtransactiondefaults-post.html | Confirms the Default Type code/meaning fields used by this task |
| Redwood UI source, `inventory-transactions-setup-ui` commit `ffeef64afea9fa606bba1b3fb1a1eed3f83e6abf`, `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/layout.json` and `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/create-page.js` | Confirms the task UI uses `INV_ITEM_TXN_DEFAULTS_TYPE` and submits the selected Meaning as `DefaultTypeMeaning` |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Default Type resolution | Resolve a supplied DefaultType or DefaultTypeMeaning to a standard-lookup Meaning before Data Loader preparation |
| 2 | Data Loader metadata visibility | Use the registered Item Transaction Defaults business object for execution planning |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| default_type_identity | Default Type identity | Conditional | DefaultType or DefaultTypeMeaning is supplied | Lookup | standardLookupsLOV (`INV_ITEM_TXN_DEFAULTS_TYPE`) | resolve_default_type_meaning | The Redwood UI renders standard-lookup Meaning values and sends DefaultTypeMeaning in its staged payload | Supply an exact LookupCode in DefaultType or Meaning in DefaultTypeMeaning | DefaultTypeMeaning |
| item_transaction_defaults_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares an import | Satisfied | Live metadata query for Item Transaction Defaults |  | The registered business object is visible in the configured environment | Use Item Transaction Defaults for Data Loader preparation | Item Transaction Defaults |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A supplied code/display value resolved to one standard-lookup row and BO visibility is confirmed | Continue |
| Lookup | A supplied DefaultType or DefaultTypeMeaning must be resolved | Read-only only |
| Blocked | The standard lookup is unavailable, matches zero or many values, supplied values conflict, or BO metadata is unavailable | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITD.CHECK_READINESS | decision | 40 | resolve_dependency | ready->ITD.DATA_LOADER_HANDOFF;blocked->ITD.HANDLE_ERROR | ITD.RESOLVE_DEFAULT_TYPE_MEANING | stop | After Default Type standard-lookup resolution |
