# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_salary_range_differential_business_object | Before accepting a Salary Range Differentials data request | Registered business object discriminator SalaryRangeDifferential | /hcmRestApi/resources/latest/dataLoaderBusinessObjects?finder=findDataLoaderBos&onlyData=true&limit=500&offset=<n> | BusObjTopDiscriminator, UIName, TemplateFileName, BusinessObjectId | Follow pagination and require exactly one case-sensitive BusObjTopDiscriminator equal to SalaryRangeDifferential | BusinessObject: SalaryRangeDifferential; UI Name: Salary Range Differential; Template File Name: SalaryRangeDifferential.dat; BusinessObjectId | Stop as a registered-business-object validation gap; do not substitute a similarly named object |
| read_salary_range_differential_schema | Before accepting any Salary Range Differential field | Resolved SalaryRangeDifferential business object | /hcmRestApi/resources/latest/dataLoaderBusinessObjects/<BusinessObjectId>; /documents/files/<UcmContentId>/data; child business-object and attribute metadata collections | Template sections SalaryRangeDifferential and SalaryRangeDifferentialValue; AttributeName, AttributeLabel, DataType, MandatoryStatus, DataLength, NumberPrecision, lookup and reference-object metadata | Require a readable current template whose root discriminator is SalaryRangeDifferential and whose attribute metadata agrees with that template | Current field contract, mandatory flags, lengths, lookup and reference dependencies | Stop as a schema-validation gap; do not infer field names, accepted values, relationship rules, or a write contract |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Registered business object or schema lookup returns 401 or 403 | Stop as an authentication or privilege failure. |
| Registered business object or schema lookup returns 500 or an incompatible response | Stop as a Fusion API or schema-validation failure; do not retry automatically. |
| Current schema changes after validation | Revalidate before any preview or import preparation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SRD.RESOLVE_BUSINESS_OBJECT | step | 10 | reference_lookup | resolved->SRD.READ_SCHEMA;not_found->SRD.HANDLE_ISSUE;lookup_failed->SRD.HANDLE_ISSUE | none | stop | Before handling a Salary Range Differentials request |
| SRD.READ_SCHEMA | step | 20 | reference_lookup | schema_ready->SRD.VALIDATE_INPUT;schema_unavailable->SRD.HANDLE_ISSUE | SRD.RESOLVE_BUSINESS_OBJECT | stop | Before field-level validation, preview, or import preparation |
