# Filters — Main Combined Create and Existing-Site POST

## Supported scope

Support only additive standard Filters. Each Filter has one `DimensionTypeCode` and exactly one matching value:

| Filter type | `DimensionTypeCode` | Required value |
| --- | --- | --- |
| Job Location | `ORA_LOCATION` | `GeographyId` |
| Organization | `ORA_ORGANIZATION` | `OrganizationId` |
| Job Category | `ORA_JOB_FAMILY` | `JobFamilyId` |
| Job Function | `ORA_JOB_FUNCTION` | `JobFunctionCode` |
| Recruiting Type | `ORA_RECRUITING_TYPE` | `RecruitingTypeCode` |

Reject an unknown type, a blank matching value, multiple type-specific values in one Filter, or duplicate requested type/value pairs. DFF filters, Filter PATCH, and Filter DELETE are out of scope.

## Effective filter behavior

For a read of current site filtering, an empty `filters` collection is not an unconfigured or unknown state. It is the Site Editor's **All** selection: no site-level restriction applies to Job Locations, Organizations, Job Categories, Job Functions, or Recruiting Types. State that effective behavior explicitly.

When a collection contains one or more rows of a supported type, state the resolved persisted values for that type. An absent type remains **All**; do not imply that a restriction in one category restricts another category.

## LOV resolution and input validation

Resolve every requested Filter against the live Site Editor LOV immediately before archive generation. Perform a fresh read for each Filter type in every create, existing-site Filter POST, and preflight rerun; reuse a collection only within that one preflight. Do not use a project copy, a prior preflight response, a previously displayed list, or a caller-supplied ID/code without confirming it is currently selectable. Persist only the selected value and display label as redacted preflight evidence.

| Filter type | Live LOV request | Selected value written to DAT | Validation rule |
| --- | --- | --- | --- |
| Job Location | Search `recruitingGeographyHierarchyLocationsLOV` with `findByWord`, `FilterAttributes=GeographyName`, `SearchTerms=<search>`, `limit=100`; then confirm with `recruitingHierarchyLocations?finder=findByGeographyIds;Ids=<GeographyId>` | exact returned `GeographyId` | Accept an exact supplied ID only after the by-ID response contains that ID. A name search must produce one exact display-name match; otherwise show the choices and require a selection. |
| Organization | Search `recruitingOrganizationsLOV` with `findByWord`, `FilterAttributes=Name`, `SearchTerms=<search>`, `StartsWithFlag=true`, `limit=100`; then read `recruitingOrganizationsLOV/<OrganizationId>` | exact returned `OrganizationId` | Accept an exact supplied ID only after the item read returns that ID. A name search must produce one exact display-name match; otherwise require a selection. |
| Job Category | List `jobFamiliesLov` with `limit=499`, `offset=0`, `orderBy=JobFamilyCode`, `onlyData=true` | exact returned `JobFamilyId` | Require one exact ID or display-name match and `ActiveStatus='A'`; filter inactive rows from the returned collection before presenting choices. |
| Job Function | `recruitingCEDictionaries/1/lov/genericHcmLookups?finder=findByLookupType;LookupType=JOB_FUNCTION_CODE&onlyData=true&limit=1000` | exact returned `LookupCode` | Require an exact case-sensitive code, or exactly one case-insensitive display-meaning match. More than one display-meaning match requires a selection. |
| Recruiting Type | `recruitingCEDictionaries/1/lov/genericHcmLookups?finder=findByLookupType;LookupType=ORA_IRC_RECRUITING_TYPE&onlyData=true&limit=1000` | exact returned `LookupCode` | Require an exact case-sensitive code, or exactly one case-insensitive display-meaning match. More than one display-meaning match requires a selection. |

The read-only resolver may present matching LOV entries to the user, but it must not guess among multiple matches. If the lookup is unavailable, empty, or fails to return the selected identifier/code, stop before preview. For Job Category, an inactive result is invalid even if its name or ID otherwise matches. The current Site Editor contracts expose no equivalent active-status field for the Location, Organization, Job Function, or Recruiting Type responses, so their eligibility is their presence in the respective live LOV.

For the generic HCM lookup responses, normalize field names only: read `LookupCode` or `lookupCode` as the code and `Meaning` or `meaning` as the display meaning. Do not lowercase or otherwise transform the returned code when writing the DAT. Thus a unique `Administrative` meaning resolves to `ADMIN`; unique `Campus` and `Contingent` meanings resolve to `ORA_CAMPUS` and `ORA_CONTINGENT`, respectively. These are lookup results, not caller-provided substitutions.

For all five Filter LOV requests, preserve the Site Editor language context: include `Ora-Irc-Language: en` and `Accept-Language: en`. For either generic HCM LOV, send `finder=findByLookupType;LookupType=<exact lookup type>`, `onlyData=true`, and `limit=1000` as separate query parameters. The finder expression is the *value* of the `finder` parameter; do not split `LookupType` into a separate query parameter or omit the language headers. Do **not** send `REST-Framework-Version`: this LOV returns HTTP 500 in the target environment when that header is present. An empty collection from a request that does not meet this shape is a lookup-request defect, not evidence that the Fusion values are absent.

For every generic-LOV resolution, persist a redacted request receipt beside the response: endpoint path, the complete `finder` value, `onlyData`, `limit`, the two language-header **names and values**, response status, and returned count. Never persist authorization, cookies, or other headers. A response file containing only an empty `items` array without this receipt is insufficient to report that a Job Function or Recruiting Type is unavailable. A single fresh, correctly evidenced empty response blocks the request; do not perform a redundant second read.

Use the shared core client, not a browser replay or a direct curl. For Job Function the required read is:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /hcmRestApi/resources/latest/recruitingCEDictionaries/1/lov/genericHcmLookups \
  --query 'finder=findByLookupType;LookupType=JOB_FUNCTION_CODE' \
  --query onlyData=true --query limit=1000 \
  --header 'Ora-Irc-Language=en' --header 'Accept-Language=en'
```

For Recruiting Type, substitute only `ORA_IRC_RECRUITING_TYPE` for `JOB_FUNCTION_CODE`. Capture the response through the core client's safe output mechanism; never copy authorization or cookie headers into project evidence.

The Job Function request has exactly these additional headers: `Ora-Irc-Language: en` and `Accept-Language: en`. Do not add `REST-Framework-Version`, even when it is used by another Recruiting REST request.

The confirmed Job Function REST body is `{"DimensionTypeCode":"ORA_JOB_FUNCTION","JobFunctionCode":"ADMIN"}`. It demonstrates that the DAT must carry `ADMIN`, never the display text `Administrative`.

Normalize the request to the returned identifier/code before checking duplicates. For an existing site, compare that normalized `DimensionTypeCode`/value pair to the expanded Filters collection. For a combined create, compare normalized pairs within the requested set. A same type with a different resolved value is permitted.

## Required main registration contract

Use the fresh portal registration and generated DAT as the source of truth. The Filters contract must have:

| Setting | Required value |
| --- | --- |
| Table / surrogate | `IRC_AVAIL_CONTEXT`; `ObjectCtxId` / `OBJECT_CXT_ID` |
| Parent hierarchy | `ParentId=SiteNumber`, with a String `SiteNumber` routing attribute |
| Parent alternate key | `SiteCode` resolves `SITE_NUMBER AS SiteNumber` from external `IRC_CX_SITES_B` for `SITE_TYPE='EXT'` |
| Child foreign keys | Empty. Do not configure an `ObjectId` foreign key or resolver. |
| Child object user keys | None for POST-only Filters support |
| POST / PATCH URL overrides | Blank; do not depend on custom URLs |
| Mandatory on create | `DimensionTypeCode` only |
| Exclude in payload | `SiteNumber`, `SiteCode`, and internal nonbusiness fields; never `ObjectCtxId`. `ObjectId` may be absent from the generated header. |

`ObjectCtxId` is a selected REST key. It must remain in the DAT and REST mapping, be blank for a new POST, and remain nonmandatory. Excluding it from the REST model makes template generation fail. `ObjectId` is the physical database relationship, but Fusion supplies it through the nested REST association and may omit it from the generated header. A Data Loader `ObjectId` foreign-key lookup would run before a same-load parent exists, so it must not be configured.

## Combined create

Include the `filters` metadata section only when the caller requests one or more Filters. For each approved Filter, create one `MERGE|filters|...` row from the sanitized live header.

### Type-to-column serialization invariant

Build each Filter row as a header-indexed field map, never by appending a value after a run of blank delimiters. Set `DimensionTypeCode` and exactly one value column from this table; set every other type-specific value column to blank.

| `DimensionTypeCode` | Sole populated value column |
| --- | --- |
| `ORA_LOCATION` | `GeographyId` |
| `ORA_ORGANIZATION` | `OrganizationId` |
| `ORA_JOB_FAMILY` | `JobFamilyId` |
| `ORA_JOB_FUNCTION` | `JobFunctionCode` |
| `ORA_RECRUITING_TYPE` | `RecruitingTypeCode` |

After constructing the final pipe-delimited row, split it using the exact live `filters` header and assert all of the following before preview:

1. `DimensionTypeCode` equals the approved type.
2. Its mapped value column equals the resolved ID or lookup code.
3. Every other type-specific value column is blank.
4. `ObjectCtxId` and `SiteNumber` are blank, `SiteCode` is the requested parent code, and `RestAction=POST`.

For the current generated header order, a Recruiting Type row must map as follows; this is an illustration of the header-indexed result, not a template to concatenate manually:

```text
ObjectCtxId=blank
DimensionTypeCode=ORA_RECRUITING_TYPE
GeographyId=blank
JobFamilyId=blank
JobFunctionCode=blank
OrganizationId=blank
RecruitingTypeCode=ORA_CAMPUS
SiteNumber=blank
SiteCode=<parent SiteCode>
RestAction=POST
```

Reject the source as a structural/mapping defect if an approved Recruiting Type value appears in `OrganizationId`, or if any resolved value appears in a column other than its mapped column. Do not submit or retry such an archive.

| Field | Combined-create value |
| --- | --- |
| `ObjectCtxId` | blank |
| `SiteNumber` | blank |
| `SiteCode` | exact requested parent Site Code when present in the live header |
| `DimensionTypeCode` | approved type |
| matching type-specific business field | approved value |
| every other type-specific business field | blank |
| `RestAction` | `POST` |

Use the normal field-map serializer and cardinality gate. A Filter row must not include a value for an excluded internal field or a second type-specific business field. After a successful combined load, read the parent and confirm each approved type/value pair is present in its Filters collection.

## Existing-site Filter POST

Resolve exactly one existing parent by Site Code and retain its opaque String `SiteNumber`. Check the current Filters collection first; stop as an idempotent duplicate if the exact requested type/value pair already exists.

Generate a child-only archive with top-level `recruitingCESites` metadata and `filters` metadata, but no parent data row. For each requested Filter row:

| Field | Existing-site POST value |
| --- | --- |
| `ObjectCtxId` | blank |
| `SiteNumber` | blank |
| `SiteCode` | exact persisted parent code |
| `DimensionTypeCode` and one matching business field | approved values |
| all other business fields | blank |
| `RestAction` | `POST` |

Generate an immutable archive preview and obtain the ordinary per-archive Data Loader approval. After final success, read back the parent Filters collection and verify all approved additions; verify parent, Languages, and Cookie Consent remain unchanged.
