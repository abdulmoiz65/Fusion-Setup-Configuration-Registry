# Specify Supplier Numbering Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_supplier_numbering_row | Before a Data Loader handoff and after initialization or update verification | None | /fscmRestApi/resources/11.13.18.05/supplierNumbering | No fields projection; use full response | Exactly one returned setup row | SupplierNumberingId, NextSupplierNumber | Zero rows require the approved `supplierNumberingInitializeSetup` Data Loader POST artifact; multiple rows block; no row may be selected by guesswork |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A live read is needed | Use a read-only collection or item request before and after the approved Data Loader workflow completes |
| A row is returned | Retain only the returned SupplierNumberingId and NextSupplierNumber |
| Bootstrap returns SUCCESS or ROW EXISTS | Run the same lookup again and require exactly one row before treating the request as ready |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.READ_CURRENT | decision | 20 | reference_lookup | found->SN.CHECK_DEPENDENCY_READINESS;missing->SN.CHECK_DEPENDENCY_READINESS;failure->SN.HANDLE_ERROR | SN.VALIDATE_INPUT | stop | Before create or update |
