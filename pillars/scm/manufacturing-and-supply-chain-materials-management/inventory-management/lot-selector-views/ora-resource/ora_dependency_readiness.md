# Lot Selector Views Dependency Readiness

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| LSV.DATA_LOADER_METADATA | inventorySearchViews REST Data Loader business object | Yes | Before every Data Loader handoff | Verify | Per-run Core Data Loader metadata preflight against the selected environment |  | External BO registration is user-provided provenance only; successful prior metadata is not reusable runtime readiness. | Run a fresh metadata preflight for inventorySearchViews; stop if it is unavailable, unregistered, or incompatible. | Selected environment; inventorySearchViews discriminator; resolved template and schema |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The current selected environment exposes compatible inventorySearchViews Data Loader metadata. | Yes, read-only metadata only. |
| Blocked | Metadata preflight fails, is unavailable, or does not expose the selected BO. | No; do not fall back to direct REST execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSV.CHECK_METADATA | decision | 50 | resolve_dependency | ready->LSV.DATA_LOADER_HANDOFF;blocked->LSV.HANDLE_ERROR | LSV.RESOLVE_TASK_FLOW | stop | Before handing normalized data to core.data-loader. |
