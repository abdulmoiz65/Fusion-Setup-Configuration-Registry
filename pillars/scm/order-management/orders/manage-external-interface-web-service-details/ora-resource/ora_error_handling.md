# Manage External Interface Web Service Details Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Target system, connector name, or invocation mode is missing, or Connector URL is missing for Synchronous Service or Asynchronous Service | Stop before Data Loader preparation and request the missing configuration decision. An omitted response processing option defaults ResponseProcessPartialMode to ANY. |
| Neither a complete CSF Key Passcode and CSF Key User pair nor a complete raw user name and password pair is supplied | Stop before Data Loader preparation and request one complete credential pair. Do not store, display, or persist raw credential values. |
| The connector URL references an Oracle internal service or does not identify a fulfillment-system service | Stop and correct the endpoint with the service provider; do not prepare an import artifact. This check does not apply when Invocation Mode is Business event and Connector URL is omitted. |
| The selected invocation mode conflicts with the documented scenario | Stop and select the appropriate synchronous, asynchronous, or Business event mode. |
| The target-system lookup returns zero or multiple exact OrigSystem matches | Stop before import preparation and request an exact target system. Do not select an arbitrary source order system. |
| A supplied response-processing-option lookup returns zero or multiple exact meaning matches | Stop before import preparation and request an exact response processing option. Do not select an arbitrary lookup code. An omitted option does not run this lookup and defaults ResponseProcessPartialMode to ANY. |
| A supplied Product Code or Product Name does not map to exactly one developer-provided Orchestration Application mapping-table row | Stop before import preparation and request an exact Product Code or Product Name. Do not select an arbitrary OrchestrationApplicationId. When both values are omitted, default OrchestrationApplicationId to 10008. |
| An update to an existing connector uses PUT, POST, or omits the reconciled WebServiceId | Stop before import preparation, set RestAction to PATCH, and retain the exact WebServiceId. Do not submit the invalid archive. |
| The omWebServiceDefinitions GET fails, is incomplete, or returns an ambiguous requested definition | Stop before import preparation; retain a sanitized diagnostic or request an exact supported identity. Do not infer current state. |
| REST Data Loader sample metadata, reviewed input, or approval is missing | Stop before import. Generate the omWebServiceDefinitions sample and follow the core.data-loader workflow. |
| A Data Loader import fails | Preserve the sanitized diagnostic and follow core.data-loader's error-handling and retry policy; do not retry a live import without its required controls. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required connector detail is missing or invalid | Correct the configuration values before import preparation. An omitted response processing option is handled by the ANY default. |
| Service contract | The endpoint, SOAP requirement, or certificate configuration does not meet the documented connector contract | Correct the integration contract with the fulfillment-system provider. |
| Design blocker | Invocation mode is inconsistent with the documented rules | Revise the invocation selection or integration design. |
| Fusion API | The read-only omWebServiceDefinitions GET cannot provide an unambiguous current definition | Resolve the transport, auth/authz, Fusion API, or identity issue before import preparation. |
| Target system mapping | omSourceOrderSystemsLOV cannot return exactly one OrigSystem for the supplied target system | Correct the target system and rerun the read-only lookup before import preparation. |
| Response processing mapping | ORA_DOO_RESPONSE_PROCESS_OPTNS lookup codes cannot return exactly one meaning for a supplied response processing option | Correct the response processing option and rerun the read-only lookup before import preparation. An omitted option defaults ResponseProcessPartialMode to ANY. |
| Orchestration application mapping | The developer-provided mapping table cannot return exactly one row for a supplied Product Code or Product Name | Correct the product or feature value before import preparation. When neither is supplied, use OrchestrationApplicationId 10008. |
| Existing connector update action | An existing connector update does not use PATCH with its reconciled WebServiceId | Correct RestAction to PATCH and rebuild the immutable archive before approval. |
| Approval blocker | A REST Data Loader import lacks a reviewed immutable input or required approval | Complete the core.data-loader approval workflow. |
| Process failed | Data Loader reports a failed import | Persist a sanitized diagnostic and use the prescribed recovery path. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or design blocker | The failed requirement, corrective action, and that no Fusion import was attempted. |
| Import failure | The sanitized Data Loader diagnostic, last known status, and approved next action; never credentials or secrets. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The connector contract, sample, review, or approval gate fails | Execute, retry, or bypass a REST Data Loader import. |
| Credentials are requested for an artifact or diagnostic | Store, display, or persist the user name, password, token, private key, or certificate material. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|
| OM_WEB_SERVICE.GATE_REST_IMPORT | step | 30 | execution_gate | approved_input->RETURN_SUCCESS;approval_or_input_missing->RETURN_ISSUES | OM_WEB_SERVICE.ENFORCE_CONNECTOR_DESIGN | stop | After the connector design passes and before any REST Data Loader import. |
| RETURN_SUCCESS | terminal | 40 | terminal | none | OM_WEB_SERVICE.GATE_REST_IMPORT | continue | The connector details are valid and the import gate is satisfied. |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | continue | A connector validation, design, or import gate fails. |
