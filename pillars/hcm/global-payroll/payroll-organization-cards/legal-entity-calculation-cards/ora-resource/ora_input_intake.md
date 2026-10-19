# Legal Entity Calculation Cards Input Intake

Source scope is limited to task metadata, effective catalog support flags, the release catalog description, a developer-provided redacted FSM launch URL, and a developer-provided HAR capture for the Legal Entity Calculation Cards Redwood flow. Environment host, concrete IDs, user identity, and display names are redacted.

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Guided request | Desired business outcome, target payroll statutory unit, card/component/field names, requested value, and effective date | Automatic existence discovery, operation classification, validation, preview |
| Legal entity availability request | Nonblank legal-entity name or identifier search text, with optional user-supplied `%` wildcards | Read-only legal-entity discovery and PSU eligibility check |
| Legislative Data Group availability request | Nonblank full or partial LDG name, or a territory-scoped phrase such as “all US LDGs” | Read-only LDG discovery independent of PSU selection |
| Combined LDG-owner association request | Territory or country plus a request for LDGs and their associated PSUs and TRUs | Parent-orchestrated, read-only grouped discovery |
| Legislation or country code PSU list request | Nonblank legislation code such as US | Read-only PSU discovery for Legal Entity organization cards |
| Component flexfield value request | Exact payroll statutory unit, card, component business name, and effective date; when names repeat, select from displayed business intervals | Read-only current/default FLEX value list; component sequence remains internal |
| FSM export artifact | Task-specific export request or exported CSV package for Legal Entity Calculation Cards | Baseline and comparison |
| FSM import artifact | Task-specific import package or CSV rows for Legal Entity Calculation Cards | Import preparation and validation |
| Tabular data | Row set mapped to the approved task-specific CSV or FSM contract | Bulk validation and import preparation |
| FSM launch URL | Redacted launch path with FS_SOURCE=FS, source=FSM, pageTitle=Legal Entity Calculation Cards, and FS_SCOPEINFOS | Launch-context parsing and target-owner resolution |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| Requested business outcome | Yes | Describes what the user wants changed; create/update/correct wording remains provisional until target-state discovery | No | classify_requested_calculation_card_operation |
| Legal entity search text | Yes for availability checks | Builds the `findByAdvancedSearchQuery` query value | POST request body | find_legal_entities_by_advanced_search_query |
| Legislative Data Group search text | Yes for direct LDG availability checks | Supplies the trimmed full or partial LDG name unchanged | POST request body | find_legislative_data_groups_by_advanced_search_query |
| Legislative Data Group territory | Yes for a territory-scoped LDG list | Maps `US` or `United States` to the exact Fusion value `United States` | POST request body as the `TerritoryShortName` filter | find_legislative_data_groups_by_advanced_search_query |
| Combined LDG-owner association request | Yes for combined discovery | Requests a complete PSU contribution grouped later by exact `LdgId` | No; workflow intent | list_payroll_statutory_units_by_legislation_code |
| PSU eligibility filter | Yes for every legal entity availability check | Restricts results to legal entities whose PsuFlag is Y | POST request body as `filters` | find_legal_entities_by_advanced_search_query |
| Legislation code | Yes for legislation-scoped PSU list requests | Binds `OrgPayrollStatutoryUnitPVO` by country or legislation | Finder parameter `pLegislationCode` | list_payroll_statutory_units_by_legislation_code |
| LDG ID | Conditional for legislation-scoped PSU list requests | Narrows `OrgPayrollStatutoryUnitPVO` to one legislative data group when already known | Finder parameter `pLdgId` | list_payroll_statutory_units_by_legislation_and_ldg |
| Payroll statutory unit source ID | Yes | Identifies the PSU-scoped source owner; observed as sourceId with sourceType=PSU | Body for Redwood calculationEntries calls | parse_legal_entity_launch_scope followed by resolve_payroll_statutory_unit when only LEGAL_ENTITY_ID is present |
| Legislative data group ID | Yes for component, LOV, add-template, and HDL preparation flows | Scopes read-only component/value-set resolution and resolves the HDL LDG name | Body or finder parameter for retrieval only | validate_legislative_data_group_id |
| FSM launch scope | Conditional | Carries task launch context from FS_SCOPEINFOS, including XLE_ENTITY_PROFILE, LEGAL_ENTITY_ID, and legal entity display value | No | parse_legal_entity_launch_scope |
| Calculation card business name | Yes for card work | Identifies the requested card functionally; the skill resolves `dirCardId` internally when the card exists | No; used to select read-only results | list_existing_legal_entity_calculation_cards_for_hdl then find_legal_entity_calculation_card |
| Runtime technical identifiers | Never required from a functional user | `dirCardId`, definition/component IDs, override-group IDs, source/LDG IDs, and assignment/association IDs are internal lookup outputs | Retrieval requests only after automatic resolution; never DAT values | resolve_runtime_technical_keys |
| Effective date | Yes for every requested business change | Scopes current/future/history retrieval and the proposed HDL slice or correction target | Body or finder parameter for retrieval; DAT field for HDL | validate_effective_date and classify_requested_calculation_card_operation |
| Card base name | Yes for add-template and component lookup; used as evidence for HDL card-definition mapping | Identifies the card definition display or base name | Body or finder parameter for retrieval only | validate_card_base_name |
| Component sequence | Conditional | Identifies the component instance and resolves the HDL component user key | Body for retrieval only; DAT field for HDL | find_card_component_definition |
| Component name or base name | Yes for component flexfield values | Selects one component whose current/default FLEX rows are listed | No; used to select the returned component | list_component_flexfield_values |
| Override group ID | Conditional | Retained only as read-only component identity evidence; never written to the DAT or used for REST mutation | Retrieval body only | find_card_component_definition |
| CSV or FSM source artifact | Conditional | Supplies rows for import or comparison | No | Validate against the approved task-specific CSV or FSM shape |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Export or import is requested | Use the task-specific FSM or CSV export/import workflow because the catalog flags export/import and CSV export/import as supported |
| FSM launch URL is supplied | Parse only redacted query parameters needed for task context; do not persist environment-specific host, legal entity ID, or legal entity display value in packaged resources |
| FS_SCOPEINFOS is supplied | Split scope groups on ## and fields on ***; if a group has LEGAL_ENTITY_ID as the second segment, classify it as sourceType=PSU and preserve the display segment as sourceTypeName |
| FS_SCOPEINFOS supplies LEGAL_ENTITY_ID | Call payGenericRestQuery with the one serialized finder `finder=findByWord;PayRestName=OrgPayrollStatutoryUnitPVO,AdditionalViewCriteria=findByLegalEntityId,ParameterKeys=pLegalEntityId,ParameterValues={LegalEntityId},DisplayAttributes=OrganizationId&#124;&#124;LdgId`; use OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=PSU |
| User supplies legislation or country code for PSU or Legal Entity Org Cards | Call payGenericRestQuery with one serialized finder containing OrgPayrollStatutoryUnitPVO, AdditionalViewCriteria=findByLegislationCode, ParameterKeys=pLegislationCode, ParameterValues set to the supplied code such as US, and DisplayAttributes=LegalEntityId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId; when an LDG ID is known, combine the criteria, keys, and values with &#124;&#124; inside that same finder. Return only Name values for list-only requests |
| Legal entity availability is requested | Build the wildcard query from nonblank user search text, add the mandatory `filters` object with `name=["PsuFlag"]` and `terms=["Y"]`, and send the source-backed `findByAdvancedSearchQuery` POST body through `core.fusion-api.rest-api-client`; do not resolve a card until one legal entity is selected |
| Legislative Data Group availability is requested | For name mode, preserve the trimmed name as `query` with `filters=[]`. For “all US LDGs”, send `query=""` with the exact `TerritoryShortName=United States` filter. Return the complete names-only result and do not require a PSU |
| Combined LDG-owner associations are requested | For United States, return one completely paged `OrgPayrollStatutoryUnitPVO` legislation-code dataset with `Name`, `OrganizationId`, and `LdgId` to the parent workflow. Do not render or select an owner in this nested contribution |
| Card details are requested | Start from owner, LDG, card business name, and effective date. Run owner-scoped mode=G discovery without `dirCardId`, retain the unique returned `dirCardId` internally, then call the exact drilldown with expand=Cards or expand=Cards,Components,Overrides,CompAssociation |
| Addable cards are requested | Read-only discovery: call getCardDetails with sourceType=PSU, sourceId, effectiveDate, expand=Cards, and mode=ADD; do not require dirCardId |
| Addable components for a card are requested | Read-only discovery: call payGenericRestQuery with CIRComponentPVO using pRelId=sourceId, pCardBaseName, pEffectiveDate, and pLDGId |
| Addable attributes or required overrides for a component are requested | Read-only discovery: call getCardDetails with mode=ADD, sourceType=PSU, sourceId, legislativeDataGroupId, effectiveDate, and cardBaseName. Select the component either with `dirCardCompDefId` alone or by mapping `BaseComponentName` to `overrideBaseGroupName` and `ComponentName` to `overrideGroupName`; never send both forms. Resolve ComponentContextPVO first and send each required `contextN` value before reading override metadata. |
| Current/default flexfield values for a component are requested | Read-only discovery: retrieve the exact existing or add-template component, filter only its `overrideType=FLEX` rows, and return business-facing `Name: Value` lines; do not create or mutate data |
| A business change is requested | Retrieve complete current, future, and historical state for every requested card/component/override/FLEX/value/assignment/association business key. Classify each leaf as CREATE, EXISTING_AT_DATE, EXISTS_OUTSIDE_DATE, or AMBIGUOUS before applying HDL defaults |
| Existing data is found | Notify with business names, current value when relevant, effective interval, requested date, and adjacent future row; keep IDs internal and ask for Update or Correction confirmation before DAT preview |
| No existing leaf row is found | Treat only the missing leaf as create after completeness is proven; reuse resolved existing parents and do not create a duplicate card/component |
| HDL card or component creation omits sequence or effective dates | Default new-card CardSequence to 1, new-component ComponentSequence to 1, EffectiveStartDate to the runtime system date resolved at DAT preview, and EffectiveEndDate to 4712/12/31; preserve explicit user values and validate parent linkage before preview |
| Payroll statutory unit is supplied by name | Resolve it through an approved lookup contract before preview; launch-scope resolution uses LEGAL_ENTITY_ID through OrgPayrollStatutoryUnitPVO, while legislation-code discovery uses findByLegislationCode |
| Calculation card details are supplied | Preserve business details as mapping input, independently resolve technical keys and complete effective history through read-only retrieval, and map only to live target `CalculationCard` HDL sections |
| Source authority is not explicit | Mark the owning lookup, validation, HDL action, or field as TBD rather than treating user-provided data as local authority |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LEC.COLLECT | step | 1 | collect_input | complete->LEC.VALIDATE | none | stop | Every Legal Entity Calculation Cards request |
