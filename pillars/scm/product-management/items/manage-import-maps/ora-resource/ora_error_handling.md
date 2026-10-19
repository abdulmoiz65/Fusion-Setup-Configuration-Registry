# Manage Import Maps Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A standard lookup returns no exact Meaning match | Stop before REST Data Loader preview and request a valid value for the affected field and lookup type |
| A standard lookup returns more than one exact Meaning match | Stop before REST Data Loader preview and request an unambiguous value; never select the first result |
| The ROOT_ICC item-class lookup returns no exact item | Stop before preview and disclose that ItemClassName could not be defaulted from the current ROOT_ICC response |
| The ROOT_ICC item-class lookup returns more than one exact item | Stop before preview and classify the response as ambiguous; never select the first item |
| The matched ROOT_ICC item-class response lacks ItemClassCode or a nonblank ItemClass | Stop before preview and classify the response as an incompatible item-class contract |
| An applicable REST create request needs ROOT_ICC and its cached response belongs to another target environment or endpoint contract or cannot validate the exact item | Do not use it; refresh the read-only GET for the current environment and contract before defaulting ItemClassName |
| importMapAttributes returns no exact REST destination attribute | Stop the destination child row and request a valid destination identity |
| importMapAttributes returns multiple exact REST destination attributes | Stop the destination child row and request more precise input; never combine or select partial results |
| The selected REST importMapAttributes item is no longer present in the current response | Treat the selection as stale, refresh once through the declared read-only lookup, and stop before preview if it still does not resolve exactly once |
| A matched REST destination item lacks EntityName, AttributeGroupName, AttributeCode, or AttributeName | Stop before preview and classify the response as an incompatible destination contract; a null LanguageCode remains valid |
| A matched REST destination item has a non-null LanguageCode but the destination child, workbook, or DAT omits it or contains a different value | Stop before preview, copy the exact returned LanguageCode, and rebuild the immutable archive before requesting fresh approval |
| A destination mapping is requested without its corresponding SourceColumn | Reject the REST request as input validation before lookup, preview, or Data Loader handoff |
| A REST transformation or expression is supplied without a destination mapping | Return MISSING at MIM.AWAIT_TRANSFORMATION_MAPPING and ask for the destination mapping; preserve the supplied transformation unchanged |
| A REST transformation is supplied without a nonblank ExpressionCode | Reject the transformation before importMapFunctions lookup and request ExpressionCode |
| An importMapFunctions request contains a query string or any query parameter | Block before dispatch and reconstruct the request as GET /fscmRestApi/scm/redwood/11.13.18.05/importMapFunctions with no question mark or query parameters |
| The exact bare importMapFunctions GET returns an empty, malformed, or incompatible response | Stop before preview and classify the response as a Fusion API contract failure; do not retry by adding projection, filtering, finder, or pagination parameters |
| A parsed REST transformation function has no exact FunctionName match | Stop before preview and return case-insensitive exact suggestions first, followed by case-insensitive substring suggestions; never auto-select |
| A parsed REST transformation function has multiple exact FunctionName matches | Stop before preview, report the candidate and match count, and request an unambiguous current function |
| A REST transformation ExpressionCode differs from matched FunctionSyntax after outer trimming | Preserve ExpressionCode, return FunctionSyntax and Examples as advisory guidance, and continue |
| A REST transformation parent destination cannot resolve exactly once | Stop before preview; do not preserve, infer, or partially construct ReturnAttributeName |
| A REST transformation destination has null LanguageCode | Build the three-part ReturnAttributeName without a trailing separator or language component |
| A REST transformation SourceColumns value cannot be derived | Reject the transformation before preview and request the missing current or participating source-column information |
| IgnoreFlag is not N for a mapped source child or is missing or not Y for a source-only child | Normalize the REST source payload from destination-child presence before preview |
| A cached REST importMapAttributes or importMapFunctions response belongs to another target environment or endpoint contract or cannot validate the selected item or function | Do not use it; refresh the declared read-only GET for the current environment and contract before validation |
| A cache-managed read-only lookup first returns 401 or 403 | Classify the result as auth_expired_or_invalid and let core.fusion-api.rest-api-client refresh once and retry only that read |
| A read-only lookup returns 403 after the permitted refresh or the required Fusion role is missing | Stop and classify the result as authorization_or_privilege; do not retry or continue to preview |
| A read-only lookup has a transport, timeout, Fusion API, or incompatible-response failure | Stop and record the failure class; do not infer a value, use stale lookup data, or continue to preview |
| A lookup result, source value, or derived transformation value changes after preview | Invalidate the prior archive and approval, rebuild the immutable Data Loader preview, and request fresh approval |
| The import route is absent or ambiguous | Stop at MIM.AWAIT_ROUTE and request an explicit REST Data Loader or FSM task-level ZIP choice |
| An FSM task-level ZIP is unreadable, mutable, for another task, or missing required task CSV content | Stop before core.data-loader can display approval or upload, and request a valid immutable ZIP for EGI_MANAGE_IMPORT_MAPS |
| An FSM destination row returns no exact four-field code match | Record an unmatched warning with the row identity and match count, preserve the row and ZIP unchanged, and continue toward FSM readiness |
| An FSM destination row returns multiple exact four-field code matches | Stop before upload, classify the row as ambiguous, and report its unchanged code key and match count |
| An FSM ZIP contains transformations or expressions | Preserve them unchanged; do not invoke REST transformation validation or rewrite the archive |

## Failure Classifications

| Failure Class | When Used | Next Action |
|---|---|---|
| `input_validation` | A REST transformation or expression has no destination mapping | Return MISSING and request the destination mapping before resuming at MIM.VALIDATE_INPUT |
| `input_validation` | A required REST destination value, SourceColumn, or ExpressionCode is missing | Request only the missing or invalid value |
| `input_validation` | The import route is missing or the FSM ZIP is invalid for EGI_MANAGE_IMPORT_MAPS | Obtain an explicit route or correct the immutable archive before route-specific execution |
| `catalog_or_metadata_mismatch` | A selected destination item or transformation function is absent, duplicated, incomplete, or incompatible with its expected REST contract | Correct the selection or task resource guidance before continuing; do not select the first result |
| `catalog_or_metadata_mismatch` | An FSM destination row has multiple exact four-field code matches | Stop before FSM upload and correct the ambiguity; do not select the first item |
| `auth_expired_or_invalid` | A cache-managed token receives an initial 401 or 403 for a read-only lookup | Let the routed authentication workflow refresh once and retry only that read |
| `authorization_or_privilege` | A read-only lookup returns 403 after refresh or the required Fusion role is missing | Stop and recommend the required role, privilege, or environment-access correction |
| `transport_or_environment` | The read-only request cannot securely reach the selected environment | Correct the environment or trust issue before retrying |
| `fusion_api_error` | Fusion rejects a lookup request, or the exact bare importMapFunctions GET returns an empty, malformed, or incompatible contract | Preserve sanitized evidence and correct the environment or endpoint contract before retrying; never add query parameters to importMapFunctions |
| `approval_blocker` | Resolved or derived values differ from the values in the current Data Loader preview | Rebuild the archive and obtain approval for the new immutable preview |

## Non-Failure Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| `advisory` | ExpressionCode resolves to one FunctionName but differs from FunctionSyntax after outer trimming | Show FunctionSyntax and Examples, preserve ExpressionCode, and continue |
| `catalog_warning` | An FSM destination row has zero exact four-field code matches | Preserve and report the row; continue because Fusion FSM is authoritative for import validation |
| `not_applicable` | An FSM destination row's unchanged DestinationTable contains the exact case-sensitive substring DUMMY_TABLE | Record the unchanged row and skip reason without a match count or warning; continue because Fusion FSM remains authoritative |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup blocked | Affected field, REST resource, sanitized supplied value or function candidate, match count, ordered suggestions when available, and one safe corrective action |
| Transformation syntax advisory | Supplied ExpressionCode, matched FunctionName, authoritative FunctionSyntax, and Examples without changing the payload value |
| Data Loader handoff | Exact resolved and derived values including ReturnAttributeName, SourceColumns, conditional LanguageCode, syntax advisories, target environment, operation, immutable archive identity, and approval state |
| FSM validation result | Route, immutable ZIP identity, expression presence, archive readiness, skipped-row count and DUMMY_TABLE reason, and each exact, unmatched-warning, multiple-match, or skipped destination row |
| FSM Data Loader return | Task code EGI_MANAGE_IMPORT_MAPS, target environment, immutable ZIP identity, unmatched warning count, absence of multiple-match blockers, orchestration owner core.data-loader, and required Task Hook validation before approval |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A display value has no exact standard lookup result | Do not copy the display value into the Data Loader field or invent a LookupCode |
| A lookup result is ambiguous | Do not choose the first item, fuzzy-match, or combine results |
| Destination metadata was not returned by one importMapAttributes item | Do not hand-build or mix destination payload values or a non-null LanguageCode |
| A REST transformation or expression lacks a destination mapping | Do not drop, sanitize, attach elsewhere, or preview it; request its destination mapping |
| A REST transformation function has no exact FunctionName match | Do not auto-select a suggestion or treat a case-insensitive or substring match as authoritative |
| A REST transformation syntax differs from FunctionSyntax | Do not overwrite or reject ExpressionCode solely for the mismatch; return FunctionSyntax and Examples as advisory guidance |
| importMapFunctions metadata is required | Do not append a query string, including an empty question mark, or fields, onlyData, limit, offset, q, finder, or any other query parameter; do not retry a failed bare GET with collection projection, filtering, finder, or pagination semantics |
| A transformation ReturnAttributeName was not resolved from its exact parent destination item | Do not preserve a caller-supplied value, drop a non-null LanguageCode, add a null language component, or construct a partial key |
| A transformation SourceColumns value is produced | Do not change participating-source order, omit the current source prefix, or remove the current source from the suffix when it participates |
| A root-node lookup returned ITEM or another LookupCode | Do not write that code to DestinationEntity; use EntityName from the matched importMapAttributes item |
| DestinationColumn is supplied without SourceColumn | Do not infer, default, or reuse a source column from another mapping row |
| A read-only lookup failed | Do not bypass the lookup with cached, guessed, or previously observed values |
| The source changed after approval | Do not upload or initiate the changed archive under stale approval |
| An FSM destination row is evaluated | Do not apply REST transformation rules or match on display fields; do not trim, case-normalize, fuzzy-match, or combine partial destination results |
| An FSM destination row's unchanged DestinationTable contains the exact case-sensitive substring DUMMY_TABLE | Do not invoke importMapAttributes, assign a match count, produce an unmatched warning, drop the row, or rewrite the ZIP |
| An FSM destination row has zero exact matches | Do not drop, rewrite, or block the row solely for that result; preserve it for Fusion FSM validation |
| An FSM destination row has multiple exact matches | Do not continue to upload or choose the first match |
| An FSM ZIP contains transformations or expressions | Do not strip, rewrite, interpret, or route them through REST transformation validation |
| An FSM ZIP is ready for submission | Do not invoke shared.setup-import.task-level-import or another import adapter directly; return the unchanged artifact and task context to core.data-loader |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIM.HANDLE_ISSUE | step | 900 | error_handler | disclosed->RETURN_ISSUES | none | stop | A validation, lookup, dependency, or enforcement node reports a blocked or failed result |
| MIM.DONE | terminal | 910 | terminal | none | MIM.ENFORCE_LOOKUP_RESULTS | stop | All documented REST lookup, destination, transformation, derivation, and enforcement gates passed; syntax advisories were disclosed |
| MIM.FSM_READY | terminal | 915 | terminal | none | MIM.CHECK_FSM_READINESS | stop | The unchanged FSM task-level ZIP is ready to return to core.data-loader with its validation report, orchestration_owner core.data-loader, task_hook_required true, and no multiple-match blocker |
| RETURN_ISSUES | terminal | 920 | terminal | none | none | stop | Error disclosure complete |
| MIM.AWAIT_TRANSFORMATION_MAPPING | terminal | 932 | terminal | none | MIM.VALIDATE_INPUT | stop | Return MISSING without REST lookups, workbook, or DAT preparation; resume at MIM.VALIDATE_INPUT when the destination mapping is supplied |
| MIM.AWAIT_ROUTE | terminal | 935 | terminal | none | MIM.SELECT_IMPORT_ROUTE | stop | Return MISSING without route-specific validation or handoff; resume at MIM.SELECT_IMPORT_ROUTE when an explicit route arrives |
