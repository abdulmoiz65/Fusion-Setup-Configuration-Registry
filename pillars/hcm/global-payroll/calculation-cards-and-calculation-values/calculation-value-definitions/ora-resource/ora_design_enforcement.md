# Calculation Value Definitions Design Enforcement

## Current Authority

CVD-HDL01 governs the released native HDL boundary. The only executable shapes
are CVD-HDL04 native Parent Create, CVD-HDL10 combined Parent-plus-Range-Item
Create, CVD-HDL05 Range Item Create, CVD-HDL11 Range Item Override Create,
CVD-HDL07A currency-only Parent Correct, CVD-HDL07B currency-only new-slice
Parent Update, CVD-HDL07C childless single-slice Parent Delete, CVD-HDL09A
Range Item Correct, CVD-HDL09B Range Item Update, and restricted CVD-HDL09D
Range Item Delete. Every other mutation returns `CVD_HDL_ROUTE_FROZEN`.

## Registered-BO Boundary

Child writes for resource objects without a released native HDL business-object
contract are unavailable. Product REST is GET-only. Return
`CVD_HDL_ROUTE_FROZEN` before candidate authoring, approval, or dispatch; do
not use Product REST as a fallback. Reconsider the boundary only when new
authoritative proof establishes a supported contract.

## Native HDL Contract

The executable Data Loader objects are **Payroll Deduction Value Definition**
and the narrowly released **Payroll Deduction Range Item Override** Create
profile. The first archive contains `ValueDefinition.dat`; its top discriminator
is `ValueDefinition`, and its supported child discriminator is `RangeItem`.
The second archive contains only `RangeItemOverride.dat` and uses the separate
LDG-level root discriminator `RangeItemOverride`. Native rows use delivered
business-key labels. Surrogate IDs, `RestAction`, `effectiveOf`, and product
REST headers are never DAT fields. Every CVD-HDL04 parent create omits
`Language` and `SourceLang` so Fusion applies base-language defaulting; its
conditional fields come only from a resolved `parentPayloadShape`. Flat
Amount/Money is the runtime-proven baseline, while other exact tenant-valid
shapes are live-metadata-gated QA candidates.
`RangeItemOverride` is released only for CVD-HDL11 Create; its other lifecycle
actions remain frozen.

| Profile | Instruction and control | Exact authored fields |
|---|---|---|
| CVD-HDL04 Parent Create | One ValueDefinition MERGE; SET PURGE_FUTURE_CHANGES Y | Fixed fields BaseName, EffectiveStartDate, ValueGroupName, CalculationTypeName, LegislativeDataGroupName, and ValueDefinitionName; add only the resolved current-template-supported subset of CurrencyCode, Uom, DateMode, Periodicity, DatabaseItemName, and ValueIdentifier, with declared resolver lineage and read-back mapping for every conditional field |
| CVD-HDL10 Parent plus Range Item Create | One parent MERGE and one same-start child MERGE; SET PURGE_FUTURE_CHANGES Y | Fixed Flat Amount/Money parent fields BaseName, EffectiveStartDate, ValueGroupName, CalculationTypeName, LegislativeDataGroupName, ValueDefinitionName, CurrencyCode, and Uom; child EffectiveStartDate, LowValue, HighValue, Value1, LegislativeDataGroupName, and ValueDefinitionName |
| CVD-HDL05 Range Item Create | Zero parent rows and one RangeItem MERGE; SET PURGE_FUTURE_CHANGES Y | EffectiveStartDate, LowValue, HighValue, Value1, LegislativeDataGroupName, ValueDefinitionName |
| CVD-HDL11 Range Item Override Create | One independent-root RangeItemOverride MERGE; SET PURGE_FUTURE_CHANGES Y | Fixed business fields EffectiveStartDate, LowValue, HighValue, CalculationTypeName, LegislativeDataGroupName, and ValueDefinitionName; the exact current-template-supported subset of Value1, Value2, and Value3 required by the resolved result shape; and only the exact set of additional business result fields for which current live metadata, a declared resolver, the live template, and a declared expanded-read reconciliation mapping each prove the field and value |
| CVD-HDL07A Parent Correct | One in-place ValueDefinition MERGE; SET PURGE_FUTURE_CHANGES N | EffectiveStartDate, LegislativeDataGroupName, ValueDefinitionName, CurrencyCode |
| CVD-HDL07B Parent Update | One future-slice ValueDefinition MERGE; SET PURGE_FUTURE_CHANGES N | EffectiveStartDate, LegislativeDataGroupName, ValueDefinitionName, CurrencyCode |
| CVD-HDL07C Parent Delete | One complete-range ValueDefinition DELETE | EffectiveStartDate, EffectiveEndDate, LegislativeDataGroupName, ValueDefinitionName |
| CVD-HDL09A Range Item Correct | Zero parent rows and one in-place RangeItem MERGE; SET PURGE_FUTURE_CHANGES N | EffectiveStartDate, LowValue, HighValue, Value1, LegislativeDataGroupName, ValueDefinitionName |
| CVD-HDL09B Range Item Update | Zero parent rows and one future-slice RangeItem MERGE; SET PURGE_FUTURE_CHANGES N | EffectiveStartDate, LowValue, HighValue, Value1, LegislativeDataGroupName, ValueDefinitionName |
| CVD-HDL09D Range Item Delete | Zero parent rows and one complete-range RangeItem DELETE | EffectiveStartDate, EffectiveEndDate, LowValue, LegislativeDataGroupName, ValueDefinitionName |

Every packet must be constructed deterministically from its exact profile in
this task-owned resource, validated against current live HDL metadata, and
reconciled using the operation-specific rules below. No table row broadens
these profiles.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Route classification | Match the request to GET-only product REST, one of the ten released native HDL route profiles, or a blocked registered-BO child request. Flat Amount/Money is the runtime-proven CVD-HDL04 baseline; another fully resolved CVD-HDL04 field shape is a controlled live-metadata-gated QA candidate within the same route profile. |
| 2 | Scope allowlist | Reject resources and actions outside the current CVD task allowlist. |
| 3 | Dependency and lookup integrity | Require exact scoped references and current response links. |
| 4 | DAT allowlist | Require the exact operation-specific native HDL contract, including HDL09D's business-key Range Item Delete fields; reject RestAction, effectiveOf, surrogate IDs, and unproved sections. |
| 5 | Semantic review | For CVD-HDL04, use the exact live Calculation Type and current field-state evidence to resolve preliminary UOM applicability; collect an exact UOM only when applicable; then finalize parentPayloadShape from the exact selections, current create semantics, live HDL metadata/template, declared field resolvers, and read-back mappings. Apply the unchanged fixed profile for CVD-HDL10 and the operation-specific constraints for every other route. |
| 6 | Lifecycle gate | For every allowed native mutation, require immutable preview, archive fingerprint, explicit confirmation, idempotency state, and reconciliation strategy before handoff. Parent Correct, Update, and Delete additionally bind and revalidate the selected-target fingerprint. |
| 7 | Secret and receipt hygiene | Ensure state, logs, diagnostics, and receipts contain no credentials or session secrets. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any product REST write is proposed | Error | | Method is POST, PATCH, PUT, or DELETE on a product resource | Refuse the request; product REST is GET-only for this task | No |
| Allowed Override or Override Usage create is proposed | Error | | Registered-BO child creation is unavailable | Return CVD_HDL_ROUTE_FROZEN; do not construct a candidate, replay evidence, or fall back to product REST | No |
| A setup-task CSV archive is supplied to this native-HDL contract | Error | | The plan attempts to parse, convert, validate, or dispatch CSV through the native-HDL rules | Stop this HDL route and return the request to the catalog-supported CSV workflow declared in `SKILL.md`; do not convert CSV to DAT | Yes, by routing before native-HDL authoring |
| Any operation other than search/read, the exact HDL04 parent create, HDL10 combined parent-plus-Range-Item create, HDL05 Range Item create, HDL11 Range Item Override Create, HDL09A Range Item Correct, HDL09B Range Item Update, restricted HDL09D Range Item Delete, HDL07A Parent Correct, HDL07B Parent Update, or HDL07C Parent Delete is proposed for execution | Error | | The operation is outside the current route registry | Return CVD_HDL_ROUTE_FROZEN and perform zero archive authoring, approval, or write | No |
| A supported mutation is collecting input | Error | | A surrogate ID is requested or displayed, the next dependency lookup is skipped, or the response ends without the next missing business question | Apply the input-kind and continuation contract in ora_input_validation.md, keep IDs in machine state, and continue with the next label-based or free-form question | Yes, before preview |
| A supported native HDL mutation advances toward dispatch | Error | | A stage in the Governed Write Sequence below is skipped or reordered, approval is absent or not hash-bound, the archive changed, or upload/initiation would repeat | Stop at the first unmet stage; rebuild or reapprove as required and never replay a write automatically | Yes before upload; no automatic retry after dispatch |
| A supported native HDL mutation is reconciled | Error | find_parent_definition | Parent and Range Items do not come from the required complete expanded parent GET, or the direct /child/RangeItems link was used | Reject the evidence and repeat only the collection-level expanded parent GET; never retry or reconstruct the direct child route | Yes, with a fresh read-only GET |
| A CVD-HDL10 combined create resolves its Legislative Data Group | Error | find_legislative_data_group | The selected Legislative Data Group does not resolve exactly in the current operation | Keep the plan in collecting until the user selects one exact Legislative Data Group | Yes, before archive generation |
| A CVD-HDL10 combined create resolves its Value Definition Group | Error | find_value_definition_group | The selected existing Value Definition Group does not resolve exactly in the selected scope | Keep the plan in collecting until the user selects one exact existing group | Yes, before archive generation |
| A CVD-HDL10 combined create resolves its Calculation Type | Error | find_calculation_type | The selected Calculation Type does not resolve exactly or is not Flat Amount | Preserve any valid unsupported selection as evidence and stop before archive authoring | No for an unsupported type; yes for an unresolved selection |
| A CVD-HDL10 combined create resolves its Unit of Measure | Error | find_unit_of_measure_code | The selected Unit of Measure does not resolve exactly or is not Money | Preserve any valid unsupported selection as evidence and stop before archive authoring | No for an unsupported unit; yes for an unresolved selection |
| A CVD-HDL10 combined create resolves its supplied Currency | Error | find_currency | A supplied Currency does not resolve exactly | Keep the plan in collecting until the user selects one exact Currency | Yes, before archive generation |
| A CVD-HDL10 combined create validates its local scope | Error | | The target is production, the parent duplicate count is not zero, the child date differs from the parent date, or more than one Range Item is requested | Keep the plan in collecting or preflight; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL10 archive is handed off or reconciled | Error | find_parent_definition | The archive is not exactly one parent and one same-start Range Item in one member, its hash/schema evidence is stale, loader success is absent, or one expanded read does not prove the exact parent, exact child, and zero other children | Rebuild before approval or classify the dispatched result as incomplete; never replay a write | Yes before dispatch; no automatic retry afterward |
| A CVD-HDL05 child create is planned | Error | find_parent_definition | More than one child is selected, the target is not nonproduction, a surrogate ID is authored, the parent is not the proved Flat Amount/Money/open-ended profile, the baseline is not zero Range Items, or live template preflight has not completed | Keep the plan in preflight; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL05 archive is handed off | Error | find_parent_definition | The DAT has a parent MERGE, another child section, an end date, an ID, a REST/language field, anything other than exactly one RangeItem row using the MERGE instruction, or a stale parent/duplicate/schema check | Rebuild from the exact CVD-HDL05 profile and restart validation | Yes, before preview |
| A CVD-HDL11 Range Item Override Create is planned | Error | find_parent_definition | More than one row is selected; the target is production or not open-ended; its Calculation Type or applicable Unit of Measure does not resolve exactly in the current tenant; its required result-slot shape is unresolved; the complete baseline is not exactly one Range Item with zero other child families; the proposed lower bound exists; a type-comparable interval overlaps; or live RangeItemOverride template preflight has not completed | Keep the plan in preflight; accept every exact delivered or customer-defined live type/unit value and resolve its payload shape rather than applying a Flat Amount/Money gate | Yes, before archive generation |
| A CVD-HDL11 archive is handed off or ready to dispatch | Error | find_parent_definition | The ZIP is not exactly one RangeItemOverride.dat; the DAT lacks SET PURGE_FUTURE_CHANGES Y; it has anything other than one RangeItemOverride MERGE whose fixed keys and resolved result fields follow current live-template order; it includes an end date, target ID, REST/language field, COMMENT, parent row, extra member, or unproved optional field; or its parent/type/unit/baseline/schema/Task Hook/hash evidence is stale | Invalidate approval and rebuild from the exact CVD-HDL11 profile and current read-only evidence | Yes before dispatch; no automatic retry afterward |
| A CVD-HDL11 result is reconciled | Error | find_parent_definition | Loader detail does not prove one loaded and zero failed row; the complete expanded parent GET does not prove Range Item count 1 -> 2; the baseline changed; the requested row is absent or duplicated; any authored Value1, Value2, or Value3 fails its type-aware mapping to RangeValueA, RangeValueB, or RangeValueC; any additional authored result field lacks or fails its declared expanded-read mapping; the new row is not open-ended; or another child count changed | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the request and receipt, and never replay the write automatically | No automatic write retry |
| A CVD-HDL09D Range Item Delete resolves its parent | Error | find_parent_definition | The parent was not resolved before Range Item selection or has another child | Return to label-only parent selection; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL09D Range Item Delete resolves its item | Error | find_range_item | The target was not selected through CVD-HDL09S, is not the sole open-ended Flat Amount Range Item, or current schema/Task Hook evidence is missing | Return to label-only Range Item selection; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL09D archive is handed off or dispatched | Error | find_range_item | The DAT is not exactly one business-key RangeItem row using the DELETE instruction, its physical dates or target fingerprint changed, the archive hash changed, or a write would be replayed | Invalidate approval and rebuild from fresh read-only evidence; never replay an uncertain write | Yes before dispatch; no automatic retry afterward |
| A CVD-HDL09D result is reconciled | Error | find_parent_definition | Loader detail does not prove one loaded and zero failed child rows, the parent is absent, or Range Items remain on the item start date or following day | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the request, and do not replay it | No automatic write retry |
| Range Item End Date is requested | Error | find_range_item | ReplaceLastEffectiveEndDate remains absent from the live UCM template and the shared validator has no sanctioned special-control path | Return CVD_HDL_ROUTE_FROZEN, cite CVD-HDL09E, and perform zero archive authoring or mutation | No; requires shared-loader support and a new controlled proof |
| A CVD-HDL07A Parent Correct resolves its target | Error | find_parent_definition | The target was not explicitly selected through CVD-HDL07S for this operation, is not nonproduction, or is not an open-ended Flat Amount/Money childless parent | Return to label-only target selection; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL07A Parent Correct resolves its Currency change | Error | find_currency | The current and corrected Currency do not resolve exactly or do not differ | Return to Currency selection; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL07A archive is handed off | Error | find_parent_definition | The DAT changes anything except Currency, omits SET PURGE_FUTURE_CHANGES N, has anything other than one parent MERGE, contains a surrogate ID/REST/language field, or its schema/Task Hook evidence is stale | Rebuild from the exact CVD-HDL07A profile and restart validation | Yes, before preview |
| A confirmed CVD-HDL07A archive is ready to dispatch | Error | find_parent_definition | A fresh exact expanded read or archive rehash differs from the approved target fingerprint or SHA-256 | Invalidate approval, rebuild from current state, and request a new approval; do not dispatch | Yes, with fresh read-only evidence |
| A CVD-HDL07B Parent Update resolves its target and boundary | Error | find_parent_definition | The target was not explicitly selected through CVD-HDL07S for this operation, is not nonproduction, is not an open-ended Flat Amount/Money childless parent, already has a future slice, or the new boundary is not after the physical start | Return to label-only target selection or boundary entry; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL07B Parent Update resolves its Currency change | Error | find_currency | The current and new Currency do not resolve exactly or do not differ | Return to Currency selection; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL07B archive is handed off | Error | find_parent_definition | The DAT changes anything except Currency on the explicit new boundary, omits SET PURGE_FUTURE_CHANGES N, has anything other than one parent MERGE, contains a surrogate ID/REST/language field, or its schema/Task Hook evidence is stale | Rebuild from the exact CVD-HDL07B profile and restart validation | Yes, before preview |
| A confirmed CVD-HDL07B archive is ready to dispatch | Error | find_parent_definition | A fresh exact expanded read, future-slice check, or archive rehash differs from the approved target fingerprint, boundary, or SHA-256 | Invalidate approval, rebuild from current state, and request a new approval; do not dispatch | Yes, with fresh read-only evidence |
| A CVD-HDL07B result is reconciled | Error | find_parent_definition | The prior-day read does not show the old Currency and range ending immediately before the boundary, the boundary/following-day reads do not show the new open-ended slice and Currency, or any read shows children | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the request, and do not replay it | No automatic write retry |
| A CVD-HDL07C Parent Delete is planned | Error | find_parent_definition | The target was not explicitly selected through CVD-HDL07S for this operation, is not nonproduction, has children, lacks complete timeline evidence, or does not have exactly one physical slice | Return to label-only target selection or timeline proof; do not author an archive or ask for approval | Yes, before archive generation |
| A CVD-HDL07C archive is handed off | Error | find_parent_definition | The DAT has anything other than exactly one complete-range ValueDefinition row using the DELETE instruction, contains a child/ID/REST/language field, or its schema/Task Hook evidence is stale | Rebuild from the exact CVD-HDL07C profile and restart validation | Yes, before preview |
| A confirmed CVD-HDL07C archive is ready to dispatch | Error | find_parent_definition | A fresh exact expanded read, complete timeline check, or archive rehash differs from the approved target fingerprint or SHA-256 | Invalidate approval, rebuild from current state, and request a new approval; do not dispatch | Yes, with fresh read-only evidence |
| A CVD-HDL07C result is reconciled | Error | find_parent_definition | Loader detail does not prove one successful Delete row or any complete exact Name-and-LDG read at the former start, following day, or later date still finds the parent | Classify as CONTRACT_INCOMPLETE or OUTCOME_UNKNOWN, preserve the request, and do not replay it | No automatic write retry |
| Parent create is planned | Error | find_value_definition_group | The plan creates a new value definition group | Use one exact existing group; group creation is outside this task's native HDL scope | Yes, by selecting an existing group |
| CVD-HDL04 parent create resolves its Calculation Type | Error | find_calculation_type | The selected Calculation Type is not one exact current CalculationTypeVO row | Resolve the selection again. Do not substitute Flat Amount and do not reject an exact customer-defined label merely because it is absent from the packaged map | Yes, before shape resolution |
| CVD-HDL04 parent create resolves an applicable Unit of Measure | Error | find_unit_of_measure_code | The selected Unit of Measure is not one exact current PAY_UNITS row or is forbidden by the resolved parent shape | Resolve an applicable selection again. Do not substitute Money and do not reject an exact non-Money value solely because of its code | Yes, before archive generation |
| CVD-HDL04 parent create is planned | Error | resolve_parent_payload_shape | parentPayloadShape does not identify the semantic type, applicable unit, required/optional/forbidden fields, live-template membership, resolver lineage, and readable reconciliation mapping for every conditional field | Return PAYLOAD_SHAPE_UNRESOLVED, retain the exact business selections, and stop before DAT authoring. Never guess a field set or call the LOV value invalid | Yes, with current metadata or an explicit missing business value |
| A nonbaseline CVD-HDL04 parent shape is ready for QA | Error | resolve_parent_payload_shape | The target is production, the request is not explicitly a controlled QA proof, or the immutable preview and approval are absent | Return CONTROLLED_VERIFICATION_REQUIRED; permit only an explicitly requested disposable nonproduction test after exact live-value, template, resolver, read-back, preview, and approval gates pass | Yes, before controlled nonproduction dispatch |
| Parent create is handed to Data Loader | Error | find_legislative_data_group | LegislativeDataGroupName is absent, or LegislativeDataGroupId or LegislationCode appears in the DAT | Re-resolve the selected LDG and author only its exact business name | Yes, before archive generation |
| Parent create is handed to Data Loader | Error | find_value_definition_group | ValueGroupName is absent or mismatched, or ValueGroupId appears in the DAT | Re-resolve the current-operation group and author only its exact business name | Yes, before archive generation |
| Parent create is handed to Data Loader | Error | find_calculation_type | CalculationTypeName is absent or mismatched, or CalcTypeId or CalculationTypeId appears in the DAT | Re-resolve the current-operation type and author only its exact business name | Yes, before archive generation |
| Parent create is handed to Data Loader | Error | | The DAT filename is not ValueDefinition.dat, the discriminator is not ValueDefinition, the row is not one MERGE, or it contains REST controls, surrogate IDs, Language, or SourceLang | Rebuild from the exact CVD-HDL04 profile | Yes, before preview |
| Parent create is handed to Data Loader | Error | | Live native HDL hierarchy, attributes, or UCM template was not refreshed, does not exactly match, or changed after archive generation | Stop and rebuild from current metadata | Yes, before preview |
| A CVD-HDL04 FM parent is planned | Error | find_database_item | The required database item does not resolve exactly, DatabaseItemId would be exposed/authored, DatabaseItemName is absent from the live template, or its REST read-back mapping is missing | Resolve the business item again and author only DatabaseItemName; otherwise keep the payload shape unresolved | Yes, before archive generation |
| CVD-HDL04 parent conditional fields are planned | Error | resolve_parent_payload_shape | A supplied field is forbidden by the resolved shape, a required field is missing, or an authored conditional field lacks current template support, a declared resolver where applicable, or an exact readable reconciliation mapping | Reject an inapplicable extra field or collect the missing business value. If evidence is insufficient, return PAYLOAD_SHAPE_UNRESOLVED; never silently remove or guess a requested value | Yes, before archive generation |
| A Create command shares an operation ID or business-value provenance with a prior run | Error | | The new operation inherited inputs, IDs, lookup results, defaults, drafts, payloads, archives, approvals, or receipts | Allocate a new operation ID, initialize empty collecting state, and resolve the current command independently | Yes, before any lookup or authoring |
| A Value Definition Group create is requested | Error | | The task has no released native HDL group-create profile | Return CVD_HDL_ROUTE_FROZEN; do not author an archive or ask for approval | No |
| A parent create plan lacks current-operation user-selection provenance for Value Definition Group, Calculation Type, or applicable Unit of Measure | Error | find_value_definition_group | A value was inherited or an unselected lookup result was used | Present complete in-scope choices and remain collecting until the user selects every unresolved value | Yes, before authoring |
| Parent create archive is handed off | Error | | Exact immutable preview, SHA-256, live validation, Task Hook validation, current approval, or exact read-back plan is missing | Complete the native HDL lifecycle gate first | Yes |
| A prior mutation outcome is unknown | Error | find_parent_definition | A replay is proposed before request and exact parent reconciliation | Reconcile first; never retry blindly | No |
| A mutation response is treated as completion | Error | | Data Loader detail status or exact parent read-back is missing or mismatched | Keep the operation in verification and do not replay | No |
| State or diagnostics are persisted | Error | | Password, token, cookie, authorization header, CSRF value, or raw secret is present | Remove secret material and retain only credential references/environment alias | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_legislative_data_group | Before any scoped read or mutation plan | LDG ID, Name, LegislationCode | ora_reference_lookups.md |
| find_calculation_type | Parent create and CVD-HDL11 calculation-value field enforcement | CalculationTypeId, exact current name, and semantic code when returned or resolved | ora_reference_lookups.md |
| resolve_parent_payload_shape | Standalone CVD-HDL04 after exact Calculation Type selection; finalize after exact UOM selection only when preliminary field-state evidence makes UOM applicable | Preliminary UOM applicability, semantic type, applicable unit when any, required/optional/forbidden parent fields, authored field set, resolver lineage, template fingerprint, and read-back mappings | ora_reference_lookups.md |
| find_unit_of_measure_code | Parent create and CVD-HDL11 parent-unit validation | UnitOfMeasure code and meaning | ora_reference_lookups.md |
| find_value_definition_group | Parent create | Existing ValueGroupId and Name | ora_reference_lookups.md |
| find_parent_definition | Exact reads, reconciliation, or Parent Correct/Update/Delete target validation | Effective slice, business identity, Type, every authored parent conditional field, IDs, child counts, links, and timeline state | ora_reference_lookups.md |
| find_range_item | Range Item target selection, validation, and reconciliation after the parent resolves | Range bounds, type-specific result slots, effective range, and internal child identity | ora_reference_lookups.md |
| extract_active_resource_links | GET navigation, reconciliation, and future native HDL investigation | Current item/collection links, opaque keys, physical effective range, retrieval time | ora_reference_lookups.md |
| find_database_item | CVD-HDL04 when its resolved shape requires a database item | Internal DatabaseItemId and business DatabaseItemName | ora_reference_lookups.md |
| find_currency | Parent create with an explicit currency, or Parent Correct/Update current/new Currency validation | CurrencyCode and Name | ora_reference_lookups.md |
| find_override_type | Read-only Allowed Override semantics or future native HDL investigation | Eligible OverrideType code and meaning | ora_reference_lookups.md |
| find_calculation_component | Read-only Override Usage semantics or future native HDL investigation | Component ID and owning card ID | ora_reference_lookups.md |
| find_table_value_set | Read-only Usage Rule semantics or future native HDL investigation | Code and TABLE validation type | ora_reference_lookups.md |
| find_override_usage_receipt | Read-only Override Usage reconciliation, including nested reads that return 404 with reconstructed ancestor keys | Exact usage ID, effective slice, owning Allowed Override, submitted historical values, and joined display values | ora_reference_lookups.md |

## Governed Write Sequence

Every supported mutation follows this order. Only upload and initiation are
writes; all earlier Fusion calls are read-only discovery or validation.

| Sequence | Stage | Required Result |
|---|---|---|
| 1 | Fresh operation state | Allocate a new operation ID and empty operation-local business state. |
| 2 | REST GET discovery | Resolve every user-facing choice in the selected environment and scope. |
| 3 | Target or duplicate check | Prove one eligible target or zero exact create duplicates, as required by the operation. |
| 4 | Live HDL template validation | Refresh the relevant native business object hierarchy, fields, and ValueDefinition.dat or RangeItemOverride.dat template through core/data-loader. |
| 5 | Deterministic DAT/ZIP generation | Construct from the exact operation-specific task-owned profile and validate the unuploaded archive. |
| 6 | Immutable preview and SHA-256 | Show business-facing values, row counts, expected effect, and the exact archive hash. |
| 7 | Standalone approval | Accept only the exact standalone approve bound to operation ID, environment, archive hash, and target fingerprint when applicable. |
| 8 | Pre-dispatch revalidation | Rehash the archive and refresh stale-sensitive target or duplicate evidence; invalidate approval on any change. |
| 9 | Data Loader upload | Upload the approved archive once and persist the receipt immediately. |
| 10 | Data Loader initiation | Initiate the uploaded request once and persist its request/process identifier immediately. |
| 11 | Automatic read-only polling | Poll the same request until terminal, then retrieve its detail result or log without requiring another user prompt. |
| 12 | Authoritative reconciliation | Run the operation-specific expanded parent GET and classify completion only when loader detail and read-back agree. |

Never replay upload or initiation after an uncertain response. Reconcile the
existing request by persisted identifiers and read-only history before another
write can be considered.

## Native HDL Mutation Handoff

For CVD-HDL04, return an operation plan containing:

- environment alias and resource path without credentials;
- operation and support status;
- proof that Calculation Type and every applicable Unit of Measure are exact
  current tenant LOV matches, including customer-defined labels and non-Money
  units when selected;
- the resolved `parentPayloadShape`, including semantic type,
  required/optional/forbidden fields, resolver lineage, current template
  fingerprint, exact authored field set, and readable mapping for every
  conditional field;
- effective start date and the open-ended native HDL create profile;
- native business object, `ValueDefinition.dat` filename, `ValueDefinition`
  discriminator, six fixed business fields, only the resolved conditional
  fields, and one parent row;
- proof that the DAT contains LegislativeDataGroupName, ValueGroupName, and
  CalculationTypeName and omits their surrogate IDs and LegislationCode;
- resolved business labels in both preview and DAT, with IDs retained only as
  internal read evidence;
- resolved references with source resolver and retrieval time;
- expected exact read-back for every authored conditional field;
- expected business effect and date-effective warning where applicable;
- archive SHA-256, idempotency key, reconciliation lookup, and expiry;
- a statement that no write has occurred and separate confirmation is required.

For CVD-HDL05, return the same environment, immutable hash, confirmation, and
reconciliation controls plus the exact parent and LDG labels, child Effective
Start Date, From, To, Flat Amount, zero-Range-Item baseline, lower-bound
duplicate proof, `ValueDefinition`/`RangeItem` schema fields, zero parent rows,
and one child row. Never expose or author parent or child IDs.

For CVD-HDL11, return the same controls plus the exact parent and LDG labels,
explicit Effective Start Date, From, To, exact current tenant Calculation Type
and applicable Unit of Measure, every input required by the resolved result
shape, proof of one unchanged baseline Range Item and zero other child
families, zero lower-bound matches, and zero type-comparable interval overlaps.
Delivered and customer-defined labels are equally eligible when their live
LOV rows and semantic payload shape resolve. Show one `RangeItemOverride.dat`
member, the fixed business keys and resolved result fields in current live
template order, one independent root `MERGE`, `SET PURGE_FUTURE_CHANGES Y`,
archive SHA-256, and the baseline fingerprint. Reconciliation requires loader
detail with one loaded and zero failed rows and one complete expanded parent
GET proving the unchanged parent and baseline, Range Item count `1 -> 2`,
exactly one requested open-ended row, every authored `Value1`/`Value2`/`Value3`
mapped type-aware to `RangeValueA`/`RangeValueB`/`RangeValueC`, every additional
authored result field matched through its predeclared expanded-read attribute,
and zero changes in other child counts. If any authored field has no readable
current mapping, the result shape is unresolved and cannot reach preview.

For CVD-HDL10, return the same controls plus the full parent business preview,
one derived same-start Range Item, zero-parent duplicate proof, both validated
template sections, one parent row, one child row, and zero other children. Use
the exact CVD-HDL10 profile in this resource and bind approval to the exact
archive SHA-256. Reconciliation must use one complete expanded parent
GET and prove the exact parent, exact Range Item, and zero other child rows.

For CVD-HDL09A, return the same operation-bound lifecycle controls plus a
business-facing preview containing the CVD-HDL09S-selected parent and LDG
labels, item physical start and end dates,
unchanged From and To, current and corrected Flat Amount, `SET
PURGE_FUTURE_CHANGES N`, zero parent rows, one `RangeItem` `MERGE`, archive
SHA-256, and target fingerprint. Bind approval to the operation ID, environment,
archive hash, and selected target. Immediately before dispatch, rehash the
archive and repeat the exact expanded parent GET and target selection; any
identity, date, bound, current amount, hash, or fingerprint change invalidates
approval. Reconciliation requires one successfully loaded Range Item with zero
failed rows and complete expanded parent GETs at the item start and following
day, proving the same physical range, unchanged From and To, the corrected Flat
Amount, and no timeline split. Keep every surrogate ID in machine evidence.

For CVD-HDL09B, return the same operation-bound lifecycle controls plus a
business-facing preview containing the CVD-HDL09S-selected parent and LDG
labels, current item physical range,
unchanged From and To, current Flat Amount, explicit later update boundary,
updated Flat Amount, `SET PURGE_FUTURE_CHANGES N`, zero parent rows, one
`RangeItem` `MERGE`, archive SHA-256, and target fingerprint. Bind approval to
the operation ID, environment, archive hash, selected target, and update
boundary. Immediately before dispatch, rehash the archive and repeat the exact
expanded parent GET and target selection; any target, boundary, hash, or
fingerprint change invalidates approval. Reconciliation requires one
successfully loaded Range Item with zero failed rows and complete expanded
parent GETs on the day before the boundary, the boundary, and the following
day. The old slice must retain the prior Flat Amount and end the day before the
boundary; the new slice must start on the boundary, remain open-ended, retain
From and To, and show the updated Flat Amount on both post-boundary reads. Keep
every surrogate ID in machine evidence.

For CVD-HDL09D, return the same operation-bound lifecycle controls plus the
selected Range Item business values, proof it is the sole open-ended Flat
Amount Range Item and that all other child counts are zero, one child
`DELETE`, archive SHA-256, and target fingerprint. Reconciliation must prove
the parent remains and Range Items are empty on the item start and following
day.

For CVD-HDL07A, return the same environment and lifecycle controls plus the
operation-bound CVD-HDL07S business target, unchanged physical range and
identity labels, current and corrected Currency labels, zero-child proof, the
exact `ValueDefinition` schema, `SET PURGE_FUTURE_CHANGES N`, one parent
`MERGE`, archive SHA-256, and selected-target fingerprint. Before dispatch,
rehash the archive and refresh the exact target; any mismatch invalidates
approval. Reconciliation requires exact expanded parent reads at the physical
start date and the following day. Keep every surrogate ID in machine evidence.

For CVD-HDL07B, return the same operation-bound target and lifecycle controls
plus the explicit later boundary, prior and new Currency labels, proof that the
target is open-ended and childless with no future slice, `SET
PURGE_FUTURE_CHANGES N`, one parent `MERGE`, archive SHA-256, and target
fingerprint. Reconciliation must prove the closed prior slice and the new
open-ended slice with complete expanded reads around the boundary.

For CVD-HDL07C, return the same operation-bound target and lifecycle controls
plus complete timeline provenance, proof of exactly one physical slice and zero
children, the exact complete physical range, one parent `DELETE`, archive
SHA-256, and a target-and-timeline fingerprint. Before dispatch, rehash the
archive and refresh both the target and timeline. Reconciliation requires one
successful loader Delete row and complete exact Name-and-LDG absence reads at
the former start date, following day, and a later date.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.ENFORCE_DESIGN | decision | 5 | design_enforcement | compliant->CVD.EXECUTION_GATE;noncompliant->CVD.HANDLE_ERROR | CVD.APPLY_DEFAULTS | stop | Dependencies, references, and defaults are ready for review |
