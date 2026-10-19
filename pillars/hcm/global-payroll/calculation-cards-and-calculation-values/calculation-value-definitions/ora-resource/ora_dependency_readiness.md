# Calculation Value Definitions Dependency Readiness

## Route Dependency Boundary

Resolve dependencies only for reads and the released native HDL profiles. An
unavailable registered-BO child write cannot become ready through lookup,
registration, metadata, or target resolution. Return
`CVD_HDL_ROUTE_FROZEN` before archive authoring, approval, or dispatch.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Operation and target | Classify the requested operation and bind it to one environment alias without storing credentials. |
| 2 | Effective and legislative scope | Resolve effectiveAsOfDate, one LDG, and its LegislationCode. |
| 3 | Calculation semantics | For standalone CVD-HDL04 parent create, obtain current-operation user selections for one calculation type and one existing value definition group. Use the exact Calculation Type plus current field-state evidence to determine whether Unit of Measure is applicable; only then collect and resolve an exact UOM selection and finalize parentPayloadShape. Every exact current tenant type/unit value is eligible, including customer-defined labels and non-Money units. For CVD-HDL10, retain exact Flat Amount (F) with Money (M). For CVD-HDL11, derive the existing parent's exact Calculation Type and applicable Unit of Measure and revalidate them against the current scoped tenant lookups. |
| 4 | Route support | Continue to normal execution only for the ten released native HDL profiles. CVD-HDL04 non-baseline field shapes are live-metadata-gated QA candidates; they are not represented as separately runtime-proven operations. Registered-BO child creation is unavailable; historical evidence is non-authorizing. Every unsupported mutation remains CVD_HDL_ROUTE_FROZEN. |
| 5 | Target or duplicate state | For parent create and combined create, require zero exact parent matches. For CVD-HDL05 Range Item Create, require one exact parent, zero existing Range Items, and zero children with the proposed lower bound. For CVD-HDL11 Range Item Override Create, require one exact nonproduction parent, exactly one existing baseline Range Item, zero other child families, zero Range Items with the proposed lower bound, and no overlap when the resolved bound type is comparable. For Parent Correct or Update, require one explicitly selected CVD-HDL07S target whose current exact expanded read proves the released profile; Update also requires no existing future slice and a later new boundary. For Parent Delete, require zero children and complete timeline evidence proving exactly one physical slice. For Range Item Correct, Update, or Delete, first resolve the parent, then select one item by From value and item start date; Update requires a later boundary, and Delete requires the sole open-ended Range Item plus zero other children. |
| 6 | Native HDL metadata | Refresh the ValueDefinition/RangeItem hierarchy and the separate RangeItemOverride root, their attributes, and the relevant UCM ValueDefinition.dat or RangeItemOverride.dat template through core.data-loader. |
| 7 | Deterministic archive | Build the exact operation profile: one parent MERGE, one parent plus one same-start child MERGE, one RangeItem child MERGE, one independent-root RangeItemOverride MERGE, one currency-only in-place parent MERGE, one currency-only future-slice parent MERGE, one complete-range parent DELETE, one in-place Range Item MERGE, one future-slice Range Item MERGE, or one complete-range Range Item DELETE. Validate the ZIP without uploading it. |
| 8 | Immutable preview and confirmation | Fingerprint the exact ZIP and obtain confirmation through the separate governed lifecycle. |

## Create Command Isolation

- Every `create_parent`, `create_range_item`, `create_range_item_override`,
  `create_allowed_override`, or `create_override_usage` command allocates a new operation ID and starts in
  `collecting` with empty operation-local business state.
- A Create command is never interpreted as resume, retry, clone, or continuation
  of a previous run, even when its target or requested values resemble an
  earlier operation.
- No prior input, resolved ID, LOV selection, lookup result, derived default,
  child draft, payload, archive, fingerprint, approval, or receipt is valid as
  a value in the new operation. Current-request values must be resolved again,
  and defaults must be recalculated in the new operation.
- A child Create command is still isolated. CVD-HDL05 may prepare one Range
  Item only after a fresh exact parent read, zero-child baseline, duplicate
  check, and current live native template proof. It never inherits cached
  parent or child keys.
- A Range Item Override Create is also isolated. CVD-HDL11 may prepare one
  independent-root row only after a fresh exact parent read proves the strict
  one-baseline-Range-Item profile, zero other child families, no matching lower
  bound, and the current live `RangeItemOverride` template.
- A combined Create command is also isolated. CVD-HDL10 resolves every parent
  choice again, derives the one child start from the new parent start, and
  requires a fresh zero-parent duplicate result before authoring.
- Resume and reconciliation retain an existing operation ID only when the user
  explicitly requests resume or reconciliation and identifies that operation.
  A new Create command is not sufficient authorization to resume it.
- A prior receipt may be consulted only for collision detection or required
  reconciliation. It cannot seed business values in the new operation.
- Static repository contracts, configured environment/session references, and
  task schema are reusable infrastructure, not prior-run create values, and
  remain subject to their existing freshness checks.

## Validation Guidance Discovery Compatibility

- The required CVD guidance source is the task-owned `ora-resource/` directory.
- If the shared setup-data validation context resolves this task correctly but
  reports no guidance files and requests Oracle-documentation fallback, inspect
  `ora-resource/ora_*.md` and `ora-resource/ora-*.md` directly.
- Read the canonical Markdown sources selected by the official planner's task
  nodes and source anchors, and use `ora_rule_registry.json` only as their
  generated execution index. When they are present and readable, classify the
  helper result as a nonblocking discovery mismatch and continue validation
  using those task-owned sources.
- Do not ask the user to waive the discovery mismatch. A waiver cannot replace
  a missing required task contract and is unnecessary when the contracts are
  present.
- Block only for unresolved or mismatched task metadata, or a missing or
  unreadable required task-owned guidance file. All substantive validation,
  archive, Task Hook, approval, upload, and initiation gates remain unchanged.

## Dependency Rules

Rows for unsupported child families and lifecycle shapes preserve only the
read dependencies useful for future native HDL investigation. Historical REST
headers, registered-BO controls, opaque keys, and effective-range syntax never
become native HDL DAT controls.

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CVD-DEP-001 | Target environment alias | Yes | Always | Configuration required | FDOS environment/session configuration | | Prevents cross-environment reads and writes | Select the intended configured environment; never paste credentials | environmentAlias |
| CVD-DEP-002 | Legislative Data Group | Yes | Always | Lookup required | LegislativeDataGroupLOV | find_legislative_data_group | Defines data security, legislation, country, and dependent LOV scope | Select one exact LDG from returned matches | LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode |
| CVD-DEP-003 | Effective as-of date | Yes | Always | Input required | User input or task default | | Controls date-effective reads, links, and mutation boundaries | Confirm the date before any mutation preview | effectiveAsOfDate |
| CVD-DEP-004 | Calculation type | Yes | create_parent, create_parent_with_range_item, or create_range_item_override | Current-operation user selection required for a new parent; fresh-parent lookup validation required for CVD-HDL11 | Current request or current-run user selection, or the CVD-HDL11 parent receipt, validated by CalculationTypeVO | find_calculation_type | Determines parent fields and calculation-value result-slot shape | For CVD-HDL04, present the scoped choices and require selection; accept every exact current Fusion LOV row, including customer-defined labels, then resolve parentPayloadShape. For CVD-HDL10, only Flat Amount (F) is released because its ordinary Range Item remains narrow. For CVD-HDL11, use the exact type on the freshly resolved parent and accept every exact current Fusion LOV row. A missing packaged semantic-map entry must not reject CVD-HDL04 or CVD-HDL11. | CalculationTypeId, CalculationTypeCode when returned, CalculationTypeName, calculationTypeResolution, parentPayloadShape for CVD-HDL04, resultSlotShape for CVD-HDL11 |
| CVD-DEP-005 | Existing value definition group | Yes | create_parent or create_parent_with_range_item | Current-operation user selection required | Current request or current-run user selection validated by payrollValueDefinitionGroups | find_value_definition_group | Parent create requires one existing group | If omitted, present the small scoped set or searchable bounded pages and require selection; this task does not create a group | ValueGroupId, ValueGroupName |
| CVD-DEP-006 | Active parent definition | Yes | read, CVD-HDL04 reconciliation, CVD-HDL05 Range Item create, CVD-HDL11 Range Item Override create, CVD-HDL09S Range Item target selection, CVD-HDL07A Parent Correct, CVD-HDL07B Parent Update, CVD-HDL07C Parent Delete, or read-only lifecycle classification | Lookup required | payrollCalculationValueDefinitions GET | find_parent_definition | Provides logical identity, physical effective range, calculation type, links, child inventory, conditional parent-field read-back, and the business-key labels used by native HDL or the registered-BO adapter | Select exactly one result by business name in the requested LDG and date; never ask for or display its ID | ValueDefnId, parentItemKey, selfLink, ValueDefinitionName, LegislativeDataGroupName, ValueGroupName, CalculationTypeId, CalculationTypeName, Type, UnitOfMeasure, CurrencyCode, DateMode, Periodicity, DatabaseItemId, DBItemBaseUserName, ValueIdentifier, EffectiveStartDate, EffectiveEndDate, childCollectionLinks, childCounts |
| CVD-DEP-007 | Calculation value definition reference | Conditional | create_range_item for GC, RDB, or FP, or create_range_item_override when the resolved result-slot shape requires a referenced definition | Lookup required | CalculationValueDefinitionLOVVO | find_calculation_value_definition | Some calculation types store a referenced definition as a result input | Select an exact definition other than the current parent; retain its ID internally when the live result slot requires it | ReferencedValueDefnId, ReferencedValueDefnName |
| CVD-DEP-008 | Override type | Yes | create_allowed_override | Lookup required | OverrideTypeLOVVO | find_override_type | Determines enterable value type and stored OverrideType code | Select one exact eligible type for the parent calculation type | OverrideType, OverrideTypeMeaning |
| CVD-DEP-009 | Allowed override row | Yes | read-only Allowed Override or Override Usage inspection | Persisted row required | Active parent's AllowedOverrides collection | find_allowed_override | Supplies the allowed-override item and nested OverrideUsages routes; create also requires its ID in the body | Select one persisted allowed override by business prompt and type; inject the resolved ID without exposing it as user input | AllowOverridesId, allowedOverrideItemKey, allowedOverrideSelfLink, overrideUsagesCollectionLink |
| CVD-DEP-010 | Calculation card | Yes | create_override_usage | Lookup required | CalculationCardLOVVO | find_calculation_card | Scopes the component lookup but is not posted in the usage body | Select one exact card | DirCardDefinitionId, CalculationCardName |
| CVD-DEP-011 | Calculation component and LDG create context | Yes | create_override_usage | Lookup required | CalculationComponentLOVVO plus selected LDG receipt | find_calculation_component | DirCardCompDefId is persisted by the usage row; the POST also requires the operation's LegislativeDataGroupId | Select a component returned for the selected card and inject both resolved IDs internally | DirCardCompDefId, CalculationComponentName, LegislativeDataGroupId |
| CVD-DEP-012 | Table value set | Conditional | create_override_usage, or create_range_item_override when its live-resolved result shape requires ValueSetName | Optional lookup for Override Usage; lookup required when the CVD-HDL11 result shape requires the set name | TableValueSetLOVVO | find_table_value_set | A value-set-backed result must use one exact tenant-valid value set | Select one exact eligible value set. ValueSetValue is not validated by this resolver; if a result shape requires it and no separate declared resolver proves the exact member, keep that shape unresolved. | ValueSetCode, ValueSetMeaning, ValueSetId, ValueDataType |
| CVD-DEP-013 | Database item | Conditional | CVD-HDL04 create_parent when parentPayloadShape requires a database item | Current-operation user selection and lookup required | RangeDatabaseItemLOVVO | find_database_item | Flat Amount Multiplier requires one exact scoped database item | Select by business name; retain DatabaseItemId internally and author only DatabaseItemName in native HDL | DatabaseItemId, DatabaseItemName |
| CVD-DEP-014 | Fresh self link | Conditional | Read-only lifecycle classification or reconciliation | Current link required | Exact effective-as-of parent or child GET | extract_active_resource_links | Opaque keys vary by date and hierarchy and must not be reconstructed | Retain it internally for GET navigation and evidence only | selfLink, parentItemKey, childItemKey, retrievedAt |
| CVD-DEP-015 | Mutation confirmation | Yes | Any released native HDL profile, including CVD-HDL09D Range Item Delete | Confirmation required | Immutable native HDL ZIP; lifecycle operations also bind the selected target fingerprint | | Prevents guessed, stale, or repeated uploads | Confirm the business-facing effect and exact archive SHA-256 without exposing technical target identifiers | archiveSha256, confirmedSha256, confirmedAt, targetFingerprint when applicable |
| CVD-DEP-016 | Delete-safe parent shape | Yes | CVD-HDL07C delete_parent | Childless single-slice parent required | Exact expanded parent GET plus complete physical timeline evidence | find_parent_definition | Native HDL Delete is proved only for a parent with zero children and exactly one physical slice | Select the target by business labels and explain any failed eligibility condition; never request IDs | childCounts, physicalSliceCount, rangeStartDate, rangeEndDate, timelineEvidenceSource |
| CVD-DEP-017 | Unit of measure | Conditional | CVD-HDL04 create_parent when preliminaryParentFieldState makes UOM applicable, verified Flat Amount create_parent_with_range_item, or CVD-HDL11 when the existing parent has a UnitOfMeasure | Current-operation user selection required for a new parent after preliminary field-state resolution; fresh-parent lookup validation required for CVD-HDL11 | Current request or current-run user selection, or the CVD-HDL11 parent receipt, validated by PAY_UNITS | find_unit_of_measure_code | Unit semantics must be exact for the active operation | For CVD-HDL04, first determine UOM applicability from the exact Calculation Type and current field-state evidence; then present the scoped PAY_UNITS choices and accept any exact applicable current lookup match, including non-Money values. CVD-HDL10 remains Money (M) only. For CVD-HDL11, validate and retain the exact existing-parent value and do not author Uom in the RangeItemOverride row. | UnitOfMeasure, UnitOfMeasureMeaning |
| CVD-DEP-018 | Unreleased child slice | Conditional | Read-only inspection of Allowed Overrides, Override Usages, Value Usages, Related Elements, or a Range Item Override lifecycle action outside CVD-HDL11 Create | Current item required | Expanded parent read, nested collection read, or exact Override Usage finder | extract_active_resource_links | Identity and effective ranges remain useful as read-only evidence; they do not establish a broader child-write route | Retain only as read evidence and never ask the user for IDs | childType, childBusinessLabel, childId, effectiveStartDate, effectiveEndDate, childSelfLink |
| CVD-DEP-019 | Native HDL operation proof | Yes | Any mutation outside CVD-HDL04, CVD-HDL10, CVD-HDL05, CVD-HDL11, CVD-HDL09A, CVD-HDL09B, CVD-HDL09D, CVD-HDL07A, CVD-HDL07B, or CVD-HDL07C | Runtime proof required | The operation allowlist and exact DAT rules in ora_design_enforcement.md | | Historical product REST or registered-BO evidence does not prove a native HDL operation or broader field shape | Classify the request as CVD_HDL_ROUTE_FROZEN and stop before archive authoring or approval | executionProfile, requiredEvidence |
| CVD-DEP-026 | Native HDL Range Item Correct target and schema | Yes | CVD-HDL09A correct_range_item | Current target receipt and runtime-proven contract required | CVD-HDL09S selection after CVD-DEP-006 resolves the parent, fresh expanded parent GET, live ValueDefinition and RangeItem schema, archive validation, and Task Hook validation | find_range_item | Proves one open-ended selected Range Item, unchanged dates and bounds, and the exact Flat Amount-only child MERGE | Select the target and enter the corrected Flat Amount by business values only | operationId, targetFingerprint, parentName, LDG, itemStartDate, lowValue, highValue, currentValue1, correctedValue1 |
| CVD-DEP-027 | Native HDL Range Item Update target and schema | Yes | CVD-HDL09B update_range_item | Current target receipt and runtime-proven contract required | CVD-HDL09S selection after CVD-DEP-006 resolves the parent, fresh expanded parent GET, live ValueDefinition and RangeItem schema, archive validation, and Task Hook validation | find_range_item | Proves one open-ended selected Flat Amount Range Item, a later update boundary, unchanged bounds, and a changed amount | Select the target and enter the update date and updated Flat Amount by business values only | operationId, targetFingerprint, parentName, LDG, itemStartDate, updateStartDate, lowValue, highValue, currentValue1, updatedValue1 |
| CVD-DEP-028 | Native HDL Range Item Delete target and schema | Yes | CVD-HDL09D delete_range_item | Current target receipt and runtime-proven contract required | CVD-HDL09S selection after CVD-DEP-006 resolves the parent, fresh expanded parent GET, live ValueDefinition and RangeItem schema, archive validation, and Task Hook validation | find_range_item | Proves the selected item is the sole open-ended Flat Amount Range Item and the parent has no other children | Select the target by business values only; never ask for IDs or mutation fields | operationId, targetFingerprint, parentName, LDG, itemStartDate, itemEndDate, lowValue, highValue, currentValue1, childCounts |
| CVD-DEP-020 | Registered-BO child lifecycle | Yes | Any Allowed Override or Override Usage lifecycle request | Registered-BO child creation is unavailable | Stable registered-BO evidence reference | | Container deletion and nested cascade behavior are not executable task dependencies | Return CVD_HDL_ROUTE_FROZEN before lookup, archive authoring, approval, or dispatch | |
| CVD-DEP-021 | Registered-BO child operation | Yes | create_allowed_override or create_override_usage | Registered-BO child creation is unavailable | Stable registered-BO evidence reference | | Registration and historical product REST observations do not establish an execution contract | Return CVD_HDL_ROUTE_FROZEN; no candidate, proof, approval, or dispatch path is available | |
| CVD-DEP-033 | Native HDL standalone parent schema and payload shape | Yes | create_parent | Live metadata and template required, with a completely resolved field shape and readable reconciliation map | core/data-loader business-object metadata and template reads, the exact CalculationTypeVO row, current create-field semantics, the exact PAY_UNITS row only when preliminary field-state evidence makes UOM applicable, and declared field resolvers | resolve_parent_payload_shape | Prevents stale, wrong, circular, or guessed CVD-HDL04 DAT construction | Resolve preliminary field state from the exact Calculation Type; collect UOM only when applicable; then finalize required, optional, and forbidden fields plus a read-back mapping for every authored conditional field | businessObject, topDiscriminator, datFilename, validatedSections, schemaFingerprint, preliminaryParentFieldState, parentPayloadShape, authoredParentFields, parentReadbackMappings |
| CVD-DEP-034 | Native HDL combined parent schema | Yes | create_parent_with_range_item | Live metadata and template required for the fixed Flat Amount/Money parent and ordinary Range Item child | core/data-loader business-object metadata and template reads | | Prevents generalized CVD-HDL04 fields from leaking into CVD-HDL10 | Retain the exact fixed CVD-HDL10 parent and child fields | businessObject, topDiscriminator, datFilename, validatedSections, schemaFingerprint |
| CVD-DEP-022 | Native HDL Range Item schema and baseline | Yes | CVD-HDL05 create_range_item | Controlled live proof required | core.data-loader schema GET plus exact expanded parent GET | find_parent_definition | Proves the native child section, parent business key, date range, zero-child baseline, and proposed lower-bound uniqueness | Supply only Effective Start Date, From, To, and Flat Amount after selecting the parent | validatedSections, validatedFields, parentEffectiveRange, baselineChildCounts, matchingRangeCount |
| CVD-DEP-031 | Native HDL Range Item Override schema, result shape, and baseline | Yes | CVD-HDL11 create_range_item_override | Runtime-proven root contract plus current live tenant proof required | core.data-loader schema/template GET, exact expanded parent GET, current calculation-type and applicable-unit lookups, and type-specific reference lookups when required | find_parent_definition | Proves the independent root, parent business key, effective range, exact tenant-valid type and unit, required result field signature, a readable reconciliation mapping for every authored result field, exactly one baseline Range Item, zero other child families, proposed lower-bound uniqueness, and type-appropriate overlap safety | Supply Effective Start Date, From, To, and every result value required by the live-resolved shape after selecting the parent. A delivered or customer-defined type or non-Money unit is not itself a blocker. | validatedSections, validatedFields, parentEffectiveRange, CalculationTypeName, UnitOfMeasure, resultSlotShape, authoredResultFields, resultReadbackMappings, baselineChildCounts, matchingRangeCount, overlappingRangeCount, schemaFingerprint |
| CVD-DEP-032 | Rate definition result reference | Conditional | create_range_item_override when the live-resolved result shape requires a rate definition | Lookup required | RateDefinitionLOVVO | find_rate_definition | A rate-definition-backed result must resolve in the same LDG, legislation, and effective context | Select one exact rate definition by business name; retain any returned identifier internally and place it only in the live-template result slot that requires it | RateDefinitionId, RateDefinitionName |
| CVD-DEP-023 | Native HDL Parent Correct target and schema | Yes | CVD-HDL07A correct_parent | Current target receipt and controlled contract required | CVD-HDL07S selection, exact expanded parent GET, live ValueDefinition schema, and Task Hook validation | find_parent_definition | Proves one selected childless open-ended Flat Amount/Money parent and the exact currency-only MERGE shape | Select the parent by business labels only; never ask for or expose IDs | operationId, targetFingerprint, ValueDefinitionName, LegislativeDataGroupName, ValueGroupName, CalculationTypeName, UnitOfMeasure, currentCurrencyCode, parentEffectiveRange, childCounts, schemaFingerprint |
| CVD-DEP-029 | Native HDL Parent Correct currency change | Yes | CVD-HDL07A correct_parent | Current and corrected Currency must resolve exactly and differ | Selected parent CurrencyCode plus current Currency LOV evidence | find_currency | Proves both currency values are valid and the correction is not a no-op | Select the corrected Currency by business code or name | currentCurrencyCode, correctedCurrencyCode |
| CVD-DEP-024 | Native HDL Parent Update target, boundary, and schema | Yes | CVD-HDL07B update_parent | Current target receipt and controlled contract required | CVD-HDL07S selection, exact expanded parent GET, complete timeline/future-slice check, live ValueDefinition schema, and Task Hook validation | find_parent_definition | Proves one selected childless open-ended Flat Amount/Money parent, no existing future slice, a later new boundary, and the exact currency-only new-slice MERGE shape | Select the parent by business labels and enter the new boundary as an ISO date; never ask for or expose IDs | operationId, targetFingerprint, ValueDefinitionName, LegislativeDataGroupName, ValueGroupName, CalculationTypeName, UnitOfMeasure, currentCurrencyCode, baselineEffectiveStartDate, effectiveStartDate, parentEffectiveRange, childCounts, schemaFingerprint |
| CVD-DEP-030 | Native HDL Parent Update currency change | Yes | CVD-HDL07B update_parent | Current and new Currency must resolve exactly and differ | Selected parent CurrencyCode plus current Currency LOV evidence | find_currency | Proves both currency values are valid and the update is not a no-op | Select the new Currency by business code or name | currentCurrencyCode, newCurrencyCode |
| CVD-DEP-025 | Native HDL Parent Delete target, timeline, and schema | Yes | CVD-HDL07C delete_parent | Current target receipt and runtime-proven contract required | CVD-HDL07S selection, exact expanded parent GET, complete one-slice timeline evidence, live ValueDefinition schema, and Task Hook validation | find_parent_definition | Proves one explicitly selected childless parent, its complete physical range, and the exact one-row DELETE shape | Select the parent by business labels only; never ask for IDs or mutation fields | operationId, targetFingerprint, ValueDefinitionName, LegislativeDataGroupName, parentEffectiveRange, childCounts, physicalSliceCount, timelineEvidenceSource, schemaFingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| READY | All mandatory dependencies are exact, current, and source-backed | Yes for reads or one exact released native HDL profile, including CVD-HDL11 Range Item Override Create and CVD-HDL09D Range Item Delete |
| NEEDS_INPUT | A user-owned required field or current-operation semantic selection is missing | Read-only choice lookup only; present the complete choices and request a selection |
| NOT_FOUND | An exact scoped lookup returns zero rows | No; report the field and supplied value |
| AMBIGUOUS | A lookup returns multiple plausible rows | No; present concise choices and require selection |
| STALE | A cached key, link, lookup, or preview no longer matches the active scope | Read-only refresh only |
| HDL_PROOF_UNAVAILABLE | The requested native HDL section or operation lacks runtime DAT/load/read-back proof | No; return CVD_HDL_ROUTE_FROZEN before archive authoring, approval, or write |
| PAYLOAD_SHAPE_UNRESOLVED | An exact tenant-valid CVD-HDL04 Calculation Type or applicable Unit of Measure resolved, but the required/optional/forbidden parent fields or a readable mapping for an authored conditional field cannot be established from current evidence | Read-only lookup and metadata refresh only; keep the valid selection and stop before DAT authoring without calling it invalid |
| REGISTERED_BO_PROOF_UNAVAILABLE | Allowed Override or Override Usage child creation is terminally unavailable in this task | No; return CVD_HDL_ROUTE_FROZEN before lookup, archive authoring, approval, or dispatch. |
| UNSUPPORTED | The requested capability is outside the shipped task allowlist | No; return the blocking contract rule |
| READY_FOR_CONFIRMATION | All validation, lookup, defaulting, and enforcement checks passed and an immutable mutation plan exists | No write here; hand off to the governed lifecycle |

## Parent Create Selection Provenance

- Value Definition Group, Calculation Type, and applicable Unit of Measure are
  user-owned choices for each new `create_parent` operation.
- Accepted provenance is either an explicit value in the current user request
  or an explicit user selection made during the current operation.
- A resolver validates a supplied selection or builds a complete choice list;
  it never supplies consent. Present a single returned candidate for selection
  just as you would a multi-row list.
- Values from prior runs, archives, project state, receipts, or
  examples may not satisfy these dependencies. They can be considered only
  after the user independently selects the same semantic value in the current
  operation and a current lookup validates it.
- While any selection is unresolved, keep the operation in `collecting` and do
  not author an archive, calculate an archive hash, request mutation approval,
  upload, initiate Data Loader, or dispatch a REST mutation.
- Once CVD-HDL04 selections resolve, allow archive work for every exact current
  tenant Calculation Type and applicable Unit of Measure whose
  `parentPayloadShape`, live-template fields, resolver lineage, and read-back
  mappings all resolve. Another exact selection is not an input error; an
  unresolved shape remains `PAYLOAD_SHAPE_UNRESOLVED` before DAT authoring.
- Keep CVD-HDL10 Flat Amount (`F`)/Money (`M`) only. Generalizing standalone
  CVD-HDL04 does not broaden the ordinary Range Item child contract.

## Invalidation Rules

| Changed Value | Invalidate |
|---|---|
| Environment alias | All session-bound data, lookups, IDs, links, previews, confirmations, and receipts not belonging to the new environment |
| LDG or LegislationCode | Calculation types, value groups, parent matches, cards, components, value sets, and the parent archive plan |
| Effective as-of date | Parent keys and links, child links, effective slices, mutation plans, and confirmations |
| Calculation type | Preliminary parent field state, applicable UOM selection, every conditional-field lookup, parentPayloadShape, authoredParentFields, parentReadbackMappings, shape-dependent defaults, DAT/archive bytes, fingerprints, approvals, and previews |
| Unit of Measure | Finalized parentPayloadShape, authoredParentFields, parentReadbackMappings, shape-dependent defaults, DAT/archive bytes, fingerprints, approvals, and previews |
| Parent definition | Every child row, child link, usage hierarchy, and mutation plan |
| Allowed override | Usage rule target and nested collection link |
| Calculation card | Calculation component and usage preview |
| Calculation component | Usage preview |
| Any authored DAT field, source plan, live native HDL metadata, or archive byte | Archive SHA-256 and confirmation |
| Parent Correct target, baseline currency, physical range, or child count | Target fingerprint, archive SHA-256, and confirmation |
| Parent Update target, baseline currency, new boundary, future-slice state, physical range, or child count | Target fingerprint, archive SHA-256, and confirmation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->CVD.RESOLVE_REFERENCES;blocked->CVD.HANDLE_ERROR | CVD.VALIDATE_INPUT | stop | Input validation succeeds |
