# Manage External Interface Web Service Details Input Validation

Source: Oracle, *Manage Connector Details Between Order Management and Your Fulfillment System* (25D).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Connector identity | Target System and Connector Name | Stop before Data Loader preparation | Provide the target system and a connector name that describes the intended connection | A connector is created or changed | |
| Target system mapping | TargetSystem resolved through resolve_target_system_id | Stop before Data Loader preparation | Provide the target system and map OrigSystemId to TargetSystemId and OrigSystem to TargetSystem | A connector is created or changed | resolve_target_system_id |
| Product or feature mapping | Optional Product Code or Product Name resolved through resolve_orchestration_application_id | Stop before Data Loader preparation | Supply an exact Product Code or Product Name from the developer-provided Orchestration Application mapping table; when omitted, default OrchestrationApplicationId to 10008 | A connector is created or changed | resolve_orchestration_application_id |
| Service location | Connector URL copied from the fulfillment service endpoint | Stop before Data Loader preparation | Obtain the endpoint URI from the service provider or Oracle Enterprise Manager as documented; Connector URL is optional when Invocation Mode is Business event | Invocation Mode is Synchronous Service or Asynchronous Service | |
| Credentials | CSF Key Passcode and CSF Key User, or a raw user name and password pair supplied for runtime use; never include raw credential values in a project artifact | Stop before Data Loader preparation | Provide one complete credential pair through the approved secure administration process | The service requires authentication | |
| Error response behavior | One response processing option, or an omitted value that defaults ResponseProcessPartialMode to ANY | Set ResponseProcessPartialMode to ANY | Choose Reject All Lines on First Error, Reject All Lines When Error on at Least One Line Occurs, or Reject Groups With Lines That Contain Errors to override the default | A connector is created or changed | |
| Response processing option mapping | ResponseProcessingOption resolved through resolve_response_processing_option | Stop before Data Loader preparation | Provide the response processing option and map LookupCode to ResponseProcessPartialMode and meaning to ResponseProcessingOption | ResponseProcessingOption is provided | resolve_response_processing_option |
| Invocation behavior | One invocation mode | Stop before Data Loader preparation | Choose Synchronous service, Asynchronous service, or Business event | A connector is created or changed | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Connector URL host | Require a URL for the fulfillment system service and reject an Oracle internal web service reference | Invocation Mode is Synchronous Service or Asynchronous Service | |
| Connector URL for Business event | Treat Connector URL as optional | Invocation Mode is Business event | |
| Product or feature | When supplied, require one exact Product Code or Product Name from the developer-provided Orchestration Application mapping table; when omitted, set OrchestrationApplicationId to 10008 | A connector is created or changed | resolve_orchestration_application_id |
| Existing connector update action | Require WebServiceId for the reconciled existing connector and set RestAction to PATCH; reject PUT or POST for an update | A change to an existing connector is requested | fetch_web_service_definitions |
| Credential pair | Require both CSF Key Passcode and CSF Key User, or both raw user name and password values; raw values are runtime-only and must not be persisted | The service requires authentication | |
| SOAP service model | Require the fulfillment service to host a synchronous SOAP web service when using the documented connector pattern | The connector uses the documented ConnectorServiceComposite pattern | |
| Invocation Mode: Business event | Allow Business event for the configured target system | Business event is selected | |
| Invocation Mode: Synchronous Service | Use only when Order Management must wait for the service response before it continues | Synchronous Service is selected | |
| Invocation Mode: Asynchronous Service | Use only when Order Management can continue while it waits for the response | Asynchronous Service is selected | |
| Send Attachments | Allow Yes only when sales-order attachments must be sent to the fulfillment system | Send Attachments is supplied | |
| Callback connector name | Require CallbackConnectorName to equal the configured Connector Name when a documented fulfillment-response or response service uses it | A callback service payload is configured | |
| Response processing default | Set ResponseProcessPartialMode to ANY without a ResponseProcessingOption value | ResponseProcessingOption is omitted | |
| Existing web service details | Obtain the current omWebServiceDefinitions response through fetch_web_service_definitions; stop before reconciliation or import preparation if the read is unavailable or ambiguous | Existing connector definitions must be reviewed or reconciled | fetch_web_service_definitions |
| Data Loader route | Use REST Data Loader preparation for the exact registered business object omWebServiceDefinitions; do not invent payload fields from this guide | Setup data import is requested | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_WEB_SERVICE.VALIDATE_CONNECTOR_DETAILS | step | 10 | validate_input | valid_details->OM_WEB_SERVICE.RESOLVE_TARGET_SYSTEM;invalid_details->RETURN_ISSUES | none | stop | Before resolving connector values, reading existing connector definitions, preparing a connector definition, or preparing a REST Data Loader import artifact. |
