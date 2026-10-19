# Landed Cost Charges Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Primary charge identity | Name, Code, Description, Procurement BU Set | Stop before preview or import preparation | Obtain the missing business value; resolve the selected set before using it as SetId. | Creating a landed cost charge | resolve_procurement_bu_set |
| Charge attributes | TrackMissingInvoicesFlag, TaxApplicableFlag, Charge Currency, Currency Conversion Type, Charge Basis, Allocation Basis | Stop before preview or import preparation | Obtain the missing business value and resolve every LOV-backed value. AutoTaxCalculation is optional unless the user explicitly supplies it. | Creating a landed cost charge | resolve_charge_currency |
| Per-unit charge basis | Charge Basis UOM | Stop before preview or import preparation | Supply and resolve the UOM. | Charge Basis resolves to PER_UNIT | resolve_charge_basis_uom |
| Allocation UOM | Allocation Basis UOM | Stop before preview or import preparation | Supply and resolve the UOM when applicable to the selected allocation basis. | An allocation UOM is applicable | resolve_allocation_basis_uom |
| Default reference type association | Parent charge identity, selected reference type, DefaultAutoAssociateFlag | Stop only the requested child association | Resolve one applicable global or selected-set reference type and include its child row after the parent section. | Adding a default reference type | resolve_default_charge_reference_type |
| Cost analysis association | Parent charge identity, selected analysis group, selected analysis code | Stop only the requested child association | Resolve the group and code, then include its child row after the parent section. | Adding a cost analysis association | resolve_cost_analysis_group |
| Cost analysis association removal | Existing primary charge identity and exact ChargeAnalysisCodeId | Stop only the requested child deletion | Resolve the exact existing child association before preparing the deletion. | Removing a cost analysis association | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ChargeBasisUOMCode is conditional | Include ChargeBasisUOMCode only when ChargeBasisCode is PER_UNIT. | Preparing the primary charge values | resolve_charge_basis |
| Optional child scope | Do not require attachments, default charge reference types, or cost analysis group/code associations to create the primary charge. | Optional values are omitted | |
| Data Loader workbook source | Provide resolved parent and requested child-association values in the current landedCostCharges Data Loader workbook; core.data-loader owns source generation and serialization. | Every routed import | |
| Parent-before-child serialization rule | For a new charge, serialize the parent section before `chargeDefaultReferenceTypes` and `chargeAnalysisCodes` in the same archive. | Creating a charge with optional children | |
| Analysis association removal identity | Do not use analysis group or code as a substitute delete key; use the exact existing ChargeAnalysisCodeId. | Removing a cost analysis association | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A primary charge request has all required values resolved | Prepare the parent with SetId, EnteredCurrencyCode, CurrencyConversionType, ChargeBasisCode, and DefaultAllocBasisCode; include conditional UOM fields only when applicable. | Continue to immutable preview through core.data-loader. | |
| A default reference type is selected | Resolve it and prepare the child row after the parent section. | Continue through core.data-loader using the current child-row contract. | resolve_default_charge_reference_type |
| A cost analysis association is selected | Resolve the group and code and prepare the child row after the parent section. | Continue through core.data-loader using the current child-row contract. | resolve_cost_analysis_group |
| A cost analysis association is removed | Keep the primary charge unchanged and prepare only the child deletion with the exact resolved ChargeAnalysisCodeId. | Continue through core.data-loader. | |

## Nested Resource Contract

| Parent Resource | Child Resource | Supported Use |
|---|---|---|
| landedCostCharges | chargeDefaultReferenceTypes | Add an optional default charge reference type after the parent section in the same archive, or to an existing charge. |
| landedCostCharges | chargeAnalysisCodes | Add an optional Cost Analysis Group and Code association after the parent section in the same archive, or to an existing charge. |
| landedCostCharges | chargeAnalysisCodes | Remove one exactly resolved Cost Analysis association without deleting or recreating the primary charge. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCC.VALIDATE_INPUT | step | 10 | validate_input | valid->LCC.RESOLVE_SET;invalid->RETURN_ISSUES | none | stop | A landed cost charge is requested. |
