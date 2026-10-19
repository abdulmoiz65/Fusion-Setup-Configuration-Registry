# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The top-level Data Loader discriminator does not match financialOrchestrationManageDropshipAgreements, or the configured child resource does not match financialOrchestrationDropshipPrimaryTradeRelations | Stop and correct the selected discriminator or child resource before preparing source data |
| The current sample or attribute-details workbook is unavailable | Stop; do not hand-build field mappings or payloads |
| SupplierOwnershipChangeEventId is missing or not 1200 or 1300 | Stop and provide 1200 for ASN From Supplier or 1300 for AP Invoice Match |
| AgreementType is not DROP_SHIP or Status is not DRAFT | Stop; do not override the fixed create defaults |
| An agreement with the exact requested AgreementNumber already exists, or the name search fails or is incomplete | Stop before preparing or approving a create; request a different name or restore the lookup |
| An update attempts to change AgreementNumber, or its exact-name lookup returns an AgreementId different from the supplied AgreementId | Stop; retain the existing agreement name and identify the original agreement by its exact name and AgreementId |
| A header status update supplies a value other than DRAFT, ACTIVE, or CANCELLED | Stop; select a code from the documented FOS_AGREEMENT_STATUS values |
| A header update omits AgreementNumber, AgreementId, RestAction=PATCH, or every changed value exposed by the current live template; or populates CustomParentKey | Stop and provide the exact lookup's AgreementId, the documented PATCH operation, and at least one supported changed value; leave CustomParentKey blank |
| An effective-dated correction header update omits its required supplied effectiveOf range | Stop and provide the exact correction range required by the selected live template |
| A child correction omits a returned child identity, RestAction=PATCH, OperationType=Correct, replacement dates, ParentEffectiveStartDate, ParentEffectiveEndDate, or `effectiveOf=RangeMode=CORRECTION` using the returned child range | Stop; resolve the requested child and parent ranges before preparing the source |
| A child-record end date, insert, delete, or another unsupported operation is requested | Stop; this resource supports child create and documented child correction only |
| An end-date request omits AgreementOperation=EndDate, EffectiveStartDate, the new EffectiveEndDate, or an effectiveOf range built from the current header range | Stop and resolve the header before preparing the source |
| A child primary trade relation create omits the parent agreement, either child date, SellingBusinessUnitName, or ReceivingTradeOrganizationName | Stop and request the missing value; do not infer a parent or organization identifier |
| A selling-business-unit or receiving-trade-organization LOV lookup returns zero or multiple exact-name matches | Stop and ask for a more precise name; do not infer an ID |
| A preview, import, or live operation fails | Preserve redacted diagnostics and stop before retrying or changing the configuration |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The current Data Loader contract is incomplete | Do not prepare an upload artifact, generate a request body, or request approval |
| An unsupported non-create operation is requested | Do not infer identity keys, date ranges, or update behavior |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN-ISSUES | terminal | 99 | terminal | none | none | stop | Any blocking outcome |
| RETURN-SUCCESS | terminal | 100 | terminal | none | FOS.DSF.CONFIRM-LOADER-READINESS | stop | Validated task-plan outcome |
| RETURN-UPDATE-SUCCESS | terminal | 101 | terminal | none | FOS.DSF.CONFIRM-HEADER-UPDATE-READINESS | stop | Validated header-update outcome |
| RETURN-CHILD-CREATE-SUCCESS | terminal | 102 | terminal | none | FOS.DSF.CONFIRM-CHILD-CREATE-READINESS | stop | Validated child primary trade relation create outcome |
| RETURN-CHILD-CORRECTION-SUCCESS | terminal | 103 | terminal | none | FOS.DSF.CONFIRM-CHILD-CORRECTION-READINESS | stop | Validated child primary trade relation correction outcome |
