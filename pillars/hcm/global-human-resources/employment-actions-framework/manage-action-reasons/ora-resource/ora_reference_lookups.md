# Action Reason Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_action_reasons | A list search, exact target lookup, or create uniqueness check is requested | Reason Code, exact action-reason name, or user-supplied name fragment | /hcmRestApi/resources/{version}/hrActionReasons | Resolve exact names against ActionReason. For an explicitly requested contains search, use q=ActionReason like '%term%' and replace term with the escaped caller value; request reason identity, Reason Code, effective dates, and current association values. | Return all list matches. Require one exact action reason or association for read, edit, or delete, and zero exact Reason Code matches for create. | Resolved action-reason identity, effective context, and current values | Return zero or all matches for a list search. For read, edit, or delete, stop on zero or multiple exact matches. For create, one or more exact matches block duplicate creation. |
| resolve_action_reason_common_lookup | A configured lookup value is supplied | Lookup type, exact code or meaning, and effective date | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md) | Exact enabled LookupCode and Meaning | Require one compatible result; never select by position. | Registered-object-compatible stored value | Stop and request a more precise value. |
| resolve_action_reason_action | An action-reason usage association is supplied | Exact Action Code or action name and effective context | hrActions read resource | Action identity, Action Code, active state, and effective range | Require one current compatible Action. | Validated Action value | Stop on zero or multiple matches. |
| resolve_action_reason_country | Country is supplied or required | Country display name and effective context | shared.project-intake.country-localization-intake | Canonical country code | Require one resolved country; do not derive a code from display text. | Validated country code | Stop on zero or ambiguous matches. |
| resolve_action_reason_role | A role condition is supplied | Exact role display name | Current authorized role lookup | Active RoleCode and RoleName | Require one active exact RoleName match. | Transient RoleCode for the registered object | Stop on zero or multiple active matches. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.READ | decision | 3 | reference_lookup | resolved->AR.LOOKUPS;list_returned->AR.DEFAULTS;create_available->AR.LOOKUPS;not_found->AR.ERROR;duplicate->AR.ERROR;ambiguous->AR.ERROR;failed->AR.ERROR | AR.DEPENDENCIES | stop | Read is requested, an exact target is required before edit or delete, or a uniqueness check is required before create |
| AR.LOOKUPS | step | 4 | reference_lookup | resolved->AR.DEFAULTS;blocked->AR.ERROR | AR.READ | stop | A supplied action, country, role, or configured reference needs an exact stored value |
