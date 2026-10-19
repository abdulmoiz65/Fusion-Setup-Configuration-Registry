# Landed Cost Charges Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve primary values | Resolve all required primary LOV values before preparing the create request. |
| 2 | Apply conditional UOM rule | Send ChargeBasisUOMCode only for PER_UNIT. |
| 3 | Preserve primary independence | Do not require optional children to create a primary charge; when selected, serialize them after the primary section. |
| 4 | Route mutation | Use the task's approved Data Loader route for the parent-first archive, including selected supported child rows. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Preparing a primary charge | Error | resolve_procurement_bu_set | The Procurement BU Set is unresolved or ambiguous. | Stop before preview and resolve the exact selected value. | Yes |
| Preparing a primary charge | Error | resolve_charge_currency | The charge currency is unresolved or ambiguous. | Stop before preview and resolve the exact selected value. | Yes |
| Preparing a primary charge | Error | resolve_currency_conversion_type | The currency conversion type is unresolved or ambiguous. | Stop before preview and resolve the exact selected value. | Yes |
| Preparing a primary charge | Error | resolve_charge_basis | The charge basis is unresolved or ambiguous. | Stop before preview and resolve the exact selected value. | Yes |
| Preparing a primary charge | Error | resolve_allocation_basis | The allocation basis is unresolved or ambiguous. | Stop before preview and resolve the exact selected value. | Yes |
| Preparing a PER_UNIT charge | Error | resolve_charge_basis_uom | ChargeBasisUOMCode is omitted or sent for a non-PER_UNIT basis. | Include the UOM only for PER_UNIT. | Yes |
| Preparing an optional default reference type | Error | resolve_default_charge_reference_type | The selected child identity is unresolved or the primary creation has not succeeded. | Create the primary record independently; then use only the resolved selection. | Yes |
| Preparing an optional analysis association | Error | resolve_cost_analysis_group | The selected group is unresolved or the primary creation has not succeeded. | Create the primary record independently; then use only the resolved selection. | Yes |
| Preparing an optional analysis association | Error | resolve_cost_analysis_code | The selected code is unresolved or the primary creation has not succeeded. | Create the primary record independently; then use only the resolved selection. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_procurement_bu_set | Creating a primary charge | SetId | ora_reference_lookups.md |
| resolve_charge_currency | Creating a primary charge | EnteredCurrencyCode | ora_reference_lookups.md |
| resolve_currency_conversion_type | Creating a primary charge | CurrencyConversionType | ora_reference_lookups.md |
| resolve_charge_basis | Creating a primary charge | ChargeBasisCode | ora_reference_lookups.md |
| resolve_allocation_basis | Creating a primary charge | DefaultAllocBasisCode | ora_reference_lookups.md |
| resolve_charge_basis_uom | ChargeBasisCode is PER_UNIT | ChargeBasisUOMCode | ora_reference_lookups.md |
| resolve_default_charge_reference_type | A default reference type is selected | ChargeReferenceTypeId | ora_reference_lookups.md |
| resolve_cost_analysis_group | An analysis association is selected | AnalysisGroupId | ora_reference_lookups.md |
| resolve_cost_analysis_code | An analysis association is selected | AnalysisCodeId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCC.ENFORCE_PRIMARY_FIRST | step | 110 | design_enforcement | compliant->LCC.DONE_PRIMARY_READY;blocked->RETURN_ISSUES | LCC.CHECK_OPTIONAL_CHILDREN | stop | A primary charge request is ready for routed execution. |
| LCC.ENFORCE_PRIMARY_FIRST_NO_ALLOCATION_UOM | step | 105 | design_enforcement | compliant->LCC.DONE_PRIMARY_READY_NO_ALLOCATION_UOM;blocked->RETURN_ISSUES | LCC.CHECK_OPTIONAL_NO_ALLOCATION_UOM | stop | A primary charge request without an applicable allocation UOM is ready for routed execution. |
