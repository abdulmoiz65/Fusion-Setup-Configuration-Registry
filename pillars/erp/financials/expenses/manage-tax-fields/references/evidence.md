# Reviewed evidence

## Contract follow-up — 2026-10-05

### DOC-REST-BU

[Oracle Financials 26C: Get all business units](https://docs.oracle.com/en/cloud/saas/financials/26c/farfa/op-finbusinessunitslov-get.html) documents finBusinessUnitsLOV, queryable BusinessUnitName and response BusinessUnitId/BusinessUnitName/ActiveFlag. This supports an exact-name, active-BU preflight contract. It does not prove privileges, availability or enterprise equivalence on the target; the returned ID must not replace FSM's own enterprise-scoped name resolution.

### DOC-REST-TERRITORY

[Oracle Common Features 26C: Get all territories](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-servername-fscmrestapi-resources-11.13.18.05-territorieslov-get.html) documents territoriesLOV and PrimaryKey finder with TerritoryCode. This supplies the country existence request contract. Literal OTHER remains the source-established exception, not an ISO territory lookup.

### SRC-CS-LOOKUP-PVO

[ExmLookupPVO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/lookups/pubicView/src/oracle/apps/financials/expenses/lookups/publicView/ExmLookupPVO.xml), retrieved through authenticated external Chrome on 2026-10-05: lines 7-15 select lookup fields from EXM_LOOKUP_VALUES; ByLookupType and ByLookupCode criteria appear at 62-112, active-date criteria at 113-165, enabled criterion begins at 166. Do not substitute standardLookups solely because its attribute names resemble this view; equivalence still needs verification.

### SRC-CS-LOOKUP-VIEW

[EXM_LOOKUP_VALUES.view](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/shared/lookups/dbSchema/database/fusionDB/FUSION/EXM_LOOKUP_VALUES.view), retrieved 2026-10-05: lines 69-88 join FND_LOOKUP_VALUES_B/TL to FND_LOOKUP_TYPES; filter module 47110F64AC0608E2E040449823C60DB6 and view application IDs 0 or 10016. Generic REST lookup equivalence requires checking this context, not only the lookup type text. A standardLookups URI is therefore a discovery candidate, not yet the confirmed task resolver.

### DOC-FSM-PACKAGE

[Oracle FSM: Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html), latest accessible HTML found for this topic after 26B/26C URLs failed: retain every CSV member; a member without intended data may retain only its header. Preserve exported value formats. These generic rules do not establish how this task processes two members mapped to the same setup-option XML, nor create-time audit serialization.

[Oracle FSM 26C: Compare Task Setup Data](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/compare-task-setup-data.html) states that CSV import does not delete destination records. This supports distinguishing absence from deletion, but does not establish blank-as-clear semantics.

### Framework source search

Authenticated CodeSearch searches for MigratorHelper.java and then MigratorHelper returned no matching files in FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64 on 2026-10-05 (index 2026-10-05). The collected task services delegate key reconciliation and XML reading to that helper. Its create/audit handling remains unverified; missing source is not evidence of a default.

Source branch: FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64, indexed 2026-10-02. Source behavior is not proof of successful import on another build. No setup mutation or import test was performed during that source-review phase; subsequent execution coverage is summarized below.

## SRC-CS-TASK

[SetupTaskSD.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/fun/db/data/FinFunShared/SetupTaskSD.xml#11469)

Task EXM_MANAGE_TAX_FIELDS is enabled, named Manage Tax Fields, and routes to /WEB-INF/oracle/apps/financials/expenses/policy/taxfields/ui/flow/FinExmPolicyTaxFieldsMaster.xml#FinExmPolicyTaxFieldsMaster. Lines 11469-11488.

## SRC-CS-TASK-BO

[SetupTaskBusinessObjectSD.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/fun/db/data/FinFunShared/SetupTaskBusinessObjectSD.xml#2729)

Lines 2729-2743: task owns enabled EXM_SETUP_OPTION and EXM_VAT_FIELD mappings, each ImportSequence 0. Extra cash advance CSV membership still requires explanation.

## SRC-CS-UI-AM

[FinExmPolicyTaxFieldsAMImpl.java](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/taxfields/model/src/oracle/apps/financials/expenses/policy/taxfields/uiModel/applicationModule/FinExmPolicyTaxFieldsAMImpl.java)

Lines 84-109: doEnableTax creates or updates setup option using ENABLE_TAX constant and Y/N. Lines 225-235 create country row. Lines 259-284 create missing OTHER row on BU navigation. Lines 306-329 behavior lookup EXM_FIELD_BEHAVIOUR. UI behavior only; do not infer import defaults.

## SRC-CS-UI-AM-XML

[FinExmPolicyTaxFieldsAM.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/taxfields/model/src/oracle/apps/financials/expenses/policy/taxfields/uiModel/applicationModule/FinExmPolicyTaxFieldsAM.xml)

Lines 17-40 bind VatFieldsVO, VatFieldsOtherVO, SetupOptionsVO, BehaviorsVO, BusinessUnitVO, TaxFieldsVO, TerritoryLOVVO. Lines 41-52 BU view links.

## SRC-CS-UI-VO

[VatFieldsVO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/taxfields/model/src/oracle/apps/financials/expenses/policy/taxfields/uiModel/view/VatFieldsVO.xml)

EXM_VAT_FIELDS joined to FND_TERRITORIES_VL. Lines 111-112 shared VatFieldEO and read-only TerritoryPEO. UI defaults lines 126-167: ENABLED for merchant name and tax classification, DISABLED for other four. Not import-default evidence.

## SRC-CS-EO

[VatFieldEO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/shared/model/src/oracle/apps/financials/expenses/policy/shared/model/entity/VatFieldEO.xml)

Lines 23-30 EXM_VAT_FIELDS and VatFieldEOImpl. BU validation uses active BusinessUnitPVO; behavior resolver EXM_FIELD_BEHAVIOUR enabled Y. Territory validated except literal OTHER. Six controls validate DISABLED, ENABLED, REQUIRED. EnabledFlag validates Y/N. Primary key VatSetupId; unique alternate key OrgId+TerritoryCode at lines 562-593. Audit fields have history metadata.

## SRC-CS-FSM-AM

[ExpenseVatFieldServiceAMImpl.java](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/shared/model/src/oracle/apps/financials/expenses/policy/shared/expenseVatFieldService/applicationModule/ExpenseVatFieldServiceAMImpl.java)

Export excludes VatSetupId, OrgId, BusinessUnitId, ObjectVersionNumber (78-81). Import resolves BuName with tenant enterprise ID through BusinessUnitP/BuAltKeyByName (120-164), writes OrgId when found, updates PK using AltKey (168-171), then readXML (175-177). Exceptions become processing errors (183-188). Missing/multiple resolution semantics require helper review; do not assert successful import behavior.

## SRC-CS-FSM-VO

[VatFieldVO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/shared/model/src/oracle/apps/financials/expenses/policy/shared/expenseVatFieldService/view/VatFieldVO.xml)

FSM view joins EXM_VAT_FIELDS to FUN_ORGANIZATIONS_V and reuses VatFieldEO. AltKey maps VatFieldEOAltKey (lines 180-186). Six controls and EnabledFlag have no explicit DefaultValue. Audit attributes IsUpdateable=false. Shared framework behavior still requires validation; do not infer omitted-field behavior.

## SRC-CS-EO-IMPL

[VatFieldEOImpl.java](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/shared/model/src/oracle/apps/financials/expenses/policy/shared/model/entity/VatFieldEOImpl.java)

Entity class extends OAEntityImpl; inspected generated getters/setters and complete source; no local create override or explicit business-field default assignment. This does not establish base-class defaults.

## SRC-CS-CASH-BO

[SetupBusinessObjectSD.xml: cash-advance object](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/fun/db/data/FinFunShared/SetupBusinessObjectSD.xml#13711)

Visually verified lines 13711-13735: EXM_CASH_ADV_SETUP_AND_POLICY uses oracle.apps.financials.expenses.setup.shared.expenseSetupOptionService.ExpenseSetupOptionService, XmlFileName EXM_SETUP_OPTION.xml, XmlNodePath /SetupOptionVO/SetupOptionVORow. MigrationModeFlag Y. This proves shared service/XML routing, not permission to change cash-advance options.

## SRC-CS-SETUP-FSM-AM

[ExpenseSetupOptionServiceAMImpl.java](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/shared/model/src/oracle/apps/financials/expenses/setup/shared/expenseSetupOptionService/applicationModule/ExpenseSetupOptionServiceAMImpl.java)

Export lines 64-89 filters by FUN_BUSINESS_UNIT, excludes OptionId/OrgId/BusinessUnitId/ObjectVersionNumber and emits EXM_SETUP_OPTION.xml. No task-specific OptionCode filter appears in this method. Import lines 143-177 resolves BuName plus enterprise via BuAltKeyByName, reports BU not found as processing message, maps missing-BU OtherOrgId=-1 to OrgId=-1 and other values to -999, then updates PK by AltKey and invokes readXML. This is shared service behavior, not authorization for global scope or unrelated setup-option changes.

## SRC-CS-TAX-SETUP-VO

[SetupOptionsVO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/policy/taxfields/model/src/oracle/apps/financials/expenses/policy/taxfields/uiModel/view/SetupOptionsVO.xml)

Visually verified lines 28-43: filters ORG_ID=:BindOrgId AND OPTION_CODE=:bindEnableTax; bindEnableTax DefaultValue ENABLE_TAX. Combined with UI AM doEnableTax, task business values are Y/N for ENABLE_TAX.

## SRC-CS-SETUP-EO

[SetupOptionEO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/shared/model/src/oracle/apps/financials/expenses/setup/shared/model/entity/SetupOptionEO.xml)

Entity OptionCode required, length 30, validated through enabled EXM_SETUP_OPTIONS lookup; ValueCode length 30 with no literal list in this XML. Alternate key OptionCode+OrgId (363-375). Shared entity is broader than tax task. EOImpl and import view remain to review for complete field contracts.

## FSM-EXPORT

Same-task current export and header-only template were completed for EXM_MANAGE_TAX_FIELDS on release 11.13.27.01.0. Package structure and headers agree. Current package SHA256: 468c98ead693f993e88ce1941c8af38f181634bc23eadcb5cf336b440d7f1864. Template SHA256: 2cf184724f49384f901eec7de4c7d9391915a370463226f0a798ccc5a415bc28. Raw data, credentials and environment-specific business values are intentionally excluded.

## FSM-DUPLICATE-CHECK

A direct byte comparison of EXM_SETUP_OPTION.csv and EXM_CASH_ADV_SETUP_AND_POLICY.csv in each collected ZIP returned identical for both current and template exports. This verifies duplicate contents in those exact artifacts; it does not establish whether a future export is identical or authorize removing a member. The shared XML/service mapping is corroborated by SRC-CS-CASH-BO and SRC-CS-SETUP-FSM-AM.


## SRC-CS-BEHAVIOR-BOOTSTRAP (historical corroboration only)

[EXM_SEED_LOOKUP.sql](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/exm/noship/bootstrap/EXM_SEED_LOOKUP.sql#125)

Visually reviewed lines 125-178 on 2026-10-05. The lookup type uses X_VIEW_APPSNAME=EXM and X_APPLICATION_SHORT_NAME=EXM. Value definitions map REQUIRED to Required, ENABLED to Optional and DISABLED to Hidden, each enabled Y. This file is under noship/bootstrap and last modified in 2009; it is historical corroboration, not proof of current shipped seeds or target configuration. EXM is a candidate application context to investigate for the generic lookup resolver, not an established callable contract.

## SRC-CS-MAPPING-MIGRATION (related implementation only)

[MappingSetsServiceAMImpl.java](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/ledger/xla/accountingMethodSetup/mappingSets/model/src/oracle/apps/financials/subledgerAccounting/accountingMethodSetup/mappingSetsService/model/applicationModule/MappingSetsServiceAMImpl.java#1698)

Definition search for updatePrimaryKeysInXML found six results in the selected Fusion project. Reviewed this local implementation: lines 1790-1802 convert absent/empty alternate-key values to NullValue; lines 1811-1849 find a row by alternate key, reuse its primary key, or generate a new sequence key if eligible and absent. This is a method on MappingSetsServiceAMImpl, not the MigratorHelper implementation invoked by Expenses. It does not resolve audit-column serialization or CSV-to-XML shared-member behavior and must not be used to close those contracts.

Search limitation: the all-project definition search for MigratorHelper returned HTTP 502. The narrower full-text EXM_FIELD_BEHAVIOUR search succeeded; *seed* path filtering returned two historical noship SQL files. Literal seed path filtering returned no matches, so that result is not evidence of seed absence.


## REPO-AR-ADAPTER-REVIEW

Reviewed origin/lmallick_receivables_system_options at commit f6f74dc3d880b7ef7a00167ac15c68e3a9a06d6a, task folder pillars/erp/financials/receivables/manage-receivables-system-options. The e2e-adapter.json descriptor allows update only and has generation.readiness=blocked. Its runtime emits only requested rows, blanks audit cells, retains all members and uses current baseline metadata. It is a packaging precedent, not successful create evidence or evidence about Expenses' two members sharing one XML mapping. Do not copy its readiness or infer live validation.

## BUILDER-AUDIT-CONTRACT

The previously downloaded deliverable builder assets/fsm_task_adapter.py, SHA256 4921669d4b5f71f53c0084778a2df55c3d5c3a05ff5af9bd14a77b85368acd20, clears each entity audit field at lines 1119-1120 and rejects populated audit cells at 1190-1193. references/fsm-task-adapter-contract-v1.md permits standard Fusion who-column identification. Together with the task's non-updateable audit VO attributes, this establishes the candidate convention: keep headers, emit empty audit cells, retain baseline evidence separately. It does not establish blank business-field semantics or successful target execution.

## BUILDER-FSM-VALIDATION

The same builder contract's Builder readiness rules explicitly permit Confirmed fsm_import_resolved/fsm_import_validated references without a public GET when keys, validation and failure semantics are retained. SRC-CS-EO lines 46-59 binds ExmLookupPVO to EXM_FIELD_BEHAVIOUR and EnabledFlag=Y; each behavior's ListValidationBean validates LookupCode membership and reports FND_CMN_INVALID_ATTRB_API_SRV2. The reviewed import path uses the corresponding entity-backed VO. The resolver is therefore import-time validation; it does not pre-populate target values, select a first match or invent a REST endpoint.


## DOC-CSV-EMPTY-MEMBER

[Oracle: Export and Import CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/export-and-import-csv-file-packages.html), Modify Setup Data, reviewed 2026-10-05. Oracle instructs retaining every CSV member and using a heading-only file when its setup data is not to be included. The equivalent 26C URL was attempted but inaccessible. Combined with the user's explicit single setup-CSV instruction, the task contract populates EXM_SETUP_OPTION only for tax switches and leaves EXM_CASH_ADV_SETUP_AND_POLICY header-only. This is a documented exclusion policy, not proof of how duplicate populated members merge. Target release acceptance and preservation must still be reconciled after an approved import.


## Validation coverage — 2026-10-07

The [Manage Tax Fields Testing campaign](https://confluence.oraclecorp.com/confluence/display/FFT/Manage+Tax+Fields+Testing) records selected nonproduction execution evidence separately from the source review above. Its snapshot at this date includes 57 live setup passes, covering selected creates, updates, all 18 field/value combinations and 30 directed transitions. BU and territory preflight, terminal import results and fresh-export reconciliation were exercised. UI01 (hidden) and UI02 (optional blank) passed; UI03 is partial because required-field validation was observed but supplied-value persistence was not verified. Remaining transition and setup cases are not certified.

The repository suite has 27 passing offline tests, including nine cleanup-lifecycle tests. These are reference-harness and mocked-core checks, not production-adapter or complete live E2E coverage. Live cleanup is not certified. The source references and package hashes above describe the original authoring artifacts, not every later run. Target identity, privileges, current references, candidate approval and fresh-export reconciliation remain mandatory for each execution. Tenant names, credentials, business-unit values and transaction identifiers are intentionally excluded from this reusable summary.
