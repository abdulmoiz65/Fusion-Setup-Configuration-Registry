# Manage Legal Jurisdictions Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_jurisdiction_geography | Territory is supplied or a visible row is selected | Territory term plus optional visible-row refinement | /crmRestApi/resources/11.13.18.05/addressGeographies | Identity projection, separate level probes, and coherent tuple projection under the protocol below; Framework Version 9 | Complete identity pagination and applicable enrichment; preserve every eligible source identity and require one eligible visible tuple/source identity or explicit selection | Territory hierarchy and source-specific receipt-only GeographyIdentifierId; identity and enrichment receipts | Zero eligible, many unresolved, partial/failed reads, unknown flags, or unreconciled hierarchy blocks; never ask for an ID or prefer a country |
| resolve_legislative_category | Legislative Category is supplied | Exact legislative category code or meaning | https://<host>/fscmRestApi/resources/11.13.18.05/standardLookups/LEGISLATIVE_CATEGORY/child/lookupCodes?onlyData=true | LookupCode, Meaning, EnabledFlag and effective dates available from the response | Retrieve all result pages; require one enabled exact code or normalized exact meaning match | LOV display Meaning, Legislative Category internal code, and evidence receipt | Zero or many blocks; UI meaning is not an import value without export evidence |
| resolve_legal_entity_registration_code | Legal Entity Registration Code is supplied | Exact code or meaning | https://<host>/fscmRestApi/resources/11.13.18.05/standardLookups/XLE_REG_CODE/child/lookupCodes?orderBy=Meaning:asc&onlyData=true | LookupCode, Meaning, EnabledFlag and effective dates available from the response | Retrieve all result pages; require one enabled exact code or normalized exact meaning match | LOV display Meaning, Legal Entity Registration Code internal code, and evidence receipt | Zero or many blocks |
| resolve_lru_registration_code | Legal Reporting Unit Registration Code is supplied | Exact code or meaning | https://<host>/fscmRestApi/resources/11.13.18.05/standardLookups/XLE_REG_CODE_EST/child/lookupCodes?orderBy=Meaning:asc&onlyData=true | LookupCode, Meaning, EnabledFlag and effective dates available from the response | Retrieve all result pages; require one enabled exact code or normalized exact meaning match | LOV display Meaning, Legal Reporting Unit Registration Code internal code, and evidence receipt | Zero or many blocks |
| resolve_legal_jurisdiction_function_code | A Legal Function is supplied | Exact function code or displayed function name | /crmRestApi/resources/11.13.18.05/fndStaticLookups using LookupTypeIsActiveEnabledFinder with BindLookupType=XLE_LE_FUNCTION | LookupCode, Meaning, EnabledFlag | Require one enabled exact code or normalized exact meaning match. The supplied UI evidence shows Generate intercompany invoice, Incoming tax control, Salary annual declaration, and State incoming tax control as available choices; retain the resolved code rather than the display text in FunctionCode. | FunctionCode and evidence receipt | Zero or many blocks the function row; do not infer a code from a display label |
| list_jurisdiction_territories | Territory discovery or incomplete/ambiguous create | Optional Territory term and explicit narrowing; bounded initial page when missing | /crmRestApi/resources/11.13.18.05/addressGeographies | Identity projection and applicable enrichment under the protocol below; count, hasMore, limit, offset | Prefix search through hasMore=false; preserve identity set while enriching, primary-filter coherent tuples, deduplicate and display all eligible visible choices through 50 or first 50 plus linked full list | Territory, Geography Type, Name, Name, Name; internal source IDs retained only in receipts | Failed/incomplete reads, unknown eligibility, ambiguous hierarchy, or incomplete choice delivery blocks resolution and remaining LOVs |
| list_jurisdiction_lovs | mode=discover_lovs after the Territory Resolution Gate resolves, or a guided create has all other required choices missing | Resolved Territory receipt and optional as-of date | addressGeographies, standardLookups/LEGISLATIVE_CATEGORY, standardLookups/XLE_REG_CODE, standardLookups/XLE_REG_CODE_EST, and fndStaticLookups with BindLookupType=XLE_LE_FUNCTION | Each endpoint's display field, internal code, enabled flag, and effective dates when supplied | Call every required endpoint read-only and retrieve every result page. Return only enabled/current values and retain each endpoint receipt. For each of the four LOVs, state its eligible count and render every dropdown value as its own ordinary Markdown `Choice` row through 50. Above 50, render the first 50, state the total, and write/link a complete per-LOV Markdown artifact. Never substitute the first item, `<br>` values, or a delimiter-separated summary. The standard-lookup endpoints provide available code lists; do not claim a Territory-specific restriction unless metadata proves it. | Resolved Territory plus display label/internal-code pairs for Legislative Category, Legal Entity Registration Code, Legal Reporting Unit Registration Code, and optional Legal Function | If Territory is not gate-resolved, or any required endpoint is unavailable, unauthorized, partial, ambiguous, unrendered, or lacks its required complete-list artifact, return no partial list; disclose the blocked stage as `lov_delivery_failed` and stop discovery |
| find_legal_jurisdiction_existing | Before create, rename, or mutable validation | Exact Name, resolved Geography ID, Legislative Category, and as-of date | /fscmRestApi/resources/11.13.18.05/legalJurisdictionsLOV | JurisdictionId, Name, GeographyId, LegislativeCategoryCode, LegalEntityRegistrationCode, LegalReportingUnitRegistrationCode, IdentifyingFlag, StartDate, EndDate | Retrieve all result pages; compare normalized exact Name and exact GeographyId plus LegislativeCategoryCode independently. | Existing definition, natural key, field-level differences, identifying-set receipt, and receipt-only Jurisdiction ID | Lookup failure, partial result, equivalent, different, duplicate-name, verified duplicate geography/category, or ambiguity blocks; unavailable canonical mapping alone defers only the two declared checks; never use an existing jurisdiction row as a source for new business values |
| verify_active_jurisdiction_registrations | Before end-date or start-date change | Existing jurisdiction natural key, receipt-only Jurisdiction ID, and as-of date | Fresh same-target FSM exports for Manage Legal Entity Registrations and Manage Legal Reporting Unit Registrations | Registration identity, jurisdiction relationship, effective dates, and status | Require authoritative current export evidence that no active registration references the jurisdiction | Active-registration clearance evidence | Any active, missing, stale, partial, or ambiguous registration evidence blocks |
| verify_jurisdiction_package_baseline | Before FSM package generation and final readiness | Fresh same-target task export archive and ASM metadata | Exported FSM metadata and CSV templates for XLE_MANAGE_LEGAL_JURISDICTIONS | ASM_SETUP_CSV_METADATA.xml; XLE_JURISDICTION.csv; ORA_XLE_JURISDICTION_DATA.csv; exact headers, order, encoding, technical defaults (using the reusable create policy in ora_defaulting_rules.md for its declared fields), target/release identity, successful status, and fingerprint | Require a successful fresh same-target export with the two CSV members and metadata XML. Use it only to prove template structure and technical defaults (using the reusable create policy in ora_defaulting_rules.md for its declared fields); do not inspect, copy, or infer new jurisdiction business values from existing data rows. Preserve node order XLE_JURISDICTION=1 then ORA_XLE_JURISDICTION_DATA=2. For a nonempty Legal Function child row, apply the documented RequiredFlag default of Y unless valid explicit user input overrides it. | Package contract, exact member inventory, technical defaults (using the reusable create policy in ora_defaulting_rules.md for its declared fields), and baseline fingerprint; record missing canonical geography carriers as warnings | Missing, stale, partial, warning, wrong-target, or ambiguous evidence blocks |

## Lookup Projection and Source Identity

Use only addressGeographies for Territory discovery and hierarchy enrichment.
Send `REST-Framework-Version: 9` explicitly on every GET through the shared
OAuth REST client. Pass q and fields separately; use onlyData, limit and offset.
Escape quotes in q literals by doubling them; escape literal wildcard characters
before appending the intentional prefix percent. Do not pre-encode q.

1. Discover with fields `GeographyIdentifierId,CountryCode,GeographyValue,
   GeographyType,PrimaryGeographyFlag,LanguageCode,StartDate,EndDate`. With a
   term, q is `GeographyValue LIKE '<escaped-term>%'`; read every matching page.
   With no term, retain the first bounded page and request a search term. Never
   request lower-level values or flags in this identity projection. Preserve
   the complete identity set and all primary/date evidence.
2. COUNTRY identities need no lower-level read. GeographyValue supplies their
   displayed first Name and GeographyElement1 under the existing country-level
   mapping; this is an explicit derivation, not a returned level-1 field.
   Do not infer geography code or usage from CountryCode.
3. For each eligible non-country source identity, read separate projections for
   level 2, level 3, and level 4, each containing the identity fields plus only
   GeographyLevelNValue and PrimaryGeographyLevelNFlag. Bind reads to exact
   GeographyValue, CountryCode and GeographyType from discovery, and correlate
   returned GeographyIdentifierId before accepting any row. This identity-bound
   country predicate is enrichment, not an automatic discovery restriction.
   Complete every page. A successful zero-row level projection means that level
   is unavailable in this retrieval; retain that evidence and the base identity.
   It does not prove a null database value. Failed/incomplete reads block.
4. From levels with verified values for that same identity, request a joint
   projection containing exactly those levels and their flags. Use its coherent
   rows, not a Cartesian product of independent probes. Do not request unavailable
   deeper levels. Preserve level positions. Every populated value requires its
   own primary flag; filter alternates only after evaluating the complete tuple.
   Reconcile the joint rows with all populated probe levels and the discovery
   identity. If joint enrichment loses an identity that had populated probe
   evidence, or no coherent primary tuple can be established without discarding
   unresolved evidence, stop as a hierarchy gap rather than silently dropping it.
   If all probes are empty, keep the identity visible with blank hierarchy and
   an unavailable-hierarchy warning; source uniqueness still applies.
5. Preserve every primary/effective base identity through enrichment. Only
   proven alternates/ineffective rows may be excluded. Re-read unknown required
   flags using the affected projection; unresolved flags block delivery. An
   empty deeper projection must never replace the base identity set. Do not
   hard-code country-specific depth, name, language, ID, or abbreviation.
6. Persist request q, fields, explicit header, timestamps, pagination, base IDs,
   per-level availability, coherent tuple matching, primary decisions and counts.
   IDs remain source-specific and receipt-only. GeographyIdentifierId is not
   GeographyId and cannot be used as canonical mapping for duplicate checks.

Map CountryCode to GeoCountryCodeTransient, GeographyType to
GeographyTypeTransient and GeographyValue to GeographyNameTransient. Preserve
available GeographyLevel2Value through GeographyLevel4Value as GeographyElement2
through GeographyElement4. Never shift or synthesize local hierarchy. Missing
canonical geography code, usage or unavailable first hierarchy level remains a
warning under the existing create policy; leave the corresponding carriers blank.
Copy every shared parent geography carrier exactly to Legal Function child rows.
Use only template structure and declared defaults; do not copy existing data.
The jurisdiction LOV can verify Name and persisted GeographyId but cannot prove
omitted carrier values were stored blank or verify a new identity's mapping.

## Two Checks Deferred When Canonical Geography Mapping Is Unavailable

For a create with a uniquely selected, primary-eligible Territory, defer only
these two pre-import checks when the supported read-only endpoints cannot verify
the selected source identity's relationship to a canonical GeographyId:

1. Existing jurisdiction with the same GeographyId and LegislativeCategoryCode.
2. Existing identifying jurisdiction for that GeographyId and the impact of
   the supplied IdentifyingFlag.

Record each excluded check as not_applicable with a warning and reason
canonical_geography_mapping_unavailable. Disclose that Fusion will enforce the
geography/category rule and apply identifying behavior during import. Do not ask
for a separate waiver, require allowReadinessOverride, or label the checks passed.
Retain the source receipts and exact selected primary hierarchy; never guess a
GeographyId, equate it with GeographyIdentifierId, or use unrelated jurisdictions
to infer the selected geography. Do not scan the entire geography catalogue or
require a full-data export merely to make these two checks executable.

When verified mapping is available, run both checks normally; known conflicts
still block under existing rules. The exclusion is caused by mapping capability,
not automatically by the addressGeographies source. Missing/ambiguous Territory,
unknown primary flags, failed or incomplete lookup requests, name uniqueness,
input/code validation, dates, immutable-field and active-registration checks,
package structure, Task Hook preview, and import approval are not excluded.
This create policy does not authorize an unverified update to existing records.

Task Hook must retain both warnings in the applicable dependency/design resource
results and preview. A resource may be passed only when all its other applicable
checks pass; keep the two individual excluded checks explicitly not_applicable
in its evidence. Do not mark the entire resource not_applicable or overridden.
After submission, review the actual Data Loader errors and FSM ProcessLog before
quoting success or failure. Reconcile any rejected or indeterminate import before
preparing a separately validated and approved retry; never replay automatically.

## Primary Territory Eligibility

| Situation | What Happens |
|---|---|
| Territory value | Require PrimaryGeographyFlag=true on addressGeographies rows before they enter any choice or resolution set. |
| Populated displayed hierarchy level | Require the corresponding PrimaryGeographyLevel2Flag, PrimaryGeographyLevel3Flag, or PrimaryGeographyLevel4Flag=true for each nonblank level 2, 3, or 4 value. Ignore a level flag only when that level is blank; do not shift levels. |
| Explicit alternate | Exclude the entire row when any applicable flag is false. Retain its raw response and exclusion reason internally; omit it from inline/link tables, suggestion lists, candidate counts, selection matching, and import data. |
| Flag representation | Accept Boolean true/false and equivalent explicit strings true/false or Y/N, case-insensitively. For rows not already excluded by an explicit false flag, missing/null/unrecognized required flags are unknown; never infer primary status or use string truthiness. |
| Unknown primary eligibility | Re-read the affected identity or coherent level projection. If any required flag remains unknown, stop choice delivery and resolution as a primary-flag metadata gap; do not silently exclude unknown rows or declare no matches. |
| COUNTRY identity | Retain primary/effective country identities from the minimal projection without requiring unavailable lower-level flags. |
| Same alternate identifier | Evaluate each visible hierarchy variant's flags before deduplication. Never choose the first row, prefer an abbreviation by text, or deduplicate solely by GeographyIdentifierId. |
| Supplied alternate selection | Do not resolve an excluded tuple or silently normalize it. Deliver eligible primary candidates and request a visible-row selection. A retained old receipt must meet the same gate. |
| Delivery and receipts | Retrieve all required pages before filtering. Retain raw, eligible-primary, and excluded-alternate counts plus exclusion reasons. Merge and deduplicate only eligible rows; use their count for the five-column table, linked full list, 50-row limit, and uniqueness checks. |

### Empty-Endpoint and Conditional-Check Review Scenarios

| Scenario | Expected result |
|---|---|
| Identity retrieval returns a primary country and hierarchy probes are inapplicable | Retain the country and resolve only under the normal uniqueness/selection gate |
| Identity or required enrichment read fails or pagination is incomplete | Block discovery; do not apply the two-check exclusion to endpoint failures |
| Valid create has no verified canonical mapping | Record only geography/category uniqueness and identifying impact as individual not_applicable warnings; require no waiver |
| Canonical mapping is verified | Run both geography-dependent checks; retain known-conflict blockers |
| Name is duplicate while canonical mapping is unavailable | Block on name uniqueness; the exclusion does not apply |
| Update has unresolved geography mapping | Do not apply the create-only exclusion |

### Primary-Choice Review Scenarios

| Scenario | Expected result |
|---|---|
| Primary Territory and all three populated hierarchy levels have true flags | Include the row in the eligible choice set. |
| Two rows share one alternate identifier; only one has PrimaryGeographyLevel2Flag=true | Include only the primary hierarchy variant, regardless of response order. |
| Territory is primary but any populated level 2, 3, or 4 flag is false | Exclude the entire alternate row, including from linked lists and exact-match suggestions. |
| A hierarchy level is blank and its flag is null | Ignore that blank level's flag; eligibility still depends on every other applicable flag. |
| An otherwise eligible row has a missing/null/unrecognized required flag | Re-read the affected projection; block discovery if the required flag remains unknown. |
| PrimaryGeographyFlag is false and other flags are missing | Exclude the known alternate; missing flags on that excluded row do not block other choices. |
| The Boolean flag arrives as the string false or N | Interpret it as false and exclude the row; never use nonempty-string truthiness. |
| Valid primary country has no lower hierarchy flags | Keep the country; lower levels are inapplicable and must not be projected into identity discovery. |
| User explicitly selects an excluded hierarchy variant | Return eligible primary choices and request selection; do not silently substitute hierarchy values. |

## Lookup Execution Rules

### Territory Prefix-Result Invariant

For every supplied Territory term, including an exact match, call
`addressGeographies` with `GeographyValue LIKE '<escaped-territory>%'` and
page the response through `hasMore=false`, without a CountryCode condition.
Do not add CountryCode merely because it is supplied or can be inferred: the
UI can return cross-country and special geography rows for one Territory term.
Use CountryCode only for a subsequent search the user explicitly asks to
narrow after seeing the unfiltered candidate set.

An exact-result receipt never replaces complete prefix identity pagination.
Enrich without losing countries or shorter hierarchies, apply primary eligibility,
and deliver the eligible five-column candidate table before resolving ambiguity.

| Situation | What Happens |
|---|---|
| Territory free-text lookup input | Complete minimal identity prefix discovery and applicable coherent enrichment. Preserve every eligible identity, primary-filter before deduplication, and deliver all visible candidates through 50 or first 50 plus a linked full list. Require visible-row selection when ambiguous; never nominate a preferred country or ask for an internal ID. |
| Other free-text lookup input | Use exact code or normalized exact meaning matching, eligibility/effective-date checks, pagination, and cardinality one. |
| LOV display | Return the display Meaning/Name with its internal LookupCode or natural key. Display values are advisory selection text; package fields use internal codes only when the current export/template proves the field accepts them. |
| LOV discovery mode | Invoke automatically for an incomplete create request as well as for explicit discovery. It is read-only and returns complete enabled lists only after all required lookup sources succeed; it never creates a jurisdiction or generates an FSM package. |
| Guided missing-input flow | Preserve values already supplied. If Territory is missing, return the first bounded primary-eligible LOV page in the UI-style Territory, Geography Type, Name, Name, Name format and ask for a Territory search term; Country is optional narrowing. If supplied Territory is unclear, return exact and nearest candidates in the same table and request a visible-row selection, never an internal ID. Do not invoke remaining LOV discovery until the Territory Resolution Gate resolves from complete identity and applicable enrichment receipts. Then return all remaining required choices and the optional Legal Function list as separate complete one-column `Choice` tables using the exact UI-displayed dropdown values. If Identifying Flag is absent, include the required Y/N choice table. If either date is absent, prompt for optional `YYYY/MM/DD` values or explicit confirmation to leave it blank. Do not ask one field at a time, return comma- or semicolon-separated lists, repeat supplied values, expose internal lookup metadata, infer an identifying outcome, synthesize dates, or start template export before this response. |
| Duplicate check | Query legalJurisdictionsLOV before create, read every result page, then evaluate exact Name independently. Evaluate exact GeographyId plus LegislativeCategoryCode and identifying impact only with verified canonical mapping; otherwise record just those two checks as not_applicable warnings under the conditional exclusion policy. Never treat a partial page, a fuzzy name, or a failed request as an available name. |
| Export-derived technical field | Use the task export before package generation; retain source file, column, observed value, and export fingerprint in the import-readiness record. |
| FSM geography carrier availability | Retain selected tuple, source identity, raw attributes, and template fingerprint. If the supported endpoint omits canonical carrier attributes, record a warning and continue through package preparation and explicitly approved import submission. |
| Physical ID returned | Keep it as receipt-only relationship evidence unless the fresh FSM template explicitly requires it. |
| Registration-impact verification | Treat active, missing, stale, partial, or ambiguous registration evidence as a blocker for end dating or conflicting start-date changes. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.DISCOVER_TERRITORIES | decision | 4 | reference_lookup | candidates_ready->LJ.TERRITORY_SELECTION_GATE;unavailable->LJ.HANDLE_ERROR | none | stop | Explicit mode=discover_territories, a create request is missing Territory, or Territory text is supplied; complete minimal identity pagination and applicable coherent enrichment, preserving countries and shorter hierarchies before primary-filtered choice delivery |
| LJ.DISCOVER_LOVS | decision | 6 | reference_lookup | listed->LJ.RETURN_LOVS;lov_delivery_failed->LJ.HANDLE_ERROR;not_requested->LJ.VALIDATE_INPUT;unavailable->LJ.HANDLE_ERROR | LJ.TERRITORY_SELECTION_GATE | stop | Explicit mode=discover_lovs or guided create after the Territory Resolution Gate resolves; listed requires four complete, separately rendered LOV tables |
| LJ.RESOLVE_REFERENCES | step | 20 | reference_lookup | resolved->LJ.CHECK_DEPENDENCIES;blocked->LJ.HANDLE_ERROR;failure->LJ.HANDLE_ERROR | LJ.VALIDATE_INPUT | stop | Resolve required live and export-backed references |

## Projection-Safety Review Scenarios

| Scenario | Expected result |
|---|---|
| COUNTRY disappears from a hierarchy projection | Keep the primary country identity; no lower-level query is needed for COUNTRY |
| A local identity has levels 2 and 3 but its level-4 projection is empty | Preserve the identity; jointly read only levels 2 and 3 and retain level-4 unavailability evidence |
| Expanded fields multiply alternate hierarchy variants | Accept only coherent primary tuples; do not deduplicate by ID before filtering |
| Independent level probes contain values but the joint projection loses their identity | Block with a hierarchy gap; do not synthesize a tuple from separate rows |
| Any identity/probe/joint request is failed or partially paged | Block; do not convert transport or projection errors into an empty hierarchy |
| Geography mapping remains unavailable | Preserve the two existing create-only exclusions and all other validation/approval requirements |
