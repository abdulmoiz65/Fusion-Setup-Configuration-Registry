# Calculation Value Definitions Input Validation

## Scope

This resource validates Calculation Value Definition reads, the current native
HDL plans, and rejected registered-BO child requests. It does not execute
Fusion writes. Catalog-supported setup-task CSV export and import remain under
the task workflow declared in `SKILL.md`, including its shared export and
`core.data-loader` routing; a CSV request exits this native-HDL task-hook
contract and must not be converted to DAT.

## Input Route Classification

Validate the requested operation before collecting mutation-specific fields.
Within this native-HDL task-hook contract, only search, read, and the released
native HDL profiles continue to detailed input collection. Route an explicit
setup-task CSV request back to the catalog-supported workflow in `SKILL.md`.
An unavailable child write has no mutation input contract: return
`CVD_HDL_ROUTE_FROZEN` before lookup, candidate authoring, approval, or
dispatch.

## Large Choice Validation

For an omitted required business choice with more than 20 eligible values,
remain in `collecting`, ask for a business-name or business-code search term,
and present at most 20 sorted case-insensitive contains matches per page. Use a
server-side filter only when the selected resolver documents it; otherwise
complete pagination and filter locally. Never require an exact value that was
not shown, and never treat a single filtered match as a user selection.

## Input Kind and Continuation Contract

Classify every unresolved requirement before prompting. Use the corresponding
user-facing label verbatim:

| Input kind | Prompt label | Behavior |
|---|---|---|
| fusion_lov | Select from Fusion | Run the declared scoped lookup, present eligible business labels, and require an explicit selection. Apply Large Choice Validation when needed. |
| fixed_choice | Select one | Present the complete closed set of task-supported business choices. Do not run a Fusion LOV. |
| free_form | Enter a free-form value | Ask for user-authored text, a number, or a date and state its format or validation rule. Do not imply that Fusion supplies a list. |
| defaulted | No prompt unless an override is supported | Apply only a declared default and show it in the immutable preview. |
| derived_or_route_owned | No prompt | Resolve internally and never request an ID, link, semantic code, or service-controlled value from the user. |

For every supported mutation, follow the input-kind catalog and continuation
rules in this file, then resolve dependencies in
`ora_dependency_readiness.md`. All Fusion surrogate IDs are machine-only:
never request or display them in prompts, choices, approval previews, business
receipts, or conversational summaries.

Use this prompt catalog for supported operations:

| Business requirement | Input kind | Prompt detail |
|---|---|---|
| Operation, when it cannot be inferred | fixed_choice | Show only supported operation labels. |
| Legislative Data Group | fusion_lov | Show LDG names; retain its ID and legislation internally. |
| Existing Calculation Value Definition | fusion_lov | Search in the selected LDG and effective context and show business names. |
| Value Definition Group | fusion_lov | Show groups scoped to the selected LDG. |
| Calculation Type | fusion_lov | Show every current scoped CalculationTypeVO choice. Standalone CVD-HDL04 accepts any exact selected row, including a customer-defined label, subject to parentPayloadShape; CVD-HDL10 remains Flat Amount only. CVD-HDL11 inherits and validates the existing parent's exact value. |
| Unit of Measure | fusion_lov | After Calculation Type is selected, first resolve the preliminary parent field state. Show eligible PAY_UNITS values only when that result makes UOM applicable. Standalone CVD-HDL04 accepts any exact applicable value, including non-Money units; CVD-HDL10 remains Money only. CVD-HDL11 validates the existing parent's exact value when a unit applies. |
| Retrieval Date, Currency, Periodicity, Database Item, Rate Definition, referenced Calculation Value Definition, Value Type, selected Enterable Value, Calculation Card, Calculation Component, and Value Set | fusion_lov | Run the field's declared resolver in its active scope. |
| Use Existing Value Definition Group | fixed_choice | Existing groups are supported for parent create. Creating a new group is outside this task's executable scope. |
| Name and Base Name | free_form | Nonblank text, at most 120 characters. |
| Effective As-of Date, Effective Start Date, Effective End Date, and mutation boundary | free_form | ISO date in YYYY-MM-DD format; the verified parent create is open-ended, so a supplied parent Effective End Date blocks that route. |
| From Value, To Value, and calculation result values | free_form | State the data type required by the selected parent Calculation Type. |
| Enterable Calculation Value Display Value | free_form | Nonblank display prompt. |
| Value Identifier | fusion_lov or free_form | Select exactly the source declared for the chosen Calculation Type, then label the prompt with that resolved input kind. |
| Calculation Type Override | No prompt | An independent calculation-type override on a regular RangeItem child is blocked while its mapping is unreliable. CVD-HDL11 does not prompt for another type; it derives the existing parent's exact live type. |
| Fusion IDs, semantic codes, legislation code, service-controlled dates, and returned links | derived_or_route_owned | Resolve from the current operation and never expose as a requested value. |

After each user answer:

1. Validate a fixed or free-form value, or resolve the selected LOV row.
2. If invalid or unresolved, explain the business rule and ask the same
   requirement again with its input-kind label.
3. If accepted, persist it only in the current operation, invalidate affected
   dependents, recompute the dependency order, and immediately run any lookup
   needed for the next requirement.
4. End the response with the next direct, actionable question. A compact batch
   is allowed only for independent requirements, and a partial batch answer
   advances immediately to the next unresolved requirement.

Do not end a `collecting` turn with only progress, a list of completed fields,
or "ask me for the next step." Stop this continuation only when the request is
ready for confirmation, completed read-only, blocked, cancelled, explicitly
paused, or awaiting mutation approval.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | search, read, create_parent, create_parent_with_range_item, create_range_item, create_range_item_override, create_allowed_override, create_override_usage, correct_parent, update_parent, end_date_parent, delete_parent, correct_range_item, update_range_item, end_date_range_item, delete_range_item, correct_allowed_override, update_allowed_override, end_date_allowed_override, delete_allowed_override, correct_override_usage, update_override_usage, end_date_override_usage, or delete_override_usage | Stop and request one recognized operation; only search/read and the exact released native HDL profiles may execute normally | Classify the route before collecting mutation fields; return CVD_HDL_ROUTE_FROZEN for every registered-BO child request and every other unsupported mutation | Always | |
| Create command isolation | A newly allocated operationId, collecting state, and business-value provenance belonging only to the current Create command | Reject inherited operation state before any lookup, archive, preview, or mutation | Initialize empty operation-local state and ingest only values supplied, selected, resolved, or freshly defaulted for this operation | create_parent, create_parent_with_range_item, create_range_item, create_range_item_override, create_allowed_override, or create_override_usage | |
| Target context | environment alias, effectiveAsOfDate, LegislativeDataGroupId, Legislative Data Group name, and LegislationCode | Stop before target reads or planning a mutation | Resolve one exact legislative data group and derive its legislation code for workflow/display and REST lookup context | Always | find_legislative_data_group |
| Native HDL legislative key | Exact LegislativeDataGroupName from the selected current-operation LDG; LegislativeDataGroupId and LegislationCode absent from the DAT | Stop before archive generation | Retain IDs and legislation only in technical state and author the exact selected LDG name | create_parent or create_parent_with_range_item | find_legislative_data_group |
| Range Item Override native business keys | Exact LegislativeDataGroupName, ValueDefinitionName, and exact current CalculationTypeName derived from the fresh eligible-parent receipt; every target surrogate ID is absent from the DAT | Stop before archive generation | Retain target IDs only as read evidence and author the exact current business labels in the CVD-HDL11 row | create_range_item_override | find_parent_definition |
| Native HDL value group key | Exact ValueGroupName from the selected current-operation group; ValueGroupId absent from the DAT | Stop before archive generation | Retain the ID only as lookup evidence and author the exact selected group name | create_parent or create_parent_with_range_item | find_value_definition_group |
| Native HDL calculation type key | Exact CalculationTypeName from the selected current-operation type; CalcTypeId and CalculationTypeId absent from the DAT | Stop before archive generation | Retain the ID and semantic code only as validation evidence and author the exact selected type name | create_parent or create_parent_with_range_item | find_calculation_type |
| Parent identity | ValueDefnId plus the fresh effective-as-of item self link, or an exact parent name plus LDG and as-of date | Stop before parent or child access | Resolve exactly one effective parent and retain its returned links | Read, child create, or any parent/child lifecycle mutation | find_parent_definition |
| Range Item Override baseline | One exact nonproduction open-ended parent whose Calculation Type and applicable Unit of Measure resolve exactly in the current tenant and whose complete expanded read proves exactly one baseline Range Item and zero Allowed Overrides, nested Override Usages, Value Usages, or Related Elements | Stop before preview or archive generation | Resolve the parent by business labels, retain its live type/unit and complete baseline fingerprint internally, resolve the required result-slot shape, and require zero matching lower bounds plus zero overlaps when the bounds are comparable | CVD-HDL11 create_range_item_override | find_parent_definition |
| Parent create identity | Name, BaseName, EffectiveStartDate, Legislative Data Group label, and current-operation user selections for one existing value definition group, one calculation type, and Unit of Measure when applicable | Stay in collecting; do not author an archive or preview | Resolve complete in-scope choice sets and apply Large Choice Validation before asking the user to select every omitted semantic value | create_parent or create_parent_with_range_item | find_calculation_type |
| CVD-HDL04 parent payload shape | One exact current tenant Calculation Type and a preliminaryParentFieldState that classifies whether UOM applies; when applicable, one exact current tenant Unit of Measure; then a complete parentPayloadShape that classifies required/optional/forbidden fields and proves template membership, resolver lineage, and readable reconciliation for every conditional field | Return PAYLOAD_SHAPE_UNRESOLVED before archive generation without declaring an exact LOV value invalid | Resolve the preliminary field state through resolve_parent_payload_shape; collect and resolve UOM only when applicable; then finalize the shape, collect missing required business values, and author only its proved field set | create_parent | resolve_parent_payload_shape |
| Runtime-verified narrow parent shape | Exact normalized Calculation Type Flat Amount with semantic code F, exact Unit of Measure Money with code M, and no type-specific field outside the operation's fixed DAT allowlist. The combined create authors no EffectiveEndDate; Parent Correct and Update require an existing open-ended physical range. | Return CVD_HDL_ROUTE_FROZEN before archive generation | Preserve valid selected labels as read-only evidence and explain that the requested shape is outside the unchanged narrow profile | create_parent_with_range_item, correct_parent, or update_parent | find_calculation_type |
| Existing value definition group | Current-operation user selection plus the exact group Name in the selected LDG | Stay in collecting before parent create | Present the scoped group choices or searchable bounded pages and require selection; do not reuse a prior operation's group | create_parent or create_parent_with_range_item | find_value_definition_group |
| Unit of measure | Current-operation user selection plus exact UnitOfMeasure code and meaning when the selected calculation type makes UOM applicable | Stay in collecting before parent create | Present the PAY_UNITS choices or searchable bounded pages and require selection; do not default or reuse a prior operation's unit | create_parent or create_parent_with_range_item when UnitOfMeasure is applicable | find_unit_of_measure_code |
| Calculation value bounds | LowValue and HighValue | Stop before child preview | Ask for both values and validate them against the selected parent calculation type | create_range_item, create_range_item_override, or create_parent_with_range_item | |
| Calculation value result | The calculation-type-specific result inputs represented by RangeValueA, RangeValueB, and RangeValueC and any live resolver-backed reference required by the resolved result-slot shape | Stop before child preview | Collect every required result and author only its live-template-supported HDL field; for CVD-HDL11 map Value1, Value2, and Value3 to RangeValueA, RangeValueB, and RangeValueC respectively, and require a declared readable reconciliation attribute for every additional authored result field | create_range_item, create_range_item_override, or create_parent_with_range_item | |
| Enterable calculation value | OverrideType and Prompt | Stop before child preview | Resolve one eligible override type and collect the display prompt | create_allowed_override | find_override_type |
| Usage rule parent | AllowOverridesId plus the selected allowed override's fresh nested OverrideUsages collection link | Stop before usage preview | Resolve exactly one allowed override from the active parent; inject its ID internally into the create body and never request it from the user | create_override_usage or any Override Usage lifecycle mutation | find_allowed_override |
| Usage rule hierarchy | LegislativeDataGroupId, DirCardDefinitionId, DirCardCompDefId, and optional ValueSetCode | Stop before usage preview | Resolve the LDG and card first, then its component, then an optional table value set; inject the LDG ID internally into the create body | create_override_usage | find_calculation_card |
| Child mutation target | One exact active Range Item selected by parent name, LDG, as-of date, From value, and item start date; retain its internal ID and complete physical range only as read evidence | Stop before child preview | Resolve from the current expanded parent and never request an ID from the user | Supported Range Item Correct, Update, or Delete | find_range_item |
| Date-effective mutation | operation profile, boundary date or complete delete range, selected business key, and fresh target fingerprint | Stop before preview | Re-read the exact slice and bind the operation to the native HDL business-key row | Supported Parent or Range Item Correct, Update, or Delete | find_parent_definition |
| Parent Correct change | One corrected Currency selected from the current Currency LOV, different from the target's current Currency; no other requested change | Stop before archive generation | Resolve the exact currency by business code or name and bind it to the selected CVD-HDL07S target | CVD-HDL07A correct_parent | find_currency |
| Parent Update change | One new effective start date strictly after the target physical start and one different Currency selected from the current Currency LOV; no other requested change | Stop before archive generation | Resolve the exact currency by business code or name and bind the new boundary and currency to the selected CVD-HDL07S target | CVD-HDL07B update_parent | find_currency |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Any target operation is requested | Valid only when one exact LDG, legislation code, and effective-as-of date define the scope | Resolve the scope before any dependent lookup | find_legislative_data_group |
| A parent create is requested | Valid only when the current operation records explicit user selections for the value definition group, calculation type, and applicable unit of measure, and the selected values resolve in the same LDG and effective context | If any choice was omitted, complete its read-only LOV, apply Large Choice Validation, and remain in collecting; otherwise resolve the selected values and apply parent defaults | find_calculation_type |
| A combined parent and Range Item create is requested | Eligible only for CVD-HDL10 with one new Flat Amount/Money parent, one same-start Range Item, and zero other children | Resolve all parent labels, collect From/To/Flat Amount, derive the child start from the parent, require zero exact parent matches, and author the exact native HDL parent and child rows | find_calculation_type |
| A standalone CVD-HDL04 parent Calculation Type resolves exactly and, after preliminary field-state resolution, every applicable Unit of Measure resolves exactly | The business selections are valid regardless of delivered/customer-defined label or Money/non-Money unit | First determine UOM applicability, collect UOM only when applicable, then finalize parentPayloadShape; collect its required conditional values and stop as PAYLOAD_SHAPE_UNRESOLVED only if the complete field/read-back contract cannot be proved | resolve_parent_payload_shape |
| A Range Item create is requested | Eligible only for the CVD-HDL05 supported Flat Amount profile | Resolve the exact parent and zero-child baseline, collect Effective Start Date, From, To, and Flat Amount, and author the exact native HDL child row; no other RangeItem child-discriminator Create route is released, while CVD-HDL11 is a separate root | find_parent_definition |
| A Range Item Override create is requested | Eligible only for CVD-HDL11 against one exact nonproduction, open-ended parent whose exact Calculation Type, applicable Unit of Measure, required result-slot shape, one baseline Range Item, and zero other child families are established from current tenant evidence | Collect explicit Effective Start Date, From, To, and every result required by the resolved shape; require zero existing Range Items with the proposed lower bound and no type-comparable overlap; author one independent-root RangeItemOverride row using only current-template-supported fields | find_parent_definition |
| A calculation value is requested | Valid only when the supplied result fields match the parent calculation-type field matrix | Remove fields not rendered for the type and collect every rendered required field | |
| An explicit calculation type override is requested for a RangeItem | Invalid because the short-code-to-ID mapping can resolve an unusable value | Record the historical inheritance observation and stop; do not author a child row | |
| An Allowed Override create is requested | Registered ADF REST BO child creation is unavailable | Return CVD_HDL_ROUTE_FROZEN before lookup, candidate authoring, approval, or dispatch; the registered-BO child-write boundary is non-authorizing | |
| An Override Usage create is requested | Registered ADF REST BO child creation is unavailable | Return CVD_HDL_ROUTE_FROZEN before lookup, candidate authoring, approval, or dispatch; never ask the user for IDs | |
| A ValueSetCode is supplied for a usage rule | Valid only when it resolves as a TABLE validation-type value set | Resolve the exact code or omit the optional field | find_table_value_set |
| Parent Correct is requested | Eligible only for CVD-HDL07A after one explicit CVD-HDL07S target selection proves the exact childless, open-ended Flat Amount/Money profile and the user selects a different exact Currency | Build and validate the currency-only native HDL archive, then require target-bound immutable approval and pre-dispatch revalidation | find_parent_definition |
| Parent Update is requested | Eligible only for CVD-HDL07B after one explicit CVD-HDL07S target selection proves the exact childless, open-ended Flat Amount/Money profile, no existing future slice, a new boundary after the current physical start, and a different exact Currency | Build and validate the currency-only new-slice archive, then require target-bound immutable approval and pre-dispatch revalidation | find_parent_definition |
| Parent Delete is requested | Eligible only for CVD-HDL07C after one explicit CVD-HDL07S target selection proves zero children and complete timeline evidence proves exactly one physical slice | Build and validate the complete-range one-row Delete archive, then require target-bound immutable approval and pre-dispatch revalidation | find_parent_definition |
| Range Item Delete is requested | Eligible only for CVD-HDL09D after CVD-HDL09S selects the sole open-ended Flat Amount Range Item and a fresh expanded parent read proves zero other children | Build and validate the one-row child Delete archive, then require target-bound immutable approval and pre-dispatch revalidation | find_range_item |
| End Date, any child lifecycle mutation outside CVD-HDL09A Range Item Correct, CVD-HDL09B Range Item Update, or CVD-HDL09D Range Item Delete, Parent Delete outside CVD-HDL07C, Parent Correct outside CVD-HDL07A, or Parent Update outside CVD-HDL07B is requested | Ineligible for execution because no released native HDL operation contract covers it | Return CVD_HDL_ROUTE_FROZEN; do not author an archive, request approval, or write | find_parent_definition |
| A registered-BO child proof is requested | No current task input contract supports a new child proof | Return CVD_HDL_ROUTE_FROZEN; reconsideration is outside this task until new authoritative proof establishes a supported contract | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name and BaseName are nonblank and no longer than 120 characters | Return every missing or overlength field and stop | create_parent | |
| Every business value, resolved ID, lookup result, derived default, child draft, payload, archive, fingerprint, approval, and receipt belongs to the current Create operation | Reject prior-run provenance and return to fresh collecting state; do not convert a Create command into an implicit resume | create_parent, create_parent_with_range_item, create_range_item, create_range_item_override, create_allowed_override, or create_override_usage | |
| effectiveAsOfDate, EffectiveStartDate, and mutation boundaries use YYYY-MM-DD | Reject malformed dates | Any date-aware operation | |
| EffectiveEndDate is supplied for parent create | Return CVD_HDL_ROUTE_FROZEN; the released CVD-HDL04 create contract is open-ended for every resolved payload shape | create_parent | |
| Internally resolved IDs are positive decimal values no longer than the registered field length; users are never asked to enter them | Reject names, booleans, nondecimal values, zero, negatives, and overlength values | Any operation using an internal ID | |
| Value Definition Group, Calculation Type, and applicable Unit of Measure each have current-operation user-selection provenance | Stay in collecting and present the unresolved field's complete small choice set or searchable bounded pages; a previous run, archive, project artifact, recorded evidence, example, or unselected lookup result is not user input | create_parent | find_value_definition_group |
| A native HDL parent DAT row has exact LegislativeDataGroupName, ValueGroupName, and CalculationTypeName from current-operation selections and omits their surrogate IDs and LegislationCode | Reject missing, stale, mismatched, ID-based, or mixed-scope fields before archive generation | create_parent or create_parent_with_range_item | find_legislative_data_group |
| The CVD-HDL04 parent DAT contains exactly one MERGE row with the six fixed business fields and only the conditional fields in authoredParentFields, without RestAction, effectiveOf, surrogate IDs, Language, or SourceLang | Reject unknown/forbidden fields, a missing required field, another row, REST controls, IDs, language fields, or malformed dates | create_parent | resolve_parent_payload_shape |
| The selected calculation type is one exact current CalculationTypeVO row | For CVD-HDL04, accept a delivered or customer-defined value and use a returned semantic code or exact known-name mapping only as shape guidance; an unknown semantic shape is PAYLOAD_SHAPE_UNRESOLVED, not a catalog mismatch. CVD-HDL10 and ordinary Range Item profiles retain their explicit Flat Amount restriction. | create_parent, create_parent_with_range_item, or create_range_item | find_calculation_type |
| The CVD-HDL11 parent's CalculationTypeId and exact CalculationTypeName resolve to one current CalculationTypeVO row | Accept every exact delivered or customer-defined tenant value; absence from the packaged semantic map is not invalid. Continue only after the required result-slot shape is established from the returned semantic code, current metadata, and baseline row. | create_range_item_override | find_calculation_type |
| The CVD-HDL11 parent has no applicable UnitOfMeasure, or its exact UnitOfMeasure resolves to one current PAY_UNITS row | Accept every exact tenant value, including a non-Money unit; do not author Uom in RangeItemOverride.dat | create_range_item_override | find_unit_of_measure_code |
| The executable CVD-HDL04 parent has one exact tenant-valid Calculation Type, an exact tenant-valid UOM only when preliminaryParentFieldState makes it applicable, and a complete parentPayloadShape, authoredParentFields, and parentReadbackMappings receipt | Return PAYLOAD_SHAPE_UNRESOLVED when the preliminary decision, finalized shape, or mapping is incomplete; do not reject the live LOV value or guess a DAT row | create_parent | resolve_parent_payload_shape |
| CurrencyCode is absent because the resolved shape forbids it, blank where optional, or resolves exactly through the currency LOV when authored | Reject an unresolved authored code; do not invent one when no default exists | CVD-HDL04 when parentPayloadShape allows/requires CurrencyCode, or fixed CVD-HDL10 Flat Amount parent | find_currency |
| The Parent Correct target's current Currency and the requested corrected Currency each resolve exactly and differ | Reject unresolved, stale, ambiguous, or no-op currency changes | CVD-HDL07A correct_parent | find_currency |
| DateMode, Periodicity, Database Item, or ValueIdentifier is applicable to CVD-HDL04 | Require the field to be allowed/required by parentPayloadShape, resolve it through its declared input/lookup contract, verify current template membership and read-back mapping, and author DatabaseItemName rather than DatabaseItemId | create_parent | resolve_parent_payload_shape |
| A Range Item create reaches archive authoring before the exact CVD-HDL05 parent, duplicate, live template, immutable archive, and Task Hook gates pass | Reject it and return to controlled preflight | create_range_item | find_parent_definition |
| A Range Item Override create reaches archive authoring before the exact CVD-HDL11 parent, live type/unit and result-slot resolution, one-baseline-Range-Item state, duplicate/overlap, live template, immutable archive, and Task Hook gates pass | Reject it and return to controlled preflight | create_range_item_override | find_parent_definition |
| An Allowed Override or Override Usage create reaches archive authoring, approval, or execution | Reject it as CVD_HDL_ROUTE_FROZEN; registered-BO child creation is unavailable | create_allowed_override or create_override_usage | |
| A Value Usage, Related Element, or Range Item Override operation outside CVD-HDL11 Create reaches archive authoring | Reject it as CVD_HDL_ROUTE_FROZEN | Every unsupported child create or Range Item Override lifecycle operation | |
| A child lifecycle mutation outside CVD-HDL09A, CVD-HDL09B, or CVD-HDL09D reaches archive authoring | Reject it as CVD_HDL_ROUTE_FROZEN | Every unsupported child lifecycle mutation | |
| A Parent Correct reaches DAT authoring outside the exact CVD-HDL07A currency-only contract, or without its fresh target/schema/Task Hook evidence | Reject it as CVD_HDL_ROUTE_FROZEN or stale; historical REST headers and verbs are not DAT controls | correct_parent | find_parent_definition |
| A Parent Update reaches DAT authoring outside the exact CVD-HDL07B currency-only new-slice contract, or without its fresh target/schema/Task Hook evidence | Reject it as CVD_HDL_ROUTE_FROZEN or stale; historical REST headers and verbs are not DAT controls | update_parent | find_parent_definition |
| An End Date, Parent Delete outside CVD-HDL07C, or child lifecycle mutation outside CVD-HDL09A/CVD-HDL09B/CVD-HDL09D reaches DAT authoring | Reject it as CVD_HDL_ROUTE_FROZEN; historical REST headers and verbs are not DAT controls | Every unsupported lifecycle mutation | |
| Range Item Correct reaches DAT authoring outside CVD-HDL09A or without a fresh CVD-HDL09S target, live schema validation, immutable archive hash, and Task Hook result | Reject it as frozen or stale; do not infer correctness from historical REST evidence | correct_range_item | find_range_item |
| Range Item Update reaches DAT authoring outside CVD-HDL09B or without a fresh CVD-HDL09S open-ended target, a later boundary, changed Flat Amount, live schema validation, immutable archive hash, and Task Hook result | Reject it as frozen or stale; do not infer correctness from historical REST evidence | update_range_item | find_range_item |
| LowValue and HighValue are both present and LowValue is not greater than HighValue when their data type is comparable | Reject an incomplete or reversed interval | create_range_item, create_range_item_override, or create_parent_with_range_item | |
| Prompt is nonblank | Stop before preview | create_allowed_override | |
| ValueSetCode, when supplied, is the exact Code returned by TableValueSetLOVVO | Reject a display meaning or arbitrary value | create_override_usage | find_table_value_set |
| A historical REST Effective-Of header or product-resource mutation target appears in an execution plan | Reject the plan; these values are evidence only and cannot be dispatched | Every mutation | |
| Parent Delete target has any child row in RangeItems, AllowedOverrides, nested OverrideUsages, ValueUsages, or RelatedElements, or lacks complete proof of exactly one physical slice | Block rather than infer cascade or multi-slice behavior | delete_parent | find_parent_definition |
| Allowed Override Delete target contains no nested Override Usage | Block container Delete and resolve its usages first | delete_allowed_override | find_allowed_override |
| A child mutation body exceeds its closed allowlist: calculation-type-specific Range Item fields for Correct, Prompt for Allowed Override Correct/Update, or DirCardComponentDefId and ValueSetCode for Override Usage Correct/Update | Reject hidden, route-owned, date, identity, display-only, or unrelated fields | Child Correct or Update | |
| A future native HDL lifecycle row contains only fields proven by its live template and controlled runtime evidence | Keep the operation frozen until that exact action contract is productized; controlled evidence alone is not a release route | End Date, broader Delete, child lifecycle, or out-of-profile Correct/Update | |
| Parent Name or Base Name change is requested | Reject it; CVD-HDL07A and CVD-HDL07B permit only their declared Currency change | correct_parent or update_parent | |
| Opaque item keys and child keys come from current response links | Use them only for GET reads and reconciliation; reject their use as a product REST mutation target | Parent or child read/lifecycle classification | extract_active_resource_links |
| A mutation target and payload fingerprint differ from the approved preview | Invalidate approval and stop | Any mutation handoff | |
| End Date verification does not read immediately before, on, and after the boundary | Keep the operation unverified | Any End Date reconciliation | find_parent_definition |
| Delete verification does not prove zero exact matches across the former range | Keep the operation outcome unknown and never replay automatically | Any Delete reconciliation | find_parent_definition |
| Any mutation returns 2xx but authoritative read-back does not match the approved values and effective timeline | Record a verification mismatch, block the operation, and do not replay it automatically | Any mutation reconciliation | |

## CVD-HDL07A Parent Correct Allowlist

The released Parent Correct archive is valid only when all checks pass:

- CVD-HDL07S resolves one explicitly selected target for the same operation;
- the target is nonproduction, open-ended, Flat Amount, Money, and has zero
  Range Items, Allowed Overrides, nested Override Usages, Value Usages, and
  Related Elements;
- the target's current Currency and the requested corrected Currency each
  resolve exactly through the current Currency LOV and are different;
- Name, Base Name, physical start/end dates, LDG, Value Definition Group,
  Calculation Type, Unit of Measure, and every other business field are
  unchanged and cannot be supplied as edits;
- `ValueDefinition.dat` contains `SET PURGE_FUTURE_CHANGES N` and exactly one
  `MERGE|ValueDefinition` row using only the CVD-HDL07A ordered fields;
- the immutable preview binds both the archive SHA-256 and selected-target
  fingerprint, and a fresh pre-dispatch expanded read still matches both; and
- reconciliation uses exact expanded parent reads at the physical start date
  and the following day, proving the same physical range, corrected Currency,
  and zero child rows.

Any mismatch invalidates approval. Never replay an uncertain Data Loader
request.

## CVD-HDL07C Parent Delete Allowlist

The released Parent Delete archive is valid only when all checks pass:

- CVD-HDL07S resolves one explicitly selected target for the same operation;
- a fresh exact expanded GET proves zero Range Items, Allowed Overrides, nested
  Override Usages, Value Usages, and Related Elements;
- operation-local creation evidence or a separately source-backed complete
  timeline read proves exactly one physical slice;
- `ValueDefinition.dat` contains exactly one `DELETE|ValueDefinition` row using
  the complete physical start/end range, LDG label, and Value Definition Name;
- the immutable preview binds the archive SHA-256, selected-target fingerprint,
  and timeline evidence, and fresh pre-dispatch evidence still matches; and
- reconciliation proves one loaded and zero failed Delete rows, then zero exact
  Name-and-LDG matches at the former start, following day, and a later date.

Any mismatch invalidates approval. Never replay an uncertain deletion. Parents
with children or multiple physical slices remain frozen.

## CVD-HDL07B Parent Update Allowlist

The released Parent Update archive is valid only when all checks pass:

- CVD-HDL07S resolves one explicitly selected target for the same operation;
- the target is nonproduction, open-ended, Flat Amount, Money, childless, and
  has no existing future effective slice;
- the new effective start date is strictly after the target physical start;
- the current Currency and requested new Currency each resolve exactly through
  the current Currency LOV and are different;
- Name, Base Name, LDG, Value Definition Group, Calculation Type, Unit of
  Measure, and every other business field are unchanged;
- `ValueDefinition.dat` contains `SET PURGE_FUTURE_CHANGES N` and exactly one
  `MERGE|ValueDefinition` row using only the CVD-HDL07B ordered fields;
- the immutable preview binds the archive SHA-256, selected-target fingerprint,
  and new effective boundary, and fresh pre-dispatch evidence still matches;
  and
- reconciliation uses exact expanded parent reads immediately before, on, and
  after the new boundary, proving the old Currency before it, the new Currency
  on and after it, the expected split ranges, and zero child rows.

Any mismatch invalidates approval. Never replay an uncertain Data Loader
request.

## CVD-HDL04 ValueDefinition Create Allowlist

The standalone parent archive is valid only when all checks pass:

- one existing Value Definition Group, one Calculation Type, and every
  applicable Unit of Measure are explicit current-operation selections and
  exact current tenant LOV matches;
- every exact CalculationTypeVO row is eligible, including a customer-defined
  label, and every exact applicable PAY_UNITS row is eligible, including a
  non-Money unit; packaged semantic guidance is not an allowlist;
- the exact Calculation Type, Name, LDG, and effective-date duplicate preflight
  returns zero exact parent matches before archive authoring;
- `resolve_parent_payload_shape` first establishes the semantic type and
  preliminary field state, determines whether UOM applies, resolves an exact
  UOM selection only when applicable, and then finalizes required/optional/
  forbidden fields, resolver lineage, current template fingerprint,
  `authoredParentFields`, and `parentReadbackMappings`;
- the fixed fields are exactly `BaseName`, `EffectiveStartDate`,
  `ValueGroupName`, `CalculationTypeName`, `LegislativeDataGroupName`, and
  `ValueDefinitionName`;
- only the resolved subset of `CurrencyCode`, `Uom`, `DateMode`, `Periodicity`,
  `DatabaseItemName`, and `ValueIdentifier` is added; never author
  `DatabaseItemId` or another surrogate ID;
- a required conditional value is explicit or produced by its declared default
  and exact resolver, and no forbidden/inapplicable value is silently removed;
- the ZIP contains only `ValueDefinition.dat`, `SET PURGE_FUTURE_CHANGES Y`,
  one `METADATA|ValueDefinition` row, and one `MERGE|ValueDefinition` row, with
  fields in current live-template order and no end date, REST control, language
  field, child row, or extra member; and
- reconciliation uses one complete exact expanded parent GET and matches every
  fixed and conditional field through the operation-bound read-back map.

Known create semantics provide shape guidance, not business-value restrictions:
`F`, `FM`, `T`, and `RD` may expose Currency and Periodicity; `FM` requires a
database item; `D`, `N`, and `X` may expose Value Identifier; Retrieval Date and
applicable UOM follow their live field state. A customer-defined label can use a
known shape when its exact current row supplies that semantic code. If any
shape fact is missing, return `PAYLOAD_SHAPE_UNRESOLVED` before DAT authoring.

QA coverage is by distinct parent payload/resolver shapes, plus at least one
customer-defined label and one non-Money unit. It does not require a Cartesian
test of every Calculation Type and Unit combination because exact live LOV
validation and the payload-shape receipt are the runtime gates.

## CVD-HDL05 Range Item Allowlist

The controlled native child archive is valid only when all checks pass:

- one exact existing parent resolves by business name, LDG, and as-of date;
- the parent is open-ended Flat Amount with Money and has zero Range Items;
- the child Effective Start Date uses `YYYY-MM-DD` and falls within the parent
  effective range;
- From, To, and Flat Amount are finite decimals and From does not exceed To;
- no existing Range Item has the same lower bound;
- the root metadata fields are exactly `LegislativeDataGroupName` and
  `ValueDefinitionName`;
- the child fields are exactly `EffectiveStartDate`, `LowValue`, `HighValue`,
  `Value1`, `LegislativeDataGroupName`, and `ValueDefinitionName`; and
- the archive contains no parent `MERGE`, surrogate ID, end date, REST control,
  or language field.

`Value1` is the controlled Flat Amount hypothesis and must reconcile to
`RangeValueA`. A different calculation type or result shape remains frozen.

## CVD-HDL11 Range Item Override Create Allowlist

The released independent-root Create archive is valid only when all checks
pass:

- one exact existing parent resolves by business name, LDG, and as-of date;
- the target is nonproduction and open-ended; its CalculationTypeId and exact
  CalculationTypeName resolve to one current CalculationTypeVO row, and its
  UnitOfMeasure, when applicable, resolves to one current PAY_UNITS row;
- every exact current tenant type and applicable unit is accepted, including a
  customer-defined type label or a non-Money unit; a packaged-map omission is
  not an invalid value;
- one complete expanded parent GET proves exactly one baseline Range Item and
  zero Allowed Overrides, nested Override Usages, Value Usages, or Related
  Elements;
- the requested Effective Start Date uses `YYYY-MM-DD`, falls within the parent
  effective range, and is supplied explicitly with From, To, and every result
  input required by the resolved result-slot shape;
- no existing Range Item has the same lower bound; bound ordering and overlap
  checks run only when the resolved bound data type is comparable;
- the ZIP contains only `RangeItemOverride.dat`, `SET PURGE_FUTURE_CHANGES Y`,
  one `METADATA|RangeItemOverride` row, and one `MERGE|RangeItemOverride` row;
- the fixed business fields are `EffectiveStartDate`, `LowValue`, `HighValue`,
  `CalculationTypeName`, `LegislativeDataGroupName`, and
  `ValueDefinitionName`; add the exact live-template-supported subset of
  `Value1`, `Value2`, and `Value3`, plus the exact set of additional business
  result fields only when current metadata proves they are required and a
  declared resolver, the live template, and an exact expanded-read
  reconciliation mapping validate every field and value; a shape needing an
  extra field without all of that evidence remains unresolved;
- fields follow the current live `RangeItemOverride.dat` template order; the
  archive contains no target surrogate ID, end date, REST or language field,
  `COMMENT` directive, parent row, or additional member; result-reference IDs
  may appear only inside the applicable `Value1`/`Value2`/`Value3` slot when
  its type-specific resolver and the live template require them, and are never
  exposed as user-entered IDs; and
- reconciliation proves terminal one-loaded/zero-failed detail, Range Item
  count `1 -> 2`, and one exact new open-ended candidate in the complete
  expanded parent response while preserving the one baseline Range Item, the
  parent, and the zero counts for every other child family; every additional
  authored result field must match its predeclared readable response attribute.

Every authored result slot must reconcile type-aware: `Value1` to
`RangeValueA`, `Value2` to `RangeValueB`, and `Value3` to `RangeValueC`. This
profile releases Create only; Range Item Override Correct, Update, End Date,
and Delete remain frozen.

## CVD-HDL10 Combined Create Allowlist

The combined archive is valid only when all checks pass:

- the parent uses the fixed CVD-HDL10 Flat Amount/Money business profile; this
  combined route does not inherit generalized CVD-HDL04 conditional shapes;
- a complete Name, LDG, and effective-date duplicate check returns zero;
- exactly one Range Item is requested and its start equals the parent start;
- From, To, and Flat Amount are finite decimals and From does not exceed To;
- the live template validates both `ValueDefinition` and `RangeItem` fields;
- one immutable `ValueDefinition.dat` contains exactly one parent `MERGE` and
  one child `MERGE`, with no other children, IDs, end dates, language fields,
  or REST controls; and
- reconciliation proves exactly one parent, one matching Range Item, and zero
  other children in one complete expanded parent GET.

## CVD-HDL11 Calculation Result Shape Guidance

This matrix records known result-slot shapes for CVD-HDL11. It is guidance, not
a Calculation Type allowlist: an exact current tenant value remains eligible
when its semantic code maps to one of these shapes, including when its display
label is customer-defined. A genuinely new semantic code requires current live
metadata and the required baseline Range Item to establish its exact result
slots; until then the shape remains unresolved without declaring the LOV value
invalid. This result-slot matrix does not broaden CVD-HDL05 or CVD-HDL10 and
does not define the separate CVD-HDL04 parent payload shape.

QA coverage is organized by distinct result-slot and resolver shape, plus a
customer-defined label and a non-Money unit. It does not require a Cartesian
test of every Calculation Type and Unit of Measure combination because exact
current tenant LOV validation is the business-value gate.

| Parent Semantic Code | Required CVD-HDL11 Result Inputs | HDL to REST Reconciliation |
|---|---|---|
| F, FM, T, X, D, N, or G | One type-appropriate result | Value1 to RangeValueA |
| S1 | Two numeric parameters | Value1/Value2 to RangeValueA/RangeValueB |
| S2 | Three numeric parameters | Value1/Value2/Value3 to RangeValueA/RangeValueB/RangeValueC |
| RD | One rate-definition reference resolved by find_rate_definition | Value1 to RangeValueA |
| RDB or FP | One rate plus one referenced Calculation Value Definition resolved by find_calculation_value_definition | Value1/Value2 to RangeValueA/RangeValueB |
| GC | One referenced Calculation Value Definition resolved by find_calculation_value_definition | Value1 to RangeValueA |
| Other exact current tenant LOV value | Use its known semantic-code shape; for a new code, establish the exact field set from current metadata and the required baseline row | Reconcile each authored Value1/Value2/Value3 slot to its corresponding RangeValueA/RangeValueB/RangeValueC and each additional field through a predeclared expanded-read mapping; an unresolved shape stays collecting or blocked, but the LOV value is not invalid |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.VALIDATE_INPUT | decision | 1 | validate_input | valid->CVD.RESOLVE_DEPENDENCIES;invalid->CVD.HANDLE_ERROR | none | stop | Always |
