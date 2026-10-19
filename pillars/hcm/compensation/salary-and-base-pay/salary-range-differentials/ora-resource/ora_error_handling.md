# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| No exact SalaryRangeDifferential business object is registered | Stop and report a registered-business-object validation gap. |
| Multiple matching business objects are returned | Stop and request catalog correction; do not choose one. |
| Current template or attribute metadata is unavailable, inconsistent, or returns HTTP 500 | Stop as a Fusion API or schema-validation gap; do not infer fields, payloads, or a write route. |
| A live metadata request returns 401 or 403 | Stop as an authentication or privilege failure. |
| A supplied value fails schema validation | Stop before preview, export, or import preparation and identify the affected field. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Catalog mismatch | The registered object is missing or ambiguous | Correct the Data Loader catalog or provide the exact registered object. |
| Fusion API | Fusion returns HTTP 500 or an incompatible metadata response | Resolve the environment issue, then start a new validation attempt. |
| Schema validation | Template or attribute metadata is unavailable, inconsistent, or rejects supplied data | Refresh the current metadata and correct the source data. |
| Auth/authz | Fusion rejects the metadata request with 401 or 403 | Authenticate with a user that has Data Loader metadata access. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation stops | Failure class, affected resolver or field, and the safe next action; never disclose credentials or tokens. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Schema or execution contract is incomplete | Do not invent a write payload, create/update route, action value, or reference lookup. |
| A validation or lookup fails | Do not retry a live mutation automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SRD.HANDLE_ISSUE | terminal | 40 | terminal | none | none | stop | A lookup or validation failure is classified |
| SRD.COMPLETE | terminal | 50 | terminal | none | SRD.VALIDATE_INPUT | stop | All applicable metadata-backed validation succeeds |
