# Sales Plays and Content Read Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Environment, user, and operation | fusion_environment_context, acting_user_identity, sales_play_operation | Block the request | Supply the target environment, acting user, and LIST, GET, QUERY, or CONTENT_SEARCH. | Always |  |
| Record identity | sales_play_id | Block the request | Supply the exact Sales Play or content bundle record ID; never infer an ID from display text. | GET |  |
| Type-qualified read | sales_play_type | Do not apply a type filter | Supply SALES_PLAY for a Sales Play or CONTENT_BUNDLE for a content bundle or content packet only when the request explicitly distinguishes a type. | LIST, GET, or QUERY when a record type is explicit |  |
| List query | sales_play_query with documented bounded query parameters | Use a bounded default | Default to $limit=5 when the user does not request another supported bound. | LIST |  |
| Advanced query | sales_play_query with documented fields, accessors, collection criteria, and optional $effectiveDate | Block the request | Translate the read request into the documented $query body and keep collection.limit bounded. | QUERY |  |
| Content Intelligence search | content_intelligence_question and content_intelligence_sales_play_id | Block the request | Supply one non-empty question and one exact, non-empty Sales Play ID. | CONTENT_SEARCH |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Operation is LIST and the environment and user are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is GET and the environment, user, and exact record ID are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is QUERY and the environment, user, and a valid bounded query can be derived | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is CONTENT_SEARCH and the environment, user, question, and exact Sales Play ID are present | Ready | Validate environment, Knowledge Management OAuth readiness by selecting the `knowledge-management` token from the regular `scope` property, and effective Knowledge content access. |  |
| GET has no exact record ID | Blocked | Request the exact ID and do not call Fusion. |  |
| Operation is CREATE, UPDATE, DELETE, PATCH, PUT, BULK, or POST to any endpoint other than salesPlays/$query or /api/knowledge-management/v2/contentIntelligence | Unsupported | State that the current skill revision is read-only and stop. |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is LIST, GET, QUERY, or CONTENT_SEARCH | Normalize the operation and continue. | Always |  |
| Operation is outside LIST, GET, QUERY, or CONTENT_SEARCH | Reject it as unsupported without previewing or calling Fusion. | Always |  |
| sales_play_id is blank or ambiguous | Block and request the exact ID. | GET |  |
| sales_play_type is explicitly supplied | Normalize only SALES_PLAY or CONTENT_BUNDLE. Treat content bundle and content packet, including their plural forms, as CONTENT_BUNDLE; reject another value. | LIST, GET, or QUERY |  |
| The request refers to the Sales Plays and Content collection generally without distinguishing a record type | Do not infer sales_play_type and do not add a salesPlayType filter. | LIST or QUERY |  |
| GET includes an expected sales_play_type | Fetch only the exact ID, require salesPlayType in the response, and report a type mismatch when the returned canonical value differs; do not substitute another record. | GET |  |
| $limit or $offset is not a nonnegative integer | Block and identify the invalid query parameter. | LIST |  |
| $includeTotalItems is present but is not boolean | Block and identify the invalid query parameter. | LIST |  |
| LIST has an explicit SALES_PLAY type | Build the raw filter value exactly as ((salesPlayType = 'SALES_PLAY')); do not use eq. | LIST |  |
| LIST has an explicit CONTENT_BUNDLE type | Build the raw filter value exactly as ((salesPlayType = 'CONTENT_BUNDLE')); do not use eq. | LIST |  |
| LIST $filter uses OData eq or another unverified equality form | Block before Fusion and rebuild only from the runtime-validated BOSS type-filter templates. | LIST |  |
| LIST query values are already percent-encoded | Block execution and pass decoded raw key=value query arguments to the shared client so it performs encoding once. | LIST |  |
| LIST $sortBy is present | Require a target-release sortable field and field:direction syntax; timeCreated:desc is the runtime-validated descending creation-time form. | LIST |  |
| Query parameter is not documented by the target-release contract | Block and request a supported query. | LIST or GET |  |
| QUERY collection.limit is not a positive integer or collection.offset is not a nonnegative integer | Block and identify the invalid collection field. | QUERY |  |
| QUERY has an explicit record status | Normalize only DRAFT, ACTIVE, or ARCHIVE; reject another value. Build the status comparison inside collection.filter, never as a root request property. | QUERY |  |
| LIST has an explicit record type | Apply the corresponding runtime-validated raw LIST type-filter template and include salesPlayType in the returned fields. | LIST |  |
| QUERY has an explicit record type | Normalize only SALES_PLAY or CONTENT_BUNDLE. Build the type comparison inside collection.filter and include salesPlayType in returned fields; do not reuse the LIST $filter template or place the type at the request root. | QUERY |  |
| QUERY combines record status and type | Build collection.filter with each normalized equality comparison joined by lowercase and; for example, status = 'ACTIVE' and salesPlayType = 'SALES_PLAY'. | QUERY |  |
| QUERY salesPlayArtifacts type is supplied | Normalize only CUSTOMER, PRODUCT, PERSONA, SALESMOTION, or DOCUMENTS; reject another value. | QUERY with salesPlayArtifacts |  |
| QUERY salesPlayArtifacts status is supplied | Normalize only NOT_STARTED, WARN, or COMPLETE; reject another value. | QUERY with salesPlayArtifacts |  |
| QUERY filter or sortBy uses a field that is not respectively searchable or sortable in the target-release contract | Block and identify the unsupported field. | QUERY |  |
| QUERY accessors are supplied | Allow only accessors documented by the target-release contract, including salesPlayArtifacts and $translations. | QUERY |  |
| QUERY has no explicit sort criterion | Preserve service order and disclose that top or first N refers to service order. | QUERY |  |
| Content Intelligence question is blank | Block and request one non-empty user question. | CONTENT_SEARCH |  |
| Content Intelligence Sales Play ID is blank or ambiguous | Block and request one exact Sales Play ID; do not infer it from a display name. | CONTENT_SEARCH |  |
| Content Intelligence request changes connectorId, contentState, either fieldName, either operator, additionalFilters, or extractFiltersFromQuestion | Reject the changed contract; replace only the question and exact Sales Play ID. | CONTENT_SEARCH |  |
| Content Intelligence question is being placed into the nested userInput string | Build and serialize the inner userInput object first, then serialize the outer request; do not interpolate unescaped question text. | CONTENT_SEARCH |  |
| Input includes a password, Basic credential, bearer token, refresh token, client secret, Authorization header, or token-cache content | Ignore and redact the secret; rebuild authentication through the shared OAuth client. | Always |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPC.VALIDATE | step | 1 | validate_input | valid->SPC.ACCESS;invalid->SPC.ERROR;unsupported->SPC.ERROR | none | stop | A Sales Play, content bundle, or Content Intelligence search request has been normalized. |
