# Legal Reporting Unit HCM Information Design Enforcement

## Purpose

Defines mandatory identity, classification, EFF, effective-date,
presentation, synchronization, and Core Data Loader route gates. It does not
perform lookups, build loader files, approve mutations, or invoke Fusion writes.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact LRU and current classification properties |
| 2 | Synchronize organization | Route only ManageLegalReportingUnit through Core Data Loader once for the exact fresh LRU and refresh before any branch read |
| 3 | Resolve classification identity when required | Treat `Both` or `Yes to both` as explicit Yes/Yes while the paired questions are pending, then resolve one OrganizationId from organizationsLOV using exact Name plus ClassificationCode=HCM_LRU; do not require an active branch root |
| 4 | Change classification when required | Map both answers internally, route only ManageLegalReportingUnitHcmClassifications through Core Data Loader, execute once after its separate approval gate, and refresh |
| 5 | Branch and localize | Only after a branch is active, resolve every applicable root for today's or the user-selected date, exact CategoryCode describe, context, and value set |
| 6 | Validate CUD semantics | Enforce EFF-only changes, effective boundary, create-versus-update, cardinality, and eligible delete scope |
| 7 | Enforce mutation routes | Route classification, EFF, and date-effective delete mutations only through Core Data Loader |
| 8 | Decide readiness | Return synchronization readiness, read completion, or Core Data Loader handoff only when no blocker remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LRU-DES-01 | Every request | Blocking | find_lru_by_exact_name | Zero or multiple exact Name matches | Supply one unique Name | Input fix |
| LRU-DES-02 | Every branch read, EFF mutation precheck, or history operation after classification is active | Blocking | resolve_active_lru_branch_identity | Required same-session ManageLegalReportingUnit synchronization evidence is absent, older than 24 hours, or the exact EstablishmentId root query did not return current OrganizationId | Complete or reconcile synchronization once for the exact fresh LRU, then query each active root by EstablishmentId; never invent or substitute the identifier | No |
| LRU-DES-03 | A classification change is required after synchronization | Blocking | find_lru_by_exact_name | Either business-facing Tax Reporting Unit or Reporting Establishment Yes/No answer is absent | Ask both exact classification questions | Input fix |
| LRU-DES-04 | A classification change is required after synchronization | Blocking | resolve_lru_classification_organization | organizationsLOV does not yield one distinct OrganizationId for exact Name and ClassificationCode=HCM_LRU, or ManageLegalReportingUnitHcmClassifications is absent or stale, its row omits that organizationId or the advanced-search establishmentId, either target flag, or RestAction POST, or ManageLegalReportingUnit is included in the classification archive | Resolve the pre-classification identity without an active-root prerequisite, rebuild the classification-only archive from current live loader metadata, and hand it to core.data-loader | Mapping fix |
| LRU-DES-05 | Every Get | Blocking |  | A supplied date is ambiguous or not normalized to YYYY-MM-DD, is not appended to the top-level GET, or child links are reused from another effective date | Use today's system date by default; otherwise append &effectiveDate=<YYYY-MM-DD> to the top-level GET and follow only its returned child links | Input fix |
| LRU-DES-06 | Classification loader process completed | Blocking | find_lru_by_exact_name | TruStatus or ReStatus does not match the approved active/inactive target after refresh | Stop and do not replay automatically | No |
| LRU-DES-07 | Tax Reporting Unit property is A | Blocking | resolve_tax_reporting_unit_root | The effective root, CategoryCode, or EFF envelope is absent or ambiguous | Refresh the read-only root | Lookup fix |
| LRU-DES-08 | Reporting Establishment property is A | Blocking | resolve_reporting_establishment_root | The effective root, CategoryCode, or EFF envelope is absent or ambiguous | Refresh the read-only root | Lookup fix |
| LRU-DES-09 | Tax Reporting Unit property is A | Blocking | resolve_tax_reporting_unit_eff_metadata | Metadata scope differs from the environment, resource, or exact CategoryCode | Refresh current polymorphic describe | Lookup fix |
| LRU-DES-10 | Reporting Establishment property is A | Blocking | resolve_reporting_establishment_eff_metadata | Metadata scope differs from the environment, resource, or exact CategoryCode | Refresh current polymorphic describe | Lookup fix |
| LRU-DES-11 | A context or segment is requested | Blocking | read_lru_eff_context | The context, segment, row identity, cardinality, or returned link is absent, stale, or ambiguous | Refresh link-bearing context data and do not construct a path | Lookup fix |
| LRU-DES-12 | A segment has a value set | Blocking | validate_lru_segment_value | The proposed value does not resolve to one typed stored value for the declared target attribute | Resolve one current compatible value | Lookup fix |
| LRU-DES-13 | View output | Blocking | read_lru_eff_context | Branch details are absent, an EFF Name/context heading is absent, configured segments are not shown with display values, or a zero-row context is hidden, treated as an error, or has its empty fields enumerated | Show branch details first, then EFF Name and context headings; show configured segments only, or `No configured segments` for a zero-row context | Output fix |
| LRU-DES-14 | Any ordinary Edit | Blocking |  | Name, Status, classification, CategoryCode, or another parent attribute would change outside the explicit classification route | Reject the parent change; ordinary Edit mutates only supported EFF data | No |
| LRU-DES-15 | An EFF context changes | Blocking | read_lru_eff_context | Create versus update is not derived from current effective row existence | Create for zero rows or update the one selected current row | Lookup fix |
| LRU-DES-16 | An EFF segment changes | Blocking | read_lru_eff_context | The segment is unknown, read-only, display-only, or belongs to another context | Map only the describe-approved typed stored attribute | Input fix |
| LRU-DES-17 | Every Edit | Blocking | resolve_lru_loader_contract | Operation EffectiveStartDate is missing or earlier than any affected top-level organization's current EffectiveStartDate | Obtain a YYYY-MM-DD date valid for every affected organization | Input fix |
| LRU-DES-18 | Operation date equals an affected top-level organization's current EffectiveStartDate | Blocking | resolve_lru_loader_contract | The selected EFF branch omits ModifyOrganizationUnitForChildCorrect, a new child omits a required parent locator or populates OrgInformationId, EffectiveStartDate, or EffectiveEndDate, or the action populates OrgInformationId | Add ModifyOrganizationUnitForChildCorrect with blank action OrgInformationId; for a new POST child populate available fresh parent locators, leave all child identity/date fields blank, and put the operation date in correction effectiveOf and action fields only | Mapping fix |
| LRU-DES-19 | Operation date is later than an affected top-level organization's current EffectiveStartDate | Blocking | resolve_lru_loader_contract | The selected EFF branch omits SplitOrganizationUnitForEFFUpdate, a new child omits a required parent locator or populates OrgInformationId, EffectiveStartDate, or EffectiveEndDate, or the action populates OrgInformationId | Add SplitOrganizationUnitForEFFUpdate with blank action OrgInformationId; for a new POST child populate available fresh parent locators, leave all child identity/date fields blank, and put the requested date in effectiveOf and split-action fields only | Mapping fix |
| LRU-DES-20 | Every Edit | Blocking | read_lru_eff_context | Unchanged or unrequested contexts or segments are included | Retain only requested changed EFF data | Mapping fix |
| LRU-DES-21 | A child removal is requested | Blocking | read_lru_eff_context | Context is single-row, row selection is ambiguous, or current loader metadata does not support removal | Reject or select one supported multirow child | Input fix |
| LRU-DES-22 | An unqualified delete is requested | Blocking | resolve_lru_delete_history | The request could mean physical LRU deletion or an ineligible historical row | Limit the request to the latest eligible date-effective HCM Information change | Input fix |
| LRU-DES-23 | Date-effective delete is requested | Blocking | resolve_lru_delete_history | Target is the first, only, historical, future, or otherwise ineligible row | Refuse without substituting another target | No |
| LRU-DES-24 | Date-effective parent delete is requested | Blocking | resolve_lru_loader_contract | The selected object, current identity, eligible history, or current loader contract is incomplete or inconsistent | Re-resolve the current loader contract and selected eligible history before handoff | Mapping fix |
| LRU-DES-25 | Date-effective parent delete is requested | Blocking | resolve_lru_loader_contract | The same organization and selected history start are repeated, or the delete is combined with an EFF mutation | Keep one parent-delete operation per distinct organization and selected history start | Mapping fix |
| LRU-DES-26 | Loader deletion completed | Blocking | resolve_lru_delete_history | The selected row remains or unaffected boundaries changed | Report failed verification and do not retry | No |
| LRU-DES-27 | Any supported mutation | Blocking |  | Direct REST, ADF batch, or another non-loader route is selected | Route the mutation only through core.data-loader | No |
| LRU-DES-28 | Synchronization or any supported mutation | Blocking | resolve_lru_loader_contract | The selected business object does not match the requested synchronization, classification, EFF, or parent-delete operation | Select only the exact applicable registered business object | Mapping fix |
| LRU-DES-29 | Any EFF mutation | Blocking | resolve_lru_loader_contract | The selected object's current loader contract is missing or does not match the requested operation | Re-resolve current loader metadata before handoff | Mapping fix |
| LRU-DES-30 | Any EFF context mutation | Blocking | resolve_lru_loader_contract | Required context or category controls are absent or do not match current metadata | Re-resolve current loader metadata and selected context before handoff | Mapping fix |
| LRU-DES-31 | Correction, dated update, or end date | Blocking | resolve_lru_loader_contract | The current loader operation contract does not match the requested effective-date operation | Re-resolve the current loader operation contract before handoff | Mapping fix |
| LRU-DES-32 | Loader execution is requested | Blocking |  | Core Data Loader preview or approval is absent, stale, or belongs to different source/environment state | Return loader readiness and let core.data-loader own its approval workflow | No |
| LRU-DES-33 | Every user-facing result | Blocking |  | Output exposes IDs, raw codes, CategoryCode, contextVO, links, versions, payloads, or audit data | Render business labels and values only | Output fix |
| LRU-DES-34 | View, edit, or delete output | Blocking |  | A top-level combined Classifications field is shown | Use classification names only as branch headings or per-change values | Output fix |
| LRU-DES-35 | A read is selected | Blocking |  | The request uses a mutating endpoint or a client other than core.fusion-api.rest-api-client | Use only the declared read-only lookup contract | No |
| LRU-DES-36 | Every branch read or mutation precheck | Blocking | resolve_lru_loader_contract | ManageLegalReportingUnit synchronization is skipped, routed outside core.data-loader, repeated automatically after an uncertain result, or treated as classification approval | Return LRU.SYNC_LOADER_READY for one synchronization-only archive and reconcile uncertainty through refreshed search | No |
| LRU-DES-37 | A classification change is selected | Blocking | resolve_lru_loader_contract | ManageLegalReportingUnitHcmClassifications is routed outside core.data-loader or is combined with ManageLegalReportingUnit | Return LRU.CLASSIFICATION_LOADER_READY with only the exact classification business object | No |
| LRU-DES-38 | An EFF or date-effective delete mutation is selected | Blocking |  | The request uses REST directly instead of core.data-loader in REST mode | Return LRU.LOADER_READY with the exact selected mutation business objects | No |
| LRU-DES-39 | Validation or execution fails | Blocking |  | The plan falls back to a direct REST mutation or an unrequested transport | Preserve the loader route and reconcile through declared reads | No |
| LRU-DES-40 | An EFF update targets an existing or new child | Blocking | resolve_lru_loader_contract | The source changes a fresh existing child's current OrgInformationId, EffectiveStartDate, or EffectiveEndDate; omits fresh parent locators; populates OrgInformationId, EffectiveStartDate, or EffectiveEndDate for a new POST child; requires a field absent from the selected object's live template; or copies a locator contract from another object | Preserve current existing-child keys and the fresh parent locator set; for a new POST child keep all child identity/date fields blank; validate each row independently, and author only fields declared by the exact selected object's current live template | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_lru_by_exact_name | Every request | Exact record, supported classification properties, and read-only identifiers | ora_reference_lookups.md |
| resolve_lru_classification_organization | A classification change is required | One OrganizationId from exact Name and ClassificationCode=HCM_LRU before active roots exist | ora_reference_lookups.md |
| resolve_active_lru_branch_identity | A branch read, EFF mutation precheck, or history operation runs after classification is active | OrganizationId and shared identity evidence from every active EstablishmentId root | ora_reference_lookups.md |
| resolve_tax_reporting_unit_root | Tax Reporting Unit property is A | Basic details, dates, CategoryCode, keys, and EFF envelope | ora_reference_lookups.md |
| resolve_reporting_establishment_root | Reporting Establishment property is A | Basic details, dates, CategoryCode, keys, and EFF envelope | ora_reference_lookups.md |
| resolve_tax_reporting_unit_eff_metadata | Tax Reporting Unit property is A | Contexts, labels, cardinality, attributes, and LOV mappings | ora_reference_lookups.md |
| resolve_reporting_establishment_eff_metadata | Reporting Establishment property is A | Contexts, labels, cardinality, attributes, and LOV mappings | ora_reference_lookups.md |
| read_lru_eff_context | A context, segment, row, or edit boundary is required | Current values, row identity, links, cardinality, and effective range | ora_reference_lookups.md |
| validate_lru_segment_value | A segment has a value set | One typed stored value | ora_reference_lookups.md |
| resolve_lru_delete_history | Date-effective delete is requested or verified | Complete history and selected eligible range | ora_reference_lookups.md |
| resolve_lru_loader_contract | Every supported mutation or import | Registered objects and the current operation contract | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| pass | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.DESIGN | decision | 19 | design_enforcement | pass->LRU.ROUTE;not_required->LRU.ROUTE;blocked->LRU.ERROR | LRU.DEFAULTS | stop | After defaults and preservation rules are applied |
