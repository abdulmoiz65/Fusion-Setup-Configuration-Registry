# Landed Cost Charges Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Procurement BU Set | Resolve one selected costing set to SetId. |
| 2 | Charge Currency and Conversion Type | Resolve one currency and one conversion type. |
| 3 | Charge and Allocation Basis | Resolve one charge basis and one allocation basis. |
| 4 | Conditional UOMs | Resolve a Charge Basis UOM only for PER_UNIT and an Allocation Basis UOM only when applicable. |
| 5 | Optional child selections | Resolve selected child values, then serialize their rows after the primary section in the same archive for a new charge. |
| 6 | Existing analysis association | Resolve the exact ChargeAnalysisCodeId before removing an existing association. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| procurement_bu_set | Procurement BU Set | Yes | Creating a primary charge | Lookup | Fusion costing sets LOV | resolve_procurement_bu_set | The create contract requires SetId. | Select exactly one Procurement BU Set. | SetId |
| charge_currency | Charge Currency | Yes | Creating a primary charge | Lookup | Fusion currencies LOV | resolve_charge_currency | The create contract requires EnteredCurrencyCode. | Select exactly one charge currency. | EnteredCurrencyCode |
| conversion_type | Currency Conversion Type | Yes | Creating a primary charge | Lookup | Fusion currency conversion types LOV | resolve_currency_conversion_type | The create contract requires CurrencyConversionType. | Select exactly one conversion type. | CurrencyConversionType |
| charge_basis | Charge Basis | Yes | Creating a primary charge | Lookup | Fusion standard lookups | resolve_charge_basis | The create contract requires ChargeBasisCode. | Select exactly one charge basis. | ChargeBasisCode |
| allocation_basis | Allocation Basis | Yes | Creating a primary charge | Lookup | Fusion standard lookups | resolve_allocation_basis | The create contract requires DefaultAllocBasisCode. | Select exactly one allocation basis. | DefaultAllocBasisCode |
| default_reference_type | Default Charge Reference Type | No | A user elects to add a default reference type | Lookup | Fusion landed cost reference types | resolve_default_charge_reference_type | The child association requires ChargeReferenceTypeId. | Select one applicable global or selected-set reference type. | ChargeReferenceTypeId |
| analysis_group | Cost Analysis Group | No | A user elects to add an analysis association | Lookup | Fusion cost analysis groups | resolve_cost_analysis_group | The child association requires a selected group. | Select a group before selecting its code. | AnalysisGroupId |
| analysis_code | Cost Analysis Code | No | A user elects to add an analysis association | Lookup | Fusion cost analysis group child codes | resolve_cost_analysis_code | The child association requires a code in the selected group. | Select one code in the selected group. | AnalysisCodeId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Required primary LOV values resolve uniquely and conditional UOM requirements are met. | Yes, read-only lookup only. |
| Blocked | A required primary LOV lookup has no match, multiple matches, or an unavailable response. | No |
| Ready | Optional child data is not supplied. | Yes, create only the primary charge through the approved route. |
| Blocked | A requested optional child selection does not resolve uniquely. | No, for that child association only. |
| Blocked | A requested analysis-association deletion lacks an exact ChargeAnalysisCodeId. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCC.CHECK_OPTIONAL_CHILDREN | decision | 100 | resolve_dependency | primary-only->LCC.ENFORCE_PRIMARY_FIRST;children-selected->LCC.ENFORCE_PRIMARY_FIRST;unresolved->RETURN_ISSUES | LCC.RESOLVE_ALLOCATION_UOM | stop | Primary LOV values are resolved. |
| LCC.CHECK_OPTIONAL_NO_ALLOCATION_UOM | decision | 90 | resolve_dependency | primary-only->LCC.ENFORCE_PRIMARY_FIRST_NO_ALLOCATION_UOM;children-selected->LCC.ENFORCE_PRIMARY_FIRST_NO_ALLOCATION_UOM;unresolved->RETURN_ISSUES | LCC.RESOLVE_ALLOCATION_BASIS | stop | Primary LOV values are resolved and no allocation UOM is applicable. |
