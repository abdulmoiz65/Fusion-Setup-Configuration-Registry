# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplier numbering row | Read the collection and find exactly one row, or establish that it is absent |
| 2 | Initialization | When absent, prepare the approved `supplierNumberingInitializeSetup` Data Loader POST artifact, submit it once, then re-read the collection |
| 3 | Backend identifier | Retain SupplierNumberingId for update and verification |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SN-ROW | Supplier Numbering row | Yes | Every request | Lookup | supplierNumbering collection | find_supplier_numbering_row | Determines initialization versus update | Do not provide a row ID manually | SupplierNumberingId, NextSupplierNumber |
| SN-INITIALIZE | Initialization outcome | Yes | The row is absent | Verify | Approved `supplierNumberingInitializeSetup` Data Loader POST result and re-read | find_supplier_numbering_row | Establishes the initial setup row before an update | Accept only a successful initialization followed by exactly one row; otherwise stop | SupplierNumberingId, NextSupplierNumber |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.CHECK_DEPENDENCY_READINESS | decision | 30 | resolve_dependency | existing_ready->SN.ENFORCE_EXISTING;missing_ready->SN.ENFORCE_CREATE;blocked->SN.HANDLE_ERROR | SN.READ_CURRENT | stop | After the row lookup, before selecting the existing-row or missing-row branch |
