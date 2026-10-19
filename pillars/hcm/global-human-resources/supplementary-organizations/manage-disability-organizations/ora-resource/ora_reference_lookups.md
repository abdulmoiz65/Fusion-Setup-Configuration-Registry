# Manage Disability Organizations Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_disability_organizations | A list search, exact target lookup, or create uniqueness check is requested | OrganizationId, exact Name, or user-supplied name fragment; use today's date for delete | /hcmRestApi/resources/{version}/disabilityOrganizations; delete uses effectiveDate={today} | OrganizationId, Name, EffectiveStartDate, EffectiveEndDate, and item link | For a name-fragment list search, pass q=Name like '%<name-fragment>%' and return every match. Require one exact OrganizationId or Name for read, edit, or delete, and zero exact name matches for create. | Resolved business identity, effective context, current values, and item link when available | Return zero or all matches for a list search. For read, edit, or delete, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches block duplicate creation. |
| resolve_disability_organization_delete_history | Date-effective delete or its verification is requested | Fresh OrganizationId and current effective range | /hcmRestApi/resources/{version}:9/hcmDateEffectiveObjectHistory?fields=FirstSplitFlag,EffectiveStartDate,EffectiveEndDate&finder=findHistory;HistoryDefClassName=oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.DisabilityOrganizationHistoryDef,PrimaryObjectId={OrganizationId} | FirstSplitFlag, EffectiveStartDate, and EffectiveEndDate | Evaluate returned items; before delete, match one current row; after delete, require it absent and all other rows unchanged except the preceding end boundary | Selected row dates, internal eligibility, and before/after evidence | Stop on request failure, no exact row, ambiguity, or inconsistent verification |
| resolve_disability_organization_eff_context | A Disability Organization EFF context or segment is requested or supplied | HCM_DISABILITY_ORGANIZATION and context or segment business wording | Current HCM_DISABILITY_ORGANIZATION polymorphic describe | Context code and label, segment name and label, target attribute, native type, cardinality, and value-set contract | Require one exact context and segment belonging to that context | Resolved context and segment contract | Stop on zero or multiple matches; do not guess |
| read_disability_organization_eff_context | An existing Disability Organization EFF context or segment is read or edited | Exact organization, effective date, and context or segment | Fresh link-bearing parent and HCM_DISABILITY_ORGANIZATION envelope, current polymorphic describe, and returned context child link | Context and segment labels, business values, and row count | Require one exact parent and envelope and one describe-matched returned context link | Business-facing context values | Re-read in link-bearing form before treating a link as missing; never construct a path |
| resolve_disability_organization_eff_segment_value | A supplied Disability Organization EFF segment declares a value set | Proposed value and resolved segment contract | Describe-declared LOV resource and parameters; use a fresh returned runtime URL only when provided | Lookup value, display value, target attribute, and native type | Require one value-set match through the declared lookup or display attribute | Typed stored value for the declared target attribute | Stop on zero or multiple matches, type mismatch, or target mismatch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A general reference value or lookup code is required | Route resolution to hcm.global-human-resources.global-human-resources-common.manage-common-lookups unless the Disability Organization EFF segment declares its own value-set contract. |
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A Disability Organization EFF context or segment is requested | Resolve it from current HCM_DISABILITY_ORGANIZATION polymorphic describe. For an existing organization, read the exact parent and envelope without `onlyData=true` and follow the matching returned child link from `links` or `@context.links`. |
| A supplied Disability Organization EFF segment declares a value set | Use only its describe-declared LOV contract; retain the display value for preview and write the typed stored value to the declared target attribute. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Disability Organization history is requested | Execute the history finder once and evaluate its returned items; do not apply generic collection pagination. |
| An eligible delete row is presented | Show organization name, status, and effective period; state that complete deletion is unsupported and offer date-effective deletion of this row. Keep FirstSplitFlag and internal identifiers hidden. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DISORG.READ | decision | 2 | reference_lookup | resolved->DISORG.HISTORY;list_returned->DISORG.HISTORY;create_available->DISORG.HISTORY;not_found->DISORG.ERROR;duplicate->DISORG.ERROR;ambiguous->DISORG.ERROR;failed->DISORG.ERROR | DISORG.VALIDATE | stop | Read is requested, an exact target is required before edit, inactivate, or delete, or a uniqueness check is required before create |
| DISORG.HISTORY | decision | 3 | reference_lookup | eligible->DISORG.CONTEXT;not_required->DISORG.CONTEXT;first_row->DISORG.ERROR;missing->DISORG.ERROR;ambiguous->DISORG.ERROR;failed->DISORG.ERROR | DISORG.READ | stop | Date-effective delete is requested after the current organization is read using today's effective date |
| DISORG.CONTEXT | decision | 4 | reference_lookup | resolved->DISORG.VALUESET;not_required->DISORG.VALUESET;ambiguous->DISORG.ERROR;failed->DISORG.ERROR | DISORG.HISTORY | stop | A Disability Organization EFF context or segment is requested or supplied |
| DISORG.VALUESET | decision | 5 | reference_lookup | valid->DISORG.DEPENDENCIES;not_required->DISORG.DEPENDENCIES;invalid->DISORG.ERROR;failed->DISORG.ERROR | DISORG.CONTEXT | stop | A supplied Disability Organization EFF segment declares a value set |
