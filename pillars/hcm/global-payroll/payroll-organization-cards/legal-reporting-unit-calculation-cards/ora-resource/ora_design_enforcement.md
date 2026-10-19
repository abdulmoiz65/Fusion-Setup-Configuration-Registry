# Legal Reporting Unit Calculation Cards Design Enforcement

## Mandatory Mutation Route Gate

| Proposed operation | Severity | Required behavior | Blocking |
|---|---|---|---|
| Any calculation-card create, update, correction, end-date, delete-record, delete-history, or association change selects direct REST | Error | Reject the direct REST mutation. Resolve current state with read-only REST, then prepare only target-supported `CalculationCard` HDL through `core.data-loader` | Yes |
| A requested HDL action is absent or ambiguous in current target metadata | Error | Block the operation and report the missing HDL action or key contract; never fall back to REST | Yes |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task scope | Task code and task name must match the nested skill manifest |
| 2 | Confirm target owner | Tax reporting unit must resolve uniquely and runtime responses must verify sourceType=TRU |
| 2a | Confirm legal reporting selection | An availability search with multiple matches must stop before TRU or card resolution until the user selects one |
| 2b | Confirm direct LDG search completeness | A full or partial LDG-name or territory list must include every page and preserve all matching names before a list-only request completes |
| 3 | Confirm source contract | Parity-backed calculationEntries retrieval is allowed only for read-only review and HDL key/value resolution; all create, update, end-date, and delete behavior uses target-supported HDL |
| 4 | Confirm value sources | Component metadata, deduction group, and LOV-backed override values must resolve before HDL preview |
| 4a | Confirm flexfield value scope | A read-only flexfield value list must use one exact component and only that component's FLEX rows |
| 5 | Confirm no invented behavior | Unknown endpoints, defaults, field mappings, and validation rules remain TBD |
| 5a | Confirm object-level operation | Prove complete current/future/history state, resolve all runtime IDs internally, and obtain Update/Correction confirmation for every existing requested business key |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LRUC.SCOPE | Every request | Blocker | None | Task code or task name differs from the nested skill manifest | Use the Legal Reporting Unit Calculation Cards task metadata | Yes |
| LRUC.TRU_REQUIRED | Card-specific review or edit | Blocker | resolve_tax_reporting_unit | Tax reporting unit is missing or ambiguous | Supply a unique tax reporting unit reference | Yes |
| LRUC.LRU_AVAILABILITY_SELECTION | Legal reporting availability is used for downstream TRU or card work | Blocker | find_legal_reporting_units_by_advanced_search_query | The response has zero candidates, multiple candidates without user selection, or a selected row whose TruStatus is not A | Refine the search, select one returned name, and confirm active TRU status before continuing | Yes |
| LRUC.LDG_AVAILABILITY | Full or partial LDG-name or territory availability is requested | Blocker | find_legislative_data_groups_by_advanced_search_query | Name search is blank or all `%`; an empty query lacks a nonblank restrictive filter; the payload differs from the documented fields; paging is incomplete; a returned row lacks Name or LegislativeDataGroupId; a territory-filtered row has the wrong TerritoryShortName; or downstream card work has multiple LDGs without user selection | Send the exact name or territory advanced-search body, return every matching Name for list-only requests, and select one LDG before downstream work | Yes |
| LRUC.TRU_PARITY | Card summary, drilldown, add-card metadata, or HDL key/value resolution | Blocker | find_legal_reporting_unit_calculation_card | Read-only response does not confirm sourceType=TRU or cannot be mapped to the parity-backed calculationEntries retrieval contract | Use only the retrieval endpoint, request fields, and response fields in ora_rest_execution.md after TRU verification | Yes |
| LRUC.CSV_CONTRACT_REQUIRED | Setup task CSV export or import | Blocker | TBD | Task-specific CSV package shape, rows, or job contract is missing | Provide approved CSV/FSM contract evidence before preview | Yes |
| LRUC.COMPONENT_SCOPE | Component-specific HDL preparation | Blocker | get_legal_reporting_unit_card_components | Component identity is missing, ambiguous, or not attached to the selected dirCardId and sourceId | Resolve the component through read-only getCardDetails and CIRComponentPVO retrieval | Yes |
| LRUC.FLEXFIELD_VALUE_SCOPE | Current/default component flexfield values are requested | Blocker | list_component_flexfield_values | Owner, card, component, or effective date is unresolved; multiple component instances match; or returned scope differs from the request | Resolve one exact component, filter only its `overrideType=FLEX` rows, and keep technical metadata internal | Yes |
| LRUC.LOV_BACKED_OVERRIDES | LOV-backed override value is supplied | Blocker | resolve_override_lov_values | Value is not found uniquely in the active card's metadata-declared LOV source | Resolve the supplied display value or code through payrollGenericLOV or the declared resolver | Yes |
| LRUC.CARD_SCHEMA | Any override value is supplied | Blocker | build_card_override_schema | Requested override is not returned by the selected card/component metadata | Use only override fields from getCardDetails for the active card and effective date | Yes |
| LRUC.DEPENDENT_LOV | LOV-backed override has parent binds | Blocker | resolve_dependent_override_lov | Required parent override, LDG, legislation code, effective date, or context value is missing or invalid | Resolve parent values first and re-query the child LOV | Yes |
| LRUC.NO_STATIC_PAYLOAD | Any business change request | Blocker | None | HDL rows are inferred from chat context or sample rows only | Use live target metadata and preview before loader handoff | No |
| LRUC.NO_ENV_VALUES | Authoring packaged resources | Blocker | None | Environment-specific host, tax reporting unit ID, legal reporting unit name, token, or secret would be persisted in tracked resource files | Redact values and use placeholders | Yes |
| LRUC.AUTO_TECHNICAL_KEYS | Every card-specific request | Blocker | resolve_runtime_technical_keys | The workflow asks the functional user for dirCardId, component/definition ID, override-group ID, source/LDG ID, or assignment/association ID | Resolve IDs automatically from unique business-name/date context and keep them internal | No |
| LRUC.OBJECT_EXISTENCE | Every business change | Blocker | resolve_calculation_card_object_existence | Any requested card/component/override/FLEX/value/assignment/association state is based on a failed, partial, or single-date-only lookup, or an existing ancestor/absent child is misclassified | Build the complete object-level graph and reuse existing ancestors while creating only absent leaves | Yes |
| LRUC.DATE_ACTION_CONFIRMATION | Any requested business key exists | Blocker | classify_requested_calculation_card_operation | Existing data was not disclosed, Update/Correction was auto-selected, or no user confirmation exists | Show business path, current value, effective interval, requested date, recommendation, and obtain the user's choice | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| LRUC.TRU_REQUIRED | resolve_tax_reporting_unit | Card-specific request | Tax reporting unit ID and display name | ora_reference_lookups.md |
| LRUC.LRU_AVAILABILITY_SELECTION | find_legal_reporting_units_by_advanced_search_query | Legal reporting availability or name-first TRU resolution | Ordered candidate names, selected EstablishmentId, TruStatus, parent legal entity, and effective dates | ora_reference_lookups.md |
| LRUC.LDG_AVAILABILITY | find_legislative_data_groups_by_advanced_search_query | Full or partial LDG-name or territory discovery | Ordered candidate names plus internally retained LegislativeDataGroupId, territory, currency, and costing structure | ora_reference_lookups.md |
| LRUC.TRU_SOURCE_RESOLUTION | resolve_tax_reporting_unit | readScopeInfoParams returns sourceType=TRU | OrganizationId, LdgId, sourceType=TRU | ora_reference_lookups.md |
| LRUC.TRU_PARITY | find_legal_reporting_unit_calculation_card | Card summary, drilldown, or HDL key/value resolution | dirCardId, cardBaseName, sourceId, sourceType, LDG, and current effective state | ora_reference_lookups.md |
| LRUC.COMPONENT_SCOPE | get_legal_reporting_unit_card_components | Component-specific operation | dirCardCompId, dirCardCompDefId, componentSequence, overrideBaseGroupName, overrideGroupId | ora_reference_lookups.md |
| LRUC.FLEXFIELD_VALUE_SCOPE | list_component_flexfield_values | Current/default component flexfield value list | Exact component identity, ordered FLEX rows, business labels, current/default values, and uniquely resolved LOV meanings when available | ora_reference_lookups.md |
| LRUC.LOV_BACKED_OVERRIDES | resolve_override_lov_values | LOV-backed override value is supplied | override context, name, code, meaning, dataSource, LDG bind | ora_reference_lookups.md |
| LRUC.CARD_SCHEMA | build_card_override_schema | Any override value is supplied | Active-card override metadata and current values | ora_reference_lookups.md |
| LRUC.DEPENDENT_LOV | resolve_dependent_override_lov | LOV dataSource declares parent binds | Parent values, context, LDG, legislation code, effective date, child resolver | ora_reference_lookups.md |
| LRUC.AUTO_TECHNICAL_KEYS | resolve_runtime_technical_keys | Every card-specific request | Internal owner/card/component/field/assignment keys resolved from business context | ora_reference_lookups.md |
| LRUC.OBJECT_EXISTENCE | resolve_calculation_card_object_existence | Every business change | Per-object state, all effective intervals, current values, and adjacent future rows | ora_reference_lookups.md |
| LRUC.DATE_ACTION_CONFIRMATION | classify_requested_calculation_card_operation | Any requested business key exists | Recommended and user-confirmed Update or Correction per object and requested date | ora_reference_lookups.md |
| LRUC.CSV_CONTRACT_REQUIRED | TBD | Export or import | CSV package shape, required columns, import job fields, result identifiers | ora_reference_lookups.md |

## Combined Discovery Enforcement

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LRUC.LDG_TRU_ASSOCIATIONS | Parent combines territory LDGs with PSUs and TRUs | Blocker | list_tax_reporting_unit_associations_by_legislation | The TRU finder requests LegalEntityId instead of PsuId; the query is run per LDG; paging is incomplete; Name, OrganizationId, or LdgId is blank; IDs conflict; an LdgId is orphaned; a returned PsuId conflicts with the same-LDG PSU set; or grouping uses anything except exact LdgId-to-LegislativeDataGroupId equality | Fetch the legislation TRU dataset once with `PsuId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId`, complete paging, deduplicate by OrganizationId, and return the validated candidate set to the parent | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUC.ENFORCE | decision | 5 | design_enforcement | passed->LRUC.PREVIEW_BLOCK;blocked->LRUC.DONE_BLOCKED | LRUC.LOOKUP | stop | Before preview or execution |
