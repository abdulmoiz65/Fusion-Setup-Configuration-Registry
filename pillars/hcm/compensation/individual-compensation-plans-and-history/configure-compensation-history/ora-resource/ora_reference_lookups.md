# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_compensation_history_business_object | Before accepting a Configure Compensation History data request | Registered business object discriminator compensationHistoryElements | /hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos&onlyData=true&limit=500&offset=<n> | BusObjTopDiscriminator, UIName, TemplateFileName, BusinessObjectId | Follow pagination and require exactly one case-sensitive BusObjTopDiscriminator equal to compensationHistoryElements | BusinessObject: compensationHistoryElements; UI Name; Template File Name; BusinessObjectId | Stop as a registered-business-object validation gap; do not substitute an object with a similar name |
| read_compensation_history_elements_schema | Before accepting any Compensation History element field | Resolved compensationHistoryElements business object | /hcmRestApi/resources/latest/dataLoaderBusinessObjects/<BusinessObjectId>; /documents/files/<UcmContentId>/data; child business-object and attribute metadata collections | Template sections, AttributeName, AttributeLabel, DataType, MandatoryStatus, DataLength, Description, lookup and reference-object metadata | Require a readable current template whose root discriminator is compensationHistoryElements and whose attribute metadata agrees with that template | Current field contract, mandatory flags, lengths, lookup and reference dependencies | Stop as a schema-validation gap; do not infer field names, accepted values, relationship rules, or a write contract |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Registered business object or schema lookup returns 401 or 403 | Stop as an authentication or privilege failure. |
| Current schema changes after validation | Revalidate before any preview or import preparation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCH.RESOLVE_BUSINESS_OBJECT | step | 10 | reference_lookup | resolved->CCH.READ_SCHEMA;not_found->CCH.HANDLE_ISSUE;lookup_failed->CCH.HANDLE_ISSUE | none | stop | Before handling a Configure Compensation History request |
| CCH.READ_SCHEMA | step | 20 | reference_lookup | schema_ready->CCH.VALIDATE_INPUT;schema_unavailable->CCH.HANDLE_ISSUE | CCH.RESOLVE_BUSINESS_OBJECT | stop | Before field-level validation, preview, or import preparation |
