# Reference Lookups

Use live target-environment Sales object metadata only when a requested change
includes `FusionObjectName` or `FusionAttributeName`. Preference-only changes do
not require this lookup.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| validate_fusion_mapping_attributes | After resolving the effective selected-row source and before package preparation, when either mapping field changes | Effective `FusionObjectName` after overlaying the requested changes on the fresh-export row or seeded fallback; `limit=1000`, `offset=0`, `onlyData=true`, `totalResults=true` | `/crmRestApi/resources/11.13.18.05/objectMetadata/{FusionObjectName}/child/attributes` through `core.fusion-api.rest-api-client` | `AttributeCode`, `count`, `totalResults`, `hasMore` | Require one complete response per distinct nonblank effective object with `hasMore=false` and `count=totalResults=items.length`. Match `FusionObjectName` to the requested metadata object exactly and each nonblank `FusionAttributeName` to exactly one case-sensitive `AttributeCode`. | Validated effective object/attribute pair for both FSM members; sanitized target identifier; response SHA-256 and attribute count | Stop before package preparation when the object metadata is unavailable, incomplete, duplicated, from a different target, or lacks the exact nonblank attribute. Do not accept a similar, case-insensitive, documented, seeded, or caller-asserted name as a substitute. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| No mapping field changes | Skip live attribute discovery; preference-only changes continue using local validation. |
| Both effective mapping fields are blank | Treat the row as explicitly unmapped; no object lookup is required for that row. |
| `FusionObjectName` is nonblank and `FusionAttributeName` is blank | Require complete metadata for the exact object, then accept the explicit no-attribute state. |
| `FusionAttributeName` is nonblank and `FusionObjectName` is blank | Stop as input validation; an attribute cannot be validated without its object. |
| The response reports more results | Stop before preview. Do not validate against a partial page or infer missing attributes. |
| The response is complete | Pass the raw response to the package builder from a temporary local path; persist only its SHA-256, count, requested-pair result, and sanitized environment identifier. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| DAAS.RESOLVE_FUSION_ATTRIBUTES | step | 3 | reference_lookup | resolved->DAAS.ENFORCE_SELECTED_ROWS;skipped->DAAS.ENFORCE_SELECTED_ROWS;failure->DAAS.ERROR | DAAS.RESOLVE_ROW_SOURCE | stop | After row-source resolution; run for mapping-field changes and skip for preference-only changes |
