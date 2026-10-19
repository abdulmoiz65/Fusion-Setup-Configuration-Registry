# Design Enforcement

Source: Oracle [Currency Options in Accounting Rules](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/faims/currency-options-in-accounting-rules.html) and [Manage Documentation and Accounting Rule in Redwood Pages](https://docs.oracle.com/en/cloud/saas/readiness/scm/24c/inv24c/24C-inventory-wn-f33534.htm).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Choose currency policy | Select the currency source that matches the financial-orchestration design |
| 2 | Confirm documentation outcomes | Select trade distributions, intercompany invoice, or both; apply the Track Profits default or eligible override |
| 3 | Confirm effective dating | Use an effective start date appropriate for the deployment plan |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| CurrencyOption is ORA_STANDARD_CURRENCY | Error | resolve_preferred_currency_by_name_or_code | StandardCurrency is missing or was not resolved from the preferred-currencies lookup | Provide a Standard Currency name or code and use the returned CurrencyCode | Yes |
| Any documentation and accounting rule | Error | | TaRuleSetName, EffectiveStartDate, CurrencyOption, or both documentation outcomes are missing | Complete the required create inputs before preview | Yes |
| Any documentation and accounting rule | Error | | TradeDistributions and InterCompanyInvoice are both N | Enable at least one documentation outcome | Yes |
| TrackProfitsFlag is true | Error | | TradeDistributions is not Y | Set TrackProfitsFlag to false or select TradeDistributions | Yes |
| UserConversionType is supplied | Error | resolve_currency_conversion_type_by_exact_user_conversion_type | ConversionTypeId was not resolved from the currency conversion types LOV | Provide a valid, unambiguous UserConversionType and use the returned ConversionTypeId | Yes |
| A Documentation and Accounting Rule correction or update request | Error | resolve_trade_accounting_rule_set_by_name | The target TaRuleSetId or effective-date context has not been resolved from exactly one rule whose TaRuleSetName exactly matches the update request | Use only values returned by the declared lookup. | No |
| A Documentation and Accounting Rule delete request | Error | check_financial_orchestration_flow_usage_for_dar | Any FinancialTradeRelation references the resolved TaRuleSetId, or the complete agreement-to-PTR-to-FTR scan is not verified | If referenced, do not delete or cascade; remove/change the reference through its owning Financial Orchestration Flow setup workflow, verify it is gone, then re-run the delete preflight. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_preferred_currency_by_name_or_code | CurrencyOption is ORA_STANDARD_CURRENCY | StandardCurrency from CurrencyCode | ora_reference_lookups.md |
| resolve_currency_conversion_type_by_exact_user_conversion_type | UserConversionType is supplied | ConversionType from ConversionTypeId | ora_reference_lookups.md |
| resolve_trade_accounting_rule_set_by_name | Before correcting or updating a Documentation and Accounting Rule by name | TaRuleSetId, TaRuleSetName, EffectiveStartDate, EffectiveEndDate, and correction context dates | ora_reference_lookups.md |
| check_financial_orchestration_flow_usage_for_dar | Before preparing any Documentation and Accounting Rule delete source | Exact usage scan result for the resolved TaRuleSetId; matching agreement/PTR/FTR identity if used | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FO.DAR.ENFORCE-CURRENCY-POLICY | step | 7 | design_enforcement | passed->RETURN-SUCCESS;blocked->RETURN-ISSUES | FO.DAR.CONFIRM-BO-CONTRACT | stop | Always |
| FO.DAR.ENFORCE-DELETE-ELIGIBILITY | step | 10 | design_enforcement | eligible->FO.DAR.DELETE-ELIGIBILITY-PASSED;blocked->RETURN-ISSUES | FO.DAR.CHECK-DELETE-FLOW-USAGE | stop | Delete is eligible only after a complete usage scan finds no matching FinancialTradeRelation |
