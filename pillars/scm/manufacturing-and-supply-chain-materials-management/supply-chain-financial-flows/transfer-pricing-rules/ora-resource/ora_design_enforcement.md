# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 30 | Confirm pricing-basis contract | Use only the selected pricing basis and its documented field combination from the confirmed current create contract. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Transfer Pricing Rule create request includes Item Cost Basis, Transaction Cost Basis, or Source Document Price Basis | Block |  | The request does not use the exact basis field exposed by the current Data Loader metadata, or it supplies a markup field that is unrelated to the selected basis. | Select the matching basis field and omit unrelated optional markup fields. | Yes |
| A Transfer Pricing Rule update request | Block | resolve_transfer_pricing_rule_by_name | The target PricingId, effective-date key in ISO YYYY-MM-DD, or current ObjectVersionNumber has not been resolved from exactly one rule whose PricingOptionName exactly matches the target supplied in the update request. | Use only the values returned by the declared lookup. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_transfer_pricing_rule_by_name | Before updating a Transfer Pricing Rule by name | PricingId, EffectiveStartDate (YYYY-MM-DD), EffectiveEndDate (YYYY-MM-DD), and current ObjectVersionNumber | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPR.ENFORCE_DESIGN | step | 30 | design_enforcement | passed->TPR.DONE_READY;blocked->TPR.HANDLE_ISSUE | TPR.VALIDATE_INPUT | stop | A Transfer Pricing Rule create request is validated |
| TPR.ENFORCE_UPDATE_DESIGN | step | 35 | design_enforcement | passed->TPR.DONE_UPDATE_READY;blocked->TPR.HANDLE_ISSUE | TPR.FIND_RULE_BY_NAME | stop | A Transfer Pricing Rule update request is validated and the target PricingId is resolved |
