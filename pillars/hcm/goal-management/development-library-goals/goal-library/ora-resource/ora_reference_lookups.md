# Development Library Goal Reference Lookups

## Search and reuse evidence

`scripts/library_goal_search.py` delegates to Goal Management's
`goal-management-common/scripts/library_goal_search_contract.py`. Use its full envelope with
empty filters for duplicate checks. Only current action-supported fields may
use field-to-array filters such as `{"StatusCode":["A"]}`; never send legacy
`name/terms` or assume TypeCode is filterable. Keep status unfiltered for
duplicate checks. Source: [Oracle search schema](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-librarygoals-action-findbyadvancedsearchquery-post.html).

Complete pagination through the core client and run `assess_duplicate_evidence`
with exact name, Development variant and environment. Hydrate unknown types or
map meanings through current tenant metadata. A candidate is not proof of a
usable goal. Read its fresh returned item link, never a constructed numeric
GoalId URL, then run `verify_existing_goal_for_reuse` from
`goal-management-common/scripts/library_goal_create_payload.py` with all required dates and scope
fields. Preserve explicit keep/create choices. Unresolved evidence cannot turn
requested creates into completed tasks or prove visibility under UI filters.

Apply [Goal Management Dependent Setup Routing](../../../goal-management-common/dependent-setup-routing.md)
to every shared or cross-product reference. This task may read dependencies
for validation; dependency maintenance is an independent owner-routed task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| library_goal_resource_route | Before the first Development Library Goal management request | Connected environment | Validate `/hcmRestApi/resources/latest/libraryGoals/describe` first; use trusted current metadata/OpenAPI fallback only if the standard route is unavailable | Collection, search action, item and child links, supported methods, and any resolved numeric release returned by Fusion | Same configured host and expected object names only; reject any placeholder such as `rv:null` | In-memory `resourceRoot` and operation contract | Stop as transport/environment or contract blocker; never invent or persist the root |
| goal_variant_contract_lookup | Every request | development | Current runtime metadata plus approved OpenAPI when available | Resource, `DevCategoryCode`, `TypeCode`, children, operations | Requested variant fields and operation are exposed | Variant contract status and fingerprint | Block mutation and return metadata-mismatch plan |
| library_goal_availability_lookup | Create | Source availability statement; optional resolved Business Unit | Local Goal Setup Field Resolution plus current writable `Visible` and scope-field metadata | `Visible`, read-only `AvailableTo`, and `BusinessUnitId` when scoped | “All employees” resolves to `Visible=ALL`; Business Unit wording also requires one exact BusinessUnitId. “Required” does not request assignment. An absent inline enum is not a failure for the source-backed `ALL` mapping. | Canonical `Visible=ALL`, expected Available To meaning, optional BusinessUnitId, provenance | Block an unknown audience, nonwritable field, or unresolved Business Unit; never omit the audience and continue |
| library_goal_search | list/search or create idempotency | Free-text GoalName query, verified action fields, limit, offset | `{resourceRoot}/libraryGoals/action/findByAdvancedSearchQuery` using `scripts/library_goal_search.py` | Identity, name, type/status meaning, audience/scope, pagination | Full envelope, no TypeCode filter; verify Development type locally after complete pagination | Candidate rows, not proof of usability | Unknown type or incomplete pagination prevents a clear duplicate decision |
| library_goal_lookup | Existing target or create duplicate control | Supplied external ID when exposed or exact GoalName | Search action then fresh returned item link with supported fields/expansion; never synthesize an item key from numeric GoalId | Identity, GoalId, GoalExternalId, GoalName, variant, status, dates, scope, concurrency | Exact external ID plus variant preferred; otherwise exact GoalName within Development type; verify_existing_goal_for_reuse checks required fields after item hydration | Fresh verified target state or unresolved candidate | Return MISSING or unresolved evidence; do not skip creates or complete work from an untyped search hit |
| library_goal_child_collection_lookup | A standalone Library Goal Task or Target Outcome create is selected, or a parent create must be followed by child work | Fresh returned parent item and its child links | Use the returned `libraryGoalTasks` or `libGoalTargetOutcomes` child collection link from the parent response/read | Parent GoalId, returned composite parent identity, child collection link, current child rows, and concurrency when advertised | Use the fresh returned child collection link; never construct a BusinessGroupId/composite parent key from an input GoalId | Exact child collection route and duplicate-check rows | Block when the parent/child link is absent, stale, or does not belong to the selected variant/goal |
| target_outcome_lookup | A Target Outcome is selected for parent-create or standalone child-create | Selected subscription/section and an exact Content Item name or ID | Resolve trusted current hcm runtime root. GET `/targetOutcomeSubscriptionsLOV?finder=FindBySourceId;SourceId=119&fields=ContentTypeId,Description,Name,SectionId,SourceId,ValueSetName`, then GET `/contentItemsLov?finder=findByWord;ContentTypeId={ContentTypeId},ContentValueSetId={ValueSetName}&fields=ContentItemId,ContentSectionId,ContentTypeName,ContentValueSetCode,ContentValueSetId,GoalBusinessUnitName,GoalCategory,GoalDepartmentName,GoalJobFamilyName,GoalLegalEntityName,GoalSubType,ItemDescription,Name` with supported exact/word query and pagination. When several already returned ContentItemIds need hydration, POST `/contentItemsLov/action/getMultipleContentItemDetails` with `{"contentItems":"{commaSeparatedReturnedContentItemIds}"}` and ADF action media type | Subscription ContentTypeId, ValueSetName, SectionId; content ContentItemId, name/description, type/value-set metadata, scope fields; bulk action result only as advertised by current metadata | Select exactly one subscription and exactly one returned Content Item; bulk action accepts only a nonempty comma-separated set of current returned ContentItemIds. Respect returned scope/metadata and reject duplicate TypeItemId for the parent | `TypeId=ContentTypeId`, `TypeItemId=ContentItemId`, explicit RelationshipCode, and selection display evidence | Block zero/many subscription or item matches; never invent a TypeId/TypeItemId from a label or assume an undocumented bulk-action response schema |
| library_goal_lookup_values | A category, level, task, or goal type code is supplied or required | Submitted `DevCategoryCode`, `LevelCode`, PriorityCode, TaskTypeCode, UomCode, or goal variant | GET `/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` through Apps Common | LookupType, returned LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Retain only enabled codes effective today. Resolve exact code or one normalized exact meaning. Use `HRG_DEV_GOAL_CATEGORY`, `HRG_GOAL_MEASUREMENT_LEVEL`, `HRG_PRIORITY`, `HRG_GOAL_TASK_TYPE`, `HRG_GOAL_QUANTITATIVE_UOM`, or `HRG_GOAL_TYPE` as applicable | Validated codes/meanings and lookup provenance | Block a supplied/required code on zero or many effective matches; never submit display meanings or captured values |
| library_goal_usage_lookup | Delete is requested | Library Goal identity | Current exposed consumer reads | Reference identity and status | Count every page | Usage count and safe reference summary | Block delete when unavailable or nonzero |
| library_goal_translation_lookup | Translation list/read/update is selected | `LibraryGoalId`; returned goal-translation key; or returned task-translation key | Resolve the trusted current runtime root from `describe.openapi` for `libGoalTranslations` and `libGoalTaskTranslations`. List goal translations with `GET /libGoalTranslations?finder=findByGoalId;ContentItemId={LibraryGoalId}`; use `/libGoalTranslations/{returnedTranslationKey}` or `/libGoalTaskTranslations/{returnedTaskTranslationKey}` for an item | BusinessGroupId, ContentItemId, Language, `Name`, `Description`, `SuccessCriteria`, `TaskName`, `Comments`, and concurrency | Use only an exact returned identity. Never synthesize a key from language display text or assume task-key ordering | Current translation state, writable fields, and concurrency requirement | Block write when the current runtime root, item identity, or advertised operation is unavailable |
| library_goal_hdl_translation_context | `ContentItemTranslation.dat` is supplied with explicit HDL intent | Configured environment and supplied translation rows | Through `core.data-loader`, obtain current Content Item Translation template metadata; through declared read providers obtain base language, enabled languages, and exact existing parent evidence | Mandatory translation attributes, supported parent keys, base language, enabled language codes, and parent existence | Match each translation to a package GOAL source key or one exact existing target parent. Allow one non-base enabled language per parent. | Internal runtime context for enrichment, manifest generation, and validation | Block orphan, ambiguous, duplicate, disabled-language, or base-language rows; never ask the consultant for audit evidence |
| decimal_weight_policy_lookup | Fractional Library Goal weighting is supplied or policy is requested | Connected environment | `core.fusion-api.apps-common` using `HRG_ALLOW_DECIMALS_IN_WEIGHTS` as `ProfileOptionName` | Effective `HRG_ALLOW_DECIMALS_IN_WEIGHTS` value and provider provenance | One effective value only | `allow_decimal_weight` boolean and policy provenance | Return `PROVIDER_SKILL_UNAVAILABLE` when the declared common provider is unavailable; never call a profile endpoint or maintain the profile value here |

## Foundation Profile-Option Delegation

`HRG_ALLOW_DECIMALS_IN_WEIGHTS` is a conditional runtime policy lookup, not an
allowlist. A consultant request to inspect or maintain any exact profile option
is a separate foundation request: pass the supplied `profile_option_code`
unchanged as `ProfileOptionName` to external capability
`core.fusion-api.apps-common.profile-options` through the parent profile-option
routing contract. Query before proposing a provider-owned change. If the
foundation request requires a code and none is supplied, ask the consultant for
the exact code; do not substitute the decimal-weight policy. Return
`validation_gap` for an unknown or ambiguous code and
`PROVIDER_SKILL_UNAVAILABLE` when the provider is unavailable.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Development variant is selected | Set the development discriminator/fields from the public baseline and verify current updateability before preview |
| Child collections are returned | Read every page and preserve omitted values |
| A Library Goal create uses server External-ID derivation | Before create, prove current metadata has `hasDefaultValueExpression=true` for both `GoalId` and `GoalExternalId`; omit both fields, search exact `GoalName` within `TypeCode=DEVELOPMENT`, and disclose the derivation in preview. After create, re-read when needed and verify returned `GoalExternalId` equals returned `GoalId`; otherwise return verification failure. |
| A Library Goal create returns HTTP 201 | Treat the response as provisional. Use response `GoalId` only when present, then re-read the exact created row by returned identity or approved idempotency key. Run `verify_created_goal`; require exact non-null GoalName, TypeCode, StatusCode, Visible, matching AvailableTo meaning, and every approved scope field before success or child work. Never guess the parent composite key. |
| Exact duplicate search finds null lifecycle or audience | Run `classify_existing_goal`. Return `INVALID_EXISTING_LIBRARY_GOAL_STATE` and stop before automatic suffix/punctuation replacement. |
| Standalone Task or Target Outcome create is requested | Re-read the selected parent's returned child collection. Create only through that fresh link; Tasks return a three-part child identity and Target Outcomes return `ContentItemRlatId`. Preserve returned links and use them for later item work. |
| Target Outcome picker is used | Resolve a SourceId=119 subscription first, then use its returned ContentTypeId and ValueSetName to page `contentItemsLov`. Map only returned IDs; apply the returned content scope fields before preview. To hydrate multiple already returned selections, POST `contentItemsLov/action/getMultipleContentItemDetails` with `contentItems` as a comma-separated string of those IDs and ADF action media type. Treat its response shape as metadata-governed and read-only. |
| Category, level, task, or Goal Type lookup is used | Resolve the corresponding public Apps Common `commonLookups/{LookupType}?expand=lookupCodes` route. Validate enabled/effective returned LookupCode values, not Meaning labels. |

## Foundation Lookup Delegation

The `HRG_*` types above are current runtime validation inputs for the selected
Development Library Goal. A consultant request to inspect or maintain an exact
lookup type/code requires external capability
`core.fusion-api.apps-common.lookups` through the parent
lookup-routing contract. Never mutate a lookup or place a lookup
mutation in a Library Goal payload.

## Foundation Value-Set Delegation

The Target Outcome `ValueSetName` returned by current subscription metadata is
a read-only `contentItemsLov` selector for this task. A consultant request to
inspect or maintain an exact Foundation value-set code routes separately to
external capability `core.fusion-api.apps-common.value-sets`
through the parent value-set routing contract; never mutate that value set
through a Library Goal payload.

## Foundation Flexfield Delegation

A consultant-supplied exact Descriptive Flexfield code is a separate foundation
request. Require external capability
`core.fusion-api.apps-common.descriptive-flexfields` using
`HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD` and the parent flexfield
routing contract. `dff_changes` may carry only explicitly requested runtime
business data after current `libraryGoals` metadata confirms the field; it
never configures, deploys, or imports a DFF.
| Many identity matches remain | Stop and require disambiguation |
| Standard route is resolved | Prefer `/hcmRestApi/resources/latest`; a numeric release in returned self/canonical links is Fusion's resolution of `latest`, not a version to hardcode |
| Standard route is unavailable | Resolve a trusted current runtime route before preview, reject `rv:null`, and never change routes after approval |
| Authentication is not yet established | Make one harmless serialized metadata/read request first; do not start parallel first-use requests that can contend for the same OAuth callback |
| Search action is HTTP POST | Classify it as READ because the action only evaluates a query; no mutation approval is required |
| Development Library Goal search/list | Build the action body with `scripts/library_goal_search.py`. Do not place `TypeCode`, `StatusCode`, or any metadata-queryable field in the free-text `query` expression unless current action metadata explicitly supports it. |
| Creation-time filter is requested | Resolve an exact UTC interval, hydrate missing detail fields, filter locally, and sort newest first |
| Translation route is needed | Resolve the trusted current runtime root from current `describe.openapi`. Use the concrete `libGoalTranslations` and `libGoalTaskTranslations` resources; use the supplied goal finder only for goal translations and use only a current OpenAPI-advertised finder for task translations. Do not cache tenant runtime literals |
| Decimal-weight provider returns `N` | Round a non-null weighting using the verified runtime rule before payload mapping, then show and verify the persisted integer value |
| Decimal-weight provider is absent | Return `PROVIDER_SKILL_UNAVAILABLE` for external capability `core.fusion-api.apps-common.profile-options`; do not substitute a direct profile-value REST call |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.LOOKUPS | step | 40 | reference_lookup | resolved->GOAL_LIBRARY.DEFAULTS;unresolved->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.DEPENDENCIES | stop | Variant, identity, references, or usage must be resolved |
| GOAL_LIBRARY.SEARCH | step | 26 | reference_lookup | found->GOAL_LIBRARY.DONE_SEARCH;empty->GOAL_LIBRARY.DONE_SEARCH;unavailable->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | list/search is selected for one explicit variant |
| GOAL_LIBRARY.DECIMAL_POLICY_READ | step | 246 | reference_lookup | found->GOAL_LIBRARY.DONE_DECIMAL_POLICY_READ;unavailable->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | Decimal-weight policy read is selected through the owning provider |


---

# Development Library Goal REST Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| `/hcmRestApi/resources/latest/libraryGoals/describe` | Preferred release-independent route validation and current shared development attributes, children, and operations |
| Trusted current REST link/metadata or approved OpenAPI | Fallback only when the standard `latest` route is unavailable |
| shared setup export/import skills | Catalog-supported FSM CSV routes |

## Execution Contract

| Situation | What Happens |
|---|---|
| Get | Resolve one goal and return parent plus requested child collections |
| List/search | Use scripts/library_goal_search.py, complete pagination, hydrate requested details, and verify Development type locally. query is GoalName free text; only current action-supported fields may be server filters. |
| Create | Preserve and length-validate a supplied `GoalExternalId`; never alter it. If it is omitted and metadata has `hasDefaultValueExpression=true` for both `GoalId` and `GoalExternalId`, omit both fields, run exact `GoalName` within `TypeCode=DEVELOPMENT` duplicate controls, disclose server derivation in preview, create inactive, and verify returned `GoalExternalId` equals returned `GoalId`. Otherwise use those exact duplicate controls with explicit duplicate-risk acknowledgement and never invent an ID. A verified parent POST may include optional `libraryGoalMeasures`, `libraryGoalTasks`, and `libGoalTargetOutcomes` arrays. Use response `GoalId` and returned child links when present; otherwise re-read the exact created goal before any follow-on child call. |
| Update | Patch explicit parent/child changes and preserve omitted collections; validate current concurrency metadata and use the returned optimistic-lock contract when advertised |
| Add a Library Goal Task | Re-read the selected parent and use its fresh returned `libraryGoalTasks` child collection link. POST only explicit task fields, then retain the returned item identity/link and re-read the child collection. |
| Add a Target Outcome | Re-read the selected parent and use its fresh returned `libGoalTargetOutcomes` child collection link. POST `TypeId`, `TypeItemId`, and `RelationshipCode`; reject a duplicate TypeItemId and re-read the child collection. |
| Activate or inactivate | Run independently after a fresh read and separate approval |
| Delete | Require zero references and separate delete approval; otherwise prefer inactivation |
| Development variant | Use the same `libraryGoals` resource with `DevCategoryCode`; stop only when current metadata does not verify the requested fields/operation |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Search/list | POST (read-only action) | `{resourceRoot}/libraryGoals/action/findByAdvancedSearchQuery` |
| Read | GET | `{resourceRoot}/libraryGoals/{LibraryGoalId}?fields=*` with requested child expansion or the fresh returned item/child path |
| Create parent, optionally with children | POST | `{resourceRoot}/libraryGoals`; may include verified `libraryGoalMeasures`, `libraryGoalTasks`, and `libGoalTargetOutcomes` arrays in the parent body. Use returned GoalId and parent/child links; when absent, re-read the exact created parent before later child work |
| Update, activate, or inactivate | PATCH | `{resourceRoot}/libraryGoals/{LibraryGoalId}` or fresh returned child paths |
| Delete | DELETE | Fresh returned item path after zero-reference proof |
| Add Library Goal Task | POST | Fresh returned `{libraryGoalTasksCollectionLink}` from the selected parent; map explicit task fields such as TaskName, Description, dates, TaskTypeCode, PriorityCode, Comments, UomCode, and only applicable target fields. The returned item identity is `TaskContentId,BusinessGroupId,TaskId` |
| Add Target Outcome | POST | Fresh returned `{libGoalTargetOutcomesCollectionLink}` from the selected parent with `{TypeId,TypeItemId,RelationshipCode}`. The returned child identity is `ContentItemRlatId` |
| List Target Outcome subscriptions | GET | `{hcmRuntimeRoot}/targetOutcomeSubscriptionsLOV?finder=FindBySourceId;SourceId=119&fields=ContentTypeId,Description,Name,SectionId,SourceId,ValueSetName`; select one returned subscription before listing content items |
| List Target Outcome content items | GET | `{hcmRuntimeRoot}/contentItemsLov?finder=findByWord;ContentTypeId={returnedContentTypeId},ContentValueSetId={returnedValueSetName}&fields=ContentItemId,ContentSectionId,ContentTypeName,ContentValueSetCode,ContentValueSetId,GoalBusinessUnitName,GoalCategory,GoalDepartmentName,GoalJobFamilyName,GoalLegalEntityName,GoalSubType,ItemDescription,Name` with supported query and pagination; map TypeId from ContentTypeId and TypeItemId from ContentItemId |
| Hydrate multiple Target Outcome content items | POST (read-only ADF action) | `{hcmRuntimeRoot}/contentItemsLov/action/getMultipleContentItemDetails` with `Content-Type: application/vnd.oracle.adf.action+json` and body `{ "contentItems": "{commaSeparatedReturnedContentItemIds}" }`; use only IDs from the current content-items read and parse only the response fields advertised by current metadata |
| Validate category, level, task, and goal type codes | GET | `{restBaseUrl}/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` through Apps Common; filter enabled/effective rows and map only a returned `LookupCode` |
| List Goal translations | GET | `{translationRuntimeRoot}/libGoalTranslations?finder=findByGoalId;ContentItemId={LibraryGoalId}` |
| Read or update Goal translation | GET or PATCH | `{translationRuntimeRoot}/libGoalTranslations/{returnedTranslationKey}`; map only `Name`, `Description`, and `SuccessCriteria` for PATCH |
| List Task translations | GET | `{translationRuntimeRoot}/libGoalTaskTranslations` with only the collection finder advertised by current OpenAPI metadata |
| Read or update Task translation | GET or PATCH | `{translationRuntimeRoot}/libGoalTaskTranslations/{returnedTaskTranslationKey}`; map only `TaskName` and `Comments` for PATCH |
| Read decimal-weight policy | Owning-provider read | External capability `core.fusion-api.apps-common.profile-options` for `HRG_ALLOW_DECIMALS_IN_WEIGHTS`; no direct profile endpoint or profile mutation |

## Required Media Type

Select the media type before sending the first request. Do not probe Fusion by
cycling through content types after a failure.

| Request shape | Required header |
|---|---|
| Top-level JSON object contains a `parts` array | `Content-Type: application/vnd.oracle.adf.batch+json` |
| Custom action path contains `/action/`, including `findByAdvancedSearchQuery` | `Content-Type: application/vnd.oracle.adf.action+json` |
| Ordinary entity or child POST, PUT, or PATCH with a JSON body | `Content-Type: application/json` |
| Ordinary GET with no body | `Accept: application/json`; omit request `Content-Type` |

Batch classification has precedence whenever the top-level `parts` array is
present. Otherwise, the search/list endpoint above is always an ADF action and
must use the action media type. Apply the same rule to development requests, and fail closed if the selected header conflicts with
the path or payload shape.

Set `resourceRoot` to `/hcmRestApi/resources/latest` after validating the
Library Goal describe route. A numeric release in a returned self/canonical
link is Fusion's resolution of `latest`, not a version to hardcode. Only if the
standard route is unavailable may trusted current metadata resolve a volatile
runtime root before preview. Reject placeholder roots such as `rv:null`, and
never switch routes after approval. Never store the host, runtime revision,
language/release suffix, composite item keys, or concurrency headers.

Establish authentication with one harmless serialized metadata/read call before
starting multiple reads. Do not launch parallel first-use calls while the token
may be absent or expired, and never parallelize mutations. Execute all calls through
`core.auth.fusion-oauth-authentication` and
`core.fusion-api.rest-api-client` with the secure per-user cache. Chrome is
limited to an OAuth sign-in handoff or an explicitly requested UI test.

The search POST is semantically read-only and bypasses all mutation approval
nodes. Create, update, status, delete, and import operations never do.

## Parent-create and known child-create contracts

The verified parent create accepts the Development Library Goal parent fields
and may include nested `libraryGoalMeasures`, `libraryGoalTasks`, and
`libGoalTargetOutcomes` arrays. The parent response can return `GoalId`, a
composite parent key, child collections, child item keys, and child links. Map
only fields explicitly requested and current-metadata writable. A compact
success response is not an error: re-read the exact created parent before any
separate child POST when it does not expose a usable ID/link.

For an existing parent, the verified standalone creates are ordinary JSON POSTs
to the fresh returned child collection links. A Task create returns the exact
three-part item identity `TaskContentId,BusinessGroupId,TaskId`; a Target
Outcome create returns `ContentItemRlatId`. Treat those values and their
returned links as opaque. Do not construct composite keys, infer a child update
or delete path, or add a `libraryGoals/batch` route until current metadata or a
captured canonical request proves that operation.

## Target Outcome and Task code resolution

Before mapping a Target Outcome, list subscriptions with `SourceId=119` and
select one returned row. Its `ContentTypeId` and `ValueSetName` are the only
permitted inputs for the `contentItemsLov` finder. Select one returned
ContentItemId and map `TypeId=ContentTypeId` and `TypeItemId=ContentItemId`;
the response label is display evidence only. Page content items and reject an
ambiguous selection, a returned scope mismatch, or a duplicate TypeItemId.

Before a Task mutation, validate its `PriorityCode`, `TaskTypeCode`, and
`UomCode` through public Apps Common lookup types `HRG_PRIORITY`,
`HRG_GOAL_TASK_TYPE`, and `HRG_GOAL_QUANTITATIVE_UOM`. Validate
`DevCategoryCode` and `LevelCode` through `HRG_DEV_GOAL_CATEGORY` and
`HRG_GOAL_MEASUREMENT_LEVEL` when those fields are supplied or required. When a Goal Type lookup is
needed, use `HRG_GOAL_TYPE` and require its returned LookupCode to agree with
the selected PERFORMANCE or DEVELOPMENT variant. Map LookupCode values only;
never map a display Meaning. The observed `getMultipleContentItemDetails`
action is a read-only ADF POST whose body is a `contentItems` comma-separated
string. Use it only to hydrate multiple IDs returned by the current
`contentItemsLov` query; never use labels or invented IDs, and do not assume a
response schema beyond current metadata.

## Translation and decimal-weight contracts

| Functional flow | Contract status | Execution rule |
|---|---|---|
| Goal translation list, read, and update | OpenAPI-confirmed runtime resource | Resolve the current `libGoalTranslations` root. List with `findByGoalId;ContentItemId={LibraryGoalId}`; use the returned `BusinessGroupId,ContentItemId,Language` key for GET/PATCH. Map only `Name`, `Description`, and `SuccessCriteria`; preserve base language, preview/approve once, and re-read after save |
| Task translation list, read, and update | OpenAPI-confirmed runtime resource | Resolve the current `libGoalTaskTranslations` root. Use only its current OpenAPI-advertised finder and returned item key. Map only `TaskName` and `Comments`; preserve base language, preview/approve once, and re-read after save |
| Decimal-weight policy | VBCS evidence plus owning-provider lookup | Read `HRG_ALLOW_DECIMALS_IN_WEIGHTS` through `core.fusion-api.apps-common.profile-options`. `N` means round a non-null weight before save; absent provider means `PROVIDER_SKILL_UNAVAILABLE` and blocks a fractional-weight write |

## Preview Pattern

Use `scripts/library_goal_payload.py` to render the field-level create preview
and canonical SHA-256 fingerprint from the final payload. The user must select
any suggested replacement external ID before this preview is regenerated. The
preview must disclose server `GoalExternalId` derivation when applicable and
must be rebuilt for every payload change; a changed fingerprint always requires
a fresh, separate approval.

| Step | Requirement |
|---|---|
| 1 | Verify variant contract and cache lean current updateable metadata |
| 2 | Re-read full requested parent/child state |
| 3 | Run `scripts/library_goal_payload.py`; generate the saved mapped payload and report with materialized StatusCode, Visible, and TypeCode defaults; show environment, operation, exact identity, every supplied field/value, optional omissions, exact duplicate control, server External-ID derivation when applicable, child-collection effect, and complete JSON payload; retain the fingerprint internally |
| 4 | Apply the [shared Goal Management approval convention](../../../goal-management-common/approval-convention.md). Accept a clear contextual affirmative only for one immediately preceding unchanged preview, identified operation, or explicitly combined batch. Any payload change invalidates that approval; activation and delete remain separate unless both appear in one exact approved batch |

## Live Pattern

| Step | Requirement |
|---|---|
| 1 | Recheck identity, variant, references, metadata, concurrency, and fingerprint; reject a stale optimistic-lock state and rebuild the preview from the winning server state |
| 2 | Submit one mutation once; never chain activation from create/update |
| 3 | Re-read the complete parent with `fields=*` (or an explicit complete field set), expand/re-read affected children, and classify outcome. For create, run the helper's exact verification and block completion on null or mismatched key fields. Do not treat fields omitted by Fusion's compact default response as null; hydrate first. |
| 4 | Never replay an ambiguous mutation automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.READ | step | 25 | reference_lookup | found->GOAL_LIBRARY.DONE_READ;missing->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | get is selected and the variant read contract is verified |
| GOAL_LIBRARY.REST_DESCRIBE | step | 70 | reference_lookup | ready->GOAL_LIBRARY.REST_PAYLOAD;unavailable->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.DESIGN | stop | A variant-supported mutation is selected |
| GOAL_LIBRARY.REST_PAYLOAD | step | 80 | reference_lookup | mapped->GOAL_LIBRARY.WRITE_ROUTE;rejected->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_DESCRIBE | stop | Current variant metadata is available |
| GOAL_LIBRARY.CREATE_PREVIEW | decision | 100 | reference_lookup | reviewed->GOAL_LIBRARY.CREATE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | create is selected |
| GOAL_LIBRARY.CREATE_APPROVAL | decision | 110 | reference_lookup | approved->GOAL_LIBRARY.CREATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.CREATE_PREVIEW | stop | Final inactive-create preview is reviewed |
| GOAL_LIBRARY.CREATE | step | 120 | reference_lookup | created->GOAL_LIBRARY.CREATE_VERIFY;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.CREATE_APPROVAL | stop | Approved create is ready |
| GOAL_LIBRARY.CREATE_VERIFY | step | 121 | reference_lookup | verified->GOAL_LIBRARY.DONE_CREATED;invalid_state->GOAL_LIBRARY.BLOCKED;ambiguous->GOAL_LIBRARY.UNKNOWN | GOAL_LIBRARY.CREATE | stop | HTTP 201 returned and the exact created Development Library Goal must pass key-field and audience verification |
| GOAL_LIBRARY.UPDATE_PREVIEW | decision | 130 | reference_lookup | reviewed->GOAL_LIBRARY.UPDATE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | update is selected |
| GOAL_LIBRARY.UPDATE_APPROVAL | decision | 140 | reference_lookup | approved->GOAL_LIBRARY.UPDATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.UPDATE_PREVIEW | stop | Final update preview and child diff are reviewed |
| GOAL_LIBRARY.UPDATE | step | 150 | reference_lookup | verified->GOAL_LIBRARY.DONE_UPDATED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.UPDATE_APPROVAL | stop | Approved update is ready |
| GOAL_LIBRARY.ACTIVATE_PREVIEW | decision | 160 | reference_lookup | reviewed->GOAL_LIBRARY.ACTIVATE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | activate is independently selected |
| GOAL_LIBRARY.ACTIVATE_APPROVAL | decision | 170 | reference_lookup | approved->GOAL_LIBRARY.ACTIVATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.ACTIVATE_PREVIEW | stop | Final activation preview is reviewed |
| GOAL_LIBRARY.ACTIVATE | step | 180 | reference_lookup | verified->GOAL_LIBRARY.DONE_ACTIVATED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.ACTIVATE_APPROVAL | stop | Approved activation is ready |
| GOAL_LIBRARY.INACTIVATE_PREVIEW | decision | 190 | reference_lookup | reviewed->GOAL_LIBRARY.INACTIVATE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | inactivate is independently selected |
| GOAL_LIBRARY.INACTIVATE_APPROVAL | decision | 200 | reference_lookup | approved->GOAL_LIBRARY.INACTIVATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.INACTIVATE_PREVIEW | stop | Final inactivation preview is reviewed |
| GOAL_LIBRARY.INACTIVATE | step | 210 | reference_lookup | verified->GOAL_LIBRARY.DONE_INACTIVATED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.INACTIVATE_APPROVAL | stop | Approved inactivation is ready |
| GOAL_LIBRARY.DELETE_PREVIEW | decision | 220 | reference_lookup | reviewed->GOAL_LIBRARY.DELETE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | delete is selected and zero references are proven |
| GOAL_LIBRARY.DELETE_APPROVAL | decision | 230 | reference_lookup | approved->GOAL_LIBRARY.DELETE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.DELETE_PREVIEW | stop | Final guarded delete preview is reviewed |
| GOAL_LIBRARY.DELETE | step | 240 | reference_lookup | verified->GOAL_LIBRARY.DONE_DELETED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.DELETE_APPROVAL | stop | Approved delete is ready |
| GOAL_LIBRARY.TRANSLATION_SEARCH | step | 245 | reference_lookup | found->GOAL_LIBRARY.DONE_TRANSLATION_READ;empty->GOAL_LIBRARY.DONE_TRANSLATION_READ;unavailable->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | Translation list or item read is selected |
| GOAL_LIBRARY.TRANSLATION_PREVIEW | decision | 247 | reference_lookup | reviewed->GOAL_LIBRARY.TRANSLATION_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | One translation update has a verified current contract |
| GOAL_LIBRARY.TRANSLATION_APPROVAL | decision | 248 | reference_lookup | approved->GOAL_LIBRARY.TRANSLATION_UPDATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.TRANSLATION_PREVIEW | stop | Final translation update preview is reviewed |
| GOAL_LIBRARY.TRANSLATION_UPDATE | step | 249 | reference_lookup | verified->GOAL_LIBRARY.DONE_TRANSLATION_UPDATED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.TRANSLATION_APPROVAL | stop | Approved translation update is ready |


---

# Development Library Goal Captured API Path Reference

The supplied captures establish these stable paths and request shapes. They do
not make the captured tenant host, runtime revision, release suffix, IDs, or
payload literals reusable contract values.

| Purpose | Method | Stable path | Runtime values and payload guidance |
|---|---|---|---|
| Create Development Library Goal | POST | `/libraryGoals` | Map only current metadata-supported parent/optional child fields. `TypeCode=DEVELOPMENT` and `DevCategoryCode` are variant fields. |
| Search Library Goals | POST | `/libraryGoals/action/findByAdvancedSearchQuery` | Full ADF action envelope; verify Development type locally after complete pagination. |
| Read one Library Goal | GET | `/libraryGoals/{LibraryGoalId}` | Resolve `LibraryGoalId` from the current selected/search/create result and request necessary child expansion. |
| List Target Outcome subscriptions | GET | `/targetOutcomeSubscriptionsLOV` | `SourceId` is a current selector; select one returned subscription before deriving content-item criteria. |
| List Target Outcome content items | GET | `/contentItemsLov` | `ContentTypeId` and `ContentValueSetId`/value-set name come from the selected subscription; search criteria and pagination are runtime inputs. |
| Add Target Outcome | POST | `/libraryGoals/{LibraryGoalId}/child/libGoalTargetOutcomes` | Prefer the fresh returned collection link. Body maps `TypeId`, `TypeItemId`, and `RelationshipCode` from the current content-item selection. |
| Add Library Goal Task | POST | `/libraryGoals/{LibraryGoalId}/child/libraryGoalTasks` | Prefer the fresh returned collection link. Map only explicit applicable task fields; the captured call is a create, not a fetch. |
| Validate category, level, goal, and task codes | GET | `/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` | Resolve `LookupType` and an exact code/meaning at runtime; use only enabled/effective returned LookupCode values. This is validation-only. |

Library Goal/LOV business-object paths resolve from the current HCM root;
common lookups resolve from the current FSCM root. A captured item ID must
never become the parent for a later task or Target Outcome create.

## Mutation preflight and verification

Before every Library Goal parent or child mutation, resolve current
`/libraryGoals/describe` metadata to confirm the requested method, writable
fields, child capability, media type, and concurrency contract. A new parent
create uses an exact Development duplicate search because no target item yet
exists. For update, status, delete, task, Target Outcome, or translation work,
immediately GET the parent and relevant child/item link before preview and use
the returned ETag or other optimistic-lock state when supplied. Submit once,
then re-read the changed parent/child/translation to verify. A capture's ETag,
child key, or content-item selection must never be reused.

## Narrow-delta payload rule

The captured `libraryGoals` create body may demonstrate optional
`libraryGoalMeasures`, `libraryGoalTasks`, and `libGoalTargetOutcomes` arrays
for one Development use case. It is not an update template. A parent update
maps only explicitly requested writable scalar fields and never replays an
embedded child array or unchanged captured field. A task or Target Outcome is
one targeted child create/update/delete using its current returned child link
and only its requested fields. Do not include parent identity, ETag, returned
links, read-only attributes, or unrelated content-item values in the body.

## Additional lifecycle, child-maintenance, translation, validation, and verification examples

| Purpose | Method | Stable path | Guard and verification |
|---|---|---|---|
| Activate or inactivate | PATCH | `/libraryGoals/{LibraryGoalId}` | Status-only narrow delta after fresh read and separate approval; re-read the parent. |
| Delete parent | DELETE | Fresh metadata-returned Library Goal item link | Only when current metadata advertises DELETE and zero references are proven; separate approval, then confirm absence. |
| Add/update/delete a measure, task, or Target Outcome | Current metadata-advertised child method | Fresh returned child collection/item link | Use the child’s returned identity and a narrow body. Do not infer an update/delete path from a captured create. Re-read the affected child collection. |
| List/read/update goal translation | GET/PATCH | `/libGoalTranslations` and fresh returned translation item link | List by current goal ID, then map only `Name`, `Description`, and `SuccessCriteria`; preserve base language and re-read. |
| List/read/update task translation | GET/PATCH | `/libGoalTaskTranslations` and fresh returned task-translation item link | Use only the current OpenAPI-advertised finder/key; map only `TaskName` and `Comments`, then re-read. |
| Validate category, level, goal/task codes and decimal policy | GET / owning-provider read | `/fscmRestApi/resources/latest/commonLookups/{LookupType}` / `HRG_ALLOW_DECIMALS_IN_WEIGHTS` provider | Use enabled/effective returned LookupCodes for category, level, goal, and task fields; obtain fractional-weight policy only from the owning provider. |
| Verify parent/child/translation write | GET | Fresh parent, child, or translation item link | Confirm the approved delta and preserved sibling collections after one write. |
