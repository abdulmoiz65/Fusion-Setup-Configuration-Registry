# Intrastat Parameters Lookup Outcomes

These terminals return the result of the approved exclusion lookups to the invoking workflow. Success means lookup preparation succeeded or was not needed; it does not mean Intrastat Parameters were created or updated in Fusion.

## Error Situations

| Situation | What Should Happen |
|---|---|
| No exact match, multiple matches, or conflicting code and meaning | Return issues identifying the affected source row and exclusion field. Request an unambiguous code or meaning. Do not overwrite conflicting input or release a partially resolved row to Data Loader. |
| Input mapping is unknown, conflicts, or targets an attribute absent from live BO metadata | Stop preparation and report the source header and proposed target for correction. Do not discard a field solely because its value is null. |
| Lookup request fails or results are incomplete | Return failure with the affected resolver and a sanitized reason. Stop before handoff; do not infer a code or automatically retry. |
| All applicable lookups resolve uniquely, or both field pairs are blank | Return the resolved values or unchanged blanks to the invoking workflow. Leave Fusion mutations to the governed Data Loader workflow. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Task name, affected source row and field, resolver name, failure category, and next corrective action. Redact credentials and sensitive runtime data. |
| Lookup success | Which field pairs resolved or were skipped. State that no Fusion mutation was performed by these rules. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INTRASTAT_PARAMETERS.RETURN_SUCCESS | terminal | 20 | terminal | none | INTRASTAT_PARAMETERS.RESOLVE_EXCLUSIONS | stop | The exclusion lookup step returns resolved or not_required; return lookup results to the invoking workflow. |
| INTRASTAT_PARAMETERS.RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | Input mapping or the exclusion lookup step returns blocked or failure; return issues and stop Data Loader handoff. |
