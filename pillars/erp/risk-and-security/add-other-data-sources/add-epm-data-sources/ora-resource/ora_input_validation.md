# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Connector selection | One connector_type: EPM ARCS or EPM FCCS; one non-empty connector_name | Stop | Request one exact supported type and connector name | Every request | |
| Seeded source type | EPM-ARCS for EPM ARCS; EPM-FCCS for EPM FCCS | Stop | Resolve the source type name from the parsed connector type | Before seeded-connector lookup | query_seeded_epm_connector_definition |
| BOSS read client | Target environment and BOSS OAuth configuration | Stop | Use core.fusion-api.rest-api-client with boss_scope | Before seeded-connector lookup | query_seeded_epm_connector_definition |
| OpenAPI extraction response schema | Every selected successful JSON response has a resolvable schema with at least one derivable leaf attribute | Stop | Correct the documentation-backed OpenAPI schema, then regenerate REST Operations before approval-artifact preparation | After seeded connector readiness and before approval-artifact preparation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| OpenAPI response extraction readiness | Reject a successful JSON response with no schema, an object without documented properties, an array without items, unresolved or cyclic references, unsupported composition, or zero derivable leaf attributes | Before approval-artifact preparation | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The prompt does not identify one supported connector type and connector name | Blocked | Request the missing or ambiguous value | |
| BOSS OAuth is unavailable | Blocked | Correct the shared BOSS OAuth configuration before the read-only query | query_seeded_epm_connector_definition |
| The OpenAPI response schema is not extraction-ready | Blocked | Correct the source-backed OpenAPI schema and regenerate the REST-operation contract; do not create an approval artifact | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPMDS.VALIDATE_INPUT | step | 10 | validate_input | valid->EPMDS.CHECK_DEPENDENCIES;invalid->EPMDS.HANDLE_ISSUE | none | stop | Before seeded-connector lookup |
| EPMDS.VALIDATE_RESPONSE_SCHEMA | step | 95 | validate_input | valid->EPMDS.OPENAPI_READY;invalid->EPMDS.HANDLE_OPENAPI_SCHEMA_ISSUE | EPMDS.SEEDED_READY | stop | After OpenAPI generation and before REST-operation extraction or approval-artifact preparation |
