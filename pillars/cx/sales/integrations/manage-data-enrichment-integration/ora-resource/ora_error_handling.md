# Manage Data Enrichment Integration Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation or environment input is missing | Stop before a REST call and request only the missing non-secret value. |
| A subscription, role, or authenticated read prerequisite is missing | Return the missing dependency and one safe next action; do not attempt to create or assign it. |
| The shared client returns a second 401 or 403 after one cache-managed refresh | Classify auth_or_authz and stop; do not infer that configuration is absent. |
| Fusion returns 404 for the exact documented resource | Classify catalog_or_release_mismatch and stop; do not substitute another API version. |
| Fusion returns a transport error or malformed response | Classify transport_environment or fusion_api and preserve redacted evidence. |
| Pagination does not complete | Stop as incomplete_response and do not report a final record count or absence. |
| More than one visible configuration record is returned | Stop as catalog_mismatch or ambiguous_response and do not choose a record. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | A required non-secret operation or environment value is absent or invalid | Correct the input and rerun from DEI.SELECT_OPERATION |
| approval_blocker | The request exceeds guidance and read-only status scope | Select a separately authorized workflow for the requested action |
| auth_or_authz | Authentication or privilege remains unavailable after the one permitted refresh | Confirm environment access and privileges before retrying |
| catalog_or_release_mismatch | The exact resource is unavailable or the response cardinality is ambiguous | Verify the target release and endpoint contract |
| transport_environment | The target cannot be reached or the response is incomplete | Resolve connectivity and rerun the GET once |
| fusion_api | Fusion returns a non-authentication error or malformed payload | Preserve the HTTP status, endpoint path, safe response summary, and ECID when available |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before the GET | Exact target environment and the read-only endpoint path; never show tokens or Authorization headers. |
| Successful result | API reachability, completed record count, raw enablement value, endpoint-present indicators, configuration visibility, and status limitations. |
| Failed result | Failure class, HTTP status when available, redacted message, ECID when available, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Credentials or tokens are supplied | Do not echo, store, validate, or send them outside the authorized local authentication flow. |
| The GET succeeds | Do not claim end-to-end enrichment health, external credential validity, batch readiness, or enrichment-job success. |
| A retry is considered | Do not retry except the shared client's single cache-refresh retry for 401 or 403; require a corrected condition before any later run. |
| A mutation is requested | Do not issue POST, PATCH, PUT, DELETE, import, or Data Loader operations. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEI.HANDLE_ERROR | step | 5 | error_handler | classified->DEI.DONE_FAILED | none | stop | Any validation, dependency, design, lookup, authentication, transport, API, or scope failure occurs. |
| DEI.DONE_GUIDANCE | terminal | 6 | terminal | none | DEI.DESIGN_GATE | stop | Configuration guidance and checklist are returned without entering credentials or changing Fusion. |
| DEI.DONE_VISIBLE | terminal | 7 | terminal | none | DEI.READ_SMART_DATA | stop | One visible Smart Data configuration record is returned with qualified status fields. |
| DEI.DONE_NOT_VISIBLE | terminal | 8 | terminal | none | DEI.READ_SMART_DATA | stop | The completed collection GET returns zero visible records and the result limitations are disclosed. |
| DEI.DONE_FAILED | terminal | 9 | terminal | none | DEI.HANDLE_ERROR | stop | A failure is classified and returned with redacted evidence and one safe next action. |
