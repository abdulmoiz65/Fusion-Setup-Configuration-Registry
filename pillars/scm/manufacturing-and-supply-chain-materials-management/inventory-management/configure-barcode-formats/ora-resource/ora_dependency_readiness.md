# Configure Barcode Formats Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| User confirmation | External BO registration is complete for inventoryBarcodeFormats |
| Per-run Data Loader metadata preflight | Verifies that inventoryBarcodeFormats is visible in the selected environment; the result is runtime evidence, not reusable readiness evidence |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader business object metadata | Complete a read-only per-run metadata preflight for inventoryBarcodeFormats in the selected environment before Data Loader preparation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| inventory_barcode_formats_bo | Data Loader business object metadata | Yes | Before core.data-loader prepares a request containing Configure Barcode Formats | Required per run | Read-only Data Loader metadata preflight for inventoryBarcodeFormats in the selected environment |  | BO visibility can vary by environment and over time | Verify inventoryBarcodeFormats and record the sanitized result in the task validation artifact and skill-run record | inventoryBarcodeFormats |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BCF.CHECK_READINESS | decision | 20 | resolve_dependency | ready->BCF.APPLY_DEFAULTS;blocked->BCF.HANDLE_ERROR | BCF.NORMALIZE_BOOLEAN_FIELDS | stop | After DateFormat and route-aware switch/status normalization, perform the current run's read-only Data Loader metadata preflight for inventoryBarcodeFormats before defaulting, lookup resolution, or Data Loader handoff |
