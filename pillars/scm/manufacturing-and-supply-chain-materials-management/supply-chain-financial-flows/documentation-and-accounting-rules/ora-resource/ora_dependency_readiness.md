# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Data Loader business object and current create/update contract | Generate and review the current Documentation and Accounting Rules sample before source preparation |
| 2 | Documentation and Accounting Rules | Create or maintain the rule before it is selected on a financial orchestration flow |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| documentation_and_accounting_rules_contract | Registered Data Loader business object and current contract | Yes | Every create, import, or validation request | Ready | Live Data Loader catalog and attribute-details workbook retrieved for financialOrchestrationDocumentationAndAccountingRules | | The registered object requires loader-column treatment for EffectiveEndDate, RestAction, TaRuleSetId, and TrackProfitsFlag, including any default or system-generated treatment | Generate a fresh editable sample and attribute-details workbook before preparing a source. Use the Data Loader Task Hook before requesting approval. | Current registered Data Loader headers and technical-field treatment |
| documentation_and_accounting_rules_correction_context | Existing rule identity and effective-date key | Yes | Every correction or update | Lookup | Existing rule, approved source baseline, and current live template | | A correction must target one known rule and its existing effective-date key | Resolve TaRuleSetId, TaRuleSetName, EffectiveStartDate, EffectiveEndDate, and current `Operation` support before preparing the correction source. | TaRuleSetId, TaRuleSetName, EffectiveStartDate, EffectiveEndDate, and current `Operation` support |
| currency_conversion_type | Currency conversion type | Conditional | UserConversionType is supplied | Lookup | Currency conversion types LOV | resolve_currency_conversion_type_by_exact_user_conversion_type | A user-facing conversion type must be resolved to its Fusion identifier before it is sent | Provide one exact UserConversionType value | ConversionType: ConversionTypeId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The registered business object and current contract are confirmed | No |
| Blocked | The registered business object, live template, or Task Hook validation is unavailable or incomplete | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FO.DAR.CONFIRM-BO-CONTRACT | step | 4 | resolve_dependency | standard_currency->FO.DAR.RESOLVE-STANDARD-CURRENCY;other_currency_with_conversion->FO.DAR.RESOLVE-CONVERSION-TYPE;other_currency->FO.DAR.ENFORCE-CURRENCY-POLICY;incomplete->RETURN-ISSUES | FO.DAR.DEFAULT-TRACK-PROFITS | stop | Always |
