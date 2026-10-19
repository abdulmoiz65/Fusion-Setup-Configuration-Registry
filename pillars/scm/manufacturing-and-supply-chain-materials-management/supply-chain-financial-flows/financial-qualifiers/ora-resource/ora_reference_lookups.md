# Reference Lookups

Use the configured Fusion `restBaseUrl` with every relative REST path below.
All lookups are read-only and must send
`REST-Framework-Version: 9`. Use the returned stored code, not a display
meaning, in the Data Loader source.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_financial_orchestration_business_flow_type | A business process type is supplied | Business process type display value | /fscmRestApi/resources/latest/financialOrchestrationBusinessFlowTypesLOV?fields=LookupCode%2CMeaning&finder=findByLookupType%3BbindLookupType%3DORA_FOS_AGREEMENT_TYPE_FOR_VAL%2Cbprofileoption%3DORA_FOS_EXTERNAL_TRADE_EVENTS&onlyData=true | LookupCode, Meaning | Match the supplied display value or code to exactly one returned record | AgreementType and AgreementTypeSearch: LookupCode | Zero or multiple matches: stop and request an exact supported business process type. |
| resolve_financial_orchestration_user_catalog | A user defined catalog is supplied or required | Catalog code, category-set name, or category-set ID | /fscmRestApi/resources/latest/financialOrchestrationUserCatalogsLOV?fields=CatalogCode%2CCatalogContentCode%2CCategorySetName%2CCategorySetId%2CDescription&onlyData=true&limit=25&offset=0 | CatalogCode, CatalogContentCode, CategorySetName, CategorySetId, Description | Require one exact catalog code, category-set name, or ID match | UserDefCategorySetId: CategorySetId | Zero or multiple matches: stop and request the exact catalog or category set. |
| resolve_financial_orchestration_parameter | Procurement parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=GpQualifierFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_parameter | Shipment parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=ShipmentQualifierFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_parameter | Dropship parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=DropShipQualifierFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_parameter | External Trade parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=ExternalTradeFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_parameter | Internal Transfer parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=ImtQualifierFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match; when B2B is disabled, exclude `BACK_TO_BACK` | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_parameter | Nonshippable Sales parameter is supplied | Parameter display value or code | /fscmRestApi/resources/latest/financialOrchestrationParametersLOV?fields=QualifierCode%2CQualifierMeaning&onlyData=true&q=ServiceSalesQualifierFlag%3D%27Y%27&limit=25&offset=0 | QualifierCode, QualifierMeaning | Require exactly one QualifierCode or QualifierMeaning match | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning | Zero or multiple matches: stop and request the exact parameter. |
| resolve_financial_orchestration_operator | A qualifier operator is supplied | Operator display value or code | /fscmRestApi/resources/latest/standardLookupsLOV?fields=LookupCode%2CMeaning&onlyData=true&q=LookupType%3D%27FOS_QUALIFIER_OPERATORS%27&limit=25&offset=0 | LookupCode, Meaning | Require exactly one operator code or meaning match | qualifierRules.QualifierOperator: LookupCode | Zero or multiple matches: stop and request the exact operator. |
| resolve_financial_orchestration_conjunction | A rule has more than one condition and a conjunction is supplied | Conjunction display value or code | /fscmRestApi/resources/latest/standardLookupsLOV?fields=LookupCode%2CMeaning&onlyData=true&q=LookupType%3D%27FOS_CONJUNCTION%27&limit=25&offset=0 | LookupCode, Meaning | Require exactly one response record matching the supplied code or meaning; do not infer a conjunction when no second condition exists | qualifierRules.Conjunction: LookupCode | Zero or multiple matches: stop and request the exact conjunction or omit it for a single-condition rule. |
| check_financial_orchestration_qualifier_delete_eligibility | A specific qualifier is requested for deletion | QualifierRuleSetId or the selected exact QualifierRuleSetName | /fscmRestApi/resources/latest/financialOrchestrationQualifiers?fields=QualifierRuleSetId%2CQualifierRuleSetName%2CAgreementTypeMeaning%2CAgreementType%2CDescription%2CCategorySetName%2CUsedInFlow%2CFlowCount%2CLastUpdateDateTime%2CRuleText%2CCreatedBy%2CCreationDate%2CLastUpdatedBy%2CUserDefCategorySetId&q=%28UPPER%28QualifierRuleSetName%29%20LIKE%20UPPER%28%27%25{search_term}%25%27%29%20OR%20UPPER%28Description%29%20LIKE%20UPPER%28%27%25{search_term}%25%27%29%29&limit=25&offset=0 | QualifierRuleSetId, QualifierRuleSetName, UsedInFlow, FlowCount | Select one exact qualifier by ID or exact name from the returned candidates, then allow delete only when UsedInFlow is JSON null | QualifierRuleSetId, QualifierRuleSetName, UsedInFlow, delete eligibility | Zero or multiple exact candidates, an unreadable UsedInFlow property, or any UsedInFlow value other than JSON null: stop and do not prepare or submit a delete. |

## Parameter-Specific Rule Value LOVs

The Redwood qualifier-rule layout determines the value source from the resolved
`QualifierCode`, not from the business-flow label. Match a single result and
store the indicated code or identifier in `qualifierRules.Value`.

| QualifierCode | Value source | Requested fields | Stored value |
|---|---|---|---|
| `SHIP_FROM_ORG`, `SHIP_TO_ORG` | `financialOrchestrationItemOrganizationsLOV` | `OrganizationCode,OrganizationName` | `OrganizationCode` |
| `FOS_CATEGORY` | `financialOrchestrationCategoriesLOV?q=FunctionalAreaId=32` | `CategoryName,CategoryId` | `CategoryId` |
| `PURCHASE_CATEGORY` | `financialOrchestrationCategoriesLOV?q=FunctionalAreaId=2` | `CategoryName,CategoryId` | `CategoryId` |
| `SUPPLIER_SITE_CODE` | `financialOrchestrationQualifierSupplierSitesLOV` | `VendorSiteCode` | `VendorSiteCode` |
| `ITEM_NUMBER` | `financialOrchestrationQualifierItemNumbersLOV` | `ItemNumber,InventoryItemId` | `InventoryItemId` |
| `ITEM_CLASS` | `itemClasses` | `ItemClass,Description,ItemCreationAllowedFlag,ItemClassCode,ItemClassId` | `ItemClassId` |
| `DESTINATION_TYPE` with `INTERNAL_TRANSFER` | `standardLookupsLOV?q=LookupType='ORA_INV_TO_DESTINATION_TYPE'` | `LookupCode,Meaning` | `LookupCode` |
| `DESTINATION_TYPE` for every other flow | `financialOrchestrationDestinationTypesLOV` | `LookupCode,DisplayedField` | `LookupCode` |
| `SOLD_TO_PARTY`, `SHIP_TO_PARTY`, `BILL_TO_PARTY` | `financialOrchestrationPartiesLOV` | `PartyName,PartyId,PartyNumber,PartyType` | `PartyId` |
| `SHIP_TO_ADDRESS` | `financialOrchestrationShipToAddressesLOV` | `PartySiteNumber,LocationId,PartySiteName,PartyName,FormattedAddress` | `LocationId` |
| `ORDER_TYPE` | `standardLookupsLOV?q=LookupType='ORA_DOO_ORDER_TYPES'` | `LookupCode,Meaning` | `LookupCode` |
| `USER_DEFINED_CATEGORY` | `financialOrchestrationUserDefinedCategoriesLOV?q=CategorySetId=<UserDefCategorySetId>` | `CategorySetName,CategoryId,CategoryCode,CategoryName,Description` | `CategoryId` |
| `ORDER_MANAGEMENT_BU` | `financialOrchestrationOrderManagementBusinessUnitsLOV` | `BUName,LegalEntityId,BUId` | `BUId` |
| `PROJECT_NUMBER` | `financialOrchestrationProjectNumbersLOV` | `ProjectCode,Name,ProjectId` | `ProjectId` |
| `INVENTORY_ASSET_FLAG`, `BACK_TO_BACK` | `standardLookupsLOV?q=LookupType='YES_NO'` | `LookupCode,Meaning` | `LookupCode` |
| `SUPPLIER` | `financialOrchestrationSuppliersLOV` | `PartyName,VendorCode,BusinessRelationship,DUNSNumber` | `VendorCode` |
| `SUPPLIER_COUNTRY`, `SHIP_TO_COUNTRY`, `SOLD_TO_COUNTRY`, `BILL_TO_COUNTRY`, `COUNTRY_OF_ORIGIN` | `financialOrchestrationCountryOfOriginsLOV` | `CurrencyCode,Description,TerritoryShortName,TerritoryCode` | `TerritoryCode` |
| `ITEM_TYPE` | `standardLookupsLOV?q=LookupType='EGP_ITEM_TYPE'` | `LookupCode,Meaning` | `LookupCode` |
| `FOS_HEADER_ATTRIBUTE1` through `FOS_HEADER_ATTRIBUTE5`; `FOS_LINE_ATTRIBUTE1` through `FOS_LINE_ATTRIBUTE15` | Free text | N/A | The entered text |

All non-free-text sources above use this request shape:

```text
/fscmRestApi/resources/latest/<resource>?fields=<encoded-fields>&onlyData=true[&q=<encoded-filter>]&limit=25&offset=0
```

## Rule Value Examples

| Use when | LOV path | Store in Data Loader |
|---|---|---|
| The parameter uses a YES/NO value | `/fscmRestApi/resources/latest/standardLookupsLOV?fields=LookupCode%2CMeaning&onlyData=true&q=LookupType%3D%27YES_NO%27&limit=25&offset=0` | Matching `LookupCode` in `qualifierRules.Value` |
| The parameter uses a ship-from organization | `/fscmRestApi/resources/latest/financialOrchestrationItemOrganizationsLOV?fields=OrganizationCode%2COrganizationName&onlyData=true&limit=25&offset=0` | Matching `OrganizationCode` in `qualifierRules.Value` |

For the verified Asset Item condition, the YES/NO LOV maps display value `No`
to stored code `N`.

## Operator and Conjunction LOVs

Resolve operators through:

```text
/fscmRestApi/resources/latest/standardLookupsLOV?fields=LookupCode%2CMeaning&onlyData=true&q=LookupType%3D%27FOS_QUALIFIER_OPERATORS%27&limit=25&offset=0
```

For example, `Equals` maps to `EQUAL_TO`. Resolve conjunctions only when the
rule has more than one condition through:

```text
/fscmRestApi/resources/latest/standardLookupsLOV?fields=LookupCode%2CMeaning&onlyData=true&q=LookupType%3D%27FOS_CONJUNCTION%27&limit=25&offset=0
```

The Redwood page uses lookup type `FOS_CONJUNCTION`; populate
`qualifierRules.Conjunction` with its returned `LookupCode`.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A requested display value has no single LOV match | Stop before source preparation and request the exact value. |
| A value LOV returns a different stored code | Use the code in the Data Loader field; retain the meaning only as display evidence. |
| No condition is supplied | Stop: Fusion requires at least one `qualifierRules` child row. |
| Category-set fields are selected for payload exclusion | Leave `CategorySetId` and `CategorySetName` blank; validate the generated source before approval. |
| A delete is requested | Permit it only after check_financial_orchestration_qualifier_delete_eligibility returns UsedInFlow as JSON null. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FOS.FQ.RESOLVE_BUSINESS_FLOW | step | 15 | reference_lookup | resolved->FOS.FQ.RESOLVE_USER_CATALOG;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.VALIDATE_INPUT | stop | A business process type is supplied |
| FOS.FQ.RESOLVE_USER_CATALOG | step | 16 | reference_lookup | resolved->FOS.FQ.RESOLVE_PARAMETER;not-applicable->FOS.FQ.RESOLVE_PARAMETER;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.RESOLVE_BUSINESS_FLOW | stop | A user defined catalog is supplied or required by the Data Loader REST schema |
| FOS.FQ.RESOLVE_PARAMETER | step | 17 | reference_lookup | resolved->FOS.FQ.RESOLVE_OPERATOR;not-applicable->FOS.FQ.RESOLVE_OPERATOR;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.RESOLVE_USER_CATALOG | stop | A qualifier parameter is supplied |
| FOS.FQ.RESOLVE_OPERATOR | step | 18 | reference_lookup | resolved->FOS.FQ.RESOLVE_CONJUNCTION;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.RESOLVE_PARAMETER | stop | A qualifier operator is supplied |
| FOS.FQ.RESOLVE_CONJUNCTION | step | 19 | reference_lookup | resolved->FOS.FQ.CHECK_EXECUTION_CONTRACT;not-applicable->FOS.FQ.CHECK_EXECUTION_CONTRACT;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.RESOLVE_OPERATOR | stop | A conjunction is supplied |
| FOS.FQ.CHECK_DELETE_ELIGIBILITY | step | 21 | reference_lookup | allowed->FOS.FQ.DONE;not-applicable->FOS.FQ.DONE;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.CHECK_EXECUTION_CONTRACT | stop | A qualifier delete is requested |
