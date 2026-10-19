# Legal Entity Calculation Cards REST Execution

## Binding REST Access Boundary

REST access in this resource is retrieval-only. Use it to discover PSU, LDG, card, component, override, LOV, and template data. Never construct, preview, approve, retry, or call a direct REST mutation payload. Route every create, update, correction, end-date, and delete to target-supported `CalculationCard` HDL through `core.data-loader`. A read-only action may use `POST` when that is its retrieval contract. This boundary overrides any historical mutation evidence.

## Read-Only Existing-State and Operation Sequence

1. Resolve the functional PSU and LDG, then run owner-scoped mode=G card discovery without `dirCardId`.
2. Match the requested card by business name across every source-backed current, future, and historical interval. Retain the unique returned `dirCardId` internally and use it for exact drilldown; never ask the functional user for it.
3. Resolve component, override/FLEX/value, assignment/association, and other source-backed related rows by parent-scoped business keys. Retain every technical ID only as internal retrieval correlation.
4. Classify each requested object as CREATE, EXISTING_AT_DATE, EXISTS_OUTSIDE_DATE, or AMBIGUOUS. Do not interpret an empty response for one date as global absence.
5. For a complete no-match leaf, announce the create classification and prepare HDL using resolved parents. For any existing business key, show its business interval/value and requested date, then ask for Update or Correction before DAT preview.
6. Recommend Correction when the requested date equals the selected row start. Recommend Update when it is later inside the selected interval. For gaps or future-row conflicts, offer only actions proven by live HDL metadata.

## Runtime Sources

| Source | Purpose |
|---|---|
| Task manifest | Provides task code, task name, and CSV export/import support flags |
| Effective setup task catalog | Confirms task availability and export/import support |
| Release setup task catalog description | Identifies the task as predefined calculation cards for payroll statutory units |
| Redacted Legal Entity Calculation Cards FSM launch URL | Documents the UI launch path and FS_SCOPEINFOS shape for task-scoped launch context |
| Redacted Legal Entity Calculation Cards HAR | Documents read-only Redwood calculationEntries retrieval, query finders, response fields, and LOV metadata; any captured mutation behavior is historical, prohibited, and non-executable |
| Live `hcmLegalEntities` describe plus redacted advanced-search validation | Confirms the versioned standard resource path, POST method, Oracle action request/response media types, request fields, pagination, response shape, and successful read-only execution without retaining environment-specific values |
| Redacted legislative-data-group advanced-search capture | Documents the POST-with-JSON-body contract for full or partial LDG-name and territory-scoped discovery; the environment host and `rv:` route token remain runtime-only |
| Calculation entries UI source resolution pattern | Provides the Legal Entity ID to payroll statutory unit source resolver through payGenericRestQuery and OrgPayrollStatutoryUnitPVO |
| Calculation entries UI add-card pattern | Provides the read-only `getCardDetails mode=ADD` definition and default-value lookup; it does not create a card |
| Task-specific CSV export contract | Required only for a requested read-only setup export; currently TBD |
| Oracle REST metadata or describe source | Required only for a read-only retrieval contract |

## Execution Contract

| Situation | What Happens |
|---|---|
| Read-only setup export is requested | Use the approved task-specific CSV export contract when supplied |
| Calculation-card import is requested | Prepare target-supported `CalculationCard` HDL and route the approved artifact through `core.data-loader`; do not use CSV/FSM or direct business REST as the mutation route |
| Launching the task UI is requested | Use the Redwood calculation-entries launch URL with source=FSM and the redacted FS_SCOPEINFOS shape; this is UI navigation, not REST execution |
| FS_SCOPEINFOS contains a LEGAL_ENTITY_ID group | Parse the launch context with the launch-page readScopeInfoParams rule, resolve the payroll statutory unit through OrgPayrollStatutoryUnitPVO, and verify sourceType=PSU before preview or live execution |
| Legal entity availability is requested | Send a read-only POST to the versioned standard `findByAdvancedSearchQuery` action with the Oracle action media types and the mandatory `PsuFlag=Y` filter; for one or more matches, return only the `Name` values under `Legal Entity names:`, one per line. Complete a list-only request after the list; require selection only before downstream PSU or card work when multiple rows matched |
| Legislative Data Group availability is requested | For name search, send the trimmed full or partial name as `query` with no filters. For “all US LDGs”, send an empty query with the `TerritoryShortName=United States` filter. Return every matched `Name` under `Legislative Data Group names:` and require a selection only before downstream card work when multiple rows matched |
| Parent requests combined LDG, PSU, and TRU discovery | Contribute one completely paged `OrgPayrollStatutoryUnitPVO` query by legislation code with `Name`, `OrganizationId`, and `LdgId`. Do not fan out by LDG, render a standalone list, or mutate data |
| Card summary is requested | Resolve `dirCardId` automatically from owner-scoped business-name discovery, then POST getCardDetails with the internal ID, effectiveDate, and expand=Cards |
| Available cards for create are requested | Only after complete existing-state discovery finds no matching card, POST getCardDetails with sourceId, sourceType=PSU, effectiveDate, expand=Cards, and mode=ADD; do not ask for dirCardId |
| Available components for create are requested | GET payGenericRestQuery with PayRestName=CIRComponentPVO, ParameterKeys=pRelId&#124;&#124;pCardBaseName&#124;&#124;pEffectiveDate&#124;&#124;pLDGId, and pRelId populated from sourceId |
| Card drilldown is requested | POST getCardDetails with expand=Cards,Components,Overrides,CompAssociation, mode=G, isGlobalPage=true, showEmptyComponent=N, sourceId, and sourceType=PSU |
| Current/default flexfield values for one component are requested | Use the read-only getCardDetails existing-component or add-template contract, select one exact component, keep only its `overrideType=FLEX` rows, and return the business-facing value list defined below |
| Add-card or add-component attribute template is requested | POST getCardDetails with mode=ADD, expand=Cards,Components,Overrides,Associations, sourceType=PSU, sourceId, legislativeDataGroupId, effectiveDate, cardBaseName, and either `dirCardCompDefId` alone or BaseComponentName-to-overrideBaseGroupName plus ComponentName-to-overrideGroupName. Resolve and send required `contextN` fields first; never combine the definition ID with group-name fields. |
| New card is requested | First prove no matching card exists across complete current/future/history state; then retrieve definitions with `getCardDetails mode=ADD` and prepare a `CalculationCard` HDL create preview |
| Component or LOV choices are requested | Use payGenericRestQuery or payrollGenericLOV with PayRestName, ParameterKeys, DisplayAttributes, and binds derived from the active card metadata |
| Override, FLEX, value, assignment, association, or related row is requested | Resolve its complete business-key state. Create only a complete no-match leaf; when it exists, disclose the interval/current value and ask for Update or Correction |
| Component is corrected, updated, or end-dated | Retrieve complete history and parent keys, disclose existing data, obtain the applicable user confirmation, then prepare the target-supported HDL operation |
| Card or component is deleted | Prepare a target-supported HDL delete only after live template and action validation; block instead of falling back to REST |
| Task-specific CSV export contract is missing | Block only the requested read-only CSV export; it does not change the HDL mutation route |
| Direct REST write is requested | Reject the route and prepare HDL instead; REST mutation metadata does not authorize a write |
| Sample payload is supplied outside the HAR-backed contract | Treat it as an example only and do not use it as the payload contract |
| Live business change is requested | Require an exact HDL DAT preview and the `core.data-loader` approval gate before upload or load; do not retry automatically |

## HDL Date-Effective Operation Guardrails

| Mode | Required Behavior |
|---|---|
| Correct or update | Retrieve the exact current row and history, preserve the original parent keys and effective interval, and use only a target-supported HDL action |
| End date | Retrieve the exact target interval and prepare the target-supported HDL end-date action; block when live metadata does not prove it |
| Delete record or history | Require current target metadata to prove the HDL delete action and complete user key; otherwise block without a REST fallback |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Launch Legal Entity Calculation Cards UI | GET | /fscmUI/redwood/calculation-entries/calculation-entries/launch?FS_SOURCE=FS&source=FSM&pageTitle=Legal+Entity+Calculation+Cards&FS_SCOPEINFOS=XLE_ENTITY_PROFILE***LEGAL_ENTITY_ID***{LegalEntityId}***{LegalEntityName} |
| Open Legal Entity Calculation Cards card details UI | GET | /fscmUI/redwood/calculation-entries/calculation-entries/card-details?sourceType=PSU&sourceId={sourceId}&pDirCardId={dirCardId}&pCardBaseName={cardBaseName}&pCardName={cardName}&pEffectiveDate={effectiveDate}&pLegislativeDataGroupId={legislativeDataGroupId}&pDirCardDefinitionId={dirCardDefinitionId}&pDisplayName={displayName} |
| Describe legal entities and action media types | GET | /hcmRestApi/resources/11.13.18.05/hcmLegalEntities/describe |
| Find legal entities by advanced search | POST with JSON body and Oracle action media types | /hcmRestApi/resources/11.13.18.05/hcmLegalEntities/action/findByAdvancedSearchQuery |
| Find Legislative Data Groups by full or partial name or territory | POST with JSON body | /hcmRestApi/rest/rv:{runtime-route-id}/en/11.13.18.05:9/legislativeDataGroups/action/findByAdvancedSearchQuery |
| Get card summary | POST | /hcmRestApi/redwood/11.13.18.05/calculationEntries/getCardDetails |
| List cards available for create | POST | /hcmRestApi/redwood/11.13.18.05/calculationEntries/getCardDetails |
| Get card details with components and overrides | POST | /hcmRestApi/redwood/11.13.18.05/calculationEntries/getCardDetails |
| Get add-card template | POST | /hcmRestApi/redwood/11.13.18.05/calculationEntries/getCardDetails |
| Query component definitions | GET | /hcmRestApi/redwood/11.13.18.05/calculationEntries/payGenericRestQuery |
| Query component contexts | GET | /hcmRestApi/redwood/11.13.18.05/calculationEntries/payGenericRestQuery |
| Resolve payroll statutory unit from legal entity | GET | /hcmRestApi/redwood/11.13.18.05/calculationEntries/payGenericRestQuery |
| Query deduction group or override LOV | GET | /hcmRestApi/resources/11.13.18.05/payrollGenericLOV |
| Setup task CSV export job | POST | /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports |
| Setup task CSV template export job | POST | /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports |

## Legal Entity Availability REST Contract

Use this contract only for read-only legal-entity discovery. Route it through `core.fusion-api.rest-api-client/scripts/fusion_rest_client.py` with `--method POST`, the two required `--header` options below, and a JSON body. Read the active host and OAuth configuration from `core/auth/fusionEnv.properties`.

| Item | Contract |
|---|---|
| Method | `POST` with a JSON request body |
| Primary resource path | `/hcmRestApi/resources/11.13.18.05/hcmLegalEntities/action/findByAdvancedSearchQuery` |
| Describe path | `/hcmRestApi/resources/11.13.18.05/hcmLegalEntities/describe` |
| Request media type | `Content-Type: application/vnd.oracle.adf.action+json` |
| Response media types | `Accept: application/vnd.oracle.adf.actionresult+json, application/json` |
| UI-captured alternative form | `/hcmRestApi/rest/rv:{runtime-route-id}/en/11.13.18.05:9/hcmLegalEntities/action/findByAdvancedSearchQuery`; reference only, not the default execution path |
| Environment rule | Use `restBaseUrl` from `core/auth/fusionEnv.properties`; never persist or reuse a captured pod hostname |
| Route-token rule | Treat `rv:{runtime-route-id}` as environment/runtime-specific; never hardcode it, substitute `rv:null`, or use a token captured from another environment. Prefer the versioned standard resource path. |
| Body encoding | JSON encoded with the Oracle ADF action request media type; plain `Content-Type: application/json` is not sufficient for the versioned standard action |
| PSU eligibility filter | Always send `filters` as an array containing one object with `name: ["PsuFlag"]` and `terms: ["Y"]`; an empty filter array is invalid for this PSU-scoped availability contract |
| Side effects | None; availability search needs no mutation approval |

For the Central client, pass these options exactly:

```text
--method POST
--header "Content-Type: application/vnd.oracle.adf.action+json"
--header "Accept: application/vnd.oracle.adf.actionresult+json, application/json"
```

If Fusion reports that the operation is unsupported for the invoked HTTP method, retrieve the `describe` path and verify the action method and media types before one corrected attempt. Do not repeat the unchanged failing POST.

Construct `query` as follows:

1. Trim the user input and reject empty text or a value containing only `%` wildcards.
2. If the user supplies a valid wildcard query, preserve it.
3. Otherwise split the text on whitespace, join the nonblank terms with `%`, and add leading and trailing `%`. Example: `SA Regression` becomes `%SA%Regression%`.
4. Do not append the search text to the URL. Send it only in the JSON body.
5. Independently of the query text, add the mandatory `PsuFlag=Y` filter. Do not treat `PsuFlag` as a search field or append it to the query string.

### Sample Request

```json
{
  "query": "%SA%Regression%",
  "displayFields": [
    "Name",
    "LegalEmployerFlag",
    "PsuFlag",
    "ParentPsuName",
    "LegalEntityIdentifier",
    "EffectiveFrom",
    "EffectiveTo",
    "LegalEntityId"
  ],
  "searchFields": [
    "Name",
    "LegalEntityIdentifier"
  ],
  "limit": "500",
  "filters": [
    {
      "name": [
        "PsuFlag"
      ],
      "terms": [
        "Y"
      ]
    }
  ],
  "offset": 0
}
```

### Redacted Sample Response

```json
{
  "result": {
    "summary": [
      {
        "offset": "0",
        "limit": "500",
        "count": "3",
        "hasMore": "false"
      }
    ],
    "items": [
      {
        "LegalEntityIdentifier": "EXAMPLE_SA_REGRESSION_LE1",
        "LegalEntityId": "300100000000001",
        "LegalEmployerFlag": "Y",
        "EffectiveFrom": "2009-01-01",
        "ParentPsuName": null,
        "PsuFlag": "Y",
        "EffectiveTo": null,
        "Name": "Example SA Regression Legal Entity"
      },
      {
        "LegalEntityIdentifier": "EXAMPLE_SA_REGRESSION_LE23",
        "LegalEntityId": "300100000000002",
        "LegalEmployerFlag": "Y",
        "EffectiveFrom": "2009-01-01",
        "ParentPsuName": null,
        "PsuFlag": "Y",
        "EffectiveTo": null,
        "Name": "Example SA Regression Legal Entity23"
      },
      {
        "LegalEntityIdentifier": "EXAMPLE_SA_REGRESSION_LEQA",
        "LegalEntityId": "300100000000003",
        "LegalEmployerFlag": "Y",
        "EffectiveFrom": "2009-01-01",
        "ParentPsuName": null,
        "PsuFlag": "Y",
        "EffectiveTo": null,
        "Name": "Example SA Regression Legal EntityQA"
      }
    ]
  }
}
```

### Response Handling

1. Parse `result.summary[0]` and `result.items`. Accept numeric fields returned as strings or numbers.
2. If `hasMore` is true, request the next offset with the same query, fields, and `PsuFlag=Y` filter until it is false. Deduplicate by `LegalEntityId` while preserving response order.
3. For zero candidates, state that no legal entity matched and ask the user to refine the search.
4. For one or more candidates, show only the heading `Legal Entity names:` and every returned `Name`, one name per line in response order. Do not number the names.
5. Do not display `LegalEntityId`, `LegalEntityIdentifier`, `PsuFlag`, `LegalEmployerFlag`, `ParentPsuName`, effective dates, counts, offsets, or `hasMore` by default. Retain these values internally for validation and downstream routing, and show them only when the user explicitly requests technical details.
6. For a list-only request, stop successfully after the names-only response. When downstream PSU or card work is also requested and multiple candidates matched, wait for the user to select one; do not rank or fuzzy-select.
7. Verify every returned row has `PsuFlag=Y`. A different value is a Fusion API/source-contract failure because the request already includes the PSU eligibility filter; do not return or use that row.

Default response shape:

```text
Legal Entity names:
Example Legal Entity One
Example Legal Entity Two
```

## Legislative Data Group Availability REST Contract

Route this read-only lookup through `core.fusion-api.rest-api-client`, using `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py --method POST`. Resolve the host and authentication at runtime from `core/auth/fusionEnv.properties` and resolve the route identifier in the active environment.

| Property | Contract |
|---|---|
| Method | `POST` with a JSON request body |
| Observed browser-routed path | `/hcmRestApi/rest/rv:{runtime-route-id}/en/11.13.18.05:9/legislativeDataGroups/action/findByAdvancedSearchQuery` |
| Headers | Send `Content-Type: application/json` and `Accept: application/json` |
| Environment rule | Build the absolute URL from the active `restBaseUrl`; never persist or reuse the supplied example pod hostname |
| Route rule | Discover or receive the `rv:` route identifier at runtime; never hardcode a captured route token or copy it to another environment |
| Name-query rule | Trim surrounding whitespace, reject blank or all-`%` name input, preserve the remaining full or partial LDG name exactly, and send `filters=[]`; do not add wildcards |
| Territory-query rule | For “all US LDGs”, send `query=""` and `filters=[{"name":["TerritoryShortName"],"terms":["United States"]}]`. Empty query is valid only because this nonblank restrictive filter is present |
| Unbounded-search rule | Reject `query=""` with `filters=[]`, a blank filter term, or an unsupported territory mapping |
| Side effects | None; this search does not create, update, ZIP, upload, or load data |

### LDG Sample Request

The example uses synthetic names while preserving the supplied request shape.

```json
{
  "query": "Example US Sun Power",
  "limit": "500",
  "displayFields": [
    "Name",
    "CurrencyName",
    "TerritoryShortName",
    "CostAllocationStructureName",
    "LegislativeDataGroupId"
  ],
  "searchFields": [
    "Name"
  ],
  "filters": [],
  "offset": 0
}
```

A partial-name request changes only `query`, for example `"query": "Example US"`. Preserve all other fields.

### Territory Sample Request

Use this payload when the user asks for all US LDGs:

```json
{
  "query": "",
  "limit": "500",
  "displayFields": [
    "Name",
    "CurrencyName",
    "TerritoryShortName",
    "CostAllocationStructureName",
    "LegislativeDataGroupId"
  ],
  "searchFields": [
    "Name"
  ],
  "filters": [
    {
      "name": [
        "TerritoryShortName"
      ],
      "terms": [
        "United States"
      ]
    }
  ],
  "offset": 0
}
```

### LDG Redacted Sample Response

```json
{
  "result": {
    "summary": [
      {
        "offset": "0",
        "limit": "500",
        "count": "1",
        "hasMore": "false"
      }
    ],
    "items": [
      {
        "LegislativeDataGroupId": "300100000000201",
        "TerritoryShortName": "United States",
        "Name": "Example US Sun Power",
        "CurrencyName": "US Dollar",
        "CostAllocationStructureName": "Example Costing Structure"
      }
    ]
  }
}
```

### LDG Response Handling

1. Parse `result.summary` and `result.items`; accept numeric pagination fields as strings or numbers.
2. If `hasMore` is true, repeat the same POST with the next offset until false, preserving the query, fields, and filters. Deduplicate by `LegislativeDataGroupId` and preserve first-seen order.
3. For a territory-scoped response, verify every returned `TerritoryShortName` equals the normalized requested territory. Treat a mismatch as a response-contract failure.
4. For zero rows, state that no Legislative Data Group matched the supplied name or territory and invite the user to refine it.
5. For one or more rows, return only `Legislative Data Group names:` followed by every returned `Name`, one name per line in response order. Do not number the names.
6. Keep IDs, currency, territory, costing structure, counts, offsets, and pagination internal unless technical details are requested.
7. Complete a list-only request after returning the full list. If downstream card work was also requested and multiple LDGs matched, wait for the user to select one; do not rank or fuzzy-select.

Default response shape:

```text
Legislative Data Group names:
Example US Sun Power
```

When more than one row matches, include every name in the same shape:

```text
Legislative Data Group names:
Example US Sun Power
Example US Solar Services
```

## Component Flexfield Value List


### Request Routing

| Component state | Request contract | Selection rule |
|---|---|---|
| Existing component | POST `getCardDetails` with `sourceType=PSU`, `mode=G`, `isGlobalPage=true`, `showEmptyComponent=N`, and `expand=Cards,Components,Overrides,CompAssociation` for the exact card and effective date | Match one returned component by component name or base name; when names repeat, show business labels/effective intervals for user selection and keep `componentSequence` internal |
| Addable component template | POST `getCardDetails` with `sourceType=PSU`, `mode=ADD`, `isGlobalPage=true`, and `expand=Cards,Components,Overrides,Associations`, using the selected card base name and source-backed component override group names | Match one component template and report its returned default values; do not present template defaults as saved card values |

### Response Handling

1. Verify that the returned card has `sourceType=PSU`, the selected owner/card, and the requested effective date context.
2. Select exactly one component. Do not combine overrides from components that share a display name; use source-backed business labels, effective intervals, and current-value context for user selection, and keep `componentSequence` internal.
3. From the selected component only, retain rows whose `overrideType=FLEX`, preserving response order.
4. Use nonblank `title` as the business label and otherwise use `name`. A row without either label is a malformed source response and must not be invented.
5. Use the current/default `value`. For an LOV-backed row with a stored code, resolve one display meaning through the metadata-declared `dataSource` when possible. If zero or multiple meanings match, return the stored value and do not guess. This read-only fallback does not validate the code for a future write.
6. Render a null or empty value as `Blank`. When no FLEX rows exist for the exact component, return `None` under the heading.
7. Return only the heading `Flexfield values:` and one `Name: Value` line per FLEX row. Do not display IDs, override codes, categories, flags, `dataSource`, pagination, or component metadata unless the user explicitly requests technical details.
8. If the user asks for allowed or available values for a field, run the metadata-declared LOV option-list lookup instead. Do not silently replace current/default values with LOV options.

Default response shape:

```text
Flexfield values:
Example Attribute: Example Value
Example Optional Attribute: Blank
```

## Finder Contracts

For `payGenericRestQuery`, serialize the complete finder contract in one query parameter: `finder=findByWord;PayRestName=<PVO>,AdditionalViewCriteria=<criteria>,ParameterKeys=<keys>,ParameterValues=<values>,DisplayAttributes=<attributes>`. Keep `||` as the runtime separator inside values and encode it as `%7C%7C` only in a rendered URL. Never split these finder inputs into separate query parameters.

| Operation | Endpoint | Finder | PayRestName | Parameter Keys | Display Attributes | Response Fields |
|---|---|---|---|---|---|---|
| Deduction group lookup | payrollGenericLOV | findByWord | DeductionGroupVO | pBaseCardDisplayName, pEffectiveDate, pLegCode | BaseName, Name, DeductionGroupId | ResultValue1, ResultValue2, ResultValue3 |
| Override value lookup | payrollGenericLOV | findByWord | PayValueSetVO or metadata-declared source | pValueSetCode, pBinds, and metadata-declared binds | Code, Meaning, declared key attributes | Code, Meaning, ResultValue fields, and declared key fields |
| Existing-card component lookup | payGenericRestQuery | findByWord | CIRComponentPVO | pRelId, pCardBaseName, pEffectiveDate, pLDGId | BaseDisplayName, DirCardDefinitionId, BaseComponentName, DirCardCompDefId, ComponentName, DeductionGroupId, ParentDirCardCompDefId, ComponentSequence | Code, Meaning, BaseDisplayName, DirCardDefinitionId, BaseComponentName, DirCardCompDefId, ComponentName, DeductionGroupId, ParentDirCardCompDefId, ComponentSequence |
| Add-card component lookup | payGenericRestQuery | findByWord | CIRComponentPVO | pCardBaseName, pEffectiveDate, pLDGId | BaseDisplayName, DirCardDefinitionId, BaseComponentName, DirCardCompDefId, ComponentName, DeductionGroupId, ParentDirCardCompDefId, ComponentSequence | Code, Meaning, BaseDisplayName, DirCardDefinitionId, BaseComponentName, DirCardCompDefId, ComponentName, DeductionGroupId, ParentDirCardCompDefId, ComponentSequence |
| Component context lookup | payGenericRestQuery | findByWord | ComponentContextPVO | pDirCardCompDefId, pEffectiveDate, pLc, pLdg | DisplayContextName, Sequence, VoName, LookupType | DisplayContextName, Sequence, VoName, LookupType when rows exist; HAR sample returned zero rows |
| Legal entity to payroll statutory unit lookup | payGenericRestQuery | findByWord with AdditionalViewCriteria=findByLegalEntityId | OrgPayrollStatutoryUnitPVO | pLegalEntityId | OrganizationId&#124;&#124;LdgId | OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=PSU as task scope |
| Legislation code to payroll statutory unit list | payGenericRestQuery | findByWord with AdditionalViewCriteria=findByLegislationCode | OrgPayrollStatutoryUnitPVO | pLegislationCode | LegalEntityId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId | LegalEntityId as legal entity context, Name for user-facing list, OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=PSU as task scope |
| Legislation code and LDG ID to payroll statutory unit list | payGenericRestQuery | findByWord with AdditionalViewCriteria=findByLegislationCode&#124;&#124;findByLdgId | OrgPayrollStatutoryUnitPVO | pLegislationCode&#124;&#124;pLdgId | LegalEntityId&#124;&#124;Name&#124;&#124;OrganizationId&#124;&#124;LdgId | Preferred when LdgId is already known; LegalEntityId as legal entity context, Name for user-facing list, OrganizationId as sourceId, LdgId as legislativeDataGroupId, and sourceType=PSU as task scope |

## Request and Response Fields

| Operation | Field | Placement | Type | Required | Source-Backed Rule |
|---|---|---|---|---|---|
| Card summary | dirCardId | Request body | number | Yes | Identifies the card for getCardDetails |
| Card summary | effectiveDate | Request body | date | Yes | Observed format is YYYY-MM-DD |
| Card summary | expand | Request body | string | Yes | Use Cards for summary |
| Create-card list | sourceId, sourceType, effectiveDate | Request body | mixed | Yes | sourceType must be PSU and sourceId must be resolved before listing available cards |
| Create-card list | mode, expand | Request body | string | Yes | Use mode=ADD and expand=Cards; dirCardId is not expected before card creation |
| Create-card list response | cardName | Response body | string | Yes for user display | Display this value to the user when listing cards that can be added |
| Card summary response | cardBaseName, cardName, dirCardDefinitionId, dirCardId, cardSequence | Response body | mixed | Yes for card identity | Preserve for drilldown and HDL parent-key resolution; never place runtime IDs in the DAT |
| Card summary response | sourceType, sourceId, payrollStatUnitId, legislativeDataGroupId, legislationCode | Response body | mixed | Yes for scoped operations | sourceType must be PSU for this Legal Entity flow |
| Card summary response | readOnlyFlag | Response body | string | Yes for editability evidence | Treat `Y` as a blocker for the requested HDL business change; it never enables a REST write |
| Card drilldown | expand | Request body | string | Yes | Use Cards,Components,Overrides,CompAssociation |
| Card drilldown | mode | Request body | string | Yes | Use G for existing card drilldown |
| Card drilldown | isGlobalPage | Request body | boolean | Yes | Observed as true |
| Card drilldown | showEmptyComponent | Request body | string | Yes | Observed as N |
| Card drilldown response | components[].componentSequence, dirCardCompId, dirCardCompDefId | Response body | mixed | Conditional | Use sequence for component-specific HDL key mapping; retain runtime IDs only as lookup evidence |
| Card drilldown response | components[].overrideBaseGroupName, overrideGroupDisplayName, deductionGroupId, deductionGroupName | Response body | mixed | Conditional | Required for override grouping |
| Card drilldown response | components[].processingType, multipleAllowed, effectiveStartDate, effectiveEndDate | Response body | mixed | Conditional | Used for preview and design checks |
| Override metadata | overrides[].code, name, title, category | Response body | string | Yes for mapped overrides | Use values returned by the selected card/component; do not hard-code sample categories |
| Override metadata | overrides[].overrideType, controlType, type, nullable, contextRequired, display | Response body | mixed | Yes for validation | Metadata controls editability, null behavior, display behavior, and type validation |
| Override metadata | overrides[].dataSource | Response body | string | Conditional | Use dataSource and required binds to resolve LOV-backed fields |
| Override metadata | overrides[].format, uom, value, userOverridden | Response body | mixed | Conditional | Use for type validation, unit handling, current-state preview, and unchanged-value preservation |
| Dependent LOV metadata | dataSource binds, ParameterKeys, DisplayAttributes, parent override references | Response body or LOV request metadata | mixed | Conditional | Required when one LOV depends on another field or context value |
| Legal entity to PSU lookup | pLegalEntityId | Finder parameter | number/string | Yes when readScopeInfoParams returns sourceType=PSU | Use the redacted FS_SCOPEINFOS legal entity ID as the bind value |
| Legal entity to PSU lookup response | OrganizationId, LdgId | payGenericRestQuery response | mixed | Yes | Map OrganizationId to sourceId, LdgId to legislativeDataGroupId, and set sourceType=PSU |
| Legislation to PSU lookup | pLegislationCode | Finder parameter | string | Yes when the user supplies legislation or country code for PSU or Legal Entity Org Cards | Use the supplied legislation code, for example US |
| Legislation to PSU lookup response | LegalEntityId, Name, OrganizationId, LdgId | payGenericRestQuery response | mixed | Yes | Return Name values for list-only requests; map OrganizationId to sourceId, LdgId to legislativeDataGroupId, retain LegalEntityId, and set sourceType=PSU |
| Legislation and LDG to PSU lookup | pLegislationCode, pLdgId | Finder parameter | string/number | Yes when the user supplies legislation or country code and the LDG ID is already known | Use AdditionalViewCriteria=findByLegislationCode&#124;&#124;findByLdgId, ParameterKeys=pLegislationCode&#124;&#124;pLdgId, and ParameterValues={LegislationCode}&#124;&#124;{LdgId} |
| Add-card template | sourceId, sourceType, legislativeDataGroupId, effectiveDate, cardBaseName | Request body | mixed | Yes | sourceType must be PSU |
| Add-card template | mode, isGlobalPage, expand | Request body | mixed | Yes | mode=ADD, isGlobalPage=true, expand=Cards,Components,Overrides,Associations |
| Add-card template | components[].overrideBaseGroupName, overrideGroupName | Request body | string | Yes | Names the override group used to build the template |

## Dynamic Override Resolution

| Step | Requirement |
|---|---|
| 1 | Retrieve getCardDetails with components and overrides for the selected card/component and effective date |
| 2 | Build a per-card override schema from returned override metadata |
| 3 | Parse each LOV-backed override dataSource into resolver name, value set or lookup source, ParameterKeys, DisplayAttributes, and bind inputs |
| 4 | Build a dependency graph when any bind depends on another override or component context |
| 5 | Seed the component record from ComponentInstanceRecord, including context values, component sequence, override base group, and component ID when returned |
| 6 | Auto-carry required or populated FLEX context overrides from active metadata even when the user did not change them |
| 7 | Merge user-changed overrides by name and context so changed values replace auto-carried values |
| 8 | Resolve parent overrides, LDG, legislation code, effective date, and context binds before dependent child LOVs |
| 9 | Clear or revalidate dependent child LOV values whenever a parent value changes |
| 10 | Validate each supplied or auto-carried override value against metadata type, nullability, dataSource, and dependency order |

## Observed Override Field Examples

| Code | Name | Category | Control Type | Type | Nullable | Context Required | Value Source |
|---|---|---|---|---|---|---|---|
| BASIS_FOR_CALCULATION | Calculation Basis | HRX_AE_GRATUITY_PSU | LOV | string | true | Y | PayValueSetVO with HRX_AE_GRATUITY_BASIS |
| GRATUITY_SALARY_FORMULA | Salary Formula | HRX_AE_GRATUITY_PSU | LOV | string | true | Y | PayValueSetVO with HRX_AE_FORMULAS and LegislativeDataGroupId bind |
| GRATUITY_REFERENCE_FORMULA | Reference Formula | HRX_AE_GRATUITY_PSU | LOV | string | true | Y | PayValueSetVO with HRX_AE_FORMULAS and LegislativeDataGroupId bind |

## Preview Pattern

| Step | Requirement |
|---|---|
| 1 | Confirm task identity and nested task scope |
| 2 | If launched from FSM, parse FS_SCOPEINFOS and show the redacted legal entity scope values |
| 3 | Retrieve card summary, create-card list, or add-card template from getCardDetails |
| 4 | Build the per-card override schema and resolve LOV-backed override values in dependency order |
| 5 | Show the exact HDL `METADATA` and operation rows, resolved parent keys, target card/component, and validation evidence |
| 6 | Validate a retrieved CSV package against its approved contract when read-only setup export is requested; never use CSV/FSM import for a calculation-card business change |
| 7 | Show all remaining target-template, HDL action, lookup, and field-mapping blockers |

## HDL Handoff Pattern

| Step | Requirement |
|---|---|
| 1 | Stop when any target-template, HDL action, lookup, user-key, effective-date, or field mapping remains unresolved |
| 2 | Keep the exact DAT in chat until the user approves the preview |
| 3 | Route approved DAT/ZIP validation, upload, and load initiation only through `core.data-loader` |
| 4 | Never substitute a direct calculation-card REST mutation |
| 5 | Return loader status, identifiers, rejected rows, and redacted diagnostics when a load was explicitly authorized |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LEC.PREVIEW_BLOCK | decision | 6 | preview_gate | blocked->LEC.DONE_BLOCKED | LEC.ENFORCE | stop | HDL preview or loader handoff is requested while a read-only lookup, HDL schema, user key, action, artifact, or approval field remains unresolved |
