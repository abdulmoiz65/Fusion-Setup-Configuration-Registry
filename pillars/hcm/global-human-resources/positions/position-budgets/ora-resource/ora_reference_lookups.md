# Position Budgets Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_position_budget_profile | Before Position Budget create or edit | ProfileOptionCode=ORA_PER_POSITION_BUDGETING_ENABLED | Invoke hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values to read the current profile option value | Current profile option value | Exactly one resolved value | Y permits create or edit | N, no match, ambiguity, or a read failure blocks create or edit; do not use an alternate route |
| resolve_enterprise_allocate_by | After the profile gate and before Position Budget create or edit | Enterprise Position Budget Configuration context | Invoke hcm.global-human-resources.enterprise.manage-enterprise-hcm-information to read the exact link-bearing Enterprise and ENTERPRISE envelope, resolve the context from current polymorphic describe, and follow its returned child link | Current AllocateBy value | Exactly one supported nonblank value | Department, Location, or Department and Location | Blank, unsupported, no match, ambiguity, or a read failure blocks create or edit |
| read_position_budget | Before read, edit, delete, or create uniqueness validation | User-supplied Name, Code, selected result, or search text | Search: GET /hcmRestApi/resources/{version}/positionBudgets with `q=Name='<escaped value>'` or `q=Code='<escaped value>'`; selected item: returned item link or GET /hcmRestApi/resources/{version}/positionBudgets/{PositionBudgetId} | Name, Code, BudgetPeriodStartYear, DepartmentId, LocationId, AllocatedHeadcount, AllocatedFTE, and AllocatedAmount | Query the supplied Name or Code and return bounded candidates. For create, query Name and Code separately and require zero exact matches for both; require one exact refreshed item for read, edit, or delete. | Candidate details, create availability, or one refreshed current Position Budget | Block a duplicate create; for an exact target stop on zero or multiple matches |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| Position Budgets are searched by name or code | Use a bounded collection GET with `q=Name='<escaped value>'` or `q=Code='<escaped value>'`; do not use `findByAdvancedSearchQuery`. |
| One search result is selected | Refresh it through its returned item link or PositionBudgetId item path before edit, delete, or detail display. |
| Enterprise Position Budget Configuration is read | Do not use `onlyData=true`; follow the describe-matched child link returned in `links` or `@context.links` and never construct its path. |
| A profile option value change is requested | Route the change to hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values outside this lookup, then rerun resolve_position_budget_profile. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PB.READ_POSITION_BUDGET | decision | 10 | reference_lookup | resolved->PB.VERIFY_PROFILE;list_returned->PB.VERIFY_PROFILE;create_available->PB.VERIFY_PROFILE;blocked->PB.ERROR;failed->PB.ERROR | PB.VALIDATE | stop | A Position Budget read, edit, delete, or create uniqueness check is requested |
