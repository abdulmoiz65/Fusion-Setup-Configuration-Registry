# Legal Entity Calculation Cards Design Enforcement

## Mandatory Mutation Route Gate

| Proposed operation | Severity | Required behavior | Blocking |
|---|---|---|---|
| Any calculation-card create, update, correction, end-date, delete-record, delete-history, or association change selects direct REST | Error | Reject the direct REST mutation. Resolve current state with read-only REST, then prepare only target-supported `CalculationCard` HDL through `core.data-loader` | Yes |
| A requested HDL action is absent or ambiguous in current target metadata | Error | Block the operation and report the missing HDL action or key contract; never fall back to REST | Yes |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task scope | Task code and task name must match the nested skill manifest |
| 2 | Confirm launch scope | If a launch URL is supplied, FS_SCOPEINFOS must parse as Legal Entity Calculation Cards context |
| 3 | Confirm target owner | Payroll statutory unit must resolve uniquely or be verified from launch scope |
| 3a | Confirm legal entity selection | An availability search with multiple matches must stop before PSU or card resolution until the user selects one |
| 3b | Confirm direct LDG search completeness | A full or partial LDG-name or territory list must include every page and preserve all matching names before a list-only request completes |
| 4 | Confirm source contract | HAR-backed calculationEntries retrieval is allowed only for read-only review and HDL key/value resolution; all create, update, end-date, and delete behavior uses target-supported HDL |
| 5 | Confirm value sources | Component metadata, deduction group, and LOV-backed override values must resolve before HDL preview |
| 5a | Confirm flexfield value scope | A read-only flexfield value list must use one exact component and only that component's FLEX rows |
| 6 | Confirm no invented behavior | Unknown endpoints, defaults, field mappings, and validation rules remain TBD |
| 7 | Confirm target environment | Resolve the active target from `core/auth/fusionEnv.properties` and keep source evidence separate |
| 8 | Confirm existing HDL parent keys | Search existing cards/components first and resolve original dates and sequences before applying creation defaults |
| 8a | Confirm HDL component name and value type | Resolve the exact DirCardCompDefName and dispatch every field by overrideType before selecting child sections |
| 8b | Confirm HDL schema and mapping | Validate only the planned FLEX or enterable-value sections and keys against the live target `CalculationCard` template |
| 8c | Confirm object-level operation | Prove complete current/future/history state, resolve all runtime IDs internally, and obtain Update/Correction confirmation for every existing requested business key |
| 9 | Confirm staged approval | Show exact DAT content before writing any file; separately gate ZIP, upload, and load initiation |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LEC.SCOPE | Every request | Blocker | None | Task code or task name differs from the nested skill manifest | Use the Legal Entity Calculation Cards task metadata | Yes |
| LEC.LAUNCH_SCOPE | FSM launch URL is supplied | Blocker | parse_legal_entity_launch_scope | FS_SCOPEINFOS is missing, malformed, or does not include a LEGAL_ENTITY_ID group | Provide a redacted launch URL or extracted scope values | Yes |
| LEC.PSU_REQUIRED | Card-specific review or edit | Blocker | resolve_payroll_statutory_unit | Payroll statutory unit is missing or ambiguous after launch-scope parsing | Supply a unique payroll statutory unit reference or approved verification source | Yes |
| LEC.LE_AVAILABILITY_SELECTION | Legal entity availability or name-first PSU resolution is requested | Blocker | find_legal_entities_by_advanced_search_query | The request omits or changes the mandatory PsuFlag=Y filter; the response has zero candidates; multiple candidates lack user selection for downstream work; or any returned row has PsuFlag other than Y | Send the required PSU filter, refine the search when needed, select one returned name for downstream work, and reject a non-PSU response row | Yes |
| LEC.LDG_AVAILABILITY | Full or partial LDG-name or territory availability is requested | Blocker | find_legislative_data_groups_by_advanced_search_query | Name search is blank or all `%`; an empty query lacks a nonblank restrictive filter; the payload differs from the documented fields; paging is incomplete; a returned row lacks Name or LegislativeDataGroupId; a territory-filtered row has the wrong TerritoryShortName; or downstream card work has multiple LDGs without user selection | Send the exact name or territory advanced-search body, return every matching Name for list-only requests, and select one LDG before downstream work | Yes |
| LEC.PSU_LEGISLATION_LIST | PSU or Legal Entity Org Cards are requested by legislation or country code | Blocker | list_payroll_statutory_units_by_legislation_code or list_payroll_statutory_units_by_legislation_and_ldg | The legislation code is missing; the LDG-filtered resolver is skipped when LdgId is already known; OrgPayrollStatutoryUnitPVO returns zero rows; downstream card work has multiple rows without user selection; or a selected row lacks LegalEntityId, Name, OrganizationId, or LdgId | Send findByLegislationCode with pLegislationCode; if LdgId is known, add findByLdgId and pLdgId; return names for list-only requests, and select one PSU before downstream card work | Yes |
| LEC.HAR_CONTRACT | Card summary, drilldown, add-card metadata, or HDL key/value resolution | Blocker | find_legal_entity_calculation_card | Read-only retrieval cannot be mapped to a captured calculationEntries endpoint and field set | Use only the source-backed retrieval endpoint, request fields, and response fields in ora_rest_execution.md | Yes |
| LEC.CSV_CONTRACT_REQUIRED | Setup task CSV export or import | Blocker | TBD | Task-specific CSV package shape, rows, or job contract is missing | Provide approved CSV/FSM contract evidence before preview | Yes |
| LEC.COMPONENT_SCOPE | Component-specific HDL preparation | Blocker | get_legal_entity_card_components | Component identity is missing, ambiguous, or not attached to the selected dirCardId and sourceId | Resolve the component through read-only getCardDetails and CIRComponentPVO retrieval | Yes |
| LEC.FLEXFIELD_VALUE_SCOPE | Current/default component flexfield values are requested | Blocker | list_component_flexfield_values | Owner, card, component, or effective date is unresolved; multiple component instances match; or returned scope differs from the request | Resolve one exact component, filter only its `overrideType=FLEX` rows, and keep technical metadata internal | Yes |
| LEC.LOV_BACKED_OVERRIDES | LOV-backed override value is supplied | Blocker | resolve_override_lov_values | Value is not found uniquely in the active card's metadata-declared LOV source | Resolve the supplied display value or code through payrollGenericLOV or the declared resolver | Yes |
| LEC.CARD_SCHEMA | Any override value is supplied | Blocker | build_card_override_schema | Requested override is not returned by the selected card/component metadata | Use only override fields from getCardDetails for the active card and effective date | Yes |
| LEC.DEPENDENT_LOV | LOV-backed override has parent binds | Blocker | resolve_dependent_override_lov | Required parent override, LDG, legislation code, effective date, or context value is missing or invalid | Resolve parent values first and re-query the child LOV | Yes |
| LEC.NO_HAR_FIELD_REUSE | Any non-gratuity card is selected | Blocker | build_card_override_schema | Gratuity sample override codes are applied to a card that did not return those codes | Treat HAR override rows as examples only | No |
| LEC.NO_STATIC_PAYLOAD | Any business change request | Blocker | None | HDL rows are inferred from chat context or sample rows only | Use live target metadata and preview before loader handoff | No |
| LEC.HAR_SCOPE_LIMIT | Legal Reporting Unit or non-PSU flow is requested | Blocker | None | The source contract is being reused outside the Legal Entity sourceType=PSU HAR scope | Capture or provide a matching TRU/non-PSU HAR or approved contract | No |
| LEC.NO_ENV_VALUES | Authoring packaged resources | Blocker | None | Environment-specific host, legal entity ID, legal entity name, token, or secret would be persisted in tracked resource files | Redact values and use placeholders | Yes |
| LEC.TARGET_ENV_AUTHORITY | Target lookup, preview, or import | Blocker | resolve_target_environment | Active target differs from `core/auth/fusionEnv.properties` or the source host is being reused implicitly | Re-read the properties file and show only the non-secret environment identity | Yes |
| LEC.HDL_LIVE_SCHEMA | Component HDL preview | Blocker | get_live_calculation_card_template | A planned section, key, Flex context, or segment column is absent or ambiguous in the live template | Use only exact live-template section and attribute names | Yes |
| LEC.HDL_NO_SOURCE_IDS | Source-equivalent component HDL preview | Blocker | map_component_to_hdl | A source card, component, definition, Flex, owner, or LDG ID is present in the proposed DAT | Remove source IDs and link by validated target names, dates, and sequences | Yes |
| LEC.HDL_EXISTING_CARD_KEYS | Every create-or-update HDL preview | Blocker | list_existing_legal_entity_calculation_cards_for_hdl and find_legal_entity_calculation_card | Existing-card discovery was skipped, failed/incomplete discovery is treated as absence, multiple cards remain, or an existing card lacks original EffectiveStartDate, current EffectiveEndDate, or CardSequence | Run owner-scoped mode=G first, select one exact card, and reuse its returned parent keys; use mode=ADD only after a complete zero-match result | Yes |
| LEC.HDL_EXISTING_COMPONENT | Component HDL preview | Blocker | resolve_existing_component_hdl_keys | An existing component is duplicated, its history/keys are incomplete, or a new component sequence is selected without a complete conflict check | Disclose the existing business interval and ask for Update or Correction; create only after a complete no-match result | Yes |
| LEC.AUTO_TECHNICAL_KEYS | Every card-specific request | Blocker | resolve_runtime_technical_keys | The workflow asks the functional user for dirCardId, component/definition ID, override-group ID, source/LDG ID, or assignment/association ID | Resolve IDs automatically from unique business-name/date context and keep them internal | No |
| LEC.OBJECT_EXISTENCE | Every business change | Blocker | resolve_calculation_card_object_existence | Any requested card/component/override/FLEX/value/assignment/association state is based on a failed, partial, or single-date-only lookup, or an existing ancestor/absent child is misclassified | Build the complete object-level graph and reuse existing ancestors while creating only absent leaves | Yes |
| LEC.DATE_ACTION_CONFIRMATION | Any requested business key exists | Blocker | classify_requested_calculation_card_operation | Existing data was not disclosed, Update/Correction was auto-selected, or no user confirmation exists | Show business path, current value, effective interval, requested date, recommendation, and obtain the user's choice | Yes |
| LEC.HDL_COMPONENT_NAME | Component HDL preview | Blocker | resolve_hdl_component_definition_name | The exact existing target export or unique target `CIRComponentPVO.ComponentName` is unresolved; a source/UI/base/generic-guidance label overrides target metadata; the target definition ID is proposed as a DAT workaround; or the resolved name is not propagated unchanged to every applicable child | Use the exact target-supported component name. When the selected target `US_ORG_FEDERAL_INCOME_TAX` row returns `ComponentName=Federal Taxes`, use `Federal Taxes` and retain `DirCardCompDefId` only as lookup evidence | Yes |
| LEC.HDL_VALUE_RECORD_TYPE | Any requested component value in HDL | Blocker | classify_hdl_override_record_type | A FLEX-only filter discards an OVERRIDE field, an OVERRIDE is mapped to ComponentDetail, a FLEX row is mapped to enterable-value records, or overrideType is unsupported | Dispatch FLEX to ComponentDetail and OVERRIDE to CalculationValueDefinition plus EnterableCalculationValue | Yes |
| LEC.HDL_ENTERABLE_VALUE | overrideType=OVERRIDE | Blocker | resolve_hdl_enterable_calculation_value | ValueDefinitionName, stored Value1, type/format, null contract, effective dates, or parent keys are missing or ambiguous | Resolve the exact live field and stored value, then emit one CalculationValueDefinition/EnterableCalculationValue pair with parent-contained dates | Yes |
| LEC.HDL_PARENT_KEY | ComponentDetail HDL preview | Blocker | map_component_to_hdl | `ComponentDetail.DirCardCompDefName` differs from the parent `CardComponent.DirCardCompDefName` or is populated with a Flex-context display name | Copy the exact component definition name from the parent row; keep the Flex context code in the DFF context columns | Yes |
| LEC.HDL_NO_PLACEHOLDERS | Completed DAT preview | Blocker | map_component_to_hdl | Any implementation-owned date, sequence, component name, value-definition name, or stored value remains as a placeholder or TBD | Finish the owning read-only resolver or return a blocking diagnostic; never present placeholders as a completed preview | Yes |
| LEC.DAT_PREVIEW_GATE | DAT, ZIP, upload, or load initiation | Blocker | None | The exact DAT preview was not shown and explicitly approved | Keep the result in chat and request approval before file creation | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| LEC.LAUNCH_SCOPE | parse_legal_entity_launch_scope | FSM launch URL is supplied | Scope type, legal entity ID, legal entity display value | ora_reference_lookups.md |
| LEC.PSU_REQUIRED | resolve_payroll_statutory_unit | Card-specific request | Payroll statutory unit ID and display name | ora_reference_lookups.md |
| LEC.LE_AVAILABILITY_SELECTION | find_legal_entities_by_advanced_search_query | Legal entity availability or name-first PSU resolution | Ordered candidate names, selected LegalEntityId, PsuFlag, and effective dates | ora_reference_lookups.md |
| LEC.LDG_AVAILABILITY | find_legislative_data_groups_by_advanced_search_query | Full or partial LDG-name or territory discovery | Ordered candidate names plus internally retained LegislativeDataGroupId, territory, currency, and costing structure | ora_reference_lookups.md |
| LEC.PSU_LEGISLATION_LIST | list_payroll_statutory_units_by_legislation_code or list_payroll_statutory_units_by_legislation_and_ldg | PSU or Legal Entity Org Cards by legislation or country code, optionally narrowed by LdgId | Ordered candidate names, LegalEntityId, OrganizationId, LdgId, and sourceType=PSU | ora_reference_lookups.md |
| LEC.PSU_SOURCE_RESOLUTION | resolve_payroll_statutory_unit | readScopeInfoParams returns sourceType=PSU | OrganizationId, LdgId, sourceType=PSU | ora_reference_lookups.md |
| LEC.HAR_CONTRACT | find_legal_entity_calculation_card | Card summary, drilldown, or HDL key/value resolution | dirCardId, cardBaseName, sourceId, sourceType, LDG, and current effective state | ora_reference_lookups.md |
| LEC.COMPONENT_SCOPE | get_legal_entity_card_components | Component-specific operation | dirCardCompId, dirCardCompDefId, componentSequence, overrideBaseGroupName, overrideGroupId | ora_reference_lookups.md |
| LEC.FLEXFIELD_VALUE_SCOPE | list_component_flexfield_values | Current/default component flexfield value list | Exact component identity, ordered FLEX rows, business labels, current/default values, and uniquely resolved LOV meanings when available | ora_reference_lookups.md |
| LEC.LOV_BACKED_OVERRIDES | resolve_override_lov_values | LOV-backed override value is supplied | override context, name, code, meaning, value set, LDG bind | ora_reference_lookups.md |
| LEC.CARD_SCHEMA | build_card_override_schema | Any override value is supplied | Active-card override metadata and current values | ora_reference_lookups.md |
| LEC.DEPENDENT_LOV | resolve_dependent_override_lov | LOV dataSource declares parent binds | Parent values, context, LDG, legislation code, effective date, child resolver | ora_reference_lookups.md |
| LEC.CSV_CONTRACT_REQUIRED | TBD | Export or import | CSV package shape, required columns, import job fields, result identifiers | ora_reference_lookups.md |
| LEC.TARGET_ENV_AUTHORITY | resolve_target_environment | Target lookup, preview, or import | Non-secret target environment identity and REST base URL | ora_reference_lookups.md |
| LEC.HDL_LIVE_SCHEMA | get_live_calculation_card_template | Component HDL preview or generation | Exact CalculationCard/CardComponent keys plus applicable ComponentDetail/FLEX or CalculationValueDefinition/EnterableCalculationValue columns | ora_reference_lookups.md |
| LEC.HDL_NO_SOURCE_IDS | map_component_to_hdl | Source-equivalent component HDL | Target names, dates, sequences, component/context metadata, and raw override values | ora_reference_lookups.md |
| LEC.HDL_EXISTING_CARD_KEYS | list_existing_legal_entity_calculation_cards_for_hdl and find_legal_entity_calculation_card | Every create-or-update HDL preview | Existing-or-new state, original card start, current card end, CardSequence, card name/base name, and exact dirCardId drilldown evidence when existing | ora_reference_lookups.md |
| LEC.HDL_EXISTING_COMPONENT | resolve_existing_component_hdl_keys | Component HDL preview | Existing-or-new state, original component start, current component end, ComponentSequence, definition metadata, and used sequences | ora_reference_lookups.md |
| LEC.AUTO_TECHNICAL_KEYS | resolve_runtime_technical_keys | Every card-specific request | Internal owner/card/component/field/assignment keys resolved from business context | ora_reference_lookups.md |
| LEC.OBJECT_EXISTENCE | resolve_calculation_card_object_existence | Every business change | Per-object state, all effective intervals, current values, and adjacent future rows | ora_reference_lookups.md |
| LEC.DATE_ACTION_CONFIRMATION | classify_requested_calculation_card_operation | Any requested business key exists | Recommended and user-confirmed Update or Correction per object and requested date | ora_reference_lookups.md |
| LEC.HDL_COMPONENT_NAME | resolve_hdl_component_definition_name | Component HDL preview | Exact target-supported `DirCardCompDefName`, its matching internal definition-ID evidence, and proof of unchanged child-key propagation | ora_reference_lookups.md |
| LEC.HDL_VALUE_RECORD_TYPE | classify_hdl_override_record_type | Every requested component field | Exact overrideType and applicable HDL child section plan | ora_reference_lookups.md |
| LEC.HDL_ENTERABLE_VALUE | resolve_hdl_enterable_calculation_value | overrideType=OVERRIDE | ValueDefinitionName, Value1, parent user keys, and effective interval | ora_reference_lookups.md |
| LEC.HDL_PARENT_KEY | map_component_to_hdl | ComponentDetail HDL preview | Exact parent CardComponent definition name plus the separately resolved Flex context code | ora_reference_lookups.md |
| LEC.HDL_NO_PLACEHOLDERS | map_component_to_hdl | Completed DAT preview | Concrete dates, sequences, names, sections, and stored values | ora_reference_lookups.md |

## Combined Discovery Enforcement

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| LEC.LDG_PSU_ASSOCIATIONS | Parent combines territory LDGs with PSUs and TRUs | Blocker | list_payroll_statutory_unit_associations_by_legislation | The PSU query is run per LDG; paging is incomplete; Name, OrganizationId, or LdgId is blank; IDs conflict; an LdgId is orphaned; or grouping uses anything except exact LdgId-to-LegislativeDataGroupId equality | Fetch the legislation PSU dataset once, complete paging, deduplicate by OrganizationId, and return the validated candidate set to the parent | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LEC.ENFORCE | decision | 5 | design_enforcement | passed->LEC.PREVIEW_BLOCK;blocked->LEC.DONE_BLOCKED | LEC.LOOKUP | stop | Before preview or execution |
