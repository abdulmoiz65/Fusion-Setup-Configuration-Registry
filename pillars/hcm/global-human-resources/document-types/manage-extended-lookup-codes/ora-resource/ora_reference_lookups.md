# Manage Extended Lookup Codes Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_extended_lookup_codes | A list search, exact target lookup, or create uniqueness check is requested | LookupType, LookupCode, ExtendedLookupCode, exact ExtendedLookupName, explicit legislation scope, requested count, or user-supplied name fragment | /hcmRestApi/resources/{version}/hcmExtendedLookupCodes | Apply supplied LookupType, LookupCode, and LegislationCode context. Resolve exact names against ExtendedLookupName; for an explicitly requested contains search, use q=ExtendedLookupName like '%term%' and replace term with the escaped caller value. Group translated projections by runtime identity before applying a requested count. | Require one exact complete code tuple for read, edit, or delete, and zero exact tuple matches for create. For a requested count, continue bounded pages until that many unique records are collected or no more rows exist. | Resolved business identity, effective context, current values, and current-run-only item identity when available | Return zero or all matches for a list search. If fewer than the requested count exist, return them and state that the result is exhausted. For exact operations, apply the declared cardinality rule. |
| resolve_extended_lookup_parent_scope | Create or edit supplies a parent lookup type or code | Supplied Lookup Type/Code values, which may be UI meanings, plus requested legislation display value or code | Resolve the Common Lookup Type by exact `Meaning` when the supplied type is not a stored `LookupType`; resolve the child Lookup Code by exact `Meaning` when the supplied code is not a stored `LookupCode`; then query `/hcmRestApi/resources/{version}/hcmExtendedLookupCodes` for the resolved stored tuple | Stored parent LookupType, LookupCode, LegislationCode, enabled state, and effective range | Require one enabled current Common Lookup code and one compatible resolved tuple. Use its exact LegislationCode; blank is global, while a nonblank code is legislation-specific. | Stored parent codes and validated legislation scope | Stop on zero or multiple exact display-meaning matches. Do not send the display word `Global`; use the resolved blank value for global. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection count is requested | Follow bounded pages, group by runtime identity, and apply the count only after grouping; stop at the requested count or exhaustion. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.READ | decision | 3 | reference_lookup | resolved->XLOOK.DEFAULTS;list_returned->XLOOK.DEFAULTS;create_available->XLOOK.DEFAULTS;not_found->XLOOK.ERROR;duplicate->XLOOK.ERROR;ambiguous->XLOOK.ERROR;failed->XLOOK.ERROR | XLOOK.DEPENDENCY | stop | Read is requested, an exact target is required before edit or delete, or a uniqueness check is required before create |
