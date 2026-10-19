# Manage External Interface Web Service Details Design Enforcement

Source: Oracle, *Manage Connector Details Between Order Management and Your Fulfillment System* (25D).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate connector details | Confirm the target system, connector name, response behavior, and invocation mode meet the documented contract; require Connector URL only for synchronous or asynchronous service invocation. |
| 2 | Reconcile current definitions | Review the read-only omWebServiceDefinitions response before preparing an update or deciding a new definition is required. |
| 3 | Validate service boundary | Confirm the fulfillment system hosts the service and no Oracle internal web service is referenced. |
| 4 | Validate invocation choice | Confirm the selected mode matches the documented response dependency or Business event use case. |
| 5 | Set existing-connector update action | Set RestAction to PATCH for every change to a reconciled existing connector. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A connector uses Synchronous Service or Asynchronous Service | Critical |  | The connector URL does not locate a fulfillment-system service, references an Oracle internal web service, or the documented synchronous SOAP service requirement is not met | Correct the service endpoint with the fulfillment-system provider before preparing import data | Yes |
| A connector uses Business event | Critical |  | The remaining connector contract is not satisfied | Leave Connector URL optional; validate the remaining connector contract | Yes |
| A connector is created or changed | Critical | resolve_orchestration_application_id | OrchestrationApplicationId is neither resolved from an exact Product Code or Product Name nor defaulted to 10008 when both are omitted | Use the developer-provided Orchestration Application mapping table for a supplied product or feature; otherwise use 10008 | No |
| An existing connector is changed | Critical | fetch_web_service_definitions | RestAction is not PATCH or the reconciled WebServiceId is missing | Set RestAction to PATCH and retain the exact WebServiceId before preparing the update archive | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_orchestration_application_id | A Product Code or Product Name is supplied for a connector | OrchestrationApplicationId | ora_reference_lookups.md |
| fetch_web_service_definitions | An existing connector is changed | WebServiceId and current connector details | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_WEB_SERVICE.ENFORCE_CONNECTOR_DESIGN | step | 22 | design_enforcement | design_valid->OM_WEB_SERVICE.GATE_REST_IMPORT;design_invalid->RETURN_ISSUES | OM_WEB_SERVICE.SET_UPDATE_REST_ACTION | stop | After current connector definitions are retrieved and the existing-connector update action is set when applicable, before preparing a REST Data Loader import. |
