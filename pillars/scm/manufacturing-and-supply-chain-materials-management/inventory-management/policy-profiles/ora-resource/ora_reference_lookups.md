# Policy Profiles Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| review_min_max_policy_profiles_metadata | Before a Policy Profiles Data Loader operation | Current-run Data Loader attribute-details preflight result for minMaxPolicyProfiles | Accept exactly one successful current-run result that identifies business object minMaxPolicyProfiles. | metadata_preflight_status; attribute_details_artifact | No successful result or a result for another business object: block the operation and rerun the metadata preflight. |
| resolve_policy_type_ui_mapping | A PolicyType value is supplied | PolicyType; Redwood static option values 1 and 2 | Match the supplied value exactly to static value 1 or 2. Map 1 to the Min-Max Planning UI option and 2 to the PAR UI option. | PolicyType | No match: block and request PolicyType 1 or 2. Many matches cannot occur because the UI option values are static. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_max_qty_calculation_method | A MaxCalcMethod value is supplied | MaxCalcMethod; lookup type ORA_MSC_ROP_MAX_CALC_METHOD | /fscmRestApi/resources/11.13.18.05/standardLookups/ORA_MSC_ROP_MAX_CALC_METHOD/child/lookupCodes?onlyData=true | LookupCode; Meaning; EnabledFlag; StartDateActive; EndDateActive | Retrieve all result pages. Trim and case-insensitively exact-match the supplied value to one currently enabled LookupCode or Meaning, then use LookupCode. | MaxCalcMethod: LookupCode | Zero matches or more than one active exact match: block and request a valid Max Qty Calculation Method. |
| resolve_safety_stock_calculation_method | An SsCalcMethod value is supplied | SsCalcMethod; lookup type ORA_MSC_ROP_SS_METHOD | /fscmRestApi/resources/11.13.18.05/standardLookups/ORA_MSC_ROP_SS_METHOD/child/lookupCodes?onlyData=true | LookupCode; Meaning; EnabledFlag; StartDateActive; EndDateActive | Retrieve all result pages. Trim and case-insensitively exact-match the supplied value to one currently enabled LookupCode or Meaning, then use LookupCode. | SsCalcMethod: LookupCode | Zero matches or more than one active exact match: block and request a valid Safety Stock Calculation Method. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A Policy Type, Max Qty Calculation Method, or Safety Stock Calculation Method is supplied | Resolve only the documented mapping or read-only lookup. Do not default, clear, or conditionally set any value. |
| The live lookup returns HTTP 401 or 403 | Refresh the cached OAuth token once through the selected Fusion REST client, then stop if the retry fails. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PP.LOOKUP_MAX_QTY_METHOD | decision | 4 | reference_lookup | found_or_not_supplied->PP.LOOKUP_SAFETY_STOCK_METHOD;not_found_or_ambiguous->PP.STOP_LOOKUP | PP.MAP_POLICY_TYPE | stop | A selected task-local mapping or lookup request is processed |
| PP.LOOKUP_SAFETY_STOCK_METHOD | decision | 5 | reference_lookup | found_or_not_supplied->PP.COMPLETE;not_found_or_ambiguous->PP.STOP_LOOKUP | PP.LOOKUP_MAX_QTY_METHOD | stop | A selected task-local mapping or lookup request is processed |
