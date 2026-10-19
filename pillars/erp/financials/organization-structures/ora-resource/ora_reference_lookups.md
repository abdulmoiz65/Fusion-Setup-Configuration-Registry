# Organization Structures Reference Lookups

Use read-only lookups before any CSV/import action. Match exact values only and retrieve all pages. Missing required references, multiple matches, incomplete results or unavailable reads block the affected step. A complete exact-name zero match for the requested new BU establishes the create path; it is not a missing-reference error. These APIs identify references; they do not replace the task-level CSV contract or authorize a direct write. The internal data lineage below is validation evidence only, never an import contract.

## Declared API Contracts

| Purpose | Operation | Exact matching and fields | Use in validation |
|---|---|---|---|
| Business Unit identity and financial foundation | `GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV` | Query `BusinessUnitName` with `q`; request `BusinessUnitId`, `BusinessUnitName`, `PrimaryLedgerId`, `LegalEntityId`, and `ActiveFlag`; use `totalResults=true` and page until complete | Idempotency and function-assignment compatibility. ModuleIdFinder supplies module membership within the queried visibility scope, not ConfigurationStatus; ServiceProviderFinder is supporting BU discovery whose target context must be established, not a general four-key relationship-row reader. Neither replaces exact BU identity or a complete maintenance comparison. |
| Primary ledger | `GET /fscmRestApi/resources/11.13.18.05/ledgersLOV` | Exact ledger-name match; retain the resolved ledger identifier | Resolve the requested primary ledger before financial-function import. |
| Legal entity and ledger association | `GET /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV` | Query `Name` with `q` to resolve the requested legal entity. Then use `finder=LedgerFinder;LedgerId={resolved LedgerId}`; request `LegalEntityId` and `Name`, use `totalResults=true`, and page until complete. | Resolve the requested default legal entity and prove that it is associated with the resolved primary ledger. |
| Optional Business Unit location | `GET /hcmRestApi/resources/11.13.18.05/locationsLovV2` | When a location is supplied, use the documented finder with the request effective date; retain `LocationId`, `LocationCode`, and `LocationName` and require one active/effective candidate | Resolve an optional BU location. A blank request value remains blank and does not call HCM. |
| Optional Business Unit manager | `GET /hcmRestApi/resources/11.13.18.05/publicWorkers` | When a manager is supplied, search by the supplied worker identity; retain `PersonId`, `PersonNumber`, and `DisplayName` and require one active worker | Resolve an optional BU manager as a person, not an assignment. This lookup does not prove that the worker has a manager assignment. A blank request value remains blank and does not call HCM. |
| Existing Reference Data Set — numeric BU field value | `GET /hcmRestApi/resources/11.13.18.05/hcmSetsLOV` | Resolve an exact unique set; retain `SetId`, `SetCode`, `SetName`, and `Description` | Preferred resolver when the fresh Manage Business Unit contract requires numeric `DefaultSetId`. Use `SetId` as the value and Set Name/Code as display evidence. |
| Existing Reference Data Set — FSCM code/name alternative | `GET /fscmRestApi/resources/11.13.18.05/setIdSetsLOV` | Resolve an exact unique Set Code or Set Name using the live response contract; retain returned Set Code and Set Name | Confirm an existing Default Set or a BU set assignment when a numeric Set ID is not required by the field or current export contract. Do not use a name-only partial match. |
| Create Reference Data Set | POST /fscmRestApi/resources/11.13.18.05/setIdSets through core.fusion-api.rest-api-client | Require SetCode and SetName, inspect live describe for the native create contract, preview the exact payload and obtain approval; create once and immediately re-query exact code/name | This native prerequisite is owned by the BU guidance. Do not invoke HCM Manage Reference Data Sets or package the native resource as an FSM/HDL business object. Reference the set only after exact re-validation. |
| Existing BU function assignment | Fresh target function-assignment data | For eligible additive preparation, use declared ModuleIdFinder with exact BU identity and controlled module; maintenance/status comparisons still require a source exposing the requested status | Validate BU roles in service-provider relationships and determine an existing function assignment. |
| Existing provider relationship | Fresh target provider-relationship data | Match the four-key identity: Client BU, Upstream Function, Downstream Function, Provider BU. Read `AnyProvidersFlag` with the matching row. | Detect a duplicate only; do not infer function-pair compatibility from existing provider rows. |
| Provider function-pair policy | Target evidence for seeded `FUN_RELATED_FUNCTIONS` | Match the exact `UPSTREAM_FUNCTION_ID` + `DOWNSTREAM_FUNCTION_ID` pair and record the returned `OUTSOURCING_POLICY_CODE`. | Validate pair compatibility as a pre-import gate. Obtain authoritative semantics before treating a policy code as a behavioral rule. |

Published API references: Financials BUs LOV: `https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-finbusinessunitslov-get.html`; Legal Entities LOV: `https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-legalentitieslov-get.html`; HCM Sets LOV: `https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-hcmsetslov-get.html`; Locations LOV V2: `https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-locationslovv2-get.html`; Public Workers: `https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-publicworkers-get.html`; Financials REST API index: `https://docs.oracle.com/en/cloud/saas/financials/26c/api.html`.

## Idempotency Decisions

| Task Code | Task Name | Lookup Key | Result | Required Action |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact normalized `BusinessUnitName` plus effective context | Zero matches | New: continue only after Default Set verification. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact normalized `BusinessUnitName` plus effective context | One matching BU with identical requested effective attributes | Existing identical: no-op; do not generate or import a duplicate row. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact normalized `BusinessUnitName` plus effective context | One matching BU with a different default set, ledger, legal entity, location, status, or other requested effective attribute | Existing different: stop and obtain an explicit update or new-name decision. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact normalized `BusinessUnitName` plus effective context | Multiple candidates or unresolved effective-date interpretation | Ambiguous: stop; do not choose a record. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | `FUN_BU_USAGES(BUSINESS_UNIT_ID, MODULE_ID)` | Existing assignment has the requested configuration | No-op; do not reimport it. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | `FUN_BU_USAGES(BUSINESS_UNIT_ID, MODULE_ID)` | Existing assignment differs or candidate set is ambiguous | Stop for an explicit maintenance decision. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | `FUN_BU_SERVICE_PROVIDERS(CLIENT_BU_ORG_ID, UPSTREAM_FUNCTION_ID, DOWNSTREAM_FUNCTION_ID, PROVIDER_BU_ORG_ID)` | Existing relationship has the requested supported values | No-op; do not reimport it. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Same composite key | Existing relationship differs or candidate set is ambiguous | Stop for an explicit maintenance decision. |

## Internal Data Lineage and Compatibility Evidence

| Concept | Persistence/View Evidence | Validation Use |
|---|---|---|
| Business Unit | `HR_ALL_ORGANIZATION_UNITS_F` joined to `HR_ORG_UNIT_CLASSIFICATIONS_F`, filtered by classification `FUN_BUSINESS_UNIT` | Resolve a BU as an effective-dated Business Unit, not merely an organization-name string. |
| BU default attributes | `HR_ORGANIZATION_INFORMATION_F`, context `FUN_BUSINESS_UNIT`: `ORG_INFORMATION2` legal entity, `ORG_INFORMATION3` ledger, `ORG_INFORMATION4` default set | Compare a financial function's resolved ledger/legal entity with the selected BU's actual configuration. |
| Business-function assignment | `FUN_BU_USAGES`, key `(BUSINESS_UNIT_ID, MODULE_ID)` | Prevent duplicate assignments and prove provider/downstream eligibility where required by `AnyProvidersFlag`. |
| Business-function catalog | `FUN_BUSINESS_FUNCTIONS_B`; assignment UI reads `FUN_BUSINESS_FUNCTIONS_VL` and exposes `Enabled`, `GENERATE_FIN_TXN_FLAG`, and `SETUP_API` | Resolve a unique code, record target availability evidence when supplied, and decide whether financial foundation validation is mandatory. |
| Provider function-pair policy | `FUN_RELATED_FUNCTIONS`, key `(UPSTREAM_FUNCTION_ID, DOWNSTREAM_FUNCTION_ID)`, with `OUTSOURCING_POLICY_CODE` | Require a seeded related-function pair as a pre-import compatibility gate; never invent pair compatibility or policy-code semantics. |
| Service-provider relationship | `FUN_BU_SERVICE_PROVIDERS`, key `(CLIENT_BU_ORG_ID, UPSTREAM_FUNCTION_ID, DOWNSTREAM_FUNCTION_ID, PROVIDER_BU_ORG_ID)` | With `N`, require provider/downstream eligibility. With `Y`, do not require named-provider equality. The source does not establish client/upstream ownership as a required validation. |
| BU set assignment | `FND_SETID_ASSIGNMENTS` joined to `FND_SETID_SETS_VL`, `FND_SETID_REFERENCE_GROUPS_VL`, and `HR_ORGANIZATION_V` | Require `DETERMINANT_TYPE = 'BU'`, `DETERMINANT_VALUE = ORGANIZATION_ID`, and `CLASSIFICATION_CODE = 'FUN_BUSINESS_UNIT'` when interpreting internal evidence. |

## Lookup Operations

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | BU and Reference Data Set resolver | A name or set must be resolved | Business Unit Name; Set Code; Set Name | `finBusinessUnitsLOV`; `hcmSetsLOV` when `DefaultSetId` is required; `setIdSetsLOV` as the FSCM code/name alternative | BU identity and financial foundation; `SetId`, Set Code, and Set Name when numeric field mapping is required | Exact unique match only | Existing BU facts or an existing set identity | Stop and ask for a unique value; a new-set request must run the separate set-creation route and re-lookup |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | verify_ledger_legal_entity_association | A Business Unit create or financial-function assignment requires a primary ledger and default legal entity | Resolved LedgerId; resolved LegalEntityId; requested ledger and legal-entity names | `GET /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV?finder=LedgerFinder;LedgerId={resolved LedgerId}&onlyData=true&totalResults=true&limit=500`, following every page | LegalEntityId; Name; totalResults; hasMore | The complete LedgerFinder result has exactly one item with LegalEntityId equal to the resolved LegalEntityId and Name equal to the requested legal-entity name | Verified ledger/legal-entity association | Stop when the associated legal entity is absent, repeated, nonexact, incomplete, or unavailable |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Optional manager and location resolver | Manager or location is supplied | Manager display name/person number; location name/code; request effective date | `publicWorkers`; `locationsLovV2` | PersonId, PersonNumber, DisplayName; LocationId, LocationCode, LocationName | One active worker; one active/effective location | ManagerId and LocationId for comparison with current task-template fields | Stop on zero, multiple, inactive, ineffective, inaccessible, or unavailable results. Do not query HCM or populate either ID when its request value is blank. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | verify_ledger_legal_entity_association | A financial business-function assignment requires a primary ledger and default legal entity | Resolved LedgerId; resolved LegalEntityId; requested ledger and legal-entity names | `GET /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV?finder=LedgerFinder;LedgerId={resolved LedgerId}&onlyData=true&totalResults=true&limit=500`, following every page | LegalEntityId; Name; totalResults; hasMore | The complete LedgerFinder result has exactly one item with LegalEntityId equal to the resolved LegalEntityId and Name equal to the requested legal-entity name | Verified ledger/legal-entity association, then compare the resolved IDs with the selected BU foundation | Stop on absent, repeated, nonexact, incomplete, or nonmatching foundation values |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Client/provider, assignment, and relationship resolver | Client, provider, or function must be verified | Client BU; Provider BU; upstream/downstream function codes | `finBusinessUnitsLOV`; fresh target assignment and provider-relationship data; target `FUN_RELATED_FUNCTIONS` evidence | BU IDs; BU/function assignments; current four-key relationships; pair policy | Exact unique role matches; exact seeded pair; check the documented composite relationship key | Resolved references, role evidence, and pair policy | Stop and ask for clarification or the target pair-policy evidence |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | BU and set resolver | Assignment values must be verified | Business Unit; Set Code | `finBusinessUnitsLOV`; `setIdSetsLOV` | Exact resolved BU and set | Exact unique match only | Resolved references | Stop and ask for a unique value |

## Business Function Seed Data

| Task Code | Task Name | Business Function ID | Business Function Code | Match Rule |
|---|---|---:|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 10 | PAYABLES_INVOICING_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 20 | PAYABLES_PAYMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 30 | BILLING_REVENUE_MNG_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 40 | CUSTOMER_PAYMENTS_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 50 | SERVICE_REQUEST_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 70 | COLLECTIONS_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 80 | MATERIALS_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 90 | CUST_CONTRACT_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 100 | PROJECT_ACCOUNTING_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 110 | PROCUREMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 120 | REQUISITIONING_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 130 | RECEIVING_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 140 | EXPENSE_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 160 | SALES_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 180 | PRC_CONTRACT_MANAGEMENT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 190 | INCENTIVE_COMPENSATION_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 200 | REV_COMPL_AND_ACCTG_MGT_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 210 | FLA_LEASE_ACCOUNTING_BF | Exact code match; derive Module ID |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | 220 | GLOBAL_HUMAN_RESOURCES_BF | Exact code match; derive Module ID |

## Controlled Related-Function Pairs

The following directed `FUN_RELATED_FUNCTIONS` pairs are controlled, user-supplied seed evidence. The source reports `ORA_SEED_SET1 = Y` and `ORA_SEED_SET2 = Y` for each pair from `fin/fun/db/data/FinFunBusinessFunctions/BFRelatedFunctionSD.xml`. Use this table to resolve the direction and policy-code value without asking requesters for numeric IDs. `OUTSOURCING_POLICY_CODE` values are retained as opaque codes: do not infer operational semantics for `O` or `M` without authoritative Oracle evidence.

| Upstream Function | Upstream ID | Downstream Function | Downstream ID | Outsourcing Policy Code | Seed Evidence |
|---|---:|---|---:|---|---|
| Payables Invoicing | 10 | Payables Payments | 20 | `O` | `BFRelatedFunctionSD.xml`; both seed-set flags `Y` |
| Payables Invoicing | 10 | Procurement | 110 | `M` | `BFRelatedFunctionSD.xml`; both seed-set flags `Y` |
| Billing and Revenue Management | 30 | Customer Payments | 40 | `O` | `BFRelatedFunctionSD.xml`; both seed-set flags `Y` |
| Requisitioning | 120 | Procurement | 110 | `M` | `BFRelatedFunctionSD.xml`; both seed-set flags `Y` |

For a live relationship import, use the table as controlled seed evidence and fresh target role evidence. For SPR_FSM_ADD_RELATIONSHIP_V1 the tested pair and bounded current-workflow first-submission evidence qualify preparation; outside it obtain the required current relationship/policy evidence. If a requested behavior depends on the meaning of `O` or `M`, block until its semantics are authoritatively evidenced or the user explicitly approves a documented exception.

## Controlled Reference Group Names

| Task Code | Task Name | ReferenceGroupName |
|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AP_PAYMENT_TERMS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_ACCOUNTING_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_AGING_BUCKETS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_APP_EXCEPTION_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_AUTOCASH_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_AUTOMATCH_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_COLLECTORS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_LOCKBOX |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_MEMO_LINES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_PAYMENT_TERMS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_RECEIPT_METHOD_ACCOUNT |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_RECEIPT_SOURCE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_TRANSACTION_TYPE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_REMIT_TO_ADDRESS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_REVENUE_CONTINGENCIES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | AR_TRANSACTION_SOURCE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | CN_CREDIT_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | DOO_HOLD_CODES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | DOO_ORCHESTRATION_PROCESS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | FND_TREE_GROUP |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HRA_PERFORMANCE_TEMPLATES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HRG_GOAL_PLAN_TEMPLATES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HRR_DASHBOARD_TEMPLATES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HZ_CUSTOMER_ACCOUNT_RELATION |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HZ_CUSTOMER_ACCOUNT_SITE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HZ_SALES_PERSON |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | IEX_COLLECTIONS_SETUPS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | IEX_DUNNING_PLANS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | JA_CN_TRANSFER_RULE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | CML_SETUPS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HED_ADJ_CAL_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | HED_DUE_DATE_CAL_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_DEAL_TYPE_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_LEAD_BUDGET_STATUS_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_LEAD_CHANNEL_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_LEAD_RANK_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_LEAD_REASSIGN_REASON_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_LEAD_TIMELINE_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_REJECT_REASON_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MKL_RETIRE_REASON_CD_SETID |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_CRED_ALLOC_TEMPLATES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SALES_METHODS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_ASSESS_OVRRIDE_RSN |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_DEAL_HORIZION |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_DECISION_LEVEL |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_REVENUE_TYPE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_REVN_CATEGORY |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_RISK_LEVEL |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_STRATEGIC_VALUE |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_SETID_WIN_LOSS_REASON |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOO_STAGE_PHASE_CD |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | MOW_ASSESS_TEMPL_GROUP |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OKC_APPLY_HOLD_REASONS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OKC_CANCELLATION_REASONS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OKC_CLOSE_REASONS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OKC_CONTRACT_STATUSES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | OKC_CONTRACT_TYPES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PER_DEPARTMENTS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PER_GRADES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PER_JOBS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PER_LOCATIONS |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PJB_PROJ_CONTRACT_BILLING |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PJF_ACCOUNTING_DEFINITION |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | PJF_RATES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | QP_PRICING_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | SALARY_CODE_GROUP |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | SVC_SR_SEVERITIES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | VRM_REVENUE_POLICIES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | VRM_REVENUE_RULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | ZBS_STATUS_LOOKUP_VALUES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | ZMM_NOTE_TYPES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | ZMM_SCHEDULES |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | ZX_TAX_CLASSIFICATION_CODES |

## Lookup Execution Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Default Set lookup returns zero, many, or a nonexact result | Block the BU import. For Create New, complete separate set creation and re-lookup before preparing the emitted parent-BU data. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Exact BU lookup returns an existing candidate | Apply the idempotency decision table in `ora_input_validation.md`; do not create on lookup result alone. |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Manager or location is supplied | Resolve it through the respective HCM LOV before creating the BU; verify the resolved ID against the current task-template column semantics. HCM authorization is a required dependency only when that optional field is supplied. |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A supplied business name matches more than one candidate | Block preview and ask the user to disambiguate |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A financial function resolves | Resolve ledger and legal entity exactly once and require their IDs to equal the selected BU's `FUN_BUSINESS_UNIT` information values before import. |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Relationship direction, `AnyProvidersFlag` handling, required provider/downstream eligibility, related-function pair, or policy semantics needed for the requested behavior is unresolved | Block the import and request the target contract, an assignment correction, or authoritative pair-policy evidence. |
## Ledger-to-Legal-Entity Association Gate

When both foundation values are supplied for BU creation, or a financial business function requires them, resolve the primary ledger and default legal entity exactly, then call `verify_ledger_legal_entity_association`. Require the complete `legalEntitiesLOV` `LedgerFinder` response for the resolved LedgerId to contain exactly one item matching the resolved LegalEntityId and requested legal-entity name. Independent `ledgersLOV` and name-query `legalEntitiesLOV` matches do not prove an association. An absent, repeated, nonexact, incomplete, or unavailable LedgerFinder result blocks the import.

  <!-- -->

## Native Default-Set Creation

| Task Code | Task Name | Step | Required Evidence or Action | On Failure |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Validate intent and uniqueness | For Create New require SetCode and SetName; enforce code 30, name 80 and description 2000 character limits; query both identifiers exactly through declared set LOVs and complete paging | Stop on a collision, ambiguity, incomplete results or unavailable privilege; do not infer absence from an error |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Inspect native contract | GET /fscmRestApi/resources/11.13.18.05/setIdSets/describe through the core REST client; confirm create availability and actual fields | Report the native privilege/contract gap; do not route to an HCM skill or invent a write endpoint |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Preview and approve | Exact target and body containing SetCode, SetName and optional user Description; omit generated SetId and audit fields; an omitted Description remains unspecified | Preserve authorization for this exact action; apply the repository and core approval rules without duplicate approval requests |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Create once | POST /fscmRestApi/resources/11.13.18.05/setIdSets through the core REST client with REST-Framework-Version 9 and core OAuth; retain the receipt | On failure or uncertain response, record diagnostics and reconcile by exact reads before any retry |
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Re-resolve | Require one exact code/name identity from current set LOVs and retain SetId when the template needs numeric DefaultSetId | Block BU preparation until re-resolution succeeds; never invent a numeric ID |

This route requires no HCM setup-task skill, no HCM task added to the Run Book and no Data Loader discriminator for setIdSets. HCM Sets LOV remains a permitted reference GET. Perform OAuth bootstrap/refresh serially before batching independent reads so callbacks do not compete.

## BU Assignment Verification APIs

| Task Code | Task Name | Purpose | Read Operation | Match and Limits |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Resolve reference-group display mapping | GET /fscmRestApi/resources/11.13.18.05/setIdReferenceGroups | Retain ReferenceGroupName and current visible label; complete paging, then match the requested controlled group exactly; do not invent a friendly-label alias |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Read saved BU group assignments | GET /fscmRestApi/resources/11.13.18.05/setIdAssignmentsBusinessUnit with finder=AssignmentFinder;DeterminantValue={resolved BusinessUnitId},ReferenceGroupName={resolved group} | Require determinant BU, matching BU/group and intended SetCode/SetId; complete paging; setIdAssignmentsSet is the SET determinant resource and cannot establish BU absence |

Use the documented/live-confirmed finder variables and response fields. REST OrganizationCode and an emitted FSM organization key have different contracts; validate the mapping before populating a CSV key. The finBusinessUnitsLOV response proves identity, active state and foundation, but does not expose every default-set or effective-date attribute. Use ModuleIdFinder as module-presence evidence for BUF_FSM_ADD_FUNCTION_V1; ServiceProviderFinder remains supporting relationship discovery. Neither substitutes for exact-name identity, complete maintenance comparison or unexposed ConfigurationStatus.

Native creation is confirmed through the current target setIdSets/describe contract; do not assume a write operation from a published lookup index. BU assignment GET contract: https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-setidassignmentsbusinessunit-get.html . Confirm the target exposes the contract before using it; API availability alone does not grant write authorization.

## Permitted Current-State Sources

Run the declared exact BU, set, group and BU-determinant assignment GETs before acquiring populated data. Complete paging and record scope. A successful zero-assignment result supplies absence evidence; it does not supply a generated parent OrganizationCode or effective dates. Select the operation-specific additive profile before requiring unexposed parent keys/dates. Obtain an exact value only when that selected contract requires it, using a declared richer read/adapter, verified current-workflow facts or a named authorized genuinely scoped route. Never infer those values from a template, display name, historical successful row or a full export. The packaged BUSA_FSM_PARENT_KEY_V1 correspondence removes the need for a populated assignment CSV to qualify mapping; it does not enlarge the fields exposed by finBusinessUnitsLOV or setIdAssignmentsBusinessUnit.

## Function Presence for the Additive Profile

| Task Code | Task Name | Purpose | Read Operation | Match and Limits |
|---|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Preflight and post-import module membership | GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV with finder=ModuleIdFinder;ModuleId={controlled ModuleId} | Use declared target finder variables and configured security scope, request returned BU identity/active/foundation fields, complete paging, then match exact saved BusinessUnitId and name |

Oracle's published finder contract defines ModuleId as the business function performed by the BU, with optional Intent and SearchTerm variables. Use an already configured valid Intent when required; never invent a privilege string or treat a broad keyword as exact identity. Source: https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-finbusinessunitslov-get.html ; confirm target availability before calling.

A successful complete zero result means no matching module membership observed in the selected scope and allows eligible additive preparation; disclose visibility limits. Failed, partial or known-invalid visibility cannot prove absence. A positive exact match supports module membership, not a read of ConfigurationStatus or all parent attributes. Preserve the same queried scope before/after the import and compare exact identity/foundation. A newly positive post-import match plus reviewed successful processing supports visible assignment completion with those limits. Complete status equality, independent default/date preservation and every provider eligibility rule remain separate evidence requirements.


## Relationship Read Scope and First Submission

| Task Code | Task Name | Purpose | Read Operation or Evidence | Match and Limits |
|---|---|---|---|---|
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Verify qualified provider/downstream membership | GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV with finder=ModuleIdFinder;ModuleId={controlled downstream ID}; complete paging and exact provider identity/active/foundation match | Combine with reviewed successful current-workflow function import for SPR_FSM_ADD_RELATIONSHIP_V1; ConfigurationStatus is unexposed, not independently verified |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Supporting provider discovery when target context is available | GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV using the target-supported ServiceProviderFinder variables and required context confirmed through core contract discovery | Published variables are ModuleId, UpstreamFunctionId, DownstreamFunctionId, optional Intent/SearchTerm. A target error requiring Business Unit ID is contract/context failure, not absence; do not invent BusinessUnitId as an undocumented finder parameter |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | First-submission assurance | Exact-zero creation checks, inspected current-workflow archive scopes and reconciled stage receipts required by SPR_FSM_ADD_RELATIONSHIP_V1 | This is bounded workflow provenance, not a read of global relationship absence. A missing independent row reader is a disclosed verification limit only when full profile eligibility passes |

ServiceProviderFinder returns BU LOV records, not every four-key relationship attribute, AnyProvidersFlag or ActiveFlag. Even a successful result must be interpreted within its documented scope. If required target context is unavailable, retain the read error and do not repeat unchanged calls or fabricate a new endpoint/parameter. The eligible first-submission profile can proceed through normal validation/approval with that limit; existing-state comparison, strict verification and uncertain-write reconciliation cannot borrow it. Reference: https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-finbusinessunitslov-get.html ; current 26d page was unavailable during authoring, so confirm target describe/availability rather than claiming newer finder support.


## Endpoint-Only Duplicate and Verification Checks

Perform exact identity, duplicate, relationship, membership and saved-state checks only through this task's declared core-client endpoints and authorized FSCR evidence routes. Complete pagination and inspect the actual response and available client diagnostics before reporting a match, absence or no-op. UI navigation, DOM/network inspection, screenshots, grid extracts and manually transcribed UI values are prohibited verification sources, including delegated fallbacks. A failed read is not absence evidence. Qualified active-workflow first-submission assurance remains bounded provenance, not endpoint proof of global absence. Disclose missing/unexposed facts without inventing a read contract or requiring UI evidence. Core.auth user login handoff does not authorize task UI access.
