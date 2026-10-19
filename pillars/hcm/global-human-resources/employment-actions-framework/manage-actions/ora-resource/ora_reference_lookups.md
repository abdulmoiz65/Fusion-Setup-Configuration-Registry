# Action Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_actions | A list search, exact target lookup, copy source, or create uniqueness check is requested | Action Code, exact action name, or user-supplied name fragment | /hcmRestApi/resources/{version}/hrActions; after one exact match, use its item read with current actionReasonUsages for full details | ActionCode, ActionName, Action Type, effective dates, item identity, and current association values | Use q=ActionCode='value' for a supplied code and q=ActionName='value' for a supplied display name. For an explicitly requested name contains search, use q=ActionName like '%term%' and replace term with the escaped caller value. Require one exact action for details, copy, edit, or delete; create requires zero exact ActionCode matches. | Resolved action identity, effective context, current parent values, and actionReasonUsages | Return zero or all matches for a list search. For an exact operation, stop on zero or multiple matches; for create, one or more exact code matches block creation. |
| resolve_action_common_lookup | An Action Type, Action Reason, assignment status, or configured lookup value is supplied | Lookup type, exact code or meaning, and effective date | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md) | Exact enabled LookupCode and Meaning | Require one compatible result; never select by position. | Registered-object-compatible stored value | Stop and request a more precise value. |
| resolve_action_country | Country is supplied or required | Country display name and effective context | shared.project-intake.country-localization-intake | Canonical country code | Require one resolved country; do not derive a code from display text. | Validated country code | Stop on zero or ambiguous matches. |
| resolve_action_role | An action-reason role mapping is supplied | Exact role display name | Current authorized role lookup | Active RoleCode and RoleName | Require one active exact RoleName match. | Transient RoleCode for the registered object | Stop on zero or multiple active matches. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACT.READ | decision | 3 | reference_lookup | resolved->ACT.LOOKUPS;list_returned->ACT.DEFAULTS;create_available->ACT.LOOKUPS;not_found->ACT.ERROR;duplicate->ACT.ERROR;ambiguous->ACT.ERROR;failed->ACT.ERROR | ACT.DEPENDENCIES | stop | Read is requested, an exact target is required before edit or delete, or a uniqueness check is required before create |
| ACT.LOOKUPS | step | 4 | reference_lookup | resolved->ACT.DEFAULTS;blocked->ACT.ERROR | ACT.READ | stop | A supplied action, country, role, or association reference needs an exact stored value |
