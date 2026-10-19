# Manage Cost Factors Reference Lookups

Source: User-provided Fusion REST endpoint for supplierNegotiationCostFactors; Data Loader attribute contract in the enclosing Manage Cost Factors skill.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_cost_factor_by_name | The user requests details for a Cost Factor by name or code | Cost Factor name or Cost Factor code | GET /fscmRestApi/resources/latest/supplierNegotiationCostFactors | CostFactorId, CostFactorName, CostFactorCode, CostFactorDescription, PricingBasisCode, PricingBasis, EnabledFlag, CostFactorType, CostFactorTypeCode | Page through the collection and retain exactly one case-insensitive exact match on supplied CostFactorName or CostFactorCode. | Cost Factor ID, Cost Factor Name, Cost Factor Code, Description, Pricing Basis Code, Pricing Basis, Enabled, Cost Factor Type | No match: report that no Cost Factor match was returned. Many matches: return the matches and require the user to select one. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Request execution | Use core.fusion-api.rest-api-client with GET only, REST-Framework-Version 9, onlyData=true, and pagination until hasMore is false. |
| Scope | This lookup uses the top-level supplierNegotiationCostFactors collection supplied by the user. |
| Authorization or transport failure | Stop and report the read failure without retrying the lookup outside the shared REST client retry policy. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COST_FACTOR.LOOKUP_COST_FACTOR | step | 15 | reference_lookup | found->COST_FACTOR.RETURN_LOOKUP_RESULT;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES | COST_FACTOR.CLASSIFY_OPERATION | stop | The user requests Cost Factor details and supplies a name or code. |
