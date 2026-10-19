# Manage Extended Lookup Codes Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Extended Lookup Codes. This file does not own input validation, lookup
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
| LegislationCode | Exact parent LegislationCode; Blank means global | Create or edit supplies an exact parent LookupType and LookupCode | No | resolve_extended_lookup_parent_scope | Block when the parent tuple is missing or ambiguous; Never send the display word `Global` |
| SourceSystemOwner | FDOS | A base create omits both source-key values | Yes, only as part of a complete validated pair |  | Block if only one caller value is supplied or owner provenance is unvalidated |
| SourceSystemId | FDOS_XLOOK_ plus the first 32 uppercase SHA-256 hexadecimal characters of the UTF-8 compact JSON array [LookupType,LookupCode,LegislationCode-or-GLOBAL,ExtendedLookupCode] | A base create omits both source-key values | Yes, only as part of a complete validated pair |  | Block if the resolved business key is incomplete or the generated value fails live schema validation |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Operation | A mutation is not explicit | Do not infer it; exploratory intent may remain read-only | not_required |
| Create source | A create source is prepared | Use the current live-validated Core Data Loader XLSX source; DAT conversion remains internal | preserved |
| Base-create source identity | A base ExtendedLookupCode create XLSX is prepared | Preserve a complete validated caller pair or apply the deterministic FDOS pair; never omit both source-key columns | preserved |
| Edit source and omitted value | An edit omits an existing value | Use the reviewed current XLSX source and preserve the fresh value | preserved |
| Runtime ID or fingerprint | A current value resolves or regenerates successfully | Preserve it only for the current run; never reuse a prior value | preserved |
| Runtime ID or fingerprint | Current resolution or regeneration fails | Apply no value and stop | blocked |
| Approval | Exact current approval is present | Preserve it only for the approved immutable preview | preserved |
| Approval | Exact current approval is absent | Never infer it from authentication or prior activity | blocked |
| Contract mismatch | Metadata, source, or reference data differs from this contract | Stop and report the gap; do not invent a mapping | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.DEFAULTS | decision | 4 | apply_default | applied->XLOOK.ENFORCE;preserved->XLOOK.ENFORCE;not_required->XLOOK.ENFORCE;blocked->XLOOK.ERROR | XLOOK.READ | stop | After validation, current-state reads, and required resolvers are complete |
