# Manage Divisions Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_divisions | A list search, exact target lookup, or create uniqueness check is requested | Exact Name or user-supplied name fragment; use today's date for delete-effective-split | /hcmRestApi/resources/{version}/divisions; delete-effective-split uses effectiveDate={today} | OrganizationId, Name, ClassificationCode, Status, EffectiveStartDate, EffectiveEndDate, and item link | For a name-fragment list search, pass q=Name like '%<name-fragment>%' and return every match. Require one exact Name for read, edit, inactivate, or delete-effective-split, and zero exact Name matches for create. | Resolved OrganizationId, business identity, effective context, current values, and item link when available | Return zero or all matches for a list search. For read, edit, inactivate, or delete-effective-split, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches block duplicate creation. |
| resolve_division_delete_history | Future date-effective split deletion or its verification is requested | Fresh OrganizationId and complete Division history | /hcmRestApi/resources/{version}:9/hcmDateEffectiveObjectHistory?fields=FirstSplitFlag,EffectiveStartDate,EffectiveEndDate&finder=findHistory;HistoryDefClassName=oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.DivisionHistoryDef,PrimaryObjectId={OrganizationId} | FirstSplitFlag, EffectiveStartDate, and EffectiveEndDate | Confirm the retained start is an existing row start, the requested deletion end aligns to the final adjacent future split, and the predecessor is not the first row to remove. After delete, require deleted split rows absent and all retained rows unchanged except the predecessor end boundary. | Confirmed retained start, inclusive deletion end, and before/after evidence | Stop on request failure, no later split, empty or misaligned range, first-row deletion, ambiguity, or inconsistent verification |
| resolve_division_eff_context | A Division EFF context or segment is requested or supplied | `HCM_DIVISION` and context or segment business wording | Current HCM_DIVISION polymorphic describe | Context code and label, segment name and label, target attribute, native type, cardinality, and value-set contract | Require one exact context and segment belonging to that context | Resolved context and segment contract | Stop on zero or multiple matches; do not guess |
| read_division_eff_context | An existing Division EFF context or segment is read or edited | Exact Division, effective date, and context or segment | Fresh link-bearing parent and HCM_DIVISION envelope, current polymorphic describe, and returned context child link | Context and segment labels, business values, and row count | Require one exact parent and envelope and one describe-matched returned context link | Business-facing context values | Re-read in link-bearing form before treating a link as missing; never construct a path |
| resolve_division_eff_segment_value | A supplied Division EFF segment declares a value set | Proposed value and resolved segment contract | Describe-declared LOV resource and parameters; use a fresh returned runtime URL only when provided | Lookup value, display value, target attribute, and native type | Require one value-set match through the declared lookup or display attribute | Typed stored value for the declared target attribute | Stop on zero or multiple matches, type mismatch, or target mismatch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A general reference value or lookup code is required | Route resolution to hcm.global-human-resources.global-human-resources-common.manage-common-lookups unless the Division EFF segment declares its own value-set contract. |
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A Division EFF context or segment is requested | Resolve it from current HCM_DIVISION polymorphic describe. For an existing Division, read the exact parent and envelope without `onlyData=true` and follow the matching returned child link from `links` or `@context.links`. |
| A supplied Division EFF segment declares a value set | Use only its describe-declared LOV contract; retain the display value for preview and write the typed stored value to the declared target attribute. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Division history is requested | Execute the history finder once and evaluate its returned items; do not apply generic collection pagination. |
| An eligible split deletion range is presented | Show Division name, status, retained predecessor period, and future range to remove; state that logical-record deletion is unsupported and offer only the bounded split deletion. Keep FirstSplitFlag and internal identifiers hidden. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DIV.READ | decision | 2 | reference_lookup | resolved->DIV.CONTEXT;list_returned->DIV.CONTEXT;create_available->DIV.CONTEXT;delete_resolved->DIV.HISTORY;not_found->DIV.ERROR;duplicate->DIV.ERROR;ambiguous->DIV.ERROR;failed->DIV.ERROR | DIV.VALIDATE | stop | Read or list is requested, an exact target is required before edit, inactivate, or delete-effective-split, or a uniqueness check is required before create |
| DIV.HISTORY | decision | 3 | reference_lookup | eligible->DIV.CONTEXT;not_required->DIV.CONTEXT;first_row->DIV.ERROR;missing->DIV.ERROR;ambiguous->DIV.ERROR;failed->DIV.ERROR | DIV.READ | stop | delete-effective-split is requested after the current Division is read using today's effective date |
| DIV.CONTEXT | decision | 4 | reference_lookup | resolved->DIV.VALUESET;not_required->DIV.VALUESET;ambiguous->DIV.ERROR;failed->DIV.ERROR | DIV.READ | stop | A Division EFF context or segment is requested or supplied |
| DIV.VALUESET | decision | 5 | reference_lookup | valid->DIV.DEPENDENCIES;not_required->DIV.DEPENDENCIES;invalid->DIV.ERROR;failed->DIV.ERROR | DIV.CONTEXT | stop | A supplied Division EFF segment declares a value set |
