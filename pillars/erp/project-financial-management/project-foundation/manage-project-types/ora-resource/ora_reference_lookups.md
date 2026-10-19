# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Resolution Contract

First resolve the requested CSV column using CSV Column Intent Resolution in the input validation resource. Then resolve its value against the authority below. Accept codes, meanings, descriptions, names, translations, identifiers supported by the source, and ordinary natural-language phrasing in any language when evidence and context identify exactly one eligible member. Canonical tables are resolution targets, not restrictions on input language or exact wording. Block known invalid values, multiple plausible matches, or conflicting requests for one field. Missing offline authority alone follows the non-blocking deferral policy below.

Static tables below are the runtime authority for their exact scopes. They require no live request or export to determine membership. Seeded system membership cannot be added to or deleted through supported maintenance; the task also constrains its Boolean and burden-method domains. Display translations can vary without expanding membership. Each table includes every eligible code and its canonical meaning; excluded client-extension choices are not eligible. No optional active-date columns are needed because all eligible evidenced members are enabled with no end date.

## Dynamic Validation Policy

PT-POL-001 is this task package’s retained FSCR validation-disposition policy, not a claim of standing authorization from a previous user. It allows non-blocking service-layer validation when a documented dynamic source or supplemental eligibility check is unavailable. It does not override an incomplete registry, missing source contract, failed authentication/privilege check, or a required package/baseline gate. Use each verified REST, FSM export or other declared source when available. Otherwise state exactly "it has no data source", record validation_status=deferred_to_fusion and blocking=false, and continue preview and the approved FSM upload with the supplied CSV-ready value. Missing supplemental eligibility evidence is likewise deferred; do not claim it was verified.

This is a validation disposition, not an invented lookup match or a substitute data authority. Do not invent IDs, translate an unknown name into a guessed code, mark Exists=false from an unavailable source, or silently populate evidence-dependent defaults. Preserve supplied CSV-ready codes/names/numbers and omitted update values. If the required CSV representation itself is missing or ambiguous, ask only for that value. Known invalid values and actual conflicting matches remain validation failures. A negative result from a partial candidate source is not proof that a supplied value is invalid.

Fusion service validation is deferred to the normal core/data-loader upload; its process log/results are checked only in the later explicitly requested status or verification stage declared in SKILL.md. Accepted initiation returns in_progress without automatic follow-up and leaves deferred membership unverified. A successful preview does not certify deferred membership or imply import success. Missing-source deferral does not waive package shape, required inputs, known static/domain constraints, target identity or the normal upload approval and result checks. Disclose each deferred field and its risk in the immutable preview; the selected execution workflow must obtain approval for those exact bytes and disclosed dispositions. Same-request auto-approval remains limited to the identified load under core.data-loader; it is never a waiver of a failed rule.

SB4 was authoring evidence, not the current target's runtime business-value catalog. Do not hardcode editable records from it. A template proves CSV shape, not current membership.

## Dynamic Data Source Coverage

| Field or check | Offline data source | Coverage | Missing-source disposition |
|---|---|---|---|
| Current project type and children | Fresh PJF_MANAGE_PROJECT_TYPES FSM data export through shared.setup-export.task-level-export | Existing identity/baseline and child rows, not all possible referenced setup values | Baseline needed for a safe update remains a package-preservation prerequisite |
| Project/template use and transferred-asset-line state | it has no data source | No verified acquisition contract for this offline state check | Non-blocking deferred_to_fusion; retain supplied value and enforce restrictions only when their triggering state is known |
| PJF_PROJECT_TYPE.csv.SetCode | setIdSetsLOV REST via resolve_project_type_set | Full dynamic set code/name/description collection; no fixed UI eligibility filter | Validate from the complete current-target collection; unavailable retrieval remains non-blocking deferred_to_fusion with supplied set code |
| PJF_CLASS_CATEGORY.csv.ClassCategory | it has no data source | No verified complete category catalog acquisition | Non-blocking deferred_to_fusion; retain supplied category name |
| PJF_PROJECT_TYPE_TRANSLATION.csv.Language and SourceLang | it has no data source | Target installed/activated language eligibility not available offline | Non-blocking deferred_to_fusion; retain supplied language codes |
| PJF_PROJECT_TYPE.csv.AttributeCategory and Attribute1-Attribute10 | it has no data source | Target deployed main flexfield metadata not available offline | Non-blocking deferred_to_fusion; preserve supplied context code and segment values |
| PJF_CLASS_CATEGORY.csv.AttributeCategory and Attribute1-Attribute15 | it has no data source | Target deployed child flexfield metadata not available offline | Non-blocking deferred_to_fusion; preserve supplied context code and segment values |
| PJF_PROJECT_TYPE.csv.Name | workTypesLOV REST via resolve_project_type_work_type | Identity, canonical name and active dates | Use verified fields; unavailable offline membership is deferred |
| PJF_PROJECT_TYPE.csv.IndSchName | burdenSchedulesLOV REST via resolve_project_type_burden_schedule | ProjectId/AwardId null from base resource, TaskId null from q, inclusive dates from finder UserDate | UI business predicates covered; REST schedule-type lookup join can narrow coverage, so unavailable parity remains non-blocking |
| PJF_PROJECT_TYPE.csv.Name2 | projectsLOV REST via resolve_project_type_burden_project | Financial-project identity/name; supplemental effective organization checks: it has no data source | Validate available fields; defer missing eligibility without blocking upload |
| PJF_PROJECT_TYPE.csv.ElementNumber and Name1 | projectTasksLOV REST via resolve_project_type_burden_task, with resolved parent | Selected-project chargeable financial tasks filtered to nonnull ParentTaskId; REST structure/security restrictions can narrow UI coverage | If parent ID or candidate coverage is unavailable, retain supplied task number/project name and defer membership |



## Burden Cost Accounting Method
CSV columns: PJF_PROJECT_TYPE.csv.BurdenAmtDisplayMethod

| Lookup Code | Meaning |
|---|---|
| S | Include burden cost on same expenditure item |
| D | Create separate expenditure item for burden cost |

Authority: fixed S/D task attribute domain and UI radio bindings; see SRC-EO and SRC-UI in the source evidence index. Both radio choices write one shared field. Resolve one choice and emit S or D; conflicting same/separate requests block.

## Capital Cost Type
CSV columns: PJF_PROJECT_TYPE.csv.CapitalCostTypeCode

| Lookup Code | Meaning |
|---|---|
| B | Burdened |
| R | Raw |

Authority: PJC_CAPITAL_COST_TYPE seed data (SRC-PJC-SEED). Emit the code; conditional capitalization policy belongs in design enforcement.

## Asset Line Grouping Method
CSV columns: PJF_PROJECT_TYPE.csv.CipGroupingMethodCode

| Lookup Code | Meaning |
|---|---|
| ALL | All |
| EC | Expenditure category |
| ECNLR | Expenditure category nonlabor resource |
| EI | Expenditure item |
| EO | Expenditure organization |
| ET | Expenditure type |
| ETNLR | Expenditure type nonlabor resource |
| ORA_CIP_GPC | Project Process Configurator |

Authority: PJC_CIP_GROUPING_METHOD seed data (SRC-PJC-SEED). The supported subset of this task excludes CIPGCE (client extension); this package does not claim that the seeded lookup lacks that member. ALL denotes the grouping combination of expenditure category, expenditure type, and nonlabor resource. ORA_CIP_GPC denotes sources selected in Project Process Configurator. Emit the canonical code.

## Asset Cost Allocation Method
CSV columns: PJF_PROJECT_TYPE.csv.AssetAllocationMethod

| Lookup Code | Meaning |
|---|---|
| AU | Actual units |
| CC | Current cost |
| EC | Estimated cost |
| N | None |
| SC | Standard unit cost |
| SE | Spread evenly |

Authority: PJC_ASSET_ALLOCATION_METHOD seed data (SRC-PJC-SEED). CE (client extension) is excluded from this task’s supported subset; it is present in the seeded lookup. N is an actual choice, not an empty value. Emit the canonical code.

## Capital Event Processing Method
CSV columns: PJF_PROJECT_TYPE.csv.CapitalEventProcessing

| Lookup Code | Meaning |
|---|---|
| M | Manual |
| N | None |
| P | Periodic |

Authority: PJC_CAPITAL_EVENT_PROCESSING seed data (SRC-PJC-SEED). Emit the code; N is the explicit no-event-processing choice.

## Supplier Invoice Addition Treatment
CSV columns: PJF_PROJECT_TYPE.csv.VendorInvoiceGroupingCode

| Lookup Code | Meaning |
|---|---|
| M | As merged additions |
| N | As new additions |

Authority: PJF_VENDOR_INV_GROUPING_CODE seed data (SRC-PJF-SEED). These are all radio members, not the whole combined checkbox/radio field domain.

The same field also has a separately proven Boolean control transformation: selecting Use grouping method for supplier invoices writes G; clearing that checkbox writes M. An explicit radio choice N remains N. G has no seeded code/meaning pair in this lookup and is not represented as a fabricated static table member. Resolve combined intent before serialization; enabled grouping plus an explicit merged/new-addition request conflicts and requires clarification. Conditional compatibility belongs in design enforcement.

## Yes or No Options
CSV columns: PJF_PROJECT_TYPE.csv.EnableBillingFlag; PJF_PROJECT_TYPE.csv.EnableCapitalizationFlag; PJF_PROJECT_TYPE.csv.BurdenCostFlag; PJF_PROJECT_TYPE.csv.CostSchOverrideFlag; PJF_PROJECT_TYPE.csv.BurdenAccountFlag; PJF_PROJECT_TYPE.csv.InterfaceCompleteAssetFlag; PJF_PROJECT_TYPE.csv.BurdenCostJournalFlag; PJF_PROJECT_TYPE.csv.TotalBurdenedJournalFlag; PJF_PROJECT_TYPE.csv.CintSchOverrideFlag; PJF_PROJECT_TYPE.csv.SponsoredFlag; PJF_PROJECT_TYPE.csv.AutoAssetCreateFlag; PJF_CLASS_CATEGORY.csv.MandatoryFlag

| Lookup Code | Meaning |
|---|---|
| N | No |
| Y | Yes |

Authority: fixed Y/N task attribute domains and Boolean controls (SRC-EO, SRC-UI). These task domains have no maintenance path to admit other codes. Emit Y/N, including the child MandatoryFlag; do not serialize true/false.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_project_type | Every create/update/import | Fresh target joined project-type base, translations and class-category FSM export | Resolve supplied identity within resolved SetCode to one canonical ProjectType; aliases require evidence, not exact-English input | Exists, canonical ProjectType, current groups and children | Verified absence permits create only; ambiguity or incomplete export blocks |
| resolve_project_type_use | Protected field changes | it has no data source; use already supplied current target use/transfer evidence when present | Check known project/template use or transfer status; absent evidence returns deferred_to_fusion, blocking=false | Known InUse/HasTransferredAssetLines only; otherwise deferred status, never invented false flags | Unknown state is non-blocking; a proven protected change still fails |
| resolve_project_type_references | Referenced groups change | Individual verified resolver outputs or explicit deferred_to_fusion dispositions | Complete each applicable resolver as validated or deferred; the aggregate supplies no independent authority | Canonical resolved values or preserved supplied CSV-ready values; per-field validation status | Propagate known invalid/ambiguous results; missing offline sources or supplemental checks are non-blocking |
| verify_project_type_scope | Before validation | Effective task catalog and selected target context | Match PJF_MANAGE_PROJECT_TYPES and requested target | Verified scope | Block mismatch |
| verify_project_type_package | Before import | Fresh target template/export and generated package | Match exact three CSV members, headers, parent/child identities, row counts and checksum; template is not a dynamic value catalog | Verified CSV contract | Block unproven, changed or mixed package |
| resolve_project_type_burden_method | Burden accounting choice supplied or required | Burden Cost Accounting Method table | Resolve exactly one S/D member across both radios | PJF_PROJECT_TYPE.csv.BurdenAmtDisplayMethod = canonical code | Block unresolved or conflicting same/separate intent |
| resolve_project_type_capital_cost | Cost Type supplied or required | Capital Cost Type table | Resolve exactly one B/R member | PJF_PROJECT_TYPE.csv.CapitalCostTypeCode = canonical code | Block unresolved or ambiguous intent |
| resolve_project_type_asset_grouping | Grouping method supplied or required | Asset Line Grouping Method table | Resolve one eligible member; exclude CIPGCE | PJF_PROJECT_TYPE.csv.CipGroupingMethodCode = canonical code | Block unresolved, ambiguous or excluded choice |
| resolve_project_type_asset_allocation | Allocation method supplied or required | Asset Cost Allocation Method table | Resolve one eligible member; exclude CE | PJF_PROJECT_TYPE.csv.AssetAllocationMethod = canonical code | Block unresolved, ambiguous or excluded choice |
| resolve_project_type_capital_event | Event processing supplied or required | Capital Event Processing Method table | Resolve one M/N/P member | PJF_PROJECT_TYPE.csv.CapitalEventProcessing = canonical code | Block unresolved or ambiguous intent |
| resolve_project_type_supplier_grouping | Supplier invoice treatment supplied or required | Supplier Invoice Addition Treatment table and the separately proven checkbox transformation | Resolve one coherent checkbox/radio intent; preserve explicit M/N selection | PJF_PROJECT_TYPE.csv.VendorInvoiceGroupingCode = G, M or N according to resolved control intent | Block unresolved or contradictory control intents |
| resolve_project_type_boolean_flags | Any scoped Yes or No option supplied or required | Yes or No Options table and its exact CSV scopes | Resolve affirmative or negative intent in the selected field context | Each scoped CSV column = canonical Y or N | Block unresolved or conflicting intent |
| resolve_project_type_class_category | Classification assignments supplied or changed | it has no data source; no verified runtime acquisition for current PJF_CLASS_CATEGORIES_VL identities/default flags | Use authoritative category evidence when supplied; otherwise retain supplied category name and defer membership/default checks | PJF_CLASS_CATEGORY.csv.ClassCategory; category flags only when known | No source: non-blocking. Do not substitute an ID or guess category-dependent default flags |
| resolve_project_type_languages | Translation Language or SourceLang supplied | it has no data source; current target installed/activated language retrieval not authored | Use authoritative evidence when available; otherwise preserve supplied CSV-ready language codes and defer installation/activation checks | PJF_PROJECT_TYPE_TRANSLATION.csv.Language and SourceLang; deferred_to_fusion when unverified | No source: non-blocking. Request a missing code if representation cannot be resolved; never guess ISO-to-Fusion mappings |
| resolve_project_type_flexfields | Main or child descriptive flexfield values supplied | it has no data source; target deployed PJF_PROJECT_TYPES_DESC_FLEX and PJF_PROJ_TYPE_CLASS_CAT_DESC_FLEX metadata unavailable | If metadata is supplied, resolve context then segments; otherwise preserve supplied scoped context code/segment values and defer deployed validation | Exact supplied AttributeCategory and Attribute segment values; validation_status=deferred_to_fusion when unverified | No source: non-blocking. Preserve DFF footnote scopes; do not infer labels, value sets or defaults |
| resolve_project_type_auto_asset_mode | Automatic asset allocation mode supplied or changed | Verified task control serialization and fixed literal attribute domain; no seeded meaning table is claimed | Resolve associated-only intent to DIRECT_COSTS and all-cost intent to ALL_COSTS; explicit codes accepted; reject actual ambiguity or other codes | PJF_PROJECT_TYPE.csv.AutoAssetLineAllocateMode = DIRECT_COSTS or ALL_COSTS | Absent seeded meanings do not block this proven control mapping; do not fabricate a lookup table |

## Live Lookups

Invoke these only through the active workflow's declared read-only client after its prerequisites pass. Safely encode parameter values and paginate before claiming uniqueness or absence. Historical authoring notes report the Work Type date-filter request on cptcwxaqy with REST-Framework-Version: 9 and evaluation date 2026-09-11: HTTP 200, 27 rows across two pages, final hasMore=false, and no returned row violated the date predicate. All returned end dates were null; a populated end-date boundary was not exercised. Historical notes also describe the three burdening requests on cptcwxaqy with framework version 9; results and remaining parity limitations follow the lookup table.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_project_type_set | Set supplied or changed, or required for identity resolution | User-supplied set code, name, description, translation or ordinary-language intent; current target and authenticated identity | /fscmRestApi/resources/11.13.18.05/setIdSetsLOV?onlyData=true&limit=500 | Full response; require SetCode and SetName, retain Description when present | Fetch all pages once per validation run/target/identity and reuse for all CSV rows. Match a supplied code exactly; otherwise resolve wording to one distinct SetCode. No SetCodeFinder, name/description q, active-date, business-unit or project-unit restriction applies to this shared collection | PJF_PROJECT_TYPE.csv.SetCode = canonical returned SetCode; SetName and Description as evidence | Block proven no-match or ambiguity only with complete successful evidence. Unavailable/incomplete retrieval defers membership non-blockingly with supplied CSV-ready SetCode; never guess a code or substitute a set |
| resolve_project_type_work_type | Work type supplied or changed | Current target work types; supported identity/name/description intent; sysdate = current system date aligned with the Fusion database timezone, formatted YYYY-MM-DD at call time | /fscmRestApi/resources/11.13.18.05/workTypesLOV?onlyData=true&limit=500&fields=WorkTypeId,Name,Description,StartDateActive,EndDateActive&q=StartDateActive <= '{sysdate}' and (EndDateActive is null or EndDateActive >= '{sysdate}') | WorkTypeId, Name, Description, StartDateActive, EndDateActive | Substitute sysdate before sending the request; resolve one member active on that date, inclusive start/end and allowing a null end date; no evidenced billing/capitalization, set or project-unit predicate | PJF_PROJECT_TYPE.csv.Name = canonical Name, not WorkTypeId | Block proven inactive/invalid or ambiguous values; unavailable/incomplete retrieval or unverified target-date alignment defers membership non-blockingly with supplied work-type name |
| resolve_project_type_burden_schedule | Default cost burden schedule supplied or required | Current target burdenSchedulesLOV; sysdate = current system date aligned with the Fusion database timezone, formatted YYYY-MM-DD at call time | /fscmRestApi/resources/11.13.18.05/burdenSchedulesLOV?onlyData=true&limit=500&finder=ActiveBurdenSchedulesFinder;UserDate={sysdate}&q=TaskId is null&fields=BurdenScheduleId,Name,Description,FromDate,ToDate,Type | BurdenScheduleId, Name, Description, FromDate, ToDate, Type | Base resource enforces ProjectId and AwardId null; q enforces TaskId null even though TaskId is hidden from the response; finder enforces FromDate on/before UserDate and ToDate null or on/after UserDate. Substitute sysdate and resolve one eligible schedule. REST additionally joins schedule-type lookup data absent from the UI query; complete UI coverage is not established | PJF_PROJECT_TYPE.csv.IndSchName = canonical cost burden schedule name | Block proven invalid or ambiguous matches; unavailable date alignment, retrieval or complete UI coverage is non-blocking deferred_to_fusion with supplied schedule name |
| resolve_project_type_burden_project | BurdenCostFlag Y, BurdenAmtDisplayMethod S and BurdenAccountFlag Y | Current target projectsLOV; supplemental organization language/effectivity and UI-versus-REST security parity checks: it has no data source | /fscmRestApi/resources/11.13.18.05/projectsLOV?onlyData=true&limit=500&q=TemplateFlag = 'N'&fields=ProjectId,ProjectName,ProjectNumber,ProjectStartDate,ProjectFinishDate | ProjectId, ProjectName, ProjectNumber, ProjectStartDate, ProjectFinishDate | Base resource enforces ProjectCategory=FIN_EXEC; q enforces the UI TemplateFlag=N restriction. Resolve one candidate; do not use findFinancialProjects because it adds CreatedFromProjectId IS NOT NULL absent from the UI. Do not impose project active-date or CLOSED-status restrictions. Defer unavailable organization and security-parity checks | PJF_PROJECT_TYPE.csv.Name2 = canonical ProjectName; ProjectId for dependent task | Block proven invalid or ambiguous identity; missing supplemental proof or REST candidate absence without complete UI coverage is non-blocking with supplied project name |
| resolve_project_type_burden_task | Same-item component routing enabled and optional task supplied, after project resolution | Resolved destination ProjectId; current chargeable financial task candidates | /fscmRestApi/resources/11.13.18.05/projectTasksLOV?onlyData=true&limit=500&finder=findChargeableFinancialTasksByProjectId;ProjectId={resolvedProjectId}&q=ParentTaskId is not null&fields=ProjectId,TaskId,TaskName,TaskNumber,ElementType,ParentTaskId | ProjectId, TaskId, TaskName, TaskNumber, ElementType, ParentTaskId | Finder enforces selected ProjectId, ElementType=FINANCIAL and chargeable Y; q enforces nonnull ParentTaskId. Resolve one task and verify owning/destination projects are the same identity. No task active-date filter applies. REST additionally requires financial execution structure, a task-table row and REST security; exact UI coverage is not established | PJF_PROJECT_TYPE.csv.ElementNumber = TaskNumber; Name1 = canonical owning project name; Name2 remains canonical destination project name | Block actual ambiguity, missing required task number or proven parent mismatch; unavailable parent ID or absent conservative candidate is non-blocking with supplied task number and project names |

### Historical Burdening Filter Notes

These are inherited authoring summaries without retained process/response receipts in this package. They are not accepted package test results, proof of current target membership, or proof of identical UI/REST coverage. Current source references below substantiate only the contracts explicitly listed.

| LOV | UI eligibility and REST coverage | Live verification on cptcwxaqy |
|---|---|---|
| Default Cost Burden Schedule | UI requires project, task and award null and inclusive current-date eligibility. REST base covers project/award null; TaskId-null q and dated finder complete the business predicates. REST also joins schedule-type lookup data | HTTP 200; active finder plus TaskId-null returned 73 rows, hasMore=false. Inverse TaskId-not-null returned 0. Existing end-dated schedule was included at its end date and excluded the next day; finder with explicit UserDate and explicit date q returned identical sets, 65 then 64 rows |
| Project Name | UI requires FIN_EXEC and TemplateFlag=N, effective session-language organization/project-unit/BU joins and a project-status reference join. REST base plus TemplateFlag=N q covers the first two; supplemental joins/security parity: it has no data source. Removed finder imposed an extra CreatedFromProjectId-not-null restriction | HTTP 200; corrected request returned 25 rows, hasMore=true, so no full catalog/uniqueness claim. Targeted candidate returned 1 without the old finder and 0 with it. TemplateFlag=Y negative control returned 0 |
| Task Name | UI requires selected project, FINANCIAL element, chargeable Y and nonnull parent. Finder plus ParentTaskId-not-null q covers these; REST additionally restricts financial execution structure, task-table membership and security | HTTP 200 for one selected project; finder and finder-plus-parent filter each returned the same 2 tasks, hasMore=false; inverse parent-null returned 0. Response project/type/parent fields satisfied the predicates; chargeability is established by finder source |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| Fetching a GET-all LOV collection | Use core.fusion-api.rest-api-client through the declared read-only workflow, with onlyData=true, limit=500 and the REST-Framework-Version header resolved from that workflow. Fetch once per validation run, target, authenticated identity and eligibility-parameter scope; reuse for every applicable CSV row. Task collections are scoped per resolved ProjectId; date-filtered collections per captured date. Preserve all UI eligibility filters; refresh on a new run, identity/target change or known reference-data change |
| GET-all pagination | If hasMore=true, repeat the same request with offset = returned offset + returned limit; honor the server's returned limit rather than assuming 500. Accumulate and deduplicate by stable identity (SetCode for sets) until hasMore=false. Failed pages, conflicting duplicate identities, missing required fields or nonadvancing pagination cannot establish absence or uniqueness; defer unavailable dynamic validation non-blockingly under this task's policy |
| Set REST collection | Use no finder, q or fields projection for setIdSetsLOV. Resolve code/name/description intent locally from the completed collection and preserve canonical SetCode. No per-row REST call or reference-data-set export is required. Verified on cptcwxaqy: HTTP 200, 304 distinct SetCodes, limit=500, hasMore=false; same identities as the earlier complete 13-page unfiltered scan |
| Preparing burdening schedule, project or task lookup | Resolve REST-Framework-Version from the selected core workflow and verify expanded-query compatibility. For schedule UserDate, calculate {sysdate} at call time in YYYY-MM-DD using the Fusion database timezone; keep that date for all pages of one lookup and recalculate for the next invocation. Substitute resolved IDs and date placeholders before safely URL-encoding each query parameter. Preserve all authored eligibility predicates when adding a selective identity/name search. Paginate before claiming uniqueness; a successful REST response alone does not prove identical UI coverage |
| Preparing resolve_project_type_work_type REST request | Calculate the current system date (SYSDATE intent) at runtime using the Fusion database timezone and format it as YYYY-MM-DD. Replace both {sysdate} placeholders with that date literal before URL-encoding the q value. Do not send SYSDATE, TRUNC(SYSDATE), or an unresolved placeholder to REST, and do not retain a fixed authoring-time date. Use the same captured date for all pages of one lookup; calculate a fresh date for each new lookup invocation. Use the selected core workflow's REST-Framework-Version header only after confirming support for the compound filter's expanded syntax. The live check used an explicit evaluation date and did not verify Fusion database timezone alignment; unavailable date alignment or lookup validation remains non-blocking deferred_to_fusion |
| Static choice supplied | Use its one local table; no live lookup or duplicate dynamic route |
| Dynamic source or supplemental eligibility check is unavailable | State it has no data source; record deferred_to_fusion with blocking=false and continue with supplied CSV-ready values. Use the normal FSM upload for service validation; do not invent an exploratory retrieval route |
| Group or child collection omitted on update | Preserve existing rows and values; do not silently clear them |
| Name, Name1, Name2 or ElementNumber supplied | Use exact scope: work-type name, task-owning project name, burden destination project name, and task number respectively |
| Default capitalized-interest schedule requested | No exported destination exists; block this CSV intent. IndSchName is the cost burden schedule and CintSchOverrideFlag is only the override Boolean |
| Static membership translated or paraphrased | Resolve semantic intent to one canonical member; never require exact English wording |
| Reference evidence unavailable | For offline dynamic checks, disclose it has no data source and defer non-blockingly. Missing required CSV values, package/target evidence, actual conflicts and known invalid values remain separate checks |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PTYPE.FIND_TYPE | step | 2 | reference_lookup | resolved->PTYPE.RESOLVE_REFERENCES;deferred->PTYPE.RESOLVE_REFERENCES;failure->PTYPE.RETURN_ISSUES | PTYPE.VALIDATE_INPUT | stop | Resolve required baseline; unavailable offline use-state may be explicitly deferred |
| PTYPE.RESOLVE_REFERENCES | step | 3 | reference_lookup | resolved->PTYPE.APPLY_DEFAULTS;deferred->PTYPE.APPLY_DEFAULTS;failure->PTYPE.RETURN_ISSUES | PTYPE.FIND_TYPE | stop | Resolve changed references and conditional options before dependent defaults |

## Source Evidence Index

Reviewed October 9, 2026. ADE discovery used series FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64 and excluded test files. The current FSCR workspace contains no Fusion source view; exact files were read from the central read-only label 261008.1801.S, not from a customer environment. Paths below are relative to fusionapps under that label. Development-label evidence does not establish that a particular tenant runs identical code; verify the target package and supported release at runtime.

| Source ID | Source | Rules Supported | Evidence Boundary |
|---|---|---|---|
| SRC-DOC | https://docs.oracle.com/en/cloud/saas/project-management/26d/fapfm/create-project-types.html | Project-type identity, set, inherited financial options, burden schedule/override decisions, capitalization choices and classifications | Public 26D guidance; does not establish CSV serialization, complete seeded codes or UI/REST parity |
| SRC-UI-CREATE | User-supplied Create Project Type screenshots, October 9, 2026: codex-clipboard-6c0e0efe-1765-4ce6-9d9d-eac8e031ca9c.png; codex-clipboard-c8b5477d-bc1f-4985-a68c-4da5a81aee61.png; codex-clipboard-29bd98ce-43cf-4ba2-a4ab-32420480704c.png | Required-field markers, prepopulated From Date, initial disabled burdening/capitalization controls, selected supplier grouping and empty Classifications table | Visual evidence of one blank UI state only; no save, enabled-feature behavior, target import, or reproduction of the reported Add Row error was observed |
| SRC-UI-SEPARATE | Three user-supplied Create Project Type screenshots, October 12, 2026, accompanying the repair request and linked prior create thread | Burdening/billing selected; D radio selected; component checkbox and destination project/task disabled; override and both journal checkboxes selected; capitalization disabled and empty Classifications | Configured unsaved UI state only; corroborates mode applicability and the create-default policy, not a successful save, import setter order or a general default for billing/overrides |
| SRC-EO | prj/components/projectsFinancials/foundation/setup/projects/model/src/oracle/apps/projects/foundation/setup/projects/model/entity/ProjectTypeEO.xml | Description/name lengths (312/322); N/S/G defaults (237-883); ALL_COSTS and fixed allocation domain (975-1003); unique name/set and capitalization validators (1060-1200) | SHA-256 46af668a7d39de454820d0c978d7c21bb6c72aec10cc83ab8f1c8ddaf5707c32 |
| SRC-EOIMPL | prj/components/projectsFinancials/foundation/setup/projects/model/src/oracle/apps/projects/foundation/setup/projects/model/entity/ProjectTypeEOImpl.java | setEnableCapitalizationFlag (387-395); protected-use validators (1290-1339); supplier transitions (1815-1905); EI/G rejection (1911-1921); disabled-capitalization consistency (1927-1950) | SHA-256 9db27ee5c628658671eda018f28283a44a98c58e5a68004a9936d3581354b125; setter existence does not prove FSM setter order |
| SRC-UI | prj/components/projectsFinancials/foundation/setup/projects/ui/src/oracle/apps/projects/foundation/setup/projects/ui/bean/CustomEventHandler.java | capitalFlagValueChangeList (348-383); sponsoredFlagChkBoxChangeListener (407-438); burdenFlagChangeListener (453-509); save-warning behavior (529 onward) | SHA-256 632acfc3df0537057d3747160f30042869d102f74b5ca95a44e1d4047fc72573; UI event behavior only, not import normalization |
| SRC-PJC-SEED | prj/pjc/db/data/PjcCommon/StandardLookupTypeSD.xml | PJC_ASSET_ALLOCATION_METHOD (4824-4954); PJC_CAPITAL_COST_TYPE (5175-5225); PJC_CAPITAL_EVENT_PROCESSING (5226-5292); PJC_CIP_GROUPING_METHOD (6081-6243) | SHA-256 fcd100e265437108113c20e7de6a0bdaee89b2204290cf59e11428caf28c833e; task subset exclusions are separate from seeded membership |
| SRC-PJF-SEED | prj/pjf/db/data/PjfCommon/StandardLookupTypeSD.xml | PJF_VENDOR_INV_GROUPING_CODE M/N (19980-20030) | SHA-256 bf9ca7181d3cddf96512ffe50cbc5f289afed2c551ce26bcba6bf707f59be6d0; G is a combined control value, not a member of this radio lookup |
| SRC-WORK | prj/components/projectsFinancials/foundation/setup/projects/restModel/src/oracle/apps/projects/foundation/setup/projects/restModel/view/WorkTypeLovVO.xml | Name and active-date attributes (45-73); date criteria (197 onward) | SHA-256 2a801cfd79aa09c59dbe4fd0e3ff946696eb5f3a37870045d708a7570647182a; no target-timezone or populated-end-date runtime verification |
| SRC-SCHEDULE | prj/components/projectsFinancials/foundation/setup/burdenRates/restModel/src/oracle/apps/projects/foundation/setup/burdenRates/restModel/view/BurdenScheduleLovVO.xml | Additional lookup inner join (42-62); inclusive date criteria (502-538); ActiveBurdenSchedulesFinder/UserDate (584-592) | SHA-256 edecfc2c51370946d76c17f70c85927d7bae232939f91cd3ebd6d401891dd73c; complete UI coverage remains unproven |
| SRC-TASK | prj/components/projectsFinancials/foundation/projectDefinition/restModelLov/src/oracle/apps/projects/foundation/projectDefinition/restModelLov/view/TaskLOVVO.xml | Financial element and chargeable defaults (36/49); FIN_EXEC and structure joins (73-105); project-scoped finder (600 onward) | SHA-256 63a9adbe337ad0cb387b1a395460d814d5535fb6415760b731a0610e228e4d1c; does not prove same-session UI/security parity |
| SRC-PROJECT | prj/components/projectsFinancials/foundation/projectDefinition/restModelLov/src/oracle/apps/projects/foundation/projectDefinition/restModelLov/view/ProjectLovPVO.xml | FIN_EXEC and non-template base criteria (446-471) | SHA-256 b4dd338a283d07df62b77ed1f0aed7a5f8e3c0476acbea4acb444d70e556a8a3; supplemental organization/security parity is still unavailable |
| SRC-FSCR | SKILL.md; core/data-loader/SKILL.md; core/data-loader/references/task-rule-registry-execution.md | Preservation, exact package/approval, no invented identity, bounded execution handoff and PT-POL-001 | FSCR package policy, not an Oracle product constraint or a standing user authorization |
| SRC-HISTORICAL | Historical work-type, set and burdening notes above | Context for authored lookup requests and disclosed limitations | No retained live receipts; not used to satisfy this package’s validation evidence gate |

The set collection request is retained from the existing task contract; this audit did not independently establish its complete UI eligibility or re-run it. Its runtime resolver requires complete successful retrieval before claiming absence or uniqueness. A failed authentication/authorization preflight cannot be relabelled as missing dynamic membership to bypass core workflow gates.
