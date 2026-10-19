# Shipping Exceptions Reference Lookups

Source: Shipping Exceptions Redwood page, VBC service catalog, user-provided REST URL pattern, and approved resolver scope.

## Core REST Delegation

All live lookup nodes invoke `core.fusion-api.rest-api-client` against the configured Fusion environment with a read-only GET request. That core owns REST transport, `REST-Framework-Version: 9`, response handling, and the one cached-token 401 or 403 refresh boundary; it delegates OAuth acquisition and refresh to `core.auth.fusion-oauth-authentication`. No resolver creates, updates, deletes, imports, or submits data.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_shipping_exception_type_code | ExceptionType or ExceptionTypeCode is supplied | ExceptionType; ExceptionTypeCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_EXCEPTION_TYPE'&fields=Meaning,LookupCode&onlyData=true | Meaning; LookupCode | Trim outer whitespace and require exactly one case-insensitive exact Meaning or LookupCode match. When both are supplied, require that they identify the same row. | ExceptionTypeCode: LookupCode | Zero or multiple matches, including the current target's zero-row result, or conflicting inputs block preview. Never fuzzy-match or select the first row. |
| resolve_shipping_exception_severity_code | ExceptionSeverity or ExceptionSeverityCode is supplied | ExceptionSeverity; ExceptionSeverityCode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_EXCEPTION_BEHAVIOR'&fields=Meaning,LookupCode&onlyData=true | Meaning; LookupCode | Trim outer whitespace and require exactly one case-insensitive exact Meaning or LookupCode match. When both are supplied, require that they identify the same row. | ExceptionSeverityCode: LookupCode | Zero or multiple matches or conflicting inputs block preview. Never fuzzy-match or select the first row. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A display meaning or code resolves exactly once | Populate only the corresponding backend code field and retain the display meaning only in sanitized validation evidence. |
| A meaning and code both resolve to the same row | Retain the returned LookupCode as the backend field. |
| A lookup returns zero, multiple, or conflicting rows | Stop before preview or Data Loader handoff and request an exact supported meaning or matching code. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SE.RESOLVE_TYPE | step | 20 | reference_lookup | resolved->SE.RESOLVE_SEVERITY;not-applicable->SE.RESOLVE_SEVERITY;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SE.VALIDATE_INPUT | stop | Resolve supplied Type input to ExceptionTypeCode |
| SE.RESOLVE_SEVERITY | step | 30 | reference_lookup | resolved->SE.DONE;not-applicable->SE.DONE;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SE.RESOLVE_TYPE | stop | Resolve supplied Severity input to ExceptionSeverityCode |
