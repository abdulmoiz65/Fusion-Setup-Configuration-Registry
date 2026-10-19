# Manage Position Trees Defaulting Rules

## Purpose

Defines creation-only defaults and existing-version preservation rules for Position Tree versions.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied | Preserve the supplied value | preserved |
| 2 | An existing version is changed and a field is omitted | Preserve the freshly read current value | preserved |
| 3 | A new version omits EffectiveEndDate | Bind `4712-12-31` internally | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | Current version identity or required date evidence is unresolved | Apply no value and stop | blocked |

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| EffectiveEndDate | `4712-12-31` | A new Position Tree version omits the end date | Yes |  | Block if the resulting interval is invalid |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Existing-version field | A version update omits the field | Preserve the freshly read current value; never apply a creation default | preserved |
| Existing version identity | A version is updated | Resolve and preserve the exact Draft version identity; never substitute a version name | preserved |
| Explicit end date | A version update supplies EffectiveEndDate | Preserve and validate the supplied date against the current start date | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSTREE.DEFAULTS | decision | 4 | apply_default | applied->POSTREE.DESIGN;preserved->POSTREE.DESIGN;not_required->POSTREE.DESIGN;blocked->POSTREE.ERROR | POSTREE.RESOLVE_MEMBERS | stop | After member resolution and before design enforcement |
