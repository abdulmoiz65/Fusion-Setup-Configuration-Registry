# Manage Enterprise HCM Information Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_enterprise | Enterprise details, a context, or delete is requested | Requested effective date, or today's date for delete | /hcmRestApi/resources/{version}/enterprise?effectiveDate={date} | OrganizationId, EffectiveStartDate, EffectiveEndDate, and requested parent values | One Enterprise row covers the effective date | Parent identity, effective range, and requested parent values | Stop when no Enterprise row covers the date |
| resolve_enterprise_read_scope | Enterprise parent, selected-context, or all-context details are requested | Requested parent field, context/segment wording, or explicit all-context intent | No Fusion request; choose parent, selected-context, or all-context mode | Read mode and requested scope | Select all-context mode only for an explicit request; otherwise preserve the selected parent field, context, or segment | Applicable read resolver | Stop when no supported scope is supplied |
| resolve_enterprise_delete_history | Date-effective delete or its verification is requested | Fresh OrganizationId and current Enterprise effective range | /hcmRestApi/resources/{version}/hcmDateEffectiveObjectHistory?fields=FirstSplitFlag,EffectiveStartDate,EffectiveEndDate&finder=findHistory;HistoryDefClassName=oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.EnterpriseHistoryDef,PrimaryObjectId={OrganizationId} | FirstSplitFlag, EffectiveStartDate, and EffectiveEndDate | Evaluate returned items; before delete, match one current row; after delete, require it absent and all other rows unchanged except the preceding end boundary | Selected row dates, internal eligibility, and before/after evidence | Stop on request failure, no exact row, ambiguity, or inconsistent verification |
| resolve_enterprise_classification | An Enterprise OrgInformation EFF row is built | Fresh Enterprise parent and its returned enterpriseEFF envelope | Follow the Enterprise item enterpriseEFF link | OrgUnitClassificationId, CategoryCode, EffectiveStartDate, EffectiveEndDate | Exactly one Enterprise classification envelope with CategoryCode ENTERPRISE | Classification parent identity, category ENTERPRISE, and effective values needed by the OrgInformation row | Stop when the Enterprise classification row is absent or ambiguous; do not build the EFF row |
| resolve_enterprise_context | A context or segment is requested | Context or segment business wording | Enterprise polymorphic describe for enterprise.enterpriseEFF:ENTERPRISE | Context codes and labels, context collection, segment names and labels, cardinality, value-set contract | Exact code, then normalized label, then one unique token match; the segment must belong to the resolved context | Resolved context collection and segment contract | Stop on zero or multiple matches; do not guess |
| read_enterprise_context | Enterprise context details or an edit precheck is requested | Resolved context and exact effective Enterprise | Re-read the parent and ENTERPRISE envelope in link-bearing form, then follow the describe-matched returned context child link | OrgInformationId, EffectiveStartDate, EffectiveEndDate, SequenceNumber, business values, and row count | One returned Enterprise EFF link and one matching context child row | Existing-row identity, effective range, SequenceNumber, and current values | Re-read in link-bearing form before treating a link as missing; never construct a path |
| read_all_enterprise_contexts | The user explicitly asks to show all Additional Information contexts | Explicit all-context request and exact effective Enterprise | Read the Enterprise polymorphic describe for enterprise.enterpriseEFF:ENTERPRISE; re-read the parent and ENTERPRISE envelope in link-bearing form; then follow every live child link whose context code exactly matches a describe-declared context | Context codes, labels, child links, business values, and row count | Preserve describe order; each context code must have at most one matching live child link | Every describe-declared context title and its returned business labels and values; report `No current context row` when no live child link is returned | Stop on an ambiguous context code or multiple matching child links; never construct a child path or infer a context |
| validate_enterprise_segment_value | A proposed segment value is supplied | Proposed value and active segment value-set metadata | Describe-declared LOV resource and exact filter; use a fresh server-returned runtime URL only when provided | Source value, display attributes, target attribute, and native type | Exactly one value-set match using the declared display or source attribute | Validated typed stored value for the declared target attribute | Block on no match, multiple matches, type mismatch, or target mismatch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A Fusion REST request runs | Send `REST-Framework-Version: 9` as an HTTP header; do not append it to the resource version in the URL. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| An Enterprise EFF context or segment is requested | Read the exact parent and ENTERPRISE envelope without onlyData=true, resolve the context from current polymorphic describe, and follow the matching returned child link from links or @context.links. |
| The user explicitly requests all Additional Information contexts | Use `read_all_enterprise_contexts`. Read only context codes declared by the current polymorphic describe and follow only their current server-returned child links. Do not enumerate guessed paths, context names, or links. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Enterprise history is requested | Execute the history finder once and evaluate its returned items; do not apply generic collection pagination. |
| Enterprise details are returned | Show parent Enterprise values and parent EffectiveStartDate to EffectiveEndDate only. |
| Parent end date is 4712-12-31 | Show End Of Time. |
| Context details are returned | Show context title, business labels, and values only; do not show context EffectiveStartDate or EffectiveEndDate. |
| An eligible delete row is presented | Show Enterprise name, status, and effective period; state that complete deletion is unsupported and offer date-effective deletion of this row. Keep FirstSplitFlag and internal identifiers hidden. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENT.READ | decision | 2 | reference_lookup | resolved->ENT.HISTORY;not_found->ENT.ERROR;failed->ENT.ERROR | ENT.VALIDATE | stop | Enterprise details, context details, edit precheck, or delete is requested |
| ENT.HISTORY | decision | 3 | reference_lookup | eligible->ENT.CLASSIFICATION;not_required->ENT.CLASSIFICATION;first_row->ENT.ERROR;missing->ENT.ERROR;ambiguous->ENT.ERROR;failed->ENT.ERROR | ENT.READ | stop | Date-effective delete is requested after the Enterprise is read using today's effective date |
| ENT.CLASSIFICATION | decision | 4 | reference_lookup | resolved->ENT.CONTEXT;not_required->ENT.CONTEXT;ambiguous->ENT.ERROR;failed->ENT.ERROR | ENT.HISTORY | stop | An Enterprise OrgInformation EFF row is built |
| ENT.CONTEXT | decision | 5 | reference_lookup | resolved->ENT.CONTEXT_READ;all_requested->ENT.CONTEXT_READ;not_required->ENT.VALUESET;ambiguous->ENT.ERROR;failed->ENT.ERROR | ENT.HISTORY, ENT.CLASSIFICATION | stop | A context, segment, or explicit all-context read is requested |
| ENT.CONTEXT_READ | step | 6 | reference_lookup | resolved->ENT.VALUESET;failed->ENT.ERROR | ENT.CONTEXT | stop | A selected context or all explicitly requested Additional Information contexts are read from live links |
| ENT.VALUESET | decision | 7 | reference_lookup | valid->ENT.DEPENDENCIES;not_required->ENT.DEPENDENCIES;invalid->ENT.ERROR;failed->ENT.ERROR | ENT.HISTORY, ENT.CLASSIFICATION | stop | A proposed segment value is supplied |
