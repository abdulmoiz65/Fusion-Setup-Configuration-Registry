# Specify Supplier Numbering Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Row discovery | Resolve the Supplier Numbering row or establish that it is absent |
| 2 | Data Loader handoff | When the row is absent, use the approved `supplierNumberingInitializeSetup` Data Loader POST artifact; otherwise prepare the Data Loader update from the resolved row |
| 3 | Number safety | Validate the requested number and require explicit approval for a rollback at or below the current maximum |
| 4 | Verification | Re-read the row after the approved Data Loader workflow completes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Missing row | Error | find_supplier_numbering_row | The approved `supplierNumberingInitializeSetup` Data Loader POST artifact is not selected before the request continues | Submit the approved artifact once, re-read, and then validate readiness | Yes |
| Existing row | Error | find_supplier_numbering_row | The resolved row is ambiguous or has no SupplierNumberingId | Resolve the row identity before the Data Loader handoff | Yes |
| Requested number is at or below NextSupplierNumber | Error | find_supplier_numbering_row | No explicit rollback approval and evidence that the requested value is unused | Treat as a rollback; confirm business approval and collision evidence before the Data Loader handoff | Yes |
| Any mutation | Error |  | The mutation bypasses the approved Data Loader workflow | Stop and use the approved workflow; do not describe or substitute an execution route here | Yes |
| Data Loader handoff | Error | find_supplier_numbering_row | The handoff lacks the exact resolved SupplierNumberingId and current NextSupplierNumber | Refresh the read-only lookup and rebuild the handoff | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_supplier_numbering_row | Before Data Loader handoff and verification | SupplierNumberingId and NextSupplierNumber | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.ENFORCE_EXISTING | decision | 60 | design_enforcement | passed->SN.UPDATE_EXISTING_GATE;blocked->SN.HANDLE_ERROR | SN.READ_CURRENT,SN.CHECK_DEPENDENCY_READINESS | stop | An existing Supplier Numbering row is available |
| SN.ENFORCE_CREATE | decision | 61 | design_enforcement | passed->SN.APPLY_INITIAL_DEFAULT;blocked->SN.HANDLE_ERROR | SN.READ_CURRENT,SN.CHECK_DEPENDENCY_READINESS | stop | No Supplier Numbering row is available |
