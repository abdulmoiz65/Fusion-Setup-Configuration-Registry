# Defaulting Rules

## Standard Defaults

| Field | Internal | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|
| SegmentNDescription | No | Human-readable sentence-case form of the corresponding SegmentN value | The labelled segment value is confirmed absent from its resolved value set and its description is blank | No | resolve_asset_key_segment_values |
| StructureInstanceCode / underlying StructureInstanceNumber | Yes | Preserve the System Controls-selected AssetStructureInstanceCode in the FSM contract's StructureInstanceCode field. Fusion resolves the underlying number; never derive it from optional StructureInstanceIdentifier. Require a verified numeric source only for a contract that requires the number. | New Asset Key | No | resolve_asset_key_system_control |
| SummaryFlag | No | N | New Asset Key | No | |
| EnabledFlag | No | Preserve supplied Yes/Y as Y or No/N as N; obtain the choice when omitted for create, and preserve existing state for an explicitly selected update | Create or update | No | |
| StartDateActive / EndDateActive | No | Blank on create when omitted; preserve existing dates for an explicitly selected update unless a change or clearing is requested | Create or update | No | |
| ObjectVersionNumber | Yes | 1 | Insert | No | |
| Audit fields | Yes | Fusion audit framework values | Insert or update | No | |

## Default Safety Rules

| Situation | What Happens |
|---|---|
| Structure metadata or a segment default is needed | Resolve it from the target environment's active KEY# structure. Do not use a checked-in structure code, delimiter, or segment value as a default. |
| Enabled was omitted for a new Asset Key | Obtain the desired enabled state before artifact creation; do not infer an undefined runtime default. |
| A Create request matches an existing exact key | Do not default, preserve, or alter EnabledFlag, StartDateActive, or EndDateActive. Stop for an explicit update-versus-new decision. |
| System Controls has no row | Stop. Do not default an AssetStructureInstanceCode or substitute an alternate KEY# structure. |
| A defaulting decision depends on controlled-configuration behavior | Resolve the exact per-code result through `resolve_asset_key_controlled_configurations`; do not infer behavior or treat an unverified result as a default. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---:|---:|---|---|---|---|---|
| MAK.APPLY_DEFAULTS | step | 40 | apply_default | applied->MAK.ENFORCE_DESIGN | MAK.RESOLVE_OPERATION | stop | Resolved records contain defaultable technical fields. |
