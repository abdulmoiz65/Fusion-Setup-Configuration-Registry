# CAP root read contract

Only the declared standard shared GET client performs HTTP. No root PATCH item URL or Data Loader prerequisite is needed for collection retrieval. Use the current authorized metadata, not historical APEX display values. Product-specific unknowns remain unavailable in references/runtime-contract.md.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-BATCH-OBSERVE | step | 360 | reference_lookup | passed->CAP-BATCH-DESIGN | CAP-BATCH-INPUT | stop | Shared GET root metadata, complete exact-number baseline and fresh canonical item; writable requested attributes; rename duplicate checks; visibility inline enum or source-bound commonLookupsLOV LookupTypeFinder ORA_WLF_CAP_ADMIN_VISIBILITY complete bounded shared GET required |
| CAP-I-READ | step | 280 | reference_lookup | observed->CAP-I-DONE | CAP-I-PREREQ | stop | Bounded canonical root/child metadata and counts; unavailable children remain explicit |
| CAP-R-METADATA | step | 120 | reference_lookup | passed->CAP-R-GET | CAP-R-PREREQ | stop | GET root describe within60 seconds including auth; validate before collection |
| CAP-R-GET | step | 130 | reference_lookup | complete->CAP-R-DONE;partial->CAP-R-PARTIAL | CAP-R-METADATA | stop | Fetch exact matches or every accessible list page within bounded execution |
| CAP-CHECK-ROOT | step | 180 | reference_lookup | passed->CAP-CHECK-LOADER | CAP-CHECK-PREREQ | stop | Read root describe facts for write-contract assessment, never infer privilege/default semantics |
| CAP-CHECK-LOADER | step | 190 | reference_lookup | observed->CAP-CHECK-DONE | CAP-CHECK-ROOT | stop | Read advertised loader metadata and unique CAP registration; no template download, validation, upload or job |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| describe_cap_root | After read preflight | Confirmed configured origin and environment | GET /hcmRestApi/resources/11.13.18.05/learningCatalogProfiles/describe via core/fusion-api/rest-api-client/scripts/fusion_rest_client.py | Named Resources.learningCatalogProfiles attributes, collection GET and exact selector/finder metadata | cap_read.resource_description; stable text profile number, text display fields, GET advertised; exact selector queryable; number finder has explicit number argument | Only metadata-supported projection plus exact selector; optional expected ID validated independently | Missing or inconsistent metadata stops before business GET |
| read_cap_collection | After metadata | mode exact or list, optional exact text name or number, same headers/target | GET /hcmRestApi/resources/11.13.18.05/learningCatalogProfiles through the same shared client | learningCatalogProfileNumber,name,description,status,visibility,isSystemDefault,processingStatus where declared; identity required; optional learningCatalogProfileId only for expected-ID check | List uses onlyData,fields,limit,offset; exact name uses q name equality and client exact comparison; number uses findByLearningCatalogProfileNumber;learningCatalogProfileNumber=value plus independent number q equality scan, requiring equal identities | Exact matched/ambiguous/no_accessible_match; list items,count,pagination_completed,errors and retrieval_only/write_eligible=false | Exhaust pages before uniqueness/absence assessment; incomplete exact query fails. Listing preserves only verified complete pages and reports partial/failed; 401/403 is not zero matches |

## Contract Inspection

Contract inspection uses the existing describe_cap_root resolver for CAP-CHECK-ROOT.
CAP-CHECK-LOADER uses inspect_cap_registration below; it does not select a write.
The collection query includes ProductAreaCode is not null, as in the shared
find_business_objects root filter; exact discriminator equality narrows this to
CAP. BusinessObjectId is the lossless row identity for duplicate/loop detection.
Require the advertised findDataLoaderBos finder with no required arguments.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| inspect_profile_children | After exact-number inspection input and configured preflight | Confirmed target and unique current number; returned date-plus-number context key | cap_profile_inspection via shared GET root describe and exact number q; only advertised contributorCriteria, contributorPersonList, contentDefaults, certificates under canonical parent /child/name/describe and /child/name | Root public fields; reconcilePriority string and reconcileStartDate, reconcileEndDate, reconcileLastRunProcessDate datetime; child identities transient for counts only | Exhaust exact parent query; validate returned ISO date/number key; require child GET and typed identity: contributorCriteria uses source-verified criteriaId string even without key marker; other children require advertised keys; reject duplicate/conflicting metadata and invalid values; bounded20pages2000rows and180seconds overall | Sanitized root fields with null distinct from missing; effective date and per-child counts/partial/unavailable; never raw person/key/links, grants or completion inference | Missing canonical key forbids child calls; absent or conflicting identity schema prevents collection GET; unavailable children keep overall partial, no fallback |
| inspect_cap_registration | Read-only contract inspection after CAP root describe | Confirmed configured target; fixed learningCatalogProfiles discriminator | Shared fusion_rest_client.py GET /hcmRestApi/resources/latest/dataLoaderBusinessObjects/describe; public shared resolve_business_object with allow_aliases false and explicit shared-GET adapter for standard findDataLoaderBos query; then matched positive decimal BusinessObjectId detail | Named root describe; BusObjTopDiscriminator, BusinessObjectId ephemeral; detail ObjectType, ProductAreaCode, ServiceVersion, ValidOperations, EffectiveDated, TemplateFileName, UcmContentId presence only | Require collection GET/queryable string discriminator; bounded100/page20pages2000rawrows120seconds; shared exact discriminator and ID deduplication, distinct IDs ambiguous; typed page envelope and advancing offsets; no free-form URL; detail ID/discriminator match | Sanitized cap_write_contract.assess facts and per-operation blockers only; IDs and template reference never output; GET is not write privilege or template validation | Fail closed on absent, ambiguous, malformed, nonadvancing or incomplete registration; repeated same-ID finder rows at advancing offsets are allowed; no alternate client or guessed registration |

## Lookup Execution Rules

The `inspect-update-contract` read-only specialization of CAP-I validates exact
number input through the same compiled read prerequisites. It reads root describe,
exhausts the number equality query and observes only declared root baseline fields.
It then GETs the returned canonical ISO-date/number item and the percent-encoded
number-only item through the same shared client, within 120 seconds total.
These two explicitly selected diagnostic paths are comparisons, not write routes.
A failed shared call stops comparison (no fallback), and sanitized failures do not
claim a particular HTTP status. Item GET success never establishes loader PATCH
mapping, omission semantics or write authorization. No child or arbitrary URL is
accepted. `cap_update_inspection.py` returns only projected metadata/baseline and
match summaries, not opaque context URLs, ETags or credentials.

| Situation | What Happens |
|---|---|
| Identity | Preserve text numbers; expected ID may be exact decimal integer read losslessly by Python or text, never float. Require exact expected ID when supplied; do not expose opaque item URLs. |
| Pagination | cap_read enforces count/offset/limit/hasMore, repeated identity and empty-more checks. A short page alone never establishes completion. Bound each shared-client subprocess including authentication/refresh by remaining time. |
| Access limits | Report caller-visible records only; server-current effective date, requested language or server default, non-snapshot pagination. Neither a complete list nor zero accessible matches proves tenant-global absence. |
| Baseline review | cap_proposal.baseline_candidates compares known root values and marks ownership/membership unverified. Seeded default is recognized only by isSystemDefault=Y, not its label. Inactive candidate can suggest activation, never execute it. |
| Inspection identity contract v1 | Redwood catalog-administration-profile-details-page.js constructDeletePayload and constructUpdatePayload use returned row.criteriaId in contributorCriteria item URLs. Current child describe must contain exactly one criteriaId of type string; an explicit contradictory key marker or different advertised keys is a conflict. No inference from mandatory, inCreate, field suffix or sourceId. contributorPersonList has no established source fallback; personId is not assumed unique. |
| Inspection value and result contract | Preserve server date strings including timezone and present null, without normalization or completion inference. Unsupported metadata is unavailable; wrong JSON value types fail. Only a complete child scan yields total_count; criterion rows are not effective people or access counts. Complete observed, no_accessible_match and ambiguous are successful read outcomes; partial/failed remain nonzero CLI outcomes. All envelopes retain task, target, terminal and limitations; never write eligibility. |
