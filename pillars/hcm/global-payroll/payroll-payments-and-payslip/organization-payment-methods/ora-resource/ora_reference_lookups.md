# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_payment_source_rule_date_overlap | Before create or update design validation when PaymentMethodRule rows are proposed | Proposed rule rows and verified existing rule date ranges for the same OPM; resolved Payment Source identity, rule identity, DefaultFlag, EffectiveStartDate, EffectiveEndDate | Compare distinct rules under the same OPM and exact Payment Source identity in the resulting proposed state; do not compare an updated row against its own superseded version. Normalize dates to date values and use inclusive ranges. An omitted EffectiveEndDate means the documented end of time; a missing or invalid start date or an invalid range is unresolved. A conflict exists only when at least one rule has DefaultFlag Y and max(first start, second start) is on or before min(first end, second end). Evaluate the entire proposed effective range, including defaults that begin after the proposed start; checking only today's date or the first day is insufficient | Conflicting rule pairs and their overlap start/end dates, or verified no overlap; date-range completeness evidence | Zero overlapping pairs with complete evidence permits reuse in disjoint periods; retain every overlapping pair for the design blocker. Missing, ambiguous, or incomplete existing date-range evidence blocks validation; a current-date snapshot alone cannot prove no overlap. New-parent same-archive requests use all proposed rows and require no existing-parent lookup |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| check_organization_payment_method_duplicate | Before create preview | EffectiveStartDate, OrganizationPaymentMethodName, LegislativeDataGroupId from resolve_ldg_by_exact_name | /hcmRestApi/resources/latest/organizationPaymentMethodsLOV?effectiveDate=<EffectiveStartDate>&q=OrgPaymentMethodName='<OrganizationPaymentMethodName>' and LegislativeDataGroupId=<LegislativeDataGroupId> | OrgPaymentMethodName, LegislativeDataGroupId, CurrencyCode, PaymentTypeName, EffectiveStartDate | Match the supplied OPM name exactly within the resolved LegislativeDataGroupId as of EffectiveStartDate; zero matching items permits create preview; one or more matching items within that LDG blocks the create request | Existing organization payment method state within the resolved LDG | Stop when one or more matches within the resolved LDG are returned; stop on lookup failure |
| resolve_ldg_by_exact_name | LegislativeDataGroupName is supplied and LegislativeDataGroupId or LegislationCode is needed | LegislativeDataGroupName | GET /hcmRestApi/resources/latest/legislativeDataGroupsLOV | LegislativeDataGroupId, Name, LegislationCode | Match the supplied LDG name exactly against Name and require exactly one result | LegislativeDataGroupId: resolved LDG ID; Name: LDG display name used for the exact match; LegislationCode: resolved legislation code | Zero results: report LegislativeDataGroupName and invalid value; multiple results: report ambiguity and require a more precise LDG value |
| resolve_currency_by_exact_display | A currency name or display value is supplied instead of CurrencyCode | Currency name or display value | GET /fscmRestApi/resources/latest/currenciesLOV | CurrencyCode, Name | Match the supplied currency name or display value exactly against Name and require exactly one result | CurrencyCode: resolved currency code; Name: currency display name used for the exact match | Zero results: report the Currency field and invalid value; multiple results: report ambiguity and don't select automatically |
| resolve_payment_type_by_legislation | A payment-type name or display value is supplied, or PaymentTypeCode or PaymentTypeId is needed | Payment type name or display value, LegislationCode from resolve_ldg_by_exact_name | GET /hcmRestApi/resources/latest/paymentTypesLOV?finder=findByLegislationCode;LegislationCode=<LegislationCode> | BasePaymentTypeName, PaymentTypeName, BasePaymentTypeId, Category, LegislationCode | Restrict results to the LegislationCode resolved from the LDG; then match the supplied payment-type name or display value exactly against PaymentTypeName and require exactly one result | PaymentTypeCode: BasePaymentTypeName; PaymentTypeName: matched display name; PaymentTypeId: BasePaymentTypeId | Zero results: report Payment Type, invalid value, and legislation; multiple results: report ambiguity and don't select automatically |
| derive_payment_category_by_payment_type | Category is required for field applicability or Payment Type changes | Payment type display value, PaymentTypeCode or PaymentTypeId, LegislationCode from resolve_ldg_by_exact_name | GET /hcmRestApi/resources/latest/paymentTypesLOV?finder=findByLegislationCode;LegislationCode=<LegislationCode> | BasePaymentTypeName, PaymentTypeName, BasePaymentTypeId, Category, LegislationCode | Restrict results to the LDG-derived LegislationCode; match the selected payment type exactly by its validated BasePaymentTypeName, BasePaymentTypeId, or PaymentTypeName display value and require exactly one result | Category: category returned for the selected payment type; PaymentTypeName: matched display name | Zero results: stop and report Payment Type plus legislation; multiple results: report ambiguity and don't derive Category automatically |
| resolve_legal_employer_names_by_ldg | BankAccountName or BankAccountId must be resolved for a PaymentSource | LegislativeDataGroupId | POST /hcmRestApi/resources/latest/organizationPaymentMethods/action/getLegalEntityNames with body {"ldgId":"<LegislativeDataGroupId>"}; Content-Type: application/vnd.oracle.adf.action+json | Response key-value pairs; values are legal employer names | Accept values from the key-value response only for the supplied LegislativeDataGroupId | LegalEmployerNames: response values used as the bankAccounts query scope | Zero legal employers: stop bank-account resolution and report the LDG; duplicate returned values: de-duplicate identical legal-employer names within this operation before the bank-account query |
| resolve_bank_account_by_legal_employer | A bank-account name is supplied instead of BankAccountId, after legal-employer names are resolved | BankAccountName, LegalEmployerNames, EffectiveStartDate | GET /api/boss/data/objects/ora/erpCore/bankingSetup/v1/bankAccounts?$fields=name,startDate,endDate,payrollUseAllowedFlag,bank.name,bankBranch.name,bankBranch.branchNumber,accountNumber,bank.countryCode&$filter=legalEntity.legalEntityName IN (<LegalEmployerNames>) AND payrollUseAllowedFlag=true | items[].name, items[].startDate, items[].endDate, items[].payrollUseAllowedFlag, items[].accountNumber, items[].$id, items[].$context.etag, items[].bank.name, items[].bank.countryCode, items[].bank.$id, items[].bank.$context.etag, items[].bankBranch.name, items[].bankBranch.branchNumber, items[].bankBranch.$id, items[].bankBranch.$context.etag, hasMore | Replace <LegalEmployerNames> with the deduplicated names returned by resolve_legal_employer_names_by_ldg as individually quoted filter values; require payrollUseAllowedFlag=true; match BankAccountName exactly to items[].name and require exactly one account; confirm its Payroll use and active date range using Bank Account Identity and Activity Verification below; complete the declared metadata and detail reads if a successful identity response lacks status evidence | BankAccountId: matched items[].$id; BankAccountName: matched items[].name; Active status for the effective date, startDate, endDate and Payroll use: lookup evidence only | Zero results: report Bank Account and invalid name; multiple results: report ambiguity and don't select an account automatically; inactive or Payroll-ineligible account: stop before preview; identity-only success: complete the declared status reads before reporting a verification gap |
| resolve_tax_reporting_unit_by_ldg | TaxReportingUnitName is supplied for a PaymentMethodRule | LegislativeDataGroupId, TaxReportingUnitName | POST /hcmRestApi/resources/latest/organizationPaymentMethods/action/getTaxReportingUnits with body {"ldgId":"<LegislativeDataGroupId>"}; Content-Type: application/vnd.oracle.adf.action+json | Response key-value pairs; key is TaxReportingUnitId and value is TaxReportingUnitName | Match TaxReportingUnitName exactly against returned values and require exactly one pair | TaxReportingUnitId: matched response key; TaxReportingUnitName: matched response value | Zero results: report Tax Reporting Unit and invalid value; multiple results: report ambiguity and don't select automatically |
| resolve_payment_source_report_category_by_ldg | A worker or third-party-payee report-category name is supplied | LegislativeDataGroupId from resolve_ldg_by_exact_name, report-category name, report-category role | GET /hcmRestApi/resources/latest/paymentSourceReportCategoriesLOV?finder=findByLegislativeDataGroup;LegislativeDataGroupId=<LegislativeDataGroupId> | ReportCategoryId, CategoryName | Match the supplied category name exactly against CategoryName within the LDG and require exactly one result; retain whether the input is for workers or third-party payees | WorkerReportCategoryId: ReportCategoryId for worker input; ThirdPartyReportCategoryId: ReportCategoryId for third-party-payee input; CategoryName: matched display name | Zero results: report the applicable report-category field and invalid value; multiple results: report ambiguity and don't select automatically |
| resolve_third_party_payment_method_by_opm | A third-party name is supplied for a PaymentMethodRule | OrganizationPaymentMethodId, third-party name | GET /hcmRestApi/resources/latest/thirdPartyPersonPaymentMethods?finder=findByFilterCriteria;OrganizationPaymentMethodId=<OrganizationPaymentMethodId> | PartyId, PartyName | Restrict results to the resolved OrganizationPaymentMethodId; match the supplied third-party name exactly against PartyName and require exactly one result | ThirdPartyId: PartyId; PartyName: matched display name | Zero results: report Third-Party Name and invalid value; multiple results: report ambiguity and don't select automatically |
| resolve_opm_by_exact_name_for_physical_delete | A permanent PaymentMethodRule deletion is requested using an OPM name | LegislativeDataGroupId, OrganizationPaymentMethodName, SysEffectiveDate | GET /hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByFilterCriteria;LegislativeDataGroupId=<LegislativeDataGroupId>,SysEffectiveDate=<SysEffectiveDate> | OrgPaymentMethodId, OrgPaymentMethodName, LegislativeDataGroupId, EffectiveStartDate, EffectiveEndDate, paging metadata | Consume all pages; match OrganizationPaymentMethodName exactly within the supplied LDG and require exactly one result | OrgPaymentMethodId: matched ID; OrganizationPaymentMethodName: matched name; effective-date evidence | Zero results: stop and report the OPM name; multiple exact matches: stop and report ambiguity without selecting one |
| resolve_payment_method_rule_for_physical_delete | A permanent PaymentMethodRule deletion target must be confirmed under a resolved OPM | OrgPaymentMethodId, SysEffectiveDate | GET /hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByOrgPayMethodId;OrgPaymentMethodId=<OrgPaymentMethodId>,SysEffectiveDate=<SysEffectiveDate>&expand=paymentMethodRules,additionalDetails,paymentMethodRules.additionalDetails | OrgPaymentMethodId, paymentMethodRules, paymentMethodRules.additionalDetails, EffectiveStartDate, EffectiveEndDate, PaymentMethodRuleId or OrgPayerMappingId, PaymentSourceId or applicable returned source identifier, DefaultValue, paging metadata | Consume all pages; retain only rules active for SysEffectiveDate and require exactly one active rule; preserve its returned rule, source, and effective-date identifiers | PaymentMethodRuleId; PaymentSourceId; EffectiveStartDate; EffectiveEndDate; DefaultFlag; logical-date evidence | Zero active rules: stop and report no delete target; multiple active rules: stop and require the user to identify one rule; any unresolved returned identifier: stop without DAT generation |

## BOSS Service Authentication Contract

This supplemental contract applies to the BOSS bank-account resolver and does not replace any existing lookup, endpoint, or error-handling instruction.

| Endpoint Class | Endpoint | Required Authentication | Prohibited Authentication | Behavior |
|---|---|---|---|---|
| BOSS service | `/api/boss/data/objects/ora/erpCore/bankingSetup/v1/bankAccounts` | Obtain and use a BOSS access token using the BOSS scope and BOSS client. | A Fusion access token by itself. | Identify the request as a BOSS service before it is invoked; select the BOSS-scoped token and stop if it is unavailable. |
| Fusion service | Non-BOSS Fusion endpoints used by this task | Obtain and use a Fusion access token using the Fusion scope and Fusion client. | Reusing the BOSS client as the Fusion client. | Obtain the Fusion-scoped client before task work and select it only for Fusion service requests. |

No authored resource, diagnostic, preview, or result may disclose either access token.

## Bank Account Identity and Activity Verification

These steps are part of resolve_bank_account_by_legal_employer and are authorized read-only dependency validation. Run all BOSS requests through core/fusion-api/rest-api-client/scripts/boss-rest_client.py with the BOSS-scoped token cache and REST-Framework-Version: 9. No separate user instruction or approval is needed for these reads. Never treat an identity match or Payroll-use filter alone as proof of activity.

| Sequence | Applies When | Request or Check | Required Evidence or Outcome |
|---|---|---|---|
| 1 | Before selecting bank-account status fields for the current validation run | GET /api/boss/data/objects/ora/erpCore/bankingSetup/v1/$openapi/bankAccounts; read the bank-account item schema properties and any allOf members | Confirm name, startDate, endDate and payrollUseAllowedFlag with their live types, nullable flags and descriptions; startDate is when the account becomes active and endDate when it is no longer active; never guess an activeFlag or request $fields=* |
| 2 | The verification date is selected | Use the PaymentSource EffectiveStartDate, or its validated parent OPM EffectiveStartDate when inherited; for an explicit current-status-only query use the user's current date | A valid comparison date; do not invent a missing effective date for a create request |
| 3 | LegalEmployerNames and the live status-field contract are available | Execute the scoped collection request declared in Live Lookups and consume every page | Exactly one exact BankAccountName match within the LDG-derived legal-employer scope; retain its BankAccountId and name |
| 4 | A successful scoped response uniquely resolves identity but omits active-date or Payroll-use evidence | GET /api/boss/data/objects/ora/erpCore/bankingSetup/v1/bankAccounts/<BankAccountId>?$fields=name,startDate,endDate,payrollUseAllowedFlag, using only the ID resolved in step 3 | Returned $id and name must match the scoped account; obtain explicit startDate, endDate and payrollUseAllowedFlag fields before deciding readiness; this detail read cannot replace the legal-employer scope check |
| 5 | Identity and status fields are available | Normalize the requested YYYY/MM/DD date and returned ISO YYYY-MM-DD dates to date values; require payrollUseAllowedFlag=true; require a non-null startDate to be on or before the verification date and a non-null endDate to be after it | Account identity, Payroll use and activity all pass for the requested effective date; endDate is the date when the account is no longer active |
| 6 | A requested date field is explicitly null | Treat an explicit null as an open boundary; a null endDate means no recorded closing date | Preserve the explicit-null evidence; an absent field is not null and requires the detail read in step 4 |
| 7 | Verification succeeds | Retain the identity and active-date evidence for Task Validation and continue the existing Data Loader workflow | No repeated bank-account confirmation; never populate these lookup-only status fields in HDL |

Source: live BOSS bank-account OpenAPI field definitions verified during this session. Oracle's current metadata-access contract documents the resource-level $openapi route: https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/Access_Metadata.html.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| No matching organization payment method | Continue to the approval gate |
| One or more matching organization payment methods | Block create; require an explicit update request or a new name |
| Lookup authentication, authorization, or transport failure | Stop before preview; do not retry a write |

## BOSS Bank Account Response Field Mapping

| Response Field | Meaning | Lookup or HDL Use |
|---|---|---|
| items[].name | Bank-account display name | Compare exactly with the supplied BankAccountName and retain as the matched BankAccountName |
| items[].startDate | Date when the account becomes active | Compare with the verification date; explicit null is an open lower boundary; lookup evidence only |
| items[].endDate | Date when the account is no longer active | Require the verification date to precede a non-null endDate; explicit null means no recorded closing date; lookup evidence only |
| items[].payrollUseAllowedFlag | Whether the account is used for Payroll | Require true in addition to identity and active-date validation; lookup evidence only |
| items[].accountNumber | Bank-account number | Supporting lookup evidence only; don't substitute it for BankAccountId |
| items[].$id | Bank-account identifier | Map the uniquely matched value to BankAccountId |
| items[].$context.etag | Bank-account response version | Response metadata only; don't include it in the HDL data |
| items[].bank.name | Bank name | Supporting lookup evidence |
| items[].bank.countryCode | Bank country code | Supporting legislation and country evidence |
| items[].bank.$id | Bank identifier | Supporting lookup evidence; don't substitute it for BankAccountId |
| items[].bank.$context.etag | Bank response version | Response metadata only; don't include it in the HDL data |
| items[].bankBranch.name | Bank-branch name | Supporting lookup evidence |
| items[].bankBranch.branchNumber | Bank-branch number | Supporting lookup evidence |
| items[].bankBranch.$id | Bank-branch identifier | Supporting lookup evidence; don't substitute it for BankAccountId |
| items[].bankBranch.$context.etag | Bank-branch response version | Response metadata only; don't include it in the HDL data |
| hasMore | Pagination indicator | Continue retrieving pages until false before enforcing zero, one, or multiple exact-match behavior |

## BOSS Bank Account Sample Response

The example retains the supplied response shape while replacing environment-specific identifiers, account numbers, and ETags with placeholders.

```json
{
  "items": [
    {
      "name": "BOACheckinhAcc1",
      "accountNumber": "<bank-account-number>",
      "$id": "<bank-account-id>",
      "$context": {
        "etag": "<etag>"
      },
      "bank": {
        "name": "Bank of America1",
        "countryCode": "US",
        "$id": "<bank-id>",
        "$context": {
          "etag": "<etag>"
        }
      },
      "bankBranch": {
        "name": "Bank of America",
        "branchNumber": "<bank-branch-number>",
        "$id": "<bank-branch-id>",
        "$context": {
          "etag": "<etag>"
        }
      }
    }
  ],
  "hasMore": false
}
```

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.CHECK_DUPLICATE | decision | 4 | reference_lookup | clear->OPM.RESOLVE_PRENOTIFICATION_ENABLEMENT;exists->OPM.FAILED;failure->OPM.FAILED | OPM.VALIDATE_DEPENDENCIES | stop | Create request | check_organization_payment_method_duplicate |
| OPM.DELETE_RESOLVE_OPM | step | 121 | reference_lookup | resolved->OPM.DELETE_RESOLVE_RULE;failure->OPM.DELETE_FAILED | OPM.VALIDATE_PHYSICAL_DELETE | stop | A permanent PaymentMethodRule deletion is requested | resolve_opm_by_exact_name_for_physical_delete |
| OPM.DELETE_RESOLVE_RULE | step | 122 | reference_lookup | resolved->OPM.ENFORCE_PHYSICAL_DELETE;failure->OPM.DELETE_FAILED | OPM.DELETE_RESOLVE_OPM | stop | A permanent PaymentMethodRule deletion is requested | resolve_payment_method_rule_for_physical_delete |

## REST LOV Contract

| Contract Item | Documented Value | Runtime Use |
|---|---|---|
| Method | GET | Read-only discovery and validation only |
| Collection path | /hcmRestApi/resources/11.13.18.05/organizationPaymentMethodsLOV | Retrieve OPMs as of a specified date |
| Item path | /hcmRestApi/resources/11.13.18.05/organizationPaymentMethodsLOV/{organizationPaymentMethodsLOVUniqID} | Retrieve one OPM by its unique resource key |
| Effective-date query | effectiveDate in yyyy-MM-dd format | Retrieve rows effective as of the supplied date |
| Query filter | q supports BaseOrgPayMethodName, Category, CurrencyCode, EffectiveEndDate, EffectiveStartDate, LegislationCode, LegislativeDataGroupId, OrgPaymentMethodId, OrgPaymentMethodName, and PaymentTypeName | Narrow duplicate and reference checks |
| Field projection | fields with a comma-separated field list | Request only the fields required for validation |
| Paging | limit, offset, hasMore, and count | Continue reading until all relevant pages are evaluated |
| Mutation policy | No request body and no write operation is documented for this LOV resource | Never use this REST resource to load or mutate OPM data; use HCM Data Loader |

## LOV Response to HDL Crosswalk

| LOV Response Field | HDL Field or Validation Use |
|---|---|
| BaseOrgPayMethodName | Compare with the business or base OPM identifier when supplied |
| OrgPaymentMethodId | Existing-record identity for read-only verification; don't substitute it for the documented HDL source-key hierarchy without an approved mapping |
| OrgPaymentMethodName | OrganizationPaymentMethodName duplicate and identity validation |
| CurrencyCode | CurrencyCode combination validation |
| EffectiveStartDate | EffectiveStartDate and effective-as-of validation |
| EffectiveEndDate | EffectiveEndDate and active-range validation |
| PaymentTypeName | Validate the selected business payment type display value |
| BasePaymentTypeName | Map the resolved value to PaymentTypeCode |
| BasePaymentTypeId | Map the resolved value to PaymentTypeId |
| Category | Read-only payment category, such as cash, check, or electronic transfer |
| LegislationCode | Country-specific rule selection |
| LegislativeDataGroupId | Validate the LDG identity associated with the OPM |

The LOV endpoint is a read-only reference source. It never replaces HCM Data Loader as the Organization Payment Methods load route.

The two custom actions above are read-only value-discovery operations even though they use POST. They must not create or update Organization Payment Methods, legal employers, bank accounts, or tax reporting units.

## Reference Resolution Order

| Sequence | Reference Value | Required Resolution |
|---|---|---|
| 1 | Legislative data group | Resolve LegislativeDataGroupId and LegislationCode from an exact LegislativeDataGroupName |
| 2 | Currency | Resolve CurrencyCode when a currency display value is supplied |
| 3 | Payment type | Use the LDG-derived LegislationCode to scope paymentTypesLOV, then resolve PaymentTypeCode or PaymentTypeId |
| 4 | Legal employers | Use LegislativeDataGroupId with getLegalEntityNames before querying bank accounts |
| 5 | Bank account | Search bankAccounts only within the resolved legal-employer-name scope and resolve BankAccountId |
| 6 | Report categories | Use LegislativeDataGroupId to resolve worker and third-party-payee report-category IDs or codes independently |
| 7 | Tax reporting unit | Use LegislativeDataGroupId to resolve the TaxReportingUnitName to the returned key |
| 8 | Third party | Use the resolved OrganizationPaymentMethodId to scope thirdPartyPersonPaymentMethods and resolve the third-party ID or code |

## Standard Reference and LOV Rules

| Situation | What Happens |
|---|---|
| A reference name or LOV display value is supplied | Run the applicable resolver and write only its resolved code or ID into a code-or-ID HDL attribute |
| A code or ID is already supplied and has been validated | Use it directly and don't repeat the name-resolution lookup |
| An exact name or display value returns one result | Cache the resolved value for the current operation and reuse it for every row with the same resolver inputs |
| An exact name or display value returns no results | Stop before DAT or archive approval and report the field plus invalid supplied value |
| An exact name or display value returns multiple results | Stop with an ambiguity error; don't choose the first or any automatic match |
| A name remains unresolved for a code-or-ID field | Don't include the unresolved name in that HDL field or submit the archive |
| Resolver inputs differ between rows | Treat the inputs as a different cache key and resolve independently |
| A session isn't active when a live lookup is required | Obtain a fresh authorized Fusion session before the read-only lookup; never store or expose its token in the authored resources or output |

## Reference Attribute to HDL Mapping

| Business Field | HDL Level | Accepted Input | Resolved HDL Value | Resolver |
|---|---|---|---|---|
| Legislative data group | OrganizationPaymentMethod and child context | LegislativeDataGroupName or validated LegislativeDataGroupId | LegislativeDataGroupId and LegislationCode for dependent lookups; retain LegislativeDataGroupName when the selected HDL user-key shape uses it | resolve_ldg_by_exact_name |
| Payment Type | OrganizationPaymentMethod | Payment-type display value, validated PaymentTypeCode, or validated PaymentTypeId | PaymentTypeCode from BasePaymentTypeName or PaymentTypeId from BasePaymentTypeId according to the selected HDL shape | resolve_payment_type_by_legislation |
| Currency | OrganizationPaymentMethod | Currency display value or validated CurrencyCode | CurrencyCode | resolve_currency_by_exact_display |
| Bank Account | PaymentSource | BankAccountName or validated BankAccountId | BankAccountId, with BankAccountName retained only when the selected HDL user-reference shape uses it | resolve_bank_account_by_legal_employer |
| Report Category for workers | PaymentSource | Worker report-category name or validated ID or code | WorkerReportCategoryId or WorkerReportCategoryCode according to the selected HDL shape | resolve_payment_source_report_category_by_ldg |
| Report category for third-party payees | PaymentSource | Third-party report-category name or validated ID or code | ThirdPartyReportCategoryId or ThirdPartyReportCategoryCode according to the selected HDL shape | resolve_payment_source_report_category_by_ldg |
| Tax Reporting Unit | PaymentMethodRule | TaxReportingUnitName or validated TaxReportingUnitId | TaxReportingUnitId, with TaxReportingUnitName retained only when the selected HDL user-key shape uses it | resolve_tax_reporting_unit_by_ldg |
| Third-Party Name | PaymentMethodRule | Third-party display name or validated ThirdPartyId or ThirdPartyCode | ThirdPartyId or ThirdPartyCode according to the selected HDL shape | resolve_third_party_payment_method_by_opm |

## Organization Payment Methods REST Hierarchy Discovery

This supplemental read-only contract uses `/hcmRestApi/resources/latest/organizationPaymentMethods`. It augments the existing LOV and HDL instructions and does not authorize a REST mutation. Each invocation must process every response page before it reports a complete result.

### Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| retrieve_opms_by_ldg_and_effective_date | An OPM inventory is requested for an LDG as of a system-effective date | LegislativeDataGroupId, SysEffectiveDate | GET `/hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByFilterCriteria;LegislativeDataGroupId=<LegislativeDataGroupId>,SysEffectiveDate=<SysEffectiveDate>` | All returned attributes and paging metadata; no field projection | Retain every OPM returned for the exact LDG and system-effective date; don't reduce the result to the first match | Complete OPM collection; every returned field; runtime attribute metadata profile | Zero matches is a valid empty collection; duplicate identifiers or an unpageable response are mapping errors and must be retained and reported |
| retrieve_opm_details_by_id_and_effective_date | Complete OPM details, the parent OPM name, an existing OPM immutable-field baseline, or existing-parent PaymentSource inheritance evidence is required | OrgPaymentMethodId, SysEffectiveDate | GET `/hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByOrgPayMethodId;OrgPaymentMethodId=<OrgPaymentMethodId>,SysEffectiveDate=<SysEffectiveDate>&expand=additionalDetails` | All returned OPM and `additionalDetails` attributes, including logical start and logical end dates | Require exactly one OPM identity for the supplied ID and date; preserve the requested ID and returned denormalized name | OPM detail, OPM ID, OPM name, logical dates, every returned field, runtime attribute metadata profile; preserve returned OrgPaymentMethodName, Payment Type, Currency, and LegislativeDataGroupId as the existing-parent baseline for OPM.ENFORCE_HDL_DESIGN | Zero matches: retain the requested ID and report an unresolved OPM; multiple identities: report ambiguity and don't choose one; a missing protected-field value blocks the comparison and must not be filled from a proposed replacement or child input |
| retrieve_payment_sources_by_parent_opm_and_effective_date | Payment Sources must be reconstructed under a parent OPM, or a rule lacks its Payment Source name | ParentOrgPayMethodId, SysEffectiveDate | GET `/hcmRestApi/resources/latest/organizationPaymentMethods?finder=paymentSourceFinder;ParentOrgPayMethodId=<ParentOrgPayMethodId>,SysEffectiveDate=<SysEffectiveDate>&expand=additionalDetails` | All returned Payment Source and `additionalDetails` attributes, including bank account, worker report category, third-party-payee report category, effective dates, logical dates, parent reference, and other reference or LOV fields | Retain every source whose parent reference resolves to ParentOrgPayMethodId; preserve source IDs and names; prefer a returned OPM name, otherwise invoke `retrieve_opm_details_by_id_and_effective_date` | Payment Sources grouped under the parent; OPM ID and name; Payment Source IDs and names; reference values; logical dates; runtime attribute metadata profile | Zero sources is a valid empty child collection but must be surfaced; a source whose parent can't be resolved remains in the output with its original ID and a mapping error; duplicate source identities are not merged |
| retrieve_payment_rules_by_opm_and_effective_date | Payment Method Rules must be reconstructed beneath their Payment Sources | OrgPaymentMethodId, SysEffectiveDate | GET `/hcmRestApi/resources/latest/organizationPaymentMethods?finder=findByOrgPayMethodId;OrgPaymentMethodId=<OrgPaymentMethodId>,SysEffectiveDate=<SysEffectiveDate>&expand=paymentMethodRules,additionalDetails,paymentMethodRules.additionalDetails` | All returned OPM, Payment Method Rule, and expanded `additionalDetails` attributes, including Tax Reporting Unit, OPM ID, Payment Source ID, Payment Source name when returned, effective-dated fields, and logical dates | Retain each rule separately; map it only to the Payment Source identified by the applicable returned identifier; prefer a returned Payment Source name, otherwise invoke `retrieve_payment_sources_by_parent_opm_and_effective_date` and exact-match the identifier | OPM details and logical dates; rules grouped by Payment Source; TRU; OPM ID; Payment Source ID and name; rule logical dates; runtime attribute metadata profile | Zero rules is a valid empty child collection; unresolved or ambiguous source mapping retains the rule and original identifier and emits a mapping error; never combine rules from different sources |

### Runtime Attribute Metadata Profile

For each distinct field returned by any hierarchy lookup, create one metadata entry. The response payload establishes the returned field set; authoritative service metadata, lookup results, and existing documented contracts establish the characteristics below. If a characteristic isn't present in those sources, record it as undocumented and don't infer it from an HDL attribute with a similar name.

| Metadata Property | Required Capture Rule |
|---|---|
| Attribute name | Preserve the exact REST response property name and its object path, including expanded child paths |
| Display name | Record the documented service display label; otherwise mark it undocumented |
| Data type | Record the documented REST type; otherwise mark it undocumented; don't infer a scalar type solely from one sample value |
| Required or optional | Record endpoint- and operation-specific requiredness from authoritative metadata; otherwise mark it undocumented |
| Business key indicator | Identify documented keys and hierarchy identifiers; otherwise mark it undocumented |
| Reference or LOV type | Record the documented target or resolver and retain both returned IDs and names; otherwise mark it undocumented |
| Validation rules | Record documented format, range, cross-field, effective-date, and reference validations; otherwise mark them undocumented |
| Allowed values | Resolve through the applicable existing LOV or reference resolver when one is documented; otherwise mark them undocumented |
| Maximum length or precision | Record the documented REST limit; otherwise mark it undocumented; don't copy an HDL limit unless the REST contract explicitly shares it |
| Returned value | Preserve the value associated with the hierarchy node; sanitize only credentials, tokens, and prohibited sensitive diagnostics |

### Effective-Date and Reference Resolution Rules

| Situation | Required Behavior |
|---|---|
| `additionalDetails` is expanded | Capture logical start and logical end dates at the exact OPM, Payment Source, or Payment Method Rule level where returned |
| Logical date property names differ from business labels | Preserve the exact returned property names and associate them with the logical-start or logical-end meaning only when authoritative metadata documents that meaning |
| A returned reference includes both ID and denormalized name | Preserve both values without replacing either one |
| A required denormalized OPM name is absent | Call `retrieve_opm_details_by_id_and_effective_date` with the parent ID and the same SysEffectiveDate |
| A required denormalized Payment Source name is absent | Call `retrieve_payment_sources_by_parent_opm_and_effective_date` with the OPM ID and the same SysEffectiveDate, then exact-match the returned Payment Source identifier |
| A returned reference or LOV value has an existing resolver | Apply that resolver's exact-match and zero-or-many behavior; don't select the first result |
| A field has no documented resolver | Preserve its identifier and value, mark the unresolved metadata property as undocumented, and surface the gap instead of inventing a mapping |

### REST Hierarchy Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.READ_LIST | step | 101 | reference_lookup | matches->OPM.READ_DETAILS;no_matches->OPM.READ_HIERARCHY_EMPTY;failure->OPM.READ_HIERARCHY_FAILED | none | stop | Full OPM hierarchy discovery is requested for an LDG and date | retrieve_opms_by_ldg_and_effective_date |
| OPM.READ_DETAILS | step | 102 | reference_lookup | complete->OPM.READ_SOURCES;failure->OPM.READ_HIERARCHY_FAILED | OPM.READ_LIST | stop | For each OPM ID returned by OPM.READ_LIST | retrieve_opm_details_by_id_and_effective_date |
| OPM.READ_SOURCES | step | 103 | reference_lookup | complete->OPM.READ_RULES;failure->OPM.READ_HIERARCHY_FAILED | OPM.READ_DETAILS | stop | For each OPM ID being reconstructed | retrieve_payment_sources_by_parent_opm_and_effective_date |
| OPM.READ_RULES | step | 104 | reference_lookup | complete->OPM.READ_HIERARCHY_DONE;failure->OPM.READ_HIERARCHY_FAILED | OPM.READ_SOURCES | stop | For each OPM ID being reconstructed | retrieve_payment_rules_by_opm_and_effective_date |

## LDG-Scoped Duplicate Check Example

Use the OPM creation date for effectiveDate and the LDG identifier returned by resolve_ldg_by_exact_name. A same-name OPM in another LDG does not count as a duplicate for this lookup.

```text
/hcmRestApi/resources/latest/organizationPaymentMethodsLOV?effectiveDate=2026-01-01&q=OrgPaymentMethodName='ZHRX-CN-CLI-OPM-CASH' and LegislativeDataGroupId=300100037952462
```
