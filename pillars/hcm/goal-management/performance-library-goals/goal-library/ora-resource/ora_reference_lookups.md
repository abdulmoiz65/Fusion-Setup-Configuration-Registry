# Performance Library Goal Reference Lookups

Apply [Goal Management Dependent Setup Routing](../../../goal-management-common/dependent-setup-routing.md)
to every shared or cross-product reference. This task may read dependencies
for validation; dependency maintenance is an independent owner-routed task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| library_goal_resource_route | Before the first Performance Library Goal management request | Connected environment | Validate `/hcmRestApi/resources/latest/libraryGoals/describe` first; use trusted current metadata/OpenAPI fallback only if the standard route is unavailable | Collection, search action, item and child links, supported methods, and any resolved numeric release returned by Fusion | Same configured host and expected object names only; reject any placeholder such as `rv:null` | In-memory `resourceRoot` and operation contract | Stop as transport/environment or contract blocker; never invent or persist the root |
| goal_variant_contract_lookup | Every request | performance | Current runtime metadata plus approved OpenAPI when available | Resource, `PerfCategoryCode` requiredness/writability, `TypeCode`, children, operations, External ID maximum length, and server default-expression flags for `GoalId`/`GoalExternalId` when exposed | `TypeCode=PERFORMANCE` and requested operation are exposed. `PerfCategoryCode` is mapped only when supplied or metadata-required | Variant contract status, field metadata, and fingerprint | Block mutation and return metadata-mismatch plan |
| library_goal_availability_lookup | Create | Source availability statement; optional resolved Business Unit | Local Goal Setup Field Resolution plus current writable `Visible` and scope-field metadata | `Visible`, read-only `AvailableTo`, and `BusinessUnitId` when scoped | “All employees” resolves to `Visible=ALL`; Business Unit wording also requires one exact BusinessUnitId. “Required” does not request assignment. An absent inline enum is not a failure for the source-backed `ALL` mapping. | Canonical `Visible=ALL`, expected Available To meaning, optional BusinessUnitId, provenance | Block an unknown audience, nonwritable field, or unresolved Business Unit; never omit the audience and continue |
| library_goal_search | list/search or create idempotency | Goal Name free text, verified action filters, limit, offset | `{resourceRoot}/libraryGoals/action/findByAdvancedSearchQuery` | Identity, name, variant, status, dates, pagination | Use `goal-management-common/scripts/library_goal_search_contract.py`; no TypeCode action filter. Hydrate and retain exact Performance candidates locally. | Candidate rows, not proof of usability | Unknown type or incomplete pagination prevents a clear duplicate decision |
| library_goal_lookup | Existing target or create idempotency | Returned ID, external ID when exposed, or exact name within variant | Search action then `{resourceRoot}/libraryGoals/{LibraryGoalId}?fields=*` with requested child expansion, or the fresh returned item link | Identity, variant fields, status, collections, `CreationDate`, concurrency | Exact external ID+variant preferred; otherwise exact name within Performance type | Fresh complete target state or duplicate candidate | Return MISSING or require duplicate reconciliation |
| library_goal_parent_update_contract | Parent scalar update, including Weighting | Fresh full selected parent and current Library Goal metadata | Resolve the fresh returned self/canonical parent item link and the currently advertised update method, media type, request path, and concurrency requirements | Prefer the advertised item PATCH contract. Select ADF batch only when current metadata explicitly enables it and returns a same-host batch root plus part shape. | Every operation must target its fresh opaque `libraryGoals` item identity. Treat an ETag as state evidence only; send a concurrency header only when the selected operation contract declares it. | In-memory method, media type, request path, fresh opaque item path, writable schema, concurrency rule, and explicit batch-enabled flag when applicable | Block if no current update contract or exact parent identity is available; never infer batch from one-approval wording or substitute `performanceGoalsV2` |
| library_goal_child_collection_lookup | A standalone Library Goal Task or Target Outcome create is selected, or a parent create must be followed by child work | Fresh returned parent item and its child links | Use the returned `libraryGoalTasks` or `libGoalTargetOutcomes` child collection link from the parent response/read | Parent GoalId, returned composite parent identity, child collection link, current child rows, and concurrency when advertised | Use the fresh returned child collection link; never construct a BusinessGroupId/composite parent key from an input GoalId | Exact child collection route and duplicate-check rows | Block when the parent/child link is absent, stale, or does not belong to the selected variant/goal |
| target_outcome_lookup | A Target Outcome is selected for parent-create or standalone child-create | Selected subscription/section and an exact Content Item name or ID | Resolve trusted current hcm runtime root. GET `/targetOutcomeSubscriptionsLOV?finder=FindBySourceId;SourceId=119&fields=ContentTypeId,Description,Name,SectionId,SourceId,ValueSetName`, then GET `/contentItemsLov?finder=findByWord;ContentTypeId={ContentTypeId},ContentValueSetId={ValueSetName}&fields=ContentItemId,ContentSectionId,ContentTypeName,ContentValueSetCode,ContentValueSetId,GoalBusinessUnitName,GoalCategory,GoalDepartmentName,GoalJobFamilyName,GoalLegalEntityName,GoalSubType,ItemDescription,Name` with supported exact/word query and pagination. When several already returned ContentItemIds need hydration, POST `/contentItemsLov/action/getMultipleContentItemDetails` with `{"contentItems":"{commaSeparatedReturnedContentItemIds}"}` and ADF action media type | Subscription ContentTypeId, ValueSetName, SectionId; content ContentItemId, name/description, type/value-set metadata, scope fields; bulk action result only as advertised by current metadata | Select exactly one subscription and exactly one returned Content Item; bulk action accepts only a nonempty comma-separated set of current returned ContentItemIds. Respect returned scope/metadata and reject duplicate TypeItemId for the parent | `TypeId=ContentTypeId`, `TypeItemId=ContentItemId`, explicit RelationshipCode, and selection display evidence | Block zero/many subscription or item matches; never invent a TypeId/TypeItemId from a label or assume an undocumented bulk-action response schema |
| library_goal_lookup_values | A category, subtype, level, task, or goal type code is supplied or required | Submitted `PerfCategoryCode`, `GoalSubTypeCode`, `LevelCode`, PriorityCode, TaskTypeCode, UomCode, or goal variant | GET `/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` through Apps Common | LookupType, returned LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Retain only enabled codes effective today. Resolve exact code or one normalized exact meaning. Use `HRG_PERF_GOAL_CATEGORY`, `HRG_SUB_TYPE_CODE`, `HRG_GOAL_MEASUREMENT_LEVEL`, `HRG_PRIORITY`, `HRG_GOAL_TASK_TYPE`, `HRG_GOAL_QUANTITATIVE_UOM`, or `HRG_GOAL_TYPE` as applicable | Validated codes/meanings and lookup provenance | Block a supplied/required code on zero or many effective matches; never submit display meanings or captured values |
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
| Child collections are returned | Read every page and preserve omitted values |
| A Library Goal create returns HTTP 201 | Treat the response as provisional. Use response `GoalId` only when present, then re-read the exact created row by returned identity or approved idempotency key. Run `verify_created_goal`; require exact non-null GoalName, TypeCode, StatusCode, Visible, matching AvailableTo meaning, and every approved scope field before success or child work. Never guess the parent composite key. |
| Exact duplicate search finds null lifecycle or audience | Run `classify_existing_goal`. Return `INVALID_EXISTING_LIBRARY_GOAL_STATE` and stop before automatic suffix/punctuation replacement. |
| External ID is omitted on create | Only when current metadata exposes server default expressions for both `GoalId` and `GoalExternalId`, omit both fields, use exact Goal Name plus `TypeCode=PERFORMANCE` duplicate controls, and state the server-derived identity in preview. After create, re-read and require returned `GoalExternalId` to equal returned `GoalId`; a mismatch is a contract blocker for future omitted-External-ID creates. |
| Standalone Task or Target Outcome create is requested | Re-read the selected parent's returned child collection. Create only through that fresh link; Tasks return a three-part child identity and Target Outcomes return `ContentItemRlatId`. Preserve returned links and use them for later item work. |
| Target Outcome picker is used | Resolve a SourceId=119 subscription first, then use its returned ContentTypeId and ValueSetName to page `contentItemsLov`. Map only returned IDs; apply the returned content scope fields before preview. To hydrate multiple already returned selections, POST `contentItemsLov/action/getMultipleContentItemDetails` with `contentItems` as a comma-separated string of those IDs and ADF action media type. Treat its response shape as metadata-governed and read-only. |
| Category, subtype, level, task, or Goal Type lookup is used | Resolve the corresponding public Apps Common `commonLookups/{LookupType}?expand=lookupCodes` route. Validate enabled/effective returned LookupCode values, not Meaning labels. |

## Foundation Lookup Delegation

The `HRG_*` types above are current runtime validation inputs for the selected
Performance Library Goal. A consultant request to inspect or maintain an exact
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
| Performance Library Goal advanced search | Use the complete shared Library Goal search envelope below. Resolve the Performance discriminator locally from returned codes or current tenant meaning mappings; hydrate unknown types before deciding. |
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

# Performance Library Goal REST Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| `/hcmRestApi/resources/latest/libraryGoals/describe` | Preferred release-independent route validation and current shared performance attributes, children, and operations |
| Trusted current REST link/metadata or approved OpenAPI | Fallback only when the standard `latest` route is unavailable |
| shared setup export/import skills | Catalog-supported FSM CSV routes |

## Execution Contract

| Situation | What Happens |
|---|---|
| Get | Resolve one goal and return parent plus requested child collections |
| List/search | Run the read-only advanced-search action for one variant, page results, hydrate requested details, apply local filters, and return a sanitized list |
| Create | Search using a supplied immutable External ID when present. When current `GoalId` and `GoalExternalId` metadata both expose server default expressions, omit both IDs, use exact Goal Name plus `TypeCode=PERFORMANCE` duplicate controls, disclose the server-derived identity in preview, create inactive, and verify returned `GoalExternalId` equals returned `GoalId`. A verified parent POST may include optional `libraryGoalMeasures`, `libraryGoalTasks`, and `libGoalTargetOutcomes` arrays. Use response `GoalId` and returned child links when present; otherwise re-read the exact created goal before any follow-on child call. |
| Update | Resolve the current operation contract for each Library Goal parent scalar change. Use item PATCH when advertised; use an ADF `libraryGoals` update part only when batch is explicitly enabled. For a child change, use only its current advertised child operation. Preserve omitted collections and use a concurrency header only when the selected contract advertises it. One approval may bind several ordered requests without changing their transports. |
| Add a Library Goal Task | Re-read the selected parent and use its fresh returned `libraryGoalTasks` child collection link. POST only explicit task fields, then retain the returned item identity/link and re-read the child collection. |
| Add a Target Outcome | Re-read the selected parent and use its fresh returned `libGoalTargetOutcomes` child collection link. POST `TypeId`, `TypeItemId`, and `RelationshipCode`; reject a duplicate TypeItemId and re-read the child collection. |
| Activate or inactivate | Run independently after a fresh read and separate approval |
| Delete | Require zero references and separate delete approval; otherwise prefer inactivation |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Search/list | POST (read-only action) | `{resourceRoot}/libraryGoals/action/findByAdvancedSearchQuery` |
| Read | GET | `{resourceRoot}/libraryGoals/{LibraryGoalId}?fields=*` with requested child expansion or the fresh returned item/child path |
| Create parent, optionally with children | POST | `{resourceRoot}/libraryGoals`; may include verified `libraryGoalMeasures`, `libraryGoalTasks`, and `libGoalTargetOutcomes` arrays in the parent body. Use returned GoalId and parent/child links; when absent, re-read the exact created parent before later child work |
| Update Library Goal parent scalar | Current metadata-advertised PATCH or explicitly enabled ADF batch POST | Fresh returned opaque item path for PATCH; for batch, the current same-host batch root with a fresh relative `/libraryGoals/{freshReturnedItemKey}` update part. For Weighting-only update, send only `{"Weighting":"<validated-string>"}`. |
| Update/activate/inactivate child or lifecycle state | Current metadata-advertised method | Fresh returned parent or child path. Resolve that operation independently; do not reuse a parent update contract for another operation. |
| Delete | DELETE | Fresh returned item path after zero-reference proof |
| Add Library Goal Task | POST | Fresh returned `{libraryGoalTasksCollectionLink}` from the selected parent; map explicit task fields such as TaskName, Description, dates, TaskTypeCode, PriorityCode, Comments, UomCode, and only applicable target fields. The returned item identity is `TaskContentId,BusinessGroupId,TaskId` |
| Add Target Outcome | POST | Fresh returned `{libGoalTargetOutcomesCollectionLink}` from the selected parent with `{TypeId,TypeItemId,RelationshipCode}`. The returned child identity is `ContentItemRlatId` |
| List Target Outcome subscriptions | GET | `{hcmRuntimeRoot}/targetOutcomeSubscriptionsLOV?finder=FindBySourceId;SourceId=119&fields=ContentTypeId,Description,Name,SectionId,SourceId,ValueSetName`; select one returned subscription before listing content items |
| List Target Outcome content items | GET | `{hcmRuntimeRoot}/contentItemsLov?finder=findByWord;ContentTypeId={returnedContentTypeId},ContentValueSetId={returnedValueSetName}&fields=ContentItemId,ContentSectionId,ContentTypeName,ContentValueSetCode,ContentValueSetId,GoalBusinessUnitName,GoalCategory,GoalDepartmentName,GoalJobFamilyName,GoalLegalEntityName,GoalSubType,ItemDescription,Name` with supported query and pagination; map TypeId from ContentTypeId and TypeItemId from ContentItemId |
| Hydrate multiple Target Outcome content items | POST (read-only ADF action) | `{hcmRuntimeRoot}/contentItemsLov/action/getMultipleContentItemDetails` with `Content-Type: application/vnd.oracle.adf.action+json` and body `{ "contentItems": "{commaSeparatedReturnedContentItemIds}" }`; use only IDs from the current content-items read and parse only the response fields advertised by current metadata |
| Validate category, subtype, level, task, and goal type codes | GET | `{restBaseUrl}/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` through Apps Common; filter enabled/effective rows and map only a returned `LookupCode` |
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
must use the action media type. Apply the same rule to performance requests, and fail closed if the selected header conflicts with
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

## Performance Library Goal Advanced-Search Request

Use only `{resourceRoot}/libraryGoals/action/findByAdvancedSearchQuery` for
the Performance Library Goal advanced-search action. Build the full envelope
using `goal-management-common/scripts/library_goal_search_contract.py` (relative to Goal Management):

```json
{
  "query": "{goalNameFreeText}",
  "searchFields": ["GoalName"],
  "displayFields": ["GoalId", "GoalName", "TypeMeaning", "StatusMeaning", "AvailableTo", "LastUpdateDate"],
  "filters": [],
  "sort": [{"name":"LastUpdateDate","direction":"desc"}],
  "limit": 25,
  "offset": 0
}
```

When a free-text Goal Name search is supplied, add only these query fields:

```json
{
  "query": "{goalNameFreeText}",
  "searchFields": ["GoalName"]
}
```

Use an empty query when no free-text Goal Name search is requested.
Never put `TypeCode`, `PERFORMANCE`, category, status, External ID, or another
structured filter in `query`; represent each such constraint through the
current action filter contract only when that field is supported. TypeCode is
not an advertised action filter. Resource attribute presence does not prove
filter support. Supported filters use field-to-array mappings, for example
`{"StatusCode":["A"]}`, not `name/terms`. Keep status unfiltered for duplicate
checks so inactive goals are not missed. Complete pagination through the core
client and run `assess_duplicate_evidence` with exact name, variant and
environment. Use current tenant meaning mappings, not English-only inference.

Source: [Oracle Library Goal advanced-search schema](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-librarygoals-action-findbyadvancedsearchquery-post.html).

Before reuse, read the fresh returned item link (never construct an item key
from numeric GoalId), then run `verify_existing_goal_for_reuse` in
`goal-management-common/scripts/library_goal_create_payload.py` with every required date and
scope field as well as name/type/status/visibility. A search candidate does not
authorize skipping creation or completing the task. Preserve explicit user
keep/create decisions; unresolved candidates require reconciliation, not a
claim that all requested configuration is complete. This evidence does not
prove UI visibility under a different environment, role or filter.

## Parent-create and known child-create contracts

The verified parent create accepts the Performance Library Goal parent fields
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
or delete path until current metadata or a captured canonical request proves
that operation.

## Library Goal parent scalar update contract

Before preview, re-read the exact Performance Library Goal and resolve the
current advertised update method plus the fresh self/canonical item identity.
Prefer an advertised item PATCH. The returned identity can be composite; keep
it opaque. A captured batch or single-`GoalId` path is evidence of one runtime
acceptance shape only, not permission to reconstruct a key or select that
transport in another environment. The following ADF shape is allowed only when
current metadata explicitly enables batch and resolves its same-host root:

```http
POST {adfBatchRoot}/
Content-Type: application/vnd.oracle.adf.batch+json
```

```json
{
  "parts": [
    {
      "id": "Update-library-goal-parent",
      "path": "/libraryGoals/{freshReturnedItemKey}",
      "operation": "update",
      "payload": {"Weighting": "<validated-string>"}
    }
  ]
}
```

`Weighting` is a Library Goal string field. Do not place Goal Plan,
MassRequest, `RequiredGPGId`, `performanceGoalsV2`, or a `perfGoalsDFF` child
part in this request. A Library Goal DFF part is excluded unless current
metadata explicitly requires an independently requested DFF change. The
response's ETag is fresh state evidence, not an implicit `If-Match`
instruction. Add that request header only when the current batch operation
expressly advertises it.

This is distinct from the Goal Plan template/mass-request contract, whose
update part is under `/performanceGoalsV2/{GoalId}` and whose `Weighting` is
numeric. Never route an update between these object contracts.

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
`PerfCategoryCode`, `GoalSubTypeCode`, and `LevelCode` through
`HRG_PERF_GOAL_CATEGORY`, `HRG_SUB_TYPE_CODE`, and
`HRG_GOAL_MEASUREMENT_LEVEL` when those fields are supplied or required.
When a Goal Type lookup is needed, use `HRG_GOAL_TYPE` and require its returned LookupCode to agree with
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

| Step | Requirement |
|---|---|
| 1 | Verify variant contract and cache lean current updateable metadata |
| 2 | Re-read full requested parent/child state |
| 3 | Run `scripts/library_goal_payload.py`; generate its field-by-field approval preview and exact canonical JSON payload containing materialized StatusCode, Visible, and TypeCode defaults, and retain its SHA-256 fingerprint internally |
| 4 | Apply the [shared Goal Management approval convention](../../../goal-management-common/approval-convention.md). Accept a clear contextual affirmative only for one immediately preceding unchanged preview, identified operation, or explicitly combined batch; activation and delete remain separate unless both appear in one exact approved batch |

Any payload change, including a changed supplied value, a changed applied default,
changed omission, metadata-driven remapping, child collection effect, target,
environment, or operation, invalidates the prior approval. Re-render the full
preview and require a fresh, separate approval for its new fingerprint.

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
| GOAL_LIBRARY.CREATE_VERIFY | step | 121 | reference_lookup | verified->GOAL_LIBRARY.DONE_CREATED;invalid_state->GOAL_LIBRARY.BLOCKED;ambiguous->GOAL_LIBRARY.UNKNOWN | GOAL_LIBRARY.CREATE | stop | HTTP 201 returned and the exact created Performance Library Goal must pass key-field and audience verification |
| GOAL_LIBRARY.UPDATE_PREVIEW | decision | 130 | reference_lookup | reviewed->GOAL_LIBRARY.UPDATE_APPROVAL;blocked->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD, GOAL_LIBRARY.WRITE_ROUTE | stop | update is selected |
| GOAL_LIBRARY.UPDATE_APPROVAL | decision | 140 | reference_lookup | approved->GOAL_LIBRARY.UPDATE;declined->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.UPDATE_PREVIEW | stop | Final update preview and child diff are reviewed |
| GOAL_LIBRARY.UPDATE | step | 150 | reference_lookup | verified->GOAL_LIBRARY.DONE_UPDATED;ambiguous->GOAL_LIBRARY.UNKNOWN;failed->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.UPDATE_APPROVAL | stop | Approved Library Goal parent scalar update is ready after fresh batch-contract resolution |
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

# Performance Library Goal Captured API Path Reference

The supplied captures establish these stable paths and request shapes. Omit the
captured tenant host, runtime revision, release suffix, IDs, and sample values
from reusable contracts.

| Purpose | Method | Stable path | Runtime values and payload guidance |
|---|---|---|---|
| Validate status, type, visibility, category, level, subtype, priority, UOM, target criteria, or task type | GET | `/fscmRestApi/resources/latest/commonLookups/{LookupType}?expand=lookupCodes` | Resolve `LookupType` and an exact code/meaning at runtime; use only enabled/effective returned LookupCode values. This is a validation/read path, not a lookup-maintenance route. |
| Resolve Business Unit, Department, Legal Employer, or Job Family | GET | `/hcmBusinessUnitsLOV`, `/departmentsLov`, `/legalEmployersLov`, or `/jobFamiliesLov` | Finder search term, fields, limit, and offset are runtime query inputs. |
| Create Library Goal | POST | `/libraryGoals` | Entity body contains only current metadata-supported parent fields and, where verified, optional child arrays. `TypeCode=PERFORMANCE` is the variant discriminator. |
| Search Library Goals | POST | `/libraryGoals/action/findByAdvancedSearchQuery` | Full ADF action envelope; locally verify Performance type after complete pagination. |
| Read Library Goal | GET | `/libraryGoals/{LibraryGoalId}` or fresh returned item link | Resolve identity from search/create/fresh item link. |
| Update Library Goal parent scalar | POST | `{adfBatchRoot}/` with relative part path `/libraryGoals/{freshReturnedItemKey}` | Use one ADF batch `update` part. `Weighting` is a validated string. The item key/path comes only from the fresh returned item; never reuse a captured GoalId or composite key. |
| List goal translations | GET | `/libGoalTranslations` | Use `finder=findByGoalId;ContentItemId={LibraryGoalId}`; the selected goal ID is runtime-resolved. |

Public `commonLookups` is resolved from the configured Apps Common REST host;
Library Goal and LOV business-object paths are resolved from their current HCM
roots. Never copy a captured host, `rv:` revision, or tenant code between
environments.

## Mutation preflight and verification

Before every Library Goal parent or child mutation, resolve current
`/libraryGoals/describe` metadata to confirm the requested method, writable
fields, child capability, media type, and concurrency contract. A new parent
create uses an exact Performance duplicate search because no target item yet
exists. For update, status, delete, task, Target Outcome, or translation work,
immediately GET the parent and relevant child/item link before preview and use
the returned ETag or other optimistic-lock state only as the current operation
contract advertises. An ETag in a response does not itself authorize an
`If-Match` request header. Submit once,
then re-read the changed parent/child/translation to verify. A capture's ETag,
child key, or lookup result must never be reused.

## Narrow-delta payload rule

The captured `libraryGoals` parent body may demonstrate optional
`libraryGoalMeasures`, `libraryGoalTasks`, `libGoalTargetOutcomes`, and DFF
arrays for one create use case. It is not an update template. A parent update
maps only explicitly requested writable scalar fields and never replays an
embedded child array, DFF row, or unchanged captured field. Maintain a measure,
task, Target Outcome, or translation through its own current advertised child
operation, with only the fields requested for that child. Do not include
identity, ETag, returned links, or read-only attributes in any body.

## Weight-update schema boundary

| Object being changed | ADF batch part path | `Weighting` JSON type | Must not be copied into this contract |
|---|---|---|---|
| Performance Library Goal parent | `/libraryGoals/{freshReturnedItemKey}` | String, for example `"25"` | `performanceGoalsV2`, `GoalPlanId`, `MassRequestId`, `RequiredGPGId`, and Goal Plan DFF parts |
| Goal Plan template/mass-request Performance Goal | `/performanceGoalsV2/{GoalId}` | Number, for example `25` | `libraryGoals`, `PerfCategoryCode`, Library Goal composite-key assumptions, and Library Goal fields |

Both rows use a runtime-resolved ADF batch root, but are separate schemas. A
current metadata check remains mandatory for each part and any optional DFF
operation.

## Additional lifecycle, child-maintenance, translation, validation, and verification examples

| Purpose | Method | Stable path | Guard and verification |
|---|---|---|---|
| Activate or inactivate | PATCH | `/libraryGoals/{LibraryGoalId}` | Status-only narrow delta after fresh read and separate approval; re-read the parent. |
| Delete parent | DELETE | Fresh metadata-returned Library Goal item link | Only when current metadata advertises DELETE and zero references are proven; separate approval, then confirm absence. |
| Add/update/delete a measure, task, or Target Outcome | Current metadata-advertised child method | Fresh returned child collection/item link | Use the child’s returned identity and a narrow body. Do not infer an update/delete path from a captured create. Re-read the affected child collection. |
| List/read/update goal translation | GET/PATCH | `/libGoalTranslations` and fresh returned translation item link | List by current goal ID, then map only `Name`, `Description`, and `SuccessCriteria`; preserve base language and re-read. |
| List/read/update task translation | GET/PATCH | `/libGoalTaskTranslations` and fresh returned task-translation item link | Use only the current OpenAPI-advertised finder/key; map only `TaskName` and `Comments`, then re-read. |
| Validate goal/task codes and decimal policy | GET / owning-provider read | `/fscmRestApi/resources/latest/commonLookups/{LookupType}` / `HRG_ALLOW_DECIMALS_IN_WEIGHTS` provider | Use enabled/effective returned LookupCodes for category, subtype, level, goal, and task fields; obtain fractional-weight policy only from the owning provider. |
| Verify parent/child/translation write | GET | Fresh parent, child, or translation item link | Confirm the approved delta and preserved sibling collections after one write. |


---

# Performance Library Goal Deterministic Payload Helper

## Inputs and Validation

Run this local helper after current environment metadata, identity, and fresh
state are available and before the preview gate. Its inputs are the exact
environment, operation, resolved current metadata, exact identity, supplied
fields, fresh current state, requested collection intent, and verified defaults.

1. Validate each field marked required by **current metadata**. Do not block an
   omitted optional field.
2. For an optional field that is supplied, validate its current metadata
   constraints and only the business rules applicable to that supplied value.
3. If `ExternalId` (or the current metadata's External ID field name) is
   supplied, read its current metadata maximum length and reject a value longer
   than that maximum before approval. Produce deterministic compliant
   suggestions, such as the unchanged prefix truncated to the maximum length
   and, when space permits, a prefix plus a stable SHA-256 suffix. Suggestions
   are advisory: never silently truncate, replace, or otherwise alter user
   input. If it is omitted and current metadata has server default expressions
   for both `GoalId` and `GoalExternalId`, omit both IDs, record the
   server-derived External ID default in the preview, and bind the post-create
   check `returned GoalExternalId == returned GoalId` to the verification plan.
4. Map only supplied writable fields plus explicitly disclosed defaults. Omit
   every unsupplied optional field from a create payload. For an update, retain
   every omitted field and collection from fresh state; do not emit it in the
   update payload. For a Library Goal parent scalar update, the canonical body
   is an ADF `parts` envelope whose one update part targets the fresh
   `/libraryGoals/{freshReturnedItemKey}` path. `Weighting` is serialized as a
   string. Do not use the Goal Plan `/performanceGoalsV2` schema, its numeric
   Weighting, its context fields, or an inferred DFF part.
5. Canonicalize the exact JSON payload deterministically: UTF-8, object keys
   recursively sorted, compact separators, and no non-payload preview data.
   Canonicalize an approval binding containing that payload plus environment,
   operation, exact identity, and request path using the same rules, then
   compute the SHA-256 hex digest of its UTF-8 bytes.

## Required Approval Preview

Render this complete preview, in this order, for create, update, and delete:

| Preview section | Required content |
|---|---|
| Environment | Exact Fusion environment/host alias selected for this request |
| Operation | Exact `create`, `update`, or `delete` operation and endpoint method/path |
| Exact identity | Resolved `LibraryGoalId` and immutable External ID when present; for create, the supplied idempotency identity, or current server-derived `GoalExternalId` from generated `GoalId` plus disclosed exact-name-within-Performance-type duplicate control |
| Field-by-field effect | Each supplied field with before/after effect; explicitly identify metadata-required values and validation results |
| Defaults | Each applied default, its source, and resulting payload field |
| Omissions | Every omitted optional field and whether it is excluded on create or preserved on update |
| Collection effect | Per collection: omitted/preserved, merge, replace, add, update, remove, or delete; include child before/after identity where applicable |
| Exact JSON payload | The canonical JSON body exactly as submitted; for DELETE, show `{}` and the exact request path |
| Internal approval binding | Retain `sha256:<hex>` computed from the canonical payload plus canonical environment, operation, exact identity, and request path; do not require the consultant to copy it or display it solely for approval |

The approval is valid only for that full preview and internal fingerprint. Any
payload or bound-preview change requires a fresh preview and approval under the
[shared Goal Management approval convention](../../../goal-management-common/approval-convention.md).
Do not accept an approval tied to an earlier fingerprint.

## Library Goal Weighting Update Shape

The helper may produce this batch shape only after
`library_goal_parent_update_contract` has explicitly selected ADF batch and
resolved the runtime root, exact fresh item identity, media type, and
concurrency rule. Otherwise it must produce the advertised item PATCH request:

```json
{
  "parts": [
    {
      "id": "Update-library-goal-parent",
      "path": "/libraryGoals/{freshReturnedItemKey}",
      "operation": "update",
      "payload": {"Weighting": "<validated-string>"}
    }
  ]
}
```

The preview binds the batch root, relative item path, one-part payload, and
only headers explicitly required by the current contract. A returned
`changeIndicator` or ETag must not be transformed into `If-Match`. Re-read the
parent after submission and compare its persisted string `Weighting` with the
approved value.
