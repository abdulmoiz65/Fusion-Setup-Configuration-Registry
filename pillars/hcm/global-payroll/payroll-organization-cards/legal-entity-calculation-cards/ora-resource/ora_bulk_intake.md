# Legal Entity Calculation Cards Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| Task-specific CSV export package | Exported Legal Entity Calculation Cards data from the approved task flow | Validate package identity and preserve task scope |
| Task-specific CSV import package | Rows matching the approved task-specific CSV contract | Validate required columns and block execution until the import contract is confirmed |
| Plain-English component request | Target payroll statutory unit, LDG, card definition or existing card, effective date, component name, and requested source-equivalent overrides | Resolve names and source metadata, then produce a `CardComponent` plus `ComponentDetail` DAT preview. When the card is new, include one same-file parent `CalculationCard` MERGE row and do not require `dirCardId` |
| Source `getCardDetails` snapshot | Card, component, override, Flex context, and effective-date metadata from the explicitly selected source environment | Use as read-only mapping evidence; never carry source instance or definition IDs into target HDL |
| Tabular planning sheet | Payroll statutory unit, card/component business names, field/value, effective date, and desired outcome | Resolve existence and technical keys per business row before operation classification; never require IDs in the sheet |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Task identity | Task code and task name | Must match PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS and Legal Entity Calculation Cards |
| Owner reference | sourceType, sourceId, payrollStatUnitId, display name | sourceType must be PSU and sourceId must match the selected Legal Entity card scope |
| Card reference | card display/base name and effective date | Resolve `dirCardId`, definition ID, LDG ID, sequence, and history internally; use mode=ADD only after complete no-match discovery |
| Component reference | component business/base name and effective date | Resolve sequence, component/definition IDs, and override groups internally through card drilldown/component lookup |
| Override rows | context, name, value | context/name must match observed override metadata and value must resolve through the mapped LOV |
| HDL parent linkage | LegislativeDataGroupName, PayrollStatutoryUnitName, DirCardDefinitionName, CardSequence, ComponentSequence, target effective dates | Resolve against the target environment; keep target names and sequences consistent across `CardComponent` and `ComponentDetail` |
| HDL component row | DirCardCompDefName and optional target-resolved context keys | Use the component display name from target/source metadata; leave `DirCardCompDefId` empty unless Central requires and resolves a target ID |
| HDL component detail row | Parent component definition name, Flex-context code, `DirInformationCategory`, `FLEX:Deduction Developer DF`, and live-template Flex attributes | Set `DirCardCompDefName` to the exact value used by the parent `CardComponent`; never substitute the Flex-context display name. Repeat the context code in both context columns and place stored values in non-Display attributes |
| Action fields | review, create, update, correct, end-date, delete, export, or import intent | Treat create/update/correct as provisional. Classify each object from complete target history; existing rows require Update/Correction confirmation and absent leaves become create |
| HDL row fields | CalculationCard, CardComponent, ComponentDetail, CalculationValueDefinition, EnterableCalculationValue, and target-supported action/keys | Populate only sections and attributes confirmed by the live target template and component guidance |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Source contract | Live target `CalculationCard` HDL template and the applicable component guidance must exist; any separate CSV/FSM route needs its own approved contract |
| Read and HDL validation | sourceType=PSU, effective-date format, exact card/component state, readOnlyFlag, HDL action, parent keys, and LOV values must pass before DAT preview |
| Existence classification | Resolve card, component, override/FLEX/value, assignment/association, and related business keys per row across current/future/history. Do not infer absence from a failed or single-date lookup |
| Existing-data decision | Group rows only when they share the same effective-date semantics; disclose each existing business row/interval and obtain Update/Correction confirmation before preview |
| Row validation | Required columns, lookup outputs, and unresolved references must be shown |
| Preview | Show create/update/correction counts, blocked rows, business targets, effective intervals, confirmed decisions, exact HDL rows, and unresolved fields; keep technical IDs internal |
| DAT preview | Show the complete proposed `METADATA` and `MERGE` lines in chat; do not write a file during this gate |
| File creation | Requires explicit approval of the exact DAT preview; this approval does not authorize ZIP creation or upload |
| Live execution | Route only the approved HDL archive through `core.data-loader`; never call a direct calculation-card REST mutation |
