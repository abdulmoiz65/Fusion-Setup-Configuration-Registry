# Review Period Reference Lookups

Apply [Goal Management Dependent Setup Routing](../../../goal-management-common/dependent-setup-routing.md)
to every shared or cross-product reference. This task may read dependencies
for validation; dependency maintenance is an independent owner-routed task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| review_period_resource_route | Before the first management read or write | Connected environment | GET `/hcmRestApi/resources/latest/reviewPeriods/describe` through the core REST client | Collection, search action, item links, writable attributes, advertised methods | Expected `reviewPeriods` resource on the configured host; a numeric release in a canonical link is acceptable server resolution | In-memory `resourceRoot=/hcmRestApi/resources/latest` and supported operations | If unavailable, resolve one trusted current runtime fallback; reject `rv:null` and never invent a root |
| review_period_search | list/search or create duplicate check | Normalized query, display fields, limit, offset | Primary: `{resourceRoot}/reviewPeriods/action/findByAdvancedSearchQuery`; fallback: GET `{resourceRoot}/reviewPeriods` paged locally | ReviewPeriodId, ReviewPeriodName, Description, StartDate, EndDate, StatusCode, StatusMeaning, InUseFlag, CreationDate, CreatedBy, pagination | Use `Content-Type: application/vnd.oracle.adf.action+json` for the action. Complete pagination and compare exact `ReviewPeriodName`; dates do not distinguish duplicates. If current metadata or the action contract rejects the read, page the ordinary collection GET, hydrate missing creation dates, filter locally, and record the fallback. No write approval is required. | Candidate rows, pagination state, resolved query window, route used | Return an empty READ result only after the selected current read route is exhausted; block only when neither advertised route is available |
| review_period_lookup | An existing identity is required | ID or exact name and effective context | `{resourceRoot}/reviewPeriodsLOV` for optional ID resolution, then `{resourceRoot}/reviewPeriods/{ReviewPeriodId}?fields=*` | ReviewPeriodId, name, description, dates, status, `InUseFlag`, `CreationDate`, concurrency | Exact normalized identity; never use LOV for writes | ReviewPeriodId and fresh management state | Return MISSING or require disambiguation |
| review_period_usage_lookup | A risky change is requested | ReviewPeriodId | Current exposed Goal Plan and consumer reads | Consumer identity and reference status | Count every page and classify active references | Usage count and safe reference summary | Block when usage cannot be established |
| review_period_status_lookup | Entry-context initialization or a status-bearing mutation | Connected environment | GET `/fscmRestApi/resources/latest/commonLookups/ACTIVE_INACTIVE?expand=lookupCodes` through Apps Common | LookupCode, Meaning, EnabledFlag, effective dates | Use enabled/effective returned codes as the valid set; require one effective `A` row before applying the documented fallback | Allowed status code/meaning pairs | Block status-bearing mutation when the lookup is unavailable, empty, or lacks effective `A`; entry-context read returns a lookup diagnostic |
| review_period_describe | A metadata-gated mutation is requested | Connected environment | GET `/hcmRestApi/resources/latest/reviewPeriods/describe` through the core REST client | Writable attributes, item methods, and concurrency contract | Use only current advertised operations; never infer DELETE | Current relative route and supported mutation contract | Block the mutation and return a guided plan when metadata is unavailable |

## Foundation Profile-Option Delegation

A consultant request to inspect or maintain an exact profile option is not a
Review Period mutation. Pass the supplied `profile_option_code` unchanged as
`ProfileOptionName` to external capability
`core.fusion-api.apps-common.profile-options` through the parent profile-option
routing contract. Query current definition or effective value before proposing
a provider-owned change. If the requested foundation work needs a code and none
is supplied, ask the consultant for the exact profile option code; do not reuse
`ACTIVE_INACTIVE` or infer another identifier. Return `validation_gap` for an
unknown or ambiguous code and `PROVIDER_SKILL_UNAVAILABLE` when the provider is
unavailable.

## Foundation Lookup Delegation

`ACTIVE_INACTIVE` is a current runtime validation lookup in this task. A
consultant request to inspect or maintain that or another exact lookup type/code
is not a Review Period mutation: require external capability
`core.fusion-api.apps-common.lookups` under the parent
lookup-routing contract. Never mutate `commonLookupsLOV`.

## Foundation Value-Set Delegation

A consultant-supplied exact value-set code is not a Review Period field value.
Require external capability
`core.fusion-api.apps-common.value-sets` under the parent
value-set routing contract; resolve the code to a returned ID before any read
or child-value operation.

## Foundation Flexfield Delegation

A consultant-supplied exact Descriptive Flexfield code is not a Review Period
payload field. Route it through `core.fusion-api.apps-common` using
external capability `core.fusion-api.apps-common.descriptive-flexfields`
using `HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD` and the parent
flexfield routing contract. Do not infer a context, segment, or runtime field; DFF
configuration and import remain outside the Review Period payload.
| review_period_worker_context_lookup | Entry-context initialization and authenticated caller ID is available | Authenticated caller ID | Resolve the trusted current hcm REST runtime root, then GET `/publicWorkers/{authenticatedCallerId}?expand=assignments&fields=PersonId,PersonNumber;assignments:AssignmentId,AssignmentName,AssignmentNumber`; use returned PersonId in GET `/workerAssignmentsLOV?fields=DepartmentName,BusinessUnitName,LegalEmployerName,LegislationCode&finder=findByWorker;PersonId={PersonId}&onlyData=true` | PersonId, PersonNumber, assignment ID/name/number, DepartmentName, BusinessUnitName, LegalEmployerName, LegislationCode | Use the returned PersonId; retain the first returned current assignment/context row only as VBCS display context | Sanitized caller worker, assignment, and organizational context | Return partial entry context with a diagnostic when caller identity, worker, or assignment context is unavailable; do not block Review Period data reads or mutations |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| LOV resolves an ID | Use the ID only to read the management object |
| More than one exact match remains | Stop; do not select the first row |
| Usage source is unavailable | Deletion and date-envelope changes remain blocked |
| A runtime router URL is captured | Retain only sanitized relative action semantics; never persist host, router UUID, object ID, or concurrency token |
| Standard `latest` route is available | Keep the stable relative `resourceRoot` for the run; do not replace it with the numeric release shown in returned canonical links |
| Standard route is unavailable | Resolve one same-host current runtime root from trusted metadata, reject `rv:null`, keep it in memory only, and finish fallback before preview |
| Authentication is not ready | Run one harmless serialized request; never start parallel OAuth-dependent commands against the shared loopback callback |
| Last-N-days filter is requested | Convert to one exact UTC interval, fetch all candidate pages, hydrate missing `CreationDate` values, filter locally, and sort newest first |
| Search action is HTTP POST | Classify it as READ because it has no setup side effect; do not route through a write approval gate |
| Entry context is initialized | Resolve status first. If an authenticated caller ID is available, resolve worker then assignment context serially. Do not perform the omitted VBCS view/manage permission check; REST authorization remains authoritative |
| A captured runtime URL is supplied | Retain only the relative resource semantics and runtime placeholders; never persist its tenant host, runtime revision, caller/person ID, or returned context key |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.LOOKUPS | step | 40 | reference_lookup | resolved->REVIEW_PERIODS.DEFAULTS;unresolved->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.DEPENDENCIES | stop | Mutation dependencies require identity or usage resolution |
| REVIEW_PERIODS.SEARCH | step | 26 | reference_lookup | found->REVIEW_PERIODS.DONE_SEARCH;empty->REVIEW_PERIODS.DONE_SEARCH;unavailable->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.VALIDATE | stop | list/search is selected, including creation-time filters |
| REVIEW_PERIODS.ENTRY_CONTEXT | step | 24 | reference_lookup | ready->REVIEW_PERIODS.DONE_ENTRY_CONTEXT;partial->REVIEW_PERIODS.DONE_ENTRY_CONTEXT;unavailable->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.VALIDATE | stop | initialize_entry_context is selected |


---

# Review Period REST Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| `/hcmRestApi/resources/latest/reviewPeriods/describe` | Preferred release-independent collection, attributes, actions, media types, and item contract |
| Trusted current REST link/metadata or approved OpenAPI from the authenticated connected environment | Fallback only when the standard `latest` collection is unavailable; resolve one same-host volatile runtime root and reject `rv:null` |
| `/hcmRestApi/resources/latest/reviewPeriodsLOV` | Identifier resolution only; never a write endpoint |
| `GET /fscmRestApi/resources/latest/commonLookups/ACTIVE_INACTIVE?expand=lookupCodes` through Apps Common | Current enabled/effective Review Period status codes; never use an ADF lookup URL |
| Trusted current hcm REST metadata/OpenAPI | Runtime root and item/finder contract for publicWorkers and workerAssignmentsLOV entry-context reads |
| shared setup export/import skills | Catalog-supported FSM CSV routes |

## Execution Contract

| Situation | What Happens |
|---|---|
| Get | Resolve exactly one identity and return a sanitized current view |
| List/search | Send the normalized advanced-search query with display fields ReviewPeriodId, ReviewPeriodName, Description, StartDate, EndDate, StatusCode, StatusMeaning, InUseFlag, CreationDate, and CreatedBy. Never request `Status`; page all results up to the disclosed limit, hydrate missing detail fields, apply local filters, and return a sanitized sorted list |
| Create | Search first, map current attributes, preview the explicit valid status or proven metadata default, create with that approved status, and verify; no blanket inactive-first requirement |
| Update | Re-read usage and target; patch only explicit changes |
| Inactivate | Re-read usage, preview impact, patch status only when supported |
| Delete | Proceed only when current authoritative metadata advertises DELETE; then require `InUseFlag=false`, zero usage, explicit delete approval, one delete, and verification |
| Initialize entry context | Read the current status LOV and optionally resolve the authenticated caller's worker and assignment display context. Do not evaluate VBCS view/manage permissions; REST authorization is authoritative |
| Unsupported REST contract | Route to guided FSM/UI; do not invent an endpoint or payload |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Search/list | POST (read-only action), with GET collection fallback | `{resourceRoot}/reviewPeriods/action/findByAdvancedSearchQuery` with `query`, `searchFields`, `displayFields`, `limit`, and `offset`; on an unavailable/rejected action, GET `{resourceRoot}/reviewPeriods` page-by-page and apply the normalized filter locally |
| Read management object | GET | `{resourceRoot}/reviewPeriods/{ReviewPeriodId}?fields=*` |
| Create | POST | `{resourceRoot}/reviewPeriods` |
| Update or inactivate | PATCH | `{resourceRoot}/reviewPeriods/{ReviewPeriodId}` with fresh concurrency state and `If-Match` ETag when the current service contract supplies one; never infer an optimistic-lock bypass when it does not |
| Delete | DELETE | Only a current authoritative metadata-returned item path that explicitly advertises DELETE, after zero-usage proof |
| Read status lookup | GET | `{restBaseUrl}/fscmRestApi/resources/latest/commonLookups/ACTIVE_INACTIVE?expand=lookupCodes`; retain enabled/effective returned codes |
| Read authenticated worker context | GET | `{hcmRuntimeRoot}/publicWorkers/{authenticatedCallerId}?expand=assignments&fields=PersonId,PersonNumber;assignments:AssignmentId,AssignmentName,AssignmentNumber` |
| Read assignment context | GET | `{hcmRuntimeRoot}/workerAssignmentsLOV?fields=DepartmentName,BusinessUnitName,LegalEmployerName,LegislationCode&finder=findByWorker;PersonId={returnedPersonId}&onlyData=true` |

## Required Media Type

Select the media type before sending the first request. Do not probe Fusion by
cycling through content types after a failure.

| Request shape | Required header |
|---|---|
| Top-level JSON object contains a `parts` array | `Content-Type: application/vnd.oracle.adf.batch+json` |
| Custom action path contains `/action/`, including `findByAdvancedSearchQuery` | `Content-Type: application/vnd.oracle.adf.action+json` |
| Ordinary POST or PATCH with an entity JSON body | `Content-Type: application/json` |
| Ordinary GET with no body | `Accept: application/json`; omit request `Content-Type` |

Batch classification has precedence when the top-level `parts` array is
present. Otherwise, the search/list endpoint above is always an ADF action and
must use the action media type. Fail closed if the selected header conflicts
with the path or payload shape.

Do not convert a captured runtime-router URL into a reusable literal. The
router UUID, tenant host, language/release suffix, object ID, and concurrency
token are runtime values and must not be stored in this skill.

Set `resourceRoot=/hcmRestApi/resources/latest` when the standard describe call
advertises the expected resource and operation. A returned self/canonical link
may resolve `latest` to a numeric release; do not hardcode that release. Use a
trusted current runtime root only as a pre-preview fallback when the standard
route is unavailable, reject `rv:null`, and never change roots after approval.

Run every request through `core.auth.fusion-oauth-authentication` and
`core.fusion-api.rest-api-client` using the configured environment and secure
per-user credential cache. Never write `.fusionaim_token.json` or another
token/cookie file in the repository. If authentication needs interaction, use
Chrome only for the OAuth handoff; after authentication, the REST client—not
the browser—fetches the data.

Establish authentication with one harmless serialized request before issuing
multiple metadata/data calls. Do not start parallel commands while OAuth may
need the shared loopback callback, and never parallelize mutations.

The advanced-search POST is semantically read-only. It may execute immediately
after validation and never satisfies or consumes a mutation approval.

## Preview Pattern

| Step | Requirement |
|---|---|
| 1 | Cache only current attribute name, type, and updateable metadata |
| 2 | Generate a saved mapped payload and mapping report from current input |
| 3 | Show target, before/after values, usage, environment, and exact payload; retain the fingerprint internally |
| 4 | Apply the [shared Goal Management approval convention](../../../goal-management-common/approval-convention.md) after the final fresh read. Accept a clear contextual affirmative only for one immediately preceding unchanged preview, identified operation, or explicitly combined batch; never require the consultant to repeat the fingerprint |

## Live Pattern

| Step | Requirement |
|---|---|
| 1 | Recheck identity, metadata, usage, concurrency, and approval fingerprint; send the freshly fetched `If-Match` ETag when current metadata requires it |
| 2 | Submit once; never automatically retry POST, PATCH, or DELETE |
| 3 | Re-read with `fields=*` (or an explicit complete field list) so compact-view omission is not mistaken for a null value; classify verified, failed, or unknown-after-submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.READ | step | 25 | reference_lookup | found->REVIEW_PERIODS.DONE_READ;missing->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.VALIDATE | stop | get is selected |
| REVIEW_PERIODS.REST_DESCRIBE | step | 70 | reference_lookup | ready->REVIEW_PERIODS.REST_PAYLOAD;unavailable->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.DESIGN | stop | A REST mutation is selected |
| REVIEW_PERIODS.REST_PAYLOAD | step | 80 | reference_lookup | mapped->REVIEW_PERIODS.WRITE_ROUTE;rejected->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_DESCRIBE | stop | Current management metadata is available |
| REVIEW_PERIODS.CREATE_PREVIEW | decision | 100 | reference_lookup | reviewed->REVIEW_PERIODS.CREATE_APPROVAL;blocked->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_PAYLOAD, REVIEW_PERIODS.WRITE_ROUTE | stop | create is selected |
| REVIEW_PERIODS.CREATE_APPROVAL | decision | 110 | reference_lookup | approved->REVIEW_PERIODS.CREATE;declined->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.CREATE_PREVIEW | stop | Final create preview is reviewed |
| REVIEW_PERIODS.CREATE | step | 120 | reference_lookup | verified->REVIEW_PERIODS.DONE_CREATED;ambiguous->REVIEW_PERIODS.UNKNOWN;failed->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.CREATE_APPROVAL | stop | Approved create is ready |
| REVIEW_PERIODS.UPDATE_PREVIEW | decision | 130 | reference_lookup | reviewed->REVIEW_PERIODS.UPDATE_APPROVAL;blocked->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_PAYLOAD, REVIEW_PERIODS.WRITE_ROUTE | stop | update is selected |
| REVIEW_PERIODS.UPDATE_APPROVAL | decision | 140 | reference_lookup | approved->REVIEW_PERIODS.UPDATE;declined->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.UPDATE_PREVIEW | stop | Final update preview is reviewed |
| REVIEW_PERIODS.UPDATE | step | 150 | reference_lookup | verified->REVIEW_PERIODS.DONE_UPDATED;ambiguous->REVIEW_PERIODS.UNKNOWN;failed->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.UPDATE_APPROVAL | stop | Approved current-metadata update action is ready |
| REVIEW_PERIODS.INACTIVATE_PREVIEW | decision | 160 | reference_lookup | reviewed->REVIEW_PERIODS.INACTIVATE_APPROVAL;blocked->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_PAYLOAD, REVIEW_PERIODS.WRITE_ROUTE | stop | inactivate is selected |
| REVIEW_PERIODS.INACTIVATE_APPROVAL | decision | 170 | reference_lookup | approved->REVIEW_PERIODS.INACTIVATE;declined->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.INACTIVATE_PREVIEW | stop | Final inactivation preview is reviewed |
| REVIEW_PERIODS.INACTIVATE | step | 180 | reference_lookup | verified->REVIEW_PERIODS.DONE_INACTIVATED;ambiguous->REVIEW_PERIODS.UNKNOWN;failed->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.INACTIVATE_APPROVAL | stop | Approved current-metadata inactivation action is ready |
| REVIEW_PERIODS.DELETE_PREVIEW | decision | 190 | reference_lookup | reviewed->REVIEW_PERIODS.DELETE_APPROVAL;blocked->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_PAYLOAD, REVIEW_PERIODS.WRITE_ROUTE | stop | delete is selected and zero usage is proven |
| REVIEW_PERIODS.DELETE_APPROVAL | decision | 200 | reference_lookup | approved->REVIEW_PERIODS.DELETE;declined->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.DELETE_PREVIEW | stop | Final delete preview is reviewed |
| REVIEW_PERIODS.DELETE | step | 210 | reference_lookup | verified->REVIEW_PERIODS.DONE_DELETED;ambiguous->REVIEW_PERIODS.UNKNOWN;failed->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.DELETE_APPROVAL | stop | Approved guarded delete is ready |


---

# Review Period Captured API Path Reference

This reference normalizes the supplied working REST captures. It records the
stable API path and request shape; it does not retain a tenant host, `rv:`
revision, release suffix, record ID, ETag, or payload values from a capture.

| Purpose | Method | Stable path | Runtime values and payload guidance |
|---|---|---|---|
| Create a Review Period | POST | `/reviewPeriods` | Body is an entity JSON object. The capture demonstrates `ReviewPeriodName`, `Description`, `StartDate`, `EndDate`, and `StatusCode`; map only current metadata-supported writable fields. |
| Read one Review Period | GET | `/reviewPeriods/{ReviewPeriodId}?fields=*` | `ReviewPeriodId` comes from the selected search result, a create response, or a fresh item link. Retain returned ETag/concurrency state only for the active operation. |
| Update or inactivate one Review Period | PATCH | `/reviewPeriods/{ReviewPeriodId}` | Resolve the same ID and fresh state immediately before the write. Send only requested writable fields and `If-Match` when current metadata supplies an ETag. |
| Advanced search | POST | `/reviewPeriods/action/findByAdvancedSearchQuery` | Send `Content-Type: application/vnd.oracle.adf.action+json`. The ADF action body uses `query`, `searchFields`, `displayFields`, `limit`, and `offset`; it is read-only despite POST. If current metadata or the action contract rejects it, use the paged collection GET fallback and document the fallback. |

Use `{resourceRoot}` plus the stable path above. The captured absolute URL is
evidence only; it must not become a reusable endpoint or payload template.

## Mutation preflight and verification

Before every Review Period mutation, resolve current `/reviewPeriods/describe`
metadata to confirm the method, writable fields, headers, and concurrency
contract. For create, run the exact duplicate search first; there is no target
item to GET. For update, inactivate, or delete, immediately GET the selected
`/reviewPeriods/{ReviewPeriodId}?fields=*` before preview/submission and use
the returned item link and `If-Match` ETag when supplied. After one submission,
GET the item again to verify the outcome. Do not reuse an earlier read or a
captured ETag.

## Narrow-delta payload rule

Captured entity bodies are field examples, not update templates. A create maps
only current metadata-required fields plus explicitly requested supported
optional fields. An update or inactivation sends only the requested changed
fields: for example, a description-only change maps only `Description`, and a
status-only change maps only `StatusCode`. Never replay captured dates, name,
description, or status merely because they were present in an earlier PATCH.
Do not include response-only attributes, identity, ETag, or unchanged fields.

## Additional lifecycle, validation, and verification examples

| Purpose | Method | Stable path | Guard and verification |
|---|---|---|---|
| Inactivate | PATCH | `/reviewPeriods/{ReviewPeriodId}` | Status-only narrow delta after fresh usage check and separate approval; re-read the item. |
| Delete | DELETE | Fresh metadata-returned item link | Available only when current metadata advertises DELETE and zero usage/`InUseFlag=false` is proven; separate approval, then confirm the item is absent. |
| Validate Status Code | GET | `/fscmRestApi/resources/latest/commonLookups/ACTIVE_INACTIVE?expand=lookupCodes` | Query current enabled/effective values; map returned `LookupCode`, not display meaning. |
| Verify create/update/inactivation | GET | `/reviewPeriods/{ReviewPeriodId}?fields=*` | Compare requested fields, unchanged protected fields, status, and returned concurrency state after one write. |
