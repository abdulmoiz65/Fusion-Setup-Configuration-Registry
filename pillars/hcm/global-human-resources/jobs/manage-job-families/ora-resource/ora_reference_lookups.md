# Manage Job Families Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_job_families | A job-family list search, exact target lookup, or create uniqueness check is requested | Job Family code, exact name, or name fragment | /hcmRestApi/resources/{version}/jobFamiliesV2 | JobFamilyId, JobFamilyCode, JobFamilyName, effective dates, and item link | For a name-fragment list search, pass q=JobFamilyName like '%<name-fragment>%' and return every resource match; do not hardcode a search term. For read, edit, or delete, require one exact job family. For create, require zero exact matches. | JobFamilyId, code, name, effective dates, and item link | Return zero or all matches for a list search. For read, edit, or delete, stop on zero or multiple matches. For create, zero means the identity is available; one or more exact matches block the duplicate create. |
| resolve_job_family_subfamily | Create or edit supplies a Job Subfamily association | Exact Job Subfamily code or meaning and Job Family effective date | core.fusion-api.apps-common lookup type ORA_PER_WS_JOB_SUB_FAMILY | LookupCode, meaning, enabled status, and effective range | Require one exact enabled code effective on the Job Family date | JobSubFamily stored code | Stop on zero, multiple, disabled, or out-of-range results |
| read_job_family_associations | An association is read, changed, or verified | Fresh link-bearing Job Family item | Server-returned jobSubFamilyAssociations child link | Association identity, JobSubFamily, ActiveStatus, and effective context | Return the complete direct child collection | Current association set and child link | Re-read the link-bearing parent before treating the link as missing; never use parent expansion as the complete set |
| resolve_job_family_association_limit | Create or edit supplies associations | Job Family effective date | core.fusion-api.apps-common profile value PER_JOB_SUB_FAMILY_ASSOCIATION_TO_JOB_FAMILY_LIMIT | ProfileOptionValue | Accept zero or one effective value; require a numeric value when present | Numeric maximum or not_configured | Treat no value or HTTP 404 as not_configured; stop on malformed or multiple values |
| read_job_family_delete_history | Effective-split delete is requested | JobFamilyId and selected EffectiveStartDate | Current `jobFamiliesV2/describe` finder `findByJobFamilyId;JobFamilyId=<id>,SysEffectiveDate=<date>` | EffectiveStartDate, EffectiveEndDate, and adjacent predecessor/final-split evidence | Resolve the selected non-first final future row and its immediately preceding row; use the predecessor start as the retained boundary and the selected end as the inclusive deletion end | Retained EffectiveStartDate, deleted EffectiveEndDate, and before/after split evidence | Stop when the finder is unavailable, a row is missing or ambiguous, the selected split is first, nonfinal, nonfuture, or lacks an adjacent predecessor; do not expose internal history flags |
| find_job_references_for_job_family | Any Job Family delete is requested | Exact resolved JobFamilyId or JobFamilyCode | `/hcmRestApi/resources/{version}/jobsV2` using the current describe-supported Job Family filter | Complete matching Job set and effective ranges | Require zero Jobs referencing the exact resolved Job Family; page the declared bound before accepting zero | Zero-reference evidence | Stop when the filter contract is unavailable, paging is incomplete, or any Job reference exists |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| Job Subfamily associations are needed | Read the exact parent without onlyData=true and follow its returned jobSubFamilyAssociations link; do not construct the child path. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A Job Family delete is requested | Resolve zero Job references before source preparation; do not use an empty or unsupported filter as proof. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JF.READ | decision | 2 | reference_lookup | resolved->JF.DEPENDENCIES;create_available->JF.DEPENDENCIES;not_found->JF.ERROR;duplicate->JF.ERROR;ambiguous->JF.ERROR;failed->JF.ERROR | JF.VALIDATE | stop | Read is requested, an exact target is required before edit or delete, or a uniqueness check is required before create |
