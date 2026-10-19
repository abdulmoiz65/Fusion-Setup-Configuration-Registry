# Review Period Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Operation | requested_operation | Block | Ask for one supported operation |
| Existing identity | ReviewPeriodId or exact name plus effective context | Block item get and mutations | Run the Review Period lookup |
| Search definition | optional query filters, creation-time window, result limit | Use unfiltered bounded list | Normalize the query and disclose the returned window and limit |
| Create definition | name, start date, end date, current supported status shown in the approved preview | Block create | Require the Review Period name to be unique; validate dates separately. Preserve explicit valid status or resolve a proven metadata default; do not impose an inactive-first sequence |
| Entry-context definition | no business input; authenticated caller ID is optional for worker context | Return status choices even when caller context cannot be read | Resolve status first; resolve worker/assignment context only when caller ID is available |
| Delete evidence | exact identity, `InUseFlag=false`, zero-usage evidence, current DELETE capability, delete approval | Block delete | Re-read all exposed references and authoritative current metadata |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Start date is after end date | Invalid | Correct the inclusive range |
| Start date equals end date | Validate | Accept only when current metadata/business validation allows a one-day period; otherwise reject before preview |
| A start or end date is malformed, null when required, or changes an accepted date-only value through timezone conversion | Invalid | Require valid ISO `YYYY-MM-DD` values and preserve accepted date-only values without timezone drift |
| More than one identity match exists | Invalid | Require disambiguation |
| Existing period is in use and deletion is requested | Blocked | Prefer inactivation or create a replacement |
| Requested values equal fresh stored values | No change | Return NO_CHANGE without write approval |
| `created_within_days=N` is supplied | Valid read filter | Resolve `now-N days` through `now` as a half-open UTC interval; do not compare only calendar dates |

## Field Validation

| Check | What Happens |
|---|---|
| Dates | Normalize to YYYY-MM-DD; do not infer overlap restrictions |
| Status | Resolve the current ACTIVE_INACTIVE status LOV before a status-bearing create, update, or inactivation. Accept only its returned codes; when the proven UI/runtime contract normalizes omitted or invalid status to `A`, use and verify `A` only when `A` is returned by that LOV; otherwise reject the value rather than persisting it |
| Entry context | Return status codes with their meanings. Worker, assignment, Business Unit, Legal Employer, Department, and Legislation Code are read-only contextual values and never payload attributes or authorization evidence |
| Name | Trim only for matching; preserve approved business text for writes |
| Metadata | Map only current updateable attributes |
| Review Period fields | Validate ReviewPeriodId, ReviewPeriodName, Description, StartDate, EndDate, StatusCode, StatusMeaning, `InUseFlag`, and concurrency state from current evidence. The list/search display contract must not request a `Status` attribute |
| Approval | Invalidate when environment, target, usage, metadata, or payload fingerprint changes |
| Read pagination | Continue using returned offset/hasMore semantics until complete or the disclosed result limit is reached |
| Creation filter | Request `CreationDate` when searchable; otherwise hydrate each candidate item and filter locally, then sort newest first |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.VALIDATE | decision | 20 | validate_input | entry_context->REVIEW_PERIODS.ENTRY_CONTEXT;read_item->REVIEW_PERIODS.READ;read_search->REVIEW_PERIODS.SEARCH;csv->REVIEW_PERIODS.CSV_READY;write->REVIEW_PERIODS.DEPENDENCIES;invalid->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.INTAKE | stop | Intake is complete and one operation is selected |
| REVIEW_PERIODS.WRITE_ROUTE | decision | 95 | evaluate_result | create->REVIEW_PERIODS.CREATE_PREVIEW;update->REVIEW_PERIODS.UPDATE_PREVIEW;inactivate->REVIEW_PERIODS.INACTIVATE_PREVIEW;delete->REVIEW_PERIODS.DELETE_PREVIEW;no_change->REVIEW_PERIODS.NO_CHANGE;unsupported->REVIEW_PERIODS.BLOCKED | REVIEW_PERIODS.REST_PAYLOAD | stop | A mapped write contract exists |


---

# Review Period Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Guided request | One operation, environment, and exact identity or create values | One Review Period |
| Structured object | Operation plus named Review Period attributes | Planning or REST preview |
| FSM task ZIP | Task-level export/import ZIP and explicit requested CSV operation | CSV export or import |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| requested_operation | Yes | Select one lifecycle route | No | Normalize show/fetch to get; find/list/search to search; or create, update, inactivate, delete, initialize_entry_context, csv_export, or csv_import |
| review_period_identity | Conditional | Resolve one existing period | No | Required for item get and mutations; not required for create, list/search, or CSV routes |
| query_filters | Optional | Limit a list/search read by name, status code, dates, creator, or other current searchable fields | Search action body only | Map status filtering only to the current `StatusCode` contract; reject unsupported fields rather than silently ignoring them |
| created_from and created_to | Optional | Select records by `CreationDate` | Search display fields and local filter | Normalize to one half-open UTC interval `[created_from, created_to)` |
| created_within_days | Optional | Express a relative creation-time window such as last 3 days | No | Resolve once to the exact UTC interval and return it in the result |
| result_limit | Optional | Bound returned records | Search pagination | Positive integer; use a safe default and disclose truncation |
| review_period_name | Conditional | Exact business identity and create value | Yes for create or explicit update | Exact normalized match; do not fuzzy-match writes |
| description | Optional | Consultant-facing Review Period description | Yes only when current metadata marks it writable | Preserve omitted value on update |
| start_date and end_date | Conditional | Define inclusive date envelope | Yes when created or explicitly changed | Normalize as YYYY-MM-DD and require start not after end |
| status | Conditional | Active or inactive intent | Yes when explicitly requested | Resolve only from current supported values |
| entry context | No | Return status choices and, when the authenticated caller identity is available, contextual worker and assignment values used by the VBCS entry flow | No | Read-only initialization only; it neither checks application permissions nor authorizes a mutation |
| approvals | Conditional | Bind a mutation or import | No | Required only after final preview |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Optional supplied field is not writable in current metadata | Reject it before preview |
| Existing value is omitted on update | Preserve it |
| Delete or date change is requested | Collect `InUseFlag`, downstream usage, and fresh concurrency evidence before payload mapping |
| Delete is requested | Continue only if current authoritative metadata explicitly advertises DELETE; UI/runtime create/update evidence alone is insufficient |
| Unknown management resource or behavior | Mark the contract current_metadata_required and stop before preview |
| Search transport uses POST | Treat it as a safe read because the action only evaluates a query; do not ask for mutation approval |
| Entry-context initialization is selected | Read the status LOV; then, when an authenticated caller ID is available, read the caller's worker and assignment context. Do not require the context values to create, update, or validate a Review Period payload |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REVIEW_PERIODS.INTAKE | step | 10 | validate_input | complete->REVIEW_PERIODS.VALIDATE;missing->REVIEW_PERIODS.BLOCKED | none | stop | Every Review Period request |


---

# Review Period Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| FSM task ZIP | Unmodified task-level ZIP from the supported export route | Validate with shared setup-data validator before import |
| Review table | One operation and exact identity per synthetic row | Plan and preview each row independently |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Identity | External task keys, Review Period name, returned ID | Resolve exact targets; reject ambiguity |
| Business data | Current catalog/export columns | Preserve task ZIP shape and reject unsupported columns |
| Sensitive data | Credentials, cookies, real worker data | Reject and do not persist |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Export | Explicit csv_export request |
| Import | Validated ZIP, row summary, exact environment, and separate import approval |
| Partial failure | Preserve sanitized row errors and do not retry uncertain writes automatically |
