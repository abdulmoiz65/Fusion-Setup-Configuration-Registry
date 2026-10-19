# Data Capture Rules Read Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Intent classification | implementation_objective or data_capture_rule_operation | Block the request | Supply a clear Data Capture Rule objective or operation. | Always |  |
| Environment, user, and operation | fusion_environment_context, acting_user_identity, data_capture_rule_operation | Block the request | Supply the target environment, acting user, and LIST, GET, or QUERY. | The classified intent is a supported read. |  |
| Record identity | data_capture_rule_id | Block the request | Supply the exact Data Capture Rule ID; never infer an ID from display text. | GET |  |
| List query | data_capture_rule_query with documented bounded query parameters | Use a bounded default | Default to $limit=5 when the user does not request another supported bound. | LIST |  |
| Advanced query | data_capture_rule_query with documented fields, accessors, collection criteria, and optional $effectiveDate | Block the request | Translate the read request into the documented $query body and keep collection.limit bounded. | QUERY |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Operation is LIST and the environment and user are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is GET and the environment, user, and exact Data Capture Rule ID are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is QUERY and the environment, user, and a valid bounded query can be derived | Ready | Validate environment and BOSS OAuth readiness. |  |
| GET has no exact Data Capture Rule ID | Blocked | Request the exact ID and do not call Fusion. |  |
| Operation is CREATE, UPDATE, DELETE, PATCH, PUT, BULK, or POST to any endpoint other than dataCaptureRules/$query | Unsupported | State that the current skill revision is read-only and stop without routing, artifact generation, preview, approval, or a Fusion call. |  |
| Request asks to create, generate, draft, or sample a Data Capture Rule or local blueprint | Unsupported | Return UNSUPPORTED within this skill. Do not route to the parent skill or create a blueprint, payload, example, or project artifact. |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is LIST, GET, or QUERY | Normalize the operation and continue. | Always |  |
| Operation is outside LIST, GET, or QUERY | Reject it as unsupported without previewing or calling Fusion. | Always |  |
| data_capture_rule_id is blank or ambiguous | Block and request the exact ID. | GET |  |
| $limit or $offset is not a nonnegative integer | Block and identify the invalid query parameter. | LIST |  |
| $includeTotalItems is present but is not boolean | Block and identify the invalid query parameter. | LIST |  |
| Query parameter is not documented by the target-release contract | Block and request a supported query. | LIST or GET |  |
| LIST or QUERY equality filter is supplied | Require the raw BOSS form ((field = 'value')). Reject OData eq, double-quoted string literals, and pre-encoded filter text before the API call. | LIST or QUERY |  |
| QUERY body is supplied | Require one top-level JSON object. collection must be an object; filter and positive limit belong inside collection. fields, accessors, subTypes, and parameters remain at their documented top-level positions. Reject query, payload, or data wrapper objects. | QUERY |  |
| QUERY collection.limit is not a positive integer or collection.offset is not a nonnegative integer | Block and identify the invalid collection field. | QUERY |  |
| LIST or QUERY statusCode is supplied | Normalize only DRAFT, ACTIVE, or ARCHIVE; reject another value. For ACTIVE equality use ((statusCode = 'ACTIVE')). | LIST or QUERY |  |
| QUERY filter or sortBy uses a field that is not respectively searchable or sortable in the target-release contract | Block and identify the unsupported field. | QUERY |  |
| QUERY accessors are supplied | Allow only accessors documented by the target-release contract, including dataCaptureRuleAttributes and $translations. | QUERY |  |
| QUERY has no explicit sort criterion | Preserve service order and disclose that top or first N refers to service order. | QUERY |  |
| Request asks about Create, Update, or Delete permission prerequisites without asking to change a rule | Treat it as security guidance, not mutation authorization, and return the complete documented security contract. | Security guidance |  |
| Input includes a password, Basic credential, bearer token, refresh token, client secret, Authorization header, or token-cache content | Ignore and redact the secret; rebuild authentication through the shared OAuth client. | Always |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCR.VALIDATE | step | 1 | validate_input | valid->DCR.ACCESS;invalid->DCR.ERROR;unsupported->DCR.ERROR | none | stop | A Data Capture Rule request has been classified as a supported read or unsupported mutation intent. |
