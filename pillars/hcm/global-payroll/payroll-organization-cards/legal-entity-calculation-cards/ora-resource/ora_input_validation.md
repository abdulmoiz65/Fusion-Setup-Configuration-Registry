# Legal Entity Calculation Cards Input Validation

## Mutation Route Validation

| Requested route | Result | Required action |
|---|---|---|
| REST fetch or retrieval | Allowed only when the operation creates no Fusion business data | Validate scope, fields, paging, and response identity |
| Direct REST create, update, correction, end-date, or delete | Blocked | Never call or prepare a calculation-card REST mutation payload |
| HDL create, update, correction, end-date, or delete | Conditional | Continue only after the live `CalculationCard` template proves the requested action, sections, user keys, and effective-date contract; then route through `core.data-loader` |

## Automatic Operation Classification Validation

| Target-state result | Resolved operation | Required user interaction |
|---|---|---|
| Complete current/future/history lookup finds no exact business-key row | CREATE for that missing object only | State that no existing matching data was found; continue without an Update/Correction question |
| Exact row contains the requested date and the date equals its EffectiveStartDate | Existing data; Correction recommended | Show the business path, value and interval, then ask the user to confirm Correction or a target-supported alternative |
| Exact row contains the requested date after its EffectiveStartDate | Existing data; Update recommended | Explain that Update preserves prior history from the requested date while Correction changes the selected slice; ask which one to use |
| Same business key exists only in history/future or adjacent intervals conflict | Existing data; no duplicate create | Show the relevant intervals and ask for one target-supported date-effective action |
| Existing parent is found but the requested child business key is absent | CREATE the child under the existing parent | Reuse automatically resolved parent keys; do not create the parent again |
| Lookup is partial, failed, unauthorized, single-date-only, or ambiguous | Unresolved | Block classification; ask only for a business discriminator or fix the lookup, never a technical ID |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Request classification | Review/export intent or desired business outcome; create/update/correct wording is provisional | Block planning | Ask what business result is required, then classify the HDL operation from target state |
| Target payroll statutory unit | Payroll statutory unit business name or functional context | Block preview | Resolve the owner and internal source/LDG IDs automatically; ask for a business selection only when names remain ambiguous |
| Calculation card selection | Card display name or base name | Block card-specific edit | Resolve `dirCardId` and definition metadata automatically from owner-scoped discovery; never request a technical card ID |
| Component flexfield value list | Exact payroll statutory unit, card, component business name, and effective date | Block the value list | Resolve the card and component sequence internally; when names repeat, show business intervals/current-value context for user selection before reading FLEX rows |
| Legal entity availability search | Nonblank name or `LegalEntityIdentifier` search text; wildcard query must contain at least one non-`%` character | Block availability POST | Provide a legal-entity name or identifier fragment |
| Legislation code PSU list | Nonblank legislation or country code, such as US | Block legislation-code lookup | Provide a valid legislation code and use the `OrgPayrollStatutoryUnitPVO` findByLegislationCode contract |
| Legal entity availability REST contract | Versioned standard resource path, POST, `Content-Type: application/vnd.oracle.adf.action+json`, `Accept: application/vnd.oracle.adf.actionresult+json, application/json`, and `filters` containing `name=["PsuFlag"]` with `terms=["Y"]` | Block availability POST | Use the live-described contract in `ora_rest_execution.md`; retrieve the resource `describe` when Fusion reports a method/media-type mismatch |
| Legal entity availability response | `result.summary` and `result.items`; each candidate must have nonblank `Name` and `LegalEntityId` plus `PsuFlag=Y` | Block candidate selection | Return response diagnostics and do not infer candidates from a malformed or non-PSU payload |
| Legislative Data Group availability search | Either a nonblank full or partial name containing at least one non-`%` character, or a source-backed territory request; `US` and `United States` map to `United States` | Block LDG availability POST | Provide a meaningful LDG name fragment or a supported exact Fusion territory value |
| Legislative Data Group availability REST contract | Runtime-routed `legislativeDataGroups/action/findByAdvancedSearchQuery` path, POST, JSON body, `limit="500"`, `searchFields=["Name"]`, the five documented display fields, and `offset=0`; name mode requires a nonblank query plus `filters=[]`, while US territory mode requires `query=""` plus the exact `TerritoryShortName=United States` filter | Block LDG availability POST | Use the exact read-only name or territory contract in `ora_rest_execution.md` and resolve the host and route in the active environment |
| Legislative Data Group availability response | `result.summary` and `result.items`; each candidate must have nonblank `Name` and `LegislativeDataGroupId`, plus matching `TerritoryShortName` for territory mode | Block LDG candidate handling | Preserve redacted diagnostics and do not infer candidates from a malformed or filter-violating payload |
| Effective-dated context | Effective date when required by the approved source contract | Block effective-dated edit | Provide the effective date in the approved format |
| FSM or CSV operation | Task-specific export/import action contract and source rows | Block export/import execution | Obtain the approved task-specific contract; current source only proves catalog support |
| HDL component preview | Exact target payroll statutory unit and LDG names, requested card/component/field/value/effective date, complete object-level existence state, confirmed per-object create/update/correction decision, resolved dates/sequences, exact HDL component definition name, matched override metadata and record type, and every planned live-template section/key | Block DAT preview | Search complete current/future/history state first, resolve technical keys internally, obtain Update/Correction confirmation for existing data, dispatch FLEX versus OVERRIDE, validate parent linkage and stored values, then validate against the live `CalculationCard` UCM template |
| Card details request | Owner, LDG, card business name, effective date, and expand value; `dirCardId` is an internal resolver output | Block card drilldown | Run owner-scoped mode=G discovery without `dirCardId`, retain the unique returned ID internally, then use the required expand value |
| Create-card list request | sourceId, sourceType=PSU, effectiveDate, mode=ADD, and expand=Cards | Block card create selection | Resolve the owner first, then retrieve available cards without dirCardId |
| Add-card template request | sourceId, sourceType=PSU, legislativeDataGroupId, effectiveDate, cardBaseName, mode=ADD, isGlobalPage=true, expand=Cards,Components,Overrides,Associations, plus either `dirCardCompDefId` alone or the BaseComponentName/ComponentName group-name mapping | Block add preview | Resolve ComponentContextPVO first. Map every returned sequence to its `contextN` field and require a value before requesting the template; do not combine a definition ID with group-name fields |
| Card-level end date | Exact PSU, LDG, card user keys, current effective interval, and target-supported HDL end-date action | Block DAT preview | Retrieve the card-level target and block if live HDL metadata does not prove the action |
| Association change | Exact parent card/component keys, selected association identity, effective interval, and target-supported HDL section/action | Block DAT preview | Use read-only association metadata as evidence and map only to live target HDL; never construct a REST association payload |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Catalog task code and task name match the nested task manifest | Satisfied | Keep task scope local to this nested skill |
| ExportImportSupportedFlag and CSVExportImportSupportedFlag are Y | Satisfied | Allow task-specific FSM or CSV routing after source contract validation |
| LEGAL_ENTITY_ID resolves through OrgPayrollStatutoryUnitPVO to OrganizationId and LdgId | Satisfied | Use OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=PSU |
| Legislation code resolves through OrgPayrollStatutoryUnitPVO to LegalEntityId, Name, OrganizationId, and LdgId | Satisfied for a list-only request; blocked only for downstream card work when the selected PSU is not unique | Return the names-only list and finish when only a list was requested. If card work was also requested, wait for the user to select one |
| Legislation code plus LDG ID resolves through OrgPayrollStatutoryUnitPVO to LegalEntityId, Name, OrganizationId, and LdgId | Satisfied for a list-only request; blocked only for downstream card work when the selected PSU is not unique | Prefer this filtered lookup when LdgId is already known and verify each returned row's LdgId equals the supplied value |
| Payroll statutory unit cannot be resolved uniquely | Blocked | Show the matching PSU/legal-entity business names and LDG names and require a functional selection; keep identifiers internal |
| Calculation card or component fields are not covered by the HAR-backed contract | Blocked | Mark the field mapping as TBD and stop before preview |
| Create-card list request does not include dirCardId | Satisfied | Continue because dirCardId is not available before card creation |
| getCardDetails returns no components for a component-specific operation | Blocked | Ask for a valid card/component selection |
| Component flexfield value lookup matches multiple component rows | Blocked | Show component business names/effective intervals and ask for a functional selection; retain component sequence internally and do not combine instances |
| Owner-scoped HDL card discovery returns one exact existing card | Existing data found | Re-run exact drilldown with returned `dirCardId`, retrieve complete effective history, notify the user with business dates, and request Update/Correction confirmation before DAT preview |
| Owner-scoped HDL card discovery returns zero exact cards with a complete current/future/history response | Satisfied for new-card path | State that no existing card was found, resolve the addable definition through mode=ADD, and apply only new-row defaults |
| Owner-scoped HDL card discovery fails, is incomplete, or returns multiple exact cards | Blocked | Do not treat lookup failure as card absence; show business names/effective intervals and require a functional selection while keeping CardSequence internal |
| Existing component matches the requested component | Existing data found | Reuse the component's original EffectiveStartDate, current EffectiveEndDate, and ComponentSequence internally, disclose the selected interval/current value, and ask the user to confirm Update or Correction; do not generate a duplicate component |
| No component matches and the complete component set is known | Satisfied for create | Use the unique definition sequence when returned or a proven nonconflicting creation sequence |
| Selected component has no `overrideType=FLEX` rows | Satisfied | Return `Flexfield values:` followed by `None` |
| Current LOV value has no unique display meaning | Satisfied for the read-only value list | Return the stored value without guessing; require unique LOV validation only if the value will be written later |
| A LOV lookup returns count other than one for a required exact value | Blocked | Return the lookup source and require a unique value |
| Override field is not returned by the selected card/component metadata | Blocked | Do not reuse fields from another card; ask for a valid field from the card schema |
| Requested override has overrideType=FLEX | Satisfied after DFF mapping | Produce ComponentDetail only after the exact context, segment, stored value, and parent component name are resolved |
| Requested override has overrideType=OVERRIDE | Satisfied after value-definition mapping | Produce CalculationValueDefinition plus EnterableCalculationValue with exact ValueDefinitionName, Value1, effective dates, and parent keys |
| Requested override has blank or unsupported overrideType | Blocked | Do not force the field into ComponentDetail; return the unsupported metadata type |
| Business display value has no unique stored-code mapping | Blocked | Run the metadata-declared LOV or use component-specific authoritative guidance; do not guess from the UI label |
| Override LOV dataSource has unresolved parent binds | Blocked | Resolve parent override values or context fields first |
| Dependent override graph has a cycle or unknown parent | Blocked | Stop and request source evidence or a corrected selection |
| Required context override is not user-supplied but has a current/default metadata value | Satisfied | Auto-carry it into the HDL preview and applicable child row |
| Card-level end date is requested but only component-level END_DATE is source-confirmed | Blocked | Ask for source evidence or use the component end-date operation |
| Association identity or association end-date mode is missing | Blocked | Resolve the association from getCardDetails or request an approved source contract |
| Existing-card request has a target card that is missing or not unique for the requested owner, card business name, and effective date | Blocked | Resolve the target card by business context before authoring child HDL rows. Treat zero exact matches as new only after a complete valid owner-scoped discovery; then resolve the add-card definition and emit one same-file root `CalculationCard` row without dirCardId |
| Legal entity availability returns multiple rows | Satisfied for a list-only request; blocked only for downstream card work | Return the names-only list and finish when only a list was requested. If card work was also requested, wait for the user to select one |
| Legal entity availability request omits or changes the mandatory `PsuFlag=Y` filter | Blocked | Correct the payload before the POST; do not execute an unfiltered PSU availability search |
| Legal entity availability response contains `PsuFlag` other than `Y` | Blocked as a response-contract failure | Preserve redacted diagnostics and do not return or use the non-PSU row |
| Legislative Data Group availability returns one or more rows | Satisfied for a list-only request; blocked only for downstream card work when multiple LDGs have no user selection | Return every name in response order and finish when only a list was requested; otherwise wait for one selected LDG |
| Legislative Data Group availability response is paged | Incomplete until `hasMore=false` | Continue with the next offset, preserve the same query, fields, and filters, and deduplicate by LegislativeDataGroupId |
| US territory availability returns a row whose `TerritoryShortName` is not `United States` | Blocked as a response-contract failure | Preserve redacted diagnostics and do not return or use the mismatched row |
| Target `getCardDetails` already returns the intended component sequence/name or requested child business key | Existing data found | Carry the internal keys, show the selected interval and requested date, and ask the user to confirm Update or Correction before emitting HDL; do not auto-update or duplicate the row |
| Live `CalculationCard` template lacks a planned child section or key | Blocked | Return the exact missing CalculationCard, CardComponent, ComponentDetail/FLEX, CalculationValueDefinition, or EnterableCalculationValue item; do not invent it from a sample DAT |
| A source instance ID or definition ID is about to be copied into target HDL | Blocked | Remove the ID and resolve target linkage by names and sequences, or resolve a target ID only when Central explicitly requires it |
| DAT preview has not been explicitly approved | Blocked | Do not create a DAT file or ZIP and do not upload or initiate a load |
| HDL request omits existing CardSequence, ComponentSequence, or original start dates | Satisfied after lookup | Resolve them from the exact existing card/component; creation defaults are not applicable |
| HDL creation omits CardSequence, ComponentSequence, EffectiveStartDate, or EffectiveEndDate | Satisfied after documented defaulting | Use new-card sequence 1 when free, the unique target component sequence or 1 when free, the runtime system date resolved once, and the parent-bounded end date |
| An HDL creation sequence default conflicts | Satisfied only when complete state proves another value | Select the lowest positive unused sequence from the complete returned set; otherwise block without exposing a placeholder |
| A defaulted child date falls outside the parent interval | Blocked | Resolve a valid parent-contained date; do not silently create an invalid interval |
| Any read-only lookup contract, HDL action, target-template field, or defaulting rule is missing | Blocked | Request source evidence before DAT preview or loader handoff |

## Field Validation

| Check | What Happens |
|---|---|
| Task code | Must remain PAY_MANAGE_LEGAL_ENTITY_DEDUCTION_RECORDS |
| Task name | Must remain Legal Entity Calculation Cards |
| Target organization type | Must be payroll statutory unit unless an approved source expands the scope |
| Source type | Must be PSU for the Legal Entity Calculation Cards flow captured in the HAR |
| Availability user output | For one or more matches, show only `Legal Entity names:` and each returned `Name`, one name per line in response order. Keep IDs, identifiers, flags, parent organizations, dates, counts, offsets, and pagination internal unless explicitly requested |
| Legal entity launch source resolution | LEGAL_ENTITY_ID must resolve through the single serialized OrgPayrollStatutoryUnitPVO finder using AdditionalViewCriteria=findByLegalEntityId when sourceId and LDG are not already supplied |
| Legislation-code PSU source resolution | Legislation or country code must resolve through OrgPayrollStatutoryUnitPVO using AdditionalViewCriteria=findByLegislationCode, ParameterKeys=pLegislationCode, and DisplayAttributes=LegalEntityId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId |
| Legislation-code plus LDG source resolution | When LdgId is already known, resolve through OrgPayrollStatutoryUnitPVO using AdditionalViewCriteria=findByLegislationCode&#124;&#124;findByLdgId, ParameterKeys=pLegislationCode&#124;&#124;pLdgId, and ParameterValues={LegislationCode}&#124;&#124;{LdgId} |
| Card display name | Show `cardName` to the user for create-card lists; keep `cardBaseName` behind the scene for operations |
| Read-only state | readOnlyFlag must be N before preparing an HDL edit, end-date, or delete; this flag never authorizes REST mutation |
| Add-card mode | mode must be ADD and expand must be Cards,Components,Overrides,Associations |
| Create-card list mode | mode must be ADD and expand must be Cards |
| Drilldown mode | mode must be G, showEmptyComponent must be N, and expand must be Cards,Components,Overrides,CompAssociation |
| Dynamic override schema | Override fields must be discovered from getCardDetails for the selected card/component and effective date |
| HDL override dispatch | Each requested override must use its returned overrideType: FLEX maps only to ComponentDetail; OVERRIDE maps only to CalculationValueDefinition and EnterableCalculationValue; blank or unsupported types block preview |
| Component flexfield value output | Keep only the exact component's `overrideType=FLEX` rows and return `Flexfield values:` plus one `Name: Value` line per row in response order. Prefer `title`, otherwise `name`; render null or empty as `Blank`. Do not display IDs, codes, categories, flags, dataSource, pagination, or component metadata by default |
| Current values versus allowed values | A request for flexfield values returns current/default values only. Retrieve LOV option rows only when the user asks for allowed or available values |
| HDL override mapping | Each requested value must use the selected card's override metadata and dispatch by `overrideType` to the applicable HDL child section |
| Auto-carried required context | Required or populated FLEX context overrides may be included even when not changed by the user; user-changed values win by name and context |
| End-date component | The live target template must prove the HDL end-date action and complete component user key; runtime IDs remain read-only evidence |
| Card-level end date | The live target template must prove a card-level HDL end-date action and complete card user key |
| Component Correct or Update | Must be user-confirmed after existing-data disclosure and must preserve componentSequence, internal dirCardCompId evidence, effectiveStartDate, overrideBaseGroupName, overrides, and association context from getCardDetails |
| Component Delete History | Must use a target-supported HDL delete-history action, selected history user key, irreversible approval, and no automatic retry |
| Add association | associations[] must be populated only from active card association metadata and source-confirmed user changes |
| Override metadata | The active card metadata defines code, name, title, category, overrideType, controlType, type, nullable, contextRequired, display, dataSource, current value, and userOverridden |
| Dependent LOV | Parent override, LDG, legislation, effective date, or component context binds must be resolved before child LOV validation |
| Non-LOV override | Validate by metadata type, nullability, format, and unit of measure when returned |
| Example gratuity fields | BASIS_FOR_CALCULATION, GRATUITY_SALARY_FORMULA, and GRATUITY_REFERENCE_FORMULA are HAR examples only, not global Legal Entity fields |
| CSV rows | Must match the approved task-specific CSV shape before import |
| Route contract | REST is retrieval-only; every calculation-card create, update, correction, end-date, or delete must use target-supported HDL through `core.data-loader` |
| Target environment | Read `environment` and `restBaseUrl` from `core/auth/fusionEnv.properties`; do not hardcode or infer the active pod from a source URL or prior conversation |
| Legal entity search query | Preserve a user-supplied nonblank wildcard query; otherwise trim the text, split on whitespace, join terms with `%`, and add leading and trailing `%` |
| Legal entity search endpoint | Use `/hcmRestApi/resources/11.13.18.05/hcmLegalEntities/action/findByAdvancedSearchQuery`; do not omit the REST version or default to a browser-routed `rv:` path |
| Legal entity search media types | Send `Content-Type: application/vnd.oracle.adf.action+json` and accept `application/vnd.oracle.adf.actionresult+json, application/json`; plain request `application/json` does not satisfy the versioned action contract |
| Legal entity PSU filter | Send `filters` as an array containing the PSU eligibility object with `name=["PsuFlag"]` and `terms=["Y"]`; do not send an empty filter array or omit that object |
| Legal entity search pagination | Parse string or numeric `count`, `limit`, and `offset`; follow `hasMore=true` without changing the query and deduplicate candidates by `LegalEntityId` while preserving response order |
| Parent card context | An existing target card must resolve uniquely by payroll statutory unit, LDG, card definition/name, sequence, and effective date; its effective interval bounds all new child rows. A new card must use one same-file parent `CalculationCard` row with resolved PSU, LDG, card definition, sequence, and effective date; it does not use `dirCardId` |
| Existing parent values | Original card/component EffectiveStartDate, current EffectiveEndDate, CardSequence, and ComponentSequence must come from the exact target instance and must not be replaced by new-row defaults |
| CardComponent linkage | Use target HDL names, target effective dates, CardSequence, and ComponentSequence; do not copy source IDs, source-only dates, or Redwood group labels into HDL keys |
| HDL component definition name | Prefer an existing target HDL/exported user key; otherwise use the exact unique target `CIRComponentPVO.ComponentName` for the selected card, `BaseComponentName`, LDG, and effective date. Use `getCardDetails` group metadata only to corroborate the row, and use generic Oracle guidance only for structure. When the selected target row has `BaseComponentName=US_ORG_FEDERAL_INCOME_TAX` and `ComponentName=Federal Taxes`, `DirCardCompDefName` must be `Federal Taxes`. Block on missing, ambiguous, or conflicting target evidence |
| ComponentDetail parent key and context | `DirCardCompDefName` must exactly match `CardComponent.DirCardCompDefName`; it is not the Flex-context display name. `DirInformationCategory` and `FLEX:Deduction Developer DF` are the exact Flex context code |
| ComponentDetail parent reference | Before preview, compare payroll statutory unit, LDG, card definition, card sequence, component sequence, component definition name, and effective date linkage with the existing or same-file `CardComponent`; block when any parent user-key value differs |
| HDL override column | Must exactly match `_CODE(Deduction Developer DF=CONTEXT)` from the live target template; use `_Display` only after unique target lookup resolution of display text |
| HDL value-definition child | CalculationValueDefinition and EnterableCalculationValue must share the resolved card/component user keys and exact ValueDefinitionName; Value1 must be the validated stored value |
| HDL enterable-value dates | CalculationValueDefinition starts on the parent component start or requested override date when later. EnterableCalculationValue starts on the parent definition start or requested update date when later; both must remain within parent intervals |
| HDL enterable null | Use -999999999 only for an explicit null under the current organization-card HDL contract; blank, missing, or unresolved input is not null |
| HDL date format | Use `YYYY/MM/DD` in DAT rows after validating the request date against the target card interval |
| HDL creation defaults | Preserve explicit user values. For omitted new-row fields, apply CardSequence 1 when free, the unique target component sequence or 1 when free, runtime system date to EffectiveStartDate, and the parent-bounded end date |
| HDL parent-key propagation | CardComponent, ComponentDetail, CalculationValueDefinition, and EnterableCalculationValue must use the final parent CardSequence and ComponentSequence. Existing parent values are authoritative |
| HDL component-key propagation | Copy the exact resolved `DirCardCompDefName` unchanged from `CardComponent` into every applicable child user key. Keep the target `DirCardCompDefId` as read-only lookup evidence and never add a numeric ID to compensate for a name that the target cannot resolve |
| Completed HDL preview | Must contain concrete dates, sequences, names, sections, and stored values; tokens such as `<ORIGINAL_CARD_START_DATE>`, `<ORIGINAL_COMPONENT_START_DATE>`, `<CARD_SEQUENCE>`, and `<COMPONENT_SEQUENCE>` are blocking diagnostics, not valid preview output |
| HDL system-date stability | Resolve the system date once when the DAT preview is generated, emit the concrete `YYYY/MM/DD` date rather than `SYSDATE`, and reuse it through every approved downstream stage |
| Preview side effects | In-chat preview is read-only. File creation, ZIP packaging, upload, and load initiation are four separately gated stages |

## Combined Discovery Validation

| Validation | Required State | On Failure |
|---|---|---|
| PSU association contribution scope | The parent supplied a source-backed legislation code corresponding to the LDG territory; `US` corresponds to `United States` | Block the contribution and request a valid territory-to-legislation mapping |
| PSU association completeness | The legislation-scoped `OrgPayrollStatutoryUnitPVO` result is completely paged before grouping | Classify as a Fusion API/source-contract failure; do not return partial associations |
| PSU association identity | Every contributed row has nonblank `Name`, `OrganizationId`, and `LdgId`; conflicting rows do not share one `OrganizationId` | Block and preserve redacted diagnostics |
| PSU-to-LDG join | Normalize IDs to strings and require exact `LdgId = LegislativeDataGroupId`; every contributed LdgId exists in the parent's territory LDG set | Block on an orphan LdgId; do not infer by name or silently omit the owner |
| Combined result timing | The parent has complete LDG, PSU, and TRU datasets before rendering or asking for an LDG/PSU selection | Wait for all three datasets; do not render a partial mapping |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LEC.VALIDATE | decision | 2 | validate_input | valid->LEC.DEPENDENCY;invalid->LEC.DONE_BLOCKED | LEC.COLLECT | stop | After request collection |
