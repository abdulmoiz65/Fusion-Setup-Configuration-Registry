# Interorganization Parameters Input Validation

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Transfer Order Required normalization | Accept Yes, Y, or True in any letter case and normalize to boolean true for REST Data Loader handoff or string Y for FSM handoff; accept No, N, or False in any letter case and normalize to boolean false for REST Data Loader handoff or string N for FSM handoff; preserve a blank value; reject every other representation | Input is supplied under Transfer Order Required, TransferOrderRequired, or TransferOrderRequiredFlag |  |
| Receipt Required normalization | Accept Yes, Y, or True in any letter case and normalize to boolean true for REST Data Loader handoff or string Y for FSM handoff; accept No, N, or False in any letter case and normalize to boolean false for REST Data Loader handoff or string N for FSM handoff; preserve a blank value; reject every other representation | Input is supplied under Receipt Required, ManualReceiptExpense, or ManualReceiptExpenseFlag |  |
| Boolean route selection | Select flag serialization only from the workflow-selected import route; do not infer a route from user input | Before normalizing either selected flag |  |
| Transfer Type representation | Accept a supplied LookupCode or Meaning only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode for Data Loader handoff | A Transfer Type value is supplied | resolve_interorg_transfer_type |
| Inventory Receipt Routing representation | Accept a supplied LookupCode or Meaning only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode for Data Loader handoff | An inventory Receipt Routing value is supplied | resolve_interorg_inventory_receipt_routing |
| Inventory Cancel Backorders representation | Accept a supplied LookupCode or Meaning only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode for Data Loader handoff | An inventory Cancel Backorders value is supplied | resolve_interorg_inventory_cancel_backorders |
| Expense Receipt Routing representation | Accept a supplied LookupCode or Meaning only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode for Data Loader handoff | An expense Receipt Routing value is supplied | resolve_interorg_expense_receipt_routing |
| Expense Cancel Backorders representation | Accept a supplied LookupCode or Meaning only after it resolves to exactly one returned lookup row; normalize the resolved value to LookupCode for Data Loader handoff | An expense Cancel Backorders value is supplied | resolve_interorg_expense_cancel_backorders |
| Conflicting lookup representations | When a code and meaning are both supplied, require both representations to resolve to the same lookup row | Both representations are supplied for a selected lookup field |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IOP.VALIDATE_INPUT | step | 10 | validate_input | valid->IOP.CHECK_READINESS;invalid->IOP.HANDLE_ERROR | none | stop | Before read-only lookup resolution or Data Loader preparation |
