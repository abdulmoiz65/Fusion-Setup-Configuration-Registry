# Values Defined by Criteria HDL Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm target contract | Use current target metadata for every component header and technical calculation value field. |
| 2 | Confirm reference setup | Verify LDG, group, database item, value set, and calculation references in the target environment. |
| 3 | Enforce hierarchy design | Create root before children, prioritize criteria deliberately, and prevent cycles. |
| 4 | Enforce default and leaf completeness | Provide a tested fallback unless accepted otherwise; give every executable leaf a compatible CalculationValues payload. |
| 5 | Gate deployment | Validate in nonproduction and resolve all diagnostics before production approval through core.data-loader. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any target header or calculation payload field is selected | Blocker | verify_values_defined_by_criteria_metadata | Current target metadata does not confirm the header order, technical code, or CalculationValues mapping | Export target attributes and use only confirmed fields | Yes |
| A root, criterion, or value is prepared | Blocker | resolve_legislative_data_group | The name or code is not unique within the LDG or a linked artifact is outside that LDG | Correct the LDG-scoped identity and references | Yes |
| A criterion uses a database item, value set, operand, or literal | Blocker | verify_database_item_and_criterion_contract | The setup is absent, unsupported by the consuming context, or literal semantics conflict with the criterion | Correct the reference or criterion design before loading | Yes |
| A hierarchy is prepared | Blocker | verify_hierarchy_design | Parent links are invalid, a cycle exists, sequence does not match priority, or the fallback is untested | Reorder and test representative conditions; include a default unless formally accepted otherwise | Yes |
| A leaf calculation is prepared | Blocker | verify_calculation_value_contract | ValueDetails lacks a compatible CalculationValues payload or selected UOM, currency, periodicity, identifier, or reference | Complete the target-confirmed leaf design | Yes |
| Production import is requested | Blocker | verify_values_defined_by_criteria_metadata | Nonproduction validation, diagnostics resolution, immutable artifact reference, target environment, or current approval is absent | Complete validation and use core.data-loader approval workflow | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_values_defined_by_criteria_metadata | Before selecting headers, technical codes, or calculation payload fields | Target export and confirmed component contract | ora_reference_lookups.md |
| resolve_legislative_data_group | Before accepting LDG-scoped identity | Exact LDG name and confirmed target identity | ora_reference_lookups.md |
| verify_database_item_and_criterion_contract | Before criterion or literal acceptance | Database item, value set, operand, literal compatibility, and context | ora_reference_lookups.md |
| verify_hierarchy_design | Before artifact submission | Parent and root links, sequence, fallback, and tests | ora_reference_lookups.md |
| verify_calculation_value_contract | Before leaf acceptance | Calculation type, payload mapping, UOM, currency, periodicity, and references | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.DESIGN_GATE | decision | 50 | design_enforcement | compliant->VALUE_BY_CRITERIA.EXECUTION_GATE;blocked->VALUE_BY_CRITERIA.HANDLE_DESIGN_BLOCKER | VALUE_BY_CRITERIA.APPLY_DEFAULTS | stop | Enforce the target-specific HDL contract, LDG-scoped hierarchy integrity, fallback behavior, and complete leaf payloads. |
