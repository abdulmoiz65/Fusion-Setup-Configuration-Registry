# Manage Person Types Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_system_person_type | A system person type name or code is supplied | Exact code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type SYSTEM_PERSON_TYPE | Enabled LookupCode and Meaning | Require one exact current code or meaning match; do not derive a code from the meaning. | LookupCode to SystemPersonType | Stop on zero or multiple exact matches. |
| find_manage_person_types | Read is requested, or an exact target is needed before create, edit, or delete | Resolved SystemPersonType, user type name, exact name, or caller-supplied name fragment | /hcmRestApi/resources/{version}/personTypes | SystemPersonType, UserPersonType, active state, and current-run-only PersonTypeId | Use q=SystemPersonType='code' for an exact resolved system code and q=UserPersonType='name' for an exact user name. For an explicitly requested contains search, use q=UserPersonType like '%term%' or q=SystemPersonType like '%term%' according to the supplied value kind; never derive term from a meaning. Evaluate bounded pages, then require exactly one row matching the complete paired business key for edit or delete. | Current person-type values and current-run-only identity | Return all matches for a read by system type; stop on zero or multiple exact targets for edit or delete. |
| resolve_person_type_active | Active is supplied | Exact code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type YES_NO | Enabled LookupCode and Meaning | Require one exact current code or meaning match | LookupCode to ActiveFlag | Stop on zero or multiple exact matches |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.READ | decision | 3 | reference_lookup | resolved->PT.DEFAULTS;list_returned->PT.DEFAULTS;not_found->PT.ERROR;ambiguous->PT.ERROR;failed->PT.ERROR | PT.DEPENDENCY | stop | Read is requested, or an exact target is required before create, edit, or delete |
