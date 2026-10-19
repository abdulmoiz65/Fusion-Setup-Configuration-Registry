# Reference Lookups

## Live Lookups

All live lookups use `core.fusion-api.rest-api-client`; this resource does not
select a Fusion host, handle authentication, or execute REST requests directly.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_pick_sequence_rule_type | A Priority1Code through Priority5Code friendly value is supplied | Priority display value and already selected priority codes | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV`; invoke only through `core.fusion-api.rest-api-client` with the selected environment | LookupCode, Meaning | Filter LookupType exactly as `WSH_PICK_SEQUENCE_RULE_TYPE`; trimmed, case-insensitive exact Meaning match; exclude already selected priority codes | Priority1Code through Priority5Code: matched LookupCode | Stop before preview; do not guess a code or choose the first result |
| resolve_pick_sequence_rule_sort | A Sort1Code through Sort5Code friendly value is supplied | Sort display value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV`; invoke only through `core.fusion-api.rest-api-client` with the selected environment | LookupCode, Meaning | Filter LookupType exactly as `WSH_PICK_SEQUENCE_RULE_SORT`; trimmed, case-insensitive exact Meaning match | Sort1Code through Sort5Code: matched LookupCode | Stop before preview; do not guess a code or choose the first result |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A priority or sort display value is supplied | Confirm selected environment identity and read access, then invoke the approved resolver through `core.fusion-api.rest-api-client`. Preserve the returned LookupCode for the corresponding backend field. |
| A supplied priority or sort is already a backend code | Pass it to Data Loader for its authoritative validation; this task-local rule does not duplicate backend validation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSR.RESOLVE_PRIORITY_CODES | decision | 40 | reference_lookup | resolved->RSR.RESOLVE_SORT_CODES;unresolved->RSR.HANDLE_ISSUE;ambiguous->RSR.HANDLE_ISSUE;failed->RSR.HANDLE_ISSUE | RSR.APPLY_UI_DEFAULTS | stop | A friendly priority value requires resolution |
| RSR.RESOLVE_SORT_CODES | decision | 50 | reference_lookup | resolved->RSR.CHECK_DFF_READINESS;unresolved->RSR.HANDLE_ISSUE;ambiguous->RSR.HANDLE_ISSUE;failed->RSR.HANDLE_ISSUE | RSR.RESOLVE_PRIORITY_CODES | stop | A friendly sort value requires resolution |
