# Design enforcement

These rules are reusable across target environments. Planner readiness means the execution rules are defined; all applicable runtime checks must still pass. The portable execution contract in ../references/execution-contract.md defines environment selection, input mapping, FSM compatibility checks and the in-memory Data Loader handoff. A missing product qualification is an explicit runtime blocker, never implicit approval.

<!-- fscr-supported-operations: create, update -->
<!-- fscr-evidence-unresolved-operations:  -->

Supported create/update operations are bounded to organization-setting rows
under the shipped transport profile. A required setup-option write remains
blocked by FSM_ALIAS_COLLISION; these markers do not waive that check.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Task ownership | Prove exact rows and operations belong to this task. |
| 2 | Value and lifecycle contracts | Resolve applicable field and dependency blockers. |
| 3 | Governed handoff | Require current ready plan before handing validated intent to Data Loader. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any candidate package | Error | qualify_fsm_transport | Requested rows exceed the reviewed control mapping, or qualify_fsm_transport fails | Keep EXM_CASH_ADV_SETUP_AND_POLICY visible as a shared alias; do not edit cash-advance settings or assume its duplicate rows can be dropped | No inferred fix |
| Organization setting intent | Error | resolve_setting_code | Requested control is absent from the reviewed mapping, or proposed code conflicts with that mapping | Resolve each requested control to its exact owned code; retain an authoring gap for additional controls | No |
| Option or auto-submission intent | Error | resolve_auto_submission_value | ValueCode is outside the confirmed System enum Y/N | Use the explicit Yes/Y or No/N mapping; never turn blank into No | No |
| Create or update requested | Error | qualify_fsm_transport | Runtime template/alias/serialization checks have not passed | Preserve operation intent and return the exact compatibility error; no readiness override can supply missing product evidence | No |
| Request to edit an audit or identity field as a business value | Error |  | Audit edits or cross-scope identity ambiguity | Stop and correct the request; readiness override cannot authorize unsafe keys, audit edits or ownership bypass | No |
| Receipt/card matching setup | Error |  | A category or merchant matching change requests BU-only scope, or global scope has not been explicitly selected | SRC-HELP-26D defines matching as global only. Explain the impact and ask whether to apply globally or leave matching unchanged; do not reinterpret a BU request | No |
| Runtime or package handoff | Error | qualify_fsm_transport | Any applicable rule failed or lacks its required evidence | Return the exact runtime blocker and next action; authored planner readiness never waives product qualification | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_setting_code | Setting code selection | Exact control, owned SettingCode and scope from Reviewed control mappings | ora_reference_lookups.md |
| resolve_auto_submission_value | Auto-submission value selection | Exact Y/N from confirmed System seeds; no blank default | ora_reference_lookups.md |
| qualify_fsm_transport | Before composition and every handoff | Exact task/schema, deterministic alias selection, and applicable serialization evidence | ora_reference_lookups.md |

## Shared package boundary

The same-task metadata includes EXM_ORG_SETTING.csv, EXM_SETUP_OPTION.csv, and EXM_CASH_ADV_SETUP_AND_POLICY.csv. The latter two reference the same service/XML node. This proves a shared package relationship, not independent operation ownership, safe row duplication, or safe removal. Oracle FSM guidance requires retaining every CSV member and allows unselected business-object files to retain their headers with no data rows. Keep that general rule distinct from this shared-alias collision: the task-specific transformation/order behavior still needs qualification before constructing candidate rows. The selected task alias is EXM_SETUP_OPTION, as explained below. Never duplicate broad setup-option rows as a workaround.

### Applicability: no setup-option changes

Use the fresh same-target baseline and `split_verified_noops` to retain controls already satisfied in the result, without rewriting them. If only EXM_ORG_SETTING changes remain, both setup-option CSVs stay header-only and alias selection is not applicable. The task caller skips an entirely empty service when its empty-service profile is enabled; independently MigratorHelper.readXML invokes ADF readXML only for a positive row count (lines 677–683), so a header-only selected alias contributes no setting rows. This does not qualify a populated alias or blank/global organization-setting fields. Apply all remaining transport checks.

### Selected alias and exact remaining dependency

The captured template has three business-object CSV descriptions, but only `EXM_ORG_SETTING` and `EXM_SETUP_OPTION` have migration-object rows with `MigrateFlag=Y`. Select **`EXM_SETUP_OPTION`** as the task alias; do not ask the user to choose again. This follows the migration-object selection in the captured task metadata and the user authorization to use either alias. Both setup-option aliases have `/SetupOptionVO/SetupOptionVORow` and `NodeSequence=1`. This selection expresses task intent; it does not establish that the framework excludes the other alias during transformation.

`XmlCSVAMImpl.prepareForTransform` groups the runtime BusinessObjectCollection by XML file and node level, then stores each object in a TreeMap keyed by NodeSequence (source lines 248–335). Consequently, if both aliases reach the same file/level with sequence 1, the later insertion replaces the earlier one. `CSVXmlTransform` subsequently assigns the root VO while processing the selected CSV list (lines 160–265) and writes that root (lines 579–597). This is source evidence of an order-sensitive collision, not proof that both aliases merge.

The actual **task CSV import** chain is now captured from `MigratorAMHelper.transformCSVToXmlForImport` (SRC-FSM-TASK-IMPORT, label `FSM_MAIN_GENERIC_261001.0300.S`). It is distinct from the serialized-control overload previously investigated:

1. FSCR Data Loader preserves an existing native FSM ZIP and identifies it through `ASM_SETUP_CSV_METADATA.xml`; it does not select an Expenses alias.
2. The task caller obtains all business objects for the service and retains every present CSV, including header-only files (lines 1516–1549). Its empty-file check skips the whole service only when **all** service CSVs are empty (lines 2019–2069). The `ORA_ASM_SKIP_EMPTY_CSV` default therefore cannot select one populated alias over a header-only sibling.
3. The caller reads task metadata into `MigrationProcessCSVMetadata`, filters its business-object accessor by service short names, and appends every matching metadata object to a new collection (lines 1555–1599). It copies each object's NodeSequence from the task package. It does not filter these rows by migration-object `MigrateFlag`.
4. It passes that new collection directly to `processCSVToXmlTransform(zip, control, status)` (lines 1666–1681). This path does **not** decode `CSV_PROCESS_CONTROL_XML`; supplying or manipulating that file is not a task-import alias solution.
5. `XmlCSVAMImpl.prepareForTransform` retains one object for each XML file/node-level/NodeSequence key, with the later insertion replacing the earlier one. `processCSVToXmlTransform` builds its CSV list only from those surviving keys (lines 83–131). For the captured identical setup-option paths and sequence 1, a header-only alias can therefore suppress the populated alias, depending on collection order.
6. The metadata VO declares transient rows with ProcessId/BusinessObjectShortName as key and no sort (SRC-FSM-CSV-METADATA-VO). The caller sets a row match but no sort for that accessor; the separate batch accessor sorts ImportSequence. XML document order is not evidence of the ADF accessor's iteration order. Do not choose a winner from ZIP order, XML order, BO name, or MigrateFlag.
7. Expenses `ExpenseSetupOptionServiceAMImpl.importData` consumes `EXM_SETUP_OPTION.xml` and resolves keys/scope; it cannot recover a CSV excluded upstream.

The earlier `BusinessObjectCollectionHelper` capture remains useful for service-wide metadata construction, but it is not the final task-import collection. The missing caller dependency is closed. The additional `XmlAMImpl.getMetadataBusinessObjectCollection` capture (lines 286–319) binds pBusinessObjectId to BusinessObjectMetadataVO; that VO joins all business objects sharing the selected object's service. Its ORDER BY applies to that intermediate collection, not the final CSV-metadata accessor iteration. This is not evidence of deterministic final alias selection. **The remaining product qualification for populated setup-option writes is deterministic alias selection on the deployed task import and its exact candidate serialization.** Organization-only writes now use the shipped ../references/fsm-transport-profile.md; do not treat their qualification as a populated-alias solution. A supported same-task transformed-XML diagnostic/round-trip fixture must demonstrate the requested OptionCode and BuName, exactly once, including blank/audit/global handling; alternatively obtain the owning FSM contract or a framework fix that explicitly selects one alias. Do not manufacture this evidence from a local simulation.

Retain every original CSV and metadata member. Do not submit a customer package based on an assumed order, edit metadata to force a winner, or duplicate values across aliases as an unqualified workaround. Identical field/value maps in both aliases would make the reviewed collision order-independent in a local model, but this is not by itself a qualified end-to-end FSM import contract. Preserve this distinction and do not silently convert that inference into supported behavior.

The explicit maintainer branch in [option-alias qualification](../references/option-alias-qualification.md) permits testing the implemented identical-row candidate on a user-selected non-production target. This branch evaluates candidate conformance, exact test intent and ordinary target/approval gates; it does not assert customer transport qualification. Record that boundary in Task Hook results. Every other dependency and rule remains mandatory, with no readiness override. Reusable customer promotion requires the declared successful import/read-back evidence for the tested scope and operation.

The reviewed framework reference is `FSCORE_MAIN_GENERIC`; compatibility with the target deployed framework is still unverified. Alias names are seeded business-object metadata, not OAuth environment aliases; runtime metadata must nevertheless be checked for the target release.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AUTO_DESIGN | step | 50 | design_enforcement | passed->AUTO_HANDOFF | AUTO_DEFAULTS | stop | Task validation before any Data Loader handoff |

## Evidence

| Source ID | Source | Location | Revision boundary | Status |
|---|---|---|---|---|
| SRC-FSM-TEMPLATE | Same-task template export | Same-task ASM_SETUP_CSV_METADATA.xml and exact template headers; source artifacts retained in the project workspace | 11.13.27.01.0 | Confirmed |
| SRC-BO-SEEDS-COMPLETE | SetupBusinessObjectSD.xml | https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/fun/db/data/FinFunShared/SetupBusinessObjectSD.xml | FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64; index 2026-10-09 | Confirmed |
| SRC-ORG-VO | OrgSettingVO.xml | https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/shared/model/src/oracle/apps/financials/expenses/setup/shared/expenseOrgSettingService/view/OrgSettingVO.xml | FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64; source snapshot hash in evidence/classic/manifest.json; reviewed 2026-10-09 | Confirmed |
| SRC-OPTION-VO | SetupOptionVO.xml | https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/shared/model/src/oracle/apps/financials/expenses/setup/shared/expenseSetupOptionService/view/SetupOptionVO.xml | FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64; source snapshot hash in evidence/classic/manifest.json; reviewed 2026-10-09 | Confirmed |
| SRC-UI-DA-PAGE | FinExmSetupOptionsDigitalAssistant.jsff | https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/options/ui/public_html/oracle/apps/financials/expenses/setup/options/ui/page/FinExmSetupOptionsDigitalAssistant.jsff | FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64; indexed 2026-10-09; deployed parity unverified | Confirmed |
| SRC-FSM-CSV-TRANSFORM | CSVXmlTransform.java | https://codesearch.oraclecorp.com/source/xref/FSCORE_MAIN_GENERIC/fscore/components/setupHub/remoteApp/publicModel/src/oracle/apps/setupHub/xml/transform/CSVXmlTransform.java | FSCORE_MAIN_GENERIC; index 2026-10-09 20:00:03 UTC; deployed framework revision unverified | Confirmed |

## Additional source references

| Source ID | Source | Location | Revision boundary | Status |
|---|---|---|---|---|
| SRC-HELP-26D | Set up Expense Assistant | https://docs.oracle.com/en/cloud/saas/financials/26d/faiex/set-up-expense-assistant.html | 26D; reread 2026-10-12 | Confirmed matching scope |
| SRC-FSM-CSV-GUIDE-26B | Using Functional Setup Manager, Manage Setup Using CSV File Packages | https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/using-functional-setup-manager.pdf | 26B, page 30; newer 26C/26D HTML retrieval unavailable on 2026-10-12 | Confirmed general package-member rule; not alias qualification |
| SRC-FSM-CSV-AM | XmlCSVAMImpl.java | https://codesearch.oraclecorp.com/source/xref/FSCORE_MAIN_GENERIC/fscore/components/setupHub/remoteApp/publicModel/src/oracle/apps/setupHub/xml/model/applicationModule/XmlCSVAMImpl.java | Saved snapshot; lines 83–131, 248–343 and 438–589; deployed revision unverified | Confirmed control serialization, import decode and collection-driven grouping |
| SRC-OPTION-AM | ExpenseSetupOptionServiceAMImpl.java | https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/exm/setup/shared/model/src/oracle/apps/financials/expenses/setup/shared/expenseSetupOptionService/applicationModule/ExpenseSetupOptionServiceAMImpl.java | Saved snapshot, lines 125–177; deployed parity unverified | Confirmed import consumes EXM_SETUP_OPTION.xml |
| SRC-FSM-BO-COLLECTION | BusinessObjectCollectionHelper.java | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSCORE_MAIN_GENERIC_260924.1205&p13_path=fscore%2Fcomponents%2FsetupHub%2FremoteApp%2FpublicModel%2Fsrc%2Foracle%2Fapps%2FsetupHub%2FbusinessObject%2FBusinessObjectCollectionHelper.java | FSCORE_MAIN_GENERIC_260924.1205; captured 2026-10-12; target deployed revision unverified | Confirmed service-wide collection without alias filtering or deterministic BO order |
| SRC-FSM-COMMON-MODEL-UTIL | CommonModelUtil.java | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/commonSetup/util/src/oracle/apps/setup/commonSetup/util/model/CommonModelUtil.java | FSM_MAIN_GENERIC_261001.0300.S; source captured 2026-10-12 | Confirmed profile getter and Y fallback; caller now captured in SRC-FSM-TASK-IMPORT; target value unverified |
| SRC-FSM-MIGRATOR-CONSTANTS | MigratorConstants.java | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/model/src/oracle/apps/setup/migrator/model/common/MigratorConstants.java | FSM_MAIN_GENERIC_261001.0300.S; source captured 2026-10-12 | Confirmed filename and empty-CSV marker constants only |
| SRC-FSM-TASK-IMPORT | MigratorAMHelper.java | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/model/src/oracle/apps/setup/migrator/model/applicationModule/MigratorAMHelper.java | FSM_MAIN_GENERIC_261001.0300.S; captured 2026-10-12; deployed parity unverified | Task import reconstructs collection from service-matching CSV metadata rows and calls direct collection overload. No alias-specific filtering; empty check skips entire service only when every CSV is empty. Metadata VO iteration order controls insertion. |
| SRC-FSM-CSV-METADATA-VO | MigrationProcessBusinessObjectCSVMetadataVO.xml | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/model/src/oracle/apps/setup/migrator/csv/model/view/MigrationProcessBusinessObjectCSVMetadataVO.xml | FSM_MAIN_GENERIC_261001.0300.S; captured 2026-10-12; deployed parity unverified | Transient metadata VO with ProcessId and BusinessObjectShortName key; no declared sort. This does not establish a stable readXML/accessor iteration order. |
| SRC-FSM-IMPORT-COLLECTION | XmlAMImpl.java getMetadataBusinessObjectCollection | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/model/src/oracle/apps/setup/commonSetup/xml/model/applicationModule/XmlAMImpl.java | FSM_MAIN_GENERIC_261001.0300.S; reviewed 2026-10-13 | Builds service metadata collection for task import; CSV mode and selected object bind |
| SRC-FSM-IMPORT-COLLECTION-VO | BusinessObjectMetadataVO.xml | https://adehub.oraclecorp.com/r/adehub/adehub/code-browser?p13_label_name=FSM_MAIN_GENERIC_261001.0300.S&p13_path=fsm/components/setup/asm/model/src/oracle/apps/setup/commonSetup/xml/model/view/BusinessObjectMetadataVO.xml | FSM_MAIN_GENERIC_261001.0300.S; reviewed 2026-10-13 | SQL selects same-service objects ordered by short name; not the final CSV-metadata collection order |

## Organization-setting profile

Use [the shipped transport profile](../references/fsm-transport-profile.md) for
organization-only writes and its documented source and verified-import boundaries. It
requires no customer-provided import ZIP. Other operations keep their explicit
qualification checks.
