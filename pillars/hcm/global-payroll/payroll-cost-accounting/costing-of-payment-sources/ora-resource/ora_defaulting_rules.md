# Costing of Payment Sources HDL Defaulting Rules

Apply the Create end-date default and account-role defaults below directly.
The account defaults apply to Create/Update Liability, Cash Clearing or Cash
rows and require no Fusion lookup. Zap skips HDL defaults entirely: DELETE
identities and dates come from sealed read evidence, not creation defaults.
End Date applies only the special date-change flag; its start and end are never
defaulted from Create or Update.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Search Effective As Of Date | Use the explicit search date; otherwise the already requested operation EffectiveStartDate; otherwise the current session calendar date, disclosed with results | Search only. This is the caller's visible search-date policy, not an Oracle server default or an HDL write-date default | No | |
| Search costing state | all | Search when neither With Costing nor Without Costing restricts the results; both selected also means all | No | |
| EffectiveEndDate | 4712/12/31 | Create when EffectiveEndDate is omitted; apply automatically without user confirmation. Does not default Update, End Date or Zap dates | No | |
| Update EffectiveEndDate | The end date of the live interval selected by resolve_payment_source_update_state | Update when omitted; preserves the selected interval boundary rather than extending it | No; an explicit conflicting end date blocks under the Update date contract | resolve_payment_source_update_state |
| ReplaceLastEffectiveEndDate | Y | End Date CostInfoV3 and CostAllocationV3 MERGE rows only; render as a METADATA attribute and matching value, not a SET instruction | No; reject an explicit conflicting value. No date, account or checkbox defaults apply to End Date | |
| SourceSubType | LBLTY | Create/Update account role is Liability | No; fill when omitted, retain a matching explicit value, and reject a conflicting value without silently replacing it | |
| SourceSubType | CLRNG | Create/Update account role is Cash Clearing | No; fill when omitted, retain a matching explicit value, and reject a conflicting value without silently replacing it | |
| SourceSubType | CASH | Create/Update account role is Cash | No; fill when omitted, retain a matching explicit value, and reject a conflicting value without silently replacing it | |
| SubTypeSequence | Consecutive positive integers starting at 1. | Create and effective-dated Update CostAllocationAccountV3 account collections. | No; Create uses supplied account-row order. Update uses the complete baseline account order with deltas applied in place. Assign 1 through N to the new collection; ignore user sequence input and never claim these are REST-resolved existing-child sequences | |
| Proportion | 1 | Every Create/Update Liability, Cash Clearing or Cash account row; represents 100% for each row | No; fill when omitted and serialize an accepted numeric value equal to 1 as 1. Reject any other value; never divide by 100, distribute a total across account roles or silently replace a conflicting input | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPS.SEARCH.APPLY_DEFAULTS | decision | 2 | apply_default | applied->CPS.SEARCH.RESOLVE_LDG;unchanged->CPS.SEARCH.RESOLVE_LDG;invalid->CPS.HDL.HANDLE_ERROR | CPS.SEARCH.VALIDATE_INPUT | stop | Apply only the search date and costing-state defaults before search. Do not require or default any HDL field during Search |
| CPS.HDL.APPLY_DEFAULTS | decision | 15 | apply_default | applied->CPS.HDL.RESOLVE_KFF_LDG;skipped->CPS.HDL.RESOLVE_KFF_LDG;invalid->CPS.HDL.HANDLE_ERROR | CPS.UPDATE.VALIDATE_STATE | stop | Assign Standard Defaults after complete state validation and before Full Flexfield lookups. Create retains its date default; Update consumes its resolved end date and complete account order. Apply role, fixed Proportion and consecutive sequence defaults without user confirmation; reject conflicts |
| CPS.END_DATE.APPLY_DEFAULTS | decision | 23 | apply_default | applied->CPS.END_DATE.CHECK_DEPENDENCIES;unchanged->CPS.END_DATE.CHECK_DEPENDENCIES;invalid->CPS.HDL.HANDLE_ERROR | CPS.END_DATE.VALIDATE_STATE | stop | Apply ReplaceLastEffectiveEndDate=Y to both members of the same archive when a change is needed. Preserve S/F; CostInfoV3 carries the four observed flags, never defaults them. Skip account and Create/Update date defaults |
