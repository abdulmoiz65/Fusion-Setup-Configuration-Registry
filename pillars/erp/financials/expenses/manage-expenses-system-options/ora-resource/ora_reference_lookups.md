# Manage Expenses System Options Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_expenses_option_edit_baseline | A confirmed FSM option-edit package is prepared | The validated intake result and the exact four-member completed FSM export named by its target environment, export job ProcessId, and CSV digests | Match task code EXM_MANAGE_EXPENSES_SYSTEM_OPTIONS, target environment, and each normalized BuName plus OptionCode exactly; require one row in each option CSV. Match metadata ProcessId to the export job ID, or bind the observed `-999` placeholder through the unchanged exporter ZIP filename and member bytes | Baseline identity, source workbook digest, archive and CSV digests, selected rows, original ValueCode, and requested ValueCode | Stop package preparation and re-export or correct the workbook; never select a first or similarly named row |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The task is a confirmed FSM option edit | Resolve the baseline from the locally persisted validation result and fresh exported package; no Fusion REST lookup is selected by this contract |
| The request needs a dynamic reference, inheritance representation, an unconfirmed code, or a Create operation | Return unsupported_by_confirmed_fsm_contract with the exact field and missing evidence; do not generate a package |
