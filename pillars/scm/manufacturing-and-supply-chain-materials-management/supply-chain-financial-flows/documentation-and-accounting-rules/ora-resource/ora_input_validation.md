# Input Validation

Source: Oracle [Shipment Flow](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/faims/shipment-flow.html) and [TradeAccountingRuleSet business object](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fabsm/bo_oraScmCoreFosSetup_TradeAccountingRuleSet.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Data Loader contract | Current editable sample and attribute-details workbook for financialOrchestrationDocumentationAndAccountingRules | Stop before preview | Generate a current sample through core.data-loader and use only its exposed fields | Always | |
| Mandatory loader columns | EffectiveEndDate, RestAction, TaRuleSetId, TrackProfitsFlag | Stop before preview when a required column is absent, not solely when a defaulted or optional value is blank | Retain the required columns; validate values by operation. Metadata mandatory flags do not by themselves require user values for defaulted fields or system-generated IDs. | Always | |
| Required create inputs | TaRuleSetName, EffectiveStartDate, CurrencyOption, and TradeDistributions or InterCompanyInvoice | Stop before preview | Provide a rule name, an ISO start date that is today or in the future, a currency option, and select at least one documentation outcome | Every create | |
| Required correction identity | TaRuleSetId, TaRuleSetName, and the resolved existing effective-date range | Stop before preview | Resolve the existing rule and retain its effective start and end dates for the correction `effectiveOf` range. Serialize every date as `YYYY-MM-DD`. | Every correction or update | |
| Required delete target | TaRuleSetName for one existing Documentation and Accounting Rule | Stop before delete eligibility check | Resolve an exact-name target. If more than one effective record has that name, show the candidate IDs and date ranges and ask the user which record to delete. | Every delete request | resolve_trade_accounting_rule_set_by_name |
| Currency policy | CurrencyOption | Stop before preview | Select Selling node, Buying node, Source document, or Standard currency | Always | |
| Documentation outcomes | TradeDistributions or InterCompanyInvoice | Stop before preview | Select Y for at least one outcome; the unselected outcome may be N | Every create | |
| Optional create inputs | Description, EffectiveEndDate, TrackProfitsFlag, UserConversionType, Generate Events for Internal Transfer — Forward Flow, and Generate Events for Internal Transfer — Return Flow | Continue without the optional value only after explicitly offering every field in the initial intake | Map supplied values only to exposed fields. Omitted or explicitly none EffectiveEndDate remains blank for Fusion defaulting. Do not promote optional inputs to required solely from metadata mandatory flags. Resolve a supplied UserConversionType before sending ConversionType; allow TrackProfitsFlag=true only when TradeDistributions is Y. | Every create | resolve_currency_conversion_type_by_exact_user_conversion_type |

## Field Validation

End-date source: implementation owner confirmed use of the Transfer Pricing
Rule end-date pattern for DAR (Operation EndDate, PATCH and END_DATE range).

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Field identity and shape | Validate every value against the current registered-business-object template and attribute-details workbook | Every supplied value | |
| Effective Start Date | Accept YYYY-MM-DD only when it is today or a future date | Every create | |
| Correction effective-date range | Put replacement dates in the payload's `EffectiveStartDate` and `EffectiveEndDate`. Set `effectiveOf=RangeMode=CORRECTION;RangeStartDate={existing-start-date};RangeEndDate={existing-end-date}` using the resolved current range. Require a supplied replacement start date to be no later than the supplied replacement end date. | Operation is Correct | |
| Correction field contract | Require `Operation`, `effectiveOf`, and every supplied correction field to exist in the current live template. | Operation is Correct | |
| Delete target identity | Require one exact-name rule resolution before checking usage. If the name resolves to multiple effective records, stop and ask the user to select one; never choose the first result. | Operation is Delete | resolve_trade_accounting_rule_set_by_name |
| Update DAT shape | For `Correct` updates, include only the parent `financialOrchestrationDocumentationAndAccountingRules` METADATA and MERGE rows. Do not add child METADATA sections or child rows unless the requested change explicitly targets a supported child attribute. | Operation is Correct | |
| Correction operation | Require the exact current-template representation of `Operation=Correct` and `RestAction=PATCH`; do not infer boolean or null serialization. | Operation is Correct | |
| Start-date correction DAT assertion | Before packaging, require one parent-only METADATA/MERGE pair; leave `CustomSurrogateId` blank; set `TaRuleSetId` to the single exact-name lookup result; require `RestAction=PATCH` and `Operation=Correct`. Serialize `EffectiveStartDate`, `EffectiveEndDate`, and both dates inside `effectiveOf` as zero-padded `YYYY-MM-DD` (hyphens only). Reject slash-formatted dates or any mismatch. A passing live-schema check does not satisfy this assertion. | Operation is Correct and the requested `EffectiveStartDate` differs from the resolved existing start date | resolve_trade_accounting_rule_set_by_name |
| End-date operation | Require current parent template fields and exactly one resolved rule. Retain its TaRuleSetId, TaRuleSetName and original effective dates as ISO YYYY-MM-DD. Set Operation=EndDate, RestAction=PATCH and effectiveOf=RangeMode=END_DATE;RangeStartDate={source-start};RangeEndDate={requested-end}. Require source-start <= requested-end < source-end; equality with source-end is a no-op. Preserve business values; do not synthesize child rows. | Operation is EndDate | resolve_trade_accounting_rule_set_by_name |
| Insert Record support | Unsupported in the current skill Data Loader workflow. Return the unsupported-operation finding and stop before executable source preparation, approval, upload, or retry. Updates through Correct remain supported; do not substitute Correct for an effective-period split. | Operation is InsertRecord or the request splits an existing effective period | |
| Currency Option | Map Selling node to FROM_NODE, Buying node to TO_NODE, Source document to SOURCE_DOCUMENT, and Standard currency to ORA_STANDARD_CURRENCY; reject every other value | Every create | |
| Documentation outcomes | Require TradeDistributions=Y or InterCompanyInvoice=Y; reject a request that sets both to N | Every create | |
| Optional field mapping | Reject a supplied Description, EffectiveEndDate, Generate Events for Internal Transfer — Forward Flow, or Generate Events for Internal Transfer — Return Flow value that has no exact field in the current live template | The optional value is supplied | |
| Internal-transfer event selection | Accept exactly one numbered Forward Flow selection: `1` (Interorganization Shipment) maps to `1700`, or `2` (Interorganization Receipt) maps to `1800`. Accept exactly one numbered Return Flow selection: `1` (Interorganization Shipment Return) maps to `2000`, or `2` (Interorganization Receipt Return) maps to `1900`. Do not infer a selection. | An internal-transfer event value is supplied | |
| Conversion Type | Query only UserConversionType using its exact supplied value; require exactly one result and send its ConversionTypeId as ConversionType | UserConversionType is supplied | resolve_currency_conversion_type_by_exact_user_conversion_type |
| Track intercompany profits in inventory eligibility | Reject TrackProfitsFlag=true when TradeDistributions is not Y; otherwise default it to false or allow an eligible true value | Every create | |
| Standard Currency | Accept a Standard Currency name or Currency Code and resolve it to the returned CurrencyCode before source validation; when the prompt explicitly labels a value as Currency Code, resolve only against CurrencyCode | CurrencyOption is ORA_STANDARD_CURRENCY | resolve_preferred_currency_by_name_or_code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FO.DAR.VALIDATE-INPUTS | step | 1 | validate_input | create_update_valid->FO.DAR.VALIDATE-INSERT-RECORD;delete_valid->FO.DAR.RESOLVE-DELETE-TARGET;invalid->RETURN-ISSUES | none | stop | Always; dispatch delete only to the delete-target and usage gates |
| FO.DAR.VALIDATE-INSERT-RECORD | step | 2 | validate_input | unsupported->RETURN-ISSUES;not_applicable->FO.DAR.DEFAULT-TRACK-PROFITS | FO.DAR.VALIDATE-INPUTS | stop | Always; return unsupported for InsertRecord or an effective-period split, otherwise not_applicable |
