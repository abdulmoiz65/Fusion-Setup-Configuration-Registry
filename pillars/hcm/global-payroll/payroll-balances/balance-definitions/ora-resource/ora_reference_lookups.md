# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_balance_by_exact_name | A balance name is supplied for duplicate assessment or existing-balance selection | BalanceName, target environment | /hcmRestApi/resources/11.13.18.05/payrollBalanceDefinitionsLOV?q=BalanceName%3D%27{BalanceName}%27 | BalanceTypeId, BalanceName, BalanceCode, LegislativeDataGroupName | Match the supplied BalanceName exactly; no match is valid for a new balance | BalanceId: BalanceTypeId, existing balance identity | No match: classify as no existing match and continue. Many matches: stop and request an unambiguous target selection. |
| find_ldg_by_exact_name | A target LDG display name is supplied | LegislativeDataGroupName, target environment | /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV?q=Name%3D%27{LegislativeDataGroupName}%27 | LegislativeDataGroupId, Name, LegislationCode, DefaultCurrencyCode | Match the supplied LegislativeDataGroupName exactly against Name | LegislativeDataGroupId, LegislativeDataGroupName: Name, legislation context, default currency | No match or many matches: stop and report the supplied LDG. |
| resolve_balance_metadata | Parent HDL structure must be verified | Target environment, PayrollBalanceDefinition.dat | Data Exchange > View Business Objects: Payroll Balance Definition, then Core Data Loader live schema validation | File discriminator, required parent attributes, supported operation, and data types | Require exact discriminator PayrollBalanceDefinition and a successful live schema validation result | Validated parent business-object contract | Missing or failed validation: stop before import. |
| resolve_balance_reference_values | A category, UOM, currency, dimension, classification, element, input value, or feed date is supplied | Target environment, target LDG, supplied business value | Target Fusion payroll setup LOV for the applicable value in the selected LDG | Exact configured code or identifier and applicable LDG context | Match exactly one value in the selected LDG and legislation context | Validated code or ID and applicable attributes | No match or many matches: stop and report the supplied field and value. |
| resolve_balance_source_system_reference | BalanceId(SourceSystemId) is proposed | SourceSystemOwner, SourceSystemId, target environment | PayrollBalanceDefinition parent record resolved through the target HDL source-system cross-reference | BalanceId and source-system cross-reference behavior | Resolve exactly one parent balance record | BalanceId | No match or many matches: stop and use direct BalanceId or correct the source-system identifiers. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Direct BalanceId is supplied for a child | Use it directly. Do not call a source-system lookup. |
| BalanceCode and LDG are supplied for a child | Use the documented alternate parent key. Do not require BalanceId or source-system identifiers. |
| A display name is supplied | Resolve exactly one target-LDG value before writing the HDL field that requires a code or ID. |
| A lookup contract is marked TBD | Treat it as a readiness blocker; do not invent a REST endpoint, response shape, or local authority. |
| A lookup fails | Stop before retry, classify the failure, and disclose sanitized diagnostics. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BAL.LOOKUP_EXISTING | decision | 20 | reference_lookup | match_resolved->BAL.RESOLVE_DEPENDENCIES;no_match->BAL.RESOLVE_DEPENDENCIES;lookup_failed->BAL.HANDLE_LOOKUP_ERROR | BAL.VALIDATE_INPUT | stop | An existing-balance assessment is required |
