# Values Defined by Criteria HDL Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_values_defined_by_criteria_metadata | Before HDL preparation, validation, or import | Configured target environment and Values Defined by Criteria business object | My Client Groups > Data Exchange > View Business Objects > Values Defined by Criteria > Attributes > Export | Component names, header order, available attributes, technical codes, and CalculationValues payload fields | Use the current target release export as authoritative; do not substitute concise public examples for target metadata | Confirmed component headers, supported attributes, and calculation payload contract | Stop preparation and report missing or inconsistent metadata; do not infer a header or payload field. |
| resolve_legislative_data_group | Before accepting the LDG | Exact LegislativeDataGroupName and configured target environment | Configured target LDG metadata or supported target LOV | LDG identity and LegislativeDataGroupName | Retain exactly one target record matching the supplied LDG name | Confirmed LDG identity and name | Stop on no match or ambiguity; do not select a substitute. |
| verify_value_definition_group | Before accepting a ValueDefinitionGroupCode | Supplied group code, LDG, and target environment | Target setup evidence or supported target export | Group code and LDG association | Require exactly one existing group compatible with the target LDG | Confirmed ValueDefinitionGroupCode and LDG association | Stop on no match or ambiguity; do not create a group through this task. |
| verify_database_item_and_criterion_contract | Before a criterion or literal row is accepted | Database item, value set, operand, literal value, LDG, and consuming context | Target setup evidence and Values Defined by Criteria metadata export | Database item, value set, supported criterion attributes, and literal compatibility evidence | Require the referenced setup to exist and the literal design to match the database-item context and criterion semantics | Confirmed database item, value set, operand, and literal design | Stop on missing, ambiguous, unsupported, or incompatible references. |
| verify_calculation_value_contract | Before a leaf calculation is accepted | ValueCode, calculation type, UOM, currency, periodicity, calculation payload, and related references | Target metadata export and target setup evidence | Supported CalculationValues field, calculation type code, UOM, currency, periodicity, and referenced object identity | Require the target export and setup evidence to support the selected leaf design exactly | Confirmed leaf calculation contract and payload mapping | Stop on missing, ambiguous, or unsupported payload mapping; do not infer a display label or field. |
| verify_hierarchy_design | Before an immutable HDL artifact is submitted | Prepared root, criteria, literal, leaf, and calculation rows | Prepared immutable HDL artifact and representative-condition test evidence | Parent and root links, sequence, default path, and leaf coverage | Require parent-before-child order, no cycle, priority order, and a tested fallback unless business owner accepted non-default behavior | Confirmed hierarchy design and test evidence | Stop and report the conflicting branch, sequence, or missing fallback. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A target attribute or CalculationValues field is selected | Use the target View Business Objects export; public HDL examples do not establish every target header or payload mapping. |
| A supplied display name needs a code | Resolve it only on one exact target match and retain the resolved evidence with the load package. |
| A valid unambiguous technical code is supplied | Use it without a duplicate lookup, while still validating target metadata where required. |
| A reference has no match or many matches | Stop preparation and report the supplied field and match result; never choose automatically. |
| An HDL diagnostic rejects a reference | Preserve the sanitized component, row, and attribute diagnostic; correct the source, regenerate the immutable artifact, and obtain new approval before retry. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.RESOLVE_REFERENCES | decision | 30 | reference_lookup | resolved->VALUE_BY_CRITERIA.APPLY_DEFAULTS;blocked->VALUE_BY_CRITERIA.HANDLE_LOOKUP_ERROR | VALUE_BY_CRITERIA.RESOLVE_DEPENDENCIES | stop | Resolve target metadata and every required LDG, setup, calculation, and hierarchy reference without inventing a REST contract. |
