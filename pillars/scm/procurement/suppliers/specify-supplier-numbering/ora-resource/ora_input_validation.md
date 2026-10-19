# Specify Supplier Numbering Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested next supplier number | NextSupplierNumber or bootstrap default | Block execution handoff | Provide the value through the generated Data Loader artifact, or retain the bootstrap default when no replacement is requested | Every create or update request |  |
| Rollback acknowledgement | Explicit rollback approval | Block execution handoff | Confirm that a value at or below the current maximum is intentional and has been checked for existing supplier-number use | Requested number is at or below the current maximum |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A current Supplier Numbering row is found | Continue only when exactly one row is returned | Retain SupplierNumberingId and NextSupplierNumber for preview | find_supplier_numbering_row |
| No Supplier Numbering row is found | Stop the update branch | Use the approved execution workflow to establish the row, then re-read it | find_supplier_numbering_row |
| More than one matching row is found | Block | Resolve the duplicate configuration before any execution workflow begins | find_supplier_numbering_row |

## Data Loader Artifact Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Workbook mapping | Require the generated sample's registered fields and key-field mapping | Before any Data Loader handoff |  |
| Row identity | Reject a missing, ambiguous, or unreadable SupplierNumberingId | A row is resolved for an update | find_supplier_numbering_row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.VALIDATE_INPUT | step | 10 | validate_input | valid->SN.READ_CURRENT;invalid->SN.HANDLE_ERROR | none | stop | Before any lookup or execution handoff |
