# Rate Definitions HDL Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm merge-safe identity | Confirm the parent rate and every contributor link to the intended effective-dated record before using MERGE. |
| 2 | Select the rate category | Select Element, Derived Rate, or Value by Criteria based on the intended rate source. |
| 3 | Reconcile contributor design | Configure all contributors, periodicity conversion, currency, and FTE treatment consistently with the selected category. |
| 4 | Enforce category limitations | Apply the documented element and value-by-criteria restrictions before preparing the HDL file. |
| 5 | Gate the HDL artifact | Bind the immutable HDL artifact to the target environment and current approval in the owning core.data-loader workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A parent or contributor MERGE record is prepared | Blocker | validate_rate_definition_hdl_identity | The local HDL artifact has an ambiguous parent key, a child that does not correlate to the parent, or duplicate contributor sequence numbers | Correct the parent key or child linkage and preserve source-system identifiers when supplied before preparing the artifact | Yes |
| Category is Element | Blocker | resolve_rate_definition_hdl_contract | The selected HDL template does not support the required element, storage-type, input-value, periodicity, currency, or conversion attributes, or the element is a Hours x Rates element | Select or configure a compatible element and input value before preparing RateDefinitionV2 | Yes |
| Category is Derived Rate | Blocker | resolve_rate_definition_hdl_contract | A contributor type or source attribute is absent from the selected target template | Explicitly add only supported balance, rate-definition, base-rate, or overall-salary contributors | Yes |
| Category is Value by Criteria | Blocker | resolve_rate_definition_hdl_contract | The definition uses override or defaulting rules, or its required HDL attribute is absent from the selected target template | Do not define override/defaulting rules for this category; validate the required source definition first | Yes |
| Multiple balance or element-entry contributors are used | Blocker | resolve_rate_definition_hdl_contract | The selected currency or contributor fields are not supported by the current target template | Use the target-supported currency and contributor fields | Yes |
| Returned periodicity, factor, or FTE settings are specified | Blocker | resolve_rate_definition_hdl_contract | The conversion formula, periodicity, factor order, contributor-total FTE treatment, or returned-rate FTE treatment cannot be represented by the current target template | Reconcile the rate design with the current target HDL contract before preparation | Yes |
| Stored versus live calculation is selected | Blocker | | The request assumes CalculateLiveRatesFlag removes a documented Generate HCM Rates or country/process requirement | Select live or stored behavior deliberately and schedule Generate HCM Rates where the documented scenario requires it | Yes |
| HDL artifact is ready for import | Blocker | resolve_rate_definition_hdl_contract | The target template, immutable artifact reference, target environment, or immediate approval is absent | Complete validation and obtain approval bound to the exact artifact and environment | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| validate_rate_definition_hdl_identity | Before a parent or contributor MERGE record is accepted | Prepared parent and contributor rows, LDG, effective date, sequence, and source-system identity only when supplied | ora_reference_lookups.md |
| resolve_legislative_data_group_by_exact_name | Before accepting a parent or contributor LDG | Exact LegislativeDataGroupName and target legislative-data-group identity | ora_reference_lookups.md |
| resolve_rate_definition_hdl_contract | Before accepting category-specific sources, code values, currency, periodicity, conversion, or contributor design | Current RateDefinitionV2 business-object metadata and template | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE_DEFINITION.DESIGN_GATE | decision | 50 | design_enforcement | compliant->RATE_DEFINITION.EXECUTION_GATE;blocked->RATE_DEFINITION.HANDLE_DESIGN_BLOCKER | RATE_DEFINITION.RESOLVE_REFERENCES | stop | Enforce merge safety, category-specific rate design, and the HDL-only artifact gate. |
