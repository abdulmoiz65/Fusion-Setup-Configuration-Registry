# Values Defined by Criteria HDL Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| HDL route and object scope | ValuesDefinedByCriteria, Criteria, LiteralValuesForCriteria, ValueDetails, and calculation-type-specific CalculationValues components; METADATA headers and MERGE records | Block preparation | Use HCM Data Loader and the current target object export; do not substitute a REST create or update route | Every request | verify_values_defined_by_criteria_metadata |
| Target effective context | LegislativeDataGroupName, effective start date, and target environment | Block preparation | Supply the target LDG and an effective date in the target HDL format | Every component row | resolve_legislative_data_group |
| Root identity | ValuesDefinedByCriteriaCode, name, LDG, ValueDefinitionGroupCode, retrieval date type, calculation type, and PeriodOrUnit | Block preparation | Supply unique LDG-scoped root identity and validate the technical attributes against target metadata | Every root row | verify_values_defined_by_criteria_metadata |
| Criterion definition | CriteriaCode, sequence, operand, database item, LDG, group, and default designation when applicable | Block preparation | Supply a valid hierarchy design; use no literal for a default criterion | Every Criteria row | verify_database_item_and_criterion_contract |
| Literal condition | Criterion code, literal value, effective dates, and datatype-compatible operand | Block preparation | Supply literal rows only for non-default criteria; provide one or more literals only when the operand design supports them | A non-default criterion uses literal comparison | verify_database_item_and_criterion_contract |
| Leaf calculation value | ValueCode, criterion link, calculation type, UOM or currency, periodicity, and ValueIdentifier when multiple values share a criterion | Block preparation | Supply a unique leaf design compatible with the root and criterion | Every ValueDetails row | verify_calculation_value_contract |
| Calculation payload | CalculationValues row with the selected calculation-type-specific field | Block preparation | Export current target metadata and provide the exact payload field and value for every leaf | Every executable calculation leaf | verify_calculation_value_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The LDG, group, hierarchy, root, criteria, leaves, and calculation payload are supplied | Continue | Resolve target metadata and referenced setup before constructing the HDL hierarchy | verify_values_defined_by_criteria_metadata |
| A default criterion has a literal, a non-default criterion lacks its required literal design, or hierarchy links are cyclic or out of order | Blocked | Correct the tree and component ordering before preparing the file | verify_database_item_and_criterion_contract |
| A leaf lacks CalculationValues or its calculation type, UOM, currency, periodicity, or identifier is incompatible | Blocked | Obtain target metadata and complete the leaf payload design | verify_calculation_value_contract |
| The target metadata export does not confirm a selected header or calculation payload field | Blocked | Stop; export View Business Objects attributes for the target release | verify_values_defined_by_criteria_metadata |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| HDL structure | Require target-exported METADATA header order and MERGE rows; parent rows precede dependent component rows | Every data file | verify_values_defined_by_criteria_metadata |
| LDG and uniqueness | Require root, criterion, and value names or codes to be unique within the target LDG | Every hierarchy | resolve_legislative_data_group |
| Retrieval date type | Accept effective date or date earned only when confirmed by target metadata; effective date is the documented default | Every root or criterion that specifies retrieval date | verify_values_defined_by_criteria_metadata |
| Criterion semantics | Require supported operand semantics, numeric sequence priority, datatype-compatible literals, and no literal for a default criterion | Every Criteria and LiteralValuesForCriteria row | verify_database_item_and_criterion_contract |
| Value identifiers | Require distinct ValueIdentifier values when multiple values exist for one criterion | Multiple ValueDetails rows share a criterion | verify_calculation_value_contract |
| Calculation compatibility | Require UOM, currency, periodicity, PeriodOrUnit, calculation type, and CalculationValues field to match the target contract | Every leaf calculation | verify_calculation_value_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.VALIDATE_INPUT | decision | 10 | validate_input | valid->VALUE_BY_CRITERIA.RESOLVE_DEPENDENCIES;invalid->VALUE_BY_CRITERIA.HANDLE_INPUT_ERROR | none | stop | Validate Values Defined by Criteria HDL inputs without inferring headers, codes, or calculation payloads. |
