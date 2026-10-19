# Configure Seniority Dates Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Configure Seniority Dates. This file does not own input validation, lookup
mechanics, design policy, payload construction, or execution routing.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and user override is allowed | Preserve the supplied value | preserved |
| 2 | An edit omits a field that must retain its current value | Preserve the freshly read current value | preserved |
| 3 | Exactly one Standard Defaults row applies | Apply that default | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | A required resolver is unresolved, ambiguous, or failed | Apply no value and stop | blocked |
| 6 | Multiple conflicting default rows apply to the same field | Apply no value and stop | blocked |
| 7 | A supplied value conflicts with a non-overridable default | Apply no value and stop | blocked |

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| Active | Y | Create omits Active | Yes | resolve_seniority_active | Block when the explicit or default value cannot resolve exactly |
| Display flag | N | Create omits the display flag | Yes | resolve_seniority_display_in_ui | Block when the explicit or default value cannot resolve exactly |
| Allow Edit | Y | Create omits Allow Edit | Yes | resolve_seniority_allow_edit | Block when the explicit or default value cannot resolve exactly |
| Cumulative | N | Create omits Cumulative | Yes | resolve_seniority_cumulative | Block when the explicit or default value cannot resolve exactly |
| Scope | No restriction | Create omits all scope selectors | Yes | validate_scope_no_restriction | Preserve blank worker type, country, legal employer, union, and collective agreement fields |
| Seniority calculation basis | ORA_PER_SNDT_EITHER | Create omits the basis | No | resolve_seniority_basis | Derive only from the current template; reject user-supplied values |
| Standard time conversion | 8 hours/day, 173.3 hours/month, and 2080 hours/year | Create omits time-conversion values | No |  | Derive only from the current template; reject user-supplied values |
| Record Creator | FDOS | Create omits Record Creator and the current template exposes the field | Yes |  | Block when the template does not support the field or a supplied override is invalid |
| Seniority formula and override | Blank | Create omits formula and override | No |  | Keep read-only; reject create or update requests for formula values |
| Country selection | Blank LegislationCode | Create has no country selection | Yes |  | Do not infer country from another scope selector |
| Technical configuration fields | Approved triggering-field map below | Create after TriggeringField resolution | No | derive_seniority_configuration_tuple | Block when a required map member is absent, unsupported, or conflicts with current template/schema evidence |
| SeniorityVersion | V3 | Create template exposes SeniorityVersion | No | derive_seniority_configuration_tuple | Block when current metadata rejects V3; omit the field when absent |
| RestAction | Exact value from the current operation-specific Data Loader template | Every mutation | No |  | Block and regenerate validation when the operation or template changes |

## Approved Level and Triggering-Field Defaults

Apply these task defaults only after the current operation-specific create
template confirms the field exists and accepts the value. They are the
authoritative task mapping for tuple derivation; do not replace them with a
value copied from an existing rule.

| Condition | LevelCode default |
|---|---|
| Any assignment-level seniority | `ORA_A` |
| Any work-relationship-level seniority | `ORA_WR` |
| Any person-level seniority | `ORA_P` |

`LevelCode` identifies the Work Relationship, Assignment, or Person level at which the user configures the seniority date. `Object` is independent of that selection: it identifies the business object/table that owns the triggering field. Derive `Object`, `SourceField`, and `TriggeringFieldType` only from the authoritative triggering-field map; do not infer them from `LevelCode`. In particular, `Object=ORA_WR` denotes the Work Relationship data object and must not override a separately selected seniority level.

| TriggeringField | TriggeringFieldType | Object | SourceField |
|---|---|---|---|
| ORA_COL_AGR | NUMBER | ORA_A | ORA_FASD |
| ORA_DEPT | NUMBER | ORA_A | ORA_FASD |
| ORA_GRADE | NUMBER | ORA_A | ORA_FASD |
| ORA_GRADE_STEP | NUMBER | ORA_A | ORA_FASD |
| ORA_BU | NUMBER | ORA_A | ORA_FASD |
| ORA_POSITION | NUMBER | ORA_A | ORA_FASD |
| ORA_UNION_ID | NUMBER | ORA_A | ORA_FASD |
| ORA_JOB | NUMBER | ORA_A | ORA_FASD |
| ORA_BARG_UNIT | TEXT | ORA_A | ORA_FASD |
| ORA_LOC | NUMBER | ORA_A | ORA_FASD |
| ORA_EMP_CAT | TEXT | ORA_A | ORA_FASD |
| ORA_LEMP | NUMBER | ORA_WR | ORA_FWRSD |
| ORA_ENT | NUMBER | ORA_WR | ORA_FWRSD |
| ORA_LEG | TEXT | ORA_A | ORA_FASD |

## Preservation and No-Default Rules

### Field ownership and supported changes

Users may set or update `Active` and `Display in UI` when the current template supports them. `Object`, `SourceField`, `TriggeringFieldType`, `SetupSeniorityBasis`, Hours per Day, Hours per Month, Hours per Year, and Seniority Fast Formula are system-owned: derive them only from the current create template or preserve their fresh current values on update. Never accept user input to create or update them.

Worker Type, Country, Legal Employer, Union, and Collective Agreement are unsupported scope attributes for this Data Loader route: its DAT payload cannot serialize the required array values. Show their current values when requested, but do not offer, accept, or generate creates, updates, additions, removals, or scope-filter changes for them. Create requests default to `No restriction` for these dimensions.

For an unrestricted create, treat `Scope: No restriction` only as a control input: remove it before source generation, reject every scope-selector column and caller-supplied `RestAction` or system-owned field, then derive the technical tuple and create defaults from this document's approved mapping.

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value | Preserve the fresh current value | preserved |
| Worker-type edit | An edit supplies additions or removals | Preserve current members and apply only the requested delta | preserved |
| Operation, seniority-date code, identity, date, scope, worker type, or approval | The value is omitted | Never infer or default it | not_required |
| Create Cumulative | The value is omitted | Apply `N` after exact YES_NO validation | applied |
| Create Allow Edit | The value is omitted | Apply `Y` after exact YES_NO validation | applied |
| Create Active | The value is omitted | Apply `Y` after exact YES_NO validation | applied |
| Create Display in Guided Flows | The value is omitted | Apply `N` after exact YES_NO validation | applied |
| Create scope | Scope selectors are omitted | Apply `No restriction`; preserve blank worker type, country, legal employer, union, and collective agreement fields | applied |
| Incomplete create intake | Rule code, Attribute, or Level is missing | Stop before lookup, compatibility, uniqueness, technical-tuple, source, or preview work; ask once for exactly the missing inputs | blocked |
| `No restriction` | Create scope is explicit or defaulted unrestricted scope | Preserve blank worker type, country, legal employer, union, and collective agreement fields | preserved |
| Optional or absent technical field | The current operation-specific create template does not expose the field | Omit the field; do not emit an unsupported task default | preserved |
| Registered-object mismatch | The Data Loader object does not support a proposed default | Stop and do not substitute another value | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEN.DEFAULTS | decision | 5 | apply_default | applied->SEN.ENFORCE;preserved->SEN.ENFORCE;not_required->SEN.ENFORCE;blocked->SEN.ERROR | SEN.READ | stop | After validation, current-state reads, and required resolvers are complete |
