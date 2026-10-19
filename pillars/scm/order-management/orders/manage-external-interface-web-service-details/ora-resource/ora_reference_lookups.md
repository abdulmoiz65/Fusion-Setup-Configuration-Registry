# Manage External Interface Web Service Details Reference Lookups

Source: developer-provided REST endpoints and Orchestration Application mapping table for target systems, response-processing options, web service definitions, and product or feature mapping.

## Local Lookups

Use the developer-provided Orchestration Application mapping table below as the authoritative task-context source. Match only an exact Product Code or Product Name; do not infer a partial or alternate product or feature value.

| Resolver | Runs When | Authoritative Source | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_orchestration_application_id | Product Code or Product Name is provided for a connector | Developer-provided Orchestration Application mapping table in this task resource | Require exactly one Product Code or Product Name equal to the supplied product or feature value | OrchestrationApplicationId from Orchestration Application Id | Stop before import preparation and request an exact Product Code or Product Name from the mapping table; do not select an arbitrary application. |

### Orchestration Application Mapping

| Orchestration Application Id | Product Code | Product Name |
|---|---|---|
| 1002 | DOS | Supply Chain Orchestration |
| 1003 | FOS | Financial Orchestration |
| 10008 | DOO | Order Management |
| 1007 | VCS | Supply Chain Collaboration |
| 67 | QP | Pricing |
| 708 | CZ | Configurator |

## Live Lookups

Use `core.fusion-api.rest-api-client` for this read-only GET request. Retain only sanitized validation evidence; do not use the response as a Data Loader import artifact or expose credentials.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_target_system_id | A target system is provided for a connector | Supplied TargetSystem | /fscmRestApi/resources/11.13.18.05/omSourceOrderSystemsLOV | OrigSystemId and OrigSystem | Require exactly one OrigSystem equal to the supplied TargetSystem; do not select an arbitrary record | TargetSystemId from OrigSystemId; TargetSystem from OrigSystem | Zero or multiple exact matches block preparation; a read failure stops and records a sanitized transport, auth/authz, or Fusion API diagnostic. |
| resolve_response_processing_option | A response processing option is provided for a connector | Supplied ResponseProcessingOption | /fscmRestApi/resources/11.13.18.05/standardLookups/ORA_DOO_RESPONSE_PROCESS_OPTNS/child/lookupCodes | LookupCode and meaning | Require exactly one meaning equal to the supplied ResponseProcessingOption; do not select an arbitrary record | ResponseProcessPartialMode from LookupCode; ResponseProcessingOption from meaning | Zero or multiple exact matches block preparation; a read failure stops and records a sanitized transport, auth/authz, or Fusion API diagnostic. |
| fetch_web_service_definitions | Existing web service details must be reviewed, reconciled, or validated | No request values | /fscmRestApi/resources/11.13.18.05/omWebServiceDefinitions | Web service-definition details returned by the resource | Return the current collection; when a specific definition is supplied, reconcile it by the task's supported identity in the response rather than selecting an arbitrary record | Sanitized existing web service-definition details for validation and reconciliation | An empty collection is a valid result with no existing definitions. An ambiguous requested identity blocks import preparation; a read failure stops and records a sanitized transport, auth/authz, or Fusion API diagnostic. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The target system lookup succeeds | Map OrigSystemId to TargetSystemId and OrigSystem to TargetSystem. |
| The target system lookup is zero-match or ambiguous | Stop before import preparation and request an exact target system; do not select an arbitrary source order system. |
| The response processing option lookup succeeds | Map LookupCode to ResponseProcessPartialMode and meaning to ResponseProcessingOption. |
| The response processing option is omitted | Do not run resolve_response_processing_option. Set ResponseProcessPartialMode to ANY through OM_WEB_SERVICE.DEFAULT_RESPONSE_PROCESSING_MODE. |
| The response processing option lookup is zero-match or ambiguous | Stop before import preparation and request an exact response processing option; do not select an arbitrary lookup code. |
| The product or feature mapping succeeds | Map Orchestration Application Id to OrchestrationApplicationId. |
| The product or feature is omitted | Do not run resolve_orchestration_application_id. Set OrchestrationApplicationId to 10008 through OM_WEB_SERVICE.DEFAULT_ORCHESTRATION_APPLICATION_ID. |
| The product or feature mapping is zero-match or ambiguous | Stop before import preparation and request an exact Product Code or Product Name from the mapping table. Do not select an arbitrary application. |
| The web service definition GET succeeds | Use the returned details only to validate or reconcile the intended connector definition before preparation or import. |
| The web service definition GET returns an empty collection | Treat it as no existing definition; continue only when the requested operation permits creating a new definition. |
| A supplied identity matches multiple definitions | Stop before import preparation and request an exact supported identity; do not choose an arbitrary definition. |
| The web service definition GET fails or is incomplete | Stop before import preparation and persist a sanitized diagnostic. Do not infer current state or substitute a stale response. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_WEB_SERVICE.RESOLVE_TARGET_SYSTEM | step | 12 | reference_lookup | resolved->OM_WEB_SERVICE.RESOLVE_RESPONSE_PROCESSING_OPTION;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | OM_WEB_SERVICE.VALIDATE_CONNECTOR_DETAILS | stop | Resolve the supplied TargetSystem through omSourceOrderSystemsLOV and map OrigSystemId to TargetSystemId and OrigSystem to TargetSystem. |
| OM_WEB_SERVICE.RESOLVE_RESPONSE_PROCESSING_OPTION | step | 14 | reference_lookup | resolved->OM_WEB_SERVICE.RESOLVE_ORCHESTRATION_APPLICATION_ID;not_applicable->OM_WEB_SERVICE.DEFAULT_RESPONSE_PROCESSING_MODE;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | OM_WEB_SERVICE.RESOLVE_TARGET_SYSTEM | stop | Resolve the supplied response processing option through ORA_DOO_RESPONSE_PROCESS_OPTNS lookup codes and map LookupCode to ResponseProcessPartialMode and meaning to ResponseProcessingOption. It is not applicable when no response processing option is supplied. |
| OM_WEB_SERVICE.RESOLVE_ORCHESTRATION_APPLICATION_ID | step | 17 | reference_lookup | resolved->OM_WEB_SERVICE.GET_WEB_SERVICE_DETAILS;not_applicable->OM_WEB_SERVICE.DEFAULT_ORCHESTRATION_APPLICATION_ID;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | OM_WEB_SERVICE.RESOLVE_TARGET_SYSTEM | stop | Resolve a supplied Product Code or Product Name through the developer-provided Orchestration Application mapping table and map Orchestration Application Id to OrchestrationApplicationId. It is not applicable when no product or feature is supplied. |
| OM_WEB_SERVICE.GET_WEB_SERVICE_DETAILS | step | 19 | reference_lookup | retrieved->OM_WEB_SERVICE.SET_UPDATE_REST_ACTION;empty->OM_WEB_SERVICE.SET_UPDATE_REST_ACTION;ambiguous->RETURN_ISSUES;failure->RETURN_ISSUES | none | stop | Existing web service details must be reviewed, reconciled, or validated through the omWebServiceDefinitions GET resource after response processing and OrchestrationApplicationId are resolved or defaulted. |
