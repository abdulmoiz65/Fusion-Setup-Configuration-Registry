# Dependency Readiness

Source: developer-provided Data Loader business-object configuration screenshot.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Data Loader discriminator and configured child resource | Confirm financialOrchestrationManageDropshipAgreements is selected as the top-level Data Loader discriminator and financialOrchestrationDropshipPrimaryTradeRelations remains the configured child resource |
| 2 | Current Data Loader create contract | Generate and review the editable sample and attribute-details workbook for financialOrchestrationManageDropshipAgreements before preparing source data |
| 3 | Header update contract | Confirm the live update template uses RestAction=PATCH and AgreementId from the exact AgreementNumber lookup; CustomParentKey remains blank |
| 4 | Child primary trade relation contract | Confirm the current generated top-level template exposes financialOrchestrationDropshipPrimaryTradeRelations and resolve the parent header, selling business unit, and receiving trade organization before preparing the child row |
| 5 | Child primary trade relation correction contract | Confirm the current generated update template exposes child `PATCH`, `UniqueId`, `PrimaryTradeRelationNumber`, `EffectiveStartDate`, `EffectiveEndDate`, `OperationType`, `ParentEffectiveStartDate`, `ParentEffectiveEndDate`, and `effectiveOf`; resolve the exact child and parent range before preparing a correction |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| drop_ship_primary_trade_relations_create_contract | Registered Data Loader discriminator, configured child resource, and current create contract | Yes | Every create request | Ready | Live Data Loader metadata confirms top-level discriminator financialOrchestrationManageDropshipAgreements; the configuration screenshot confirms child resource financialOrchestrationDropshipPrimaryTradeRelations, financialOrchestrationManageDropshipAgreements.dat, ORA_FSCM_REST, required EffectiveStartDate, AgreementNumber, Priority, SupplierOwnershipChangeEventId, fixed AgreementType and Status values, and the optional fields | | A create request must use the registered top-level discriminator, retain the configured child resource, and use the current generated Data Loader contract | Generate and review the current editable sample and attribute-details workbook before preparing the source | EffectiveStartDate, AgreementNumber, Priority, SupplierOwnershipChangeEventId; AgreementType=DROP_SHIP; Status=DRAFT; optional EffectiveEndDate, SupplierOwnershipEventName, QualifierRuleSetName, Description |
| drop_ship_agreement_name_available | No existing agreement has the requested AgreementNumber | Yes | Every create request | Lookup | Complete exact AgreementNumber search in the target Fusion environment | resolve_drop_ship_name_availability | Agreement names must be unique, including agreements with another status or effective period | Supply a different name if any exact match exists; stop if the lookup cannot establish availability | Zero exact matches before source preparation |
| drop_ship_header_update_contract | Registered Data Loader discriminator and current header update contract | Yes | Every supported header update | Ready | Live Data Loader metadata confirms the top-level discriminator financialOrchestrationManageDropshipAgreements and RestAction=PATCH in the update template; the user confirms AgreementId from the exact AgreementNumber lookup identifies the existing header and CustomParentKey remains blank | | A header update must use the registered top-level discriminator, RestAction=PATCH, AgreementNumber, AgreementId, and the changed value exposed by the current live template | Generate and review the current update sample before preparing the source | AgreementNumber; AgreementId; CustomParentKey blank; RestAction=PATCH; SupplierOwnershipChangeEventId=1200 or 1300 when changing the event; Status=DRAFT, ACTIVE, or CANCELLED when changing status; effectiveOf only when the live template exposes the requested effective-dated operation |
| drop_ship_primary_trade_relation_parent | Existing Drop Ship agreement header and current child template | Yes | Every child primary trade relation create request | Lookup | Exact AgreementNumber lookup and current generated child template | resolve_drop_ship_header_by_agreement_number | A child row must be linked to one existing agreement | Provide AgreementNumber, EffectiveStartDate, and EffectiveEndDate | AgreementId; CustomParentKey blank |
| drop_ship_primary_trade_relation_selling_business_unit | Selling business unit | Yes | Every child primary trade relation create request | Lookup | Exact-name business-unit LOV lookup | resolve_selling_business_unit_by_exact_name | The child requires the selling business unit's IDs and display name from one live result | Provide SellingBusinessUnitName | ToBusinessUnitId; ToLegalEntityId; SellingBusinessUnitName |
| drop_ship_primary_trade_relation_receiving_trade_organization | Receiving trade organization | Yes | Every child primary trade relation create request | Lookup | Exact-name trade-organization LOV lookup | resolve_receiving_trade_organization_by_exact_name | The child requires the receiving trade organization's IDs and display name from one live result | Provide ReceivingTradeOrganizationName | FromTradeOrganizationId; FromLegalEntityId; FromBusinessUnitId; ReceivingTradeOrganizationName |
| drop_ship_primary_trade_relation_correction_contract | Existing child identity and current child update template | Yes | Every child primary trade relation correction request | Lookup | Expanded parent-child lookup and current generated update template | resolve_drop_ship_primary_trade_relations_by_agreement_number | A correction must target one returned child, retain its current effective range as the correction scope, and carry the resolved parent range | Provide PrimaryTradeRelationNumber or UniqueId and requested replacement dates | AgreementId; selected child identity; RestAction=PATCH; OperationType=Correct; ParentEffectiveStartDate; ParentEffectiveEndDate; effectiveOf=RangeMode=CORRECTION with returned child start/end |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The registered business object and current create contract are confirmed | No |
| Blocked | A required create field or the current Data Loader contract is missing | No |
| Lookup | An exact declared LOV lookup must resolve the requested business-unit or trade-organization name | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.DSF.CONFIRM-LOADER-READINESS | step | 4 | resolve_dependency | ready->RETURN-SUCCESS;incomplete->RETURN-ISSUES | FOS.DSF.APPLY-CREATE-DEFAULTS, FOS.DSF.CHECK-NAME-AVAILABLE | stop | Every agreement header create request |
| FOS.DSF.CONFIRM-HEADER-UPDATE-READINESS | step | 6 | resolve_dependency | ready->RETURN-UPDATE-SUCCESS;incomplete->RETURN-ISSUES | FOS.DSF.RESOLVE-HEADER-SURROGATE | stop | Every supported header update |
| FOS.DSF.CONFIRM-CHILD-CREATE-READINESS | step | 9 | resolve_dependency | ready->RETURN-CHILD-CREATE-SUCCESS;incomplete->RETURN-ISSUES | FOS.DSF.RESOLVE-RECEIVING-TRADE-ORGANIZATION | stop | Every child primary trade relation create request |
| FOS.DSF.CONFIRM-CHILD-CORRECTION-READINESS | step | 11 | resolve_dependency | ready->RETURN-CHILD-CORRECTION-SUCCESS;incomplete->RETURN-ISSUES | FOS.DSF.RESOLVE-CHILD-SURROGATE | stop | Every child primary trade relation correction request |
