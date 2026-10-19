# Legal Reporting Unit Calculation Cards Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| Task-specific CSV export package | Exported Legal Reporting Unit Calculation Cards data from the approved task flow | Validate package identity and preserve task scope |
| Task-specific CSV import package | Rows matching the approved task-specific CSV contract | Validate required columns and block execution until the import contract is confirmed |
| Tabular planning sheet | Tax reporting unit, card/component business names, field/value, effective date, and desired outcome | Resolve existence and technical keys per business row before operation classification; never require IDs in the sheet |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Task identity | Task code and task name | Must match PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS and Legal Reporting Unit Calculation Cards |
| Owner reference | sourceType, sourceId, tax reporting unit display name | sourceType must be TRU and sourceId must match the selected Legal Reporting Unit card scope |
| Card reference | card display/base name and effective date | Resolve `dirCardId`, definition ID, LDG ID, sequence, and history internally; use mode=ADD only after complete no-match discovery |
| Component reference | component business/base name and effective date | Resolve sequence, component/definition IDs, and override groups internally through card drilldown/component lookup |
| Override rows | context, name, value | context/name must match getCardDetails override metadata and value must resolve through the mapped LOV |
| Action fields | review, create, update, correct, end-date, delete, export, or import intent | Treat create/update/correct as provisional. Classify each object from complete target history; existing rows require Update/Correction confirmation and absent leaves become create |
| HDL row fields | CalculationCard, CardComponent, ComponentDetail, CalculationValueDefinition, EnterableCalculationValue, and target-supported action/keys | Populate only sections and attributes confirmed by the live target template and component guidance |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Source contract | Live target `CalculationCard` HDL template and the applicable component guidance must exist; any separate CSV/FSM route needs its own approved contract |
| Read and HDL validation | sourceType=TRU, effective-date format, exact card/component state, readOnlyFlag, HDL action, parent keys, and LOV values must pass before DAT preview |
| Existence classification | Resolve card, component, override/FLEX/value, assignment/association, and related business keys per row across current/future/history. Do not infer absence from a failed or single-date lookup |
| Existing-data decision | Group rows only when they share the same effective-date semantics; disclose each existing business row/interval and obtain Update/Correction confirmation before preview |
| Row validation | Required columns, lookup outputs, and unresolved references must be shown |
| Preview | Show create/update/correction counts, blocked rows, business targets, effective intervals, confirmed decisions, exact HDL rows, and unresolved fields; keep technical IDs internal |
| DAT preview | Show the complete proposed `METADATA` and operation lines in chat; do not write a file during this gate |
| Live execution | Route only the approved HDL archive through `core.data-loader`; never call a direct calculation-card REST mutation |
