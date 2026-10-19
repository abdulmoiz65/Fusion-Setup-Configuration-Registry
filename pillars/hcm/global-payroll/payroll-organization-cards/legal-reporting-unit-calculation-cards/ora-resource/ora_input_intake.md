# Legal Reporting Unit Calculation Cards Input Intake

Source scope includes task metadata, effective catalog support flags, the release catalog description, and user-confirmed parity with the redacted Legal Entity Calculation Cards HAR for Redwood calculationEntries calls. Runtime must verify the Legal Reporting Unit owner scope and sourceType before using the shared contract.

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Guided request | Desired business outcome, target tax reporting unit, card/component/field names, requested value, and effective date | Automatic existence discovery, operation classification, validation, preview |
| Legal reporting availability request | Nonblank legal-reporting-unit name or registration-number search text, with optional user-supplied `%` wildcards | Read-only legal-reporting-unit discovery and TRU activity check |
| Legislative Data Group availability request | Nonblank full or partial LDG name, or a territory-scoped phrase such as “all US LDGs” | Read-only LDG discovery independent of TRU selection |
| Combined LDG-owner association request | Territory or country plus a request for LDGs and their associated PSUs and TRUs | Parent-orchestrated, read-only grouped discovery |
| Component flexfield value request | Exact tax reporting unit, card, component business name, and effective date; when names repeat, select from displayed business intervals | Read-only current/default FLEX value list; component sequence remains internal |
| FSM export artifact | Task-specific export request or exported CSV package for Legal Reporting Unit Calculation Cards | Baseline and comparison |
| FSM import artifact | Task-specific import package or CSV rows for Legal Reporting Unit Calculation Cards | Import preparation and validation |
| TRU launch context | Redacted calculation-entries launch URL or extracted FS_SCOPEINFOS values for Legal Reporting Unit Calculation Cards | Owner scoping and navigation planning |
| Tabular data | Row set mapped to the live target `CalculationCard` HDL contract or approved task-specific CSV/FSM contract | Bulk validation and import preparation |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| Requested business outcome | Yes | Describes what the user wants changed; create/update/correct wording remains provisional until target-state discovery | No | classify_requested_calculation_card_operation |
| Legal reporting unit search text | Yes for availability checks | Builds the `hcmLegalReportingUnits` `findByAdvancedSearchQuery` query value | POST request body | find_legal_reporting_units_by_advanced_search_query |
| Legislative Data Group search text | Yes for direct LDG availability checks | Supplies the trimmed full or partial LDG name unchanged | POST request body | find_legislative_data_groups_by_advanced_search_query |
| Legislative Data Group territory | Yes for a territory-scoped LDG list | Maps `US` or `United States` to the exact Fusion value `United States` | POST request body as the `TerritoryShortName` filter | find_legislative_data_groups_by_advanced_search_query |
| Combined LDG-owner association request | Yes for combined discovery | Requests a complete TRU contribution grouped later by exact `LdgId` | No; workflow intent | list_tax_reporting_units_by_legislation_code |
| Tax reporting unit | Yes | Identifies the reporting-unit-level owner for predefined calculation cards | Body or URL when sourceId/sourceType are required | parse_legal_reporting_unit_launch_scope followed by resolve_tax_reporting_unit when only ESTABLISHMENT_ID is present |
| Source type | Yes for calculationEntries calls | Identifies the owner type for Legal Reporting Unit card calls | Body or URL | validate_tru_source_type |
| Calculation card business name | Yes for card work | Identifies the requested card functionally; the skill resolves `dirCardId` internally when the card exists | No; used to select read-only results | list_existing_legal_reporting_unit_calculation_cards_for_hdl then find_legal_reporting_unit_calculation_card |
| Runtime technical identifiers | Never required from a functional user | `dirCardId`, definition/component IDs, override-group IDs, source/LDG IDs, and assignment/association IDs are internal lookup outputs | Retrieval requests only after automatic resolution; never DAT values | resolve_runtime_technical_keys |
| Card base name | Conditional | Names the selected card template or existing card base for component lookup and HDL definition mapping | Body or URL for retrieval only | find_legal_reporting_unit_calculation_card |
| Effective date | Yes for every requested business change | Scopes current/future/history retrieval and the proposed HDL slice or correction target | Body, URL, or query for retrieval; DAT field for HDL | validate_effective_date and classify_requested_calculation_card_operation |
| CSV or FSM source artifact | Conditional | Supplies rows for import or comparison | No | Validate against the approved task-specific CSV or FSM shape |
| Card component business name | Conditional | Selects a component functionally; the skill resolves component and definition IDs internally | No; used to select read-only results | get_legal_reporting_unit_card_components |
| Component name or base name | Yes for component flexfield values | Selects one component whose current/default FLEX rows are listed | No; used to select the returned component | list_component_flexfield_values |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Export or import is requested | Use the task-specific FSM or CSV export/import workflow because the catalog flags export/import and CSV export/import as supported |
| FS_SCOPEINFOS is supplied | Split scope groups on ## and fields on ***; if a group has ESTABLISHMENT_ID as the second segment, classify it as sourceType=TRU and preserve the display segment as sourceTypeName |
| FS_SCOPEINFOS supplies ESTABLISHMENT_ID | Call payGenericRestQuery with the one serialized finder `finder=findByWord;PayRestName=OrgTaxReportingUnitPVO,AdditionalViewCriteria=findByEstablishmentId,ParameterKeys=pEstablishmentId,ParameterValues={EstablishmentId},DisplayAttributes=OrganizationId&#124;&#124;LdgId`; use OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=TRU |
| Legal reporting availability is requested | Preserve the trimmed user search text and send the source-backed `hcmLegalReportingUnits` `findByAdvancedSearchQuery` POST body through `core.fusion-api.rest-api-client`; do not resolve a card until one reporting unit is selected |
| Legislative Data Group availability is requested | For name mode, preserve the trimmed name as `query` with `filters=[]`. For “all US LDGs”, send `query=""` with the exact `TerritoryShortName=United States` filter. Return the complete names-only result and do not require a TRU |
| Combined LDG-owner associations are requested | For United States, return one completely paged `OrgTaxReportingUnitPVO` legislation-code dataset using `DisplayAttributes=PsuId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId`; retain PsuId, Name, OrganizationId, and LdgId for the parent workflow. Do not render or select an owner in this nested contribution |
| Card details are requested | Start from owner, LDG, card business name, and effective date. Run owner-scoped mode=G discovery without `dirCardId`, retain the unique returned `dirCardId` internally, then call the exact drilldown with expand=Cards or expand=Cards,Components,Overrides,CompAssociation |
| Addable cards are requested | Read-only discovery: call getCardDetails with sourceType=TRU, sourceId, effectiveDate, expand=Cards, and mode=ADD; do not require dirCardId |
| Addable components for a card are requested | Read-only discovery: call payGenericRestQuery with CIRComponentPVO using pRelId=sourceId, pCardBaseName, pEffectiveDate, and pLDGId |
| Addable attributes or required overrides for a component are requested | Read-only discovery: call getCardDetails with mode=ADD, sourceType=TRU, sourceId, legislativeDataGroupId, effectiveDate, cardBaseName, and an initial component carrying overrideBaseGroupName, overrideGroupName, and any selected component context values |
| Current/default flexfield values for a component are requested | Read-only discovery: retrieve the exact existing or add-template component, filter only its `overrideType=FLEX` rows, and return business-facing `Name: Value` lines; do not create or mutate data |
| A business change is requested | Retrieve complete current, future, and historical state for every requested card/component/override/FLEX/value/assignment/association business key. Classify each leaf as CREATE, EXISTING_AT_DATE, EXISTS_OUTSIDE_DATE, or AMBIGUOUS before applying HDL defaults |
| Existing data is found | Notify with business names, current value when relevant, effective interval, requested date, and adjacent future row; keep IDs internal and ask for Update or Correction confirmation before DAT preview |
| No existing leaf row is found | Treat only the missing leaf as create after completeness is proven; reuse resolved existing parents and do not create a duplicate card/component |
| HDL card or component creation omits sequence or effective dates | Default new-card CardSequence to 1, new-component ComponentSequence to 1, EffectiveStartDate to the runtime system date resolved at DAT preview, and EffectiveEndDate to 4712/12/31; preserve explicit user values and validate parent linkage before preview |
| Tax reporting unit is supplied by name | Resolve it through the launch context, sourceId, or approved lookup contract before preview; the launch-page path can resolve only by ESTABLISHMENT_ID through OrgTaxReportingUnitPVO |
| Calculation card details are supplied | Preserve business details as mapping input, independently resolve technical keys and complete effective history through read-only retrieval, and map only after the approved contract identifies editable fields |
| Source authority is not explicit | Mark the owning lookup, validation, HDL action, or field as TBD rather than treating user-provided data as local authority |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUC.COLLECT | step | 1 | collect_input | complete->LRUC.VALIDATE | none | stop | Every Legal Reporting Unit Calculation Cards request |
