# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| REST contract | The approved Add EPM Data Sources connector-definition contract: POST /api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions | Stop | Use the same approved endpoint and credential-free contract; do not substitute a route or method | Every request | |
| Connector configuration contract | Complete credential-free payload bound to the shared approved connector-definition contract | Stop | Validate supplied inputs against that approved contract | A configuration request is supplied | |
| Connector source type | One connector type: OCI or USER-DEFINED | Stop | Resolve the exact sourceTypeName and sourceTypeCode from the local connector-source-types registry | Every request | resolve_connector_source_type |
| OpenAPI extraction response schema | Every selected successful JSON response has a resolvable schema with at least one derivable leaf attribute | Stop | Correct the documentation-backed OpenAPI schema, then regenerate REST Operations before preview | Before approval-artifact preparation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| REST method and path | Accept only POST /api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions | Every request | |
| Configuration fields | Reject undocumented fields, credentials, and authentication details | A request contains configuration values | |
| Connector source type | Accept OCI only as sourceTypeName OCI with sourceTypeCode 2; accept USER-DEFINED only as sourceTypeName User-Defined with sourceTypeCode 10 | Every request | resolve_connector_source_type |
| OpenAPI response extraction readiness | Reject a successful JSON response with no schema, an object without documented properties, an array without items, unresolved or cyclic references, unsupported composition, or zero derivable leaf attributes | Before approval-artifact preparation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The connector-definition operation is not the approved shared POST contract | Blocked | Restore the approved method and path; do not substitute a route or schema | |
| Shared Risk Cloud authentication properties or rmc_scope are unavailable or inconsistent with the target environment | Blocked | Restore the approved Add EPM Data Sources authentication binding before preview or execution | |
| A credential-bearing field or undocumented payload field is supplied | Blocked | Remove the prohibited value and rebuild the credential-free payload | |
| The connector type is absent or is not OCI or USER-DEFINED | Blocked | Request one supported connector type; do not accept a task-local source type name or code | resolve_connector_source_type |
| The OpenAPI response schema is not extraction-ready | Blocked | Correct the source-backed OpenAPI schema and regenerate the REST-operation contract; do not create an approval artifact | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDS.VALIDATE_INPUT | step | 10 | validate_input | valid->CDS.VALIDATE_RESPONSE_SCHEMA;invalid->CDS.HANDLE_ISSUE | none | stop | Before configuration preview or task handoff |
| CDS.VALIDATE_RESPONSE_SCHEMA | step | 15 | validate_input | valid->CDS.RESOLVE_SOURCE_TYPE;invalid->CDS.HANDLE_ISSUE | CDS.VALIDATE_INPUT | stop | After OpenAPI generation and before REST-operation extraction or approval-artifact preparation |
