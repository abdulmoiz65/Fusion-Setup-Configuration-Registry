# Manage Lifecycle Phases Defaulting Rules

## Defaulting Rules

| Task Code | Task Name | Business Value | Implementation Field Name If Known | Default | Applies When | Can User Override? | Why This Default Is Safe | Resolver |
|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase sequence | PhaseSeq | Using the required fresh live baseline, assign the lowest whole number from 20 through 999 whose `(PhaseSeq, resolved PhaseType)` pair is absent from that export and already allocated input rows; continue the ascending scan for additional rows of the same PhaseType. Never propose a generic sequence. | PhaseSeq is not provided | Yes | The live baseline and same-type pair check prevent collisions at import. | find_exported_lifecycle_phase_sequence_type_pairs |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase code | PhaseCode | Split PhaseName into alphanumeric tokens. For each token, use its first three letters plus any trailing digits, uppercase the fragments, and join them with underscores (for example, `Engineering Phase 2` becomes `ENG_PHA_2`). Check the fresh live baseline and current input case-insensitively; on a derived collision append `_2`, `_3`, and so on, shortening the base before the suffix as needed to remain within 30 characters. | PhaseCode is not provided and PhaseName is provided | Yes | This deterministic compact code is validated against current live data and allocates a unique bounded alternative only for a derived collision. | find_exported_lifecycle_phase_codes |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase name | PhaseName | Use PhaseCode as provided | PhaseName is not provided and PhaseCode is provided | Yes | The requested derivation preserves the provided PhaseCode verbatim | |
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | Lifecycle phase type | PhaseType | Use the LookupCode returned by the EGP_LIFECYCLE_PHASES standard lookup | A valid PhaseType code or meaning resolves through the standard lookup | No | The lookup is the authoritative source for valid PhaseType values | find_lifecycle_phase_type_standard_lookup |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_LIFECYCLE_PHASES | Manage Lifecycle Phases | LCP.DEFAULT_MISSING_VALUES | step | 4 | apply_default | applied->LCP.VALIDATE_FINAL_VALUES;invalid->RETURN_ISSUES | LCP.FETCH_LIVE_SEQUENCE_BASELINE | stop | A Manage Lifecycle Phases import is requested |
# Manage Default Item Class Defaulting Rules

## Defaulting Rules

| Task Code | Task Name | Business Value | Implementation Field Name If Known | Default | Applies When | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Item class code | ItemClassCode | ROOT_ICC | Always for this task | No | This task manages the default root item class, and the supplied task rule requires ROOT_ICC. |
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | Item entity name | EntityName | ITEM_ENTITY | Always for this task | No | The supplied task rule requires ITEM_ENTITY as the default EntityName value. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| EGP_MANAGE_DEFAULT_ITEM_CLASS | Manage Default Item Class | DIC.APPLY_ROOT_ITEM_CLASS | step | 3 | apply_default | applied->DIC.PREPARE_IMPORT_DATA | DIC.CHECK_FSM_TEMPLATE | stop | A Manage Default Item Class import is requested |
