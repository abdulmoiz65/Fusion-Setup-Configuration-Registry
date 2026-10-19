# Manage External Interface Web Service Details Defaulting Rules

Source: developer-provided defaults for an omitted response processing option, omitted product or feature, and existing-connector updates.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ResponseProcessPartialMode | ANY | ResponseProcessingOption is omitted | No | |
| OrchestrationApplicationId | 10008 | Product Code and Product Name are both omitted | No | resolve_orchestration_application_id |
| RestAction | PATCH | A change to an existing connector is requested after its identity is reconciled | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_WEB_SERVICE.DEFAULT_RESPONSE_PROCESSING_MODE | step | 16 | apply_default | defaulted->OM_WEB_SERVICE.RESOLVE_ORCHESTRATION_APPLICATION_ID | OM_WEB_SERVICE.RESOLVE_RESPONSE_PROCESSING_OPTION | stop | ResponseProcessingOption is omitted after the target system resolves. |
| OM_WEB_SERVICE.DEFAULT_ORCHESTRATION_APPLICATION_ID | step | 18 | apply_default | defaulted->OM_WEB_SERVICE.GET_WEB_SERVICE_DETAILS | OM_WEB_SERVICE.RESOLVE_ORCHESTRATION_APPLICATION_ID | stop | Product Code and Product Name are both omitted after the target system resolves. |
| OM_WEB_SERVICE.SET_UPDATE_REST_ACTION | step | 20 | apply_default | patched->OM_WEB_SERVICE.ENFORCE_CONNECTOR_DESIGN;not_applicable->OM_WEB_SERVICE.ENFORCE_CONNECTOR_DESIGN | OM_WEB_SERVICE.GET_WEB_SERVICE_DETAILS | stop | A requested operation changes an existing connector that was reconciled by WebServiceId; set RestAction to PATCH. For a new connector, do not apply this default. |
