# Calculation Value Definitions Defaulting Rules

Defaults are applied only after validation, dependency resolution, and
reference lookup. Every applied default must be shown in the immutable mutation
preview. A user-supplied valid value always wins unless the row below explicitly
says otherwise.

The current mutation authority is native HDL only. CVD-HDL04 omits the parent
end date and both language fields, accepts every exact current tenant
Calculation Type and applicable Unit of Measure, and applies conditional-field
defaults only after its `parentPayloadShape` resolves. CVD-HDL10 retains its
Flat Amount/Money parent shape, defaults Base Name from Name when omitted, and
derives its one Range Item start date from the parent start date. CVD-HDL05
omits the child end date but does not default its Effective Start Date, From,
To, or Flat Amount. CVD-HDL11 also
omits the end date and does not default its Effective Start Date, From, To, or
calculation-result values. It derives the exact calculation-type label, LDG
name, parent name, and applicable unit from the fresh eligible-parent receipt,
then validates those business values against the current tenant lookups without
restricting them to Flat Amount or Money. CVD-HDL07A derives
the selected parent's identity and physical range from a fresh exact read and
requires an explicit corrected Currency. CVD-HDL07B also requires an explicit
new effective boundary and different Currency. CVD-HDL07C derives the complete
physical range from its eligible target and accepts no changed business value.
None of these lifecycle profiles defaults a changed business value.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| effectiveAsOfDate | Current target-session date in YYYY-MM-DD | The user did not provide an as-of date for search, read, or create | No | |
| EffectiveStartDate | effectiveAsOfDate | create_parent or create_parent_with_range_item and the user omitted the parent start date | No | |
| Range Item EffectiveStartDate | Parent EffectiveStartDate | CVD-HDL10 combined parent and Range Item create | Yes, because this exact profile requires the child and parent to start together | |
| EffectiveEndDate | Do not author; expect the service's open-ended result and display it as blank | CVD-HDL04 parent create, CVD-HDL10 combined parent and Range Item create, CVD-HDL05 Range Item create, CVD-HDL11 Range Item Override Create, CVD-HDL07A Parent Correct, or CVD-HDL07B Parent Update | Yes, because every executable shape begins open-ended; Parent Correct preserves the range and Parent Update lets Fusion split it at the explicit boundary | |
| EffectiveEndDate for Parent Delete | Exact physical end date from the approved CVD-HDL07S target | CVD-HDL07C Parent Delete | Yes, because it is target identity rather than a user-authored boundary | |
| groupMode | existing | create_parent and no group branch was chosen | No | |
| BaseName | Trimmed Name, limited by the validated 120-character maximum | create_parent or create_parent_with_range_item and BaseName is blank | No | |
| LegislationCode | The code returned for the selected Legislative Data Group, retained only as workflow/display and REST GET context | Any LDG-scoped operation | Yes, because it is derived from the selected LDG and omitted from native HDL rows | find_legislative_data_group |
| Country | LegislationCode for display and lookup context | Any LDG-scoped operation | Yes, because it is derived display context | find_legislative_data_group |
| CurrencyCode | First exact CurrencyCode returned by DefaultCurrencyVO for LegislationCode | CVD-HDL04 parentPayloadShape makes CurrencyCode applicable and CurrencyCode is blank, or the fixed CVD-HDL10 Flat Amount parent omits it | No | find_default_currency |
| Predefined | Do not author; display the service-returned value | Parent create | Yes, because it is service controlled | |
| REST-Framework-Version | 9 | A governed runbook prepares a request | Yes for this task contract | |
| Accept-Encoding | identity | A governed REST request is prepared | Yes for this task contract | |

## No-Default Fields

The agent must not invent values for CalculationTypeId, ValueGroupId,
UnitOfMeasure, CurrencyCode, DateMode, Periodicity, DatabaseItemId,
DatabaseItemName, ValueIdentifier,
OverrideType, Prompt, card, component, value set, range bounds, or calculation
result fields. These values must be supplied by the user or resolved through an
explicit lookup documented in `ora_reference_lookups.md`.

For `create_parent` or `create_parent_with_range_item`, lookup alone is not enough for Value Definition Group,
Calculation Type, or applicable Unit of Measure. Each must have an explicit
current-operation user selection. Values from a prior run, archive, project
artifact, recorded evidence, example, or a silently accepted single-candidate lookup are
not defaults and must not be reused.

## Default Application Rules

| Situation | What Happens |
|---|---|
| A new Create command begins | Allocate fresh operation state and recompute every applicable default. Never carry a default, resolved ID, selected value, payload, archive, fingerprint, approval, or receipt forward from another run. |
| A default depends on a failed or ambiguous lookup | Do not apply it; classify the operation as blocked. |
| A new parent omits Value Definition Group, Calculation Type, or applicable Unit of Measure | Do not default or inherit it. Run the complete read-only choice lookup, present the options, and remain in collecting until the user selects one. |
| A CVD-HDL04 parent Calculation Type or applicable Unit of Measure resolves exactly in the current tenant | Accept the selected value, including a customer-defined Calculation Type label or non-Money unit. Apply defaults only after parentPayloadShape identifies the required, optional, and forbidden fields, their resolver lineage, and their read-back mappings. A packaged-map omission is not an invalid value. |
| A CVD-HDL04 parentPayloadShape cannot be established from the exact live LOV row, current create semantics, live ValueDefinition.dat metadata/template, declared resolvers, and readable reconciliation mappings | Apply no shape-dependent default. Return PAYLOAD_SHAPE_UNRESOLVED and remain in collecting/preflight without authoring or guessing a DAT row. |
| A CVD-HDL10 parent type/unit is not exact Flat Amount (F) with Money (M), or an end date/type-specific field is supplied for that combined profile | Do not apply defaults to force the combined parent into the verified shape. Return CVD_HDL_ROUTE_FROZEN before archive authoring. This restriction does not apply to standalone CVD-HDL04 or CVD-HDL11. |
| A default changes after the target, LDG, calculation type, applicable Unit of Measure, or effective date changes | Invalidate the old value unless the user explicitly supplied it and it remains valid in the new context. A Calculation Type or UOM change also invalidates parentPayloadShape, authoredParentFields, parentReadbackMappings, every shape-dependent default, and the downstream DAT/archive fingerprint and approval. |
| The default currency is unavailable | If the finalized CVD-HDL04 parentPayloadShape requires CurrencyCode, remain in collecting until the user supplies an exact valid Currency; if it marks CurrencyCode optional, leave it blank and disclose that no default was found. The fixed CVD-HDL10 profile remains subject to its own required-field validation. |
| Open-ended parent state is represented | Render the end date as blank in the business preview and omit EffectiveEndDate from the DAT. Reconciliation may observe 4712-12-31 from Fusion. |
| A CVD-HDL05 Range Item create is requested | Require an explicit child Effective Start Date, From, To, and Flat Amount. Omit EffectiveEndDate, link by the parent business key, and do not add any REST or language field. |
| A CVD-HDL11 Range Item Override Create is requested | Require an explicit Effective Start Date, From, To, and every result value required by the parent's resolved calculation-type shape. Derive the exact Calculation Type name, Legislative Data Group name, Value Definition name, and applicable unit from the fresh eligible-parent receipt; validate the type and unit against current tenant lookups, but do not require a particular delivered or customer-defined value. Omit EffectiveEndDate and author exactly one independent-root row using only the live-template-supported result fields, with no REST, language, or COMMENT field. |
| A CVD-HDL10 combined parent and Range Item create is requested | Require explicit parent Effective Start Date, From, To, and Flat Amount. Default Base Name only when omitted, derive the child start from the parent start, author exactly one parent and one child, and omit both end dates. |
| A CVD-HDL07A Parent Correct is requested | Do not default the target or corrected Currency. Require explicit target selection and an explicit different Currency resolved through the current LOV. Derive unchanged identity, physical dates, group, type, and unit from the fresh target receipt. |
| A CVD-HDL07B Parent Update is requested | Do not default the target, new effective start date, or new Currency. Require explicit target selection, an explicit later ISO boundary, and an explicit different Currency resolved through the current LOV. Derive unchanged identity, baseline start, group, type, and unit from the fresh target receipt. |
| A CVD-HDL07C Parent Delete is requested | Do not default the target or either physical date. Require explicit target selection, derive the exact start/end range from the fresh target receipt, and require complete evidence of zero children and exactly one physical slice. |
| An Allowed Override or Override Usage create is requested | Do not apply historical registered-BO controls or construct an archive. the registered-BO child-write boundary is non-authorizing; return CVD_HDL_ROUTE_FROZEN. |
| Another unsupported child create is requested | Do not apply historical REST defaults or construct an archive. Return CVD_HDL_ROUTE_FROZEN. |
| A child lifecycle mutation outside CVD-HDL09A, CVD-HDL09B, or CVD-HDL09D is requested | Do not apply historical REST defaults or construct an archive. Return CVD_HDL_ROUTE_FROZEN. |
| An unsupported parent or child lifecycle operation, or a Parent Correct/Update/Delete outside its exact released profile, is requested | Do not default RestAction, effectiveOf, RangeMode, an action verb, a key, or a row shape from historical REST. Return CVD_HDL_ROUTE_FROZEN. |
| A native HDL parent, Range Item, or Range Item Override row is authored | Use delivered business-key labels. Never copy the historical registered-BO ID-only shape into native HDL. |
| A default is applied to a mutation plan | Recompute the plan fingerprint and require confirmation of the resulting preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CVD.APPLY_DEFAULTS | decision | 4 | apply_default | applied->CVD.ENFORCE_DESIGN;not_required->CVD.ENFORCE_DESIGN;invalid->CVD.HANDLE_ERROR | CVD.RESOLVE_REFERENCES | stop | Input, dependencies, and required references are ready |
