# Reference Lookups

Source: user-provided create-validation contract and Redwood setup UI evidence for Documentation and Accounting Rules. The preferred-currencies lookup supports both currency name and currency code. The skill uses exact lookup matching rather than the UI's substring search to ensure the prompt resolves to one currency.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_preferred_currency_by_name_or_code | CurrencyOption is ORA_STANDARD_CURRENCY | Standard Currency name or Currency Code | {Fusion REST base URL}/fscmRestApi/resources/11.13.18.05/preferredCurrenciesLOV?q=CurrencyName='{value}' and/or q=CurrencyCode='{value}' | CurrencyName, CurrencyCode | If the prompt explicitly labels the value as a Currency Code, query CurrencyCode only; otherwise query both fields separately with exact q predicates. Compare returned values case-insensitively, combine and deduplicate results by CurrencyCode, and require exactly one currency. Do not use upper(), lower(), or like in q. | StandardCurrency: returned CurrencyCode | Stop and ask for a valid, unambiguous Standard Currency name or code |
| resolve_currency_conversion_type_by_exact_user_conversion_type | UserConversionType is supplied | UserConversionType | {Fusion REST base URL}/fscmRestApi/resources/11.13.18.05/currencyConversionTypesLOV?q=UserConversionType='{UserConversionType}' | UserConversionType, ConversionTypeId | Send only q=UserConversionType='{UserConversionType}'; require exactly one returned UserConversionType value | ConversionType: ConversionTypeId | Stop and ask for a valid, unambiguous UserConversionType value |
| resolve_trade_accounting_rule_set_by_name | An existing Documentation and Accounting Rule is corrected, updated, or selected for deletion by name | Target environment from the active Fusion environment context; exact TaRuleSetName | {Fusion REST base URL}/fscmRestApi/resources/11.13.18.05/financialOrchestrationDocumentationAndAccountingRules?q=TaRuleSetName='{TaRuleSetName}' | TaRuleSetId, TaRuleSetName, EffectiveStartDate, EffectiveEndDate, Description, CurrencyOption, TradeDistributions, InterCompanyInvoice, TrackProfitsFlag | Describe the collection first and use only fields it exposes. Require exact TaRuleSetName equality; for a delete target, require one selected effective record and preserve its ID/date-key context. | TaRuleSetId, TaRuleSetName, EffectiveStartDate, EffectiveEndDate, and existing field values needed by a correction or delete source | No match: stop and request a corrected rule name. Multiple effective records: present their IDs and date ranges and ask the user to select one; never choose the first. |
| check_financial_orchestration_flow_usage_for_dar | A delete target has been resolved to one TaRuleSetId | Target environment from the active Fusion environment context; resolved TaRuleSetId | Page GET /fscmRestApi/resources/latest/financialOrchestrationTradeAgreements; for every agreement item GET <agreement-item>/child/PrimaryTradeRelation; for every PTR item GET <ptr-item>/child/FinancialTradeRelation | AgreementId, AgreementNumber, agreement effective dates and item links; PrimaryTradeRelationNumber and PTR links; SequenceNumber, TradeAccountingRuleSetId, FTR effective dates and item links | Traverse every returned agreement/version, PTR, and FTR using each collection's pagination/next links, without status or effective-date filters. Compare each FTR TradeAccountingRuleSetId exactly to the resolved TaRuleSetId. Stop early on one exact match and return its agreement and route identity; only a completed full traversal with no match proves unused. | Usage outcome: referenced with agreement/primary-route/financial-route identity; not_referenced after complete traversal; or incomplete/unknown | Any matching FTR reference means in use. Any failed page, inaccessible collection, missing TradeAccountingRuleSetId field, or incomplete traversal is unresolved and blocks deletion. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Standard Currency is selected | Run the declared read-only lookup before validating the source; accept a name or code, but always resolve it to a returned CurrencyCode |
| The query expression uses upper(), lower(), or like | Do not send the request; these expressions are rejected by this resource |
| Exactly one currency is returned for the explicitly supplied name or code | Send its returned CurrencyCode as StandardCurrency, including when the prompt supplied a code |
| No match or multiple distinct currencies are returned across the name/code queries | Stop; do not infer a currency code |
| UserConversionType is supplied | Run the declared read-only conversion-type lookup before source validation |
| The conversion-type query includes a field other than UserConversionType | Do not send the request; query only UserConversionType |
| Exactly one UserConversionType match is returned | Send its ConversionTypeId as ConversionType |
| No conversion-type match or multiple matches | Stop; do not infer a ConversionTypeId |
| A correction or update is requested by rule name | Describe the declared collection, then run the declared exact-name lookup before preparing the correction source |
| The collection does not expose a required correction identity or effective-date field | Stop; do not infer TaRuleSetId or effective-date key. |
| Exactly one TaRuleSetName match is returned | Use its TaRuleSetId and effective-date values as the correction context only after confirming the returned name exactly matches the request |
| No match or multiple TaRuleSetName matches are returned for a correction | Stop; do not choose a rule or synthesize a surrogate key |
| A delete is requested by rule name | Resolve exactly one selected rule first, then run check_financial_orchestration_flow_usage_for_dar before preparing any delete source |
| A matching FinancialTradeRelation is found | Treat the DAR as in use; stop delete preparation and report the matched agreement, PTR, and FTR identity. Do not cascade-delete or alter the FOF. |
| The agreement-to-PTR-to-FTR traversal completes with no matching ID | Mark the target unused and allow the normal Data Loader delete-preparation workflow to continue; this lookup does not perform the delete. |
| The usage scan cannot prove completeness | Stop before delete preparation; do not interpret a failed or partial scan as no usage. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FO.DAR.RESOLVE-STANDARD-CURRENCY | step | 5 | reference_lookup | resolved_with_conversion->FO.DAR.RESOLVE-CONVERSION-TYPE;resolved->FO.DAR.ENFORCE-CURRENCY-POLICY;not_found->RETURN-ISSUES;ambiguous->RETURN-ISSUES;lookup_failed->RETURN-ISSUES | FO.DAR.CONFIRM-BO-CONTRACT | stop | CurrencyOption is ORA_STANDARD_CURRENCY |
| FO.DAR.RESOLVE-CONVERSION-TYPE | step | 6 | reference_lookup | resolved->FO.DAR.ENFORCE-CURRENCY-POLICY;not_found->RETURN-ISSUES;ambiguous->RETURN-ISSUES;lookup_failed->RETURN-ISSUES | FO.DAR.CONFIRM-BO-CONTRACT | stop | UserConversionType is supplied |
| FO.DAR.RESOLVE-DELETE-TARGET | step | 8 | reference_lookup | resolved->FO.DAR.CHECK-DELETE-FLOW-USAGE;not_found->RETURN-ISSUES;ambiguous->RETURN-ISSUES;lookup_failed->RETURN-ISSUES | FO.DAR.VALIDATE-INPUTS | stop | A delete request has one validated exact rule name |
| FO.DAR.CHECK-DELETE-FLOW-USAGE | step | 9 | reference_lookup | referenced->FO.DAR.ENFORCE-DELETE-ELIGIBILITY;not_referenced->FO.DAR.ENFORCE-DELETE-ELIGIBILITY;scan_incomplete->FO.DAR.ENFORCE-DELETE-ELIGIBILITY | FO.DAR.RESOLVE-DELETE-TARGET | stop | A single TaRuleSetId has been resolved for deletion |
