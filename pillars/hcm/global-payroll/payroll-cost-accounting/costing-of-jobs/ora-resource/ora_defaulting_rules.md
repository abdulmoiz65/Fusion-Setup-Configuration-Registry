# Job Costing Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SourceType | JOB | Every CostAllocationV3 and CostAllocationAccountV3 row. | No | |
| SourceSubType | COST | Create account rows; effective-dated Update retains its existing COST default. | Create: no; apply COST only when omitted, accept explicit COST, and reject any other explicit value. Update: preserve the existing COST enforcement. Correct child DELETE and Zap retain the subtype from sealed physical-account evidence. | |
| Parent EffectiveEndDate | 4712/12/31 | Create parent row; render this nonblank value in the final CostAllocationV3.dat MERGE column before archive validation. | No | |
| End Date flag | ReplaceLastEffectiveEndDate=Y | End Date parent row after component-support validation. | No | |
| Future changes | SET PURGE_FUTURE_CHANGES N | Update in both CostAllocationV3.dat and CostAllocationAccountV3.dat. | No | |
| SubTypeSequence | Consecutive positive integers starting at 1. | Create and effective-dated Update CostAllocationAccountV3 account collections. | No; ignore a user-supplied value, assign 1 to the first supplied account row, and increase by 1 for each following row. | |
| Correct MERGE SubTypeSequence | No default. | Existing-child or new-child Correct MERGE. | No; use the positive REST-resolved value when available or ask the user for the exact positive HDL value on the child action. Never infer it. | resolve_job_correct_sequence |
| Correct child DELETE SubTypeSequence | No default and no rendered field. | One sealed non-orphaning Correct child DELETE. | No; retain physical identity, SourceSubType, and Proportion from bound current-state detail evidence only. | query_job_costing_history_accounts |
| Proportion | User percentage divided by 100, as a decimal fraction from 0 through 1. | Create and effective-dated Update account rows. | No; convert once with decimal arithmetic. | |
| HDL segment attribute | For each runtime-declared `SEGMENTn` physical column, use the corresponding case-sensitive `Segment<N>` HDL name after validating the numeric index and current account template. | Create, Update, or Correct MERGE account rows. | No; derive N separately for every runtime segment and never guess or uppercase the HDL spelling. | |
| Segment clear | No default. | A request presents #NULL, JSON null, or an empty value as an existing-segment clear. | No; block until an official explicit-clear HDL contract is documented. | |
| DAT member names | CostAllocationV3.dat and CostAllocationAccountV3.dat | Create or Update. | No | |
| Correct DAT member | CostAllocationAccountV3.dat only | Correct. | No; one physical-account action per archive. | |
| End Date DAT member | CostAllocationV3.dat only | End Date. | No | |
| Zap DAT members | CostAllocationV3.dat plus CostAllocationAccountV3.dat when the resolved logical parent has children; parent-only only with explicit no-child proof. | Zap (Delete Record And History). | No; retain each resolved physical account ID, allocation-record ID, effective date, and current proportion. Do not manufacture SubTypeSequence. | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JCP.APPLY_DEFAULTS | decision | 40 | apply_default | applied->JCP.ENFORCE_DESIGN;skipped->JCP.ENFORCE_DESIGN;invalid->JCP.HANDLE_ERROR | JCP.CHECK_DEPENDENCIES | stop | Apply official HDL defaults before package preview. |
