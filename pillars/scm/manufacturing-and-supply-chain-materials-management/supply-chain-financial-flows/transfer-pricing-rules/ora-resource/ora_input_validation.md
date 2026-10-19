# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Rule identity | PricingOptionName | Stop | Provide a name of no more than 100 characters. | A new Transfer Pricing Rule is requested |  |
| Effective dates | EffectiveStartDate; EffectiveEndDate when supplied | Stop only when EffectiveStartDate is missing or a supplied date is invalid | Provide EffectiveStartDate in ISO 8601 calendar-date format YYYY-MM-DD. EffectiveEndDate is optional for a create; when supplied, it must also use YYYY-MM-DD. | A new Transfer Pricing Rule is requested |  |
| Core create fields | RestAction, TransferPriceMultipleOptionsCriteria, TransferPricePricingStrategyBasisFlag, TransferPriceSourceDocumentPriceBasisFlag, TransferPriceTransactionCostBasisFlag, TransferPriceUseSalesOrderpriceDropshipFlag, TransferPriceUseBackToBackFlag, ObjectVersionNumber, EffectiveStartDateDisplay, and TpItemCostBasisFlag | Stop | Retain and complete the listed create fields required by the current generated template. Do not add PricingId as a create requirement. | A new Transfer Pricing Rule is requested |  |
| Create identifier | PricingId is Fusion-generated | Continue | Do not ask the user to provide PricingId for a POST. If the generated template includes the column, leave it blank for a create. | A new Transfer Pricing Rule is requested |  |
| Transfer-price basis | TpItemCostBasisFlag for Item Cost Basis; TransferPriceTransactionCostBasisFlag for Transaction Cost Basis; TransferPriceSourceDocumentPriceBasisFlag for Source Document Price Basis | Stop | Use the exact field for the selected basis. Validate its value through the current Data Loader contract during source validation. | A new Transfer Pricing Rule is requested |  |
| Optional basis markup | TpItemCostMarkupValue, TransferPriceCostBasisMarkupType, TransferPriceCostBasisMarkupValue, TransferPriceSourceDocumentMarkupType, or TransferPriceSourceDocumentMarkupValue | Continue | Include an optional markup field only when it applies to the selected basis and validate it through the current Data Loader contract. | A markup is supplied |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A requested business field is absent from the current create contract | Blocked | Correct the BO registration or obtain the documented contract, then restart validation. |  |
| The requested rule name, EffectiveStartDate in YYYY-MM-DD, optional EffectiveEndDate in YYYY-MM-DD when supplied, selected pricing basis, and all supplied fields conform to the confirmed contract | Continue | Apply the task design gate. |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Field identity and shape | Validate every supplied field only against the current registered-business-object template and attribute details. | Every supplied value |  |
| Date value shape | Accept user-supplied dates as ISO 8601 calendar dates written YYYY-MM-DD. When generating a Data Loader workbook, allow the generator's required YYYY/MM/DD date representation; do not hand-convert the generated cells. | Every supplied date-bearing value in a create or PATCH source |  |
| InsertRecord effective date | Retain the source row's EffectiveStartDate and EffectiveEndDate. Put the new version date only in `effectiveOf` as `RangeMode=UPDATE;RangeStartDate={new-start-date};RangeEndDate={source-end-date}` and set Operation to InsertRecord. | A Data Loader InsertRecord version is requested | resolve_transfer_pricing_rule_by_name |
| PATCH correction effective range | Resolve the target record before building the source. Put the requested replacement dates in `EffectiveStartDate` and `EffectiveEndDate`, but set `effectiveOf` to `RangeMode=CORRECTION;RangeStartDate={existing-start-date};RangeEndDate={existing-end-date}`. Never use the replacement dates in `effectiveOf`. | A date-effective PATCH correction is requested | resolve_transfer_pricing_rule_by_name |
| Pricing basis representation | Use TpItemCostBasisFlag, TransferPriceTransactionCostBasisFlag, or TransferPriceSourceDocumentPriceBasisFlag according to the selected basis. Do not substitute a similarly named field. | A transfer-price basis is supplied |  |
| PATCH identity and version | Resolve the target first. Use its PricingId, effective-date key in ISO YYYY-MM-DD, current ObjectVersionNumber, and RestAction PATCH in the update source. | An existing Transfer Pricing Rule is updated | resolve_transfer_pricing_rule_by_name |
| PATCH accounting-basis encoding | Use one-character Y or N values from the current Data Loader template, not REST-style true or false. Set exactly one of TpItemCostBasisFlag, TransferPriceTransactionCostBasisFlag, or TransferPriceSourceDocumentPriceBasisFlag to Y and set the other two to N. Omit AccountingTransferPriceBasis, SelectedTransferPriceBasis, and unrelated markup fields. | A PATCH changes the accounting transfer price basis |  |
| Optional markup fields | Validate markup fields only when supplied; the current metadata describes them as optional. | A markup is supplied |  |

## Create Basis Defaults

For a new Transfer Pricing Rule, resolve the requested basis to its stored
fields before generating the population JSON. The transient Redwood selection
(`ORA_ITEM_COST`, `D`, or `C`) identifies the branch; do not persist it through
`SelectedTransferPriceBasis` or another derived field.

| Requested Basis | Transient Selection | Set to `Y` | Set Other Basis Flags to `N` | Markup Field | Redwood Applicability Defaults |
|---|---|---|---|---|---|
| Item Cost | `ORA_ITEM_COST` | `TpItemCostBasisFlag` | `TransferPriceSourceDocumentPriceBasisFlag`; `TransferPriceTransactionCostBasisFlag` | `TpItemCostMarkupValue` | Set `TransferPriceUseSalesOrderpriceDropshipFlag` and `TransferPriceUseBackToBackFlag` to `N`. |
| Source Document Price | `D` | `TransferPriceSourceDocumentPriceBasisFlag` | `TpItemCostBasisFlag`; `TransferPriceTransactionCostBasisFlag` | `TransferPriceSourceDocumentMarkupValue` | Preserve explicitly supplied drop-ship and back-to-back values. Do not infer either value for a new rule when neither is supplied. |
| Transaction Cost | `C` | `TransferPriceTransactionCostBasisFlag` | `TpItemCostBasisFlag`; `TransferPriceSourceDocumentPriceBasisFlag` | `TransferPriceCostBasisMarkupValue` | Set `TransferPriceUseSalesOrderpriceDropshipFlag` and `TransferPriceUseBackToBackFlag` to `N`. |

For all three branches, preserve a supplied
`TransferPricePricingStrategyBasisFlag`; otherwise set it to `N`. Preserve a
supplied `TransferPriceMultipleOptionsCriteria`; otherwise set it to `H`.
Populate a markup field only when the requester supplies a markup. These
defaults apply only to a new create source. An update continues to use the
resolved source record and the PATCH rules above.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPR.VALIDATE_INPUT | step | 20 | validate_input | valid_create->TPR.ENFORCE_DESIGN;valid_update->TPR.FIND_RULE_BY_NAME;invalid->TPR.HANDLE_ISSUE | TPR.CONFIRM_BO_CONTRACT | stop | After the current create or update contract is confirmed |
