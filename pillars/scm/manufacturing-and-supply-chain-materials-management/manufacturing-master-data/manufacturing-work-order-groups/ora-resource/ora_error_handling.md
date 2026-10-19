# Import Route Safety and Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| workOrderGroups is not confirmed as the registered object for the requested operation | Stop before sample generation, validation, upload, or import and ask the user to confirm the object. |
| REST preflight or read-only metadata establishes that REST cannot perform the requested operation | Do not call REST or FSM directly. Use FSM only through Core Data Loader after it has prepared an immutable FSM artifact and the user explicitly approves that exact artifact. |
| A validation finds an invalid source, organization, duplicate key, invalid inactive date, protected field change, ineligible assignment, or parent with child assignments | Stop and return the safe validation finding; do not retry a live operation. |
| A live Data Loader operation fails or its outcome is uncertain | Stop, classify the failure, retain only redacted diagnostics, and do not replay the operation without idempotency or a new explicit approval. |
| An artifact, target environment, or requested operation changes after approval | Invalidate the approval and restart Core Data Loader validation for the changed request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required group, organization, source, or work-order data is missing or invalid | Correct the input and repeat read-only validation. |
| catalog_or_metadata_mismatch | The registered object or requested REST operation is not confirmed | Stop; do not invent a REST object. Consider FSM only through the approved fallback process. |
| process_failed | A group uniqueness, mutability, eligibility, inactive-date, assignment, or deletion rule fails | Correct the business request; do not retry a live import automatically. |
| auth_authz | Required work-order-group access is absent | Obtain the needed privilege and restart validation. |
| fusion_api | Core Data Loader or read-only lookup reports an API failure | Report redacted diagnostics and stop. |
| approval_blocker | The exact validated REST or FSM artifact and target environment are not explicitly approved | Wait for explicit approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Approval request | Target environment, requested operation, selected route, exact immutable artifact, validation outcome, and expected business effect. |
| REST-to-FSM fallback | The read-only finding that REST cannot perform the requested operation, plus the exact immutable FSM artifact and target environment. |
| Failure report | Failure class, safe diagnostic summary, route, and one next action; never access tokens, authorization codes, client secrets, cookies, or unredacted sensitive payload data. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any work order group import | Do not bypass Core Data Loader with a direct REST, FSM, upload, job, or import call. |
| REST route not confirmed | Do not invent or substitute a REST Business Object. |
| REST route unavailable | Do not silently switch to FSM. |
| Uncertain or failed live operation | Do not automatically retry the live operation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.ROUTE | decision | 6 | execution_gate | rest_supported->WOGROUP.REST_APPROVAL;rest_unsupported->WOGROUP.FSM_APPROVAL;unconfirmed->WOGROUP.BLOCKED | WOGROUP.DESIGN | stop | Core Data Loader preflight determines the supported import route. |
| WOGROUP.REST_APPROVAL | decision | 7 | execution_gate | approved->WOGROUP.REST_READY;approval_missing->WOGROUP.BLOCKED | WOGROUP.ROUTE | stop | REST Data Loader preflight and immutable-artifact validation have succeeded. |
| WOGROUP.FSM_APPROVAL | decision | 8 | execution_gate | approved->WOGROUP.FSM_READY;approval_missing->WOGROUP.BLOCKED | WOGROUP.ROUTE | stop | REST is proven unable to perform the requested operation and Core Data Loader prepared an immutable FSM artifact. |
| WOGROUP.REST_READY | terminal | 9 | terminal | none | WOGROUP.REST_APPROVAL | stop | The exact validated REST artifact and target environment are approved for Core Data Loader execution. |
| WOGROUP.FSM_READY | terminal | 10 | terminal | none | WOGROUP.FSM_APPROVAL | stop | The exact validated FSM fallback artifact and target environment are approved for Core Data Loader execution. |
| WOGROUP.BLOCKED | terminal | 11 | terminal | none | none | stop | A required validation, route decision, or approval is missing or failed. |
