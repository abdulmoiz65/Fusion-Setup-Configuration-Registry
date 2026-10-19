# Input Validation

Source: developer-provided Data Loader business-object configuration screenshot and field contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Registered Data Loader discriminator | financialOrchestrationManageDropshipAgreements | Stop before source preparation | Confirm the selected top-level Data Loader discriminator matches the current live template | Always | |
| Configured child resource | financialOrchestrationDropshipPrimaryTradeRelations | Stop before source preparation | Retain the configured child resource identity; do not substitute it for the top-level Data Loader discriminator | Always | |
| Current Data Loader contract | Current editable sample and attribute-details workbook for financialOrchestrationManageDropshipAgreements | Stop before preview | Generate and review the current sample through core.data-loader; use only fields and operations it exposes | Every create request | |
| Required create inputs | EffectiveStartDate, AgreementNumber, Priority, SupplierOwnershipChangeEventId | Stop before preview | Provide every required field using the current Data Loader contract | Every create request | |
| Unique agreement name | AgreementNumber | Stop before preview | Search the current Fusion environment for the exact AgreementNumber before creating; proceed only when no agreement with that name exists | Every create request | resolve_drop_ship_name_availability |
| Required defaulted fields | AgreementType, Status | Stop before preview | Apply the documented fixed defaults; do not accept a conflicting override | Every create request | |
| Optional create fields | EffectiveEndDate, SupplierOwnershipEventName, QualifierRuleSetName, Description | Continue without an omitted optional field | When QualifierRuleSetName is supplied, resolve it through the declared exact-name LOV lookup and populate QualifierRuleSetId | Every create request | resolve_qualifier_rule_set_by_exact_name |
| Header update identifier | AgreementId | Stop before preview | Populate AgreementId from the exact AgreementNumber lookup for the existing agreement header; leave CustomParentKey blank | Every supported header update | |
| Immutable agreement name | AgreementNumber | Stop before preview | Keep AgreementNumber exactly equal to the returned name of the existing AgreementId; reject a rename request | Every supported header update | resolve_drop_ship_header_by_agreement_number |
| Header event update value | SupplierOwnershipChangeEventId | Stop before preview | Supply 1200 for ASN From Supplier or 1300 for AP Invoice Match | Every supplier ownership-change-event header update | |
| Header status update LOV | Status | Stop before preview | Accept only `DRAFT`, `ACTIVE`, or `CANCELLED` from `FOS_AGREEMENT_STATUS` | Every header status update | |
| Header update operation | RestAction=PATCH | Stop before preview | Use only the live Data Loader update operation | Every supported header update | |
| Header effective-of correction range | effectiveOf=RangeMode=CORRECTION;RangeStartDate={supplied start};RangeEndDate={supplied end} | Stop before preview | Set a user-supplied correction range exactly when the selected live template requires an effective-dated correction; do not infer dates or another mode | Every effective-dated correction header update | |
| Header end-date operation | AgreementOperation=EndDate, EffectiveStartDate, and a new EffectiveEndDate | Stop before preview | Resolve the header first. Set effectiveOf=RangeMode=END_DATE;RangeStartDate={existing header start};RangeEndDate={existing header end}; send the requested replacement only in EffectiveEndDate. | Every end-date request | |
| Child primary trade relation create identifiers | AgreementNumber and AgreementId for the existing Drop Ship agreement header | Stop before preview | Resolve the exact AgreementNumber lookup, populate AgreementId, and leave CustomParentKey blank | Every child primary trade relation create request | resolve_drop_ship_header_by_agreement_number |
| Child primary trade relation correction identifiers | AgreementNumber, AgreementId, and one returned child identity (`UniqueId` or `PrimaryTradeRelationNumber`) | Stop before preview | Resolve the exact parent and expand its child relations; use only the requested returned child identity and leave CustomParentKey blank | Every child primary trade relation correction request | resolve_drop_ship_primary_trade_relations_by_agreement_number |
| Child primary trade relation dates | EffectiveStartDate and EffectiveEndDate | Stop before preview | Provide both dates from the requested child relation | Every child primary trade relation create request | |
| Child primary trade relation effective-date correction | RestAction=PATCH, OperationType=Correct, replacement EffectiveStartDate/EffectiveEndDate, ParentEffectiveStartDate, ParentEffectiveEndDate, and `effectiveOf=RangeMode=CORRECTION;RangeStartDate={existing child start};RangeEndDate={existing child end}` | Stop before preview | Resolve the child and parent first; populate ParentEffectiveStartDate and ParentEffectiveEndDate from the returned header range, keep the returned child range in effectiveOf, and place replacement dates only in the payload | Every child primary trade relation correction request | resolve_drop_ship_primary_trade_relations_by_agreement_number |
| Selling business unit | SellingBusinessUnitName | Stop before preview | Resolve the exact-name business-unit LOV and populate ToBusinessUnitId, ToLegalEntityId, and SellingBusinessUnitName from its one result | Every child primary trade relation create request | resolve_selling_business_unit_by_exact_name |
| Receiving trade organization | ReceivingTradeOrganizationName | Stop before preview | Resolve the exact-name trade-organization LOV and populate FromTradeOrganizationId, FromLegalEntityId, FromBusinessUnitId, and ReceivingTradeOrganizationName from its one result | Every child primary trade relation create request | resolve_receiving_trade_organization_by_exact_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business-object identity | Require top-level discriminator financialOrchestrationManageDropshipAgreements and retain child resource financialOrchestrationDropshipPrimaryTradeRelations; stop if either identity is substituted | Always | |
| Required create inputs | Require EffectiveStartDate, AgreementNumber, Priority, and SupplierOwnershipChangeEventId | Every create request | |
| Duplicate agreement name | Require a successful exact AgreementNumber search in the target environment with zero matching agreements before preparing a create source; treat a failed or incomplete lookup as blocking | Every create request | resolve_drop_ship_name_availability |
| Supplier ownership-change event | Accept 1200 for ASN From Supplier or 1300 for AP Invoice Match; reject every other value | Every create request | |
| Fixed header defaults | Require AgreementType=DROP_SHIP and Status=DRAFT; reject a conflicting supplied value | Every create request | |
| Optional create fields | Allow EffectiveEndDate, SupplierOwnershipEventName, QualifierRuleSetName, and Description to remain omitted. When QualifierRuleSetName is supplied, require one exact LOV match and send its QualifierRuleSetId. | Every create request | resolve_qualifier_rule_set_by_exact_name |
| Header update | Require AgreementNumber, AgreementId, RestAction=PATCH, and at least one supported changed value other than AgreementNumber from the current live template; the exact AgreementNumber lookup must return the same AgreementId. Reject any attempt to change AgreementNumber; leave CustomParentKey blank | Every supported header update | resolve_drop_ship_header_by_agreement_number |
| Header status update | Require Status to be one of `DRAFT`, `ACTIVE`, or `CANCELLED`; do not infer any other `FOS_AGREEMENT_STATUS` code | Every header status update | |
| Header effective-of correction range | Require the supplied effectiveOf correction range exactly when the selected live template requires an effective-dated correction | Every effective-dated correction header update | |
| Header end date | Require AgreementOperation=EndDate, EffectiveStartDate from the exact header lookup, and a user-supplied new EffectiveEndDate; use the existing header start and existing header end as the effectiveOf range | Every end-date request | |
| Child selling business unit | Require SellingBusinessUnitName. Populate ToBusinessUnitId, ToLegalEntityId, and SellingBusinessUnitName only from the declared exact-name business-unit LOV lookup | Every child primary trade relation create request | resolve_selling_business_unit_by_exact_name |
| Child receiving trade organization | Require ReceivingTradeOrganizationName. Populate FromTradeOrganizationId, FromLegalEntityId, FromBusinessUnitId, and ReceivingTradeOrganizationName only from the declared exact-name trade-organization LOV lookup | Every child primary trade relation create request | resolve_receiving_trade_organization_by_exact_name |
| Unsupported operation | Stop before preparation; this resource supports documented agreement-header create/update/end-date actions and child primary trade relation create/correction only | Any child-record end-date, delete, insert, or other operation; or a correction missing the live-template effective-date scope | |
| Undocumented request field or operation | Stop; do not infer a field mapping, request body, POST or PATCH route, or action name | A supplied field or operation is absent from the current contract | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.DSF.VALIDATE-CONTRACT-SOURCE | step | 1 | validate_input | create_valid->FOS.DSF.CHECK-NAME-AVAILABLE;update_valid->FOS.DSF.RESOLVE-HEADER-SURROGATE;child_create_valid->FOS.DSF.RESOLVE-HEADER-SURROGATE;child_correction_valid->FOS.DSF.RESOLVE-HEADER-SURROGATE;invalid->RETURN-ISSUES | none | stop | Every supported agreement-header, child-create, or child-correction request |
