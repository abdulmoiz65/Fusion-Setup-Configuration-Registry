# Costing of Elements Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Lookup page sizes | Element search 1000; LDG discovery 25. Other resolvers own their captured page sizes. | Shared Search | No user override defined. | |
| page_offset | 0 for a new request; resolver advances subsequent pages. | Collection lookup | Preserve bound continuation only. | |
| Optional filters | Omit when absent. | Search | Never discard a supplied filter or use a captured date/name. | |
| COST/BAL Proportion | 1 (100 percent). | Each supplied Cost Account or Offset Account | Reject a conflicting supplied proportion; do not ask for one when absent. | |
| OVRRIDE Proportion | Supplied fraction unchanged; explicit percentage divided by 100 once, with decimal arithmetic. | Priority Cost Accounts | No invented default. REST baseline normalization is owned by the detail resolver. | |
| SubTypeSequence | Start at 1 within each parent/effective-date/SourceSubType group; increase consecutively for that group's account rows. | New Create/Update account snapshot | Ignore supplied sequence; preserve explicit priority row order. COST and BAL each have their own sequence 1. Never number unrelated subtypes as one group. | |
| Create EffectiveEndDate | 4712/12/31 when omitted. | New allocation and new EL/LIV records | Preserve an explicit valid end. Never apply this default to Update/Correct/End Date/Zap. | |
| ReplaceLastEffectiveEndDate | Y as a METADATA attribute and matching MERGE value. | Every rendered End Date row: CostAllocationV3 EL and CostInfoV3 EL/LIV | No; the requested end date itself has no default. | |
| Account EffectiveDate | Requested Create or Update start. | New account snapshot | A conflicting explicit date fails validation. | |
| CostedFlag | Y for an input explicitly requested as costed. | New or explicitly enabled LIV selection | Preserve explicit disabled/N intent; omission in Update/Correct preserves baseline. | |
| Unspecified optional segments | Absent for new COST/BAL; preserved on Update. | Partial accounts | Never fill zeros or full-account defaults. | |
| Effective-dated maintenance | SET PURGE_FUTURE_CHANGES N at the start of each Update/Correct DAT. | Update/Correct | Required; no automatic purge. | |

These sequence groups follow Oracle's element-costing account identity examples;
COST and BAL each use sequence 1. The fixed proportions and priority-account
rules come from the developer's Create contract, not the captured account values.
Zap bypasses COE.HDL.APPLY_DEFAULTS: its DELETE dates and identities come from
complete history/detail, and it emits no account values, flags or sequences.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COE.SEARCH.APPLY_DEFAULTS | decision | 3 | apply_default | applied->COE.SEARCH.CHECK_DEPENDENCIES;invalid->COE.HDL.HANDLE_ERROR | COE.SEARCH.VALIDATE_INPUT | stop | Apply only Search pagination/filter defaults. |
| COE.HDL.APPLY_DEFAULTS | decision | 20 | apply_default | applied->COE.HDL.CHECK_DEPENDENCIES;skipped->COE.HDL.CHECK_DEPENDENCIES;invalid->COE.HDL.HANDLE_ERROR | COE.HDL.VALIDATE_VALUES | stop | Apply conditional defaults to requested Create/Update rows, Correct changes or End Date special attribute; do not overwrite baseline values or infer an End Date date. |
