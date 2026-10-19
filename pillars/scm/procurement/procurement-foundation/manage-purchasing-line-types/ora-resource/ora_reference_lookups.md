# Deferred Reference Lookups

The references below describe server-side resolution paths. Client-side validation must not invoke them. The approved Data Loader business object or an explicitly selected REST execution route performs any required lookup, duplicate check, foreign-key resolution, or record-existence check.

## Live Lookups

| Resolver | Execution Owner | Source Values | Request Path or URL | Server-Side Validation |
|---|---|---|---|---|
| find_purchasing_line_type_by_id | Data Loader or explicitly selected REST execution | LineTypeId | GET /fscmRestApi/resources/11.13.18.05/purchasingLineTypes/{LineTypeId} | Confirms the targeted record and returns immutable or conditional-update fields. |
| find_purchasing_line_types_by_line_type_contains | Explicitly selected read-only REST execution | LineTypeContains | GET /fscmRestApi/resources/11.13.18.05/purchasingLineTypes?q=LineType%20LIKE%20%27%25{LineTypeContains}%25%27&fields=LineTypeId,LineType,LineTypeCode,LineTypeDescription,PurchaseBasisCode,EndDate&onlyData=true | Returns matching records only after the route is selected and authorized. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Client-side validation | Does not invoke a resolver or infer a server result. |
| Data Loader execution | Validates business-object schema, references, and server acceptance through its configured workflow. |
| Explicit read-only route | May invoke the documented GET only after that route is selected; it returns the requested fields. |
| Server-side no-match or duplicate result | Is handled by the Data Loader or REST execution result; client-side validation does not manufacture a replacement identity. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| No client-side task node | n/a | n/a | n/a | Reference lookups are deferred to the selected execution route. |
