# Value Set Value Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_value_set | A create/update candidate has passed base validation | Requested ValueSetCode | /fscmRestApi/resources/11.13.18.05/valueSets | ValueSetId, ValueSetCode, MaximumLength, ValidationType, ValueDataType, ValueSubtype, ProtectedFlag | URL-encode the ValueSetCode predicate, request limit 2, then require exactly one case-sensitive ValueSetCode match | ValueSetId, ValueSetCode, MaximumLength, definition metadata | No exact match stops as not found; more than one exact match stops as ambiguous; missing, nonnumeric, or out-of-range MaximumLength stops as catalog mismatch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact match | Retain MaximumLength only for local candidate validation; do not retrieve value rows |
| Authentication, authorization, transport, or API failure | Preserve the failure class and stop without treating the value set as missing |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MVS.RESOLVE_VALUE_SET | decision | 2 | reference_lookup | resolved->MVS.CLASSIFY;none->MVS.FAILED;ambiguous->MVS.FAILED;invalid_length->MVS.FAILED | MVS.VALIDATE_BASE | stop | Create/update candidate |
