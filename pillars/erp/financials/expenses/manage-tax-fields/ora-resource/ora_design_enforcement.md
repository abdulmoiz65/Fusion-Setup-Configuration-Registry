# Manage Tax Fields scope enforcement

Evidence: SRC-CS-TASK-BO, SRC-CS-TAX-SETUP-VO, SRC-CS-CASH-BO, SRC-CS-SETUP-FSM-AM, FSM-EXPORT.

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Setup option change | Error | | OptionCode is not ENABLE_TAX or BU scope is missing | Route unrelated options separately; no global negative-ID fallback | No automatic change |
| Cash-advance CSV carries data | Error | | EXM_CASH_ADV_SETUP_AND_POLICY.csv contains any data row | Keep its exact header only; put requested ENABLE_TAX changes solely in EXM_SETUP_OPTION.csv under the single-member contract | Header-only serialization; never delete the member |
| Rename, delete or clear requested | Error | | Rename, delete and blank-as-clear are unsupported by this contract | Obtain exact operation evidence rather than treating omission as deletion | No automatic conversion |
| Any live operation | Error | | Incomplete field/resolver contracts or missing immutable preview/loader approval | Complete active runbook and core.data-loader gates | No bypass |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAX.DESIGN | step | 5 | design_enforcement | success->TAX.EXECUTION;failure->TAX.ISSUES | TAX.DEFAULTS | stop | create or update |
