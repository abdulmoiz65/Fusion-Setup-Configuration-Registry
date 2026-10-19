# Performance Library Goal Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Operation and variant | requested_operation plus performance | Block | Select one lifecycle route and one variant |
| Existing identity | returned ID, immutable external ID, or exact disambiguated key | Block item get and mutations | Run exact Library Goal lookup |
| Search definition | variant plus optional query filters, creation-time window, and result limit | Use a bounded variant list | Normalize query and disclose returned window/limit |
| Create definition | name, variant, inactive status, required current attributes, plus a supplied external ID or the verified server-derived External ID contract and exact duplicate-risk controls | Block create | Collect and map from current metadata |
| Delete evidence | exact identity and zero-reference proof | Block delete | Re-read exposed consumers and references |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Current metadata does not expose the public performance fields or requested operation | Blocked | Return mismatch evidence and resume context |
| Target outcome/profile code is unresolved | Blocked | Route to owning setup/reference resolver |
| Translation identity is incomplete or belongs to another Library Goal/task | Invalid | Re-read the returned translation item and reject the update |
| Fractional weighting is requested while `HRG_ALLOW_DECIMALS_IN_WEIGHTS` provider is unavailable or returns disabled | Blocked or normalized | Return `PROVIDER_SKILL_UNAVAILABLE` when unavailable; when the owning provider returns disabled, use the verified rounding rule before preview and disclose the before/after value |
| Existing goal has references and delete is requested | Blocked | Prefer inactivation |
| Submitted `TypeCode` conflicts with the selected performance variant | Invalid | Reject before payload mapping; never permit a cross-variant category or type combination |
| Parent start date is after target completion, a required date is malformed, or a date-only value would shift timezone | Invalid | Require valid ordered ISO `YYYY-MM-DD` values and preserve accepted date-only values unchanged |
| A child task starts or completes outside the parent goal dates | Invalid | Correct the task dates before parent or child save |
| A target-outcome subscription repeats the same `TypeItemId` | Invalid | Keep one valid relationship only and reject the duplicate |
| Requested values equal fresh state | No change | Return NO_CHANGE without mutation |
| `created_within_days=N` is supplied | Valid read filter | Resolve `now-N days` through `now` in UTC, hydrate missing `CreationDate`, and sort newest first |

## Field Validation

| Check | What Happens |
|---|---|
| External ID | Validate a supplied immutable External ID for automated idempotency when writable. When current metadata has `hasDefaultValueExpression=true` for both `GoalId` and `GoalExternalId`, a missing user External ID is valid: omit both IDs, use exact name within `TypeCode=PERFORMANCE` duplicate controls, disclose server derivation in the preview, and verify returned `GoalExternalId` equals returned `GoalId`. Otherwise exact name within variant search and duplicate-risk acknowledgement are mandatory. |
| Performance variant | Require `TypeCode=PERFORMANCE`. Map `PerfCategoryCode` only when supplied or current metadata marks it required; do not populate a development category. |
| Type and defaults | Build the exact create payload through `scripts/library_goal_payload.py`. Require `TypeCode=PERFORMANCE`; materialize omitted `StatusCode` as `I` and omitted `Visible` as `ALL`. Reject null/blank values and reject a preview that merely describes a default absent from its JSON payload. `AvailableTo` is read-only and must never be submitted. |
| Availability semantics | Map “all employees” or “HR specialist, manager, and worker” to `Visible=ALL`. A Business Unit restriction adds one exactly resolved `BusinessUnitId` while retaining `Visible=ALL`. Treat “required” as an assignment indicator only; do not assign from this task. Missing inline Describe enum values do not invalidate this source-backed full-role mapping. |
| Basic fields and codes | Goal Name is the required business input. Validate every current-metadata-required field. For an optional field, validate length, read-only state, LOV code, precision, and applicable business rules only when the caller supplies that field; its omission is not a blocker. Resolve a supplied qualifier only to one writable field/LOV match; otherwise ask which field it belongs to. Send codes, never translated labels. |
| Dates and weighting | Require parent start not after target completion. Validate weighting range and precision; when decimal weights are disabled, apply the verified runtime rounding rule before the resolved Library Goal parent update and verify the persisted string result. `Weighting` is a Library Goal string; reject a Goal Plan numeric-schema payload. |
| Quantitative measurement | Validate UOM, target type/value, minimum, maximum, percentage, numeric precision, configured negative-value policy, and configured relational constraints such as minimum ≤ target ≤ maximum |
| Qualitative measurement | When `UomCode=ORA_NONE`, require `MeasureTypeCode=QUALITATIVE` and omit target type/value and quantitative target fields from the payload |
| Non-measurable goal | Do not create a measurement child |
| Tasks and outcomes | Validate child ownership, required task fields, completion semantics, comments, measurable-task data, and parent-date containment. Permit each active target content item only once per subscription |
| Variant | Preserve the existing variant; do not convert a goal between variants unless current metadata explicitly supports it |
| Child collections | Require explicit replacement/merge intent and preserve omitted children |
| Parent create with optional children | Allow nested measurements, tasks, and target outcomes only when current metadata marks the parent/child fields writable. If a later separate child operation is requested, require the fresh created parent's GoalId and returned child link, or re-read the exact parent before previewing the child operation |
| Standalone Library Goal Task | Require a fresh selected-parent `libraryGoalTasks` collection link; validate TaskName, applicable dates, TaskTypeCode, PriorityCode, Comments, UomCode, and target fields against current metadata. Retain only the returned TaskContentId,BusinessGroupId,TaskId identity/link for later item work |
| Standalone Target Outcome | Require a fresh selected-parent `libGoalTargetOutcomes` collection link and exactly one active TypeId/TypeItemId pair. Map `RelationshipCode` explicitly, reject a duplicate TypeItemId, and retain only the returned ContentItemRlatId/link for later item work |
| Target Outcome selection | Resolve one `targetOutcomeSubscriptionsLOV` row for SourceId=119, then resolve one `contentItemsLov` row using its returned ContentTypeId and ValueSetName. Map TypeId from ContentTypeId and TypeItemId from ContentItemId; validate returned scope fields. A bulk hydration call may send only a nonempty comma-separated string of current returned ContentItemIds to `getMultipleContentItemDetails`; do not use display labels as an ID source or assume that action's response schema |
| Lookup-backed codes | Resolve `PerfCategoryCode`, `GoalSubTypeCode`, `LevelCode`, Task PriorityCode, TaskTypeCode, UomCode, and TypeCode through public Apps Common `commonLookups/{LookupType}?expand=lookupCodes` as applicable. Keep only enabled/effective rows, send returned LookupCode, never Meaning, and do not block an omitted optional field. |
| Concurrency | Use current concurrency metadata for update/delete; a response `ETag` is not by itself an `If-Match` requirement. Send `If-Match` only when the fresh operation contract explicitly advertises it; on conflict, re-read the winning parent and child state and do not overwrite or replay automatically |
| Goal translation | List with `LibraryGoalId` and update only explicit `Name`, `Description`, and `SuccessCriteria` values using the returned `BusinessGroupId,ContentItemId,Language` identity |
| Task translation | Update only explicit `TaskName` and `Comments` values using the exact returned task-translation identity; do not infer its composite-key ordering |
| Translations | Re-read the exact returned item, honor its current concurrency contract, and preserve the base language and all untouched translations |
| Decimal-weight policy | Resolve `HRG_ALLOW_DECIMALS_IN_WEIGHTS` through external capability `core.fusion-api.apps-common.profile-options` before a fractional-weight mutation; no direct profile call or profile-option write is permitted in this skill |
| Activation | Requires a separate fresh preview and approval |
| Create verification | HTTP 201 is provisional. Re-read the exact row and require non-null exact GoalName, TypeCode, StatusCode, Visible, matching `AvailableTo` meaning, and every approved scope field. Null or mismatch returns `INVALID_CREATED_STATE` and blocks Run Book completion. |
| Existing malformed duplicate | An exact existing name+variant row with null `StatusCode` or `Visible` returns `INVALID_EXISTING_LIBRARY_GOAL_STATE`. Stop before creating a suffix/punctuation replacement unless the consultant explicitly approves that separate outcome. |
| Metadata | Reject a supplied field that current describe does not mark writable or updateable. Do not require an omitted optional field. |
| External ID length | When an External ID is supplied and current metadata exposes it, validate it against the current metadata maximum length before preview. If too long, block approval and offer one or more compliant shortening suggestions without changing the supplied value. |
| Read pagination | Follow returned offset/hasMore semantics until complete or the disclosed result limit is reached |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.VALIDATE | decision | 20 | validate_input | read_item->GOAL_LIBRARY.READ;read_search->GOAL_LIBRARY.SEARCH;translation_search->GOAL_LIBRARY.TRANSLATION_SEARCH;decimal_policy_read->GOAL_LIBRARY.DECIMAL_POLICY_READ;csv->GOAL_LIBRARY.CSV_READY;hdl->GOAL_LIBRARY.HDL_VALIDATE;write->GOAL_LIBRARY.DEPENDENCIES;invalid->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.INTAKE | stop | Intake is complete; only current-metadata-required fields and applicable supplied-field rules block |
| GOAL_LIBRARY.HDL_VALIDATE | step | 21 | validate_input | passed->GOAL_LIBRARY.HDL_READY;invalid->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.VALIDATE | stop | A DAT/ZIP source and explicit HDL intent both exist |
| GOAL_LIBRARY.WRITE_ROUTE | decision | 95 | evaluate_result | create->GOAL_LIBRARY.CREATE_PREVIEW;update->GOAL_LIBRARY.UPDATE_PREVIEW;activate->GOAL_LIBRARY.ACTIVATE_PREVIEW;inactivate->GOAL_LIBRARY.INACTIVATE_PREVIEW;delete->GOAL_LIBRARY.DELETE_PREVIEW;translation_update->GOAL_LIBRARY.TRANSLATION_PREVIEW;no_change->GOAL_LIBRARY.NO_CHANGE;unsupported->GOAL_LIBRARY.BLOCKED | GOAL_LIBRARY.REST_PAYLOAD | stop | A mapped variant-specific write contract exists |

## HDL DAT Preflight

Run this preflight only when a DAT/ZIP source and explicit HDL intent both
exist. Require `ContentItem.dat`; translations are optional. Permit
`ContentItemRelationship.dat` when measurements are included. Validate archive
integrity and flat shape, UTF-8 text, `METADATA`, field counts,
template-derived mandatory data, supported source or user keys, duplicate
scoped identities, and operation agreement. Require `ContextName=GOAL` and the
current-template performance discriminator. `GOAL_MEASUREMENTS` rows require a
relationship to a supplied `GOAL` row. Reject every Development or mixed row.

The consultant supplies only the DAT/ZIP and business intent. Preserve it and
create a prepared copy. Resolve environment, current template fields, safe
defaults, source keys for confirmed creates, operations, timestamps, and audit
evidence internally. For `ContentItemTranslation.dat`, require one package or
confirmed target parent, one target-enabled non-base language per parent, and
the current translation template. Reject orphan, duplicate, disabled-language,
or base-language translation rows.

For every `MERGE`, the internally generated change manifest must classify the row as an approved
`create` or `update` from a fresh exact target identity lookup; do not infer it
from the verb. A `DELETE` requires a separate approved delete scope and exact
identity. Reject omitted, duplicate, or unresolved identities, unapproved
operation outcomes, and any target-evidence gap as non-waivable errors.


---

# Performance Library Goal Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Guided request | One operation, goal variant, environment, and exact identity or create values | One Library Goal |
| Structured object | Business attributes and explicitly changed child collections | REST planning or preview |
| FSM task ZIP | Task-level export/import ZIP and explicit CSV operation | CSV export or import |
| HDL DAT/ZIP | Supplied `.dat` or flat `.zip` and explicit HDL intent; audit context is resolved internally | `core.data-loader` only after error-free prepared-copy preflight |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| requested_operation | Yes | Select one lifecycle route | No | Normalize show/fetch to get; find/list to search; or create, update, activate, inactivate, delete, list_translations, update_translation, read_decimal_weight_policy, csv_export, or csv_import |
| goal_variant | Yes | Distinguish performance contract | Map `TypeCode=PERFORMANCE`; map `PerfCategoryCode` only when supplied or metadata-required | Reject any non-performance variant and return a product-route blocker |
| query_filters | Optional | Filter by requested name, status, variant, category, dates or creator when evidence supports the field | Use only current action-supported server filters; otherwise filter complete hydrated results locally | Unknown fields or incomplete evidence block the filtered result; never silently ignore a constraint |
| created_from, created_to, or created_within_days | Optional | Filter list/search results by `CreationDate` | Search fields or local hydrated filter | Resolve one exact half-open UTC interval and return it |
| result_limit | Optional | Bound returned records | Search pagination | Positive integer; disclose default, truncation, and completion |
| library_goal_identity or external_id | Conditional | Resolve one target and enforce idempotency | Send a supplied External ID when provided. When current metadata exposes server default expressions for both `GoalId` and `GoalExternalId`, omit both from create and disclose the server-derived External ID behavior in the approval preview. | Exact immutable external ID preferred; otherwise exact name plus Performance type duplicate controls |
| child collection changes | Conditional | Change measures, tasks, outcomes, translations, or DFF | Yes only when explicit and metadata-supported | Re-read and preserve all omitted collections |
| translation identity and changes | Conditional | List or update one goal/task translation | Yes only for an explicitly approved translation update | For a goal translation, use `LibraryGoalId` to list and the returned `BusinessGroupId,ContentItemId,Language` key to read or update. For a task translation, use only the exact returned task-translation identity; never use display language alone or derive key ordering. |
| decimal-weight policy | Conditional | Read whether decimal weights are permitted | No | Route `HRG_ALLOW_DECIMALS_IN_WEIGHTS` through external capability `core.fusion-api.apps-common.profile-options`; profile maintenance is out of scope |
| weighting change | Conditional | Change only the Library Goal parent Weighting | Yes, only as a `Weighting` string in the resolved Library Goal parent update body or explicitly enabled batch part | Validate the requested string and current writable field. This is never a Goal Plan or `performanceGoalsV2` request. |
| approvals | Conditional | Bind one mutation or import | No | Activation, delete, REST, and import approvals are independent |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Create is selected | Default inactive; activation is not chained |
| Update omits a child collection | Preserve the complete fresh collection |
| Parent Weighting update is selected | Resolve the fresh parent update contract. Use a narrow item PATCH when advertised, or one narrow `libraryGoals` batch part only when batch is explicitly enabled. Do not accept a Goal Plan numeric Weighting body, copied `performanceGoalsV2` fields, or an inferred `If-Match` header. |
| Target outcomes or profiles are referenced | Resolve through their owning setup or metadata route; do not invent codes |
| External ID is omitted | When current `GoalId` and `GoalExternalId` metadata both expose server default expressions, omit both IDs and use exact name within `TypeCode=PERFORMANCE` duplicate checks; disclose that Fusion derives External ID from generated Goal ID and verify the returned values. Otherwise use exact name within variant duplicate detection and require explicit duplicate-risk acknowledgement; never invent a field. |
| External ID change is requested | Reject the mutation when an external ID exists |
| Search transport uses POST | Treat it as a safe read-only action, not as mutation approval |
| Translation update is selected | Preserve base-language fields and untouched task translations. Map goal fields only from `Name`, `Description`, and `SuccessCriteria`; map task fields only from `TaskName` and `Comments`, subject to the current OpenAPI writable-field contract. Require the exact returned item identity and current concurrency contract before preview. |
| Decimal-policy provider is unavailable | Return `PROVIDER_SKILL_UNAVAILABLE` and block a fractional-weight mutation; do not assume rounding, call a profile endpoint directly, or change the profile option |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_LIBRARY.INTAKE | step | 10 | validate_input | complete->GOAL_LIBRARY.VALIDATE;missing->GOAL_LIBRARY.BLOCKED | none | stop | Every Performance Library Goal request |


---

# Performance Library Goal Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| FSM task ZIP | Unmodified task-level ZIP for explicit export/import | Validate through shared setup-data skills |
| Goal table | Variant, operation, business fields, and external ID when current metadata exposes it | Search/diff each row; otherwise use exact name within variant duplicate controls |
| Child collection table | Parent external ID, collection type, explicit merge/replace intent | Group by parent and preserve omitted collections |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Identity | External ID when supported, exact goal key, variant | Reject duplicate or cross-variant ambiguity; never invent an external-ID column |
| Parent business data | Current metadata-supported fields | Include only explicit changes |
| Children | Measures, tasks, outcomes, translations, DFF | Validate against current child metadata |
| Sensitive | Credentials, cookies, production employee data | Reject and do not persist |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Variant | Every row has a verified performance contract |
| Create/update | Show parent and child diff; create stays inactive |
| Activation | Separate operation, preview, and approval |
| Import | Validated ZIP and separate import approval |
