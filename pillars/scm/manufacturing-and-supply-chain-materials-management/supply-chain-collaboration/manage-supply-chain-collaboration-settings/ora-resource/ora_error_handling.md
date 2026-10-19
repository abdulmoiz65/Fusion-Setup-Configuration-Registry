# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Code is absent, non-editable, or does not resolve | Stop; report the requested Code and require an existing editable parameter. |
| Value is absent or fails a validator | Stop; report the validator category and sanitized rejected value. |
| Catalog, username, or generic lookup has no or many matches | Stop; report the resolver and require one exact selection. |
| A catalog or requester identifier is supplied as Value | Stop; require the exact validated catalog name or username. Do not submit a derived identifier because the service performs that conversion internally. |
| A generic lookup Meaning or identifier is supplied as Value | Stop; require the exact LookupCode, for example `Y` or `N` for ALLOW_FULL_DATA_ACCESS. |
| A numeric value is not an integer or is outside its documented range | Stop; require a base-10 whole number within the code's validation range. |
| A CSV, displayed-measure, boundary, plan-edit, horizon, aggregation, or layout code is invalid | Stop; resolve and submit the exact LookupCode. For multi-select fields, validate every comma-separated code. |
| A UOM, planning-calendar identifier, or planning-time-level identifier is invalid | Stop; require a service-recognized UOM or valid numeric identifier; do not construct an undocumented lookup request. |
| Related settings are incompatible | Stop; identify the dependent setting codes and required correction. |
| REST service returns a validation error | Preserve the HTTP status and sanitized server message; correct input before a fresh attempt. |
| A prior update has uncertain completion | Do not replay it; reconcile through the read-only collaborationParameters lookup first. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | A required Code, Value, or unique lookup result is absent | Supply the missing value or select one exact match. |
| INVALID | A server or local validation rule rejects a value | Correct the parameter value or its dependent setting. |
| FAILED | A transport, authorization, or unexpected REST failure occurs | Stop and investigate the environment or privileges before retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Task code, parameter Code, validation category, and safe correction guidance. |
| Lookup failure | Resolver name, resource type, match count, and required exact-value rule. |
| REST failure | HTTP status, sanitized message, failed stage, and safe next action; never disclose credentials, tokens, or full payloads. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup is unresolved or ambiguous | Do not choose a value or construct a substitute request. |
| A validation or dependency rule fails | Do not continue to preview or a mutation. |
| A REST update failed or is uncertain | Do not retry or replay the write automatically. |
| A LOV is requested | Do not send the LOV resource to Data Loader or treat it as a registered business object. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.HANDLE_ERROR | decision | 90 | error_handler | missing->CCS.MISSING;invalid->CCS.FAILED;failed->CCS.FAILED | none | stop | A prior task node reports a failure. |
| CCS.ALL_GOOD | terminal | 91 | terminal | none | CCS.ENFORCE_DESIGN | continue | The setting request is validated and ready for its separate approval-gated import workflow. |
| CCS.MISSING | terminal | 92 | terminal | none | CCS.HANDLE_ERROR | stop | A required value or unique lookup result is missing. |
| CCS.FAILED | terminal | 93 | terminal | none | CCS.HANDLE_ERROR | stop | Validation, dependency, design, or service processing failed. |
