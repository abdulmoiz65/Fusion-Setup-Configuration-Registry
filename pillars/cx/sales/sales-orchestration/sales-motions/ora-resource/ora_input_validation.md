# Sales Motions Read Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Environment, user, and operation | fusion_environment_context, acting_user_identity, sales_motion_operation | Block the request | Supply the target environment, acting user, and LIST, GET, or QUERY. | Always |  |
| Record identity | sales_motion_id | Block the request | Supply the exact Sales Motion ID; never infer an ID from display text. | GET |  |
| List query | sales_motion_query with documented bounded query parameters | Use a bounded default | Default to $limit=5 when the user does not request another supported bound. | LIST |  |
| Advanced query | sales_motion_query with documented fields, accessors, collection criteria, and optional $effectiveDate | Block the request | Translate the read request into the documented $query body and keep collection.limit bounded. | QUERY |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Operation is LIST and the environment and user are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is GET and the environment, user, and exact Sales Motion ID are present | Ready | Validate environment and BOSS OAuth readiness. |  |
| Operation is QUERY and the environment, user, and a valid bounded query can be derived | Ready | Validate environment and BOSS OAuth readiness. |  |
| GET has no exact Sales Motion ID | Blocked | Request the exact ID and do not call Fusion. |  |
| Operation is CREATE, UPDATE, DELETE, PATCH, PUT, BULK, or POST to any endpoint other than salesMotions/$query | Unsupported | State that the current skill revision is read-only and stop. |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is LIST, GET, or QUERY | Normalize the operation and continue. | Always |  |
| Operation is outside LIST, GET, or QUERY | Reject it as unsupported without previewing or calling Fusion. | Always |  |
| sales_motion_id is blank or ambiguous | Block and request the exact ID. | GET |  |
| $limit or $offset is not a nonnegative integer | Block and identify the invalid query parameter. | LIST |  |
| Query parameter is not documented by the target-release contract | Block and request a supported query. | LIST |  |
| QUERY collection.limit is not a positive integer or collection.offset is not a nonnegative integer | Block and identify the invalid collection field. | QUERY |  |
| QUERY statusCode is supplied | Normalize only DRAFT, ACTIVE, or ARCHIVE; reject another value. | QUERY |  |
| QUERY filter or sortBy uses a field that is not respectively searchable or sortable in the target-release contract | Block and identify the unsupported field. | QUERY |  |
| QUERY has no explicit sort criterion | Preserve service order and disclose that top or first N refers to service order. | QUERY |  |
| Input includes a password, Basic credential, bearer token, refresh token, client secret, Authorization header, or token-cache content | Ignore and redact the secret; rebuild authentication through the shared OAuth client. | Always |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SM.VALIDATE | step | 1 | validate_input | valid->SM.ACCESS;invalid->SM.ERROR;unsupported->SM.ERROR | none | stop | A Sales Motion read request has been normalized. |
