# Position Costing Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Position search costing filter | all | Candidate discovery or exact source resolution, including Create. | No; preserve an explicit supported filter, but never use with_costing to prove Position absence for Create. | search_position_costing_by_criteria |
| Active costing search | with_costing and active_only=true | User explicitly requests active costing records. | No; report conflicting intent instead of conflating Active with costing presence. | search_active_position_costing_records |
| Search/as-of effective date | Today's calendar date in the active session, resolved at request time | Position search and date-specific reads when no date is supplied. | No; an explicit user date takes precedence. Normalize once to ISO for GET and YYYY/MM/DD when an HDL operation needs that same date. Never inherit a HAR date. This default does not supply a requested mutation end date or replace the explicit allocation interval date required for End Date. | |
| LegislativeDataGroupName | Canonical confirmed name | LDG-scoped detail or HDL. | No; derive from selected LDG, not blank fields on an uncosted Position. | confirm_legislative_data_group |
| PositionCode | Exact returned business code, retained internally | A Position is selected by its user-facing PositionName or a returned candidate. | No; resolve uniquely from the selected Position and check any code the user volunteered for agreement. Never prompt for or display PositionCode as a search choice. | resolve_position_source |
| SourceType | POS | Every Position Costing parent or account row. | No | |
| SourceSubType | COST | Every account row. | Yes; override any supplied value with COST. | |
| Parent EffectiveEndDate | 4712/12/31 | Create and ordinary effective Update parent rows. | Yes, only with a template-validated explicit value. | |
| ReplaceLastEffectiveEndDate | Y | End Date of the exact last effective parent. | No | |
| BusinessUnitName | none | Every HDL operation and every parent or account row it renders. | No; use only the final name sealed by resolve_position_business_unit through its Position-bound ID and name-resolution stages. Caller names never replace this evidence. | resolve_position_business_unit |
| SubTypeSequence | Consecutive positive integers starting at 1. | Create and effective-dated Update CostAllocationAccountV3 account collections. | No; ignore a user-supplied value, assign 1 to the first supplied account row, and increase by 1 for each following row. | |
| Proportion | user percentage divided by 100 | Create and effective-dated Update account rows. | No; convert once with decimal arithmetic. | |
| Correct SubTypeSequence | none | Correct MERGE_EXISTING or MERGE_NEW. | No; use the positive REST-resolved value when available or ask the user for the exact positive HDL value on the child action. Never infer or hardcode it. | resolve_correct_sub_type_sequence |
| Account segment clear value | none | Create, Update, Correct, and physical DELETE account segments. | No; reject #NULL for every listed operation. Correct also rejects blank and null target clear intent until a current template-validated HDL clear contract is documented. | |
| Future changes | SET PURGE_FUTURE_CHANGES N | Every Update parent DAT member. | No; render the directive before METADATA. | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCP.APPLY_DEFAULTS | decision | 40 | apply_default | applied->PCP.ENFORCE_DESIGN;skipped->PCP.ENFORCE_DESIGN;invalid->PCP.HANDLE_ERROR | PCP.CHECK_DEPENDENCIES | stop | Validate discovery defaults already used during input/search; apply HDL defaults only to mutation preparation. Query never acquires HDL-only dependencies. |
