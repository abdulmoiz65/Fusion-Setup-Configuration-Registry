# Manage Departments Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_departments | A department list search, exact target lookup, or create uniqueness check is requested | Exact name or name fragment | /hcmRestApi/resources/{version}/departments | OrganizationId, business identity, effective range, current values, and item link | For a list search, pass q=Name like '%<name-fragment>%' and return every match. Matching is case-insensitive and substring-based. For read, edit, inactivate, or delete-effective-split, require one exact department. For create, require zero exact matches. | OrganizationId, effective range, current values, and item link | Return zero or all matches for a list search. For read, edit, inactivate, or delete-effective-split, stop on zero or multiple matches. For create, zero means the identity is available; one or more exact matches block the duplicate create. |
| resolve_department_delete_history | A delete-effective-split request or its verification is requested | Exact Department, retained EffectiveStartDate, and requested last deleted EffectiveEndDate | /hcmRestApi/resources/{version}:9/hcmDateEffectiveObjectHistory?fields=FirstSplitFlag,EffectiveStartDate,EffectiveEndDate&finder=findHistory;HistoryDefClassName=oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.DepartmentHistoryDef,PrimaryObjectId={OrganizationId} | FirstSplitFlag, EffectiveStartDate, and EffectiveEndDate | Require one logical Department. Confirm that the retained start is an existing row start, the requested end aligns to the end of an existing later row, and at least one later effective split is removed. After delete, require the deleted rows absent and all other rows unchanged except the predecessor end boundary. | Confirmed retained start, inclusive deletion end, preserved predecessor values, and before/after evidence | Stop on request failure, no later split, empty range, misaligned end, first-row deletion, ambiguity, or inconsistent verification |
| resolve_department_set | Create supplies a Department Set | SetId, SetCode, or SetName candidate | shared.validation.reference-data-validator | SetId, SetCode, and SetName | Require one internally consistent set tuple | SetId, SetCode, and SetName | Stop before preview when absent, ambiguous, or inconsistent |
| resolve_department_location | Create or edit supplies a Location | Exact LocationCode or normalized exact LocationName and Department effective date | /hcmRestApi/resources/{version}/locationsLov | LocationId, LocationName, LocationCode, TownOrCity, and CountryName | Read complete pages and require one active/effective exact match | LocationId and LocationCode; retain display fields for preview | Stop and request correction or prerequisite setup |
| resolve_department_action_reason | Create or edit supplies an Action Reason | Exact current code or meaning | Current describe-declared actionReasonsLOV | ActionReasonCode and ActionReasonId | Require one exact current match | ActionReasonCode and ActionReasonId | Stop before preview on zero or multiple matches |
| read_department_eff_context | A Department EFF context or segment is read or changed | Exact Department, effective date, and context or segment | Fresh link-bearing Department parent and DEPARTMENT envelope, current polymorphic describe, and returned context child link | Context and segment labels, business values, and row count | Require one exact parent and envelope and one describe-matched returned context link | Business-facing context values | Re-read in link-bearing form before treating a link as missing; never construct a path |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A Department EFF context or segment is requested | Read the exact parent and DEPARTMENT envelope without onlyData=true, resolve the context from current polymorphic describe, and follow the matching returned child link from links or @context.links. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Department history is requested | Execute the history finder once and evaluate its returned items; do not apply generic collection pagination. |
| A delete-effective-split request is resolved | Read the complete effective history needed to prove the retained start and inclusive deletion end; do not infer boundaries from a display name. |
| An eligible delete range is presented | Show Department name or code, status, retained effective start, and inclusive deletion end; state that complete deletion is unsupported. Keep FirstSplitFlag and internal identifiers hidden. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPT.READ | decision | 2 | reference_lookup | resolved->DEPT.HISTORY;create_available->DEPT.HISTORY;not_found->DEPT.ERROR;duplicate->DEPT.ERROR;ambiguous->DEPT.ERROR;failed->DEPT.ERROR | DEPT.VALIDATE | stop | Read is requested, an exact target is required before edit, inactivation, or delete-effective-split, or a uniqueness check is required before create |
| DEPT.HISTORY | decision | 3 | reference_lookup | eligible->DEPT.DEPENDENCIES;not_required->DEPT.DEPENDENCIES;first_row->DEPT.ERROR;missing->DEPT.ERROR;ambiguous->DEPT.ERROR;failed->DEPT.ERROR | DEPT.READ | stop | A delete-effective-split request is resolved after the exact Department is read |
