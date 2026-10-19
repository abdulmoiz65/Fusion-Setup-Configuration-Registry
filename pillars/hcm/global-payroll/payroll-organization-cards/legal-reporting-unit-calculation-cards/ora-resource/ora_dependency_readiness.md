# Legal Reporting Unit Calculation Cards Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legal reporting unit task scope | Task code and task name must match the nested task |
| 1a | Direct Legislative Data Group discovery | A full or partial LDG-name or territory list can run after environment resolution and does not require a TRU selection |
| 2 | Tax reporting unit | Target owner must be supplied and resolved before card-specific preview |
| 3 | Functional request and effective date | Resolve the requested business path/value and date; treat create/update/correct verbs as provisional intent |
| 4 | Legal reporting unit calculation card | Existing card must be identified through read-only getCardDetails before any HDL update, end-date, or delete; new-card definitions come from read-only getCardDetails mode=ADD |
| 5 | Component and override metadata | Component identity and override metadata must come from getCardDetails or payGenericRestQuery |
| 5b | Complete object-level existence graph | Resolve card, component, override/FLEX/value, assignment/association, and related source-backed history across current, future, and historical intervals |
| 5c | Date-effective action confirmation | When any requested business key exists, notify the user and obtain Update or Correction confirmation before DAT preview |
| 5a | Component flexfield value list | Exact component selection and current/default FLEX rows must come from the selected getCardDetails response before user-facing formatting |
| 6 | Override dependency graph | Dynamic override dependencies must be ordered before LOV validation |
| 9 | HDL mutation contract | Calculation-card business changes use live target `CalculationCard` HDL through `core.data-loader`; CSV/FSM import and direct business REST are not mutation routes |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| LRUC.TRU | Tax reporting unit | Yes | Every card-specific request | Lookup | Functional TRU/legal-reporting-unit name or FS_SCOPEINFOS context | resolve_tax_reporting_unit | The owner and its runtime IDs must be resolved before card discovery | Provide the TRU or legal-reporting-unit business name; the skill resolves EstablishmentId, sourceId, and LDG internally | sourceId, sourceType=TRU, legislativeDataGroupId, and effective context |
| LRUC.LDG_AVAILABILITY | Legislative Data Group candidates | Conditional | User supplies a full or partial LDG name, or requests every LDG in a territory | Lookup | `legislativeDataGroups/action/findByAdvancedSearchQuery` in the active environment | find_legislative_data_groups_by_advanced_search_query | Direct LDG discovery is owner-independent and must return the complete matching name or territory list | Provide meaningful LDG search text or the source-backed territory value; select one only if downstream card work follows a multi-match result | Ordered names and internally retained LegislativeDataGroupId, territory, currency, and costing structure |
| LRUC.LDG | Legislative data group | Yes for LDG-name lookup, component/LOV retrieval, and HDL create/update/delete preparation | A selected TRU must resolve its LDG, or a card operation uses component, override, or HDL metadata | Lookup | LdgId from resolve_tax_reporting_unit or legislativeDataGroupId from getCardDetails | resolve_legislative_data_group_name | Read-only CalculationEntries lookups use the LDG ID, while CalculationCard HDL requires the exact accessible LegislativeDataGroupName | Select one active TRU or LDG business name; the skill resolves the LDG ID and exact name through read-only retrieval | legislativeDataGroupId, legislativeDataGroupName, HDL LegislativeDataGroupName, and legislationCode |
| LRUC.CARD | Legal reporting unit calculation card | Conditional | A specific card or child operation must be resolved for HDL | Lookup | Owner-scoped getCardDetails followed by exact drilldown | list_existing_legal_reporting_unit_calculation_cards_for_hdl and find_legal_reporting_unit_calculation_card | Existing HDL operations require one target card and complete effective history | Provide owner, card business name, and requested date; the skill resolves `dirCardId` and definition IDs internally | dirCardId as internal evidence, dirCardDefinitionId, cardBaseName, cardName, readOnlyFlag, original dates, history, and CardSequence |
| LRUC.CREATE_CARD | Available card for create | Conditional | A new card is being created and dirCardId is not yet available | Lookup | getCardDetails mode=ADD expand=Cards | list_available_legal_reporting_unit_cards_for_create | Create operations select by cardBaseName/cardName and dirCardDefinitionId before a dirCardId exists | Provide card name or card base name after owner/effective date are resolved | cardBaseName, cardName, dirCardDefinitionId, legislativeDataGroupId |
| LRUC.EXISTING_CARD_HDL | Existing-or-new HDL card state | Yes for every business change | Card business name and requested date are supplied | Lookup | Owner-scoped getCardDetails mode=G followed by exact internally resolved dirCardId drilldown | list_existing_legal_reporting_unit_calculation_cards_for_hdl and find_legal_reporting_unit_calculation_card | Prevents duplicate create and supplies parent keys/history | Provide owner, card name/base name, and effective date; when multiple business matches remain, choose from business names/date ranges rather than supplying an ID | Existing state, internal dirCardId, complete intervals, original dates, CardSequence, card names, and definition ID |
| LRUC.COMPONENT | Card component definition | Conditional | Add, update, end-date, delete, or component drilldown must be prepared through HDL | Lookup | payGenericRestQuery and getCardDetails | list_component_definitions_for_card | HDL component operations require component sequence, definition name, effective dates, and override metadata | Select or resolve the component from the returned component list | Runtime definition ID as evidence, componentSequence, deductionGroupId, overrideBaseGroupName, and HDL component name |
| LRUC.FLEXFIELD_VALUES | Component flexfield values | Conditional | Current/default flexfield values are requested for a component | Lookup | Selected getCardDetails component and its metadata-declared LOV source when needed | list_component_flexfield_values | The value list must stay within one owner, card, component, and effective date | Provide the component business name and date; when names repeat, select from displayed business intervals while the skill retains ComponentSequence internally | Ordered business labels and current/default display values; Blank for null or empty; None when no FLEX rows exist |
| LRUC.OVERRIDE_SCHEMA | Per-card override schema | Conditional | Any override value is supplied | Lookup | getCardDetails override metadata | build_card_override_schema | Each card can expose different override fields and validation metadata | Retrieve the selected card/component schema before accepting values | override codes, names, categories, control types, dataSource, current values |
| LRUC.OVERRIDE_DEPENDENCIES | Override dependency graph | Conditional | Any LOV dataSource has binds from another override or context field | Lookup | override dataSource metadata | validate_override_dependency_graph | Dependent LOVs must be resolved in source-declared order | Provide or resolve parent override values first | ordered resolver plan and blocked parent fields |
| LRUC.EXISTENCE_GRAPH | Complete object-level existence state | Yes for every business change | Card/component/field/value/assignment/association path and effective date are known | Lookup | Complete owner-scoped and exact drilldown responses, including source-backed current/future/history rows | resolve_calculation_card_object_existence | Create/update/correction must be decided per requested business key, not from the user's verb | Supply business names, requested value, and date; the skill resolves all runtime IDs and reports any business ambiguity | Per-object CREATE, EXISTING_AT_DATE, EXISTS_OUTSIDE_DATE, or AMBIGUOUS state plus intervals and current values |
| LRUC.OPERATION_DECISION | Confirmed date-effective action | Yes when any requested business key exists | Existing data disclosure is ready | Blocked pending user choice | Existence graph and effective-date matrix | classify_requested_calculation_card_operation | Update creates a new dated slice while Correction changes the selected slice | Choose Update or Correction after reviewing the displayed business interval and recommendation | Confirmed per-object action, requested date, selected interval, and disclosure state |
| LRUC.FSM_CONTRACT | Task-specific read-only export contract | Yes for setup export | Read-only export operation | Blocked | TBD | TBD | Catalog support proves availability, but not the runtime export action or data shape | Supply the approved export contract before retrieval | Retrieval action, required fields, row mapping, and result identifiers |

## Combined Discovery Dependency

| Dependency ID | Dependency | Mandatory | Applies When | Resolver | Ready State | Blocked State |
|---|---|---|---|---|---|---|
| LRUC.LDG_TRU_ASSOCIATIONS | Complete TRU association candidate set | Yes for combined territory LDG/PSU/TRU discovery | Parent requests LDGs with their associated owners | list_tax_reporting_unit_associations_by_legislation | The finder uses PsuId, Name, OrganizationId, and LdgId; every page is complete; and each unique OrganizationId has the fields needed for exact parent joining | The finder requests LegalEntityId, legislation mapping is missing, paging is incomplete, fields conflict or are blank, an LdgId is orphaned, or a returned PsuId conflicts with the retrieved PSU set |

## Dependency Classification

| Result Category | When Used | Can Run Read-Only Lookup? |
|---|---|---|
| Satisfied | Required identifier and approved contract are present | No |
| Lookup | User supplies a name or display value that must resolve uniquely | Yes, after source contract is supplied |
| Blocked | Lookup path, HDL action contract, or required field mapping is TBD | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUC.DEPENDENCY | decision | 3 | resolve_dependency | ready->LRUC.LOOKUP;blocked->LRUC.DONE_BLOCKED | LRUC.VALIDATE | stop | Required dependency facts are being evaluated |
