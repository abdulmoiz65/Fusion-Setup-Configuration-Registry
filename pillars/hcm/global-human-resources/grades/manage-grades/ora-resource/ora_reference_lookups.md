# Manage Grades Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_grades | A row search, exact target lookup, or create uniqueness check is requested | GradeId, GradeCode, SetCode, exact Name, or user-supplied name fragment | /hcmRestApi/resources/{version}/gradesV2 | GradeId, GradeCode, Name, SetId, SetCode, ActiveStatus, EffectiveStartDate, EffectiveEndDate, and item link | To find rows by name fragment, pass q=Name like '%<name-fragment>%' without hardcoding the fragment and return all matches. For read, edit, or delete, require one exact GradeId or GradeCode and SetCode match. For create, require zero exact GradeCode and Name matches. | Resolved GradeId, GradeCode, SetCode, effective context, current values, and item link when available | Return zero or all matches for a row search. For read, edit, or delete, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches block duplicate creation. |
| resolve_grade_set | create supplies a Set | Exact SetCode or SetName | shared.validation.reference-data-validator | SetId, SetCode, and SetName | Require one internally consistent Set tuple | SetId and SetCode | Stop on zero, multiple, or inconsistent matches |
| resolve_grade_action_reason | A mutation supplies an Action Reason | Exact ActionReasonCode | Current loader contract | ActionReasonCode | Require one supported exact code | ActionReasonCode | Stop when unsupported or ambiguous |
| resolve_grade_split_deletion_range | An effective-split delete or its verification is requested | Fresh GradeId and exact selected EffectiveStartDate | /hcmRestApi/resources/{version}:9/hcmDateEffectiveObjectHistory?fields=FirstSplitFlag,EffectiveStartDate,EffectiveEndDate&finder=findHistory;HistoryDefClassName=oracle.apps.hcm.employment.responsive.publicUiModel.history.definitions.GradeHistoryDef,PrimaryObjectId={GradeId} | FirstSplitFlag, EffectiveStartDate, and EffectiveEndDate | Read all pages and order rows by EffectiveStartDate. Match exactly one selected row, require FirstSplitFlag=false, and select its immediately preceding row. Before authoring, set the retained start from that predecessor and the inclusive deletion end from the selected row. After load, require the selected row absent, the predecessor end extended to the selected end, and every other row unchanged. | Retained predecessor EffectiveStartDate, selected EffectiveEndDate, and before/after history evidence | Stop on request failure, incomplete pagination, no exact selected row, ambiguity, FirstSplitFlag=true, no predecessor, invalid ordering, or inconsistent verification. |
| read_grade_eff_context | A Grade legislative EFF context or segment is read or changed | Exact Grade, effective date, and context or segment | Fresh link-bearing Grade parent and GRADE_LEG envelope, current polymorphic describe, and returned context child link | Context and segment labels, business values, and row count | Require one exact parent and envelope and one describe-matched returned context link | Business-facing context values | Re-read in link-bearing form before treating a link as missing; never construct a path |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A Grade delete is requested | Resolve the logical Grade first. For effective-split delete, run resolve_grade_split_deletion_range and show only the Grade business identity, selected effective period, and resulting retained range; keep FirstSplitFlag and GradeId internal. For zap, disclose that the complete logical Grade will be purged and do not run the split-range derivation. |
| Grade history is requested | Follow every history page, order the returned rows by EffectiveStartDate, and evaluate the complete result. |
| An eligible delete range is presented | Show Grade code or name, status, retained effective start, and inclusive deletion end; state that complete deletion is unsupported. Keep FirstSplitFlag and internal identifiers hidden. |
| A Grade legislative EFF context or segment is requested | Read the exact parent and GRADE_LEG envelope without onlyData=true, resolve the context from current polymorphic describe, and follow the matching returned child link from links or @context.links. |
| An exact target is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| A reference value or lookup code is required | Route it to hcm.global-human-resources.global-human-resources-common.manage-common-lookups; keep find_manage_grades limited to Grade row read, search, and uniqueness checks. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.READ | decision | 2 | reference_lookup | resolved->GRD.HISTORY;list_returned->GRD.HISTORY;create_available->GRD.HISTORY;not_found->GRD.ERROR;duplicate->GRD.ERROR;ambiguous->GRD.ERROR;failed->GRD.ERROR | GRD.VALIDATE | stop | Read is requested, an exact target is required before edit, inactivate, or delete, or a uniqueness check is required before create |
| GRD.HISTORY | decision | 3 | reference_lookup | eligible->GRD.DEPENDENCIES;not_required->GRD.DEPENDENCIES;first_row->GRD.ERROR;missing->GRD.ERROR;ambiguous->GRD.ERROR;failed->GRD.ERROR | GRD.READ | stop | An effective-split delete is resolved after the exact Grade is read; zap proceeds as not_required |
