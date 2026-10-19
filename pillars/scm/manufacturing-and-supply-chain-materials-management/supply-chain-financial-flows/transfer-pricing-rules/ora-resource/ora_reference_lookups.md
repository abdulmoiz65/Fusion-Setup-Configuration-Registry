# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_transfer_pricing_rule_by_name | An existing Transfer Pricing Rule is updated by name | Target environment from the active Fusion environment context; PricingOptionName from the update request | {Fusion REST base URL}/fscmRestApi/resources/11.13.18.05/financialOrchestrationAllTransferPricingRules?q=PricingOptionName='{PricingOptionName}' | PricingId, PricingOptionName, EffectiveStartDate, EffectiveEndDate, ObjectVersionNumber | Require exactly one record whose PricingOptionName exactly matches the supplied PricingOptionName. | PricingId, effective-date key in YYYY-MM-DD, and current ObjectVersionNumber for the selected Transfer Pricing Rule | No match: stop and ask for the target rule identity. More than one match: stop and ask the user to select the intended PricingId. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The lookup returns exactly one matching rule | Use its returned PricingId, effective-date key in ISO YYYY-MM-DD, and current ObjectVersionNumber to prepare the update source. |
| The lookup returns 401, 403, 404, 5xx, or a non-JSON response | Stop as an authentication, privilege, or Fusion API failure. Do not infer a PricingId or retry automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPR.FIND_RULE_BY_NAME | step | 25 | reference_lookup | resolved->TPR.ENFORCE_UPDATE_DESIGN;not_found->TPR.HANDLE_ISSUE;ambiguous->TPR.HANDLE_ISSUE;lookup_failed->TPR.HANDLE_ISSUE | TPR.VALIDATE_INPUT | stop | An existing Transfer Pricing Rule is updated by name |
