# Configure Item Transaction Defaults Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Oracle Fusion Cloud Applications REST API, Standard Lookups List of Values REST Endpoints, 26b, https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-standard-lookups-list-values.html | Confirms the read-only `GET /fscmRestApi/resources/11.13.18.05/standardLookupsLOV` collection route |
| Oracle Fusion Cloud Applications REST API, Get All Standard Lookups, 25d, https://docs.oracle.com/en/cloud/saas/applications-common/25d/farca/op-servername-fscmrestapi-resources-11.13.18.05-standardlookupslov-get.html | Confirms the `LookupType`, `LookupCode`, and translated `Meaning` response fields |
| Oracle Fusion Cloud SCM REST API, Create One Item Transaction Default, 26c, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/op-itemtransactiondefaults-post.html | Confirms `DefaultType` is the default-type code and `DefaultTypeMeaning` is the code meaning |
| Redwood UI source, `inventory-transactions-setup-ui` commit `ffeef64afea9fa606bba1b3fb1a1eed3f83e6abf`, `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/layout.json` and `extension1/sources/dynamicLayouts/self/itemDefaultsLayout/create-page.js` | Confirms the UI filters `standardLookupsLOV` with `LookupType='INV_ITEM_TXN_DEFAULTS_TYPE'`, renders `Meaning`, and submits `DefaultTypeMeaning` in its staged payload |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_default_type_meaning | DefaultType is supplied as a lookup code, DefaultTypeMeaning is supplied as a display value, or both must be compared | DefaultType, DefaultTypeMeaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='INV_ITEM_TXN_DEFAULTS_TYPE'&onlyData=true | LookupCode, Meaning | Trim outer whitespace and require exactly one case-insensitive exact match: match DefaultType to LookupCode when it is supplied, and DefaultTypeMeaning to Meaning when it is supplied. When both are supplied, they must resolve to the same LOV row. | DefaultTypeMeaning: Meaning; ResolvedDefaultTypeCode: LookupCode. Preserve a supplied DefaultType. | Zero or multiple matches, an inaccessible LOV, or inputs that resolve to different rows block Data Loader preparation. Do not fuzzy-match or select the first candidate. |

## Lookup Execution Rules

All invocations of `resolve_default_type_meaning` delegate the declared
read-only Fusion GET to `core.fusion-api.rest-api-client`. That core capability
owns OAuth, target identity, authorization handling, retry boundaries, and
redacted response transport. This resource supplies only the task-specific
path, query, fields, mapping, and match rule below; it must not provide direct
REST transport guidance.

| Situation | What Happens |
|---|---|
| DefaultType is supplied without DefaultTypeMeaning | Run the resolver, preserve DefaultType, and fill DefaultTypeMeaning with the matched LOV Meaning for the staged payload |
| DefaultTypeMeaning is supplied without DefaultType | Run the resolver and replace it with the matched LOV Meaning casing for the staged payload; record LookupCode as resolved output only |
| Both fields are supplied | Run the resolver and block unless both values match the same LOV row |
| LOV request fails | Stop with lookup readiness; do not infer a type or route to direct REST write guidance |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITD.RESOLVE_DEFAULT_TYPE_MEANING | decision | 20 | reference_lookup | resolved->ITD.CHECK_READINESS;not_required->ITD.CHECK_READINESS;blocked->ITD.HANDLE_ERROR;failure->ITD.HANDLE_ERROR | ITD.VALIDATE_INPUT | stop | Resolve a supplied DefaultType or DefaultTypeMeaning through the Item Transaction Defaults standard lookup when required |
