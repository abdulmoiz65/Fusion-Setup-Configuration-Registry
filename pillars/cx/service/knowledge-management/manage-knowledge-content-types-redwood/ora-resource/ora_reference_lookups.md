# Content Type Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_content_type_by_id | Viewing a specific Knowledge content type | Content type record ID | /km/api/v1/contentTypes/{id} | recordId, name, referenceKey, counterPrefix, description, localizedAttributes, contentSchema, enableIndexing, indexStatus | Retrieve the object whose recordId exactly matches the supplied required id path parameter | Content type properties, localized values, schema attributes, indexing setting, and indexing status | Stop and report the invalid id; this single-object endpoint has no multiple-match result. |
| resolve_department_user_groups | Attribute visibility is restricted | Selected department | TBD | User groups mapped to the selected department | TBD | Available user groups | TBD |
| resolve_active_knowledge_locales | Localized content-type or schema-attribute rows are created or updated | Manage Knowledge Locales task | Manage Knowledge Locales task | Active locale code | Select each active locale and retain its exact locale code, such as en_US | localeId | Stop if active locales cannot be determined; do not generate a GUID or infer a locale code from a display name. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A content type is requested by record ID | Use the documented GET endpoint in FULL mode to retrieve the ContentType object. |
| A visibility lookup contract is not documented | Stop before applying restricted visibility and obtain the authoritative read-only lookup contract. |
| Localized rows are required | Resolve active Knowledge locales and write their exact locale code to localeId. |
