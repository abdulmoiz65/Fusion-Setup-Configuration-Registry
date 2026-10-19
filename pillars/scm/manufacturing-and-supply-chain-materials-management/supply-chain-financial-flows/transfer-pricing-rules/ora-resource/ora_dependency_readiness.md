# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 10 | Registered Data Loader business object and operation contract | Confirm the current template exposes the fields for the selected create or update operation before source preparation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| transfer_pricing_rule_create_contract | Registered Data Loader business object and create contract | Yes | A create request is prepared, imported, or validated | Ready | Current editable sample and attribute-details workbook |  | The current registration exposes effective dates, pricing-basis fields, markup fields, and fields used by a new record. PricingId is Fusion-generated on POST, and EffectiveEndDate is optional for a create. | Use the current generated workbook. Enter every supplied date as YYYY-MM-DD. Do not ask the user for PricingId on POST; leave the template column blank if present. EffectiveEndDate may be blank for a create. Regenerate the workbook whenever the BO registration changes. | RestAction, EffectiveStartDate (YYYY-MM-DD), EffectiveEndDate when supplied (YYYY-MM-DD), PricingOptionName, TransferPriceMultipleOptionsCriteria, TransferPricePricingStrategyBasisFlag, TransferPriceSourceDocumentPriceBasisFlag, TransferPriceTransactionCostBasisFlag, TransferPriceUseSalesOrderpriceDropshipFlag, TransferPriceUseBackToBackFlag, ObjectVersionNumber, EffectiveStartDateDisplay, TpItemCostBasisFlag |
| transfer_pricing_rule_update_contract | Registered Data Loader business object and update contract | Yes | An ordinary update, InsertRecord, or EndDate request is prepared, imported, or validated | Ready | Current editable sample and attribute-details workbook |  | An update requires the existing identity, source effective dates, version, and operation-specific fields rather than create defaults. | Confirm the template exposes PricingId, EffectiveStartDate, EffectiveEndDate, ObjectVersionNumber, RestAction, and the requested writable fields. InsertRecord and EndDate also require Operation and effectiveOf as documented in SKILL.md. Stop if a required field is absent. This check confirms the contract only; retain the subsequent exact-name lookup before source preparation. | Current update field contract; Operation and effectiveOf support for InsertRecord and EndDate |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Blocked | The registered business object or the selected operation's contract is unavailable or incomplete | No |
| Ready | The current contract is confirmed and includes the fields required by the selected create or update operation | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPR.CONFIRM_BO_CONTRACT | step | 10 | resolve_dependency | ready->TPR.VALIDATE_INPUT;incomplete->TPR.HANDLE_ISSUE | none | stop | Every create or update request, including ordinary updates, InsertRecord, and EndDate |
