# Legal Reporting Unit Calculation Cards Input Validation

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
| Target tax reporting unit | Tax reporting unit business name or functional context | Block preview | Resolve the owner and internal source/LDG IDs automatically; ask for a business selection only when names remain ambiguous |
| Calculation card selection | Card display name or base name | Block card-specific edit | Resolve `dirCardId` and definition metadata automatically from owner-scoped discovery; never request a technical card ID |
| Component flexfield value list | Exact tax reporting unit, card, component business name, and effective date | Block the value list | Resolve the card and component sequence internally; when names repeat, show business intervals/current-value context for user selection before reading FLEX rows |
| Legal reporting availability search | Nonblank `Name` or `RegistrationNumber` search text containing at least one non-`%` character | Block availability POST | Provide a legal-reporting-unit name or registration-number fragment |
| Legal reporting availability response | `result.summary` and `result.items`; each candidate must have nonblank `Name` and `EstablishmentId` | Block candidate selection | Return response diagnostics and do not infer candidates from a malformed payload |
| Legislative Data Group availability search | Either a nonblank full or partial name containing at least one non-`%` character, or a source-backed territory request; `US` and `United States` map to `United States` | Block LDG availability POST | Provide a meaningful LDG name fragment or a supported exact Fusion territory value |
| Legislative Data Group availability REST contract | Runtime-routed `legislativeDataGroups/action/findByAdvancedSearchQuery` path, POST, JSON body, `limit="500"`, `searchFields=["Name"]`, the five documented display fields, and `offset=0`; name mode requires a nonblank query plus `filters=[]`, while US territory mode requires `query=""` plus the exact `TerritoryShortName=United States` filter | Block LDG availability POST | Use the exact read-only name or territory contract in `ora_rest_execution.md` and resolve the host and route in the active environment |
| Legislative Data Group availability response | `result.summary` and `result.items`; each candidate must have nonblank `Name` and `LegislativeDataGroupId`, plus matching `TerritoryShortName` for territory mode | Block LDG candidate handling | Preserve redacted diagnostics and do not infer candidates from a malformed or filter-violating payload |
| Effective-dated context | Effective date when required by the approved source contract | Block effective-dated edit | Provide the effective date in the approved format |
| FSM or CSV operation | Task-specific export/import action contract and source rows | Block export/import execution | Obtain the approved task-specific contract; current source only proves catalog support |
| HDL card or component preview | Target tax reporting unit and LDG names, requested business path/value/effective date, complete object-level existence state, confirmed per-object create/update/correction decision, resolved parent keys, and live `CalculationCard` template metadata | Block DAT preview | Search complete current/future/history state, resolve technical keys internally, obtain Update/Correction confirmation for existing data, apply defaults only to absent leaf rows, and validate against the live template |
| Card details request | Owner, LDG, card business name, effective date, and expand value; `dirCardId` is an internal resolver output | Block card drilldown | Run owner-scoped mode=G discovery without `dirCardId`, retain the unique returned ID internally, then use the required expand value |
| Create-card list request | sourceId, sourceType=TRU, effectiveDate, mode=ADD, and expand=Cards | Block card create selection | Resolve the owner first, then retrieve available cards without dirCardId |
| Add-card template request | sourceId, sourceType=TRU, legislativeDataGroupId, effectiveDate, cardBaseName, mode=ADD, isGlobalPage=true, expand=Cards,Components,Overrides,Associations, and component override group names | Block add preview | Build the request from launch/card context and selected card base name |
| Card-level end date | Exact TRU, LDG, card user keys, current effective interval, and target-supported HDL end-date action | Block DAT preview | Retrieve the card-level target and block if live HDL metadata does not prove the action |
| Association change | Exact parent card/component keys, selected association identity, effective interval, and target-supported HDL section/action | Block DAT preview | Use read-only association metadata as evidence and map only to live target HDL; never construct a REST association payload |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Catalog task code and task name match the nested task manifest | Satisfied | Keep task scope local to this nested skill |
| ExportImportSupportedFlag and CSVExportImportSupportedFlag are Y | Satisfied | Allow task-specific FSM or CSV routing after source contract validation |
| ESTABLISHMENT_ID resolves through OrgTaxReportingUnitPVO to OrganizationId and LdgId | Satisfied | Use OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=TRU |
| Tax reporting unit cannot be resolved uniquely | Blocked | Show the matching TRU/legal-reporting-unit business names and LDG names and require a functional selection; keep identifiers internal |
| Calculation card or component fields are not covered by the parity-backed contract | Blocked | Mark the field mapping as TBD and stop before preview |
| getCardDetails returns sourceType other than TRU | Blocked | Do not reuse the Legal Entity lookup or HDL mapping scope for this target |
| Create-card list request does not include dirCardId | Satisfied | Continue because dirCardId is not available before card creation |
| Owner-scoped discovery returns one exact existing card or child business key | Existing data found | Resolve its technical keys internally, retrieve complete effective history, notify the user, and request Update/Correction confirmation before DAT preview |
| Owner-scoped discovery returns zero exact business-key rows with a complete current/future/history response | Satisfied for create at that object level | State that no existing matching row was found and create only the missing object under resolved parents |
| Existing-state discovery fails, is incomplete, single-date-only, unauthorized, or ambiguous | Blocked | Do not infer create; repair the read-only lookup or ask for a business discriminator, never a technical ID |
| getCardDetails returns no components for a component-specific operation | Blocked | Ask for a valid card/component selection |
| Component flexfield value lookup matches multiple component rows | Blocked | Show component business names/effective intervals and ask for a functional selection; retain component sequence internally and do not combine instances |
| Selected component has no `overrideType=FLEX` rows | Satisfied | Return `Flexfield values:` followed by `None` |
| Current LOV value has no unique display meaning | Satisfied for the read-only value list | Return the stored value without guessing; require unique LOV validation only if the value will be written later |
| A LOV lookup returns count other than one for a required exact value | Blocked | Return the lookup source and require a unique value |
| Override field is not returned by the selected card/component metadata | Blocked | Do not reuse fields from another card; ask for a valid field from the card schema |
| Override LOV dataSource has unresolved parent binds | Blocked | Resolve parent override values or context fields first |
| Dependent override graph has a cycle or unknown parent | Blocked | Stop and request source evidence or a corrected selection |
| Required context override is not user-supplied but has a current/default metadata value | Satisfied | Auto-carry it into the HDL preview and applicable child row |
| Card-level end date is requested but only component-level END_DATE is source-confirmed | Blocked | Ask for source evidence or use the component end-date operation |
| Association identity or association end-date mode is missing | Blocked | Resolve the association from getCardDetails or request an approved source contract |
| Legal reporting availability returns multiple rows | Satisfied for a list-only request; blocked only for downstream card work | Return the names-only list and finish when only a list was requested. If card work was also requested, wait for the user to select one |
| Legislative Data Group availability returns one or more rows | Satisfied for a list-only request; blocked only for downstream card work when multiple LDGs have no user selection | Return every name in response order and finish when only a list was requested; otherwise wait for one selected LDG |
| Legislative Data Group availability response is paged | Incomplete until `hasMore=false` | Continue with the next offset, preserve the same query, fields, and filters, and deduplicate by LegislativeDataGroupId |
| US territory availability returns a row whose `TerritoryShortName` is not `United States` | Blocked as a response-contract failure | Preserve redacted diagnostics and do not return or use the mismatched row |
| Selected legal reporting unit has `TruStatus` other than `A` | Blocked for TRU card work | Report the returned status and require an active TRU selection before continuing |
| Any read-only lookup contract, HDL action, target-template field, or defaulting rule is missing | Blocked | Request source evidence before DAT preview or loader handoff |
| HDL creation omits CardSequence, ComponentSequence, EffectiveStartDate, or EffectiveEndDate | Satisfied after documented defaulting | Use new-card CardSequence 1, new-component ComponentSequence 1, the runtime system date resolved once for the preview, and 4712/12/31 respectively |
| An HDL sequence default conflicts or a defaulted child date falls outside the parent card interval | Blocked | Resolve the lowest positive unused sequence from the complete target set and keep it internal; if the date is invalid, ask for a valid business effective date. Block with an internal resolver diagnostic if sequence completeness cannot be proven |

## Field Validation

| Check | What Happens |
|---|---|
| Task code | Must remain PAY_MANAGE_LEGAL_REPORTING_UNIT_DEDUCTION_RECORDS |
| Task name | Must remain Legal Reporting Unit Calculation Cards |
| Target organization type | Must be tax reporting unit unless an approved source expands the scope |
| Source type | Must be TRU for the Legal Reporting Unit Calculation Cards flow confirmed by the user |
| Availability user output | For one or more matches, show only `Legal Reporting Unit names:` and each returned `Name`, one name per line in response order. Keep IDs, registration data, parent organizations, flags, statuses, dates, counts, offsets, and pagination internal unless explicitly requested |
| Legal reporting unit launch source resolution | ESTABLISHMENT_ID must resolve through the single serialized OrgTaxReportingUnitPVO finder using AdditionalViewCriteria=findByEstablishmentId when sourceId and LDG are not already supplied |
| Read-only state | readOnlyFlag must be N before preparing an HDL edit, end-date, or delete; this flag never authorizes REST mutation |
| Add-card mode | mode must be ADD and expand must be Cards,Components,Overrides,Associations |
| Create-card list mode | mode must be ADD and expand must be Cards |
| Drilldown mode | mode must be G, showEmptyComponent must be N, and expand must be Cards,Components,Overrides,CompAssociation |
| Dynamic override schema | Override fields must be discovered from getCardDetails for the selected card/component and effective date |
| HDL creation defaults | Preserve explicit user values. For omitted fields, apply CardSequence 1 to a new card, ComponentSequence 1 to a new component, runtime system date to EffectiveStartDate, and 4712/12/31 to EffectiveEndDate |
| HDL parent-key propagation | CardComponent and ComponentDetail must use the final parent CardSequence; ComponentDetail must use the final ComponentSequence. Existing parent values are authoritative |
| HDL system-date stability | Resolve the system date once when the DAT preview is generated, emit the concrete `YYYY/MM/DD` date rather than `SYSDATE`, and reuse it through every approved downstream stage |
| Component flexfield value output | Keep only the exact component's `overrideType=FLEX` rows and return `Flexfield values:` plus one `Name: Value` line per row in response order. Prefer `title`, otherwise `name`; render null or empty as `Blank`. Do not display IDs, codes, categories, flags, dataSource, pagination, or component metadata by default |
| Current values versus allowed values | A request for flexfield values returns current/default values only. Retrieve LOV option rows only when the user asks for allowed or available values |
| HDL override mapping | Each requested value must use the selected card's override metadata and dispatch by `overrideType` to the applicable HDL child section |
| Auto-carried required context | Required or populated FLEX context overrides may be included even when not changed by the user; user-changed values win by name and context |
| End-date component | The live target template must prove the HDL end-date action and complete component user key; runtime IDs remain read-only evidence |
| Card-level end date | The live target template must prove a card-level HDL end-date action and complete card user key |
| Component Correct or Update | Must be user-confirmed after existing-data disclosure and must preserve componentSequence, internal dirCardCompId evidence, effectiveStartDate, overrideBaseGroupName, overrides, and association context from getCardDetails |
| Component Delete History | Must use a target-supported HDL delete-history action, selected history user key, irreversible approval, and no automatic retry |
| Add association | associations[] must be populated only from active card association metadata and source-confirmed user changes |
| Override metadata | Override metadata from getCardDetails defines code, name, title, category, overrideType, controlType, type, nullable, contextRequired, display, dataSource, current value, and userOverridden |
| LOV-backed overrides | Values must resolve through the override dataSource, typically payrollGenericLOV with PayValueSetVO when the response declares a value set |
| Dependent LOV | Parent override, LDG, legislation, effective date, or component context binds must be resolved before child LOV validation |
| Non-LOV override | Validate by metadata type, nullability, format, and unit of measure when returned |
| CSV rows | Must match the approved task-specific CSV shape before import |
| Route contract | REST is retrieval-only; every calculation-card create, update, correction, end-date, or delete must use target-supported HDL through `core.data-loader` |
| Legal reporting search query | Trim leading and trailing whitespace, preserve underscores and explicit `%` wildcards, and otherwise send the user's text unchanged as `query` |
| Legal reporting pagination | Parse string or numeric `count`, `limit`, and `offset`; follow `hasMore=true` without changing the query and deduplicate candidates by `EstablishmentId` while preserving response order |

## Combined Discovery Validation

| Validation | Required State | On Failure |
|---|---|---|
| TRU association contribution scope | The parent supplied a source-backed legislation code corresponding to the LDG territory; `US` corresponds to `United States` | Block the contribution and request a valid territory-to-legislation mapping |
| TRU association completeness | The legislation-scoped `OrgTaxReportingUnitPVO` result is completely paged before grouping | Classify as a Fusion API/source-contract failure; do not return partial associations |
| TRU association finder schema | `OrgTaxReportingUnitPVO` uses exactly `DisplayAttributes=PsuId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId`; `LegalEntityId` is not requested | Block the finder before execution and use the source-confirmed PsuId attribute |
| TRU association identity | Every contributed row has nonblank `Name`, `OrganizationId`, and `LdgId`; conflicting rows do not share one `OrganizationId`; retain returned `PsuId` as parent-PSU context | Block and preserve redacted diagnostics |
| TRU-to-LDG and PSU validation | Normalize IDs to strings, require exact `LdgId = LegislativeDataGroupId`, and when PsuId is nonblank require `TRU.PsuId = PSU.OrganizationId` within that LDG | Block on an orphan LdgId or mismatched parent PSU; do not infer by name or silently omit the owner |
| Combined result timing | The parent has complete LDG, PSU, and TRU datasets before rendering or asking for a selection | Wait for all three datasets; do not render a partial mapping |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUC.VALIDATE | decision | 2 | validate_input | valid->LRUC.DEPENDENCY;invalid->LRUC.DONE_BLOCKED | LRUC.COLLECT | stop | After request collection |
